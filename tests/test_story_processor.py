"""Tests for GroqStoryAnalyzer, StoryProcessor, and AudioManager."""
import pytest
from core.groq_analyzer import GroqStoryAnalyzer
from core.story_processor import StoryProcessor
from core.audio_manager import AudioManager

def test_heuristic_story_parsing():
    """Verify offline rule-based parser segments multi-character dialogue correctly."""
    analyzer = GroqStoryAnalyzer(api_key="")
    story = (
        "Narrator: The sun was setting over the city.\n"
        "Mika: \"We need to leave now!\"\n"
        "Ren: \"Wait! I forgot my bag.\"\n"
        "Mika: \"Seriously?!\""
    )
    result = analyzer.analyze_story(story)
    assert "scenes" in result
    scenes = result["scenes"]
    assert len(scenes) == 4
    assert scenes[0]["speaker"] == "Narrator"
    assert scenes[0]["voice"] == "🌙 Calm"
    assert scenes[1]["speaker"] == "Mika"
    assert scenes[2]["speaker"] == "Ren"
    assert scenes[3]["speaker"] == "Mika"

def test_empty_story_error():
    """Verify empty story input raises ValueError."""
    analyzer = GroqStoryAnalyzer(api_key="")
    with pytest.raises(ValueError, match="empty"):
        analyzer.analyze_story("   ")

def test_voice_normalization():
    """Verify arbitrary LLM strings normalize to canonical presets."""
    analyzer = GroqStoryAnalyzer()
    assert analyzer.normalize_voice("super kawaii anime girl") == "🌸 Kawaii"
    assert analyzer.normalize_voice("dark evil villain") == "😈 Villain"
    assert analyzer.normalize_voice("quiet shy girl") == "🎀 Shy"
    assert analyzer.normalize_voice("unknown string") == "🌸 Kawaii"

def test_emotion_normalization():
    """Verify arbitrary emotion strings normalize to canonical emotions."""
    analyzer = GroqStoryAnalyzer()
    assert analyzer.normalize_emotion("joyful") == "Happy"
    assert analyzer.normalize_emotion("furious and raging") == "Angry"
    assert analyzer.normalize_emotion("anxious") == "Nervous"

def test_audio_manager_combination():
    """Verify AudioManager correctly stitches multiple byte segments."""
    fake_chunk_1 = b"ID3_AUDIO_CHUNK_1"
    fake_chunk_2 = b"ID3_AUDIO_CHUNK_2"
    combined = AudioManager.combine_audio_segments([fake_chunk_1, fake_chunk_2])
    assert fake_chunk_1 in combined
    assert fake_chunk_2 in combined
    assert len(combined) == len(fake_chunk_1) + len(fake_chunk_2)

def test_audio_manager_empty_and_single():
    """Verify AudioManager handles edge cases."""
    assert AudioManager.combine_audio_segments([]) == b""
    assert AudioManager.combine_audio_segments([b""]) == b""
    single = b"SINGLE_SAMPLE"
    assert AudioManager.combine_audio_segments([single]) == single
