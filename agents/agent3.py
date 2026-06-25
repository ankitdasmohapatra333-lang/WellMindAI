# ============================================
# WELLMIND AI — Agent 3: Academic Load Agent
# Analyzes a student's study workload and burnout risk
# ============================================

from utils import ask_gemini

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
    
    return ask_gemini(prompt)


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
    print("  Pending Deadlines : 3")
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