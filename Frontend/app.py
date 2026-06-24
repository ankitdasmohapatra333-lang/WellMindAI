"""WellMind AI - Main Application Entry Point"""
import streamlit as st
import os, sys

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="WellMind AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Load global styles ──────────────────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Init session state ───────────────────────────────────────────────────────
from utils.helpers import init_session_state
init_session_state()

# ── Navigation ───────────────────────────────────────────────────────────────
from components.navbar import render_navbar, render_nav_menu
from components.animations import particle_background

particle_background()
render_navbar()
selected = render_nav_menu()
st.session_state["page"] = selected

# ── Page Routing ─────────────────────────────────────────────────────────────
if selected == "Home":
    from pages import home
    home.render()

elif selected == "Assessment":
    from pages import assessment
    assessment.render()

elif selected == "Analysis":
    from pages import analysis
    analysis.render()

elif selected == "Results":
    from pages import results
    results.render()

elif selected == "History":
    from pages import history
    history.render()
