import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from langgraph.graph import StateGraph, END
from typing import TypedDict
from app.rag.query_rewriter import rewrite_query
from app.rag.hybrid_retriever import hybrid_retrieve
from app.rag.page_reranker import rerank_documents
from app.db.create_vectordb import create_db
from app.core.config import create_client
from datetime import datetime

START_URL = "https://python.langchain.com/docs/"

vector_db_cache = create_db(START_URL)

class Graphstate(TypedDict):
    question: str
    rewritten_query: str
    answer: str
    context: str


def rewrite_node(state: Graphstate):
    rewritten = rewrite_query(state['question'])
    return {'rewritten_query': rewritten}


def retrieve_node(state: Graphstate):
    query = state.get('rewritten_query', state['question'])
    docs = hybrid_retrieve(query, k=8)
    reranked_docs = rerank_documents(query, docs)
    
    context_parts = []
    for i, doc in enumerate(reranked_docs[:5], 1):
        source = doc.metadata.get("source", "Unknown source")
        context_parts.append(f"[Document {i}] Source: {source}\n{doc.page_content}")
    
    context = "\n\n" + "="*60 + "\n\n".join(context_parts)
    return {'context': context}


def generate_node(state: Graphstate):
    client = create_client()
    
    prompt = f"""You are an expert technical documentation specialist with deep knowledge of software development.
Your task is to provide a comprehensive, professional response based ONLY on the provided documentation.

**IMPORTANT GUIDELINES:**
1. Base your answer exclusively on the provided context
2. Structure your response clearly with sections if needed
3. Include practical code examples when relevant
4. Provide step-by-step instructions for complex topics
5. Cite sources for each major point
6. If information is missing or unclear, explicitly state: \"This information is not covered in the provided documentation\"
7. Maintain a professional, technical tone
8. Be concise but complete

**User's Question:**
{state['question']}

**Relevant Documentation:**
{state['context']}

---
**Professional Response:**
"""
    
    response = client.models.generate_content(
        model=os.getenv("MODEL_NAME"),
        contents=prompt
    )
    return {"answer": response.text}


def build_graph():
    graph = StateGraph(Graphstate)
    graph.add_node("rewriter", rewrite_node)
    graph.add_node("retriever", retrieve_node)
    graph.add_node("generator", generate_node)
    
    graph.set_entry_point("rewriter")
    graph.add_edge("rewriter", "retriever")
    graph.add_edge("retriever", "generator")
    graph.add_edge("generator", END)

    return graph.compile()

app = build_graph()

if __name__ == "__main__":
    while True:
        question = input("\n> ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        if not question:
            continue
        
        result = app.invoke({'question': question, 'rewritten_query': '', 'answer': '', 'context': ''})
        print("\n" + "="*70)
        print(result['answer'])
        print("="*70 + "\n")