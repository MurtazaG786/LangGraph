from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
import numpy as np


def calculate_relevance_score(query: str, document_content: str) -> float:
    try:
        embedder = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        
        query_embedding = embedder.embed_query(query)
        doc_embedding = embedder.embed_query(document_content[:500])
        
        query_vec = np.array(query_embedding)
        doc_vec = np.array(doc_embedding)
        
        similarity = np.dot(query_vec, doc_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(doc_vec)
        )
        
        score = (similarity + 1) / 2
        return score
        
    except Exception:
        return 0.5


def rerank_documents(query: str, documents: List) -> List:
    if not documents:
        return documents
    
    scored_docs = []
    for doc in documents:
        score = calculate_relevance_score(query, doc.page_content)
        scored_docs.append((doc, score))
    
    scored_docs.sort(key=lambda x: x[1], reverse=True)
    
    return [doc for doc, score in scored_docs]
