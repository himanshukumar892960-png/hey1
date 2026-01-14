import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

try:
    resp = requests.post(
        "https://api.tavily.com/search",
        json={"api_key": api_key, "query": "latest AI news", "search_depth": "basic"},
        timeout=10
    )
    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        print("Tavily API Key is working!")
        data = resp.json()
        if 'results' in data and data['results']:
            print(f"Sample Result: {data['results'][0]['title']}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Error: {e}")
