from dotenv import load_dotenv
import os
load_dotenv()

from flask import Flask, render_template, request, jsonify, send_from_directory, redirect
from flask_cors import CORS
import json
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from gemini_client import GeminiClient
from openrouter_client import OpenRouterClient
from system_control import SystemControl
from weather_service import WeatherService
from news_service import NewsService
from imagen_client import ImagenClient
from stability_client import StabilityClient
from crypto_service import CryptoService
from stock_service import StockService
from runway_client import RunwayClient
from freepik_client import FreepikClient
from huggingface_client import HuggingFaceClient
from veo_client import VeoClient
from youtube_service import YouTubeService
from kling_client import KlingClient
from replicate_client import ReplicateClient
from github_client import GitHubClient
from groq_client import GroqClient
from comet_client import CometClient
from search_engine_client import search_client
from emoji_service import emoji_service
from google_sheets_service import sheets_service
import razorpay
import hmac
import hashlib
import json
from datetime import datetime, timedelta

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Only add file handler if we're not on Vercel or if we have write access
if not os.environ.get('VERCEL'):
    try:
        file_handler = logging.FileHandler('auth_debug.log')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logging.getLogger().addHandler(file_handler) 
        logging.getLogger().setLevel(logging.DEBUG)

    except Exception as e:
        print(f"Could not initialize file logging: {e}")

import local_db
# Initialize DB on startup
local_db.init_db()

app = Flask(__name__)
CORS(app)

@app.after_request
def add_security_headers(response):
    # Fix for Google Login COOP errors
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    # response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp' # Commented out to fix blocking issues
    return response

@app.errorhandler(500)
def handle_500_error(e):
    logger.error(f"Internal Server Error: {e}")
    return jsonify({"response": "I'm sorry, I encountered a server-side error while processing your request. Our team has been notified.", "emotion": "Sad"}), 500

# Load API key from environment variable
API_KEY = os.getenv("GEMINI_API_KEY") 
if not API_KEY:
    print("Warning: GEMINI_API_KEY not found in .env file.")

# Usage Limits
FREE_IMAGE_LIMIT = 2
FREE_VIDEO_LIMIT = 1

# Load Google OAuth Credentials
GOOGLE_CLIENT_ID = (os.getenv("GOOGLE_CLIENT_ID") or "").strip()
GOOGLE_CLIENT_SECRET = (os.getenv("GOOGLE_CLIENT_SECRET") or "").strip()

if not GOOGLE_CLIENT_ID:
    print("Warning: GOOGLE_CLIENT_ID not found in .env file.")

gemini = GeminiClient(API_KEY)
system = SystemControl()
weather = WeatherService(os.getenv("OPENWEATHER_API_KEY"))
news = NewsService(os.getenv("NEWS_API_KEY"))
crypto = CryptoService(os.getenv("CMC_API_KEY"))
stock = StockService(os.getenv("ALPHA_VANTAGE_API_KEY"))
youtube = YouTubeService(os.getenv("YOUTUBE_API_KEY"))

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")
razorpay_client = None

if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    try:
        logger.info(f"Attempting to initialize Razorpay with Key ID: {RAZORPAY_KEY_ID[:8]}...")
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        logger.info("✓ Razorpay Client initialized")
    except Exception as e:
        logger.error(f"✗ Razorpay initialization failed: {e}")
else:
    logger.warning("⚠ Razorpay keys not found in environment!")

# Initialize AI Assistants - 7 Tier Fallback System
ai_tiers = []

# Tier 1: Primary OpenRouter
tier1_key = os.getenv("OPENROUTER_API_KEY")
tier1_model = os.getenv("OPENROUTER_MODEL")
if tier1_key and tier1_key != "your_api_key_here":
    try:
        ai_tiers.append({
            "client": OpenRouterClient(tier1_key, tier1_model),
            "name": f"Tier 1 (OpenRouter - {tier1_model})",
            "tier": 1
        })
        logger.info(f"✓ Tier 1 initialized: {tier1_model}")
    except Exception as e:
        logger.error(f"✗ Tier 1 failed to initialize: {e}")

# Tier 2: Secondary OpenRouter
tier2_key = os.getenv("OPENROUTER_API_KEY_2")
tier2_model = os.getenv("OPENROUTER_MODEL_2")
if tier2_key and tier2_key != "your_api_key_here":
    try:
        ai_tiers.append({
            "client": OpenRouterClient(tier2_key, tier2_model),
            "name": f"Tier 2 (OpenRouter - {tier2_model})",
            "tier": 2
        })
        logger.info(f"✓ Tier 2 initialized: {tier2_model}")
    except Exception as e:
        logger.error(f"✗ Tier 2 failed to initialize: {e}")

# Tier 3: Third OpenRouter
tier3_key = os.getenv("OPENROUTER_API_KEY_3")
tier3_model = os.getenv("OPENROUTER_MODEL_3")
if tier3_key and tier3_key != "your_third_api_key_here":
    try:
        ai_tiers.append({
            "client": OpenRouterClient(tier3_key, tier3_model),
            "name": f"Tier 3 (OpenRouter - {tier3_model})",
            "tier": 3
        })
        logger.info(f"✓ Tier 3 initialized: {tier3_model}")
    except Exception as e:
        logger.error(f"✗ Tier 3 failed to initialize: {e}")

# Tier 4: Fourth OpenRouter
tier4_key = os.getenv("OPENROUTER_API_KEY_4")
tier4_model = os.getenv("OPENROUTER_MODEL_4")
if tier4_key and tier4_key != "your_fourth_api_key_here":
    try:
        ai_tiers.append({
            "client": OpenRouterClient(tier4_key, tier4_model),
            "name": f"Tier 4 (OpenRouter - {tier4_model})",
            "tier": 4
        })
        logger.info(f"✓ Tier 4 initialized: {tier4_model}")
    except Exception as e:
        logger.error(f"✗ Tier 4 failed to initialize: {e}")

# Tier 5: Fifth OpenRouter
tier5_key = os.getenv("OPENROUTER_API_KEY_5")
tier5_model = os.getenv("OPENROUTER_MODEL_5")
if tier5_key and tier5_key != "your_fifth_api_key_here":
    try:
        ai_tiers.append({
            "client": OpenRouterClient(tier5_key, tier5_model),
            "name": f"Tier 5 (OpenRouter - {tier5_model})",
            "tier": 5
        })
        logger.info(f"✓ Tier 5 initialized: {tier5_model}")
    except Exception as e:
        logger.error(f"✗ Tier 5 failed to initialize: {e}")

# Tier 6: Gemini Fallback
tier6_key = os.getenv("GEMINI_API_KEY_6") or API_KEY
if tier6_key:
    try:
        ai_tiers.append({
            "client": GeminiClient(tier6_key),
            "name": "Tier 6 (Gemini - High Reliability Fallback)",
            "tier": 6
        })
        logger.info(f"✓ Tier 6 initialized: Gemini")
    except Exception as e:
        logger.error(f"✗ Tier 6 failed to initialize: {e}")

# Tier 7: Seventh OpenRouter (Small Text Model)
tier7_key = os.getenv("OPENROUTER_API_KEY_7")
tier7_model = os.getenv("OPENROUTER_MODEL_7")
if tier7_key:
    try:
        ai_tiers.append({
            "client": OpenRouterClient(tier7_key, tier7_model),
            "name": f"Tier 7 (OpenRouter - {tier7_model})",
            "tier": 7
        })
        logger.info(f"✓ Tier 7 initialized: {tier7_model}")
    except Exception as e:
        logger.error(f"✗ Tier 7 failed to initialize: {e}")

