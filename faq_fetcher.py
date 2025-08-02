import requests
import openai
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
    for q in data.get("related_questions", []):
        if q.get("question"):
            faqs.append(q["question"])
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
        st.error(f"❌ ChatGPT Error: {e}")
        return []

def fetch_ai_overview(keyword):
    try:
        prompt = f"Simulate what Google AI Overview might respond for the query: '{keyword}'"
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"❌ AI Overview Error: {e}")
        return ""
