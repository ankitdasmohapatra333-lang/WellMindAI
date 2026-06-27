# ============================================
# WELLMIND AI — Agent 5: Recommendation Agent
# Synthesizes all other agents into one final, actionable report
# ============================================

from utils import ask_gemini

def _safe_int(value):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def _fallback_recommendation(physical_result, stress_result, academic_result, knowledge_result, reason=""):
    physical_score = _safe_int(physical_result.get("wellness_score"))
    stress_score = _safe_int(stress_result.get("stress_score"))
    academic_score = _safe_int(academic_result.get("academic_load_score"))

    high_risk = stress_score >= 75 or academic_score >= 75 or physical_score < 45
    moderate_risk = stress_score >= 50 or academic_score >= 50 or physical_score < 65
    if high_risk:
        overall = "Concerning"
    elif moderate_risk:
        overall = "Needs Attention"
    else:
        overall = "Stable"

    actions = []
    if physical_score < 65:
        actions.append("Protect tonight's sleep, hydrate, and add a short walk or stretch break.")
    if stress_score >= 50:
        actions.append("Use a three-minute breathing reset and write one controllable next step.")
    if academic_score >= 50:
        actions.append("Time-block the most urgent study task into two focused Pomodoro sessions.")
    actions.append("Review progress at the end of the day and keep tomorrow's plan realistic.")
    actions = actions[:3]

    takeaway = knowledge_result.get("key_takeaway", "Small routine improvements can improve wellbeing and academic focus.")
    summary = (
        f"Your current status is {overall.lower()} based on physical wellness, stress, and academic load. "
        f"{takeaway} Start with the priority actions and keep the plan simple for today."
    )
    escalation = stress_score >= 85 or str(stress_result.get("risk_level", "")).lower() == "severe"

    result = {
        "overall_status": overall,
        "priority_actions": actions,
        "summary": summary,
        "escalation_recommended": escalation,
        "escalation_reason": "Stress appears severe; speaking with a trusted adult, mentor, or counselor is recommended." if escalation else "",
    }
    if reason:
        result["_fallback"] = True
        result["_fallback_reason"] = reason
    return result


def generate_recommendation(physical_result, stress_result, academic_result, knowledge_result):
    
    prompt = f"""
    You are Agent 5 of WellMind AI — the Recommendation Agent.
    Your job is to synthesize findings from four specialist agents
    into one clear, warm, actionable summary for the student.
    
    Physical Wellness Agent found:
    - Score: {physical_result['wellness_score']}/100, Status: {physical_result['status']}
    - Observations: {physical_result['observations']}
    
    Mental Stress Agent found:
    - Score: {stress_result['stress_score']}/100, Risk: {stress_result['risk_level']}
    - Observations: {stress_result['observations']}
    
    Academic Load Agent found:
    - Score: {academic_result['academic_load_score']}/100, Burnout Risk: {academic_result['burnout_risk']}
    - Observations: {academic_result['observations']}
    
    Knowledge Agent (RAG-grounded evidence) found:
    - Key takeaway: {knowledge_result['key_takeaway']}
    
    Based on ALL of this combined, return ONLY a valid JSON object with exactly this structure:
    {{
        "overall_status": "<Stable or Needs Attention or Concerning>",
        "priority_actions": [
            "<most important action item right now>",
            "<second priority action item>",
            "<third priority action item>"
        ],
        "summary": "<a warm, encouraging 2-3 sentence summary combining all findings>",
        "escalation_recommended": <true or false>,
        "escalation_reason": "<brief reason if true, otherwise empty string>"
    }}
    
    Return ONLY the JSON. No extra text.
    """
    
    try:
        return ask_gemini(prompt)
    except Exception as exc:
        return _fallback_recommendation(physical_result, stress_result, academic_result, knowledge_result, str(exc)[:160])


# ============================================
# TEST THE AGENT
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("WellMind AI — Agent 5: Recommendation Agent")
    print("=" * 50)
    print("")
    
    sample_physical = {
        "wellness_score": 35, "status": "Poor",
        "observations": ["Only 5 hours sleep", "Low water intake", "No exercise"]
    }
    sample_stress = {
        "stress_score": 80, "risk_level": "High",
        "observations": ["High self-rated stress", "Anxious mood", "Exam pressure"]
    }
    sample_academic = {
        "academic_load_score": 85, "burnout_risk": "High",
        "observations": ["Low study hours vs deadlines", "3 pending deadlines", "Backlog subjects"]
    }
    sample_knowledge = {
        "key_takeaway": "Prioritizing sufficient sleep and a consistent routine are crucial for managing academic stress."
    }
    
    print("Agent 5 synthesizing all findings... please wait...")
    print("")
    
    result = generate_recommendation(sample_physical, sample_stress, sample_academic, sample_knowledge)
    
    print("AGENT 5 RESULT:")
    print("-" * 40)
    print(f"Overall Status: {result['overall_status']}")
    print("")
    print("Priority Actions:")
    for i, action in enumerate(result['priority_actions'], 1):
        print(f"  {i}. {action}")
    print("")
    print(f"Summary: {result['summary']}")
    print("")
    print(f"Escalation Recommended: {result['escalation_recommended']}")
    if result['escalation_recommended']:
        print(f"Reason: {result['escalation_reason']}")
    print("")
    print("=" * 50)
    print("Agent 5 completed successfully.")
    print("=" * 50)
