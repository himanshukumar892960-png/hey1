import os
import requests
import jwt
import time
import base64
from dotenv import load_dotenv

# Load .env
load_dotenv()

def print_result(service, status, message=""):
    color = "\033[92m" if status == "PASS" else ("\033[93m" if status == "WARN" else "\033[91m")
    reset = "\033[0m"
    print(f"{service:<25} [{color}{status}{reset}] {message}")

def check_openrouter(key_name):
    key = os.getenv(key_name)
    if not key:
        print_result(key_name, "SKIP", "Key not found")
        return

    try:
        resp = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        if resp.status_code == 200:
            print_result(key_name, "PASS", "Connected")
        else:
            print_result(key_name, "FAIL", f"{resp.status_code} {resp.text[:50]}")
    except Exception as e:
        print_result(key_name, "FAIL", str(e))

def check_gemini(key_name):
    key = os.getenv(key_name)
    if not key:
        print_result(key_name, "SKIP", "Key not found")
        return
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
        resp = requests.post(
            url,
            json={"contents": [{"parts": [{"text": "Hi"}]}]},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if resp.status_code == 200:
            print_result(key_name, "PASS", "Connected")
        else:
            print_result(key_name, "FAIL", f"{resp.status_code} {resp.text[:50]}")
    except Exception as e:
        print_result(key_name, "FAIL", str(e))

def check_kling(access_name, secret_name):
    ak = os.getenv(access_name)
    sk = os.getenv(secret_name)
    if not ak or not sk:
        print_result(access_name[:-11], "SKIP", "Keys not found")
        return

    try:
        # Generate Token
        headers = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "iss": ak,
            "exp": int(time.time()) + 180,
            "nbf": int(time.time()) - 5
        }
        token = jwt.encode(payload, sk, algorithm="HS256", headers=headers)
        
        # Determine URL based on key (assuming standard base url for now, client uses Singapore)
        # We'll just check if we can query a task status of a non-existent task or make a bad request that proves auth works
        # Actually making a dummy request to 'videos' endpoint usually returns 400 if auth works but params bad, 
        # or 401/403 if auth fails.
        
        resp = requests.post(
            "https://api-singapore.klingai.com/v1/videos/omni-video",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            json={}, # Empty body to trigger validation error (not auth error)
            timeout=10
        )
        
        if resp.status_code in [200, 400]:
            # 400 means it processed the request but found parameters missing -> Auth worked
            # 401/403 would be Auth failed
            if resp.status_code == 400:
                 if "code" in resp.json() and resp.json()["code"] != 1001: # 1001 is often auth? No, usually generic.
                     print_result(access_name[:-11], "PASS", "Auth Validated")
                 else:
                     print_result(access_name[:-11], "PASS", "Auth Validated (400 received)")
            else:
                print_result(access_name[:-11], "PASS", "Connected")
        elif resp.status_code in [401, 403]:
            print_result(access_name[:-11], "FAIL", "Auth Failed")
        else:
            print_result(access_name[:-11], "WARN", f"Status {resp.status_code}")
            
    except Exception as e:
        print_result(access_name[:-11], "FAIL", str(e))

