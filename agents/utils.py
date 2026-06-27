# ============================================
# WELLMIND AI — Shared Utilities
# Functions used by every agent
# Auto-failover: Gemini → Groq when quota is hit
# ============================================

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
import json
import re
import time

# Try importing Groq — it's optional
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Providers are only usable when their package/key is present.
GEMINI_READY = bool(GEMINI_API_KEY) and GEMINI_API_KEY.lower() not in {"your_key_here", "your_gemini_api_key"}
GROQ_READY = GROQ_AVAILABLE and bool(GROQ_API_KEY) and GROQ_API_KEY.lower() not in {"your_key_here", "your_groq_api_key"}

# Demo-safe retry settings. Keep these short so the UI cannot appear stuck.
MAX_RETRIES = max(1, int(os.getenv("WELLMIND_LLM_RETRIES", "1")))
BASE_DELAY = float(os.getenv("WELLMIND_LLM_RETRY_DELAY", "1"))
LLM_TIMEOUT_SECONDS = float(os.getenv("WELLMIND_LLM_TIMEOUT", "12"))
LLM_DISABLED = os.getenv("WELLMIND_DISABLE_LLM", "").lower() in {"1", "true", "yes", "on"}

# Track which provider is active (shared across all agents in the same process)
_provider_state = {
    "current": "gemini",
    "switched": False,
    "switch_reason": "",
}


def get_provider_state():
    """Returns the current provider state dict."""
    return _provider_state


def _is_retryable_error(error_msg):
    """Check if an error message indicates a quota / rate-limit / transient issue."""
    lower_msg = error_msg.lower()
    return any(
        keyword in lower_msg
        for keyword in [
            "429", "resource_exhausted", "quota", "rate limit", "rate_limit",
            "503", "unavailable", "high demand", "overloaded", "capacity",
            "temporarily", "service unavailable", "internal error", "500",
        ]
    )


def _make_llm(provider):
    """Create a LangChain LLM for the given provider."""
    if provider == "groq":
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=GROQ_API_KEY,
            temperature=0.3,
            timeout=LLM_TIMEOUT_SECONDS,
            max_retries=0,
        )
    else:
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=GEMINI_API_KEY,
            temperature=0.3,
            timeout=LLM_TIMEOUT_SECONDS,
            max_retries=0,
        )


def _call_llm(provider, prompt):
    """Call the LLM and return the parsed JSON dict."""
    llm = _make_llm(provider)
    response = llm.invoke([HumanMessage(content=prompt)])
    content = str(response.content or "").strip()
    content = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.IGNORECASE | re.DOTALL)
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if not match:
        raise ValueError(f"LLM ({provider}) returned no JSON object. Raw response: {content[:200]}")
    return json.loads(match.group())


def ask_gemini(prompt):
    """
    Sends a prompt to the active LLM and returns clean JSON.

    Flow:
      1. Try Gemini with retry + backoff
      2. If Gemini quota exhausted AND Groq is available → switch to Groq
      3. If Groq also fails or is not available → raise the error
    """
    if LLM_DISABLED:
        raise RuntimeError("LLM calls are disabled by WELLMIND_DISABLE_LLM.")

    # Build the list of providers to try. Prefer the current provider after failover.
    providers = []
    if _provider_state["current"] == "groq" and GROQ_READY:
        providers.append("groq")
    if GEMINI_READY and "gemini" not in providers:
        providers.append("gemini")
    if GROQ_READY:
        providers.append("groq")
    providers = list(dict.fromkeys(providers))

    if not providers:
        raise RuntimeError("No LLM API key is configured. Add GEMINI_API_KEY or GROQ_API_KEY, or use fallback mode.")

    for provider in providers:
        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                result = _call_llm(provider, prompt)

                # If we switched provider, record it
                if provider != _provider_state["current"]:
                    old = _provider_state["current"]
                    _provider_state["current"] = provider
                    _provider_state["switched"] = True
                    _provider_state["switch_reason"] = (
                        f"{old.capitalize()} quota exhausted — switched to {provider.capitalize()}"
                    )
                    print(f"[WellMind] Auto-switched from {old} to {provider}")

                return result

            except Exception as e:
                error_msg = str(e)
                last_error = e

                if _is_retryable_error(error_msg) and attempt < MAX_RETRIES - 1:
                    delay = BASE_DELAY * (2 ** attempt)
                    print(f"[WellMind] {provider.capitalize()} error (attempt {attempt + 1}/{MAX_RETRIES}): {error_msg[:120]}. Retrying in {delay}s...")
                    time.sleep(delay)
                    continue

                if _is_retryable_error(error_msg):
                    print(f"[WellMind] {provider.capitalize()} exhausted after {MAX_RETRIES} attempts. Trying next provider...")
                    break

                # Non-retryable error — raise immediately
                raise

    # All providers failed
    raise last_error
