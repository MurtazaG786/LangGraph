import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.genai as genai


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

st.title("PDF RAG – From Scratch")

pdf_file = st.file_uploader("Upload a PDF", type="pdf")
user_question = st.text_input("Ask a question")

prompt = PromptTemplate.from_template(
    """
You are a question answering system.
Answer the question using ONLY the context below.
If the answer is not present in the context, say "I don't know".

Context:
{context}

Question:
{input}
"""
)


def create_vectordb(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def call_llm(prompt_text: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_text
    )
    return response.text

def rag_chain(question: str, retriever):
    docs = retriever.invoke(question)

    context = format_docs(docs)
    final_prompt = prompt.format(
        context=context,
        input=question
    )
    return call_llm(final_prompt)

if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(pdf_file.getbuffer())
        tmp.flush()
        pdf_path = tmp.name

    vector_store = create_vectordb(pdf_path)
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    st.success("PDF processed and indexed.")

    if user_question:
        answer = rag_chain(user_question, retriever)
        st.subheader("Answer")
        st.write(answer)