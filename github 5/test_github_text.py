import requests
import os
from dotenv import load_dotenv

load_dotenv()

def test_github_text():
    key = os.getenv("GITHUB_ACCESS_TOKEN")
    if not key:
        print("GITHUB_ACCESS_TOKEN not found in .env")
        return

    print(f"Testing GitHub Access Token: {key[:15]}...")
    
    url = "https://models.inference.ai.azure.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you hear me?"}
        ]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            print("SUCCESS: GitHub Models (Text) is working!")
            content = resp.json()['choices'][0]['message']['content']
            print(f"Response: {content[:100]}...")
        else:
            print(f"FAILED: Status {resp.status_code}")
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_github_text()
