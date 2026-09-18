"""Modular Text-to-Speech Engine with ElevenLabs primary and Edge-TTS fallback."""
import asyncio
import io
import logging
import os
import time
from dataclasses import dataclass
from typing import Optional, Tuple
import edge_tts
from utils.config import AppConfig

logger = logging.getLogger("anime_voice_studio.tts")

@dataclass
class TTSResult:
    audio_bytes: bytes
    engine_used: str  # "ElevenLabs (Primary)" or "Edge-TTS (Fallback)"
    is_fallback: bool
    personality: str
    emotion: str
    language: str
    fallback_reason: Optional[str] = None
    duration_seconds: float = 0.0
    file_path: Optional[str] = None

class TTSEngine:
    """Orchestrates anime voice synthesis with primary ElevenLabs and resilient Edge-TTS fallback."""

    def __init__(self, elevenlabs_api_key: Optional[str] = None):
        self.elevenlabs_api_key = AppConfig.get_elevenlabs_api_key(elevenlabs_api_key)

    def set_elevenlabs_key(self, api_key: str):
        """Update ElevenLabs API key at runtime."""
        self.elevenlabs_api_key = api_key.strip() if api_key else ""

    def get_status(self) -> dict:
        """Returns status of TTS engines."""
        has_el = bool(self.elevenlabs_api_key)
        return {
            "elevenlabs_available": has_el,
            "primary_engine": "ElevenLabs" if has_el else "Edge-TTS",
            "fallback_available": True,
            "status_message": (
                "ElevenLabs Active (Primary)"
                if has_el
                else "Edge-TTS Active (Zero-config Fallback Mode)"
            )
        }

    def _calculate_edge_params(
        self,
        personality: str,
        emotion: str,
        language: str,
        speed: float = 1.0,
        pitch_option: str = "Normal"
    ) -> Tuple[str, str, str]:
        """Calculates exact voice, pitch string and rate string for Edge-TTS."""
        lang_map = AppConfig.EDGE_VOICE_MAP.get(language, AppConfig.EDGE_VOICE_MAP["Japanese"])
        preset = lang_map.get(personality, lang_map["🌸 Kawaii"])
        voice = preset["voice"]

        # Base pitch in Hz
        base_pitch_str = preset.get("base_pitch", "+0Hz").replace("Hz", "")
        base_pitch_val = int(base_pitch_str) if base_pitch_str.lstrip("+-").isdigit() else 0

        # Emotion pitch & rate delta
        emo_mod = AppConfig.EMOTION_MODIFIERS.get(emotion, {"pitch_delta": 0, "rate_delta": 0})
        emotion_pitch_delta = emo_mod.get("pitch_delta", 0)
        emotion_rate_delta = emo_mod.get("rate_delta", 0)

        # Pitch option delta
        pitch_option_delta = 0
        if pitch_option == "Low":
            pitch_option_delta = -18
        elif pitch_option == "High":
            pitch_option_delta = +20

        total_pitch = base_pitch_val + emotion_pitch_delta + pitch_option_delta
        pitch_str = f"{total_pitch:+d}Hz"

        # Rate calculation
        # Base rate in percent
        base_rate_str = preset.get("base_rate", "+0%").replace("%", "")
        base_rate_val = int(base_rate_str) if base_rate_str.lstrip("+-").isdigit() else 0

        # Speed factor from user (0.75x to 1.5x)
        speed_rate_val = int((speed - 1.0) * 100)

        total_rate = base_rate_val + emotion_rate_delta + speed_rate_val
        # Clamp to edge-tts limits
        total_rate = max(-50, min(100, total_rate))
        rate_str = f"{total_rate:+d}%"

        return voice, pitch_str, rate_str

    async def _synthesize_edge_tts(
        self,
        text: str,
        personality: str,
        emotion: str,
        language: str,
        speed: float = 1.0,
        pitch_option: str = "Normal"
    ) -> bytes:
        """Synthesize audio using Edge-TTS async communicator."""
        voice, pitch_str, rate_str = self._calculate_edge_params(
            personality=personality,
            emotion=emotion,
            language=language,
            speed=speed,
            pitch_option=pitch_option
        )

        communicate = edge_tts.Communicate(text=text, voice=voice, pitch=pitch_str, rate=rate_str)
        audio_stream = bytearray()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.extend(chunk["data"])

        if not audio_stream:
            raise RuntimeError("Edge-TTS returned empty audio stream.")

        return bytes(audio_stream)

    def _synthesize_elevenlabs(
        self,
        text: str,
        personality: str,
        emotion: str
    ) -> bytes:
        """Synthesize audio using ElevenLabs API."""
        if not self.elevenlabs_api_key:
            raise ValueError("ElevenLabs API key is missing.")

        from elevenlabs.client import ElevenLabs
        from elevenlabs import VoiceSettings

        client = ElevenLabs(api_key=self.elevenlabs_api_key)
        voice_id = AppConfig.ELEVENLABS_VOICE_MAP.get(
            personality,
            AppConfig.ELEVENLABS_VOICE_MAP["🌸 Kawaii"]
        )

        # Emotion-specific voice settings
        emo_settings = AppConfig.ELEVENLABS_EMOTION_SETTINGS.get(
            emotion,
            {"stability": 0.50, "similarity_boost": 0.80, "style": 0.40}
        )

        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(
                stability=emo_settings["stability"],
                similarity_boost=emo_settings["similarity_boost"],
                style=emo_settings["style"],
                use_speaker_boost=True
            )
        )

        audio_buffer = bytearray()
        for chunk in audio_generator:
            if chunk:
                audio_buffer.extend(chunk)

        if not audio_buffer:
            raise RuntimeError("ElevenLabs returned empty audio response.")

        return bytes(audio_buffer)

    def generate(
        self,
        text: str,
        personality: str = "🌸 Kawaii",
        emotion: str = "Happy",
        language: str = "Japanese",
        speed: float = 1.0,
        pitch_option: str = "Normal",
        force_engine: Optional[str] = None
    ) -> TTSResult:
        """
        Main entry point for generating speech.
        Automatically attempts ElevenLabs (if configured) and falls back to Edge-TTS.
        """
        clean_text = text.strip() if text else ""
        if not clean_text:
            raise ValueError("Text input cannot be empty.")

        if len(clean_text) > 4000:
            raise ValueError("Text input exceeds maximum limit of 4000 characters.")

        engine_to_use = force_engine or ("elevenlabs" if self.elevenlabs_api_key else "edge-tts")
        audio_bytes = b""
        engine_used_label = ""
        is_fallback = False
        fallback_reason = None

        if engine_to_use == "elevenlabs" and self.elevenlabs_api_key:
            try:
                audio_bytes = self._synthesize_elevenlabs(
                    text=clean_text,
                    personality=personality,
                    emotion=emotion
                )
                engine_used_label = "ElevenLabs (Primary)"
            except Exception as e:
                logger.warning(f"ElevenLabs synthesis failed: {e}. Falling back to Edge-TTS.")
                is_fallback = True
                fallback_reason = f"ElevenLabs API error: {str(e)}. Switched to high-fidelity Edge-TTS."
                # Run Edge-TTS fallback
                audio_bytes = asyncio.run(
                    self._synthesize_edge_tts(
                        text=clean_text,
                        personality=personality,
                        emotion=emotion,
                        language=language,
                        speed=speed,
                        pitch_option=pitch_option
                    )
                )
                engine_used_label = "Edge-TTS (Fallback)"
        else:
            if not self.elevenlabs_api_key and force_engine != "edge-tts":
                fallback_reason = "No ElevenLabs API key provided. Using Edge-TTS anime voice engine."
                is_fallback = True

            audio_bytes = asyncio.run(
                self._synthesize_edge_tts(
                    text=clean_text,
                    personality=personality,
                    emotion=emotion,
                    language=language,
                    speed=speed,
                    pitch_option=pitch_option
                )
            )
            engine_used_label = "Edge-TTS (Fallback)" if is_fallback else "Edge-TTS"

        # Estimate duration (approx 16-24 kbps mp3 ~= 3000 bytes per sec)
        duration_seconds = max(0.5, round(len(audio_bytes) / 3200.0, 1))

        # Save audio file to output directory
        filename = f"anime_voice_{int(time.time()*1000)}.mp3"
        output_path = AppConfig.OUTPUT_DIR / filename
        try:
            with open(output_path, "wb") as f:
                f.write(audio_bytes)
            file_path_str = str(output_path)
        except Exception:
            file_path_str = None

        return TTSResult(
            audio_bytes=audio_bytes,
            engine_used=engine_used_label,
            is_fallback=is_fallback,
            personality=personality,
            emotion=emotion,
            language=language,
            fallback_reason=fallback_reason,
            duration_seconds=duration_seconds,
            file_path=file_path_str
        )
