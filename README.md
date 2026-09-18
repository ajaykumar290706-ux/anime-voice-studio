# 🌸 AI Anime Voice Studio

> **"Turn your words into anime-inspired voices."**
> A modern AI voice synthesis and multi-character audio drama studio featuring original anime vocal personalities, emotion modulation, and intelligent script reading.

![Python](https://img.shields.io/badge/Python-3.10%2B-ff69b4.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-8A2BE2.svg)
![TTS](https://img.shields.io/badge/TTS-ElevenLabs%20%2B%20Edge--TTS-ff758c.svg)
![AI](https://img.shields.io/badge/AI%20Analyzer-Groq%20LLaMA%203.3-c084fc.svg)

---

## ✨ Features

### 1. 🌸 Text → Voice
- **Custom Text Input**: Enter any dialogue, monologue, or greeting.
- **6 Original Anime Personalities**:
  - 🌸 **Kawaii**: Sweet, youthful, playful anime heroine.
  - ⚡ **Energetic**: High-tempo, enthusiastic, shonen protagonist vibe.
  - 🌙 **Calm**: Gentle, soothing, mature anime mentor/narrator.
  - 😈 **Villain**: Menacing, dramatic, dark antagonist timbre.
  - 🎀 **Shy**: Soft, hesitant, breathy moe personality.
  - 👑 **Confident**: Bold, charismatic, regal leader voice.
- **7 Expressive Emotions**: Happy, Excited, Sad, Angry, Calm, Surprised, Nervous.
- **Languages**: Japanese, English, or Japanese-English Mixed.
- **Direct Playback & Instant MP3 Download**.

### 2. 🎭 Emotion Voice Studio
- Tailored for high-impact dramatic dialogue (e.g., *"Kore wa watashi no saigo no chance!"*).
- **Fine-Grained Acoustic Controls**:
  - Voice Speed (0.75x to 1.5x)
  - Pitch (Low, Normal, High)
  - Emotion Intensity modulation
- Dynamic visual feedback, instant replay (`Generate Again`), and MP3 download.

### 3. 📖 AI Multi-Character Story Reader
- Paste full stories with dialogue and narration.
- **Intelligent Groq LLaMA 3.3 AI Analysis**:
  - Automatically identifies speakers and scenes.
  - Differentiates narration from character speech.
  - Casts distinct anime voices (e.g., Narrator → Calm, Character 1 → Kawaii, Character 2 → Energetic, Character 3 → Confident).
  - Optional Japanese dialogue translation and anime drama dialogue enhancement.
- **Scene-by-Scene Breakdown**:
  - Play or download each scene individually.
  - Customize voice assignments per scene before final generation.
- **Complete Audio Assembly**:
  - Combines all scenes into a continuous, cinematic audio drama.
  - Unified **Play Complete Story** and **Download Complete Story (MP3)** buttons.

---

## 🔊 Dual-Layer TTS Engine & Fallback

| Engine | Role | Configuration |
|---|---|---|
| **ElevenLabs API** | **Primary Engine** | Ultra-expressive neural anime voices with emotion stability tuning. Requires `ELEVENLABS_API_KEY`. |
| **Microsoft Edge-TTS** | **Automatic Fallback** | Zero-config, high-fidelity neural voices (`ja-JP-NanamiNeural`, `ja-JP-KeitaNeural`, `en-US-AnaNeural`, etc.) with real-time SSML pitch and tempo modulation. Runs out-of-the-box even without API keys! |

> 💡 **Zero-Crash Resilience**: If ElevenLabs or Groq keys are missing or experience rate limits, the studio seamlessly switches to Edge-TTS and local heuristic script parsing with clear UI indicators.

---

## 📁 Project Structure

```
anime_voice_studio/
│
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── README.md                   # Documentation and user guide
│
├── core/                       # Core backend processing
│   ├── __init__.py
│   ├── tts_engine.py           # Modular TTS (ElevenLabs + Edge-TTS fallback)
│   ├── groq_analyzer.py        # Groq LLaMA 3.3 story analysis & parser fallback
│   ├── audio_manager.py        # Audio concatenation and export
│   └── story_processor.py      # Scene batch orchestration
│
├── ui/                         # Presentation layer
│   ├── __init__.py
│   ├── theme.py                # Sakura glassmorphism CSS & animations
│   └── components.py           # Cards, audio players, badges, preset buttons
│
├── utils/                      # Configuration and presets
│   ├── __init__.py
│   └── config.py               # Voice maps, emotions, paths, and settings
│
├── output/                     # Generated audio storage
│
└── tests/                      # Automated test suite
    ├── test_tts.py
    └── test_story_processor.py
```

---

## 🚀 Quickstart Guide

### 1. Clone or Open the Workspace
Ensure you are in the project root directory:
```bash
cd kawai
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD)**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Requirements
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
Edit `.env` to include your keys:
```ini
GROQ_API_KEY=gsk_your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```
*(Note: You can also enter API keys directly into the sidebar at runtime without restarting the server!)*

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Tests

Run the test suite using `pytest`:
```bash
python -m pytest tests/ -v
```

---

## 📜 Legal & Originality Notice
All voices generated by this application are **original anime-inspired voices** achieved through harmonic acoustic shaping, prosody tuning, and neural pitch modulation. They are not clones or impersonations of real individuals or copyrighted characters.
