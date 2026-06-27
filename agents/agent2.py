# ============================================
# WELLMIND AI — Agent 2: Mental Stress Agent
# Analyzes a student's stress level and mood
# ============================================

from utils import ask_gemini

def _clamp(value, low=0, high=100):
    return max(low, min(high, int(round(value))))


def _risk_level(score):
    if score >= 85:
        return "Severe"
    if score >= 65:
        return "High"
    if score >= 35:
        return "Moderate"
    return "Low"


def _fallback_mental(stress_level, mood, stress_cause, reason=""):
    mood_text = str(mood or "Unknown")
    mood_lower = mood_text.lower()
    mood_weight = {
        "calm": -12,
        "motivated": -8,
        "anxious": 12,
        "low": 15,
        "irritable": 14,
    }.get(mood_lower, 5)
    cause_text = (stress_cause or "Not specified").strip()
    cause_weight = 8 if cause_text.lower() not in {"not specified", "none", "no issues", "nothing"} else 0
    score = _clamp((int(stress_level) * 10) + mood_weight + cause_weight)
    risk = _risk_level(score)

    observations = [
        f"A stress rating of {stress_level}/10 indicates {risk.lower()} current pressure.",
        f"The reported mood, {mood_text}, {'may need extra care today' if mood_lower in {'anxious', 'low', 'irritable'} else 'is a helpful protective signal'}.",
        f"The main stress cause is {cause_text}, so the next step should focus on what is controllable.",
    ]
    recommendations = [
        "Use 4-4-6 breathing for three minutes before returning to study.",
        "Write one controllable next action and one worry to park for later.",
    ]
    if score >= 80:
        recommendations[1] = "Talk to a trusted person or counselor if this intensity continues today."

    result = {
        "stress_score": score,
        "risk_level": risk,
        "observations": observations,
        "coping_recommendations": recommendations,
    }
    if reason:
        result["_fallback"] = True
        result["_fallback_reason"] = reason
    return result


def analyze_mental_stress(stress_level, mood, stress_cause):
    
    prompt = f"""
    You are Agent 2 of WellMind AI — Mental Stress Analysis Agent for students.
    
    Student's mental state today:
    - Self-rated stress level: {stress_level} out of 10
    - Current mood: {mood}
    - What's causing stress: {stress_cause}
    
    Analyze this and return ONLY a valid JSON object with exactly this structure:
    {{
        "stress_score": <number 0 to 100, higher means more stressed>,
        "risk_level": "<Low or Moderate or High or Severe>",
        "observations": [
            "<one sentence interpreting their stress level>",
            "<one sentence about their mood>",
            "<one sentence about the stress cause they mentioned>"
        ],
        "coping_recommendations": [
            "<specific coping technique relevant to their situation>",
            "<another specific coping technique>"
        ]
    }}
    
    Return ONLY the JSON. No extra text. No explanation.
    """
    
    try:
        return ask_gemini(prompt)
    except Exception as exc:
        return _fallback_mental(stress_level, mood, stress_cause, str(exc)[:160])


# ============================================
# TEST THE AGENT
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("WellMind AI — Agent 2: Mental Stress")
    print("=" * 50)
    print("")
    print("Student Data Being Analyzed:")
    print("  Stress Level : 8 / 10")
    print("  Mood         : Anxious")
    print("  Cause        : Upcoming exams and project deadline")
    print("")
    print("Agent 2 analyzing... please wait...")
    print("")

    result = analyze_mental_stress(
        stress_level=8,
        mood="Anxious",
        stress_cause="Upcoming exams and project deadline"
    )

    print("AGENT 2 RESULT:")
    print("-" * 40)
    print(f"Stress Score : {result['stress_score']} / 100")
    print(f"Risk Level   : {result['risk_level']}")
    print("")
    print("Observations:")
    for i, obs in enumerate(result['observations'], 1):
        print(f"  {i}. {obs}")
    print("")
    print("Coping Recommendations:")
    for i, rec in enumerate(result['coping_recommendations'], 1):
        print(f"  {i}. {rec}")
    print("")
    print("=" * 50)
    print("Agent 2 completed successfully.")
    print("=" * 50)
