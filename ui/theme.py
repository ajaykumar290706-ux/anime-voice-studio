"""Sakura & Glassmorphism Theme CSS injector for modern Anime Voice Studio UI."""
import streamlit as st

def inject_sakura_theme():
    """Injects high-fidelity CSS styling, animations, and custom typography."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Zen+Maru+Gothic:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap');

    :root {
        --bg-dark: #0e0b16;
        --bg-card: rgba(26, 19, 41, 0.72);
        --bg-card-hover: rgba(37, 28, 59, 0.85);
        --sakura-light: #FFE4E8;
        --sakura-pink: #FF8DA1;
        --sakura-deep: #FF6584;
        --purple-accent: #A855F7;
        --purple-glow: rgba(168, 85, 247, 0.35);
        --pink-glow: rgba(255, 141, 161, 0.3);
        --border-glass: rgba(255, 183, 197, 0.2);
        --text-primary: #F8FAFC;
        --text-muted: #CBD5E1;
    }

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', 'Zen Maru Gothic', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: radial-gradient(circle at 10% 20%, #1e1333 0%, #0d0b16 55%, #08060d 100%) fixed !important;
        color: var(--text-primary) !important;
    }

    /* Subtle Floating Petals Background Animation */
    .sakura-bg-decor {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
        opacity: 0.55;
    }

    .petal {
        position: absolute;
        background: radial-gradient(circle, #ffb7c5 0%, #ff8da1 80%);
        border-radius: 150% 0 150% 0;
        opacity: 0.35;
        animation: petalFall linear infinite;
    }

    @keyframes petalFall {
        0% {
            transform: translateY(-5vh) translateX(0) rotate(0deg) scale(0.8);
            opacity: 0;
        }
        20% {
            opacity: 0.45;
        }
        80% {
            opacity: 0.4;
        }
        100% {
            transform: translateY(105vh) translateX(120px) rotate(480deg) scale(1.1);
            opacity: 0;
        }
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(18, 13, 28, 0.88) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid var(--border-glass) !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 183, 197, 0.15) !important;
    }

    /* Glassmorphic Container Cards */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-glass);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 12px 35px -8px rgba(0, 0, 0, 0.5), 0 0 25px -4px var(--pink-glow);
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(255, 183, 197, 0.4);
        box-shadow: 0 16px 45px -8px rgba(0, 0, 0, 0.6), 0 0 35px -2px var(--purple-glow);
    }

    /* Header Banner */
    .app-header {
        text-align: center;
        padding: 24px 10px 18px 10px;
        margin-bottom: 20px;
        position: relative;
    }

    .app-title {
        font-size: 2.75rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #FFF 10%, #FFB7C5 45%, #C084FC 85%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px !important;
        text-shadow: 0 0 35px rgba(255, 141, 161, 0.45);
        display: inline-flex;
        align-items: center;
        gap: 12px;
    }

    .app-subtitle {
        font-size: 1.15rem;
        color: #E2E8F0;
        font-weight: 400;
        letter-spacing: 0.04em;
    }

    .app-japanese-sub {
        display: block;
        font-size: 0.85rem;
        color: #F472B6;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-top: 4px;
        font-weight: 600;
    }

    /* Streamlit Tabs Customization */
    div[data-baseweb="tab-list"] {
        background: rgba(22, 16, 36, 0.7) !important;
        padding: 6px !important;
        border-radius: 16px !important;
        border: 1px solid var(--border-glass) !important;
        gap: 8px !important;
        margin-bottom: 24px !important;
    }

    div[data-baseweb="tab"] {
        border-radius: 12px !important;
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 10px 24px !important;
        transition: all 0.25s ease !important;
        border: none !important;
    }

    div[data-baseweb="tab"]:hover {
        background: rgba(255, 141, 161, 0.12) !important;
        color: #FFF !important;
    }

    div[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(255, 117, 140, 0.35) 0%, rgba(138, 43, 226, 0.35) 100%) !important;
        border: 1px solid rgba(255, 183, 197, 0.5) !important;
        color: #FFF !important;
        box-shadow: 0 4px 20px rgba(255, 117, 140, 0.25) !important;
    }

    /* Custom Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #FF758C 0%, #8A2BE2 100%) !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 1.0rem !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 28px !important;
        box-shadow: 0 6px 20px -2px rgba(255, 117, 140, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 10px 28px -2px rgba(168, 85, 247, 0.6) !important;
        color: #FFFFFF !important;
    }

    /* Secondary / Download Buttons */
    div.stDownloadButton > button {
        background: linear-gradient(135deg, rgba(255, 141, 161, 0.2) 0%, rgba(168, 85, 247, 0.25) 100%) !important;
        color: #FFF !important;
        border: 1px solid rgba(255, 183, 197, 0.4) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }

    div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, rgba(255, 141, 161, 0.35) 0%, rgba(168, 85, 247, 0.4) 100%) !important;
        border-color: #FF8DA1 !important;
        transform: translateY(-2px) !important;
    }

    /* Input text areas */
    .stTextArea textarea {
        background: rgba(18, 14, 30, 0.85) !important;
        border: 1px solid rgba(255, 183, 197, 0.25) !important;
        border-radius: 14px !important;
        color: #F8FAFC !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        padding: 14px !important;
        transition: border-color 0.2s ease !important;
    }

    .stTextArea textarea:focus {
        border-color: #FF8DA1 !important;
        box-shadow: 0 0 15px rgba(255, 141, 161, 0.3) !important;
    }

    /* Select boxes and sliders */
    div[data-baseweb="select"] > div {
        background: rgba(18, 14, 30, 0.85) !important;
        border: 1px solid rgba(255, 183, 197, 0.25) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
    }

    /* Badges & Pills */
    .voice-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .badge-kawaii {
        background: rgba(255, 141, 161, 0.2);
        color: #FFA6B7;
        border: 1px solid rgba(255, 141, 161, 0.4);
    }

    .badge-energetic {
        background: rgba(251, 191, 36, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(251, 191, 36, 0.4);
    }

    .badge-calm {
        background: rgba(56, 189, 248, 0.2);
        color: #7DD3FC;
        border: 1px solid rgba(56, 189, 248, 0.4);
    }

    .badge-villain {
        background: rgba(225, 29, 72, 0.2);
        color: #FDA4AF;
        border: 1px solid rgba(225, 29, 72, 0.4);
    }

    .badge-shy {
        background: rgba(192, 132, 252, 0.2);
        color: #E9D5FF;
        border: 1px solid rgba(192, 132, 252, 0.4);
    }

    .badge-confident {
        background: rgba(168, 85, 247, 0.2);
        color: #D8B4FE;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }

    .status-pill-ok {
        background: rgba(34, 197, 94, 0.18);
        color: #4ADE80;
        border: 1px solid rgba(74, 222, 128, 0.35);
    }

    .status-pill-info {
        background: rgba(56, 189, 248, 0.18);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.35);
    }

    /* Custom Scene Card */
    .scene-box {
        background: rgba(23, 17, 36, 0.75);
        border: 1px solid rgba(255, 183, 197, 0.15);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .scene-box:hover {
        border-color: rgba(255, 141, 161, 0.35);
        transform: translateX(4px);
    }

    .scene-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .scene-speaker {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F8FAFC;
    }

    .scene-text {
        font-size: 1.02rem;
        line-height: 1.6;
        color: #E2E8F0;
        margin-bottom: 12px;
        padding: 8px 12px;
        background: rgba(14, 10, 22, 0.6);
        border-radius: 10px;
        border-left: 3px solid #FF8DA1;
    }

    /* Waveform visual decoration */
    .waveform-deco {
        display: flex;
        align-items: center;
        gap: 3px;
        height: 24px;
    }

    .waveform-bar {
        width: 3px;
        background: linear-gradient(to top, #FF758C, #8A2BE2);
        border-radius: 2px;
        animation: waveAnim 1.2s ease-in-out infinite alternate;
    }

    @keyframes waveAnim {
        0% { height: 4px; }
        100% { height: 22px; }
    }
    </style>

    <!-- Floating Background Sakura Petals -->
    <div class="sakura-bg-decor">
        <div class="petal" style="left: 8%; width: 14px; height: 14px; animation-duration: 9s; animation-delay: 0s;"></div>
        <div class="petal" style="left: 22%; width: 12px; height: 12px; animation-duration: 12s; animation-delay: 2s;"></div>
        <div class="petal" style="left: 45%; width: 16px; height: 16px; animation-duration: 11s; animation-delay: 4s;"></div>
        <div class="petal" style="left: 68%; width: 13px; height: 13px; animation-duration: 10s; animation-delay: 1s;"></div>
        <div class="petal" style="left: 85%; width: 15px; height: 15px; animation-duration: 13s; animation-delay: 3s;"></div>
        <div class="petal" style="left: 92%; width: 11px; height: 11px; animation-duration: 8s; animation-delay: 5s;"></div>
    </div>
    """
    st.markdown(css, unsafe_allow_html=True)
