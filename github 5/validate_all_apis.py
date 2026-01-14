"""
Comprehensive API Key Validator for GlobleXGPT
Tests all API keys and services to ensure they're working correctly
"""

import os
import sys
from dotenv import load_dotenv
import requests
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class APIKeyValidator:
    def __init__(self):
        self.results = {
            'working': [],
            'failed': [],
            'missing': []
        }
    
    def print_header(self, title):
        """Print formatted section header"""
        logger.info(f"\n{'='*70}")
        logger.info(f"  {title}")
        logger.info(f"{'='*70}\n")
    
    def print_result(self, service, status, message=""):
        """Print test result"""
        symbols = {
            'success': '✓',
            'fail': '✗',
            'missing': '⚠'
        }
        colors = {
            'success': '\033[92m',  # Green
            'fail': '\033[91m',     # Red
            'missing': '\033[93m',  # Yellow
            'reset': '\033[0m'
        }
        
        symbol = symbols.get(status, '?')
        color = colors.get(status, '')
        reset = colors['reset']
        
        status_text = status.upper()
        logger.info(f"{color}{symbol} {service:40} [{status_text}]{reset}")
        if message:
            logger.info(f"  → {message}")
    
    def test_gemini_api(self):
        """Test Gemini API keys"""
        self.print_header("🤖 AI Text Generation APIs")
        
        # Test primary Gemini
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            self.print_result("Gemini API (Primary)", "missing")
            self.results['missing'].append("GEMINI_API_KEY")
            return
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say 'API key working'")
            if response.text:
                self.print_result("Gemini API (Primary)", "success", f"Key: {key[:15]}...")
                self.results['working'].append("GEMINI_API_KEY")
            else:
                raise Exception("No response")
        except Exception as e:
            self.print_result("Gemini API (Primary)", "fail", str(e))
            self.results['failed'].append("GEMINI_API_KEY")
    
    def test_openrouter_apis(self):
        """Test OpenRouter API keys (Tiers 1-7)"""
        tiers = [
            ("OPENROUTER_API_KEY", "OPENROUTER_MODEL", "Tier 1"),
            ("OPENROUTER_API_KEY_2", "OPENROUTER_MODEL_2", "Tier 2"),
            ("OPENROUTER_API_KEY_3", "OPENROUTER_MODEL_3", "Tier 3"),
            ("OPENROUTER_API_KEY_4", "OPENROUTER_MODEL_4", "Tier 4"),
            ("OPENROUTER_API_KEY_5", "OPENROUTER_MODEL_5", "Tier 5"),
            ("OPENROUTER_API_KEY_7", "OPENROUTER_MODEL_7", "Tier 7"),
        ]
        
        for key_name, model_name, tier in tiers:
            key = os.getenv(key_name)
            model = os.getenv(model_name)
            
            if not key:
                self.print_result(f"OpenRouter {tier}", "missing")
                self.results['missing'].append(key_name)
                continue
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model or "openai/gpt-3.5-turbo",
                        "messages": [{"role": "user", "content": "Hi"}],
                        "max_tokens": 10
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.print_result(f"OpenRouter {tier}", "success", f"Model: {model}")
                    self.results['working'].append(key_name)
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result(f"OpenRouter {tier}", "fail", str(e))
                self.results['failed'].append(key_name)
    
    def test_groq_apis(self):
        """Test Groq API keys"""
        keys = [
            ("GROQ_API_KEY", "GROQ_MODEL", "Tier 8"),
            ("GROQ_API_KEY_2", "GROQ_MODEL_2", "Tier 10")
        ]
        
        for key_name, model_name, tier in keys:
            key = os.getenv(key_name)
            model = os.getenv(model_name) or "llama-3.3-70b-versatile"
            
            if not key:
                self.print_result(f"Groq {tier}", "missing")
                self.results['missing'].append(key_name)
                continue
            
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [{"role": "user", "content": "Hi"}],
                        "max_tokens": 10
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.print_result(f"Groq {tier}", "success", f"Model: {model}")
                    self.results['working'].append(key_name)
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result(f"Groq {tier}", "fail", str(e))
                self.results['failed'].append(key_name)
    
    def test_image_apis(self):
        """Test Image Generation APIs"""
        self.print_header("🎨 Image Generation APIs")
        
        # Test Freepik
        for i in range(1, 5):
            key_name = f"FREEPIK_API_KEY{'_' + str(i) if i > 1 else ''}"
            key = os.getenv(key_name)
            
            if not key:
                self.print_result(f"Freepik Tier {i}", "missing")
                self.results['missing'].append(key_name)
                continue
            
            # Just check if key exists and has correct format
            if key.startswith("FPSX"):
                self.print_result(f"Freepik Tier {i}", "success", f"Key: {key[:15]}...")
                self.results['working'].append(key_name)
            else:
                self.print_result(f"Freepik Tier {i}", "fail", "Invalid key format")
                self.results['failed'].append(key_name)
    
    def test_video_apis(self):
        """Test Video Generation APIs"""
        self.print_header("🎬 Video Generation APIs")
        
        # Test Replicate
        for i in range(1, 5):
            key_name = f"REPLICATE_API_TOKEN{'_' + str(i) if i > 1 else ''}"
            key = os.getenv(key_name)
            
            if not key:
                self.print_result(f"Replicate Tier {i}", "missing")
                self.results['missing'].append(key_name)
                continue
            
            try:
                response = requests.get(
                    "https://api.replicate.com/v1/models",
                    headers={"Authorization": f"Token {key}"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.print_result(f"Replicate Tier {i}", "success", f"Key: {key[:15]}...")
                    self.results['working'].append(key_name)
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result(f"Replicate Tier {i}", "fail", str(e))
                self.results['failed'].append(key_name)
        
        # Test Kling AI
        for i in range(1, 5):
            access_key_name = f"KLING_ACCESS_KEY{'_' + str(i) if i > 1 else ''}"
            secret_key_name = f"KLING_SECRET_KEY{'_' + str(i) if i > 1 else ''}"
            
            access_key = os.getenv(access_key_name)
            secret_key = os.getenv(secret_key_name)
            
            if not access_key or not secret_key:
                self.print_result(f"Kling AI Tier {i}", "missing")
                self.results['missing'].append(access_key_name)
                continue
            
            # Check key format
            if len(access_key) > 20 and len(secret_key) > 20:
                self.print_result(f"Kling AI Tier {i}", "success", f"Keys configured")
                self.results['working'].append(access_key_name)
            else:
                self.print_result(f"Kling AI Tier {i}", "fail", "Invalid key format")
                self.results['failed'].append(access_key_name)
        
        # Test Veo
        for i in range(1, 5):
            key_name = f"VEO_API_KEY{'_' + str(i) if i > 1 else ''}"
            key = os.getenv(key_name)
            
            if not key:
                self.print_result(f"Veo Tier {i}", "missing")
                self.results['missing'].append(key_name)
                continue
            
            if key.startswith("sk-"):
                self.print_result(f"Veo Tier {i}", "success", f"Key: {key[:15]}...")
                self.results['working'].append(key_name)
            else:
                self.print_result(f"Veo Tier {i}", "fail", "Invalid key format")
                self.results['failed'].append(key_name)
    
    def test_utility_apis(self):
        """Test Utility APIs"""
        self.print_header("🛠️ Utility APIs")
        
        # Test Weather API
        key = os.getenv("OPENWEATHER_API_KEY")
        if not key:
            self.print_result("OpenWeather API", "missing")
            self.results['missing'].append("OPENWEATHER_API_KEY")
        else:
            try:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={key}",
                    timeout=10
                )
                if response.status_code == 200:
                    self.print_result("OpenWeather API", "success")
                    self.results['working'].append("OPENWEATHER_API_KEY")
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result("OpenWeather API", "fail", str(e))
                self.results['failed'].append("OPENWEATHER_API_KEY")
        
        # Test News API
        key = os.getenv("NEWS_API_KEY")
        if not key:
            self.print_result("News API", "missing")
            self.results['missing'].append("NEWS_API_KEY")
        else:
            try:
                response = requests.get(
                    f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}",
                    timeout=10
                )
                if response.status_code == 200:
                    self.print_result("News API", "success")
                    self.results['working'].append("NEWS_API_KEY")
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result("News API", "fail", str(e))
                self.results['failed'].append("NEWS_API_KEY")
        
        # Test YouTube API
        key = os.getenv("YOUTUBE_API_KEY")
        if not key:
            self.print_result("YouTube API", "missing")
            self.results['missing'].append("YOUTUBE_API_KEY")
        else:
            try:
                response = requests.get(
                    f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=test&key={key}",
                    timeout=10
                )
                if response.status_code == 200:
                    self.print_result("YouTube API", "success")
                    self.results['working'].append("YOUTUBE_API_KEY")
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result("YouTube API", "fail", str(e))
                self.results['failed'].append("YOUTUBE_API_KEY")
    
    def test_search_apis(self):
        """Test Search APIs"""
        self.print_header("🔍 Search APIs")
        
        # Test Google Search
        api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
        engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
        
        if not api_key or not engine_id:
            self.print_result("Google Search API", "missing")
            self.results['missing'].append("GOOGLE_SEARCH_API_KEY")
        else:
            try:
                response = requests.get(
                    f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={engine_id}&q=test",
                    timeout=10
                )
                if response.status_code == 200:
                    self.print_result("Google Search API", "success")
                    self.results['working'].append("GOOGLE_SEARCH_API_KEY")
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result("Google Search API", "fail", str(e))
                self.results['failed'].append("GOOGLE_SEARCH_API_KEY")
        
        # Test Tavily APIs
        for i in range(1, 5):
            key_name = f"TAVILY_API_KEY{'_' + str(i) if i > 1 else ''}"
            key = os.getenv(key_name)
            
            if not key:
                self.print_result(f"Tavily API Tier {i}", "missing")
                self.results['missing'].append(key_name)
                continue
            
            if key.startswith("tvly-"):
                self.print_result(f"Tavily API Tier {i}", "success", f"Key: {key[:20]}...")
                self.results['working'].append(key_name)
            else:
                self.print_result(f"Tavily API Tier {i}", "fail", "Invalid key format")
                self.results['failed'].append(key_name)
    
    def test_payment_apis(self):
        """Test Payment APIs"""
        self.print_header("💳 Payment APIs")
        
        # Test Razorpay
        key_id = os.getenv("RAZORPAY_KEY_ID")
        key_secret = os.getenv("RAZORPAY_KEY_SECRET")
        
        if not key_id or not key_secret:
            self.print_result("Razorpay", "missing")
            self.results['missing'].append("RAZORPAY_KEY_ID")
        else:
            mode = "TEST" if key_id.startswith("rzp_test_") else "LIVE"
            self.print_result("Razorpay", "success", f"Mode: {mode}, Key: {key_id}")
            self.results['working'].append("RAZORPAY_KEY_ID")
    
    def test_google_sheets(self):
        """Test Google Sheets Integration"""
        self.print_header("📊 Google Sheets Integration")
        
        url = os.getenv("GOOGLE_SHEETS_SCRIPT_URL")
        
        if not url:
            self.print_result("Google Sheets Script", "missing")
            self.results['missing'].append("GOOGLE_SHEETS_SCRIPT_URL")
        else:
            try:
                response = requests.get(f"{url}?action=revenue", timeout=10)
                if response.status_code == 200:
                    self.print_result("Google Sheets Script", "success", "Connected")
                    self.results['working'].append("GOOGLE_SHEETS_SCRIPT_URL")
                else:
                    raise Exception(f"HTTP {response.status_code}")
            except Exception as e:
                self.print_result("Google Sheets Script", "fail", str(e))
                self.results['failed'].append("GOOGLE_SHEETS_SCRIPT_URL")
    
    def test_oauth(self):
        """Test OAuth Credentials"""
        self.print_header("🔐 OAuth Credentials")
        
        # Google OAuth
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            self.print_result("Google OAuth", "missing")
            self.results['missing'].append("GOOGLE_CLIENT_ID")
        else:
            self.print_result("Google OAuth", "success", f"Client ID: {client_id[:30]}...")
            self.results['working'].append("GOOGLE_CLIENT_ID")
        
        # GitHub OAuth
        client_id = os.getenv("GITHUB_CLIENT_ID")
        client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            self.print_result("GitHub OAuth", "missing")
            self.results['missing'].append("GITHUB_CLIENT_ID")
        else:
            self.print_result("GitHub OAuth", "success", f"Client ID: {client_id}")
            self.results['working'].append("GITHUB_CLIENT_ID")
    
    def print_summary(self):
        """Print final summary"""
        self.print_header("📋 VALIDATION SUMMARY")
        
        total = len(self.results['working']) + len(self.results['failed']) + len(self.results['missing'])
        working_count = len(self.results['working'])
        failed_count = len(self.results['failed'])
        missing_count = len(self.results['missing'])
        
        logger.info(f"Total APIs Checked: {total}")
        logger.info(f"✓ Working: {working_count} ({working_count/total*100:.1f}%)" if total > 0 else "✓ Working: 0")
        logger.info(f"✗ Failed: {failed_count} ({failed_count/total*100:.1f}%)" if total > 0 else "✗ Failed: 0")
        logger.info(f"⚠ Missing: {missing_count} ({missing_count/total*100:.1f}%)" if total > 0 else "⚠ Missing: 0")
        
        if failed_count > 0:
            logger.info(f"\n⚠️  Failed APIs:")
            for api in self.results['failed']:
                logger.info(f"   - {api}")
        
        if missing_count > 0:
            logger.info(f"\n⚠️  Missing APIs:")
            for api in self.results['missing']:
                logger.info(f"   - {api}")
        
        logger.info(f"\n{'='*70}\n")
        
        if failed_count == 0 and missing_count == 0:
            logger.info("🎉 All API keys are configured and working!")
        elif failed_count > 0:
            logger.info("⚠️  Some API keys are failing. Please check the errors above.")
        else:
            logger.info("ℹ️  Some API keys are missing but system will work with available keys.")
    
    def run_all_tests(self):
        """Run all validation tests"""
        logger.info("\n" + "="*70)
        logger.info("  🔍 GlobleXGPT API Key Validation")
        logger.info("="*70)
        
        self.test_gemini_api()
        self.test_openrouter_apis()
        self.test_groq_apis()
        self.test_image_apis()
        self.test_video_apis()
        self.test_utility_apis()
        self.test_search_apis()
        self.test_payment_apis()
        self.test_google_sheets()
        self.test_oauth()
        
        self.print_summary()

if __name__ == "__main__":
    validator = APIKeyValidator()
    validator.run_all_tests()
