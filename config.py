"""
Configuration settings for the AI Voice Detection API
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
# Set your API key in .env file or environment variable
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-in-production")
API_KEY_HEADER = "x-api-key"

# Supported languages
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# Audio configuration
SUPPORTED_AUDIO_FORMATS = ["mp3"]
MAX_AUDIO_SIZE_MB = 10
MAX_AUDIO_DURATION_SECONDS = 60

# Model configuration
MODEL_CONFIDENCE_THRESHOLD = 0.5