# Tier 8: Groq (Llama 3.3 70B)
tier8_key = os.getenv("GROQ_API_KEY")
tier8_model = os.getenv("GROQ_MODEL")
if tier8_key:
    try:
        ai_tiers.append({
            "client": GroqClient(tier8_key, tier8_model),
            "name": f"Tier 8 (Groq - {tier8_model})",
            "tier": 8
        })
        logger.info(f"✓ Tier 8 initialized: {tier8_model}")
    except Exception as e:
        logger.error(f"✗ Tier 8 failed to initialize: {e}")

# Tier 9: GitHub Models (GPT-4o)
tier9_key = os.getenv("GITHUB_ACCESS_TOKEN")
if tier9_key:
    try:
        ai_tiers.append({
            "client": GitHubClient(tier9_key),
            "name": "Tier 9 (GitHub Models - GPT-4o)",
            "tier": 9
        })
        logger.info("✓ Tier 9 initialized: GitHub Models")
    except Exception as e:
        logger.error(f"✗ Tier 9 failed to initialize: {e}")

# Tier 10: Groq Secondary (Llama 3.3 70B)
tier10_key = os.getenv("GROQ_API_KEY_2")
tier10_model = os.getenv("GROQ_MODEL_2") or "llama-3.3-70b-versatile"
if tier10_key:
    try:
        ai_tiers.append({
            "client": GroqClient(tier10_key, tier10_model),
            "name": f"Tier 10 (Groq 2 - {tier10_model})",
            "tier": 10
        })
        logger.info(f"✓ Tier 10 initialized: {tier10_model}")
    except Exception as e:
        logger.error(f"✗ Tier 10 failed to initialize: {e}")

# Tier 11: CometAPI (GPT-4o)
comet_key = os.getenv("COMET_API_KEY")
if comet_key:
    try:
        ai_tiers.append({
            "client": CometClient(comet_key),
            "name": "Tier 11 (CometAPI - GPT-4o)",
            "tier": 11
        })
        logger.info("✓ Tier 11 initialized: CometAPI")
    except Exception as e:
        logger.error(f"✗ Tier 11 failed to initialize: {e}")

logger.info(f"Total AI tiers available: {len(ai_tiers)}")

# Keep legacy variables for backward compatibility
primary_ai = ai_tiers[0]["client"] if len(ai_tiers) > 0 else None
secondary_ai = ai_tiers[1]["client"] if len(ai_tiers) > 1 else None
third_ai = ai_tiers[2]["client"] if len(ai_tiers) > 2 else GeminiClient(API_KEY)

# Initialize Image Assistant
IMAGEN_API_KEY = os.getenv("IMAGEN_API_KEY")
IMAGEN_MODEL = os.getenv("IMAGEN_MODEL")
imagen_assistant = None

if IMAGEN_API_KEY:
    imagen_assistant = ImagenClient(IMAGEN_API_KEY, IMAGEN_MODEL)
    logger.info(f"Image generation enabled with model: {IMAGEN_MODEL}")

# Initialize Stability Assistant
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_MODEL = os.getenv("STABILITY_MODEL")
stability_assistant = None

if STABILITY_API_KEY:
    stability_assistant = StabilityClient(STABILITY_API_KEY, STABILITY_MODEL)
    logger.info(f"Stability AI enabled with model: {STABILITY_MODEL}")

# Initialize Kling AI Assistant (Primary Video)
KLING_ACCESS_KEY = os.getenv("KLING_ACCESS_KEY")
KLING_SECRET_KEY = os.getenv("KLING_SECRET_KEY")
kling_assistant = None

if KLING_ACCESS_KEY and KLING_SECRET_KEY:
    try:
        kling_assistant = KlingClient(KLING_ACCESS_KEY, KLING_SECRET_KEY)
        logger.info("✓ Kling AI Video enabled (Primary)")
    except Exception as e:
        logger.error(f"✗ Kling AI initialization failed: {e}")

# Initialize Kling AI Assistant Tier 2
KLING_ACCESS_KEY_2 = os.getenv("KLING_ACCESS_KEY_2")
KLING_SECRET_KEY_2 = os.getenv("KLING_SECRET_KEY_2")
kling_assistant_2 = None

if KLING_ACCESS_KEY_2 and KLING_SECRET_KEY_2:
    try:
        kling_assistant_2 = KlingClient(KLING_ACCESS_KEY_2, KLING_SECRET_KEY_2)
        logger.info("✓ Kling AI Video enabled (Tier 2)")
    except Exception as e:
        logger.error(f"✗ Kling AI Tier 2 initialization failed: {e}")

# Initialize Kling AI Assistant Tier 3
KLING_ACCESS_KEY_3 = os.getenv("KLING_ACCESS_KEY_3")
KLING_SECRET_KEY_3 = os.getenv("KLING_SECRET_KEY_3")
kling_assistant_3 = None

if KLING_ACCESS_KEY_3 and KLING_SECRET_KEY_3:
    try:
        kling_assistant_3 = KlingClient(KLING_ACCESS_KEY_3, KLING_SECRET_KEY_3)
        logger.info("✓ Kling AI Video enabled (Tier 3)")
    except Exception as e:
        logger.error(f"✗ Kling AI Tier 3 initialization failed: {e}")

# Initialize Kling AI Assistant Tier 4
KLING_ACCESS_KEY_4 = os.getenv("KLING_ACCESS_KEY_4")
KLING_SECRET_KEY_4 = os.getenv("KLING_SECRET_KEY_4")
kling_assistant_4 = None

if KLING_ACCESS_KEY_4 and KLING_SECRET_KEY_4:
    try:
        kling_assistant_4 = KlingClient(KLING_ACCESS_KEY_4, KLING_SECRET_KEY_4)
        logger.info("✓ Kling AI Video enabled (Tier 4)")
    except Exception as e:
        logger.error(f"✗ Kling AI Tier 4 initialization failed: {e}")
    except Exception as e:
        logger.error(f"✗ Kling AI Tier 4 initialization failed: {e}")

# Initialize GitHub Models Client (Tier 8)
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
github_assistant = None

if GITHUB_ACCESS_TOKEN:
    try:
        github_assistant = GitHubClient(GITHUB_ACCESS_TOKEN)
        logger.info("✓ GitHub Models enabled (Video Tier 8)")
    except Exception as e:
        logger.error(f"✗ GitHub Models initialization failed: {e}")

# Initialize Replicate Assistant (Primary Video)
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
REPLICATE_MODEL = os.getenv("REPLICATE_MODEL") or "minimax/video-01"
replicate_assistant = None

if REPLICATE_API_TOKEN:
    try:
        replicate_assistant = ReplicateClient(REPLICATE_API_TOKEN, REPLICATE_MODEL)
        logger.info(f"✓ Replicate Video enabled (Primary: {REPLICATE_MODEL})")
    except Exception as e:
        logger.error(f"✗ Replicate initialization failed: {e}")

# Initialize Replicate Assistant 2 (Secondary Video)
REPLICATE_API_TOKEN_2 = os.getenv("REPLICATE_API_TOKEN_2")
replicate_assistant_2 = None

if REPLICATE_API_TOKEN_2:
    try:
        replicate_assistant_2 = ReplicateClient(REPLICATE_API_TOKEN_2, REPLICATE_MODEL)
        logger.info(f"✓ Replicate Video enabled (Secondary: {REPLICATE_MODEL})")
    except Exception as e:
        logger.error(f"✗ Replicate 2 initialization failed: {e}")

# Initialize Replicate Assistant 3 (Tertiary Video)
REPLICATE_API_TOKEN_3 = os.getenv("REPLICATE_API_TOKEN_3")
replicate_assistant_3 = None

