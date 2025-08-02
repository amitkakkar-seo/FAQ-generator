import streamlit as st
from faq_fetcher import (
    fetch_google_faqs,
    fetch_chatgpt_faqs,
    fetch_ai_overview_from_serpapi
)

st.set_page_config(page_title="FAQ Generator", page_icon="🧠", layout="centered")

st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.image("https://your-logo-url.com/logo.png", width=160)
st.title("🧠 AI-Powered FAQ Generator")
st.caption("Get FAQs, People Also Ask, and AI Overviews — all in one click!")

keyword = st.text_input("🔍 Enter a keyword or topic", placeholder="e.g., Best CRM tools for startups")

if keyword:
    with st.spinner("Fetching data..."):
        google_faqs = fetch_google_faqs(keyword)
        chatgpt_faqs = fetch_chatgpt_faqs(keyword)
        ai_overview = fetch_ai_overview_from_serpapi(keyword)

    st.subheader("📌 AI Overview (Simulated SGE)")
    st.info(ai_overview)

    st.subheader("📊 People Also Ask (Google)")
    for faq in google_faqs:
        st.markdown(f"- {faq}")

    st.subheader("🤖 ChatGPT-Generated FAQs")
    for faq in chatgpt_faqs:
        st.markdown(f"- {faq}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Powered by OpenAI + SerpApi")
