"""Tests for TTSEngine and Edge-TTS synthesis."""
import pytest
from core.tts_engine import TTSEngine, TTSResult
from utils.config import AppConfig

def test_tts_engine_init():
    """Verify engine initializes with zero-config fallback."""
    engine = TTSEngine(elevenlabs_api_key="")
    status = engine.get_status()
    assert status["elevenlabs_available"] is False
    assert status["fallback_available"] is True
    assert "Edge-TTS" in status["primary_engine"]

def test_edge_params_calculation():
    """Verify pitch and speed calculations produce expected SSML parameter offsets."""
    engine = TTSEngine()
    voice, pitch_str, rate_str = engine._calculate_edge_params(
        personality="🌸 Kawaii",
        emotion="Excited",
        language="Japanese",
        speed=1.2,
        pitch_option="High"
    )
    assert "NanamiNeural" in voice
    assert pitch_str.startswith("+") and pitch_str.endswith("Hz")
    assert rate_str.startswith("+") and rate_str.endswith("%")

def test_empty_input_validation():
    """Verify empty text raises ValueError."""
    engine = TTSEngine()
    with pytest.raises(ValueError, match="empty"):
        engine.generate("")

    with pytest.raises(ValueError, match="empty"):
        engine.generate("   ")

def test_long_input_validation():
    """Verify excessively long text is rejected."""
    engine = TTSEngine()
    with pytest.raises(ValueError, match="maximum limit"):
        engine.generate("A" * 4001)

def test_edge_tts_speech_generation():
    """Verify real audio bytes generation via Edge-TTS."""
    engine = TTSEngine()
    result = engine.generate(
        text="Konnichiwa!",
        personality="🌸 Kawaii",
        emotion="Happy",
        language="Japanese"
    )
    assert isinstance(result, TTSResult)
    assert len(result.audio_bytes) > 1000
    assert result.duration_seconds > 0
    assert "Edge-TTS" in result.engine_used

def test_elevenlabs_fallback_on_invalid_key():
    """Verify invalid ElevenLabs key gracefully falls back to Edge-TTS without crashing."""
    engine = TTSEngine(elevenlabs_api_key="invalid_fake_key_123")
    result = engine.generate(
        text="Testing fallback resilience.",
        personality="⚡ Energetic",
        emotion="Excited",
        language="English"
    )
    assert isinstance(result, TTSResult)
    assert result.is_fallback is True
    assert "Edge-TTS" in result.engine_used
    assert len(result.audio_bytes) > 1000
