import requests
from bs4 import BeautifulSoup
import openai

# === Google FAQ Fetch via SerpAPI ===
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
            faqs.append(item.get("question"))
    return faqs

# === ChatGPT FAQs ===
def fetch_chatgpt_faqs(keyword):
    prompt = f"Generate a list of 10 frequently asked questions about '{keyword}'."
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        content = response.choices[0].message.content
        faqs = [line.strip("-• ").strip() for line in content.split("\n") if line.strip()]
        return faqs
    except Exception as e:
        return [f"❌ Error generating ChatGPT FAQs: {e}"]

# === Reddit Questions (Scraped) ===
def fetch_reddit_questions(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.reddit.com/search/?q={keyword.replace(' ', '+')}"
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        questions = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if "?" in text and len(text) < 120:
                questions.append(text)
        return list(set(questions))[:10]
    except Exception as e:
        return [f"❌ Reddit error: {e}"]

# === Quora Questions (Scraped) ===
def fetch_quora_questions(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.quora.com/search?q={keyword.replace(' ', '+')}"
    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        questions = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if "?" in text and len(text) < 120:
                questions.append(text)
        return list(set(questions))[:10]
    except Exception as e:
        return [f"❌ Quora error: {e}"]
