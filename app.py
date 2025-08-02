import streamlit as st
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_reddit_quora_threads
)

st.set_page_config(page_title="FAQ Extractor & SERP Analyzer", page_icon="📚", layout="wide")

# === Header ===
st.markdown("<h1 style='text-align: center;'>📚 FAQ Extractor & SERP Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Generate FAQs and view Reddit & Quora threads ranking in Google.</p>", unsafe_allow_html=True)

# === Keyword Input ===
keyword = st.text_input("🔍 Enter a keyword", placeholder="e.g., AI for Education")

if keyword:
    st.info("🔄 Fetching data, please wait...")

    # Google FAQs
    google_faqs = fetch_google_faqs(keyword)
    if google_faqs:
        st.subheader("🔎 People Also Ask (Google FAQs)")
        for faq in google_faqs:
            st.markdown(f"- {faq}")
    else:
        st.warning("No Google FAQs found.")

    # ChatGPT FAQs
    chatgpt_faqs = fetch_chatgpt_faqs(keyword)
    if chatgpt_faqs:
        st.subheader("🤖 ChatGPT-Generated FAQs")
        for faq in chatgpt_faqs:
            st.markdown(f"- {faq}")
    else:
        st.warning("No ChatGPT FAQs generated.")

    # Reddit & Quora from Google
    reddit_links, quora_links = fetch_reddit_quora_threads(keyword)

    if reddit_links:
        st.subheader("📌 Reddit Threads Ranking on Google")
        for item in reddit_links:
            st.markdown(f"- [{item['title']}]({item['link']})")
    else:
        st.info("No Reddit results found.")

    if quora_links:
        st.subheader("📌 Quora Threads Ranking on Google")
        for item in quora_links:
            st.markdown(f"- [{item['title']}]({item['link']})")
    else:
        st.info("No Quora results found.")

# === Footer ===
st.markdown("---")
st.markdown(
    "<footer style='text-align: center; font-size: 14px;'>"
    "Built with ❤️ by <a href='https://yourdomain.com' target='_blank'>YourName</a> | Powered by SerpAPI & OpenAI"
    "</footer>",
    unsafe_allow_html=True
)
