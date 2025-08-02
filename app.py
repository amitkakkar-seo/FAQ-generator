import requests
import openai
from bs4 import BeautifulSoup
import streamlit as st

SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

def fetch_google_faqs(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    faqs = []
    if "related_questions" in data:
        for q in data["related_questions"]:
            faqs.append(q.get("question"))
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
        faqs = [q.strip("•- ").strip() for q in content.strip().split("\n") if q.strip()]
        return faqs
    except Exception as e:
        st.error(f"❌ ChatGPT FAQ error: {e}")
        return []

def fetch_ai_overview(keyword):
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States",
            "ai_overview": "true"
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        ai_text = data.get("answer_box", {}).get("answer") or \
                  data.get("ai_overview", {}).get("text") or \
                  "⚠️ No AI Overview found."
        return ai_text
    except Exception as e:
        return f"❌ AI Overview error: {e}"
