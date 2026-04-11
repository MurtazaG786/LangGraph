from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from app.core.config import create_embadding_model
import os
from pathlib import Path


DB_PATH = os.path.join(str(Path.home()), ".rag_cache", "FAISS_DB")


def create_hybrid_retriever(k: int = 6):
    try:
        embedder = create_embadding_model()
        
        vector_store = FAISS.load_local(
            DB_PATH,
            embedder,
            allow_dangerous_deserialization=True
        )
        all_docs = vector_store.docstore._dict.values()
        doc_list = list(all_docs)

        semantic_retriever = vector_store.as_retriever(
            search_kwargs={"k": k}
        )
        bm25_retriever = BM25Retriever.from_documents(
            doc_list,
            k=k
        )        
        return {
            "semantic": semantic_retriever,
            "bm25": bm25_retriever,
            "all_docs": doc_list
        }
        
    except Exception:
        return None


def hybrid_retrieve(query: str, k: int = 6):
    retriever_dict = create_hybrid_retriever(k=k)
    
    if not retriever_dict:
        return []
    
    semantic_docs = retriever_dict["semantic"].invoke(query)
    bm25_docs = retriever_dict["bm25"].invoke(query)
    
    seen = {}
    combined_docs = []
    
    for doc in semantic_docs:
        doc_hash = doc.page_content[:100]
        if doc_hash not in seen:
            seen[doc_hash] = True
            combined_docs.append(doc)
    
    for doc in bm25_docs:
        doc_hash = doc.page_content[:100]
        if doc_hash not in seen:
            seen[doc_hash] = True
            combined_docs.append(doc)    
    return combined_docs
