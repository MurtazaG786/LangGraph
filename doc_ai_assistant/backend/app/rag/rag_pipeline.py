from app.rag.retriever import get_retriever
import google.genai as genai
from app.core.config import GOOGLE_API_KEY
retriever=get_retriever()
def generate_answer(question):
    docs=retriever.invoke(question)
    context="\n\n".join(
        doc.page_content for doc in docs
    )
    client=genai.Client(api_key=GOOGLE_API_KEY)
    prompt=f"""You are an AI assistant for website documentation.

Answer the user's question using ONLY the context below.

If answer not found, say:
"I could not find this in the documentation."

Context:
{context}

Question:
{question}

Answer:
"""
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
if __name__ == "__main__":

    while True:

        q = input("\nAsk: ")

        answer = generate_answer(q)

        print("\nAI:", answer)