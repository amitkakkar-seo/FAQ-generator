import requests
#import praw
#from bs4 import BeautifulSoup
import openai

# === CONFIGURATION ===
SERPAPI_KEY = "fdff81292ea5463e1b28cc1a215cb1b945eff54ba61c018c3b8db5f37621b25b"
OPENAI_API_KEY = "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"

# === GOOGLE FAQ FETCH ===
def fetch_google_faqs(keyword):
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": SERPAPI_KEY
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    faqs = []
    if 'related_questions' in data:
        for q in data['related_questions']:
            faqs.append(q.get('question'))
    return faqs


# === CHATGPT FAQ GENERATION ===
import openai

# Replace "YOUR_OPENAI_API_KEY" with your actual OpenAI API key
openai.api_key = OPENAI_API_KEY

def fetch_chatgpt_faqs(keyword):
    prompt = f"Generate a list of 10 frequently asked questions about '{keyword}'."

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=300
    )
    # Extract the FAQs from the response
    faqs = response.choices[0].message.content.split('\n')
    # Remove any leading/trailing whitespace and bullet points
    faqs = [q.strip().lstrip('-• ') for q in faqs if q.strip()]
    return faqs  # Return the extracted FAQs


# === MAIN ===
if __name__ == "__main__":
    keyword = input("Enter keyword: ")

    print("\n--- Google FAQs ---")
    for q in fetch_google_faqs(keyword):
        print("•", q)

    print("\n--- ChatGPT-Generated FAQs ---")
    for q in fetch_chatgpt_faqs(keyword):
        print("•", q)