if REPLICATE_API_TOKEN_3:
    try:
        replicate_assistant_3 = ReplicateClient(REPLICATE_API_TOKEN_3, REPLICATE_MODEL)
        logger.info(f"✓ Replicate Video enabled (Tertiary: {REPLICATE_MODEL})")
    except Exception as e:
        logger.error(f"✗ Replicate 3 initialization failed: {e}")

# Initialize Replicate Assistant 4 (Quaternary Video)
REPLICATE_API_TOKEN_4 = os.getenv("REPLICATE_API_TOKEN_4")
replicate_assistant_4 = None

if REPLICATE_API_TOKEN_4:
    try:
        replicate_assistant_4 = ReplicateClient(REPLICATE_API_TOKEN_4, REPLICATE_MODEL)
        logger.info(f"✓ Replicate Video enabled (Quaternary: {REPLICATE_MODEL})")
    except Exception as e:
        logger.error(f"✗ Replicate 4 initialization failed: {e}")

# Initialize Runway Assistant
RUNWAYML_API_KEY = os.getenv("RUNWAYML_API_KEY")
runway_assistant = None

if RUNWAYML_API_KEY:
    runway_assistant = RunwayClient(RUNWAYML_API_KEY)
    logger.info("RunwayML Video AI enabled")

# Initialize Veo Assistants (Sequential Video Fallback)
VEO_API_KEY = os.getenv("VEO_API_KEY")
VEO_API_KEY_2 = os.getenv("VEO_API_KEY_2")
VEO_API_KEY_3 = os.getenv("VEO_API_KEY_3")
VEO_API_KEY_4 = os.getenv("VEO_API_KEY_4")
VEO_MODEL = os.getenv("VEO_MODEL") or "veo3"
veo_assistant = None
veo_assistant_2 = None
veo_assistant_3 = None
veo_assistant_4 = None

if VEO_API_KEY:
    veo_assistant = VeoClient(VEO_API_KEY, VEO_MODEL)
    logger.info(f"✓ Veo Tier 1 enabled: {VEO_MODEL}")

if VEO_API_KEY_2:
    veo_assistant_2 = VeoClient(VEO_API_KEY_2, VEO_MODEL)
    logger.info(f"✓ Veo Tier 2 enabled: {VEO_MODEL}")

if VEO_API_KEY_3:
    veo_assistant_3 = VeoClient(VEO_API_KEY_3, VEO_MODEL)
    logger.info(f"✓ Veo Tier 3 enabled: {VEO_MODEL}")

if VEO_API_KEY_4:
    veo_assistant_4 = VeoClient(VEO_API_KEY_4, VEO_MODEL)
    logger.info(f"✓ Veo Tier 4 enabled: {VEO_MODEL}")

# Initialize Freepik Assistants (Sequential Image Fallback)
FREEPIK_API_KEY = os.getenv("FREEPIK_API_KEY")
FREEPIK_API_KEY_2 = os.getenv("FREEPIK_API_KEY_2")
FREEPIK_API_KEY_3 = os.getenv("FREEPIK_API_KEY_3")
FREEPIK_API_KEY_4 = os.getenv("FREEPIK_API_KEY_4")
freepik_assistant = None
freepik_assistant_2 = None
freepik_assistant_3 = None
freepik_assistant_4 = None

if FREEPIK_API_KEY:
    freepik_assistant = FreepikClient(FREEPIK_API_KEY)
    logger.info("✓ Freepik Tier 1 enabled")

if FREEPIK_API_KEY_2:
    freepik_assistant_2 = FreepikClient(FREEPIK_API_KEY_2)
    logger.info("✓ Freepik Tier 2 enabled")

if FREEPIK_API_KEY_3:
    freepik_assistant_3 = FreepikClient(FREEPIK_API_KEY_3)
    logger.info("✓ Freepik Tier 3 enabled")

if FREEPIK_API_KEY_4:
    freepik_assistant_4 = FreepikClient(FREEPIK_API_KEY_4)
    logger.info("✓ Freepik Tier 4 enabled")

# Initialize Hugging Face Assistant
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
huggingface_assistant = None

if HUGGINGFACE_API_KEY:
    huggingface_assistant = HuggingFaceClient(HUGGINGFACE_API_KEY)
    logger.info("Hugging Face Image AI enabled")

@app.route('/')
def index():
    return render_template('index.html', google_client_id=GOOGLE_CLIENT_ID or "YOUR_GOOGLE_CLIENT_ID", razorpay_key_id=RAZORPAY_KEY_ID)


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'logo.jpg', mimetype='image/jpeg')

@app.route('/download/<platform>')
def download_app(platform):
    """
    Route to handle app downloads for different platforms.
    You can place your app files in static/downloads/ directory
    """
    # Map platforms to file names
    download_files = {
        'android': 'GlobleXGPT.apk',
        'ios': 'GlobleXGPT.ipa',
        'windows': 'GlobleXGPT-Windows-Setup.zip',
        'mac': 'GlobleXGPT.dmg',
        'linux': 'GlobleXGPT.AppImage',
        'web': 'manifest.json'  # For PWA installation
    }
    
    filename = download_files.get(platform)
    if not filename:
        return jsonify({"error": "Platform not supported"}), 404
    
    try:
        # Check if file exists in static/downloads directory
        downloads_dir = os.path.join(app.root_path, 'static', 'downloads')
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        file_path = os.path.join(downloads_dir, filename)
        if os.path.exists(file_path):
            return send_from_directory(downloads_dir, filename, as_attachment=True)
        else:
            # Return a message if file doesn't exist yet
            return jsonify({
                "message": f"Download for {platform} is not available yet. Please contact support.",
                "platform": platform
            }), 404
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({"error": "Download failed"}), 500


