import requests
from bs4 import BeautifulSoup
import openai
import streamlit as st

# API Keys from Streamlit secrets
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# === Google FAQs ===
def fetch_google_faqs(keyword):
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States"
        }
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()
        return [q.get("question") for q in data.get("related_questions", [])]
    except Exception as e:
        st.error(f"❌ Google FAQ Error: {str(e)}")
        return []

# === ChatGPT FAQs ===
def fetch_chatgpt_faqs(keyword):
    try:
        prompt = f"Generate 10 frequently asked questions about {keyword}."
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        faqs = response.choices[0].message.content.split("\n")
        return [q.strip("•- ").strip() for q in faqs if q.strip()]
    except Exception as e:
        st.error(f"❌ ChatGPT Error: {str(e)}")
        return []

# === AI Overview using SerpAPI (SGE) ===
def fetch_ai_overview(keyword):
    try:
        params = {
            "engine": "google_sge",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States"
        }
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()
        answers = data.get("answer_box", {}).get("answers", [])
        return [a.get("text") for a in answers if a.get("text")]
    except Exception as e:
        st.error(f"❌ AI Overview Error: {str(e)}")
        return []

# === Reddit Threads (from Google SERP) ===
def fetch_reddit_faqs(keyword):
    try:
        params = {
            "engine": "google",
            "q": f"site:reddit.com {keyword}",
            "api_key": SERPAPI_KEY,
            "location": "United States"
        }
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()
        return [r.get("title") for r in data.get("organic_results", []) if "reddit.com" in r.get("link", "")]
    except Exception as e:
        st.error(f"❌ Reddit Error: {str(e)}")
        return []

# === Quora Threads (from Google SERP) ===
def fetch_quora_faqs(keyword):
    try:
        params = {
            "engine": "google",
            "q": f"site:quora.com {keyword}",
            "api_key": SERPAPI_KEY,
            "location": "United States"
        }
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()
        return [q.get("title") for q in data.get("organic_results", []) if "quora.com" in q.get("link", "")]
    except Exception as e:
        st.error(f"❌ Quora Error: {str(e)}")
        return []

# === Related Keywords (People also search + LSI) ===
def fetch_related_keywords(keyword):
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States"
        }
        res = requests.get("https://serpapi.com/search", params=params)
        data = res.json()

        # People Also Search For
        related = []
        if 'related_searches' in data:
            related = [item.get('query') for item in data['related_searches'] if item.get('query')]

        # Long-tail & LSI Keywords from organic results (title and snippet)
        lsi_keywords = []
        if 'organic_results' in data:
            for result in data['organic_results']:
                if 'title' in result:
                    lsi_keywords.append(result['title'])
                if 'snippet' in result:
                    lsi_keywords.append(result['snippet'])

        # Clean and deduplicate
        lsi_keywords = list(set(kw.strip() for kw in lsi_keywords if len(kw.strip().split()) > 2))[:10]  # Keep only long phrases

        return {
            "people_also_search_for": related[:10],
            "lsi_keywords": lsi_keywords
        }

    except Exception as e:
        st.error(f"❌ Related Keywords Error: {str(e)}")
        return {}
