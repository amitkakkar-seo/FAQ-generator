import streamlit as st
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_reddit_quora_threads
)

# Page configuration
st.set_page_config(page_title="FAQ Intelligence", page_icon="🧠", layout="wide")

# Inject custom CSS for SaaS look
st.markdown("""
<style>
body {
    background-color: #0f1117;
    color: #f1f1f1;
    font-family: 'Segoe UI', sans-serif;
}
.sidebar .sidebar-content {
    background-color: #1e1f26;
}
h1, h2, h3 {
    font-weight: 600;
    color: #ffffff;
}
.section-box {
    background-color: #1e1f26;
    padding: 1.2rem;
    border-radius: 10px;
    margin-bottom: 1.2rem;
    box-shadow: 0 0 8px rgba(0,0,0,0.4);
}
a {
    color: #9b5de5;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
.stTextInput>div>div>input {
    background-color: #272931;
    color: #fff;
    border: 1px solid #333;
    padding: 0.5em;
}
footer {
    color: #aaa;
    font-size: 0.85em;
    text-align: center;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://yourdomain.com/logo.png", width=180)
    st.markdown("### 🔍 How to Use")
    st.markdown("1. Enter a keyword\n2. View FAQs from Google, ChatGPT, Reddit & Quora\n3. Use insights for your SEO/content planning")
    st.markdown("---")
    st.markdown("✅ Powered by SerpAPI + OpenAI")

# Title
st.markdown("<h1 style='text-align:center;'>🧠 FAQ Intelligence SaaS Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Uncover high-intent questions from Google, AI, Reddit, and Quora</p>", unsafe_allow_html=True)

# Keyword input
keyword = st.text_input("Enter your target keyword:", placeholder="e.g. best cloud GPU provider for AI")

if keyword:
    with st.spinner("Fetching FAQs..."):
        google_faqs = fetch_google_faqs(keyword)
        chatgpt_faqs = fetch_chatgpt_faqs(keyword)
        reddit_links, quora_links = fetch_reddit_quora_threads(keyword)

    # Tabs UI
    tab1, tab2, tab3 = st.tabs(["📌 Google FAQs", "🤖 ChatGPT FAQs", "📢 Reddit + Quora Threads"])

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
            st.info("No Reddit results found.")

        st.markdown("### Quora Threads Ranking on Google")
        if quora_links:
            for item in quora_links:
                st.markdown(f"<div class='section-box'>🔗 <a href='{item['link']}' target='_blank'>{item['title']}</a></div>", unsafe_allow_html=True)
        else:
            st.info("No Quora results found.")

# Footer
st.markdown("""
---
<footer>
Built with ❤️ by <a href="https://yourbrand.com" target="_blank">YourBrand</a> • Powered by SerpAPI & OpenAI
</footer>
""", unsafe_allow_html=True)
