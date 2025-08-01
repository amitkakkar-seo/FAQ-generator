import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

def fetch_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

def fetch_page_snippet(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, 'html.parser')
        # Return visible text content (limit to 700 words)
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split()[:700])
    except Exception as e:
        return ""

def generate_internal_link_suggestions(pages_data):
    df = pd.DataFrame(pages_data)
    suggestions = []

    for i, row in df.iterrows():
        anchor_source = row['url']
        anchor_text = row['content']
        for j, target_row in df.iterrows():
            if i != j and target_row['url'] in anchor_text:
                continue  # avoid already existing links
            if i != j and target_row['content'].split()[0:5] == anchor_text.split()[0:5]:
                continue  # skip very similar content
            if i != j and len(set(anchor_text.lower().split()) & set(target_row['content'].lower().split())) > 10:
                suggestions.append({
                    'From URL': anchor_source,
                    'Suggested Anchor Text': ' '.join(target_row['content'].split()[:8]) + '...',
                    'Link To': target_row['url']
                })
    return pd.DataFrame(suggestions)

def fetch_reddit_questions(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.reddit.com/search/?q={keyword.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    questions = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if "?" in text and len(text) < 120:
            questions.append(text)
    return list(set(questions))[:10]

def fetch_quora_questions(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.quora.com/search?q={keyword.replace(' ', '+')}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    questions = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        if "?" in text and len(text) < 120:
            questions.append(text)
    return list(set(questions))[:10]
