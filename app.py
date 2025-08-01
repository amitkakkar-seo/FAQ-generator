import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

from link_suggester import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_reddit_questions,
    fetch_quora_questions
)

# === CONFIGURATION ===
SERPAPI_KEY = st.secrets["SERPAPI_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

st.set_page_config(page_title="AI FAQ Generator", layout="centered")

# --- Branding UI ---
st.markdown(
    """
    <div style='text-align: center; padding: 1rem;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/React-icon.svg/512px-React-icon.svg.png' width='60'/>
        <h2>FAQ Finder AI 🔍</h2>
        <p style='color:gray;'>Get real questions people ask on Google, ChatGPT, Reddit, and Quora.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Keyword Input ---
keyword = st.text_input("Enter a topic or keyword")

if keyword:
    with st.spinner("Fetching FAQs..."):
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
    """
    <hr>
    <div style='text-align: center; color: gray;'>
        Built with ❤️ by YourName • © 2025
    </div>
    """,
    unsafe_allow_html=True
)
