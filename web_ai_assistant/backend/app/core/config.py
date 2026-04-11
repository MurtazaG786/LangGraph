from dotenv import load_dotenv
import google.genai as genai
import os
from langchain_huggingface import HuggingFaceEmbeddings
import warnings
import logging

warnings.filterwarnings("ignore", message=".*embeddings.position_ids.*")
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

load_dotenv()

def create_client():
    try:
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if GOOGLE_API_KEY:
            return genai.Client(api_key=GOOGLE_API_KEY)
        return None
    except Exception:
        return None
    
def create_embadding_model():
    try:
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
    except Exception:
        return None
    
