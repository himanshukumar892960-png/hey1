import os
import time
from dotenv import load_dotenv
from replicate_client import ReplicateClient

# Load environment variables
import logging
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_generation():
    # Get API Token
    api_token = os.getenv("REPLICATE_API_TOKEN")
    if not api_token:
        print("Error: REPLICATE_API_TOKEN not found.")
        return

    # Initialize Client
    client = ReplicateClient(api_token)
    
    # improved prompt for Minimax/Video-01
    prompt = "A cinematic, highly detailed video of a futuristic cyberpunk city with neon lights reflecting in rain puddles, flying cars zooming by, shallow depth of field, 4k resolution, smooth motion."
    
    print(f"🎬 Starting Video Generation with Prompt:\n'{prompt}'")
    print("-" * 50)
    
    try:
        start_time = time.time()
        video_url = client.generate_video(prompt)
        duration = time.time() - start_time
        
        if video_url:
            print(f"\n✅ Video Generated Successfully in {duration:.1f} seconds!")
            print(f"🔗 Video URL: {video_url}")
            print("\nYou can open this URL in your browser to download/view the video.")
        else:
            print("\n❌ Failed: No URL returned.")
            
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")

if __name__ == "__main__":
    test_generation()
