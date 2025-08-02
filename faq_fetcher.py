import requests
import openai
from bs4 import BeautifulSoup
import os

SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY


def fetch_google_faqs(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    faqs = []
    if "related_questions" in data:
        faqs = [q["question"] for q in data["related_questions"] if "question" in q]
    return faqs


def fetch_chatgpt_faqs(keyword):
    prompt = f"Generate a list of 10 frequently asked questions about '{keyword}'."
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300,
        )
        return [
            line.strip("-• ").strip()
            for line in response.choices[0].message.content.strip().split("\n")
            if line.strip()
        ]
    except Exception as e:
        return [f"❌ ChatGPT Error: {str(e)}"]


def fetch_ai_overview(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get("https://serpapi.com/search", params=params).json()
    results = []
    if "answer_box" in response:
        answer = response["answer_box"].get("answer") or response["answer_box"].get("snippet")
        if answer:
            results.append(answer)
    elif "organic_results" in response:
        for result in response["organic_results"][:2]:
            if "snippet" in result:
                results.append(result["snippet"])
    return results


def fetch_quora_faqs(keyword):
    try:
        search_url = f"https://www.quora.com/search?q={keyword.replace(' ', '%20')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return list(
            set(
                text.strip()
                for a in soup.find_all("a", href=True)
                if (text := a.get_text(strip=True)) and "?" in text and len(text) < 100
            )
        )[:10]
    except:
        return []


def fetch_reddit_faqs(keyword):
    try:
        search_url = f"https://www.reddit.com/search/?q={keyword.replace(' ', '%20')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        return list(
            set(
                text.strip()
                for a in soup.find_all("a", href=True)
                if (text := a.get_text(strip=True)) and "?" in text and len(text) < 120
            )
        )[:10]
    except:
        return []


def fetch_related_keywords(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY,
        "location": "United States"
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    people_also = [item["query"] for item in data.get("related_searches", [])]
    lsi_keywords = [item.get("title") for item in data.get("organic_results", []) if "title" in item]
    return {
        "people_also_search_for": people_also[:10],
        "lsi_keywords": lsi_keywords[:10],
    }
