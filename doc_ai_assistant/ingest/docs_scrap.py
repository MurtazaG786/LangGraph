import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# ---------- TEXT CLEANER ----------

def clean_text(text):

    # remove multiple spaces/newlines/tabs
    text = re.sub(r'\s+', ' ', text)

    # remove common navigation garbage
    garbage_words = [
        "Skip to content",
        "Table of contents",
        "Sponsors",
        "Follow",
        "Join",
        "newsletter",
        "LinkedIn",
        "Twitter"
    ]

    for word in garbage_words:
        text = text.replace(word, "")

    return text.strip()


# ---------- PAGE SCRAPER ----------

def scrape_page(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # remove scripts/styles
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # try to get main content
    main = soup.find("main")

    if main:
        text = main.get_text(separator=" ")
    else:
        text = soup.get_text(separator=" ")

    text = clean_text(text)

    return text


# ---------- LINK EXTRACTOR ----------

def get_links(url, domain):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):

        link = urljoin(url, a["href"])

        if domain in link:
            links.add(link)

    return list(links)


# ---------- WEBSITE CRAWLER ----------

def crawl_docs(start_url, max_pages=20):

    domain = urlparse(start_url).netloc

    visited = set()
    to_visit = [start_url]

    documents = []

    while to_visit and len(visited) < max_pages:

        url = to_visit.pop(0)

        if url in visited:
            continue

        print("Scraping:", url)

        try:

            text = scrape_page(url)

            documents.append({
                "url": url,
                "content": text
            })

            visited.add(url)

            links = get_links(url, domain)

            for link in links:
                if link not in visited:
                    to_visit.append(link)

        except Exception as e:
            print("Error:", e)

    return documents


# ---------- RUN SCRAPER ----------

if __name__ == "__main__":

    start_url = "https://fastapi.tiangolo.com/"

    docs = crawl_docs(start_url, max_pages=10)

    import json

    with open("docs.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)

    print("Saved", len(docs), "documents.")