"""WellMind AI - Assessment Page"""
import streamlit as st
from components.cards import section_header
from components.animations import glowing_divider


def render():
    st.markdown("""
    <div class="page-hero fade-up">
        <h1>📋 Student Wellness Assessment</h1>
        <p>Complete today's check-in. Our 5 AI agents will analyze your inputs in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    prev = st.session_state.get("assessment_data") or {}

    with st.form("wellness_form", clear_on_submit=False):
        # ── Section 1: Sleep & Hydration ─────────────────────────────────────
        section_header("💤", "Sleep & Hydration")
        col1, col_div1, col2 = st.columns([1, 0.02, 1])
        with col1:
            sleep_hours = st.slider(
                "🌙 Sleep Hours (last night)",
                min_value=0.0, max_value=12.0,
                value=float(prev.get("sleep_hours", 7.0)),
                step=0.5,
                help="How many hours did you sleep last night?",
            )
            st.markdown(f'<div style="color:#94A3B8; font-size:0.8rem; margin-top:-0.5rem;">Recommended: 7–9 hrs · You entered: <b style="color:#00E5B0">{sleep_hours} hrs</b></div>', unsafe_allow_html=True)
        with col_div1:
            st.markdown('<div style="border-left:1px solid rgba(0,229,176,0.25); height:100%; min-height:80px; margin:0 auto;"></div>', unsafe_allow_html=True)
        with col2:
            water_intake = st.number_input(
                "💧 Water Intake (glasses / 250ml)",
                min_value=0, max_value=20,
                value=int(prev.get("water_intake", 6)),
                step=1,
                help="Number of 250ml glasses consumed today",
            )
            st.markdown(f'<div style="color:#94A3B8; font-size:0.8rem; margin-top:-0.5rem;">Target: 8+ glasses · You entered: <b style="color:#00E5B0">{water_intake} glasses</b></div>', unsafe_allow_html=True)

        glowing_divider()

        # ── Section 2: Stress & Study ─────────────────────────────────────────
        section_header("🧠", "Stress & Academic Load")
        col3, col_div2, col4 = st.columns([1, 0.02, 1])

        with col3:
            stress_level = st.slider(
                "😰 Stress Level (1 = calm, 10 = overwhelmed)",
                min_value=1, max_value=10,
                value=int(prev.get("stress_level", 5)),
                step=1,
            )
            stress_labels = {1: "😌 Very Calm", 2: "🙂 Calm", 3: "😊 Relaxed", 4: "🤔 Mild",
                             5: "😐 Moderate", 6: "😟 Noticeable", 7: "😓 High",
                             8: "😰 Very High", 9: "😫 Severe", 10: "🤯 Extreme"}
            st.markdown(f'<div style="color:#94A3B8; font-size:0.8rem; margin-top:-0.5rem;">Current: <b style="color:#F59E0B">{stress_labels.get(stress_level, "")}</b></div>', unsafe_allow_html=True)
        with col_div2:
            st.markdown('<div style="border-left:1px solid rgba(0,229,176,0.25); height:100%; min-height:80px; margin:0 auto;"></div>', unsafe_allow_html=True)
        with col4:
            study_hours = st.slider(
                "📚 Study Hours (today)",
                min_value=0.0, max_value=16.0,
                value=float(prev.get("study_hours", 5.0)),
                step=0.5,
            )
            study_color = "#00E5B0" if study_hours <= 6 else "#F59E0B" if study_hours <= 9 else "#EF4444"
            st.markdown(f'<div style="color:#94A3B8; font-size:0.8rem; margin-top:-0.5rem;">Optimal: ≤6 hrs · You entered: <b style="color:{study_color}">{study_hours} hrs</b></div>', unsafe_allow_html=True)

        glowing_divider()

        # ── Section 3: Physical & Mood ────────────────────────────────────────
        section_header("🏃", "Physical Activity & Mood")
        col5, col_div3, col6 = st.columns([1, 0.02, 1])

        with col5:
            exercise_minutes = st.slider(
                "🏃 Exercise Duration (minutes today)",
                min_value=0, max_value=180,
                value=int(prev.get("exercise_minutes", 30)),
                step=5,
            )
            ex_color = "#00E5B0" if exercise_minutes >= 30 else "#F59E0B" if exercise_minutes >= 15 else "#EF4444"
            st.markdown(f'<div style="color:#94A3B8; font-size:0.8rem; margin-top:-0.5rem;">Target: 30+ min · You entered: <b style="color:{ex_color}">{exercise_minutes} min</b></div>', unsafe_allow_html=True)
        with col_div3:
            st.markdown('<div style="border-left:1px solid rgba(0,229,176,0.25); height:100%; min-height:80px; margin:0 auto;"></div>', unsafe_allow_html=True)
        with col6:
            mood = st.selectbox(
                "😊 Current Mood",
                options=["Excellent", "Good", "Neutral", "Tired", "Stressed"],
                index=["Excellent", "Good", "Neutral", "Tired", "Stressed"].index(prev.get("mood", "Neutral")),
            )
            mood_icons = {"Excellent": "🤩", "Good": "😊", "Neutral": "😐", "Tired": "😴", "Stressed": "😰"}
            st.markdown(f'<div style="color:#94A3B8; font-size:0.8rem; margin-top:-0.5rem;">You selected: <b style="color:#00E5B0">{mood_icons.get(mood,"")} {mood}</b></div>', unsafe_allow_html=True)

        glowing_divider()

        # ── Validation Summary ────────────────────────────────────────────────
        issues = []
        if sleep_hours < 4:
            issues.append("⚠️ Very low sleep — this significantly impacts your score.")
        if water_intake < 3:
            issues.append("⚠️ Critical dehydration level detected.")
        if stress_level >= 8 and study_hours >= 8:
            issues.append("🚨 High stress combined with heavy study — burnout risk elevated.")

        if issues:
            for issue in issues:
                st.warning(issue)

        # ── Submit ────────────────────────────────────────────────────────────
        col_btn, col_tip = st.columns([1, 2])
        with col_btn:
            submitted = st.form_submit_button("🚀 Run AI Analysis", width="stretch")
        with col_tip:
            st.markdown('<div style="color:#94A3B8; font-size:0.82rem; padding-top:0.7rem;">5 specialized AI agents will analyze your wellness data in sequence.</div>', unsafe_allow_html=True)

        if submitted:
            st.session_state["assessment_data"] = {
                "sleep_hours": sleep_hours,
                "stress_level": stress_level,
                "study_hours": study_hours,
                "water_intake": water_intake,
                "exercise_minutes": exercise_minutes,
                "mood": mood,
            }
            st.session_state["analysis_complete"] = False
            st.session_state["analysis_result"] = None
            st.session_state["page"] = "Analysis"
            st.rerun()
