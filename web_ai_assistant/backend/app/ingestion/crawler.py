import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


visited_urls = set()

def crawl_website(start_url, max_pages=120):

    to_visit = [start_url]

    pages = []

    print(f"🕷️  Starting crawl of {start_url} (max {max_pages} pages)...")

    while to_visit and len(pages) < max_pages:

        url = to_visit.pop(0)

        if url in visited_urls:
            continue

        try:
            print(f"  📄 Crawling ({len(pages)}/{max_pages}): {url[:60]}...")

            res = requests.get(url, timeout=10)

            if res.status_code != 200:
                continue

            soup = BeautifulSoup(res.text, "lxml")

            main_content = extract_main_content(soup)

            pages.append({
                "url": url,
                "content": main_content
            })

            visited_urls.add(url)

            links = soup.find_all("a", href=True)

            for link in links:

                absolute = urljoin(url, link["href"])

                if is_valid_link(absolute, start_url):

                    to_visit.append(absolute)

        except requests.Timeout:
            print(f"  ⏱️  Timeout: {url}")
            continue

        except Exception as e:

            print(f"  ❌ Crawl error {url}: {str(e)[:50]}")
            continue

    print(f"✅ Crawl complete: {len(pages)} pages collected")
    return pages



def extract_main_content(soup):

    selectors = [
        "main",
        "article",
        "div[class*='content']",
        "div[class*='markdown']",
        "div[class*='article']"
    ]

    for selector in selectors:

        section = soup.select_one(selector)

        if section:

            return section.get_text("\n")

    return soup.get_text("\n")



def is_valid_link(url, base):

    parsed_base = urlparse(base)

    parsed_url = urlparse(url)

    return parsed_url.netloc == parsed_base.netloc
