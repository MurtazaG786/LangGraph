from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GOOGLE_API_KEY

def embadding_model():
    embadder=GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    return embadder