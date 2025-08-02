import streamlit as st
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_reddit_quora_threads
)

st.set_page_config(page_title="FAQ Intelligence Tool", page_icon="🧠", layout="wide")

# === Custom CSS for Dark Theme with White Text ===
st.markdown("""
<style>
body, html, .block-container {
    background-color: #121212 !important;
    color: white !important;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3, h4, h5, h6, p, li, div, span, label {
    color: white !important;
}
.section-box {
    background-color: #1f1f1f;
    padding: 1.2rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    color: white;
    box-shadow: 0 0 4px rgba(255, 255, 255, 0.05);
}
a {
    color: #8ab4f8;
}
a:hover {
    text-decoration: underline;
}
.stTextInput > div > div > input {
    background-color: #1e1e1e;
    color: white;
    border: 1px solid #555;
}
footer {
    text-align: center;
    color: #bbb;
    font-size: 0.85rem;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://yourdomain.com/logo.png", width=160)
    st.markdown("### 🔍 How to Use")
    st.markdown("1. Enter a keyword\n2. Get FAQs from Google, ChatGPT, Reddit, and Quora\n3. Apply them in SEO, content, or product research.")
    st.markdown("---")
    st.markdown("Built by [YourBrand](https://yourbrand.com)")

# Header
st.markdown("<h1 style='text-align:center;'>🧠 FAQ Intelligence Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Uncover user questions and search threads from top platforms</p>", unsafe_allow_html=True)

# Keyword input
keyword = st.text_input("Enter a keyword:", placeholder="e.g. best AI copywriting tools")

if keyword:
    with st.spinner("🔍 Fetching results..."):
        google_faqs = fetch_google_faqs(keyword)
        chatgpt_faqs = fetch_chatgpt_faqs(keyword)
        reddit_links, quora_links = fetch_reddit_quora_threads(keyword)

    tab1, tab2, tab3 = st.tabs(["📌 Google FAQs", "🤖 ChatGPT FAQs", "💬 Reddit + Quora"])

    with tab1:
        st.markdown("### People Also Ask (Google)")
        if google_faqs:
            for q in google_faqs:
                st.markdown(f"<div class='section-box'>❓ {q}</div>", unsafe_allow_html=True)
        else:
            st.info("No Google FAQs found.")

    with tab2:
        st.markdown("### AI-Generated FAQs (ChatGPT)")
        if chatgpt_faqs:
            for q in chatgpt_faqs:
                st.markdown(f"<div class='section-box'>🤖 {q}</div>", unsafe_allow_html=True)
        else:
            st.warning("No ChatGPT FAQs found.")

    with tab3:
        st.markdown("### Reddit Threads Ranking on Google")
        if reddit_links:
            for item in reddit_links:
                st.markdown(f"<div class='section-box'>🔗 <a href='{item['link']}' target='_blank'>{item['title']}</a></div>", unsafe_allow_html=True)
        else:
            st.info("No Reddit threads found.")

        st.markdown("### Quora Threads Ranking on Google")
        if quora_links:
            for item in quora_links:
                st.markdown(f"<div class='section-box'>🔗 <a href='{item['link']}' target='_blank'>{item['title']}</a></div>", unsafe_allow_html=True)
        else:
            st.info("No Quora threads found.")

# Footer
st.markdown("""
---
<footer>
Made with ❤️ by <a href="https://yourbrand.com" target="_blank">YourBrand</a> | Powered by SerpAPI + OpenAI
</footer>
""", unsafe_allow_html=True)
