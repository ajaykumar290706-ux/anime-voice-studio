"""Story Processor orchestrating scene analysis, multi-voice synthesis, and story assembly."""
import logging
from typing import Callable, Dict, List, Any, Optional
from core.tts_engine import TTSEngine, TTSResult
from core.groq_analyzer import GroqStoryAnalyzer
from core.audio_manager import AudioManager

logger = logging.getLogger("anime_voice_studio.story")

class StoryProcessor:
    """Coordinates parsing, casting, sequential audio generation, and full story audio compilation."""

    def __init__(
        self,
        tts_engine: Optional[TTSEngine] = None,
        analyzer: Optional[GroqStoryAnalyzer] = None
    ):
        self.tts_engine = tts_engine or TTSEngine()
        self.analyzer = analyzer or GroqStoryAnalyzer()

    def parse_story(
        self,
        story_text: str,
        translate_to_japanese: bool = False,
        enhance_dialogue: bool = False
    ) -> Dict[str, Any]:
        """Analyzes and casts story into structured scene metadata."""
        return self.analyzer.analyze_story(
            story_text=story_text,
            translate_to_japanese=translate_to_japanese,
            enhance_dialogue=enhance_dialogue
        )

    def generate_scene_audio(
        self,
        scene: Dict[str, Any],
        language: str = "Japanese",
        speed: float = 1.0,
        pitch_option: str = "Normal"
    ) -> TTSResult:
        """Synthesizes speech for a single story scene."""
        return self.tts_engine.generate(
            text=scene["text"],
            personality=scene.get("voice", "🌸 Kawaii"),
            emotion=scene.get("emotion", "Calm"),
            language=language,
            speed=speed,
            pitch_option=pitch_option
        )

    def process_and_synthesize_story(
        self,
        story_scenes: List[Dict[str, Any]],
        language: str = "Japanese",
        speed: float = 1.0,
        pitch_option: str = "Normal",
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Generates audio for every scene sequentially, then combines all into a complete audio drama.
        """
        if not story_scenes:
            raise ValueError("No scenes provided for generation.")

        processed_scenes = []
        audio_segments = []
        total_scenes = len(story_scenes)

        for idx, scene in enumerate(story_scenes):
            speaker = scene.get("speaker", f"Speaker {idx+1}")
            text = scene.get("text", "")
            voice = scene.get("voice", "🌸 Kawaii")
            emotion = scene.get("emotion", "Calm")

            if progress_callback:
                progress_callback(
                    idx + 1,
                    total_scenes,
                    f"Voicing Scene {idx+1}/{total_scenes}: {speaker} ({voice})"
                )

            # Generate scene audio
            tts_res = self.tts_engine.generate(
                text=text,
                personality=voice,
                emotion=emotion,
                language=language,
                speed=speed,
                pitch_option=pitch_option
            )

            audio_segments.append(tts_res.audio_bytes)
            processed_scenes.append({
                "scene_id": idx + 1,
                "speaker": speaker,
                "text": text,
                "voice": voice,
                "emotion": emotion,
                "audio_bytes": tts_res.audio_bytes,
                "duration_seconds": tts_res.duration_seconds,
                "engine_used": tts_res.engine_used,
                "is_fallback": tts_res.is_fallback,
                "file_path": tts_res.file_path
            })

        if progress_callback:
            progress_callback(total_scenes, total_scenes, "Merging scenes into complete story audio...")

        # Combine all audio segments
        complete_audio = AudioManager.combine_audio_segments(audio_segments)
        total_duration = sum(s["duration_seconds"] for s in processed_scenes)

        complete_file_path = AudioManager.save_audio(complete_audio, f"complete_story_{len(processed_scenes)}_scenes")

        return {
            "scenes": processed_scenes,
            "complete_audio_bytes": complete_audio,
            "complete_duration_seconds": round(total_duration, 1),
            "complete_file_path": complete_file_path,
            "total_scenes": total_scenes
        }
