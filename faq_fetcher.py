import requests
import openai
import streamlit as st

# === API Keys from Streamlit secrets ===
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# === GOOGLE FAQ FETCH ===
def fetch_google_faqs(keyword):
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States",
            "num": "20"
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        faqs = []

        if "related_questions" in data:
            for q in data["related_questions"]:
                question = q.get("question")
                if question:
                    faqs.append(question)
        return faqs

    except Exception as e:
        st.error(f"❌ Google FAQ Error: {str(e)}")
        return []

# === CHATGPT FAQ GENERATION ===
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
        st.error(f"❌ ChatGPT Error: {str(e)}")
        return []

# === FETCH REDDIT & QUORA THREADS ===
def fetch_reddit_quora_threads(keyword):
    try:
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_KEY,
            "location": "United States",
            "num": "20"
        }
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        reddit_links = []
        quora_links = []

        for result in data.get("organic_results", []):
            link = result.get("link", "")
            title = result.get("title", "")
            if "reddit.com" in link:
                reddit_links.append({"title": title, "link": link})
            elif "quora.com" in link:
                quora_links.append({"title": title, "link": link})

        return reddit_links, quora_links

    except Exception as e:
        st.error(f"❌ Reddit/Quora Error: {str(e)}")
        return [], []
