"""Reusable UI components for Anime Voice Studio."""
import streamlit as st
from typing import Dict, Any, Optional

def render_header():
    """Renders the main anime studio header with glowing typography and Japanese aesthetic."""
    header_html = """
    <div class="app-header">
        <h1 class="app-title">🌸 AI ANIME VOICE STUDIO</h1>
        <p class="app-subtitle">Turn your words into anime-inspired voices.</p>
        <span class="app-japanese-sub">アニメ風音声合成スタジオ • ULTRA HI-FI NEURAL AUDIO</span>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def get_personality_badge_html(personality: str) -> str:
    """Returns styled HTML badge corresponding to personality."""
    p_lower = personality.lower()
    if "kawaii" in p_lower:
        cls = "badge-kawaii"
    elif "energetic" in p_lower:
        cls = "badge-energetic"
    elif "calm" in p_lower:
        cls = "badge-calm"
    elif "villain" in p_lower:
        cls = "badge-villain"
    elif "shy" in p_lower:
        cls = "badge-shy"
    else:
        cls = "badge-confident"
    return f'<span class="voice-badge {cls}">{personality}</span>'

def get_emotion_badge_html(emotion: str) -> str:
    """Returns styled emotion badge HTML."""
    return f'<span class="voice-badge badge-shy" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.25); color: #FFF;">🎭 {emotion}</span>'

def render_status_badge(engine_label: str, is_fallback: bool = False, fallback_reason: Optional[str] = None):
    """Renders TTS Engine status banner."""
    if is_fallback:
        st.markdown(
            f"""
            <div style="background: rgba(234, 179, 8, 0.12); border: 1px solid rgba(251, 191, 36, 0.35); border-radius: 12px; padding: 10px 16px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.2rem;">⚡</span>
                    <div>
                        <span style="font-weight: 700; color: #FCD34D;">Engine: {engine_label}</span>
                        <div style="font-size: 0.8rem; color: #E2E8F0; opacity: 0.85;">{fallback_reason or 'Operating in high-fidelity zero-config fallback mode.'}</div>
                    </div>
                </div>
                <span class="status-pill status-pill-info">Zero-Config Mode</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(74, 222, 128, 0.3); border-radius: 12px; padding: 10px 16px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 1.2rem;">✨</span>
                    <div>
                        <span style="font-weight: 700; color: #4ADE80;">Engine: {engine_label}</span>
                        <div style="font-size: 0.8rem; color: #E2E8F0; opacity: 0.85;">Connected and generating ultra-expressive anime audio.</div>
                    </div>
                </div>
                <span class="status-pill status-pill-ok">Active</span>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_audio_card(
    audio_bytes: bytes,
    personality: str,
    emotion: str,
    language: str,
    engine_label: str,
    duration_seconds: float = 0.0,
    download_filename: str = "anime_voice.mp3",
    key_prefix: str = "audio_card"
):
    """Renders a card with audio player, meta badges, waveform animation, and download button."""
    p_badge = get_personality_badge_html(personality)
    e_badge = get_emotion_badge_html(emotion)
    l_badge = f'<span class="voice-badge badge-calm">🌐 {language}</span>'
    
    st.markdown(
        f"""
        <div class="glass-card" style="margin-top: 14px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 14px;">
                <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                    {p_badge}
                    {e_badge}
                    {l_badge}
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 0.82rem; color: #CBD5E1; font-family: 'JetBrains Mono', monospace;">~{duration_seconds}s</span>
                    <span style="font-size: 0.82rem; color: #A855F7; font-weight: 600;">{engine_label}</span>
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    st.audio(audio_bytes, format="audio/mp3")

    col1, col2 = st.columns([3, 2])
    with col2:
        st.download_button(
            label="⬇️ Download Audio (MP3)",
            data=audio_bytes,
            file_name=download_filename,
            mime="audio/mp3",
            key=f"{key_prefix}_dl"
        )
    st.markdown("</div>", unsafe_allow_html=True)

def render_scene_card(scene: Dict[str, Any], index: int, total: int):
    """Renders an individual scene card in the story reader breakdown."""
    speaker = scene.get("speaker", f"Speaker {index}")
    text = scene.get("text", "")
    voice = scene.get("voice", "🌸 Kawaii")
    emotion = scene.get("emotion", "Calm")
    duration = scene.get("duration_seconds", 0.0)
    audio_bytes = scene.get("audio_bytes")

    p_badge = get_personality_badge_html(voice)
    e_badge = get_emotion_badge_html(emotion)

    st.markdown(
        f"""
        <div class="scene-box">
            <div class="scene-header">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="color: #FF8DA1; font-weight: 800; font-size: 0.9rem;">SCENE {index}/{total}</span>
                    <span class="scene-speaker">{speaker}</span>
                </div>
                <div style="display: flex; gap: 6px;">
                    {p_badge}
                    {e_badge}
                </div>
            </div>
            <div class="scene-text">"{text}"</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3")
        c1, c2 = st.columns([4, 1])
        with c2:
            st.download_button(
                label=f"⬇️ Scene {index}",
                data=audio_bytes,
                file_name=f"scene_{index}_{speaker.lower().replace(' ', '_')}.mp3",
                mime="audio/mp3",
                key=f"scene_dl_{index}"
            )

def render_preset_dialogue_buttons(on_select):
    """Renders interactive preset pills for quick testing."""
    st.markdown("<p style='font-size: 0.85rem; color: #CBD5E1; margin-bottom: 6px;'>💡 Quick Anime Presets:</p>", unsafe_allow_html=True)
    presets = [
        ("🌸 Kawaii Greeting", "Konnichiwa! Watashi wa anata no AI anime partner desu! Today is going to be wonderful!"),
        ("⚡ Shonen Battle", "Ikuzo! Makeru wake ni wa ikanai! This is where my real power awakens!"),
        ("🌙 Gentle Twilight", "The sunset over the cherry blossoms is peaceful. You worked really hard today."),
        ("😈 Dark Villain", "Kukuku... You think friendship can conquer destiny? How deliciously naive!"),
        ("🎀 Shy Confession", "A-Ano... I made this special audio for you... Please listen carefully, okay?"),
        ("👑 Heroic Leader", "Stand behind me! Together, there is no obstacle we cannot overcome!")
    ]

    cols = st.columns(3)
    for i, (label, text) in enumerate(presets):
        col = cols[i % 3]
        if col.button(label, key=f"preset_{i}"):
            on_select(text)
