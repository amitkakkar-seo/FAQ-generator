import streamlit as st
import openai
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_reddit_questions,
    fetch_quora_questions
)

# Load API Keys from Streamlit Secrets
SERPAPI_KEY = st.secrets["fdff81292ea5463e1b28cc1a215cb1b945eff54ba61c018c3b8db5f37621b25b"]
OPENAI_API_KEY = st.secrets["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"]
openai.api_key = OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="FAQ Finder AI", layout="centered")

# --- UI Header ---
st.markdown(
    '''
    <div style='text-align: center; padding: 1rem;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/512px-React-icon.svg.png' width='60'/>
        <h2 style='margin-bottom:0;'>FAQ Finder AI 🔍</h2>
        <p style='color:gray;'>Find real questions people ask on Google, ChatGPT, Reddit, and Quora.</p>
    </div>
    ''',
    unsafe_allow_html=True
)

# --- Input ---
keyword = st.text_input("Enter a topic or keyword")

if keyword:
    with st.spinner("Fetching questions..."):
        google_faqs = fetch_google_faqs(keyword, SERPAPI_KEY)
        chatgpt_faqs = fetch_chatgpt_faqs(keyword)
        reddit_faqs = fetch_reddit_questions(keyword)
        quora_faqs = fetch_quora_questions(keyword)

    st.markdown("### 🟢 Google FAQs")
    for q in google_faqs:
        st.markdown(f"- {q}")

    st.markdown("### 🤖 ChatGPT FAQs")
    for q in chatgpt_faqs:
        st.markdown(f"- {q}")

    st.markdown("### 🔴 Reddit Questions")
    for q in reddit_faqs:
        st.markdown(f"- {q}")

    st.markdown("### 🔵 Quora Questions")
    for q in quora_faqs:
        st.markdown(f"- {q}")

# --- Footer ---
st.markdown(
    '''
    <hr>
    <div style='text-align: center; color: gray; font-size: 14px;'>
        Built with ❤️ by YourName • © 2025
    </div>
    ''',
    unsafe_allow_html=True
)
