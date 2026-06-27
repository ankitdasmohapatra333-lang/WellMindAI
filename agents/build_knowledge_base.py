# ============================================
# WELLMIND AI — Build Knowledge Base in ChromaDB
# Run this ONCE to create your vector database
# ============================================

import chromadb
from knowledge_base import WELLNESS_KNOWLEDGE

# Create a persistent database — saved to disk, not memory
client = chromadb.PersistentClient(path="./chroma_db")

# Create (or reuse) a collection — like a table for our knowledge
collection = client.get_or_create_collection(name="wellness_knowledge")

# Generate simple IDs: doc0, doc1, doc2...
ids = [f"doc{i}" for i in range(len(WELLNESS_KNOWLEDGE))]

# Add all knowledge snippets — ChromaDB converts each to a vector automatically
collection.add(
    documents=WELLNESS_KNOWLEDGE,
    ids=ids
)

print(f"Knowledge base built successfully with {len(WELLNESS_KNOWLEDGE)} entries.")
print("")

# Quick test — search the knowledge base
print("Testing retrieval with query: 'student not sleeping well and stressed about exams'")
print("-" * 50)

results = collection.query(
    query_texts=["student not sleeping well and stressed about exams"],
    n_results=3
)

for i, doc in enumerate(results['documents'][0], 1):
    print(f"{i}. {doc}")
    print("")