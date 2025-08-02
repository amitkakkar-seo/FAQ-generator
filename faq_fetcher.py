import requests
import openai
from bs4 import BeautifulSoup
import streamlit as st

SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

headers = {
    "User-Agent": "Mozilla/5.0"
}

def fetch_google_faqs(keyword):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get(url, params=params)
    data = response.json()
    faqs = []
    if "related_questions" in data:
        faqs = [q.get("question") for q in data["related_questions"] if q.get("question")]
    return faqs

def fetch_chatgpt_faqs(keyword):
    try:
        prompt = f"Generate a list of 10 frequently asked questions about '{keyword}'."
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        content = response.choices[0].message.content
        return [q.strip("•- ").strip() for q in content.strip().split("\n") if q.strip()]
    except Exception as e:
        st.error(f"❌ ChatGPT Error: {str(e)}")
        return []

def fetch_quora_faqs(keyword):
    search_url = f"https://www.quora.com/search?q={keyword.replace(' ', '+')}"
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]
        threads = [f"https://www.quora.com{link}" for link in links if "/What" in link or "/Why" in link or "/How" in link]
        return list(set(threads))[:5]
    except Exception as e:
        st.error(f"❌ Quora Error: {str(e)}")
        return []

def fetch_reddit_faqs(keyword):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": f"site:reddit.com {keyword}",
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get(url, params=params)
    data = response.json()
    faqs = []
    for result in data.get("organic_results", []):
        link = result.get("link")
        title = result.get("title")
        if "reddit.com" in link:
            faqs.append(f"{title} — {link}")
    return faqs

def fetch_ai_overview(keyword):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get(url, params=params)
    data = response.json()
    overview = []
    if "answer_box" in data:
        overview.append(data["answer_box"].get("answer") or data["answer_box"].get("snippet"))
    if "organic_results" in data:
        for item in data["organic_results"]:
            snippet = item.get("snippet")
            if snippet and snippet not in overview:
                overview.append(snippet)
    return overview[:5]

def fetch_related_keywords(keyword):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get(url, params=params)
    data = response.json()
    long_tail = []
    lsi = []
    if "related_searches" in data:
        long_tail = [s.get("query") for s in data["related_searches"] if s.get("query")]
    if "people_also_search_for" in data:
        lsi = [s.get("query") for s in data["people_also_search_for"] if s.get("query")]
    return long_tail[:5], lsi[:5]
