import streamlit as st
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_reddit_quora_threads
)

# --- Streamlit Config ---
st.set_page_config(
    page_title="FAQ Intelligence",
    page_icon="🧠",
    layout="wide"
)

# --- Custom CSS for Dark SaaS UI ---
st.markdown("""
    <style>
    body, .stApp {
        background-color: #0f1117;
        color: #f1f1f1;
        font-family: 'Segoe UI', sans-serif;
    }

    h1, h2, h3, h4, h5 {
        color: #fdfdfd;
        font-weight: 700;
    }

    .stTextInput > div > div > input {
        background-color: #1e1f26;
        color: #f1f1f1;
        border: 1px solid #3a3b3f;
        padding: 0.6em;
    }

    .stTextInput input:focus {
        border-color: #9b5de5;
        box-shadow: 0 0 0 0.1rem #9b5de5;
    }

    .stMarkdown {
        padding: 1em;
        border-radius: 8px;
        background: #1e1f26;
        margin-bottom: 1em;
    }

    footer {
        color: #777;
        font-size: 0.9em;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align:center;'>🧠 FAQ Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ccc;'>Extract FAQs + Reddit/Quora threads directly from SERPs for smarter content strategy</p>", unsafe_allow_html=True)

# --- Input ---
keyword = st.text_input("🔍 Enter a keyword to analyze:", placeholder="e.g., Cloud GPUs for LLMs")

if keyword:
    with st.spinner("🔄 Fetching SERP data..."):
        google_faqs = fetch_google_faqs(keyword)
        chatgpt_faqs = fetch_chatgpt_faqs(keyword)
        reddit_links, quora_links = fetch_reddit_quora_threads(keyword)

    st.markdown("### 📌 Google: People Also Ask")
    if google_faqs:
        for faq in google_faqs:
            st.markdown(f"🔹 {faq}")
    else:
        st.warning("No Google FAQs found.")

    st.markdown("### 🤖 ChatGPT-Generated FAQs")
    if chatgpt_faqs:
        for faq in chatgpt_faqs:
            st.markdown(f"🔹 {faq}")
    else:
        st.warning("No ChatGPT FAQs generated.")

    st.markdown("### 🔗 Reddit Threads Ranking in Google")
    if reddit_links:
        for item in reddit_links:
            st.markdown(f"- [{item['title']}]({item['link']})")
    else:
        st.info("No Reddit results found.")

    st.markdown("### 🔗 Quora Threads Ranking in Google")
    if quora_links:
        for item in quora_links:
            st.markdown(f"- [{item['title']}]({item['link']})")
    else:
        st.info("No Quora results found.")

# --- Footer ---
st.markdown("""
    <hr style="margin-top:3rem;margin-bottom:1rem;">
    <footer style='text-align: center;'>
        🚀 Built by <a href="https://yourdomain.com" target="_blank" style="color:#9b5de5;">YourBrand</a> | Powered by <strong>SerpAPI</strong> & <strong>OpenAI</strong>
    </footer>
""", unsafe_allow_html=True)
