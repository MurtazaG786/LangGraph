from langchain_community.vectorstores import FAISS
from app.ingestion.web_loader import web_docs
from app.rag.chunker import create_chunks
from app.core.config import create_embadding_model
import os
import shutil
from pathlib import Path

DB_PATH = os.path.join(str(Path.home()), ".rag_cache", "FAISS_DB")

def create_db(url):
    os.makedirs(DB_PATH, exist_ok=True)
    
    index_file = os.path.join(DB_PATH, "index.faiss")
    pkl_file = os.path.join(DB_PATH, "index.pkl")
    
    if os.path.exists(index_file) and os.path.exists(pkl_file):
        try:
            embedder = create_embadding_model()
            vector_db = FAISS.load_local(
                DB_PATH,
                embedder,
                allow_dangerous_deserialization=True
            )
            return vector_db
        except Exception:
            if os.path.exists(DB_PATH):
                shutil.rmtree(DB_PATH)
                os.makedirs(DB_PATH, exist_ok=True)
    else:
        if os.path.exists(DB_PATH):
            shutil.rmtree(DB_PATH)
            os.makedirs(DB_PATH, exist_ok=True)
    
    docs = web_docs(url)
    chunks = create_chunks(docs)
    embedder = create_embadding_model()
    vector_db = FAISS.from_documents(chunks, embedder)
    vector_db.save_local(DB_PATH)
    return vector_db