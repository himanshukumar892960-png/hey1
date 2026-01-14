import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENROUTER_API_KEY_2")
model = os.getenv("OPENROUTER_MODEL_2")

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

payload = {
    "model": model,
    "messages": [
        {"role": "user", "content": "Hi"}
    ]
}

print(f"Testing {model} with minimal payload...")
response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")
