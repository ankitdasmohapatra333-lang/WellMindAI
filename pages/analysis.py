"""WellMind AI - Analysis / AI Processing Page"""
import streamlit as st
import time
from components.cards import section_header
from components.animations import glowing_divider
from utils.constants import AGENTS
from services.api import analyze_wellness


def render():
    st.markdown("""
    <div class="page-hero fade-up">
        <h1>🤖 AI Agent Processing</h1>
        <p>5 specialized agents analyzing your wellness data in sequence.</p>
    </div>
    """, unsafe_allow_html=True)

    data = st.session_state.get("assessment_data")
    if not data:
        st.markdown("""
        <div class="glass-card" style="text-align:center; padding:3rem;">
            <div style="font-size:3rem; margin-bottom:1rem;">📋</div>
            <div style="font-size:1.1rem; color:#94A3B8;">No assessment data found.</div>
            <div style="color:#00E5B0; margin-top:0.5rem; font-size:0.9rem;">Please complete the Assessment first.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("← Go to Assessment"):
            st.session_state["page"] = "Assessment"
            st.rerun()
        return

    # ── If already analyzed, show completion state ────────────────────────────
    if st.session_state.get("analysis_complete") and st.session_state.get("analysis_result"):
        _show_complete()
        return

    # ── Run analysis animation ────────────────────────────────────────────────
    _run_analysis(data)


def _show_complete():
    st.markdown("""
    <div class="glass-card fade-up" style="text-align:center; padding:2.5rem; border-color:rgba(0,229,176,0.4);">
        <div style="font-size:3.5rem; margin-bottom:0.8rem;">✅</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:1.5rem; font-weight:700; color:#00E5B0; margin-bottom:0.5rem;">Analysis Complete!</div>
        <div style="color:#94A3B8; font-size:0.92rem;">All 5 AI agents have finished processing your wellness data.</div>
    </div>
    """, unsafe_allow_html=True)

    glowing_divider()
    section_header("🤖", "Agent Summary")

    for agent in AGENTS:
        st.markdown(f"""
        <div class="agent-card done fade-up">
            <span class="agent-icon">{agent['icon']}</span>
            <div>
                <div class="agent-name">{agent['name']}</div>
                <div class="agent-desc">{agent['desc']}</div>
            </div>
            <div class="agent-status" style="color:#5EEAD4;">✅ <span style="font-size:0.75rem;">COMPLETE</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    if st.button("📊 View Results Dashboard →", width="stretch"):
        st.session_state["page"] = "Results"
        st.rerun()


def _run_analysis(data: dict):
    section_header("⚡", "Running AI Agents")

    # Input summary
    st.markdown("""
    <div class="glass-card fade-up" style="margin-bottom:1.5rem;">
        <div style="font-size:0.8rem; color:#94A3B8; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.8rem;">Input Data Received</div>
    """, unsafe_allow_html=True)

    icols = st.columns(6)
    icons = ["🌙", "😰", "📚", "💧", "🏃", "😊"]
    labels = ["Sleep", "Stress", "Study", "Water", "Exercise", "Mood"]
    values = [
        f"{data['sleep_hours']}h", f"{data['stress_level']}/10",
        f"{data['study_hours']}h", f"{data['water_intake']}gl",
        f"{data['exercise_minutes']}m", data['mood']
    ]
    for i, col in enumerate(icols):
        with col:
            st.markdown(f"""
            <div style="text-align:center; padding:0.5rem;">
                <div style="font-size:1.5rem;">{icons[i]}</div>
                <div style="font-size:1rem; font-weight:600; color:#00E5B0;">{values[i]}</div>
                <div style="font-size:0.7rem; color:#94A3B8;">{labels[i]}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    glowing_divider()

    # Placeholders for agents + global progress
    progress_bar = st.progress(0, text="Initializing AI agents...")
    agent_placeholders = [st.empty() for _ in AGENTS]
    status_box = st.empty()

    # Initialize all as pending
    def draw_agent(ph, agent, status):
        color_map = {"pending": "#94A3B8", "active": "#00E5B0", "done": "#5EEAD4"}
        icon_map = {"pending": "⬜", "active": "⏳", "done": "✅"}
        css = "active" if status == "active" else "done" if status == "done" else ""
        ph.markdown(f"""
        <div class="agent-card {css}">
            <span class="agent-icon">{agent['icon']}</span>
            <div>
                <div class="agent-name">{agent['name']}</div>
                <div class="agent-desc">{agent['desc']}</div>
            </div>
            <div class="agent-status" style="color:{color_map[status]};">
                {icon_map[status]} <span style="font-size:0.75rem; text-transform:uppercase;">{status}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Draw all pending
    for i, (ph, agent) in enumerate(zip(agent_placeholders, AGENTS)):
        draw_agent(ph, agent, "pending")

    # Durations per agent (seconds)
    durations = [1.8, 2.0, 1.6, 2.2, 1.4]
    statuses = ["pending"] * len(AGENTS)

    for idx, (agent, dur) in enumerate(zip(AGENTS, durations)):
        statuses[idx] = "active"
        draw_agent(agent_placeholders[idx], agent, "active")
        progress_bar.progress((idx) / len(AGENTS), text=f"🤖 Running {agent['name']}...")
        status_box.markdown(f'<div style="color:#F59E0B; font-size:0.88rem; margin-top:0.3rem;">⚡ {agent["desc"]}</div>', unsafe_allow_html=True)

        steps = int(dur * 10)
        for step in range(steps):
            time.sleep(dur / steps)
            pct = (idx + (step + 1) / steps) / len(AGENTS)
            progress_bar.progress(min(pct, 0.99), text=f"🤖 Running {agent['name']}... {int(((step+1)/steps)*100)}%")

        statuses[idx] = "done"
        draw_agent(agent_placeholders[idx], agent, "done")

    # Final: call API
    progress_bar.progress(0.99, text="🔮 Synthesizing results...")
    status_box.markdown('<div style="color:#00E5B0; font-size:0.88rem;">✨ Generating personalized wellness report...</div>', unsafe_allow_html=True)
    time.sleep(0.6)

    result = analyze_wellness(data)
    st.session_state["analysis_result"] = result
    st.session_state["analysis_complete"] = True

    progress_bar.progress(1.0, text="✅ Analysis complete!")
    status_box.empty()
    time.sleep(0.5)

    st.rerun()
