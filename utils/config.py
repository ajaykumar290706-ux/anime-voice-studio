"""Configuration settings and anime voice presets for AI Anime Voice Studio."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

class AppConfig:
    """Central configuration and preset provider for anime voice studio."""

    BASE_DIR = BASE_DIR
    OUTPUT_DIR = OUTPUT_DIR

    # Personality profiles
    PERSONALITIES = [
        "🌸 Kawaii",
        "⚡ Energetic",
        "🌙 Calm",
        "😈 Villain",
        "🎀 Shy",
        "👑 Confident"
    ]

    # Emotion profiles
    EMOTIONS = [
        "Happy",
        "Excited",
        "Sad",
        "Angry",
        "Calm",
        "Surprised",
        "Nervous"
    ]

    # Supported languages
    LANGUAGES = [
        "Japanese",
        "English",
        "Japanese-English Mixed"
    ]

    # Pitch presets
    PITCH_OPTIONS = ["Low", "Normal", "High"]

    # Edge TTS base voice mappings
    # ja-JP-NanamiNeural is female, ja-JP-KeitaNeural is male
    EDGE_VOICE_MAP = {
        "Japanese": {
            "🌸 Kawaii": {"voice": "ja-JP-NanamiNeural", "base_pitch": "+20Hz", "base_rate": "+10%"},
            "⚡ Energetic": {"voice": "ja-JP-NanamiNeural", "base_pitch": "+15Hz", "base_rate": "+25%"},
            "🌙 Calm": {"voice": "ja-JP-NanamiNeural", "base_pitch": "-5Hz", "base_rate": "-10%"},
            "😈 Villain": {"voice": "ja-JP-KeitaNeural", "base_pitch": "-25Hz", "base_rate": "-12%"},
            "🎀 Shy": {"voice": "ja-JP-NanamiNeural", "base_pitch": "+8Hz", "base_rate": "-18%"},
            "👑 Confident": {"voice": "ja-JP-KeitaNeural", "base_pitch": "+5Hz", "base_rate": "+5%"}
        },
        "English": {
            "🌸 Kawaii": {"voice": "en-US-AnaNeural", "base_pitch": "+20Hz", "base_rate": "+8%"},
            "⚡ Energetic": {"voice": "en-US-AvaNeural", "base_pitch": "+15Hz", "base_rate": "+20%"},
            "🌙 Calm": {"voice": "en-US-AriaNeural", "base_pitch": "-2Hz", "base_rate": "-8%"},
            "😈 Villain": {"voice": "en-US-ChristopherNeural", "base_pitch": "-22Hz", "base_rate": "-10%"},
            "🎀 Shy": {"voice": "en-US-AnaNeural", "base_pitch": "+5Hz", "base_rate": "-15%"},
            "👑 Confident": {"voice": "en-US-ChristopherNeural", "base_pitch": "+2Hz", "base_rate": "+5%"}
        },
        "Japanese-English Mixed": {
            "🌸 Kawaii": {"voice": "ja-JP-NanamiNeural", "base_pitch": "+18Hz", "base_rate": "+10%"},
            "⚡ Energetic": {"voice": "ja-JP-NanamiNeural", "base_pitch": "+15Hz", "base_rate": "+22%"},
            "🌙 Calm": {"voice": "ja-JP-NanamiNeural", "base_pitch": "-4Hz", "base_rate": "-10%"},
            "😈 Villain": {"voice": "ja-JP-KeitaNeural", "base_pitch": "-20Hz", "base_rate": "-10%"},
            "🎀 Shy": {"voice": "ja-JP-NanamiNeural", "base_pitch": "+6Hz", "base_rate": "-16%"},
            "👑 Confident": {"voice": "ja-JP-KeitaNeural", "base_pitch": "+4Hz", "base_rate": "+5%"}
        }
    }

    # Emotion modulation offsets for pitch and rate in Edge-TTS
    EMOTION_MODIFIERS = {
        "Happy": {"pitch_delta": 10, "rate_delta": 8},
        "Excited": {"pitch_delta": 18, "rate_delta": 18},
        "Sad": {"pitch_delta": -12, "rate_delta": -15},
        "Angry": {"pitch_delta": -8, "rate_delta": 12},
        "Calm": {"pitch_delta": -5, "rate_delta": -8},
        "Surprised": {"pitch_delta": 22, "rate_delta": 14},
        "Nervous": {"pitch_delta": 12, "rate_delta": -6}
    }

    # ElevenLabs voice preset ID mappings
    # Using official well-known public premade voice IDs
    ELEVENLABS_VOICE_MAP = {
        "🌸 Kawaii": "EXAVITQu4vr4xnSDxMaL",      # Bella (sweet, young)
        "⚡ Energetic": "AZnzlk1XvdvUeBnXmlld",   # Domi (bright, strong)
        "🌙 Calm": "21m00Tcm4TlvDq8ikWAM",        # Rachel (calm, narration)
        "😈 Villain": "TxGEqnHWrfWFTfGW9XjX",     # Josh (deep, menacing)
        "🎀 Shy": "MF3mGyEYCl7XYWbV9V6O",         # Elli (soft, gentle)
        "👑 Confident": "ErXwobaYiN019PkySvjV"     # Antoni (smooth, confident)
    }

    # ElevenLabs voice stability/similarity boost tuned per emotion
    ELEVENLABS_EMOTION_SETTINGS = {
        "Happy": {"stability": 0.45, "similarity_boost": 0.85, "style": 0.45},
        "Excited": {"stability": 0.30, "similarity_boost": 0.90, "style": 0.70},
        "Sad": {"stability": 0.65, "similarity_boost": 0.80, "style": 0.20},
        "Angry": {"stability": 0.35, "similarity_boost": 0.88, "style": 0.60},
        "Calm": {"stability": 0.75, "similarity_boost": 0.80, "style": 0.15},
        "Surprised": {"stability": 0.30, "similarity_boost": 0.85, "style": 0.65},
        "Nervous": {"stability": 0.40, "similarity_boost": 0.80, "style": 0.40}
    }

    @staticmethod
    def get_groq_api_key(override: str = None) -> str:
        """Fetch Groq API key from override or environment."""
        if override and override.strip():
            return override.strip()
        return os.getenv("GROQ_API_KEY", "").strip()

    @staticmethod
    def get_elevenlabs_api_key(override: str = None) -> str:
        """Fetch ElevenLabs API key from override or environment."""
        if override and override.strip():
            return override.strip()
        return os.getenv("ELEVENLABS_API_KEY", "").strip()

    @staticmethod
    def has_groq_key(override: str = None) -> bool:
        return bool(AppConfig.get_groq_api_key(override))

    @staticmethod
    def has_elevenlabs_key(override: str = None) -> bool:
        return bool(AppConfig.get_elevenlabs_api_key(override))
