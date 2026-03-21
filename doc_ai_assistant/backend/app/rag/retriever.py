from langchain_community.vectorstores import FAISS
from app.ingestion.embedder import embadding_model


def get_retriever():

    embeddings = embadding_model()

    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever