from dotenv import load_dotenv
import os
import sys

# Add current directory to path so we can import veo_client
sys.path.append(os.getcwd())

from veo_client import VeoClient

# Load env vars
load_dotenv()

keys = [
    ("Tier 1", os.getenv("VEO_API_KEY")),
    ("Tier 2", os.getenv("VEO_API_KEY_2")),
    ("Tier 3", os.getenv("VEO_API_KEY_3")),
    ("Tier 4", os.getenv("VEO_API_KEY_4")),
]

for name, key in keys:
    if not key:
        print(f"Skipping {name}: No key")
        continue

    print(f"\nTesting {name}...")
    client = VeoClient(key, model="veo3")
    
    # Simple prompt
    url = client.generate_video("spinning gold coin")
    
    if url:
        print(f"SUCCESS with {name}: {url}")
        break
    else:
        print(f"FAILURE with {name}")
