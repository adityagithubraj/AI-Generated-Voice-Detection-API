# API Testing Guide

Quick guide on how to check/test the AI Voice Detection API.

## 🚀 Method 1: Swagger UI (Easiest - Interactive)

1. **Start the server:**
   ```bash
   python run.py
   ```
   or
   ```bash
   python main.py
   ```

2. **Open Swagger UI in browser:**
   ```
   http://localhost:8000/docs
   ```

3. **Test endpoints:**
   - Click **"GET /health"** → Click **"Try it out"** → **"Execute"** (no auth needed)
   - Click **"POST /api/voice-detection"** → Click **"Authorize"** (top right) → Enter API key → Click **"Try it out"** → Fill form → **"Execute"**

---

## 🐍 Method 2: Using the Test Script

**Usage:**
```bash
python test_api.py <audio_file.mp3> [language]
```

**Examples:**
```bash
# Test with Tamil audio
python test_api.py sample.mp3 Tamil

# Test with English audio
python test_api.py sample.mp3 English

# Test with Hindi audio
python test_api.py sample.mp3 Hindi
```

**Note:** Make sure you have:
- API server running (`python run.py`)
- Valid API key in `.env` file or environment variable
- MP3 audio file ready

---

## 💻 Method 2B: Simple CLI (Recommended)

This repo includes a lightweight CLI that:
- checks health (`GET /health`)
- does voice check (`POST /api/voice-detection`) by auto-encoding your MP3 to Base64

**Examples:**

```bash
# Health check (no API key needed)
python cli.py health

# Voice check (API key required)
python cli.py detect sample.mp3 Tamil
```

**If your API key is not in `.env`:**

```bash
python cli.py detect sample.mp3 Tamil --api-key your-secret-api-key-change-in-production
```

**If your API is running on a different host/port:**

```bash
python cli.py --base-url http://127.0.0.1:8000 health
python cli.py --base-url http://127.0.0.1:8000 detect sample.mp3 English
```

---

## 🔧 Method 3: Using cURL (Command Line)

### Health Check (No Auth Required)
```bash
curl http://localhost:8000/health
```

### Root Endpoint (No Auth Required)
```bash
curl http://localhost:8000/
```

### Voice Detection (Requires API Key)
```bash
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "x-api-key: your-secret-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "BASE64_ENCODED_AUDIO_HERE"
  }'
```

---

## 🐍 Method 4: Using Python Requests

```python
import requests
import base64

# Configuration
API_URL = "http://localhost:8000/api/voice-detection"
API_KEY = "your-secret-api-key-change-in-production"

# Encode audio file
with open("sample.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode("utf-8")

# Prepare request
payload = {
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": audio_base64
}

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# Make request
response = requests.post(API_URL, json=payload, headers=headers)
print(response.json())
```

---

## 📋 Quick Checklist

Before testing, ensure:
- ✅ Server is running (`python run.py`)
- ✅ API key is set in `.env` file or environment variable
- ✅ Audio file is MP3 format
- ✅ Audio file size < 10MB
- ✅ Language is one of: Tamil, English, Hindi, Malayalam, Telugu

---

## 🔍 Available Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | No | API info and supported languages |
| `/health` | GET | No | Health check |
| `/api/voice-detection` | POST | Yes | Detect AI vs Human voice |
| `/docs` | GET | No | Swagger UI documentation |
| `/redoc` | GET | No | ReDoc documentation |
| `/openapi.json` | GET | No | OpenAPI schema |

---

## 🐛 Troubleshooting

**Connection Error:**
- Make sure server is running: `python run.py`
- Check if port 8000 is available

**401 Unauthorized:**
- Check API key in `.env` file
- Verify `x-api-key` header is included

**422 Validation Error:**
- Check audio format is "mp3"
- Verify Base64 encoding is correct
- Check language is supported

**Audio Processing Error:**
- Verify audio file is valid MP3
- Check file size < 10MB
- Ensure audio duration < 60 seconds

