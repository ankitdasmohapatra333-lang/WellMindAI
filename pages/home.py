"""WellMind AI - Home Page"""
import streamlit as st


def render():
    st.markdown("""
    <style>
    .wm-badge { display:inline-flex; align-items:center; gap:6px; background:rgba(0,229,176,0.08); border:1px solid rgba(0,229,176,0.25); border-radius:99px; padding:4px 14px; font-size:12px; color:#94A3B8; margin-bottom:1.25rem; }
    .wm-dot { width:7px; height:7px; border-radius:50%; background:#00E5B0; display:inline-block; }
    .hero-title { font-size:2.4rem; font-weight:700; line-height:1.2; margin-bottom:0.75rem; font-family:'Space Grotesk',sans-serif; }
    .hero-title span { color:#00E5B0; }
    .hero-sub { font-size:1.05rem; color:#94A3B8; line-height:1.7; max-width:560px; margin-bottom:1.5rem; }
    .flow-wrap { display:flex; gap:0; margin-top:1rem; }
    .flow-step { flex:1; padding:1rem; background:rgba(15,29,45,0.8); border:1px solid rgba(0,229,176,0.1); position:relative; text-align:center; }
    .flow-step:first-child { border-radius:10px 0 0 10px; }
    .flow-step:last-child { border-radius:0 10px 10px 0; }
    .flow-step .fs-icon { font-size:1.5rem; margin-bottom:0.4rem; }
    .flow-step .fs-title { font-size:0.82rem; font-weight:600; color:#fff; margin-bottom:3px; }
    .flow-step .fs-sub { font-size:0.72rem; color:#94A3B8; line-height:1.4; }
    .flow-arrow { display:flex; align-items:center; color:rgba(0,229,176,0.4); font-size:1.1rem; padding:0 2px; }
    .agents-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:1rem; }
    .agent-tile { background:rgba(15,29,45,0.8); border:1px solid rgba(0,229,176,0.12); border-radius:12px; padding:1rem 1.1rem; display:flex; gap:12px; align-items:flex-start; }
    .agent-tile.wide { grid-column:1/-1; }
    .a-icon { font-size:1.6rem; }
    .a-name { font-size:0.88rem; font-weight:600; color:#fff; margin-bottom:3px; }
    .a-desc { font-size:0.78rem; color:#94A3B8; line-height:1.45; }
    .metrics-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:1rem; }
    .metric-tile { background:rgba(15,29,45,0.8); border:1px solid rgba(0,229,176,0.1); border-radius:10px; padding:0.9rem 1rem; }
    .m-label { font-size:0.7rem; text-transform:uppercase; letter-spacing:1px; color:#94A3B8; margin-bottom:6px; }
    .m-value { font-size:1.5rem; font-weight:700; font-family:'Space Grotesk',sans-serif; }
    .m-sub { font-size:0.7rem; color:#64748B; margin-top:2px; }
    .pages-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:1rem; }
    .page-tile { background:rgba(15,29,45,0.8); border:1px solid rgba(0,229,176,0.12); border-radius:12px; padding:1rem 1.1rem; }
    .pt-head { display:flex; align-items:center; gap:8px; margin-bottom:6px; }
    .pt-chip { font-size:0.65rem; background:rgba(0,229,176,0.08); border:1px solid rgba(0,229,176,0.2); border-radius:99px; padding:2px 8px; color:#00E5B0; margin-left:auto; }
    .pt-title { font-size:0.88rem; font-weight:600; color:#fff; }
    .pt-desc { font-size:0.78rem; color:#94A3B8; line-height:1.45; }
    .tech-wrap { display:flex; flex-wrap:wrap; gap:8px; margin-top:1rem; }
    .tech-pill { font-size:0.75rem; background:rgba(15,29,45,0.8); border:1px solid rgba(94,234,212,0.2); border-radius:99px; padding:4px 13px; color:#94A3B8; }
    .score-demo { display:flex; align-items:center; gap:1.2rem; background:rgba(15,29,45,0.8); border:1px solid rgba(0,229,176,0.15); border-radius:14px; padding:1.1rem 1.3rem; margin-top:1rem; }
    .sd-info h4 { font-size:1rem; font-weight:600; color:#fff; margin-bottom:4px; }
    .sd-info p { font-size:0.8rem; color:#94A3B8; }
    .tags { display:flex; gap:7px; margin-top:8px; flex-wrap:wrap; }
    .tag { font-size:0.72rem; border-radius:99px; padding:3px 10px; border:1px solid; }
    .tag-g { background:rgba(0,229,176,0.08); color:#00E5B0; border-color:rgba(0,229,176,0.3); }
    .tag-y { background:rgba(245,158,11,0.08); color:#F59E0B; border-color:rgba(245,158,11,0.3); }
    .tag-r { background:rgba(239,68,68,0.08); color:#EF4444; border-color:rgba(239,68,68,0.3); }
    .sec-eyebrow { font-size:0.7rem; text-transform:uppercase; letter-spacing:1.2px; color:#00E5B0; margin-bottom:0.5rem; }
    .sec-title { font-size:1.2rem; font-weight:700; color:#fff; font-family:'Space Grotesk',sans-serif; margin-bottom:0.4rem; }
    .sec-body { font-size:0.85rem; color:#94A3B8; line-height:1.65; }
    .divider { border:none; border-top:1px solid rgba(0,229,176,0.08); margin:2rem 0; }
    </style>
    """, unsafe_allow_html=True)

    # ── Hero ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding:2.5rem 1rem 1.5rem;">
      <div class="wm-badge"><span class="wm-dot"></span>Multi-agent AI · Streamlit · Python</div>
      <div class="hero-title">Student wellness,<br><span>analyzed by AI</span></div>
      <div class="hero-sub" style="margin:0 auto;">WellMind AI runs 5 specialized agents across your daily inputs — sleep, stress, study load, hydration, exercise — and delivers a personalized wellness report in seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── User Flow ─────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-eyebrow">User flow</div><div class="sec-title">Four steps from check-in to insight</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="flow-wrap">
      <div class="flow-step"><div class="fs-icon">📋</div><div class="fs-title">Assessment</div><div class="fs-sub">Daily wellness form — 6 inputs</div></div>
      <div class="flow-arrow">›</div>
      <div class="flow-step"><div class="fs-icon">🤖</div><div class="fs-title">Analysis</div><div class="fs-sub">5 AI agents in sequence</div></div>
      <div class="flow-arrow">›</div>
      <div class="flow-step"><div class="fs-icon">📊</div><div class="fs-title">Results</div><div class="fs-sub">Score, charts & advice</div></div>
      <div class="flow-arrow">›</div>
      <div class="flow-step"><div class="fs-icon">🕑</div><div class="fs-title">History</div><div class="fs-sub">Track trends over time</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Agents ────────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-eyebrow">AI architecture</div><div class="sec-title">Five specialized agents</div><div class="sec-body">Each agent focuses on a distinct wellness dimension. They run sequentially — each one feeding into the next — producing a holistic, evidence-backed report.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="agents-grid">
      <div class="agent-tile"><div class="a-icon">🫀</div><div><div class="a-name">Physical wellness agent</div><div class="a-desc">Analyzes sleep, hydration &amp; exercise against clinical targets</div></div></div>
      <div class="agent-tile"><div class="a-icon">🧠</div><div><div class="a-name">Mental stress agent</div><div class="a-desc">Classifies stress on a 1–10 scale; identifies severity tier</div></div></div>
      <div class="agent-tile"><div class="a-icon">📚</div><div><div class="a-name">Academic load agent</div><div class="a-desc">Assesses study hours and cognitive demand; flags burnout risk</div></div></div>
      <div class="agent-tile"><div class="a-icon">🔍</div><div><div class="a-name">RAG knowledge agent</div><div class="a-desc">Retrieves evidence from APA, Harvard Health &amp; peer-reviewed journals</div></div></div>
      <div class="agent-tile wide"><div class="a-icon">✨</div><div><div class="a-name">Recommendation agent</div><div class="a-desc">Synthesizes all agent outputs into a prioritized, personalized wellness action plan with High / Medium / Low priority labels and specific, actionable steps.</div></div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Inputs ────────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-eyebrow">What gets assessed</div><div class="sec-title">Six wellness inputs</div><div class="sec-body">Students complete a quick daily check-in. All fields are prefilled from the previous session so repeat check-ins take under 30 seconds.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metrics-grid">
      <div class="metric-tile"><div class="m-label">Sleep</div><div class="m-value" style="color:#00E5B0;">7–9 h</div><div class="m-sub">target per night</div></div>
      <div class="metric-tile"><div class="m-label">Stress</div><div class="m-value" style="color:#8B5CF6;">1 → 10</div><div class="m-sub">calm to overwhelmed</div></div>
      <div class="metric-tile"><div class="m-label">Study load</div><div class="m-value" style="color:#F59E0B;">≤ 6 h</div><div class="m-sub">optimal daily cap</div></div>
      <div class="metric-tile"><div class="m-label">Water</div><div class="m-value" style="color:#00E5B0;">8+ gl</div><div class="m-sub">250 ml glasses</div></div>
      <div class="metric-tile"><div class="m-label">Exercise</div><div class="m-value" style="color:#00E5B0;">30+ min</div><div class="m-sub">daily movement</div></div>
      <div class="metric-tile"><div class="m-label">Mood</div><div class="m-value" style="color:#5EEAD4;font-size:1.1rem;">5 levels</div><div class="m-sub">Excellent → Stressed</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Sample Output ─────────────────────────────────────────────────────────
    st.markdown('<div class="sec-eyebrow">Output preview</div><div class="sec-title">What the results dashboard shows</div><div class="sec-body">After analysis, students receive a scored wellness report with visual analytics and evidence-backed recommendations.</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="score-demo">
      <svg width="68" height="68" viewBox="0 0 68 68" role="img" aria-label="Sample wellness score 74">
        <circle cx="34" cy="34" r="28" fill="none" stroke="rgba(0,229,176,0.15)" stroke-width="6"/>
        <circle cx="34" cy="34" r="28" fill="none" stroke="#00E5B0" stroke-width="6"
          stroke-dasharray="175.9" stroke-dashoffset="47" stroke-linecap="round"
          transform="rotate(-90 34 34)"/>
        <text x="34" y="39" text-anchor="middle" font-size="15" font-weight="700" fill="#00E5B0" font-family="Space Grotesk,sans-serif">74</text>
      </svg>
      <div class="sd-info">
        <h4>Sample output — wellness score 74 / grade B</h4>
        <p>Physical status: Good · Stress class: High · Burnout risk: 38%</p>
        <div class="tags">
          <span class="tag tag-g">✓ Sleep on target</span>
          <span class="tag tag-y">⚠ Stress elevated</span>
          <span class="tag tag-r">↑ Study hours high</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    