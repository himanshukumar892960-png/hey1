import os
import sys
import requests
from dotenv import load_dotenv

# Set default encoding to UTF-8 for windows terminal output
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

# Load environment variables
load_dotenv()

# Import Clients
try:
    from openrouter_client import OpenRouterClient
    from freepik_client import FreepikClient
    from huggingface_client import HuggingFaceClient
    from imagen_client import ImagenClient
    from youtube_service import YouTubeService
    from gemini_client import GeminiClient
    from weather_service import WeatherService
    from news_service import NewsService
    from stock_service import StockService
    from crypto_service import CryptoService
    from stability_client import StabilityClient
    from runway_client import RunwayClient
except ImportError as e:
    print(f"[ERROR] Import Error: {e}")
    # Don't exit, might be able to test others

def print_separator(name):
    print(f"\n{'='*20} {name} {'='*20}")

def test_gemini():
    print_separator("Gemini")
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY_6")
    if not key:
        print("[ERROR] Missing GEMINI_API_KEY")
        return
    
    print(f"Key found: {key[:10]}...")
    try:
        client = GeminiClient(key)
        if client.model:
            print(f"Discovered Model: {client.model.model_name}")
            res = client.get_response("Hi")
            print(f"[SUCCESS] Gemini Response: {res[:100]}...")
        else:
            print("[ERROR] No working Gemini models found.")
    except Exception as e:
        print(f"[ERROR] Gemini Error: {e}")

def test_openrouter():
    print_separator("OpenRouter")
    keys = ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2", "OPENROUTER_API_KEY_3", "OPENROUTER_API_KEY_4", "OPENROUTER_API_KEY_5", "OPENROUTER_API_KEY_7"]
    for k_name in keys:
        key = os.getenv(k_name)
        if not key:
            print(f"[SKIP] {k_name} not found")
            continue
        
        model = os.getenv(k_name.replace("API_KEY", "MODEL"), "deepseek/deepseek-chat")
        print(f"Testing {k_name} with model {model}...")
        client = OpenRouterClient(key, model=model)
        try:
            response = client.get_response("Say 'OK'")
            print(f"[SUCCESS] {k_name} Response: {response[:100]}...")
        except Exception as e:
            print(f"[ERROR] {k_name} Error: {e}")

def test_freepik():
    print_separator("Freepik")
    key = os.getenv("FREEPIK_API_KEY")
    if not key:
        print("[SKIP] Missing FREEPIK_API_KEY")
        return
    
    # Try 'pikaso' which is a common Freepik engine
    print("Testing image generation (pikaso)...")
    client = FreepikClient(key, model="pikaso")
    try:
        img = client.generate_image("A small dot")
        if img:
            print("[SUCCESS] Freepik Image received")
        else:
            print("[ERROR] Freepik failed to return image")
    except Exception as e:
        print(f"[ERROR] Freepik Exception: {e}")

def test_huggingface():
    print_separator("Hugging Face")
    key = os.getenv("HUGGINGFACE_API_KEY")
    if not key:
        print("[SKIP] Missing HUGGINGFACE_API_KEY")
        return
    print("Testing image generation...")
    client = HuggingFaceClient(key)
    try:
        img = client.generate_image("A tiny star")
        if img:
            print("[SUCCESS] HF Image received")
        else:
            print("[ERROR] HF failed")
    except Exception as e:
        print(f"[ERROR] HF Exception: {e}")

def test_stability():
    print_separator("Stability AI")
    key = os.getenv("STABILITY_API_KEY")
    if not key:
        print("[SKIP] Missing STABILITY_API_KEY")
        return
    client = StabilityClient(key)
    try:
        img = client.generate_image("Sunset")
        if img and img.startswith("data:image"):
            print("[SUCCESS] Stability Image received")
        else:
            print(f"[ERROR] Stability failed: {img}")
    except Exception as e:
        print(f"[ERROR] Stability Exception: {e}")

def test_runway():
    print_separator("RunwayML")
    key = os.getenv("RUNWAYML_API_KEY")
    if not key:
        print("[SKIP] Missing RUNWAYML_API_KEY")
        return
    client = RunwayClient(key)
    print("Testing video generation (this uses credits)...")
    try:
        # Note: Previous check showed 'no credits' or 'forbidden'
        # We'll just report what happens.
        res = client.generate_video("A leaf falling")
        if res and res.startswith("http"):
            print(f"[SUCCESS] Runway Video URL: {res}")
        else:
            print(f"[ERROR] Runway failed: {res}")
    except Exception as e:
        print(f"[ERROR] Runway Exception: {e}")

def test_youtube():
    print_separator("YouTube")
    key = os.getenv("YOUTUBE_API_KEY")
    if not key:
        print("[SKIP] Missing YOUTUBE_API_KEY")
        return
    service = YouTubeService(key)
    try:
        res = service.search_videos("test", max_results=1)
        if "Error" in res:
            print(f"[ERROR] YouTube Search: {res}")
        else:
            print("[SUCCESS] YouTube Search working")
    except Exception as e:
        print(f"[ERROR] YouTube Exception: {e}")

def test_weather():
    print_separator("Weather")
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        print("[SKIP] Missing OPENWEATHER_API_KEY")
        return
    service = WeatherService(key)
    try:
        res = service.get_weather("London")
        if "Error" in res:
             print(f"[ERROR] Weather: {res}")
        else:
             print(f"[SUCCESS] Weather: {res[:50]}...")
    except Exception as e:
        print(f"[ERROR] Weather Exception: {e}")

def test_news():
    print_separator("News")
    key = os.getenv("NEWS_API_KEY")
    if not key:
        print("[SKIP] Missing NEWS_API_KEY")
        return
    service = NewsService(key)
    try:
        res = service.get_top_news()
        if not res or "Error" in res:
             print(f"[ERROR] News: {res}")
        else:
             print(f"[SUCCESS] News working")
    except Exception as e:
        print(f"[ERROR] News Exception: {e}")

def test_stocks():
    print_separator("Stocks (Alpha Vantage)")
    key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not key:
        print("[SKIP] Missing ALPHA_VANTAGE_API_KEY")
        return
    service = StockService(key)
    try:
        res = service.get_stock_price("AAPL")
        if "Error" in res or "I couldn't find" in res:
             print(f"[ERROR] Stock: {res}")
        else:
             print(f"[SUCCESS] Stock: {res}")
    except Exception as e:
        print(f"[ERROR] Stock Exception: {e}")

def test_crypto():
    print_separator("Crypto (CoinMarketCap)")
    key = os.getenv("CMC_API_KEY")
    if not key:
        print("[SKIP] Missing CMC_API_KEY")
        return
    service = CryptoService(key)
    try:
        res = service.get_price("BTC")
        if "Error" in res or "I couldn't fetch" in res:
             print(f"[ERROR] Crypto: {res}")
        else:
             print(f"[SUCCESS] Crypto: {res}")
    except Exception as e:
        print(f"[ERROR] Crypto Exception: {e}")

if __name__ == "__main__":
    print("___ COMPREHENSIVE API DIAGNOSTICS ___")
    test_gemini()
    test_openrouter()
    test_freepik()
    test_huggingface()
    test_stability()
    test_runway()
    test_youtube()
    test_weather()
    test_news()
    test_stocks()
    test_crypto()
    print("\n___ DIAGNOSTICS COMPLETE ___")
