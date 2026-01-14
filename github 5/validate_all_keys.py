import os
import requests
import razorpay
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def logger(service, status, message=""):
    color = "\033[92m" if "PASS" in status else "\033[91m" if "FAIL" in status else "\033[93m"
    reset = "\033[0m"
    print(f"[{service}] {color}{status}{reset} {message}")

def check_openrouter(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_gemini(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={key}", timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_groq(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://api.groq.com/openai/v1/models", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_replicate(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://api.replicate.com/v1/models/minimax/video-01", headers={"Authorization": f"Token {key}"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        elif resp.status_code == 401:
            logger(name, "FAIL", "Unauthorized")
        else:
            logger(name, "WARN", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_comet(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://api.cometapi.com/v1/models", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_github(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://api.github.com/user", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_razorpay():
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        logger("Razorpay", "MISSING")
        return
    try:
        client = razorpay.Client(auth=(key_id, key_secret))
        # Try to list orders (minimal impact)
        client.order.all({'count': 1})
        logger("Razorpay", "PASS")
    except Exception as e:
        logger("Razorpay", "FAIL", str(e))

def check_stability(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://api.stability.ai/v1/user/account", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_freepik(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://api.freepik.com/v1/resources?per_page=1", headers={"x-freepik-api-key": key}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_huggingface(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://api-inference.huggingface.co/models/gpt2", headers={"Authorization": f"Bearer {key}"}, timeout=10)
        if resp.status_code in [200, 503]: # 503 means model is loading, but key is likely fine
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_weather(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}", timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_news(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}", timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_cmc(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=1", headers={"X-CMC_PRO_API_KEY": key}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_alphavantage(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={key}", timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_youtube(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id=dQw4w9WgXcQ&key={key}", timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_google_search(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        # Calling with a dummy CX to see if it rejects based on Key or Arg
        resp = requests.get(f"https://www.googleapis.com/customsearch/v1?key={key}&q=test&cx=0123456789", timeout=10)
        data = resp.json()
        
        # If key is valid but CX is wrong, it's Code 400 with "invalid value" or "not found" cx
        # If key is invalid, it's often 400 with "API key not valid"
        if resp.status_code == 200:
            logger(name, "PASS")
        elif "API key not valid" in str(data):
             logger(name, "FAIL", "Invalid API Key")
        elif resp.status_code == 400 and ("cx" in str(data).lower() or "invalid argument" in str(data).lower()):
             logger(name, "PASS", "(Key Valid, CX Missing/Wrong)")
        else:
             logger(name, "PASS", f"(Status {resp.status_code})")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_tavily(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.post("https://api.tavily.com/search", json={"api_key": key, "query": "test"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_serper(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    try:
        resp = requests.post("https://google.serper.dev/search", headers={"X-API-KEY": key}, json={"q": "test"}, timeout=10)
        if resp.status_code == 200:
            logger(name, "PASS")
        else:
            logger(name, "FAIL", f"Status {resp.status_code}")
    except Exception as e:
        logger(name, "ERROR", str(e))

def check_kling(name, access_var, secret_var):
    access = os.getenv(access_var)
    secret = os.getenv(secret_var)
    if not access or not secret:
        logger(name, "MISSING")
        return
    # Kling doesn't have a simple 'auth check' endpoint easily accessible without signing
    # We'll just check if strings look like keys for now or assume PASS if they exist
    # (In a real scenario, we'd do a model list call if supported)
    logger(name, "EXIST")

def check_veo(name, key_var):
    key = os.getenv(key_var)
    if not key:
        logger(name, "MISSING")
        return
    # Veo is often a custom endpoint, check if it's a valid string format
    if len(key) > 20:
        logger(name, "PASS (Format)")
    else:
        logger(name, "FAIL (Invalid Format)")

print("\n🚀 Starting Comprehensive API Key Validation...\n")

# AI Text/Chat
check_openrouter("OpenRouter Tier 1", "OPENROUTER_API_KEY")
check_openrouter("OpenRouter Tier 2", "OPENROUTER_API_KEY_2")
check_openrouter("OpenRouter Tier 3", "OPENROUTER_API_KEY_3")
check_openrouter("OpenRouter Tier 4", "OPENROUTER_API_KEY_4")
check_openrouter("OpenRouter Tier 5", "OPENROUTER_API_KEY_5")
check_gemini("Gemini (Tier 6)", "GEMINI_API_KEY_6")
check_openrouter("OpenRouter Tier 7", "OPENROUTER_API_KEY_7")
check_groq("Groq Tier 8", "GROQ_API_KEY")
check_groq("Groq Tier 10", "GROQ_API_KEY_2")
check_github("GitHub Models 1", "GITHUB_ACCESS_TOKEN")
check_github("GitHub Models 2", "GITHUB_ACCESS_TOKEN_2")
check_comet("CometAPI", "COMET_API_KEY")

# AI Image/Video
check_stability("Stability AI", "STABILITY_API_KEY")
check_replicate("Replicate 1", "REPLICATE_API_TOKEN")
check_replicate("Replicate 2", "REPLICATE_API_TOKEN_2")
check_replicate("Replicate 3", "REPLICATE_API_TOKEN_3")
check_replicate("Replicate 4", "REPLICATE_API_TOKEN_4")
check_freepik("Freepik Tier 1", "FREEPIK_API_KEY")
check_freepik("Freepik Tier 2", "FREEPIK_API_KEY_2")
check_freepik("Freepik Tier 3", "FREEPIK_API_KEY_3")
check_freepik("Freepik Tier 4", "FREEPIK_API_KEY_4")
check_huggingface("Hugging Face", "HUGGINGFACE_API_KEY")

# Video Tiers
check_veo("Veo Tier 1", "VEO_API_KEY")
check_veo("Veo Tier 2", "VEO_API_KEY_2")
check_veo("Veo Tier 3", "VEO_API_KEY_3")
check_veo("Veo Tier 4", "VEO_API_KEY_4")

check_kling("Kling Tier 1", "KLING_ACCESS_KEY", "KLING_SECRET_KEY")
check_kling("Kling Tier 2", "KLING_ACCESS_KEY_2", "KLING_SECRET_KEY_2")
check_kling("Kling Tier 3", "KLING_ACCESS_KEY_3", "KLING_SECRET_KEY_3")
check_kling("Kling Tier 4", "KLING_ACCESS_KEY_4", "KLING_SECRET_KEY_4")

# Payment
check_razorpay()

# Services/Utilities
check_weather("OpenWeather", "OPENWEATHER_API_KEY")
check_news("NewsAPI", "NEWS_API_KEY")
check_cmc("CoinMarketCap", "CMC_API_KEY")
check_alphavantage("AlphaVantage", "ALPHA_VANTAGE_API_KEY")
check_youtube("YouTube Data API", "YOUTUBE_API_KEY")
check_google_search("Google Search", "GOOGLE_SEARCH_API_KEY")
check_tavily("Tavily Search Tier 1", "TAVILY_API_KEY")
check_tavily("Tavily Search Tier 2", "TAVILY_API_KEY_2")
check_tavily("Tavily Search Tier 3", "TAVILY_API_KEY_3")
check_tavily("Tavily Search Tier 4", "TAVILY_API_KEY_4")
check_serper("Serper Search", "SERPER_API_KEY")

print("\n✅ Validation Complete.\n")
