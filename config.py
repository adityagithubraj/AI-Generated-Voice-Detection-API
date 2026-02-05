"""
Configuration settings for the AI Voice Detection API
"""
import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

# Be explicit about loading .env from the project root (same directory as this file).
# This avoids common issues where the working directory differs or the file has a BOM.
ENV_PATH = Path(__file__).resolve().parent / ".env"
if ENV_PATH.exists():
    # override=True so changes to .env take effect even if an env var was set elsewhere
    load_dotenv(dotenv_path=ENV_PATH, override=True, encoding="utf-8-sig")
else:
    load_dotenv()

# API Configuration
# Set your API key in .env file or environment variable
def _normalize_api_key(value: str) -> str:
    """
    Normalize API keys loaded from env files.

    This avoids common Windows/.env issues like:
    - surrounding quotes: API_KEY="abc"
    - accidental whitespace: API_KEY= abc
    """
    v = value.strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        v = v[1:-1].strip()
    return v

# Prefer process env var; if missing, try reading .env directly as a fallback.
_raw_api_key = os.getenv("API_KEY")
if not _raw_api_key and ENV_PATH.exists():
    _raw_api_key = dotenv_values(ENV_PATH, encoding="utf-8-sig").get("API_KEY")

API_KEY = _normalize_api_key(_raw_api_key or "your-secret-api-key-change-in-production")
API_KEY_HEADER = "x-api-key"

# Supported languages
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# Audio configuration
SUPPORTED_AUDIO_FORMATS = ["mp3"]
MAX_AUDIO_SIZE_MB = 10
MAX_AUDIO_DURATION_SECONDS = 60

# Model configuration
MODEL_CONFIDENCE_THRESHOLD = 0.5

