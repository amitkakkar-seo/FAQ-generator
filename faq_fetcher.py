import streamlit as st
import openai
import requests

# === Load API Keys from Streamlit Secrets ===
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# === GOOGLE FAQ FETCH ===
def fetch_google_data(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "gl": "us",  # country
        "hl": "en",  # language
        "location": "United States"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()

    # FAQs
    faqs = []
    if 'related_questions' in data:
        for q in data['related_questions']:
            faqs.append(q.get('question'))

    # People Also Search For
    related_keywords = []
    if 'related_searches' in data:
        for r in data['related_searches']:
            related_keywords.append(r.get('query'))

    # Top URLs
    top_urls = []
    if 'organic_results' in data:
        for result in data['organic_results'][:5]:
            title = result.get('title')
            link = result.get('link')
            top_urls.append(f"{title} – {link}")

    return faqs, related_keywords, top_urls

# === CHATGPT FAQ FETCH ===
def fetch_chatgpt_faqs(keyword):
    try:
        prompt = f"Generate a list of 10 frequently asked questions about '{keyword}'."

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )

        content = response.choices[0].message.content
        faqs = [q.strip("•- ").strip() for q in content.strip().split("\n") if q.strip()]
        return faqs

    except Exception as e:
        st.error(f"❌ ChatGPT FAQ error: {str(e)}")
        return []
