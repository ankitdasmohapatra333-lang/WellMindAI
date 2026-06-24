"""WellMind AI - Single Navigation Bar"""
import streamlit as st
from streamlit_option_menu import option_menu

NAV_OPTIONS = ["Home", "Assessment", "Analysis", "Results", "History"]
NAV_ICONS   = ["house", "clipboard-check", "cpu", "bar-chart-line", "clock-history"]


def render_navbar():
    """Render the top logo bar (branding only)."""
    st.markdown("""
    <div class="wellmind-navbar">
        <div class="navbar-logo">
            <div class="navbar-logo-icon">🧠</div>
            <span class="navbar-logo-text">WellMind AI</span>
        </div>
        <div style="color:#94A3B8; font-size:0.82rem; font-style:italic;">
            AI-Powered Student Wellness Platform
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_nav_menu() -> str:
    """Render the single horizontal navigation and return selected page."""
    current = st.session_state.get("page", "Home")
    if current not in NAV_OPTIONS:
        current = "Home"

    selected = option_menu(
        menu_title=None,
        options=NAV_OPTIONS,
        icons=NAV_ICONS,
        default_index=NAV_OPTIONS.index(current),
        orientation="horizontal",
        styles={
            "container": {
                "padding": "6px 12px",
                "background": "rgba(15,29,45,0.6)",
                "border-radius": "14px",
                "border": "1px solid rgba(0,229,176,0.15)",
                "margin-bottom": "2rem",
            },
            "icon": {"color": "#94A3B8", "font-size": "15px"},
            "nav-link": {
                "font-size": "0.88rem",
                "font-weight": "500",
                "color": "#94A3B8",
                "border-radius": "10px",
                "padding": "8px 18px",
                "--hover-color": "rgba(0,229,176,0.08)",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #00E5B0, #5EEAD4)",
                "color": "#07131F",
                "font-weight": "700",
                "border-radius": "10px",
            },
        },
    )
    return selected
