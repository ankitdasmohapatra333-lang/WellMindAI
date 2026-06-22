# ============================================
# WELLMIND AI — Agent 4: RAG Retrieval Agent
# This agent retrieves relevant knowledge base
# context based on Agent 1-3 outputs / query
# ============================================
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="wellmind_kb")

# ============================================
# THE AGENT FUNCTION
# ============================================
def retrieve_relevant_context(query, n_results=5):
    """
    Agent 4 of WellMind AI — RAG Retrieval Agent.
    Takes a query (built from Agent 1-3 outputs), 
    returns relevant knowledge base chunks as structured JSON.
    """
    results = collection.query(query_texts=[query], n_results=n_results)
    
    retrieved_context = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        retrieved_context.append({
            "source": meta['source'],
            "content": doc
        })
    
    return {
        "query": query,
        "retrieved_context": retrieved_context,
        "num_results": len(retrieved_context)
    }

# ============================================
# TEST THE AGENT
# ============================================
print("=" * 50)
print("WellMind AI — Agent 4: RAG Retrieval")
print("=" * 50)
print("")

# Simulate a query built from Agent 1-3 outputs
test_query = "Student has low sleep, high stress, and heavy academic workload"

print(f"Query: {test_query}")
print("")
print("Agent 4 retrieving context... please wait...")
print("")

result = retrieve_relevant_context(test_query, n_results=5)

print("AGENT 4 RESULT:")
print("-" * 40)
print(f"Total chunks retrieved: {result['num_results']}")
print("")
for i, ctx in enumerate(result['retrieved_context'], 1):
    print(f"{i}. [{ctx['source']}]")
    print(f"   {ctx['content'][:150]}...")
    print("")

print("=" * 50)
print("Agent 4 completed successfully.")
print("=" * 50)