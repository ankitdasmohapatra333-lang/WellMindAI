"""WellMind AI - Animation Helpers"""
import streamlit as st
import time


def animated_progress_bar(label: str, duration: float = 2.0):
    """Show a styled animated progress bar and return when done."""
    bar = st.progress(0, text=f"⏳ {label}")
    steps = 40
    for i in range(steps + 1):
        time.sleep(duration / steps)
        pct = i / steps
        bar.progress(pct, text=f"⏳ {label} — {int(pct * 100)}%")
    bar.empty()


def loading_dots(placeholder, text: str = "Processing"):
    """Cycle dots in a placeholder."""
    for dots in [".", "..", "...", ".."]:
        placeholder.markdown(
            f'<div style="color:#00E5B0; font-size:1rem; font-weight:500;">{text}{dots}</div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.35)


def particle_background():
    """Inject a CSS particle/gradient ambient background."""
    st.markdown("""
    <style>
    .stApp::before {
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background:
            radial-gradient(ellipse at 20% 50%, rgba(0,229,176,0.04) 0%, transparent 50%),
            radial-gradient(ellipse at 80% 20%, rgba(139,92,246,0.05) 0%, transparent 50%),
            radial-gradient(ellipse at 50% 80%, rgba(94,234,212,0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
        animation: drift 20s ease-in-out infinite alternate;
    }
    @keyframes drift {
        0% { transform: translate(0,0) rotate(0deg); }
        100% { transform: translate(-2%, 2%) rotate(1deg); }
    }
    </style>
    """, unsafe_allow_html=True)


def glowing_divider(color: str = "#00E5B0"):
    st.markdown(f"""
    <div style="
        height: 1px;
        background: linear-gradient(90deg, transparent, {color}55, transparent);
        margin: 1.5rem 0;
        border-radius: 1px;
    "></div>
    """, unsafe_allow_html=True)
