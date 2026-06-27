# ============================================
# WELLMIND AI — Agent 1: Physical Wellness Agent
# This agent analyzes a student's physical health
# and returns a wellness score with observations
# ============================================

from utils import ask_gemini

# ============================================
# THE AGENT FUNCTION
# ============================================

def _clamp(value, low=0, high=100):
    return max(low, min(high, int(round(value))))


def _status(score):
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Good"
    if score >= 45:
        return "Fair"
    return "Poor"


def _fallback_physical(sleep_hours, water_glasses, exercise_minutes, meals_today, reason=""):
    sleep_score = max(0, 100 - abs(float(sleep_hours) - 8) * 18)
    water_score = min(100, (int(water_glasses) / 8) * 100)
    exercise_score = min(100, (int(exercise_minutes) / 30) * 100)
    meal_score = 100 if meals_today >= 3 else 65 if meals_today == 2 else 35 if meals_today == 1 else 10
    score = _clamp((sleep_score * 0.35) + (water_score * 0.25) + (exercise_score * 0.25) + (meal_score * 0.15))

    observations = [
        f"{sleep_hours} hours of sleep is {'in the healthy range' if 7 <= sleep_hours <= 9 else 'outside the ideal 7-9 hour range for most students'}.",
        f"{water_glasses} glasses of water suggests {'good hydration' if water_glasses >= 7 else 'hydration could be improved today'}.",
        f"{exercise_minutes} minutes of movement is {'a strong activity start' if exercise_minutes >= 30 else 'below the usual daily movement target'}.",
    ]
    actions = []
    if sleep_hours < 7:
        actions.append("Aim for an earlier bedtime tonight and avoid screens for the last 30 minutes.")
    elif sleep_hours > 9:
        actions.append("Keep wake-up time consistent tomorrow to protect your routine.")
    if water_glasses < 7:
        actions.append("Drink 2-3 more glasses of water across the next few hours.")
    if exercise_minutes < 30:
        actions.append("Take a 10-15 minute walk or stretch break today.")
    if meals_today < 3:
        actions.append("Add a balanced meal or snack with protein and complex carbohydrates.")
    actions = actions[:2] or ["Keep your current routine steady today.", "Take one short recovery break between study blocks."]

    result = {
        "wellness_score": score,
        "status": _status(score),
        "observations": observations,
        "immediate_actions": actions,
    }
    if reason:
        result["_fallback"] = True
        result["_fallback_reason"] = reason
    return result


def analyze_physical_wellness(sleep_hours, water_glasses, exercise_minutes, meals_today):
    
    prompt = f"""
    You are Agent 1 of WellMind AI — Physical Wellness Analysis Agent for students.
    
    Student's daily physical health data:
    - Sleep last night: {sleep_hours} hours
    - Water intake: {water_glasses} glasses
    - Exercise today: {exercise_minutes} minutes
    - Meals eaten today: {meals_today}
    
    Analyze this and return ONLY a valid JSON object with exactly this structure:
    {{
        "wellness_score": <number 0 to 100>,
        "status": "<Excellent or Good or Fair or Poor>",
        "observations": [
            "<one sentence about their sleep>",
            "<one sentence about their hydration>",
            "<one sentence about their exercise>"
        ],
        "immediate_actions": [
            "<specific action they should take today>",
            "<another specific action they should take today>"
        ]
    }}
    
    Return ONLY the JSON. No extra text. No explanation.
    """
    
    try:
        return ask_gemini(prompt)
    except Exception as exc:
        return _fallback_physical(sleep_hours, water_glasses, exercise_minutes, meals_today, str(exc)[:160])


# ============================================
# TEST THE AGENT
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("WellMind AI — Agent 1: Physical Wellness")
    print("=" * 50)
    print("")
    print("Student Data Being Analyzed:")
    print("  Sleep    : 5 hours")
    print("  Water    : 3 glasses")
    print("  Exercise : 0 minutes")
    print("  Meals    : 2")
    print("")
    print("Agent 1 analyzing... please wait...")
    print("")

    # Run the agent with test data
    result = analyze_physical_wellness(
        sleep_hours=5,
        water_glasses=3,
        exercise_minutes=0,
        meals_today=2
    )

    # Display the result clearly
    print("AGENT 1 RESULT:")
    print("-" * 40)
    print(f"Wellness Score  : {result['wellness_score']} / 100")
    print(f"Status          : {result['status']}")
    print("")
    print("Observations:")
    for i, obs in enumerate(result['observations'], 1):
        print(f"  {i}. {obs}")
    print("")
    print("Immediate Actions:")
    for i, action in enumerate(result['immediate_actions'], 1):
        print(f"  {i}. {action}")
    print("")
    print("=" * 50)
    print("Agent 1 completed successfully.")
    print("=" * 50)
