import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_groq():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("Groq Key not found in .env")
        return

    print(f"Testing Groq Key: {key[:10]}...")
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": "Hello, are you working?"}]
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        if resp.status_code == 200:
            print("SUCCESS: Groq API is working!")
            content = resp.json()['choices'][0]['message']['content']
            print(f"Response: {content[:100]}...")
        else:
            print(f"FAILED: Status {resp.status_code}")
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_groq()
