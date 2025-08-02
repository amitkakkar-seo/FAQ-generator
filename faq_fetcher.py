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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==== CUSTOM CSS FOR DARK MODE + STYLING ====
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
            color: white;
        }
        .css-1d391kg, .css-ffhzg2 {
            color: white !important;
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

# ==== MAIN UI ====
keyword = st.text_input("Enter a keyword to analyze:", "AI image generation")

if keyword:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Google FAQs")
        google_faqs = fetch_google_faqs(keyword)
        for q in google_faqs:
            st.markdown(f"- {q}")

        st.subheader("🧠 ChatGPT FAQs")
        chatgpt_faqs = fetch_chatgpt_faqs(keyword)
        for q in chatgpt_faqs:
            st.markdown(f"- {q}")

        st.subheader("📚 AI Overview (SGE)")
        ai_overview = fetch_ai_overview(keyword)
        for item in ai_overview:
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

        st.subheader("🔑 Related & LSI Keywords")
        keyword_data = fetch_related_keywords(keyword)
        if keyword_data:
            st.markdown("**People also search for:**")
            for item in keyword_data['people_also_search_for']:
                st.markdown(f"- {item}")

            st.markdown("**Long-tail & LSI Keywords:**")
            for item in keyword_data['lsi_keywords']:
                st.markdown(f"- {item}")

# ==== FOOTER ====
st.markdown("""
    <div class="footer">
        🚀 Built with ❤️ by YourName | Streamlit SaaS App
    </div>
""", unsafe_allow_html=True)
