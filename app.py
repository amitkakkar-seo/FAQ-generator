import streamlit as st
import pandas as pd
from link_suggester import (
    fetch_urls_from_sitemap,
    fetch_page_snippet,
    generate_internal_link_suggestions,
    fetch_reddit_questions,
    fetch_quora_questions
)

st.set_page_config(page_title="Internal Linking Assistant • Growthner", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .footer { text-align: center; font-size: 14px; color: gray; margin-top: 3rem; }
        .section { padding: 1.5rem; background: #ffffff; border: 1px solid #e6e6e6; border-radius: 12px; margin-bottom: 2rem; }
        .main-header { text-align: center; margin-bottom: 2rem; }
        .main-header h1 { font-size: 2.8rem; margin-bottom: 0.5rem; }
        .main-header p { font-size: 1.2rem; color: #666; }
        .logo { height: 60px; margin-bottom: 10px; }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main-header">
        <img src="https://growthner.com/logo.png" class="logo">
        <h1>🔗 Internal Linking Assistant</h1>
        <p>Suggesting smart internal links from your sitemap content and related Reddit/Quora questions.</p>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("### 🔍 Step 1: Enter your sitemap URL and keyword")
    sitemap_url = st.text_input("Sitemap URL", placeholder="https://example.com/sitemap.xml")
    keyword = st.text_input("Keyword (for Reddit & Quora)", placeholder="content marketing tips")

    st.markdown("### 🛠️ Step 2: Choose number of pages to analyze")
    limit = st.slider("Pages to scan", min_value=5, max_value=50, value=10, step=5)

    if st.button("🚀 Generate Insights"):
        if not sitemap_url or not keyword:
            st.warning("⚠️ Please enter both sitemap URL and keyword.")
        else:
            with st.spinner("Analyzing sitemap and scraping questions..."):
                try:
                    urls = fetch_urls_from_sitemap(sitemap_url)
                    pages_data = []
                    for url in urls[:limit]:
                        content = fetch_page_snippet(url)
                        if content.strip() and len(content.split()) > 5:
                            pages_data.append({"url": url, "content": content})

                    df = generate_internal_link_suggestions(pages_data)

                    reddit_qs = fetch_reddit_questions(keyword)
                    quora_qs = fetch_quora_questions(keyword)

                    st.success("✅ All data generated!")

                    st.markdown("### 📄 Internal Link Suggestions")
                    st.dataframe(df, use_container_width=True)
                    st.download_button("⬇️ Download CSV", df.to_csv(index=False), "internal_link_suggestions.csv", "text/csv")

                    st.markdown("### 🧠 Reddit Questions")
                    for q in reddit_qs:
                        st.write("•", q)

                    st.markdown("### ❓ Quora Questions")
                    for q in quora_qs:
                        st.write("•", q)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

st.markdown("""
    <div class='footer'>
        Made with ❤️ by <a href='https://www.linkedin.com/in/amitkakkarseo/' target='_blank'>Amit Kakkar</a> | © 2025 Growthner
    </div>
""", unsafe_allow_html=True)
