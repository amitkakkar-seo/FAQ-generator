import streamlit as st
import pandas as pd
from faq_fetcher import fetch_google_data, fetch_chatgpt_faqs

# === Page Configuration ===
st.set_page_config(
    page_title="AI FAQ Generator",
    layout="centered"
)

# === Header ===
st.markdown("""
    <h1 style='text-align: center;'>🤖 AI-Powered FAQ Generator</h1>
    <p style='text-align: center; font-size: 18px;'>Generate real user questions, related searches, and top URLs from Google and ChatGPT.</p>
    <hr>
""", unsafe_allow_html=True)

# === Input Section ===
keyword = st.text_input("🔍 Enter a keyword", placeholder="e.g. AI in education")

if st.button("🚀 Generate FAQs"):
    if not keyword.strip():
        st.warning("Please enter a keyword to continue.")
    else:
        with st.spinner("Fetching data..."):

            # Google: Get FAQs, related keywords, and top URLs
            google_faqs, related_keywords, top_urls = fetch_google_data(keyword)

            # ChatGPT FAQs
            chatgpt_faqs = fetch_chatgpt_faqs(keyword)

        # === Google FAQs ===
        if google_faqs:
            st.subheader("🌐 Google FAQs (People Also Ask)")
            for q in google_faqs:
                st.markdown(f"- {q}")
        else:
            st.info("No Google FAQs found.")

        # === People Also Search For ===
        if related_keywords:
            st.subheader("🔁 People Also Search For")
            for kw in related_keywords:
                st.markdown(f"- {kw}")
        else:
            st.info("No related keywords found.")

        # === Top Ranking URLs ===
        if top_urls:
            st.subheader("🔗 Top Ranking Pages (US)")
            for url in top_urls:
                st.markdown(f"- {url}")
        else:
            st.info("No URLs found in search results.")

        # === ChatGPT FAQs ===
        if chatgpt_faqs:
            st.subheader("🤖 ChatGPT-
