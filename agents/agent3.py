# ============================================
# WELLMIND AI — Agent 3: Academic Load Agent
# Analyzes a student's study workload and burnout risk
# ============================================

from utils import ask_gemini

def _clamp(value, low=0, high=100):
    return max(low, min(high, int(round(value))))


def _burnout_risk(score):
    if score >= 85:
        return "Severe"
    if score >= 65:
        return "High"
    if score >= 35:
        return "Moderate"
    return "Low"


def _fallback_academic(study_hours, pending_deadlines, workload_rating, backlog_subjects, reason=""):
    deadline_score = min(100, int(pending_deadlines) * 12)
    workload_score = int(workload_rating) * 10
    backlog_score = min(100, int(backlog_subjects) * 18)
    study_pressure = 55 if study_hours < 2 and (pending_deadlines > 0 or backlog_subjects > 0) else min(100, float(study_hours) * 7)
    score = _clamp((deadline_score * 0.3) + (workload_score * 0.35) + (backlog_score * 0.25) + (study_pressure * 0.1))
    risk = _burnout_risk(score)

    observations = [
        f"{study_hours} study hours today is {'low for the current workload' if study_hours < 2 and pending_deadlines else 'a reasonable study base'}.",
        f"{pending_deadlines} pending deadline(s) and {workload_rating}/10 workload pressure create {risk.lower()} academic load.",
        f"{backlog_subjects} backlog subject(s) {'increase catch-up pressure' if backlog_subjects else 'keeps backlog pressure low'}.",
    ]
    recommendations = [
        "Use two focused 25-minute study blocks for the highest-priority subject.",
        "List deadlines by urgency and finish the smallest submit-ready task first.",
    ]
    if backlog_subjects:
        recommendations[1] = "Pick one backlog topic and schedule a fixed catch-up block today."

    result = {
        "academic_load_score": score,
        "burnout_risk": risk,
        "observations": observations,
        "study_recommendations": recommendations,
    }
    if reason:
        result["_fallback"] = True
        result["_fallback_reason"] = reason
    return result


def analyze_academic_load(study_hours, pending_deadlines, workload_rating, backlog_subjects):
    
    prompt = f"""
    You are Agent 3 of WellMind AI — Academic Load Analysis Agent for students.
    
    Student's academic workload today:
    - Study hours today: {study_hours} hours
    - Pending deadlines this week: {pending_deadlines}
    - Self-rated workload pressure: {workload_rating} out of 10
    - Subjects currently in backlog: {backlog_subjects}
    
    Analyze this and return ONLY a valid JSON object with exactly this structure:
    {{
        "academic_load_score": <number 0 to 100, higher means heavier load>,
        "burnout_risk": "<Low or Moderate or High or Severe>",
        "observations": [
            "<one sentence about their study hours>",
            "<one sentence about their deadline pressure>",
            "<one sentence about backlog impact>"
        ],
        "study_recommendations": [
            "<specific time management action>",
            "<another specific action to reduce load>"
        ]
    }}
    
    Return ONLY the JSON. No extra text. No explanation.
    """
    
    try:
        return ask_gemini(prompt)
    except Exception as exc:
        return _fallback_academic(study_hours, pending_deadlines, workload_rating, backlog_subjects, str(exc)[:160])


# ============================================
# TEST THE AGENT
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("WellMind AI — Agent 3: Academic Load")
    print("=" * 50)
    print("")
    print("Student Data Being Analyzed:")
    print("  Study Hours       : 2 hours")
    print("  Pending Deadlines : 4")
    print("  Workload Rating   : 9 / 10")
    print("  Backlog Subjects  : 2")
    print("")
    print("Agent 3 analyzing... please wait...")
    print("")

    result = analyze_academic_load(
        study_hours=2,
        pending_deadlines=3,
        workload_rating=9,
        backlog_subjects=2
    )

    print("AGENT 3 RESULT:")
    print("-" * 40)
    print(f"Academic Load Score : {result['academic_load_score']} / 100")
    print(f"Burnout Risk         : {result['burnout_risk']}")
    print("")
    print("Observations:")
    for i, obs in enumerate(result['observations'], 1):
        print(f"  {i}. {obs}")
    print("")
    print("Study Recommendations:")
    for i, rec in enumerate(result['study_recommendations'], 1):
        print(f"  {i}. {rec}")
    print("")
    print("=" * 50)
    print("Agent 3 completed successfully.")
    print("=" * 50)
