import os
import requests
import json
from dotenv import load_dotenv
from gemini_client import GeminiClient
from openrouter_client import OpenRouterClient

load_dotenv()

def test_key(name, client_class, key, model=None):
    if not key or key == "your_api_key_here":
        return f"{name}: Skipped (No key)"
    
    try:
        client = client_class(key, model) if model else client_class(key)
        response = client.get_full_response("Hi")
        if response and response.get('response') and "Error" not in response.get('response'):
            return f"{name}: WORKING"
        else:
            err = response.get('response') if response else 'No response'
            return f"{name}: FAILED ({str(err)[:100]})"
    except Exception as e:
        return f"{name}: ERROR ({str(e)[:100]})"

def check_all_keys():
    results = []
    results.append(test_key("Tier 1 (OpenRouter)", OpenRouterClient, os.getenv("OPENROUTER_API_KEY"), os.getenv("OPENROUTER_MODEL")))
    results.append(test_key("Tier 2 (OpenRouter)", OpenRouterClient, os.getenv("OPENROUTER_API_KEY_2"), os.getenv("OPENROUTER_MODEL_2")))
    results.append(test_key("Tier 3 (OpenRouter)", OpenRouterClient, os.getenv("OPENROUTER_API_KEY_3"), os.getenv("OPENROUTER_MODEL_3")))
    results.append(test_key("Tier 4 (OpenRouter)", OpenRouterClient, os.getenv("OPENROUTER_API_KEY_4"), os.getenv("OPENROUTER_MODEL_4")))
    results.append(test_key("Tier 5 (OpenRouter)", OpenRouterClient, os.getenv("OPENROUTER_API_KEY_5"), os.getenv("OPENROUTER_MODEL_5")))
    results.append(test_key("Tier 6 (Gemini)", GeminiClient, os.getenv("GEMINI_API_KEY_6") or os.getenv("GEMINI_API_KEY")))
    results.append(test_key("Tier 7 (OpenRouter)", OpenRouterClient, os.getenv("OPENROUTER_API_KEY_7"), os.getenv("OPENROUTER_MODEL_7")))

    with open("key_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    
if __name__ == "__main__":
    check_all_keys()