@app.route('/signup', methods=['POST'])
def signup():
    """Manual signup with local DB"""
    data = request.json
    email = (data.get('email') or "").strip().lower()
    password = data.get('password')
    full_name = data.get('full_name', '')
    avatar_url = data.get('avatar_url', '')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user, error = local_db.create_user(email, password, full_name, avatar_url)
    
    if user:
        # Sync registration to Google Sheets
        sheets_service.register_user(
            email=email,
            name=full_name or "User",
            registration_method="Email",
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        return jsonify({"message": "Sign up successful", "user": user}), 200
    else:
        return jsonify({"error": error}), 400

@app.route('/login', methods=['POST'])
def login():
    """Manual login with local DB"""
    data = request.json
    email = (data.get('email') or "").strip().lower()
    password = data.get('password')

    user, error = local_db.authenticate_user(email, password)
    
    if user:
        # Sync login
        pro_emails = sheets_service.get_pro_emails()
        is_pro = email in pro_emails
        plan_label = "Pro (Active)" if is_pro else "Free Member"
        
        sheets_service.sync_user(
            email=email,
            name=user.get('full_name', 'N/A'),
            password="LOCAL_HASHED",
            plan_type=f"Login - {plan_label}",
            amount="N/A",
            ip_address=request.remote_addr
        )

        return jsonify({
            "message": "Login successful",
            "access_token": "local_session_token", # In a real app we'd generate a JWT here
            "user": {
                "id": user['id'],
                "email": user['email'],
                "full_name": user['full_name'],
                "avatar_url": user['avatar_url']
            }
        }), 200
    else:
        return jsonify({"error": error or "Login failed"}), 401

@app.route('/auth/google', methods=['POST'])
def google_auth():
    print("Received Google Auth Request") # Debug
    data = request.json
    token = data.get('credential')
    
    if not token:
        print("Error: No credential token in request")
        return jsonify({"error": "No credential provided"}), 400

    try:
        # Debug: Print first few chars of token
        print(f"Verifying token: {token[:10]}...")
        
        # Create a session with retry logic to handle intermittent SSL/Connection errors
        session = requests.Session()
        retry_strategy = requests.adapters.HTTPAdapter(
            max_retries=3,
            pool_connections=10,
            pool_maxsize=10
        )
        session.mount("https://", retry_strategy)
        session.mount("http://", retry_strategy)
        
        request_adapter = google_requests.Request(session=session)
        
        # Verify the token
        try:
             id_info = id_token.verify_oauth2_token(token, request_adapter, GOOGLE_CLIENT_ID)
        except ValueError as e:
             # Common error: audience mismatch if setup is wrong
             print(f"Token Verification Failed: {e}")
             return jsonify({"error": f"Invalid token: {str(e)}"}), 401
             
        print("Token verified successfully")
        user_id = id_info['sub']
        email = id_info['email'].lower()
        full_name = id_info.get('name', '')
        avatar_url = id_info.get('picture', '')
        
        print(f"User: {email}")
        
        # Save or update user in local database
        local_user, db_error = local_db.get_or_create_google_user(email, full_name, avatar_url)
        if db_error:
            logger.error(f"Local DB Error during Google Auth: {db_error}")

        # Determine current plan status for consistent sheet record
        pro_emails = sheets_service.get_pro_emails()
        # Use local_user's plan type if available, otherwise check sheets
        is_pro = (local_user and 'Pro' in local_user.get('plan_type', 'Free')) or (email in pro_emails)
        plan_label = "Pro (Active)" if is_pro else "Free Member"
        
        # Sync login activity to Google Sheets
        sheets_service.sync_user(
            email=email,
            name=full_name or "N/A",
            password="GOOGLE_OAUTH", # No password for Google Auth
            plan_type=f"Login - {plan_label}",
            amount="N/A",
            ip_address=request.remote_addr
        )

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": local_user['id'] if local_user else user_id,
                "email": email,
                "full_name": full_name,
                "avatar_url": avatar_url,
                "plan_type": local_user['plan_type'] if local_user else "Free"
            },
            "token": token
        }), 200

    except Exception as e:
        print(f"Login Error (General): {e}")
        logger.error(f"Login Error: {e}")
        return jsonify({"error": str(e)}), 500

# --- GitHub Auth ---
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

@app.route('/auth/github/login')
def github_login():
    # Explicitly define the redirect_uri to match GitHub App settings
    redirect_uri = "http://localhost:5000/api/auth/github/callback"
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&scope=user:email"
        f"&redirect_uri={redirect_uri}"
    )
    return redirect(github_auth_url)

@app.route('/api/auth/github/callback', strict_slashes=False) # Matches GitHub App setting
@app.route('/auth/github/callback', strict_slashes=False)
@app.route('/auth/callback', strict_slashes=False)
@app.route('/callback', strict_slashes=False)
def github_callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code provided", 400

    # Exchange code for access token
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code
    }
    headers = {"Accept": "application/json"}
    
    try:
        resp = requests.post(token_url, json=payload, headers=headers)
        data = resp.json()
        access_token = data.get("access_token")
        
        if not access_token:
             return f"Error: Failed to retrieve access token. {data}", 400
             
        # Fetch User Info
        user_resp = requests.get("https://api.github.com/user", headers={
            "Authorization": f"token {access_token}"
        })
        user_data = user_resp.json()
        
        # Fetch Email (if primary is private)
        email_resp = requests.get("https://api.github.com/user/emails", headers={
            "Authorization": f"token {access_token}"
        })
        emails = email_resp.json()
        
        primary_email = None
        for e in emails:
            if isinstance(e, dict) and e.get("primary") and e.get("verified"):
                primary_email = e.get("email")
                break
        if not primary_email and emails and isinstance(emails[0], dict):
             primary_email = emails[0].get("email") # Fallback
             
        email = (primary_email or f"{user_data.get('login')}@github.placeholder").lower()
        full_name = user_data.get('name') or user_data.get('login')
        avatar_url = user_data.get('avatar_url', '')
        user_id = str(user_data.get('id'))
        
        # Sync to Sheets
        pro_emails = sheets_service.get_pro_emails()
        is_pro = email in pro_emails
        plan_label = "Pro (Active)" if is_pro else "Free Member"
        
        sheets_service.sync_user(
            email=email,
            name=full_name,
            password="GITHUB_OAUTH",
            plan_type=f"Login - {plan_label}",
            amount="N/A",
            ip_address=request.remote_addr
        )
        
        # Render a self-closing script to pass data to frontend
        user_obj_json = json.dumps({
            "id": user_id,
            "email": email,
            "full_name": full_name,
            "avatar_url": avatar_url
        })
        
        html = f"""
        <html>
        <body>
            <p>Login successful! Redirecting...</p>
            <script>
                localStorage.setItem('user', JSON.stringify({user_obj_json}));
                localStorage.setItem('access_token', '{access_token}');
                window.location.href = '/';
            </script>
        </body>
        </html>
        """
        return html

    except Exception as e:
        logger.error(f"GitHub Auth Error: {e}")
        return f"GitHub Login Error: {e}", 500

# Global Promo Code Storage (In-memory for simplicity, can be DB-backed)
ACTIVE_PROMO_CODE = "HimanshuFree"
ADMIN_SECRET_CODE = "Abinav_9009" # Should match frontend secret

@app.route('/verify_promo', methods=['POST'])
def verify_promo():
    data = request.json
    code = data.get('code', '').strip()
    email = data.get('email')
    
    if not code or not email:
        return jsonify({"error": "Missing code or email"}), 400
        
    if code != ACTIVE_PROMO_CODE:
        return jsonify({"error": "Invalid promo code"}), 400
        
    # Apply upgrade
    success, error = local_db.upgrade_user_to_pro(email, 'Pro (Promo)', 30)
    
    if success:
        # Sync to Google Sheets with promo code details
        try:
            user = local_db.get_user_by_email(email)
            user_name = user.get('full_name', 'Unknown') if user else 'Unknown'
            
            sheets_service.log_promo_upgrade(
                email=email,
                name=user_name,
                promo_code=code,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )
            logger.info(f"✓ Promo upgrade synced to Google Sheets for {email}")
        except Exception as e:
            logger.error(f"✗ Failed to sync promo upgrade: {e}")
        
        return jsonify({"message": "Promo code applied successfully!", "success": True}), 200
    else:
        return jsonify({"error": f"Upgrade failed: {error}"}), 500

@app.route('/admin/update_promo', methods=['POST'])
def admin_update_promo():
    global ACTIVE_PROMO_CODE
    data = request.json
    secret = data.get('secret')
    new_code = data.get('new_code')
    
    if secret != ADMIN_SECRET_CODE:
        return jsonify({"error": "Invalid secret code"}), 403
        
    if not new_code or len(new_code) < 3:
        return jsonify({"error": "Invalid new promo code"}), 400
        
    ACTIVE_PROMO_CODE = new_code
    return jsonify({"message": f"Promo code updated to: {new_code}", "success": True}), 200

