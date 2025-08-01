import requests
from bs4 import BeautifulSoup
import openai

# Google FAQs
def fetch_google_faqs(keyword, SERPAPI_KEY):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "gl": "us"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    faqs = []
    if "related_questions" in data:
        for item in data["related_questions"]:
            if item.get("question"):
                faqs.append(item["question"])
    return faqs or ["⚠️ No FAQs found from Google."]

# ChatGPT FAQs
def fetch_chatgpt_faqs(keyword):
    try:
        prompt = f"Generate a list of 10 frequently asked questions about '{keyword}'."
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        content = response.choices[0].message.content
        return [q.strip("-• ").strip() for q in content.split("\n") if q.strip()]
    except Exception as e:
        return [f"❌ ChatGPT Error: {e}"]

# Reddit Questions
def fetch_reddit_questions(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.reddit.com/search/?q={keyword.replace(' ', '+')}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        questions = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if "?" in text and len(text) < 120:
                questions.append(text)
        return list(set(questions))[:10] or ["⚠️ No Reddit questions found."]
    except Exception as e:
        return [f"❌ Reddit error: {e}"]

# Quora Questions
def fetch_quora_questions(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.quora.com/search?q={keyword.replace(' ', '+')}"
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        questions = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if "?" in text and len(text) < 120:
                questions.append(text)
        return list(set(questions))[:10] or ["⚠️ No Quora questions found."]
    except Exception as e:
        return [f"❌ Quora error: {e}"]
