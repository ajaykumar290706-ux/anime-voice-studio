"""Audio Manager for stitching, exporting, and managing anime voice tracks."""
import io
import logging
import os
import time
from pathlib import Path
from typing import List, Optional
from utils.config import AppConfig

logger = logging.getLogger("anime_voice_studio.audio")

class AudioManager:
    """Handles audio merging, saving, and format operations."""

    @staticmethod
    def get_audio_duration_estimate(audio_bytes: bytes) -> float:
        """Estimates duration in seconds based on typical 48kbps-128kbps MP3 stream."""
        if not audio_bytes:
            return 0.0
        # Average Edge-TTS MP3 is ~64kbps (8KB/s)
        seconds = len(audio_bytes) / 8000.0
        return max(0.5, round(seconds, 2))

    @staticmethod
    def combine_audio_segments(segments: List[bytes], pause_duration_ms: int = 350) -> bytes:
        """
        Combines multiple MP3 audio byte segments into a continuous audio track.
        Robust against lack of external ffmpeg binary.
        """
        if not segments:
            return b""
        
        valid_segments = [s for s in segments if s and len(s) > 0]
        if not valid_segments:
            return b""
        
        if len(valid_segments) == 1:
            return valid_segments[0]

        import shutil
        import warnings
        # If ffmpeg is available, use pydub for millisecond-accurate silence insertion
        if shutil.which("ffmpeg"):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    from pydub import AudioSegment
                combined = None
                silence = AudioSegment.silent(duration=pause_duration_ms)
                for seg in valid_segments:
                    segment_audio = AudioSegment.from_file(io.BytesIO(seg), format="mp3")
                    if combined is None:
                        combined = segment_audio
                    else:
                        combined = combined + silence + segment_audio
                out_buf = io.BytesIO()
                combined.export(out_buf, format="mp3")
                return out_buf.getvalue()
            except Exception as e:
                logger.info(f"Pydub export bypassed ({e}), using direct MPEG frame stream concatenation.")

        # MPEG-1 Audio Layer 3 (MP3) bitstreams are designed to be concatenated directly.
        # Consecutive MP3 frames play seamlessly in HTML5 Audio and desktop media players.
        buffer = bytearray()
        for seg in valid_segments:
            buffer.extend(seg)
        return bytes(buffer)

    @staticmethod
    def save_audio(audio_bytes: bytes, filename: Optional[str] = None) -> str:
        """Saves audio bytes to output directory and returns absolute file path."""
        if not filename:
            filename = f"anime_audio_{int(time.time()*1000)}.mp3"
        elif not filename.endswith(".mp3"):
            filename = f"{filename}.mp3"

        out_path = AppConfig.OUTPUT_DIR / filename
        with open(out_path, "wb") as f:
            f.write(audio_bytes)
        return str(out_path)