# ═══════════════════════════════════════════════════════════════════════════
# 💳 RAZORPAY PAYMENT ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/create_payment_order', methods=['POST'])
def create_payment_order():
    """Create a Razorpay payment order for PRO plan purchase."""
    if not razorpay_client:
        return jsonify({"error": "Payment gateway not configured"}), 500
    
    try:
        data = request.json
        email = data.get('email', '').strip().lower()
        name = data.get('name', 'User')
        amount = data.get('amount', 49900)  # Default: ₹499 in paise
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        # Create Razorpay order
        receipt_id = f"rcpt_{int(datetime.now().timestamp())}"
        logger.info(f"Creating Razorpay order for {email}, amount: {amount}, receipt: {receipt_id}")
        
        order_data = {
            "amount": amount,  # Amount in paise (₹499 = 49900 paise)
            "currency": "INR",
            "receipt": receipt_id,
            "notes": {
                "email": email,
                "name": name,
                "plan": "PRO",
                "validity": "30 days"
            }
        }
        
        order = razorpay_client.order.create(data=order_data)
        
        logger.info(f"✓ Payment order created for {email}: {order['id']}")
        
        return jsonify({
            "success": True,
            "order_id": order['id'],
            "amount": order['amount'],
            "currency": order['currency'],
            "key_id": RAZORPAY_KEY_ID
        }), 200
        
    except Exception as e:
        logger.error(f"✗ Payment order creation failed: {e}")
        return jsonify({"error": f"Failed to create payment order: {str(e)}"}), 500

@app.route('/verify_payment', methods=['POST'])
def verify_payment():
    """
    Verify Razorpay payment signature and automatically upgrade user to PRO.
    After successful verification:
    1. Validates payment signature
    2. Upgrades user to PRO in local database (30 days)
    3. Syncs to Google Sheets with payment details
    4. Returns PRO status immediately
    """
    if not razorpay_client:
        return jsonify({"error": "Payment gateway not configured"}), 500
    
    try:
        data = request.json
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        email = data.get('email', '').strip().lower()
        name = data.get('name', 'User')
        amount = data.get('amount', 499)  # Amount in rupees
        
        if not all([payment_id, order_id, signature, email]):
            return jsonify({"error": "Missing required payment details"}), 400
        
        # ═══════════════════════════════════════════════════════════════════
        # STEP 1: Verify Payment Signature
        # ═══════════════════════════════════════════════════════════════════
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try:
            # Verify signature using Razorpay SDK
            razorpay_client.utility.verify_payment_signature(params_dict)
            logger.info(f"✓ Payment signature verified for {email}")
        except Exception as verify_error:
            logger.error(f"✗ Payment signature verification failed: {verify_error}")
            return jsonify({
                "error": "Payment verification failed. Invalid signature.",
                "success": False
            }), 400
        
        # ═══════════════════════════════════════════════════════════════════
        # STEP 2: Upgrade User to PRO in Local Database
        # ═══════════════════════════════════════════════════════════════════
        activation_date = datetime.now()
        expiry_date = activation_date + timedelta(days=30)
        
        success, error = local_db.upgrade_user_to_pro(
            email=email,
            plan_type='Pro (Razorpay)',
            validity_days=30
        )
        
        if not success:
            logger.error(f"✗ Failed to upgrade user {email}: {error}")
            # Continue anyway - payment was successful, we'll retry upgrade
        else:
            logger.info(f"✓ User {email} upgraded to PRO (30 days)")
        
        # ═══════════════════════════════════════════════════════════════════
        # STEP 3: Sync to Google Sheets with Complete Payment Details
        # ═══════════════════════════════════════════════════════════════════
        try:
            # Get payment method details from Razorpay
            payment_details = data.get('payment_details', 'Credit/Debit Card')
            
            sheets_service.log_payment_success(
                email=email,
                name=name,
                phone=data.get('phone', ''),
                payment_method="Razorpay",
                payment_details=payment_details,
                amount=str(amount),
                transaction_id=payment_id,
                razorpay_order_id=order_id,
                razorpay_payment_id=payment_id,
                promo_code="N/A",
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )
            logger.info(f"✓ Payment synced to Google Sheets for {email}")
        except Exception as sheets_error:
            logger.error(f"✗ Failed to sync to Google Sheets: {sheets_error}")
            # Continue - user is already upgraded locally
        
        # ═══════════════════════════════════════════════════════════════════
        # STEP 4: Return Success with PRO Status
        # ═══════════════════════════════════════════════════════════════════
        return jsonify({
            "success": True,
            "message": "Payment successful! You are now a PRO member.",
            "is_pro": True,
            "plan_type": "Pro (Razorpay)",
            "activation_date": activation_date.strftime('%Y-%m-%d'),
            "expiry_date": expiry_date.strftime('%Y-%m-%d'),
            "days_remaining": 30,
            "payment_id": payment_id,
            "order_id": order_id,
            "amount": amount
        }), 200
        
    except Exception as e:
        logger.error(f"✗ Payment verification error: {e}")
        return jsonify({
            "error": f"Payment verification failed: {str(e)}",
            "success": False
        }), 500

