import streamlit as st
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_quora_faqs,
    fetch_reddit_faqs,
    fetch_ai_overview,
    fetch_related_keywords
)

st.set_page_config(page_title="FAQ & Keyword Explorer", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #0d1117;
        color: white;
    }
    .stApp {
        background-color: #0d1117;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: white;
        border: 1px solid #30363d;
    }
    .stButton > button {
        background-color: #238636;
        color: white;
        border-radius: 5px;
    }
    .stMarkdown {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("# 🔎 FAQ & Keyword Explorer")
st.caption("Built for SEO & content strategy teams")

keyword = st.text_input("Enter your keyword")

if keyword:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Google FAQs")
        for q in fetch_google_faqs(keyword):
            st.markdown(f"• {q}")

        st.subheader("💬 Quora Threads")
        for q in fetch_quora_faqs(keyword):
            st.markdown(f"• [{q}]({q})")

        st.subheader("👥 Reddit Threads")
        for q in fetch_reddit_faqs(keyword):
            st.markdown(f"• {q}")

    with col2:
        st.subheader("🤖 ChatGPT FAQs")
        for q in fetch_chatgpt_faqs(keyword):
            st.markdown(f"• {q}")

        st.subheader("🧠 AI Overview")
        for q in fetch_ai_overview(keyword):
            st.markdown(f"• {q}")

        st.subheader("🔑 Keyword Suggestions")
        long_tail, lsi = fetch_related_keywords(keyword)
        st.markdown("**Long-tail Keywords**")
        for q in long_tail:
            st.markdown(f"• {q}")
        st.markdown("**LSI Keywords**")
        for q in lsi:
            st.markdown(f"• {q}")
