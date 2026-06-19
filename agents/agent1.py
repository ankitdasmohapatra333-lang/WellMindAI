# ============================================
# WELLMIND AI — Agent 1: Physical Wellness Agent
# This agent analyzes a student's physical health
# and returns a wellness score with observations
# ============================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import json

# Load your API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Connect to Gemini AI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key
)

# ============================================
# THE AGENT FUNCTION
# ============================================

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
    
    # Send prompt to Gemini and get response
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Convert response text to JSON
    #print("RAW RESPONSE:", response.content)
    #result = json.loads(response.content)
    import re
    clean = re.search(r'\{.*\}', response.content, re.DOTALL).group()
    result = json.loads(clean)
    
    return result


# ============================================
# TEST THE AGENT
# ============================================

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