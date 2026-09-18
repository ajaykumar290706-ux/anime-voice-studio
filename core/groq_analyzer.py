"""Story analyzer using Groq API with robust fallback heuristic segmentation."""
import json
import logging
import re
from typing import Dict, List, Any, Optional
from utils.config import AppConfig

logger = logging.getLogger("anime_voice_studio.analyzer")

class GroqStoryAnalyzer:
    """Analyzes stories into structured scenes, speaker attribution, and anime voice casting."""

    PERSONALITY_NORMALIZATION = {
        "kawaii": "🌸 Kawaii",
        "cute": "🌸 Kawaii",
        "sweet": "🌸 Kawaii",
        "energetic": "⚡ Energetic",
        "lively": "⚡ Energetic",
        "cheerful": "⚡ Energetic",
        "calm": "🌙 Calm",
        "gentle": "🌙 Calm",
        "narrator": "🌙 Calm",
        "villain": "😈 Villain",
        "dark": "😈 Villain",
        "evil": "😈 Villain",
        "shy": "🎀 Shy",
        "nervous": "🎀 Shy",
        "hesitant": "🎀 Shy",
        "confident": "👑 Confident",
        "bold": "👑 Confident",
        "leader": "👑 Confident"
    }

    EMOTION_NORMALIZATION = {
        "happy": "Happy",
        "joy": "Happy",
        "excited": "Excited",
        "hype": "Excited",
        "sad": "Sad",
        "sorrow": "Sad",
        "angry": "Angry",
        "furious": "Angry",
        "mad": "Angry",
        "calm": "Calm",
        "neutral": "Calm",
        "surprised": "Surprised",
        "shocked": "Surprised",
        "nervous": "Nervous",
        "anxious": "Nervous",
        "afraid": "Nervous"
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = AppConfig.get_groq_api_key(api_key)

    def set_api_key(self, api_key: str):
        """Set Groq API key dynamically."""
        self.api_key = api_key.strip() if api_key else ""

    def normalize_voice(self, voice_candidate: str) -> str:
        """Map any LLM voice string to one of the 6 canonical personalities."""
        if not voice_candidate:
            return "🌙 Calm"
        v_clean = voice_candidate.lower()
        for key, canonical in self.PERSONALITY_NORMALIZATION.items():
            if key in v_clean:
                return canonical
        for p in AppConfig.PERSONALITIES:
            if p.lower() in v_clean:
                return p
        return "🌸 Kawaii"

    def normalize_emotion(self, emotion_candidate: str) -> str:
        """Map any LLM emotion string to one of the 7 canonical emotions."""
        if not emotion_candidate:
            return "Calm"
        e_clean = emotion_candidate.lower()
        for key, canonical in self.EMOTION_NORMALIZATION.items():
            if key in e_clean:
                return canonical
        for emo in AppConfig.EMOTIONS:
            if emo.lower() in e_clean:
                return emo
        return "Calm"

    def analyze_story(
        self,
        story_text: str,
        translate_to_japanese: bool = False,
        enhance_dialogue: bool = False
    ) -> Dict[str, Any]:
        """
        Analyze story text into scenes.
        Uses Groq if API key is provided and valid, otherwise uses heuristic parser.
        """
        clean_text = story_text.strip() if story_text else ""
        if not clean_text:
            raise ValueError("Story text cannot be empty.")

        if self.api_key:
            try:
                return self._groq_analyze(clean_text, translate_to_japanese, enhance_dialogue)
            except Exception as e:
                logger.warning(f"Groq API call failed: {e}. Falling back to rule-based parser.")
                result = self._heuristic_analyze(clean_text)
                result["analyzer_used"] = "Local Heuristic Parser (Fallback)"
                result["fallback_notice"] = f"Groq API unavailable ({str(e)}). Used local intelligent parser."
                return result
        else:
            result = self._heuristic_analyze(clean_text)
            result["analyzer_used"] = "Local Heuristic Parser (Zero-config)"
            result["fallback_notice"] = "No Groq API key set. Used local intelligent speaker segmentation."
            return result

    def _groq_analyze(
        self,
        story_text: str,
        translate_to_japanese: bool,
        enhance_dialogue: bool
    ) -> Dict[str, Any]:
        """Execute Groq LLM extraction using JSON mode."""
        from groq import Groq

        client = Groq(api_key=self.api_key)

        prompt = f"""You are an anime audio director. Analyze this story/script and break it down into sequential scenes.
Divide into narration and character dialogue. Identify distinct speakers.
Assign an original anime personality to each speaker from:
- '🌸 Kawaii' (cute, sweet, playful, youthful)
- '⚡ Energetic' (hyped, enthusiastic, bold)
- '🌙 Calm' (gentle, steady, default for Narrator)
- '😈 Villain' (dramatic, mysterious, menacing)
- '🎀 Shy' (soft-spoken, reserved, hesitant)
- '👑 Confident' (heroic, charismatic, proud)

Assign an emotion to each line from: ['Happy', 'Excited', 'Sad', 'Angry', 'Calm', 'Surprised', 'Nervous'].

Requirements:
- If translate_to_japanese is TRUE: translate or adapt the spoken lines into natural anime Japanese (kanji/kana or romaji).
- If enhance_dialogue is TRUE: make the lines feel more evocative and dramatic like anime script dialogue.
- Maintain sequential order.

Translate to Japanese: {translate_to_japanese}
Enhance dialogue: {enhance_dialogue}

Input Story:
\"\"\"
{story_text}
\"\"\"

Return ONLY a valid JSON object matching this schema:
{{
  "title": "Story Title or Short Summary",
  "detected_characters": ["Narrator", "Character1", ...],
  "scenes": [
    {{
      "speaker": "Speaker Name",
      "text": "Exact text or translated dialogue to be voiced",
      "voice": "One of [🌸 Kawaii, ⚡ Energetic, 🌙 Calm, 😈 Villain, 🎀 Shy, 👑 Confident]",
      "emotion": "One of [Happy, Excited, Sad, Angry, Calm, Surprised, Nervous]"
    }}
  ]
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional anime audio drama casting director. Output only strict JSON."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=2048
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        # Validate and sanitize data
        scenes = data.get("scenes", [])
        if not isinstance(scenes, list) or not scenes:
            raise ValueError("Groq returned empty scene list.")

        sanitized_scenes = []
        characters = set()

        for idx, s in enumerate(scenes):
            speaker = str(s.get("speaker", f"Speaker {idx+1}")).strip()
            text = str(s.get("text", "")).strip()
            voice = self.normalize_voice(str(s.get("voice", "")))
            emotion = self.normalize_emotion(str(s.get("emotion", "")))

            if text:
                characters.add(speaker)
                sanitized_scenes.append({
                    "speaker": speaker,
                    "text": text,
                    "voice": voice,
                    "emotion": emotion
                })

        return {
            "title": data.get("title", "Anime Audio Drama"),
            "detected_characters": list(characters),
            "scenes": sanitized_scenes,
            "analyzer_used": "Groq AI (LLaMA 3.3)",
            "fallback_notice": None
        }

    def _heuristic_analyze(self, story_text: str) -> Dict[str, Any]:
        """
        Rule-based parser that segments narration and character dialogue.
        Provides a seamless zero-API experience.
        """
        lines = [line.strip() for line in story_text.splitlines() if line.strip()]
        scenes = []
        characters = set()

        # Rotation of anime voices for distinct characters
        character_voice_palette = [
            "🌸 Kawaii",
            "⚡ Energetic",
            "👑 Confident",
            "😈 Villain",
            "🎀 Shy",
            "🌙 Calm"
        ]
        assigned_voices = {}

        for line in lines:
            # Pattern 1: Speaker: Dialogue
            colon_match = re.match(r"^([A-Za-z0-9_\s\u3040-\u30ff\u4e00-\u9faf]+)[:：]\s*(.*)$", line)

            if colon_match:
                speaker = colon_match.group(1).strip()
                text = colon_match.group(2).strip().strip('"\'“”')
            else:
                # Pattern 2: Quoted dialogue without explicit speaker
                quote_match = re.search(r'["“](.+?)["”]', line)
                if quote_match:
                    speaker = "Character"
                    text = quote_match.group(1).strip()
                else:
                    speaker = "Narrator"
                    text = line.strip().strip('"\'“”')

            if not text:
                continue

            characters.add(speaker)

            # Assign voice
            is_narrator = "narrator" in speaker.lower()
            if is_narrator:
                voice = "🌙 Calm"
            else:
                if speaker not in assigned_voices:
                    palette_idx = len(assigned_voices) % len(character_voice_palette)
                    assigned_voices[speaker] = character_voice_palette[palette_idx]
                voice = assigned_voices[speaker]

            # Detect emotion heuristics
            if "!" in text and ("?" in text or "what" in text.lower() or "nani" in text.lower()):
                emotion = "Surprised"
            elif "!" in text:
                if any(w in text.lower() for w in ["hate", "die", "bastard", "kuso", "angry", "stop"]):
                    emotion = "Angry"
                else:
                    emotion = "Excited"
            elif "?" in text:
                emotion = "Surprised"
            elif "..." in text or any(w in text.lower() for w in ["gomen", "sorry", "sad", "tears", "goodbye"]):
                emotion = "Sad"
            elif any(w in text.lower() for w in ["scared", "nervous", "shaking", "ano"]):
                emotion = "Nervous"
            elif any(w in text.lower() for w in ["yay", "happy", "suki", "love", "smile"]):
                emotion = "Happy"
            else:
                emotion = "Calm"

            scenes.append({
                "speaker": speaker,
                "text": text,
                "voice": voice,
                "emotion": emotion
            })

        if not scenes:
            scenes = [{
                "speaker": "Narrator",
                "text": story_text.strip(),
                "voice": "🌙 Calm",
                "emotion": "Calm"
            }]

        return {
            "title": "Anime Audio Story",
            "detected_characters": list(characters) if characters else ["Narrator"],
            "scenes": scenes,
            "analyzer_used": "Local Heuristic Parser",
            "fallback_notice": None
        }
