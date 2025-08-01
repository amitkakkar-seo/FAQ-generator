import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import defaultdict
import pandas as pd

def fetch_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.text, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    return urls

def fetch_page_snippet(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        snippet = " ".join([p.get_text() for p in paragraphs[:5]])
        return snippet.strip()
    except Exception:
        return ""

def generate_internal_link_suggestions(pages_data):
    suggestions = []
    for i, page in enumerate(pages_data):
        page_url = page["url"]
        page_content = page["content"].lower()

        for j, other_page in enumerate(pages_data):
            if i != j:
                other_url = other_page["url"]
                other_content = other_page["content"].lower()
                words = set(page_content.split()) & set(other_content.split())
                if len(words) > 10:  # shared words threshold
                    suggestions.append({
                        "Source Page": page_url,
                        "Suggested Link": other_url,
                        "Shared Terms": ", ".join(list(words)[:5])
                    })
    return pd.DataFrame(suggestions)

def fetch_reddit_questions(keyword):
    search_url = f"https://www.reddit.com/search/?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    questions = set()
    for h in soup.find_all("h3"):
        text = h.get_text(strip=True)
        if "?" in text and 10 < len(text) < 150:
            questions.add(text)
    return list(questions)[:10]

def fetch_quora_questions(keyword):
    search_url = f"https://www.quora.com/search?q={keyword.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    faqs = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if "?" in text and len(text) < 100:
            faqs.append(text)
    return list(set(faqs))[:10]
