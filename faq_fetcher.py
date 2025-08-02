import requests
import openai
import streamlit as st

# Load secrets
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

# === 1. Fetch People Also Ask FAQs ===
def fetch_google_faqs(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "us"
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        faqs = []
        if 'related_questions' in data:
            for q in data['related_questions']:
                faqs.append(q.get('question'))
        return faqs
    except Exception as e:
        return [f"❌ Google FAQ Error: {str(e)}"]

# === 2. Fetch ChatGPT FAQs ===
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
        faqs = [q.strip("•- ").strip() for q in content.strip().split("\n") if q.strip()]
        return faqs
    except Exception as e:
        return [f"❌ ChatGPT Error: {str(e)}"]

# === 3. Fetch AI Overview via SerpApi ===
def fetch_ai_overview_from_serpapi(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "us"
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        if "ai_overview" in data:
            return data["ai_overview"].get("text", "No AI Overview text available.")
        else:
            return "AI Overview not available for this keyword."
    except Exception as e:
        return f"❌ AI Overview Error: {str(e)}"
