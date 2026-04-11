import google.genai as genai
import os


def rewrite_query(user_query: str) -> str:
    try:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        
        prompt = f"""You are a query optimization expert. Rewrite the following user query to make it clearer, more specific, and better for document retrieval.

Original Query: {user_query}

Your task:
1. Make the query more specific and detailed
2. Add relevant context and keywords
3. Clarify any ambiguous terms
4. Format as a single optimized query

Return ONLY the rewritten query, nothing else."""

        response = client.models.generate_content(
            model=os.getenv("MODEL_NAME", "gemini-pro"),
            contents=prompt
        )
        
        return response.text.strip()
        
    except Exception:
        return user_query
