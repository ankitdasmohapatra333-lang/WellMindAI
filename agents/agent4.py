# ============================================
# WELLMIND AI — Agent 4: RAG Knowledge Agent
# Retrieves verified wellness knowledge before generating advice
# ============================================

import chromadb
from utils import ask_gemini
from knowledge_base import WELLNESS_KNOWLEDGE

# Connect to the same persistent database we built
import os
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")
try:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name="wellness_knowledge")
except Exception as exc:
    print(f"[WellMind] Chroma knowledge base unavailable; using built-in knowledge. {exc}")
    collection = None


def retrieve_knowledge(query, n_results=3):
    """The 'Retrieval' part of RAG — searches the knowledge base."""
    if collection is None:
        terms = set(str(query).lower().replace(",", " ").split())
        ranked = sorted(
            WELLNESS_KNOWLEDGE,
            key=lambda item: sum(1 for term in terms if term and term in item.lower()),
            reverse=True,
        )
        return ranked[:n_results]

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results['documents'][0]


def _fallback_knowledge(query, retrieved_chunks, reason=""):
    lower_query = str(query).lower()
    evidence = retrieved_chunks[:2] or WELLNESS_KNOWLEDGE[:2]
    if "stress" in lower_query or "burnout" in lower_query:
        takeaway = "A steady routine, short recovery breaks, and focused study blocks can reduce stress while protecting academic progress."
    elif "sleep" in lower_query:
        takeaway = "Improving sleep consistency is likely to support concentration, mood, and recovery."
    else:
        takeaway = "Small daily habits across sleep, hydration, movement, and planning can improve student wellbeing."

    result = {
        "relevant_evidence": evidence[:2],
        "key_takeaway": takeaway,
        "retrieved_sources": retrieved_chunks,
    }
    if reason:
        result["_fallback"] = True
        result["_fallback_reason"] = reason
    return result


def rag_knowledge_agent(query):
    """
    Full RAG process:
    1. Retrieve relevant knowledge from ChromaDB
    2. Send that knowledge + query to Gemini
    3. Get a response grounded in real evidence
    """
    
    # Step 1: RETRIEVE
    retrieved_chunks = retrieve_knowledge(query, n_results=3)
    context = "\n".join([f"- {chunk}" for chunk in retrieved_chunks])
    
    # Step 2: GENERATE (grounded in retrieved context)
    prompt = f"""
    You are Agent 4 of WellMind AI — the RAG Knowledge Agent.
    
    A student's wellness concern: {query}
    
    Verified wellness knowledge retrieved from the knowledge base:
    {context}
    
    Based ONLY on the retrieved knowledge above, return ONLY a valid JSON object:
    {{
        "relevant_evidence": [
            "<first key fact from the retrieved knowledge, in plain language>",
            "<second key fact from the retrieved knowledge, in plain language>"
        ],
        "key_takeaway": "<one sentence summarizing what this evidence means for this student>"
    }}
    
    Return ONLY the JSON. No extra text.
    """
    
    try:
        result = ask_gemini(prompt)
        result["retrieved_sources"] = retrieved_chunks
        return result
    except Exception as exc:
        return _fallback_knowledge(query, retrieved_chunks, str(exc)[:160])


# ============================================
# TEST THE AGENT
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("WellMind AI — Agent 4: RAG Knowledge Agent")
    print("=" * 50)
    print("")

    test_query = "Student sleeping only 5 hours, stress level 8/10, heavy academic deadlines"
    print(f"Query: {test_query}")
    print("")
    print("Agent 4 retrieving knowledge and analyzing... please wait...")
    print("")

    result = rag_knowledge_agent(test_query)

    print("AGENT 4 RESULT:")
    print("-" * 40)
    print("Relevant Evidence:")
    for i, fact in enumerate(result['relevant_evidence'], 1):
        print(f"  {i}. {fact}")
    print("")
    print(f"Key Takeaway: {result['key_takeaway']}")
    print("")
    print("Retrieved Sources (raw):")
    for i, src in enumerate(result['retrieved_sources'], 1):
        print(f"  [{i}] {src[:80]}...")
    print("")
    print("=" * 50)
    print("Agent 4 completed successfully — RAG pipeline working.")
    print("=" * 50)
