from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

def chunk_docs(docs):
    chunker=RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )
    chunks=chunker.split_documents(docs)
    return chunks