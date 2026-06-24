"""WellMind AI - History Dashboard"""
import streamlit as st
from components.cards import section_header
from components.animations import glowing_divider
from components.charts import wellness_trend, sleep_stress_chart, burnout_trend, study_area_chart
from utils.helpers import generate_mock_history


def render():
    st.markdown("""
    <div class="page-hero fade-up">
        <h1>📅 Wellness History</h1>
        <p>7-day trend analysis across wellness, sleep, stress, and burnout indicators.</p>
    </div>
    """, unsafe_allow_html=True)

    df = st.session_state.get("history")
    if df is None or (hasattr(df, "__len__") and len(df) == 0):
        df = generate_mock_history()
        st.session_state["history"] = df

    # ── Summary KPI row ───────────────────────────────────────────────────────
    section_header("📊", "7-Day Summary")
    k1, k2, k3, k4, k5 = st.columns(5)

    avg_score = round(df["Wellness Score"].mean(), 1)
    avg_sleep = round(df["Sleep Hours"].mean(), 1)
    avg_stress = round(df["Stress Level"].mean(), 1)
    avg_burnout = round(df["Burnout Risk"].mean(), 1)
    trend = "📈" if df["Wellness Score"].iloc[-1] >= df["Wellness Score"].iloc[0] else "📉"

    for col, icon, val, label, color in [
        (k1, "🏆", avg_score, "Avg Wellness", "#00E5B0"),
        (k2, "🌙", f"{avg_sleep}h", "Avg Sleep", "#5EEAD4"),
        (k3, "😰", f"{avg_stress}/10", "Avg Stress", "#F59E0B"),
        (k4, "🔥", f"{avg_burnout}%", "Avg Burnout", "#F97316" if avg_burnout > 50 else "#00E5B0"),
        (k5, trend, "7 Days", "Trend", "#8B5CF6"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card fade-up">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value" style="color:{color}">{val}</div>
                <div class="kpi-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    glowing_divider()

    # ── Main trend charts ─────────────────────────────────────────────────────
    section_header("📈", "Wellness & Burnout Trends")
    t1, t2 = st.columns(2)

    with t1:
        st.plotly_chart(wellness_trend(df), width="stretch", config={"displayModeBar": False})

    with t2:
        st.plotly_chart(burnout_trend(df), width="stretch", config={"displayModeBar": False})

    glowing_divider()

    section_header("😴", "Sleep & Stress Correlation")
    t3, t4 = st.columns(2)

    with t3:
        st.plotly_chart(sleep_stress_chart(df), width="stretch", config={"displayModeBar": False})

    with t4:
        st.plotly_chart(study_area_chart(df), width="stretch", config={"displayModeBar": False})

    glowing_divider()

    # ── Raw Data Table ────────────────────────────────────────────────────────
    section_header("📋", "Raw Data Log")
    styled_df = df.copy()
    st.dataframe(
        styled_df,
        width="stretch",
        hide_index=True,
        column_config={
            "Date": st.column_config.TextColumn("Date"),
            "Wellness Score": st.column_config.ProgressColumn("Wellness Score", min_value=0, max_value=100, format="%d"),
            "Sleep Hours": st.column_config.NumberColumn("Sleep (hrs)", format="%.1f"),
            "Stress Level": st.column_config.NumberColumn("Stress (1-10)"),
            "Burnout Risk": st.column_config.ProgressColumn("Burnout Risk", min_value=0, max_value=100, format="%d%%"),
            "Study Hours": st.column_config.NumberColumn("Study (hrs)"),
        },
    )

    glowing_divider()

    # ── Insights Box ──────────────────────────────────────────────────────────
    section_header("💡", "AI Insights")
    best_day = df.loc[df["Wellness Score"].idxmax(), "Date"]
    worst_day = df.loc[df["Wellness Score"].idxmin(), "Date"]
    high_burnout_days = (df["Burnout Risk"] > 50).sum()
    low_sleep_days = (df["Sleep Hours"] < 6.5).sum()

    ins1, ins2 = st.columns(2)
    with ins1:
        st.markdown(f"""
        <div class="glass-card fade-up" style="border-left: 4px solid #00E5B0;">
            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:1px;">Positive Signals</div>
            <div style="color:#00E5B0; font-weight:600; margin-bottom:0.3rem;">🏆 Best Day: {best_day}</div>
            <div style="color:#94A3B8; font-size:0.85rem;">Your peak wellness score this week was on {best_day} with a score of {df.loc[df['Wellness Score'].idxmax(), 'Wellness Score']}.</div>
        </div>
        """, unsafe_allow_html=True)

    with ins2:
        attention_color = "#EF4444" if high_burnout_days >= 3 or low_sleep_days >= 3 else "#F59E0B"
        st.markdown(f"""
        <div class="glass-card fade-up" style="border-left: 4px solid {attention_color};">
            <div style="font-size:0.8rem; color:#94A3B8; margin-bottom:0.5rem; text-transform:uppercase; letter-spacing:1px;">Attention Areas</div>
            <div style="color:{attention_color}; font-weight:600; margin-bottom:0.3rem;">⚠️ Needs Attention</div>
            <div style="color:#94A3B8; font-size:0.85rem;">
                {high_burnout_days} day(s) with high burnout risk (>50%) · {low_sleep_days} day(s) with insufficient sleep (&lt;6.5 hrs).
            </div>
        </div>
        """, unsafe_allow_html=True)
