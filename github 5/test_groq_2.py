import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_groq_2():
    key = os.getenv("GROQ_API_KEY_2")
    if not key:
        print("Groq Key 2 not found in .env")
        return

    print(f"Testing Groq Key 2: {key[:10]}...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": "Are you active as Tier 10?"}]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            print("SUCCESS: Groq API (Tier 10) is working!")
            content = resp.json()['choices'][0]['message']['content']
            print(f"Response: {content[:100]}...")
        else:
            print(f"FAILED: Status {resp.status_code}")
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_groq_2()
