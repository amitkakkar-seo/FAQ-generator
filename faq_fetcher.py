import requests
import openai
import streamlit as st
from bs4 import BeautifulSoup
import praw

# === Load Secrets ===
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
REDDIT_CLIENT_ID = st.secrets["REDDIT_CLIENT_ID"]
REDDIT_SECRET = st.secrets["REDDIT_SECRET"]
REDDIT_USER_AGENT = st.secrets.get("REDDIT_USER_AGENT", "faq_tool")

openai.api_key = OPENAI_API_KEY

# === 1. Google FAQs ===
def fetch_google_faqs(keyword):
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States"
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        faqs = [q.get("question") for q in data.get("related_questions", []) if q.get("question")]
        return faqs
    except Exception as e:
        st.error(f"❌ Google FAQ Error: {e}")
        return []

# === 2. ChatGPT FAQs ===
def fetch_chatgpt_faqs(keyword):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Generate 10 FAQs about {keyword}."}],
            temperature=0.5,
            max_tokens=300
        )
        content = response.choices[0].message.content
        return [q.strip("-• ") for q in content.strip().split("\n") if q.strip()]
    except Exception as e:
        st.error(f"❌ ChatGPT Error: {e}")
        return []

# === 3. Reddit Threads ===
def fetch_reddit_faqs(keyword):
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        results = []
        for post in reddit.subreddit("all").search(keyword, limit=10):
            if post.title and "?" in post.title:
                results.append(post.title)
        return results
    except Exception as e:
        st.error(f"❌ Reddit Error: {e}")
        return []

# === 4. Quora Threads (via scraping) ===
def fetch_quora_faqs(keyword):
    try:
        url = f"https://www.quora.com/search?q={keyword.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        questions = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if "?" in text and 10 < len(text) < 120:
                questions.append(text)
        return list(set(questions))[:10]
    except Exception as e:
        st.error(f"❌ Quora Error: {e}")
        return []

# === 5. AI Overview (from SGE snippets) ===
def fetch_ai_overview(keyword):
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States",
            "api": "no"
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        overview = []

        if "answer_box" in data:
            box = data["answer_box"]
            if "answer" in box:
                overview.append(box["answer"])
            elif "snippet" in box:
                overview.append(box["snippet"])
            elif "snippet_highlighted_words" in box:
                overview.extend(box["snippet_highlighted_words"])

        return overview
    except Exception as e:
        st.error(f"❌ AI Overview Error: {e}")
        return []

# === 6. Related Keywords (Short-tail + Long-tail/LSI) ===
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

        short_tail_keywords = [item["query"] for item in data.get("related_searches", []) if item.get("query")]

        raw_texts = []
        for result in data.get("organic_results", []):
            raw_texts.extend([result.get("title", ""), result.get("snippet", "")])

        long_tail_keywords = list({
            phrase.strip()
            for phrase in raw_texts
            if len(phrase.strip().split()) >= 4
        })[:10]

        return {
            "short_tail_keywords": short_tail_keywords[:10],
            "long_tail_keywords": long_tail_keywords
        }

    except Exception as e:
        st.error(f"❌ Related Keywords Error: {str(e)}")
        return {}