@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Update user profile in local DB and sync with sheets."""
    data = request.json
    user_id = data.get('user_id')
    email = data.get('email') # Should ideally be verified via token
    full_name = data.get('full_name')
    avatar_url = data.get('avatar_url')

    if not user_id and not email:
        return jsonify({"error": "User identifier required"}), 400

    updates = {}
    if full_name: updates['full_name'] = full_name
    if avatar_url: updates['avatar_url'] = avatar_url

    if not updates:
        return jsonify({"message": "No changes provided"}), 200

    # 1. Update Local DB
    success = False
    error = None
    
    if user_id:
        success, error = local_db.update_user_profile(user_id, updates)
    
    # Fallback to email if user_id failed or wasn't provided
    if (not success or not user_id) and email:
        user = local_db.get_user_by_email(email)
        if user:
            success, error = local_db.update_user_profile(user['id'], updates)
        elif not user_id: # Only report error if we didn't try user_id or both failed
            return jsonify({"error": "User not found"}), 404

    if not success:
        return jsonify({"error": error or "Update failed"}), 500

    # 2. Sync to Sheets if email is available
    if not email and user_id:
        # We need the email to sync with sheets
        # In this app, the user object usually has it
        pass 

    return jsonify({"message": "Profile updated successfully", "success": True}), 200

@app.route('/check_pro_status', methods=['POST'])
def check_pro_status():
    """
    Checks if a user has PRO status in both local database and Google Sheets.
    """
    data = request.json
    email = (data.get('email') or "").strip().lower()
    
    if not email:
        return jsonify({"is_pro": False}), 200
        
    # 1. Check Local Database (Razorpay/Promo upgrades)
    user_data = local_db.get_user_by_email(email)
    if user_data and 'Pro' in user_data.get('plan_type', 'Free'):
        return jsonify({"is_pro": True, "source": "local"}), 200
        
    # 2. Check Google Sheets (Admin/Manual sheet upgrades)
    try:
        pro_emails = sheets_service.get_pro_emails()
        if email in pro_emails:
            return jsonify({"is_pro": True, "source": "sheets"}), 200
    except Exception as e:
        logger.error(f"Error checking sheets for pro status: {e}")
    
    return jsonify({"is_pro": False}), 200

@app.route('/video_status', methods=['GET'])
def video_status():
    """Diagnostic endpoint to check video AI configuration."""
    status = {
        "Replicate_Primary": "Enabled" if replicate_assistant else "Disabled",
        "Replicate_Secondary": "Enabled" if replicate_assistant_2 else "Disabled",
        "Replicate_Tertiary": "Enabled" if replicate_assistant_3 else "Disabled",
        "Replicate_Quaternary": "Enabled" if replicate_assistant_4 else "Disabled",
        "Kling_AI": "Enabled" if kling_assistant else "Disabled",
        "Kling_AI_Tier_2": "Enabled" if kling_assistant_2 else "Disabled",
        "Kling_AI_Tier_3": "Enabled" if kling_assistant_3 else "Disabled",
        "Kling_AI_Tier_4": "Enabled" if kling_assistant_4 else "Disabled",
        "Veo_Tier_1": "Enabled" if veo_assistant else "Disabled",
        "Veo_Tier_2": "Enabled" if veo_assistant_2 else "Disabled",
        "Veo_Tier_3": "Enabled" if veo_assistant_3 else "Disabled",
        "Veo_Tier_4": "Enabled" if veo_assistant_4 else "Disabled",
        "RunwayML": "Enabled" if runway_assistant else "Disabled",
        "GitHub_Models": "Enabled" if github_assistant else "Disabled",
        "HuggingFace": "Enabled" if huggingface_assistant else "Disabled",
        "VEO_MODEL": VEO_MODEL,
        "Is_PRO_Request": "N/A"
    }
    return jsonify(status), 200

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    user_input = data.get('prompt', '')
    if user_input is None:
        user_input = ''
    
    logger.info(f"Incoming /ask request: prompt='{user_input}', email='{data.get('email')}'")

    # Safe extraction of email and prompt
    user_email_data = data.get('email')
    if user_email_data is None:
        email = 'guest'
    else:
        email = str(user_email_data).strip().lower()
    
    is_pro = False
    current_images, current_videos = 0, 0
    
    try:
        pro_emails = sheets_service.get_pro_emails() or []
        db_user = local_db.get_user_by_email(email)
        is_pro = email in pro_emails or (db_user and db_user.get('plan_type') == 'Pro')
        
        current_images, current_videos = local_db.get_usage(email)
    except Exception as usage_err:
        logger.error(f"Error checking pro/usage status: {usage_err}")
        # Default to safe values if DB/Sheets fail
        is_pro = False 
        current_images, current_videos = 0, 0
    
    # Check for system commands first (conceptual)
    if "screenshot" in user_input.lower():
        system.take_screenshot()
        return jsonify({"response": emoji_service.augment_text_with_emojis("Screenshot taken successfully.", "Neutral"), "emotion": "Neutral"})
    elif "camera" in user_input.lower() or "photo" in user_input.lower():
        system.capture_camera()
        return jsonify({"response": emoji_service.augment_text_with_emojis("Camera image captured.", "Neutral"), "emotion": "Neutral"})
    elif "open" in user_input.lower():
        app_name = user_input.lower().split("open")[-1].strip()
        response_text = system.open_app(app_name)
        return jsonify({"response": emoji_service.augment_text_with_emojis(response_text, "Neutral"), "emotion": "Neutral"})
    elif "weather" in user_input.lower():
        # Try to extract city name
        words = user_input.lower().split()
        city = "London" # Default
        if "in" in words:
            try:
                city = user_input.lower().split("in")[-1].strip().strip('?').strip('.')
            except:
                pass
        elif "for" in words:
            try:
                city = user_input.lower().split("for")[-1].strip().strip('?').strip('.')
            except:
                pass
        
        weather_info = weather.get_weather(city)
        return jsonify({"response": emoji_service.augment_text_with_emojis(weather_info, "Neutral"), "emotion": "Neutral"})
    elif "news" in user_input.lower():
        news_info = news.get_top_news()
        return jsonify({"response": emoji_service.augment_text_with_emojis(news_info, "Neutral"), "emotion": "Neutral"})
    elif "price of" in user_input.lower() or "price for" in user_input.lower():
        # Try to extract crypto symbol
        words = user_input.lower().split()
        symbol = None
        if "of" in words:
            symbol = words[words.index("of") + 1].strip("?").strip(".")
        elif "for" in words:
            symbol = words[words.index("for") + 1].strip("?").strip(".")
        
        if symbol:
            # Map common names to symbols
            mapping = {"bitcoin": "BTC", "ethereum": "ETH", "solana": "SOL", "dogecoin": "DOGE", "cardano": "ADA"}
            symbol = mapping.get(symbol, symbol)
            
            crypto_info = crypto.get_price(symbol)
            return jsonify({"response": emoji_service.augment_text_with_emojis(crypto_info, "Neutral"), "emotion": "Neutral"})
    elif "crypto" in user_input.lower() or "cryptocurrency" in user_input.lower():
         top_cryptos = crypto.get_top_cryptos()
         return jsonify({"response": emoji_service.augment_text_with_emojis(top_cryptos, "Neutral"), "emotion": "Neutral"})
    elif "stock" in user_input.lower() or "share price" in user_input.lower():
        # Try to extract stock symbol
        words = user_input.lower().split()
        symbol = None
        if "of" in words:
            symbol = words[words.index("of") + 1].strip("?").strip(".")
        elif "for" in words:
            symbol = words[words.index("for") + 1].strip("?").strip(".")
        
        if symbol:
            stock_info = stock.get_stock_price(symbol)
            return jsonify({"response": emoji_service.augment_text_with_emojis(stock_info, "Neutral"), "emotion": "Neutral"})
        else:
            news_info = stock.get_market_news()
            return jsonify({"response": emoji_service.augment_text_with_emojis(news_info, "Neutral"), "emotion": "Neutral"})
    
    elif "youtube" in user_input.lower():
        if "trending" in user_input.lower() or "popular" in user_input.lower():
            trending = youtube.get_trending_videos()
            return jsonify({"response": emoji_service.augment_text_with_emojis(trending, "Happy"), "emotion": "Happy"})
        
        # Extract search query
        query = user_input.lower().replace("youtube", "").replace("search", "").replace("find", "").strip()
        if not query:
            return jsonify({"response": emoji_service.augment_text_with_emojis("What would you like to search for on YouTube?", "Neutral"), "emotion": "Neutral"})
        
        results = youtube.search_videos(query)
        return jsonify({"response": emoji_service.augment_text_with_emojis(results, "Happy"), "emotion": "Happy"})
    
    # Image Generation (Consolidated & Fuzzy Detection)
    # This block catches variations including typos like "genrate", "enrate", "genrrate"
    elif (any(trig in user_input.lower() for trig in ["generate", "create", "make", "paint", "draw", "render", "show me", "genrate", "enrate", "genrrate", "generrate"]) or \
         (any(img_kw in user_input.lower() for img_kw in ["image", "picture", "photo", "art", "illustration", "sketch", "painting"]) and \
          any(action in user_input.lower() for action in ["me", "give", "want", "need", "car", "girl", "boy", "person", "scene"]))) and \
         any(img_kw in user_input.lower() for img_kw in ["image", "picture", "photo", "art", "illustration", "portrait", "landscape", "sketch", "drawing", "painting", "wallpaper", "avatar", "masterpiece", "cyber"]):
        
        # Sequential Image Fallback System (All Tiers)
        image_assistants = [
            ("Freepik Tier 1", freepik_assistant),
            ("Freepik Tier 2", freepik_assistant_2),
            ("Freepik Tier 3", freepik_assistant_3),
            ("Freepik Tier 4", freepik_assistant_4),
            ("Hugging Face", huggingface_assistant),
            ("Stability AI", stability_assistant),
            ("Imagen", imagen_assistant)
        ]
        
        # Extract prompt using word boundaries
        import re
        prompt = user_input.lower()
        # Expanded keywords for cleaning, including typos
        keywords = ["generate", "create", "make", "paint", "draw", "render", "show", "me", "an", "a", "of", "image", "picture", "photo", "art", "illustration", "portrait", "landscape", "sketch", "drawing", "painting", "wallpaper", "avatar", "enrate", "genrate", "genrrate", "generrate"]
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
        prompt = re.sub(pattern, '', prompt).strip()
        
        logger.info(f"🎨 Cleaned Image Prompt: '{prompt}' for user {email}")

        if not prompt:
             return jsonify({"response": "Please provide a description for the image.", "emotion": "Neutral"})
        
        # Check usage limit
        if not is_pro and current_images >= FREE_IMAGE_LIMIT:
             return jsonify({
                 "response": f"Daily limit reached! Free users can only generate {FREE_IMAGE_LIMIT} images per day. Upgrade to PRO for unlimited generations!",
                 "emotion": "Neutral"
             })
        
        for name, assistant in image_assistants:
            if assistant:
                try:
                    logger.info(f"🔄 Attempting image generation with {name}...")
                    image_data = assistant.generate_image(prompt)
                    if image_data:
                        logger.info(f"✓ Image generated with {name}!")
                        local_db.increment_usage(email, 'image')
                        return jsonify({
                            "response": f"I've generated that image for you! ![Generated Image]({image_data})",
                            "emotion": "Happy",
                            "image_data": image_data
                        })
                except Exception as e:
                    logger.error(f"✗ {name} failure: {e}")
        
        return jsonify({"response": "I'm sorry, I couldn't generate that image with any of my available services. Please try a different description.", "emotion": "Sad"})
    
    # Video Generation (Consolidated & Fuzzy Detection)
    elif (any(trig in user_input.lower() for trig in ["generate", "create", "make", "animate", "render", "show me", "genrate", "enrate", "genrrate", "generrate"]) or \
         (any(vid_kw in user_input.lower() for vid_kw in ["video", "clip", "movie", "animation", "motion"]) and \
          any(action in user_input.lower() for action in ["me", "give", "want", "need", "animate"]))) and \
         any(vid_kw in user_input.lower() for vid_kw in ["video", "clip", "movie", "animate", "animation", "motion", "clip"]):
        
        video_assistants = [
            ("Replicate Primary", replicate_assistant),
            ("Replicate Secondary", replicate_assistant_2),
            ("Replicate Tertiary", replicate_assistant_3),
            ("Replicate Quaternary", replicate_assistant_4),
            ("Kling AI", kling_assistant),
            ("Kling AI Tier 2", kling_assistant_2),
            ("Kling AI Tier 3", kling_assistant_3),
            ("Kling AI Tier 4", kling_assistant_4),
            ("RunwayML", runway_assistant),
            ("Veo Tier 1", veo_assistant),
            ("Veo Tier 2", veo_assistant_2),
            ("Veo Tier 3", veo_assistant_3),
            ("Veo Tier 4", veo_assistant_4),
            ("GitHub Models", github_assistant),
            ("Hugging Face", huggingface_assistant)
        ]
        
        # Extract prompt using word boundaries
        import re
        prompt = user_input.lower()
        # Expanded keywords for cleaning, including typos
        keywords = ["generate", "create", "make", "animate", "render", "show", "me", "a", "an", "of", "video", "clip", "movie", "animation", "motion", "enrate", "genrate", "genrrate", "generrate"]
        pattern = r'\b(' + '|'.join(keywords) + r')\b'
        prompt = re.sub(pattern, '', prompt).strip()
        
        if not prompt:
            prompt = "Animate this image" if data.get('file') else "A cinematic scene"
            
        file_data = data.get('file')
        image_url = None
        if file_data and file_data.get('type', '').startswith('image/'):
            image_url = file_data.get('data')
        
        # Check usage limit
        if not is_pro and current_videos >= FREE_VIDEO_LIMIT:
             return jsonify({
                 "response": f"Daily limit reached! Free users can only generate {FREE_VIDEO_LIMIT} video per day. Upgrade to PRO for unlimited generations!",
                 "emotion": "Neutral"
             })

        errors = []
        for name, assistant in video_assistants:
            if assistant:
                try:
                    logger.info(f"🔄 Attempting video generation with {name} for prompt: {prompt}")
                    video_url = assistant.generate_video(prompt, image_url=image_url)
                    if video_url:
                        logger.info(f"✓ Video generated with {name}!")
                        local_db.increment_usage(email, 'video')
                        return jsonify({
                            "response": f"I've generated that video for you! \n\n<video controls width='100%' style='border-radius:10px; margin-top:10px;'><source src='{video_url}' type='video/mp4'>Your browser does not support the video tag.</video>",
                            "emotion": "Happy",
                            "video_url": video_url
                        })
                    else:
                        errors.append(f"{name}: Returned no URL")
                        logger.warning(f"⚠️ {name} returned None (no video URL)")
                except Exception as e:
                    import traceback
                    error_trace = traceback.format_exc()
                    # Capture the actual error message
                    error_msg_short = str(e).split('\n')[0]
                    errors.append(f"{name}: {error_msg_short}")
                    logger.error(f"✗ {name} failure: {e}")
        
        # Video Idea Generator
        video_ideas = [
            "A futuristic city with flying neon cars and rain-soaked streets",
            "A majestic dragon flying over a snow-capped mountain range",
            "A tiny robot exploring a giant kitchen, looking curious",
            "A peaceful underwater coral reef with glowing jellyfish",
            "A cinematic sunrise over a calm forest lake with morning mist"
        ]
        import random
        suggested_idea = random.choice(video_ideas)

        # Enhanced error message with troubleshooting info
        error_msg = (
            "I'm sorry, I couldn't generate that video. All available services returned an error.\n\n"
            "🔍 **Diagnostics:**\n"
            + "\n".join([f"• {err}" for err in errors[:10]]) + "\n\n"
            "💡 **Video Idea for you:**\n"
            f"Try this prompt: *\"{suggested_idea}\"* - it's designed to work well with video AI!\n\n"
            "🛠️ **Troubleshooting:**\n"
            "• Check if your API keys in .env are valid\n"
            "• Ensure you haven't run out of credits on Veo/Runway\n"
            "• Simplify your prompt for better success rate\n\n"
        )
        
        if not is_pro:
            error_msg += "⭐ **PRO Users** get priority access and higher reliability. Upgrade now to unlock premium video AI!"
        
        logger.error(f"❌ All video services failed for prompt: {prompt}")
        return jsonify({"response": error_msg, "emotion": "Sad"})
    
    # Web Search Capability (Fuzzy Trigger)
    search_keywords = ["search", "find", "who is", "what is", "about", "latest", "news", "price", "stock", "weather"]
    if any(kw in user_input.lower() for kw in search_keywords) and len(user_input.split()) < 20: 
        # Only search if it looks like a lookup, not a long conversation
        # We can also explicitly check for "search" or "look up"
        if "search" in user_input.lower() or "look up" in user_input.lower() or "find information" in user_input.lower():
             logger.info(f"🌐 Triggering Web Search for: {user_input}")
             search_results = search_client.search(user_input)
             user_input = f"{user_input}\n\n[CONTEXT FROM WEB SEARCH]:\n{search_results}"



    # Get combined response and emotion with 7-tier fallback logic
    file_data = data.get('file')
    result = None
    error_keywords = ["API Error", "trouble connecting to my brain", "I'm sorry, I couldn't get a response", "Rate Limit", "429"]
    
    # Try each AI tier in sequence
    for tier_info in ai_tiers:
        tier_num = tier_info["tier"]
        tier_name = tier_info["name"]
        tier_client = tier_info["client"]
        
        try:
            logger.info(f"🔄 Attempting {tier_name}...")
            result = tier_client.get_full_response(user_input, file_data=file_data)
            
            # Check if the response contains error indicators
            if result and not any(kw in result.get("response", "") for kw in error_keywords):
                logger.info(f"✓ {tier_name} succeeded!")
                break  # Success! Exit the loop
            else:
                logger.warning(f"⚠ {tier_name} returned an error response. Trying next tier...")
                result = None
                
        except Exception as e:
            logger.error(f"✗ {tier_name} critical failure: {e}")
            result = None
    
    # If all tiers failed, return a helpful error message
    if not result:
        logger.error("❌ All AI tiers failed!")
        result = {
            "response": "I am unable to fulfill that request right now. Please try again in a few moments.",
            "emotion": "Neutral"
        }
    
    # Safety Check: If response is a raw JSON string (due to model behavior), clean it
    raw_response = result.get("response", "")
    
    # Aggressive cleaning for nested JSON or prefixed responses
    if isinstance(raw_response, str):
        raw_response = raw_response.strip()
        
        # 1. Check for standard JSON structures first
        if raw_response.startswith("{") and '"' in raw_response:
            try:
                import json
                # Handle cases where the whole string is JSON
                cleaned_data = json.loads(raw_response)
                if isinstance(cleaned_data, dict):
                    if "final" in cleaned_data:
                        inner = cleaned_data["final"]
                        if isinstance(inner, dict):
                            raw_response = inner.get("response", str(inner))
                        else:
                            raw_response = str(inner)
                    elif "response" in cleaned_data:
                        raw_response = cleaned_data.get("response", raw_response)
            except:
                pass
        
        # 2. Aggressive regex-based stripping of common failure patterns
        import re
        
        # Strip prefixes
        raw_response = re.sub(r'^\{"final":\s*\{"response":\s*"', '', raw_response)
        raw_response = re.sub(r'^\{"response":\s*"', '', raw_response)
        
        # Strip trailing JSON garbage (handles the user's specific technical leak)
        # Matches patterns like: " , "emotion": "Happy" }} or " \n, "emotion": "Neutral" }}
        # The user's specific case: ""\n","emotion":"Neutral"}}
        raw_response = re.sub(r'"?\s*\n?,?\s*"emotion":\s*"[^"]*"\s*\}*$', '', raw_response)
        
        # Final cleanup: if we're left with a trailing quote and bracket, remove them
        raw_response = re.sub(r'"\s*\}*$', '', raw_response)
        
        # Additional cleanup for escaped characters if they were left raw
        raw_response = raw_response.replace('\\n', '\n').replace('\\"', '"')
        
        raw_response = raw_response.strip()
    
    # Supplement response with emojis from emoji-api.com
    final_response = emoji_service.augment_text_with_emojis(raw_response, result.get("emotion", "Neutral"))
    
    return jsonify({
        "response": final_response,
        "emotion": result.get("emotion", "Neutral")
    })

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    """
    Handle payment submission - collects user details and payment screenshot,
    then sends an email notification to heyhkhimanshu@gmail.com
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip().lower()
        screenshot = data.get('screenshot', '')
        amount = data.get('amount', '₹90')
        timestamp = data.get('timestamp', '')
        
        # Validation
        if not name or not phone or not email:
            return jsonify({"error": "Missing required fields"}), 400
        
        if not screenshot:
            return jsonify({"error": "Payment screenshot is required"}), 400
        
        # Email validation
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Send email notification
        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
            import base64
            from datetime import datetime
            
            # Email configuration
            sender_email = os.getenv("SMTP_EMAIL", "noreply@globleXgpt.com")
            sender_password = os.getenv("SMTP_PASSWORD", "")
            receiver_email = "heyhkhimanshu@gmail.com"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"🎉 New Pro Plan Payment - {name}"
            
            # Email body
            body = f"""
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
        <h2 style="color: #FFD700; text-align: center;">💰 New Pro Plan Payment Received!</h2>
        
        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #333; border-bottom: 2px solid #FFD700; padding-bottom: 10px;">Customer Details</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px; font-weight: bold; width: 150px;">Name:</td>
                    <td style="padding: 10px;">{name}</td>
                </tr>
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 10px; font-weight: bold;">Email:</td>
                    <td style="padding: 10px;">{email}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Phone:</td>
                    <td style="padding: 10px;">{phone}</td>
                </tr>
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 10px; font-weight: bold;">Amount:</td>
                    <td style="padding: 10px; color: #FFD700; font-size: 18px; font-weight: bold;">{amount}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Submitted:</td>
                    <td style="padding: 10px;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                </tr>
            </table>
        </div>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #FFD700; margin: 20px 0;">
            <p style="margin: 0; font-size: 14px;">
                <strong>📸 Payment Screenshot:</strong> Attached to this email
            </p>
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;">
            <p style="color: #666; font-size: 12px;">
                This is an automated notification from GlobleXGPT Pro Plan System
            </p>
        </div>
    </div>
</body>
</html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Attach screenshot
            try:
                # Extract base64 data from data URL
                if ',' in screenshot:
                    screenshot_data = screenshot.split(',')[1]
                else:
                    screenshot_data = screenshot
                
                # Decode base64
                image_data = base64.b64decode(screenshot_data)
                
                # Create attachment
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(image_data)
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename=payment_screenshot_{name.replace(" ", "_")}.png')
                msg.attach(attachment)
            except Exception as e:
                logger.error(f"Error attaching screenshot: {e}")
            
            # Send email
            if sender_password:
                try:
                    # Try Gmail SMTP
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(msg)
                    server.quit()
                    logger.info(f"Payment notification email sent successfully to {receiver_email}")
                except Exception as smtp_error:
                    logger.error(f"SMTP error: {smtp_error}")
                    # If email fails, still log the payment details
                    logger.info(f"Payment Details (Email Failed): Name={name}, Email={email}, Phone={phone}, Amount={amount}")
            else:
                # Log payment details if SMTP not configured
                logger.info(f"Payment Details (No SMTP): Name={name}, Email={email}, Phone={phone}, Amount={amount}")
                logger.warning("SMTP not configured. Payment details logged only.")
        
        except Exception as email_error:
            logger.error(f"Email sending error: {email_error}")
            # Continue even if email fails - we'll log the details
        
        # Log payment submission
        logger.info(f"Payment submission received: {name} ({email}) - {amount}")
        
        sheets_service.sync_user(
            email=email,
            name=name,
            phone=phone,
            amount=amount,
            plan_type="Pro (Payment)",
            expiry_date=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            ip_address=request.remote_addr
        )

        # Store in database if Supabase is configured
        if supabase:
            try:
                supabase.table('payment_submissions').insert({
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "amount": amount,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }).execute()
                logger.info("Payment stored in Supabase")
            except Exception as db_error:
                logger.error(f"Supabase storage error: {db_error}")

        return jsonify({
            "success": True,
            "message": "Payment details submitted successfully! We will verify and upgrade your account soon."
        }), 200
        
    except Exception as e:
        logger.error(f"Submit payment error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/admin_upgrade_user', methods=['POST'])
def admin_upgrade_user():
    """
    Secure admin route to upgrade a user and sync to Google Sheets.
    """
    data = request.json
    secret = data.get('secret_code') or data.get('admin_secret')
    email = (data.get('email') or "").strip().lower()
    name = data.get('name', 'N/A')
    
    # Simple secret check (should be more secure in production)
    if secret != os.getenv("ADMIN_SECRET"):
        return jsonify({"error": "Unauthorized"}), 401
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
        
    # Sync to Google Sheets as PRO version
    success = sheets_service.sync_user(
        email=email,
        name=name,
        plan_type="Pro (Admin)",
        amount="Manual",
        expiry_date=(datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    )
    
    if success:
        return jsonify({
            "success": True,
            "message": f"User {email} successfully upgraded to PRO"
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": "Failed to sync to Google Sheets"
        }), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
