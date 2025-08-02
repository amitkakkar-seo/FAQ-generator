import streamlit as st
from faq_fetcher import fetch_google_faqs, fetch_chatgpt_faqs, fetch_ai_overview

# === PAGE CONFIG ===
st.set_page_config(page_title="AI FAQ Generator", page_icon="💡", layout="wide")

# === CUSTOM STYLING ===
st.markdown("""
    <style>
    .top-banner {
        background-color: #0F1C2E;
        color: white;
        padding: 1rem 2rem;
        font-size: 20px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .result-card {
        background: #F9FAFB;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e1e1e1;
    }
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: #888;
        padding: 2rem 0 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="top-banner">
        <div>💡 <span style="color:#00c7ff;">AI FAQ Generator</span></div>
        <div><a href="https://yourdomain.com" style="color:white;text-decoration:none;">Docs</a></div>
    </div>
""", unsafe_allow_html=True)

# === MAIN SEARCH ===
st.markdown("### 🔍 Enter your keyword below")
keyword = st.text_input("", placeholder="e.g. Best AI tools for SEO", label_visibility="collapsed")

if keyword:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📋 People Also Ask (Google)")
        google_faqs = fetch_google_faqs(keyword)
        if google_faqs:
            for faq in google_faqs:
                st.markdown(f'<div class="result-card">• {faq}</div>', unsafe_allow_html=True)
        else:
            st.warning("No results from Google.")

        st.markdown("#### 🤖 ChatGPT FAQs")
        chatgpt_faqs = fetch_chatgpt_faqs(keyword)
        if chatgpt_faqs:
            for faq in chatgpt_faqs:
                st.markdown(f'<div class="result-card">• {faq}</div>', unsafe_allow_html=True)
        else:
            st.warning("ChatGPT could not generate FAQs.")

    with col2:
        st.markdown("#### 🧠 Google AI Overview")
        ai_answer = fetch_ai_overview(keyword)
        if ai_answer:
            st.markdown(f'<div class="result-card">{ai_answer}</div>', unsafe_allow_html=True)
        else:
            st.info("No AI Overview available.")

# === FOOTER ===
st.markdown("""
    <div class="footer">
        Built with ❤️ using Streamlit | © 2025 YourBrand
    </div>
""", unsafe_allow_html=True)
