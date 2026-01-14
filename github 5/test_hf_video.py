from dotenv import load_dotenv
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from huggingface_client import HuggingFaceClient

# Load env vars
load_dotenv()

api_key = os.getenv("HUGGINGFACE_API_KEY")
print(f"HF Key: {api_key[:5]}...")

client = HuggingFaceClient(api_key)

print("Attempting to generate video with HuggingFace...")
url = client.generate_video("A spinning coin")

if url:
    print(f"SUCCESS: Video saved at {url}")
else:
    print("FAILURE: No video generated")
