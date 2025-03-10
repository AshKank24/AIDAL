import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv
from googlesearch import search

load_dotenv()

genai.configure(api_key=os.environ["GEMINI"])

model = genai.GenerativeModel("gemini-1.5-flash")

def search_dsa_topic(topic):
    try:        
        # Perform the search with appropriate parameters
        query = f"{topic} data structures and algorithms"
        results = search(query, num_results=4, lang="en")
        
        # Convert generator to list
        return list(results)
    except Exception as e:
        print(f"Error during search: {e}")
        # Fallback to a predefined list of educational DSA resources
        return None

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