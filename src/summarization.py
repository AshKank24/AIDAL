import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

genai.configure(api_key=os.environ["GEMINI"])

model = genai.GenerativeModel("gemini-1.5-flash")

def search_dsa_topic(topic):
    my_api_key = os.environ["GOOGLE_API_KEY"]
    my_cse_id = os.environ["GOOGLE_CSE_ID"]
    
    service = build("customsearch", "v1", developerKey=my_api_key)
    results = service.cse().list(q=f"{topic} data structures and algorithms", cx=my_cse_id, num=4).execute()
    
    return [result['link'] for result in results['items']]

def scrape_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def summarize_content(content):
    prompt = f'''Your job is to understand the following content which is about a data structures and algorithms topic and
    explain it in a way that is easy to understand for a new programmer. Try to give examples and explain in a way that is 
    as technically sound as possible. Try to give high level details and key concepts along with examples.
    Content:\n\n{content}\n\nExplanation:'''
    response = model.generate_content(prompt)
    return response.text

def summarize_dsa_topic(topic):
    urls = search_dsa_topic(topic)
    summaries = []
    
    for url in urls:
        content = scrape_content(url)
        summary = summarize_content(content)
        summaries.append({"url": url, "summary": summary})
    
    return summaries

#Example usage:
topic = "binary search tree"
results = summarize_dsa_topic(topic)
for result in results:
    print(f"URL: {result['url']}")
    print(f"Summary: {result['summary']}\n")