from typing import TypedDict
from langgraph.graph import StateGraph,END
import google.genai as genai
from app.core.config import GOOGLE_API_KEY
from app.rag.retriever import get_retriever

class GraphState(TypedDict):
    question:str
    context:str
    answer:str

def retrieve_node(state:GraphState):
    docs=get_retriever.invoke(state["question"])
    context="\n\n".join(
    doc.page_content for doc in docs)
    return {
        "context":context   
    }

def generate_answer(state:GraphState):
    
    client=genai.Client(api_key=GOOGLE_API_KEY)
    prompt=f"""You are an AI assistant for website documentation.

Answer the user's question using ONLY the context below.

If answer not found, say:
"I could not find this in the documentation."

Context:
{state["context"]}

Question:
{state["question"]}

Answer:
"""
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {
        "answer":response.text
    }

def build_graph():
    graph=StateGraph(GraphState)
    graph.add_node("retrieve",retrieve_node)
    graph.add_node("ans genration",generate_answer)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve","ans genration")
    graph.add_edge("ans genration",END)
    return graph.compile()

if __name__=="__main__":
    app=build_graph()
    while True:

        q = input("\nAsk: ")

        result = app.invoke(
            {"question": q}
        )

        print("\nAI:", result["answer"])