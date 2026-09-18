"""🌸 AI Anime Voice Studio - Web Application
Turn your words into original anime-inspired voices.
"""
import io
import os
import streamlit as st

# Page setup
st.set_page_config(
    page_title="🌸 AI Anime Voice Studio",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.config import AppConfig
from core.tts_engine import TTSEngine, TTSResult
from core.groq_analyzer import GroqStoryAnalyzer
from core.audio_manager import AudioManager
from core.story_processor import StoryProcessor
from ui.theme import inject_sakura_theme
from ui.components import (
    render_header,
    render_status_badge,
    render_audio_card,
    render_scene_card,
    render_preset_dialogue_buttons
)

# Apply Sakura glassmorphism styling
inject_sakura_theme()

# Initialize session state for persistent results and inputs
if "groq_key_override" not in st.session_state:
    st.session_state["groq_key_override"] = os.getenv("GROQ_API_KEY", "")

if "elevenlabs_key_override" not in st.session_state:
    st.session_state["elevenlabs_key_override"] = os.getenv("ELEVENLABS_API_KEY", "")

if "t2v_result" not in st.session_state:
    st.session_state["t2v_result"] = None

if "t2v_text" not in st.session_state:
    st.session_state["t2v_text"] = "Konnichiwa! Welcome to the AI Anime Voice Studio. Let's create something magical together!"

if "emotion_result" not in st.session_state:
    st.session_state["emotion_result"] = None

if "emotion_text" not in st.session_state:
    st.session_state["emotion_text"] = "Kore wa watashi no saigo no chance!"

if "story_input" not in st.session_state:
    st.session_state["story_input"] = (
        "Narrator: The sun was setting over Neo Tokyo.\n"
        "Mika: \"We need to leave now!\"\n"
        "Ren: \"Wait! I forgot my magical crystal bag!\"\n"
        "Mika: \"Seriously?! Every single mission...\"\n"
        "Narrator: And so, their twilight sprint began."
    )

if "parsed_story" not in st.session_state:
    st.session_state["parsed_story"] = None

if "story_audio_result" not in st.session_state:
    st.session_state["story_audio_result"] = None

# Instantiate core engines with active session keys
tts_engine = TTSEngine(elevenlabs_api_key=st.session_state["elevenlabs_key_override"])
analyzer = GroqStoryAnalyzer(api_key=st.session_state["groq_key_override"])
story_processor = StoryProcessor(tts_engine=tts_engine, analyzer=analyzer)

# ==========================================
# SIDEBAR: Status, Keys & Global Settings
# ==========================================
with st.sidebar:
    st.markdown("### 🌸 Studio Hub")
    st.caption("AI Anime Voice Studio v2.0")
    
    st.markdown("---")
    st.markdown("#### ⚡ System & Engine Status")

    has_groq = AppConfig.has_groq_key(st.session_state["groq_key_override"])
    has_el = AppConfig.has_elevenlabs_key(st.session_state["elevenlabs_key_override"])

    tts_status = tts_engine.get_status()

    # Engine status pill
    if tts_status["elevenlabs_available"]:
        st.markdown(
            '<span class="status-pill status-pill-ok">● ElevenLabs Active (Primary)</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="status-pill status-pill-info">● Edge-TTS Active (Zero-Config)</span>',
            unsafe_allow_html=True
        )

    # Groq status pill
    if has_groq:
        st.markdown(
            '<span class="status-pill status-pill-ok">● Groq AI Analyzer Active</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="status-pill status-pill-info">● Local Story Parser Active</span>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("#### 🔑 API Keys (Optional)")
    st.caption("Enter keys below or store in `.env`. The app functions immediately with Edge-TTS even without keys!")

    el_key_input = st.text_input(
        "ElevenLabs API Key",
        value=st.session_state["elevenlabs_key_override"],
        type="password",
        help="Optional: Enables ultra-expressive ElevenLabs anime voices."
    )
    if el_key_input != st.session_state["elevenlabs_key_override"]:
        st.session_state["elevenlabs_key_override"] = el_key_input
        st.rerun()

    groq_key_input = st.text_input(
        "Groq API Key",
        value=st.session_state["groq_key_override"],
        type="password",
        help="Optional: Enables LLaMA 3.3 for smart story script parsing."
    )
    if groq_key_input != st.session_state["groq_key_override"]:
        st.session_state["groq_key_override"] = groq_key_input
        st.rerun()

    st.markdown("---")
    st.markdown("#### ⚙️ Global Audio Settings")

    global_speed = st.slider(
        "Default Voice Speed",
        min_value=0.75,
        max_value=1.50,
        value=1.00,
        step=0.05,
        help="Controls overall speech tempo across synthesis."
    )

    global_pitch = st.select_slider(
        "Default Pitch",
        options=AppConfig.PITCH_OPTIONS,
        value="Normal",
        help="Adjusts harmonic vocal pitch."
    )

    global_language = st.selectbox(
        "Default Language",
        options=AppConfig.LANGUAGES,
        index=0,
        help="Target language pronunciation."
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size: 0.78rem; color: #94A3B8; text-align: center; line-height: 1.5;">
            🌸 <b>AI Anime Voice Studio</b><br>
            Powered by Edge-TTS & ElevenLabs<br>
            Designed with Sakura Glassmorphism
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# MAIN CONTENT HEADER
# ==========================================
render_header()

# Render status banner if in fallback mode
if not tts_status["elevenlabs_available"]:
    render_status_badge(
        engine_label="Microsoft Edge-TTS (Anime Neural)",
        is_fallback=True,
        fallback_reason="No ElevenLabs key detected. Running in seamless zero-config anime neural fallback mode."
    )

# ==========================================
# MAIN TABS
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "🌸 Text → Voice",
    "🎭 Emotion Voice",
    "📖 Story Reader"
])

# ------------------------------------------
# TAB 1: TEXT → VOICE
# ------------------------------------------
with tab1:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #FF8DA1; display: flex; align-items: center; gap: 8px;">
                <span>🌸</span> Text → Voice Synthesizer
            </h3>
            <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 16px;">
                Type or paste any dialogue, choose an original anime personality, and generate expressive voice audio.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Preset helpers
    def set_t2v_text(txt):
        st.session_state["t2v_text"] = txt

    render_preset_dialogue_buttons(set_t2v_text)

    # Text Input Box
    t2v_input_text = st.text_area(
        "Enter text to voice:",
        value=st.session_state["t2v_text"],
        height=140,
        placeholder="Enter custom anime lines, dialogue, or greeting...",
        key="t2v_textarea"
    )

    # Controls Row
    c1, c2, c3 = st.columns(3)
    with c1:
        selected_personality = st.selectbox(
            "Anime Personality:",
            options=AppConfig.PERSONALITIES,
            index=0,
            help="Select character vocal personality.",
            key="t2v_personality"
        )
    with c2:
        selected_emotion = st.selectbox(
            "Emotion:",
            options=AppConfig.EMOTIONS,
            index=0,
            help="Select voice emotional delivery.",
            key="t2v_emotion"
        )
    with c3:
        selected_lang = st.selectbox(
            "Language:",
            options=AppConfig.LANGUAGES,
            index=AppConfig.LANGUAGES.index(global_language) if global_language in AppConfig.LANGUAGES else 0,
            key="t2v_lang"
        )

    col_btn, col_info = st.columns([2, 3])
    with col_btn:
        generate_t2v_btn = st.button("✨ Generate Voice", key="btn_t2v_generate")

    if generate_t2v_btn:
        clean_text = t2v_input_text.strip()
        if not clean_text:
            st.error("⚠️ Please enter some text before generating voice.")
        else:
            with st.spinner(f"Synthesizing {selected_personality} voice..."):
                try:
                    result = tts_engine.generate(
                        text=clean_text,
                        personality=selected_personality,
                        emotion=selected_emotion,
                        language=selected_lang,
                        speed=global_speed,
                        pitch_option=global_pitch
                    )
                    st.session_state["t2v_result"] = result
                    st.success("🎉 Anime voice generated successfully!")
                except Exception as e:
                    st.error(f"❌ Voice synthesis error: {str(e)}")

    # Display Result
    if st.session_state["t2v_result"]:
        res: TTSResult = st.session_state["t2v_result"]
        render_audio_card(
            audio_bytes=res.audio_bytes,
            personality=res.personality,
            emotion=res.emotion,
            language=res.language,
            engine_label=res.engine_used,
            duration_seconds=res.duration_seconds,
            download_filename=f"anime_{res.personality.replace(' ', '_').lower()}.mp3",
            key_prefix="t2v"
        )

# ------------------------------------------
# TAB 2: EMOTION VOICE
# ------------------------------------------
with tab2:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #C084FC; display: flex; align-items: center; gap: 8px;">
                <span>🎭</span> Emotion Voice Studio
            </h3>
            <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 16px;">
                Fine-tune high-intensity emotional vocal expressions with precise pitch, tempo, and dramatic resonance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    emo_text_input = st.text_area(
        "Enter expressive dialogue:",
        value=st.session_state["emotion_text"],
        height=100,
        placeholder='e.g., "Kore wa watashi no saigo no chance!" or "I will never forgive you!"',
        key="emotion_textarea"
    )

    # Sliders and selectors
    e_col1, e_col2, e_col3 = st.columns(3)
    with e_col1:
        emo_personality = st.selectbox(
            "Personality:",
            options=AppConfig.PERSONALITIES,
            index=1,  # Energetic default for emotion
            key="emo_personality_select"
        )
    with e_col2:
        emo_emotion = st.selectbox(
            "Emotion:",
            options=AppConfig.EMOTIONS,
            index=1,  # Excited default
            key="emo_emotion_select"
        )
    with e_col3:
        emo_language = st.selectbox(
            "Language:",
            options=AppConfig.LANGUAGES,
            index=0,
            key="emo_lang_select"
        )

    # Advanced Pitch & Speed tuning
    t_col1, t_col2 = st.columns(2)
    with t_col1:
        emo_speed = st.slider(
            "Voice Speed (0.75x – 1.5x):",
            min_value=0.75,
            max_value=1.50,
            value=float(global_speed),
            step=0.05,
            key="emo_speed_slider"
        )
    with t_col2:
        emo_pitch = st.select_slider(
            "Voice Pitch:",
            options=AppConfig.PITCH_OPTIONS,
            value=global_pitch,
            key="emo_pitch_slider"
        )

    b_col1, b_col2 = st.columns([2, 2])
    with b_col1:
        generate_emo_btn = st.button("🎭 Generate Emotion Voice", key="btn_emo_generate")
    with b_col2:
        if st.session_state["emotion_result"]:
            regen_emo_btn = st.button("🔄 Generate Again", key="btn_emo_again")
        else:
            regen_emo_btn = False

    if generate_emo_btn or regen_emo_btn:
        clean_text = emo_text_input.strip()
        if not clean_text:
            st.error("⚠️ Please enter expressive dialogue before generating.")
        else:
            with st.spinner(f"Generating expressive {emo_emotion} {emo_personality} voice..."):
                try:
                    res = tts_engine.generate(
                        text=clean_text,
                        personality=emo_personality,
                        emotion=emo_emotion,
                        language=emo_language,
                        speed=emo_speed,
                        pitch_option=emo_pitch
                    )
                    st.session_state["emotion_result"] = res
                    st.success(f"🎉 Expressive {emo_emotion} dialogue generated!")
                except Exception as e:
                    st.error(f"❌ Emotion generation error: {str(e)}")

    # Display Emotion Audio Player & Card
    if st.session_state["emotion_result"]:
        res: TTSResult = st.session_state["emotion_result"]
        render_audio_card(
            audio_bytes=res.audio_bytes,
            personality=res.personality,
            emotion=res.emotion,
            language=res.language,
            engine_label=res.engine_used,
            duration_seconds=res.duration_seconds,
            download_filename=f"emotion_{res.emotion.lower()}_{res.personality.replace(' ', '_').lower()}.mp3",
            key_prefix="emo"
        )

# ------------------------------------------
# TAB 3: STORY READER
# ------------------------------------------
with tab3:
    st.markdown(
        """
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #F472B6; display: flex; align-items: center; gap: 8px;">
                <span>📖</span> AI Multi-Character Story Reader
            </h3>
            <p style="color: #CBD5E1; font-size: 0.95rem; margin-bottom: 12px;">
                Paste any multi-character anime story or script. AI automatically segments narration, detects distinct speakers, casts unique original anime voices, generates each scene, and stitches them into a full audio drama!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sample story loader buttons
    story_preset_cols = st.columns(3)
    if story_preset_cols[0].button("📜 Sample: Neo Tokyo Crystal", key="story_preset_1"):
        st.session_state["story_input"] = (
            "Narrator: The sun was setting over Neo Tokyo.\n"
            "Mika: \"We need to leave now!\"\n"
            "Ren: \"Wait! I forgot my magical crystal bag!\"\n"
            "Mika: \"Seriously?! Every single mission...\"\n"
            "Ren: \"I found it! Let's save the universe!\"\n"
            "Narrator: And so, their twilight sprint began."
        )
        st.session_state["parsed_story"] = None
        st.session_state["story_audio_result"] = None
        st.rerun()

    if story_preset_cols[1].button("📜 Sample: Academy Showdown", key="story_preset_2"):
        st.session_state["story_input"] = (
            "Narrator: The bell chimed across the mystical academy courtyard.\n"
            "Kaito: \"You think your dark spells can pierce my shield, Malakor?\"\n"
            "Malakor: \"Foolish boy! You haven't seen true shadow power yet!\"\n"
            "Yuki: \"A-Ano... please stop fighting! Both of you!\"\n"
            "Kaito: \"Stay back, Yuki! I will protect this academy!\"\n"
            "Narrator: Tension crackled like lightning in the air."
        )
        st.session_state["parsed_story"] = None
        st.session_state["story_audio_result"] = None
        st.rerun()

    if story_preset_cols[2].button("📜 Sample: Cherry Blossom Promise", key="story_preset_3"):
        st.session_state["story_input"] = (
            "Narrator: Gentle cherry blossom petals danced on the spring breeze.\n"
            "Hana: \"Do you think we will still be friends ten years from today?\"\n"
            "Sora: \"Of course! No matter what universe we end up in!\"\n"
            "Hana: \"Yay! That's a pinky promise!\"\n"
            "Narrator: Their laughter echoed softly into the blooming afternoon."
        )
        st.session_state["parsed_story"] = None
        st.session_state["story_audio_result"] = None
        st.rerun()

    story_text = st.text_area(
        "Paste your story or script here:",
        value=st.session_state["story_input"],
        height=180,
        placeholder="Narrator: ...\nCharacter 1: ...\nCharacter 2: ...",
        key="story_textarea"
    )

    opt_col1, opt_col2, opt_col3 = st.columns(3)
    with opt_col1:
        story_lang = st.selectbox(
            "Story Audio Language:",
            options=AppConfig.LANGUAGES,
            index=1,  # English default for pasted English stories
            key="story_lang_select"
        )
    with opt_col2:
        translate_ja = st.checkbox(
            "🌸 Translate Dialogue to Japanese (Groq AI)",
            value=False,
            help="Translates character dialogue into anime Japanese phrasing."
        )
    with opt_col3:
        enhance_dialogue = st.checkbox(
            "✨ Enhance Dialogue Dramatics (Groq AI)",
            value=False,
            help="Polishes dialogue to feel more cinematic and anime-styled."
        )

    # Step 1: Analyze Story
    btn_col1, btn_col2 = st.columns([2, 3])
    with btn_col1:
        analyze_btn = st.button("🔍 Step 1: Analyze Story & Cast Voices", key="btn_analyze_story")

    if analyze_btn:
        clean_story = story_text.strip()
        if not clean_story:
            st.error("⚠️ Please paste a story first.")
        else:
            with st.spinner("Analyzing story structure, speakers, and assigning anime voices..."):
                try:
                    parsed = story_processor.parse_story(
                        story_text=clean_story,
                        translate_to_japanese=translate_ja,
                        enhance_dialogue=enhance_dialogue
                    )
                    st.session_state["parsed_story"] = parsed
                    st.session_state["story_audio_result"] = None
                    st.success(f"✨ Story parsed into {len(parsed['scenes'])} scenes using {parsed['analyzer_used']}!")
                except Exception as e:
                    st.error(f"❌ Story analysis failed: {str(e)}")

    # Show Parsed Scenes & Step 2 Generate
    if st.session_state["parsed_story"]:
        parsed = st.session_state["parsed_story"]
        scenes = parsed.get("scenes", [])

        st.markdown("---")
        st.markdown(f"#### 🎭 Cast & Scene Breakdown ({len(scenes)} Scenes)")

        if parsed.get("fallback_notice"):
            st.info(f"ℹ️ {parsed['fallback_notice']}")

        # Character assignment overview pills
        characters = parsed.get("detected_characters", [])
        st.markdown("<p style='font-size: 0.9rem; color: #CBD5E1;'>Detected Characters:</p>", unsafe_allow_html=True)
        char_pills_html = " ".join([f'<span class="voice-badge badge-confident">👤 {c}</span>' for c in characters])
        st.markdown(f"<div style='margin-bottom: 16px;'>{char_pills_html}</div>", unsafe_allow_html=True)

        # Allow user to tweak voice assignments if they want before generating
        with st.expander("🛠️ Customize Voice / Emotion per Scene", expanded=False):
            for idx, sc in enumerate(scenes):
                c_spk, c_v, c_e = st.columns([2, 2, 2])
                with c_spk:
                    st.markdown(f"**Scene {idx+1}: {sc['speaker']}**")
                    sc['text'] = st.text_input(f"Text #{idx+1}", value=sc['text'], key=f"edit_txt_{idx}")
                with c_v:
                    sc['voice'] = st.selectbox(
                        f"Voice #{idx+1}",
                        options=AppConfig.PERSONALITIES,
                        index=AppConfig.PERSONALITIES.index(sc['voice']) if sc['voice'] in AppConfig.PERSONALITIES else 0,
                        key=f"edit_v_{idx}"
                    )
                with c_e:
                    sc['emotion'] = st.selectbox(
                        f"Emotion #{idx+1}",
                        options=AppConfig.EMOTIONS,
                        index=AppConfig.EMOTIONS.index(sc['emotion']) if sc['emotion'] in AppConfig.EMOTIONS else 0,
                        key=f"edit_e_{idx}"
                    )

        # Step 2: Generate All Scenes & Combine Audio
        st.markdown("#### 🔊 Step 2: Synthesize & Assemble Complete Audio Drama")
        gen_story_btn = st.button("🎙️ Generate All Scenes & Stitch Story", key="btn_gen_all_story")

        if gen_story_btn:
            progress_bar = st.progress(0.0)
            progress_status = st.empty()

            def update_progress(current, total, msg):
                progress_bar.progress(float(current) / float(total))
                progress_status.markdown(f"*{msg}*")

            with st.spinner("Generating anime voices for every scene and stitching audio..."):
                try:
                    result = story_processor.process_and_synthesize_story(
                        story_scenes=scenes,
                        language=story_lang,
                        speed=global_speed,
                        pitch_option=global_pitch,
                        progress_callback=update_progress
                    )
                    st.session_state["story_audio_result"] = result
                    progress_bar.progress(1.0)
                    progress_status.markdown("✅ **All scenes synthesized and merged successfully!**")
                    st.success("🎉 Complete Audio Story is ready!")
                except Exception as e:
                    st.error(f"❌ Error during story synthesis: {str(e)}")

        # Display Story Results (Individual Scene Players + Complete Story Audio)
        if st.session_state["story_audio_result"]:
            res = st.session_state["story_audio_result"]
            processed_scenes = res.get("scenes", [])
            complete_bytes = res.get("complete_audio_bytes")
            total_duration = res.get("complete_duration_seconds", 0.0)

            st.markdown("---")
            st.markdown("### 🎬 Complete Story Audio Drama")

            st.markdown(
                f"""
                <div class="glass-card" style="border: 2px solid rgba(255, 141, 161, 0.4); background: rgba(30, 20, 45, 0.85);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap;">
                        <h4 style="margin: 0; color: #FFF;">▶ Complete Audio Story ({len(processed_scenes)} Scenes)</h4>
                        <span style="font-family: 'JetBrains Mono', monospace; color: #FCD34D;">Total: ~{total_duration}s</span>
                    </div>
                """,
                unsafe_allow_html=True
            )

            st.audio(complete_bytes, format="audio/mp3")

            dl_col1, dl_col2 = st.columns([3, 2])
            with dl_col2:
                st.download_button(
                    label="⬇️ Download Complete Story (MP3)",
                    data=complete_bytes,
                    file_name=f"complete_anime_story_{len(processed_scenes)}_scenes.mp3",
                    mime="audio/mp3",
                    key="dl_complete_story"
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # Individual Scenes List
            st.markdown("#### 📜 Scene by Scene Breakdown")
            for idx, sc in enumerate(processed_scenes):
                render_scene_card(sc, index=idx+1, total=len(processed_scenes))
