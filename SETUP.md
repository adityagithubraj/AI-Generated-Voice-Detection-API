# Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd AI-Generated-Voice-Detection-API
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   - Copy `.env.example` to `.env` (if available) or create a `.env` file
   - Set your API key:
     ```
     API_KEY=your-secret-api-key-change-in-production
     ```

6. **Run the API server**
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API endpoint: `http://localhost:8000/api/voice-detection`
   - API documentation: `http://localhost:8000/docs`
   - Health check: `http://localhost:8000/health`

## Testing the API

You can test the API using curl or any HTTP client:

```bash
curl -X POST "http://localhost:8000/api/voice-detection" \
  -H "x-api-key: your-secret-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "BASE64_ENCODED_MP3_AUDIO"
  }'
```

## Notes
- Make sure to change the default API key in production
- The API accepts Base64-encoded MP3 audio files
- Supported languages: Tamil, English, Hindi, Malayalam, Telugu

