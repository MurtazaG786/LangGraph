from langchain_community.vectorstores import FAISS
from app.core.config import create_embadding_model
import os
from pathlib import Path

# Use same absolute path as create_vectordb.py
DB_PATH = os.path.join(str(Path.home()), ".rag_cache", "FAISS_DB")

def create_retriever():
    embedder=create_embadding_model()

    vectore_store=FAISS.load_local(
        DB_PATH,
        embedder,
        allow_dangerous_deserialization=True
    )
    retriever=vectore_store.as_retriever(
        search_kwargs={"k":4}
    )
    return retriever