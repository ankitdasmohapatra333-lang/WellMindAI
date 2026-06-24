"""WellMind AI - Card Components"""
import streamlit as st


def kpi_card(icon: str, value: str, label: str, color: str = "#00E5B0"):
    st.markdown(f"""
    <div class="kpi-card fade-up">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value" style="color:{color}">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def recommendation_card(icon: str, title: str, desc: str, priority: str):
    priority_lower = priority.lower()
    st.markdown(f"""
    <div class="rec-card {priority_lower} fade-up">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:0.4rem;">
            <span style="font-size:1.3rem;">{icon}</span>
            <span class="rec-title">{title}</span>
        </div>
        <div class="rec-desc">{desc}</div>
        <span class="rec-priority {priority_lower}">{priority} Priority</span>
    </div>
    """, unsafe_allow_html=True)


def evidence_card(source: str, finding: str, relevance: int):
    bar_width = relevance
    st.markdown(f"""
    <div class="evidence-card fade-up">
        <div class="evidence-source">📖 {source}</div>
        <div class="evidence-finding">{finding}</div>
        <div class="evidence-relevance">Relevance: {relevance}%</div>
        <div class="progress-wrap" style="margin-top:0.5rem;">
            <div class="progress-fill" style="width:{bar_width}%; background: linear-gradient(90deg, #8B5CF6, #5EEAD4);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def agent_card(icon: str, name: str, desc: str, status: str = "pending"):
    """status: pending | active | done | error"""
    status_map = {
        "pending": ("⬜", "#94A3B8", ""),
        "active": ("⏳", "#00E5B0", "active"),
        "done": ("✅", "#5EEAD4", "done"),
        "error": ("❌", "#EF4444", ""),
    }
    status_icon, status_color, css_class = status_map.get(status, status_map["pending"])
    st.markdown(f"""
    <div class="agent-card {css_class}">
        <span class="agent-icon">{icon}</span>
        <div>
            <div class="agent-name">{name}</div>
            <div class="agent-desc">{desc}</div>
        </div>
        <div class="agent-status" style="color:{status_color};">
            {status_icon} <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.5px;">{status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(icon: str, title: str):
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size:1.4rem;">{icon}</span>
        <span class="section-title">{title}</span>
        <div class="section-accent"></div>
    </div>
    """, unsafe_allow_html=True)


def glass_container(content_fn, padding="1.5rem"):
    st.markdown(f'<div class="glass-card" style="padding:{padding};">', unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)
