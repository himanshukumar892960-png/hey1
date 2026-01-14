import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_openrouter(tier, key_var):
    key = os.getenv(key_var)
    if not key:
        print(f"Tier {tier} ({key_var}): ⚠️  MISSING")
        return

    try:
        resp = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {key}"},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            # safe access
            usage = data.get('data', {}).get('limit')
            label = "Unlimited" if usage is None else f"Limit: {usage}"
            print(f"Tier {tier} ({key_var}): PASS ({label})")
        elif resp.status_code == 401:
             print(f"Tier {tier} ({key_var}): FAIL (Invalid Key)")
        else:
            print(f"Tier {tier} ({key_var}): WARN (Status {resp.status_code})")
    except Exception as e:
        print(f"Tier {tier} ({key_var}): ERROR ({str(e)})")

def check_gemini(tier, key_var):
    key = os.getenv(key_var)
    if not key:
        print(f"Tier {tier} ({key_var}): MISSING")
        return

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
        resp = requests.get(url, timeout=10)
        
        if resp.status_code == 200:
            print(f"Tier {tier} ({key_var}): PASS (Connected)")
        else:
            print(f"Tier {tier} ({key_var}): FAIL (Status {resp.status_code})")
    except Exception as e:
        print(f"Tier {tier} ({key_var}): ERROR ({str(e)})")

print("\n=== Checking 7-Tier AI Fallback System ===\n")

# Tier 1
check_openrouter(1, "OPENROUTER_API_KEY")

# Tier 2
check_openrouter(2, "OPENROUTER_API_KEY_2")

# Tier 3
check_openrouter(3, "OPENROUTER_API_KEY_3")

# Tier 4
check_openrouter(4, "OPENROUTER_API_KEY_4")

# Tier 5
check_openrouter(5, "OPENROUTER_API_KEY_5")

# Tier 6 (Gemini)
check_gemini(6, "GEMINI_API_KEY_6")

# Tier 7
check_openrouter(7, "OPENROUTER_API_KEY_7")

print("\n==========================================\n")
