# ============================================
# WELLMIND AI — Agent 2: Mental Stress Agent
# Analyzes a student's stress level and mood
# ============================================

from utils import ask_gemini

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
    
    return ask_gemini(prompt)


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