from app.ingestion.crawler import crawl_website
from app.ingestion.cleaner import clean_text
from langchain_core.documents import Document

def web_docs(START_URL):
    print(f"🌐 Starting web loading from {START_URL}...")
    uncleaned_docs=crawl_website(START_URL)
    print(f"🧹 Cleaning {len(uncleaned_docs)} documents...")
    docs=[]

    for i, page_dict in enumerate(uncleaned_docs):
        if (i + 1) % 10 == 0:
            print(f"  Processing {i + 1}/{len(uncleaned_docs)}...")
        cleaned_content=clean_text(page_dict["content"])
        docs.append(
            Document(
                page_content=cleaned_content,
                metadata={
                    "source": page_dict["url"]
                }
            )   
        )
    return docs