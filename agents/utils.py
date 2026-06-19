# ============================================
# WELLMIND AI — Shared Utilities
# Functions used by every agent
# ============================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def ask_gemini(prompt):
    """
    Sends a prompt to Gemini and returns clean JSON.
    Every agent will use this one function.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Extract JSON even if Gemini adds extra text around it
    clean = re.search(r'\{.*\}', response.content, re.DOTALL).group()
    result = json.loads(clean)
    
    return result