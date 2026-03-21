from langchain_community.vectorstores import FAISS

from app.ingestion.chunker import chunk_docs
from app.ingestion.embedder import embadding_model
from app.ingestion.loader import load_documents

def create_vector_store():
    docs =load_documents()
    chunks=chunk_docs(docs)
    embadder=embadding_model()

    vectorstore=FAISS.from_documents(
        chunks,
        embadder
    )
    vectorstore.save_local("faiss_index")
    print("Chunks created:", len(chunks))
    print("FAISS index saved")

    return vectorstore


if __name__ == "__main__":

    create_vector_store()