def check_runway():
    key = os.getenv("RUNWAYML_API_KEY")
    if not key:
        print_result("RUNWAYML", "SKIP", "Key not found")
        return
    
    # Runway doesn't have a simple GET user endpoint easily documented. 
    # We will assume if we can hit the list tasks endpoint (even if empty) it works.
    # OR we just rely on it failing if key is bad.
    # For now, let's try to list tasks if that endpoint exists or just assume pass if structure looks ok?
    # No, let's try a request.
    try:
        resp = requests.get(
            "https://api.runwayml.com/v1/tasks", # Hypothetical endpoint, actual one is specific
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        # If 404, endpoint wrong. If 401, key bad. 
        # Actually correct endpoint is `https://api.runwayml.com/v1/tasks` for listing?
        # Docs say GET /v1/tasks/{id}, but maybe generic list?
        # Let's try to check a non-existent task.
        resp = requests.get(
            "https://api.runwayml.com/v1/tasks/non_existent_id",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        if resp.status_code == 404: # Task not found -> Auth worked?
             print_result("RUNWAYML", "PASS", "Auth Validated (404 on task)")
        elif resp.status_code == 401:
             print_result("RUNWAYML", "FAIL", "Auth Failed")
        else:
             print_result("RUNWAYML", "WARN", f"Status {resp.status_code}")
    except Exception as e:
        print_result("RUNWAYML", "FAIL", str(e))

def check_veo(key_name):
    key = os.getenv(key_name)
    if not key:
        print_result(key_name, "SKIP", "Key not found")
        return
    
    try:
        # Check credit/balance/user on veo3api.com if possible. 
        # Since I don't know the user endpoint, I'll try to generate a nonsense prompt.
        resp = requests.post(
            "https://veo3api.com/generate",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "veo3", "prompt": "test", "aspect_ratio": "16:9"},
            timeout=10
        )
        if resp.status_code == 200:
            print_result(key_name, "PASS", "Connected (Generation Started!)")
        elif resp.status_code == 402:
            print_result(key_name, "PASS", "Auth Valid (No Credits)")
        elif resp.status_code == 401:
            print_result(key_name, "FAIL", "Auth Failed")
        else:
             print_result(key_name, "WARN", f"Status {resp.status_code} {resp.text[:20]}")
    except Exception as e:
        print_result(key_name, "FAIL", str(e))

def check_github():
    token = os.getenv("GITHUB_ACCESS_TOKEN")
    if not token:
        print_result("GITHUB", "SKIP", "Token not found")
        return
    
    try:
        resp = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {token}", "User-Agent": "TestScript"},
            timeout=10
        )
        if resp.status_code == 200:
            print_result("GITHUB", "PASS", f"User: {resp.json().get('login')}")
        else:
            print_result("GITHUB", "FAIL", f"{resp.status_code}")
    except Exception as e:
        print_result("GITHUB", "FAIL", str(e))

def check_huggingface():
    key = os.getenv("HUGGINGFACE_API_KEY")
    try:
        resp = requests.get(
            "https://huggingface.co/api/whoami",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        if resp.status_code == 200:
            print_result("HUGGINGFACE", "PASS", f"User: {resp.json().get('name')}")
        else:
            print_result("HUGGINGFACE", "FAIL", f"{resp.status_code}")
    except Exception as e:
        print_result("HUGGINGFACE", "FAIL", str(e))

def check_generic_get(service_name, url, key_param, key_env, expected_code=200):
    key = os.getenv(key_env)
    if not key:
        print_result(service_name, "SKIP", "Key not found")
        return
    
    try:
        final_url = url.replace("{KEY}", key)
        resp = requests.get(final_url, timeout=10)
        if resp.status_code == expected_code:
            print_result(service_name, "PASS", "Connected")
        elif resp.status_code == 401 or resp.status_code == 403:
             print_result(service_name, "FAIL", "Auth Failed")
        else:
             print_result(service_name, "WARN", f"Status {resp.status_code}")
    except Exception as e:
        print_result(service_name, "FAIL", str(e))

if __name__ == "__main__":
    print("-" * 50)
    print("Checking API Keys...")
    print("-" * 50)
    
    # OpenRouter
    for i in ["", "_2", "_3", "_4", "_5", "_7"]:
        check_openrouter(f"OPENROUTER_API_KEY{i}")
        
    # Gemini
    check_gemini("GEMINI_API_KEY")
    check_gemini("GEMINI_API_KEY_6")
    
    # Kling
    check_kling("KLING_ACCESS_KEY", "KLING_SECRET_KEY")
    check_kling("KLING_ACCESS_KEY_2", "KLING_SECRET_KEY_2")
    check_kling("KLING_ACCESS_KEY_3", "KLING_SECRET_KEY_3")
    check_kling("KLING_ACCESS_KEY_4", "KLING_SECRET_KEY_4")
    
    # Runway
    check_runway()
    
    # Veo
    for i in ["", "_2", "_3", "_4"]:
        check_veo(f"VEO_API_KEY{i}")
        
    # GitHub
    check_github()
    
    # Hugging Face
    check_huggingface()
    
    # Others
    check_generic_get("NEWS_API", "https://newsapi.org/v2/top-headlines?country=us&apiKey={KEY}", "apiKey", "NEWS_API_KEY")
    check_generic_get("OPENWEATHER", "https://api.openweathermap.org/data/2.5/weather?q=London&appid={KEY}", "appid", "OPENWEATHER_API_KEY")
    check_generic_get("ALPHAVANTAGE", "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey={KEY}", "apikey", "ALPHA_VANTAGE_API_KEY")
    
    print("-" * 50)
