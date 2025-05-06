import streamlit as st
import pandas as pd
from faq_fetcher import fetch_google_data, fetch_chatgpt_faqs

# === SaaS-style Layout ===
st.set_page_config(page_title="FAQ Generator • Growthner", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .section {
            background-color: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .section h3 {
            margin-top: 0;
            margin-bottom: 0.8rem;
        }
        .download-button {
            margin-top: 1.2rem;
        }
    </style>
""", unsafe_allow_html=True)

# === Branding Header ===
st.markdown("<h1 style='text-align: center;'>🚀 Growthner FAQ Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: gray;'>Generate SEO FAQs, related searches, and SERP data in seconds.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# === Keyword Input ===
keyword = st.text_input("🔍 Enter a keyword", placeholder="e.g. Cloud GPUs for AI")

if st.button("Generate Insights", type="primary"):
    if not keyword.strip():
        st.warning("Please enter a keyword to continue.")
    else:
        with st.spinner("Collecting real-time data..."):
            google_faqs, related_keywords, top_urls = fetch_google_data(keyword)
            chatgpt_faqs = fetch_chatgpt_faqs(keyword)

        # === Google FAQs Section ===
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<h3>🌐 Google FAQs (People Also Ask)</h3>", unsafe_allow_html=True)
        if google_faqs:
            for q in google_faqs:
                st.markdown(f"• {q}")
        else:
            st.info("No FAQs found.")
        st.markdown("</div>", unsafe_allow_html=True)

        # === Related Keywords Section ===
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<h3>🔁 People Also Search For</h3>", unsafe_allow_html=True)
        if related_keywords:
            for kw in related_keywords:
                st.markdown(f"• {kw}")
        else:
            st.info("No related keywords found.")
        st.markdown("</div>", unsafe_allow_html=True)

        # === Top URLs Section ===
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<h3>🔗 Top Ranking Pages (US)</h3>", unsafe_allow_html=True)
        if top_urls:
            for url in top_urls:
                st.markdown(f"{url}")
        else:
            st.info("No URLs found.")
        st.markdown("</div>", unsafe_allow_html=True)

        # === ChatGPT FAQs Section ===
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<h3>🤖 ChatGPT-Generated FAQs</h3>", unsafe_allow_html=True)
        if chatgpt_faqs:
            for q in chatgpt_faqs:
                st.markdown(f"• {q}")
        else:
            st.info("No FAQs generated.")
        st.markdown("</div>", unsafe_allow_html=True)

        # === Download CSV Button ===
        all_faqs = google_faqs + chatgpt_faqs
        if all_faqs:
            df = pd.DataFrame(all_faqs, columns=["FAQ"])
            st.download_button("⬇️ Download FAQs as CSV", df.to_csv(index=False), "faqs.csv", "text/csv", key="download_faqs")
