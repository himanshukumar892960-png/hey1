import os
import requests
from dotenv import load_dotenv

load_dotenv()

APP_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not APP_TOKEN:
    print("Error: REPLICATE_API_TOKEN not found in .env")
    exit(1)

print(f"Testing Replicate API Token: {APP_TOKEN[:5]}...{APP_TOKEN[-5:]}")

# We'll check the 'account' endpoint or a model endpoint to verify access
url = "https://api.replicate.com/v1/models/minimax/video-01"
headers = {
    "Authorization": f"Token {APP_TOKEN}",
    "Content-Type": "application/json"
}

try:
    print(f"Connecting to {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCCESS: API Key is valid!")
        print(f"Model Name: {data.get('name')}")
        print(f"Owner: {data.get('owner')}")
        print("The token successfully authenticated and retrieved model details.")
    elif response.status_code == 401:
        print("❌ FAILED: Unauthorized. The API Key appears to be invalid.")
    else:
        print(f"⚠️ WARNING: Unexpected status code {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"❌ ERROR: Connection failed - {e}")
