from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(docs):
    chunker=RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )
    chunks=chunker.split_documents(docs)

    return chunks