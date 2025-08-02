import streamlit as st
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_quora_faqs,
    fetch_reddit_faqs,
    fetch_ai_overview,
    fetch_related_keywords
)

# ==== PAGE SETUP ====
st.set_page_config(
    page_title="FAQ & Keyword Explorer",
    page_icon="📊",
    layout="wide"
)

# ==== DARK MODE THEME + STYLING ====
st.markdown("""
    <style>
        body, .stApp {
            background-color: #121212;
            color: white;
        }
        .block-container {
            padding: 2rem;
        }
        h1, h2, h3, h4, h5 {
            color: white;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #1f1f1f;
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 13px;
        }
        .logo {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #fbbf24;
        }
    </style>
""", unsafe_allow_html=True)

# ==== HEADER ====
st.markdown('<div class="logo">🔍 FAQ & Keyword Explorer</div>', unsafe_allow_html=True)

# ==== MAIN ====
keyword = st.text_input("Enter a keyword to analyze:", "AI image generation")

if keyword:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Google FAQs")
        for q in fetch_google_faqs(keyword):
            st.markdown(f"- {q}")

        st.subheader("🧠 ChatGPT FAQs")
        for q in fetch_chatgpt_faqs(keyword):
            st.markdown(f"- {q}")

        st.subheader("📚 AI Overview (SGE)")
        for item in fetch_ai_overview(keyword):
            st.markdown(f"- {item}")

    with col2:
        st.subheader("💬 Reddit & Quora Threads")
        reddit = fetch_reddit_faqs(keyword)
        quora = fetch_quora_faqs(keyword)

        if reddit:
            st.markdown("**Reddit:**")
            for r in reddit:
                st.markdown(f"- {r}")

        if quora:
            st.markdown("**Quora:**")
            for q in quora:
                st.markdown(f"- {q}")

        st.subheader("🔑 Keyword Suggestions")
        keyword_data = fetch_related_keywords(keyword)

        if keyword_data:
            st.markdown("**Short-tail Keywords:**")
            for kw in keyword_data["short_tail_keywords"]:
                st.markdown(f"- {kw}")
            st.markdown("**Long-tail / LSI Keywords:**")
            for kw in keyword_data["long_tail_keywords"]:
                st.markdown(f"- {kw}")

# ==== FOOTER ====
st.markdown("""
    <div class="footer">
        🚀 Built with ❤️ by YourName | Streamlit SaaS App
    </div>
""", unsafe_allow_html=True)
