# test_gemini.py
# This is your first AI code ever.
# It connects to Gemini and asks it a question.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load your API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Connect to Gemini AI
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key
)

# Ask Gemini a question
print("Connecting to Gemini AI...")
print("Asking question...")
print("")

response = llm.invoke([HumanMessage(
    content="Say hello and tell me you are the WellMind AI system in 2 sentences."
)])

print("GEMINI RESPONSE:")
print(response.content)
print("")
print("SUCCESS! Your AI connection is working.")