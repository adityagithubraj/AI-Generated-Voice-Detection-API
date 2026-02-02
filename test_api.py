"""
Simple test script for the Voice Detection API
"""
import requests
import base64
import json
import sys

# Configuration
API_URL = "http://localhost:8000/api/voice-detection"
# Get API key from environment variable or set it here
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY", "your-secret-api-key-change-in-production")


def encode_audio_to_base64(audio_path: str) -> str:
    """
    Encode audio file to Base64 string
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Base64-encoded string
    """
    try:
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            return base64.b64encode(audio_bytes).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error encoding audio: {str(e)}")
        sys.exit(1)


def test_voice_detection(audio_path: str, language: str = "Tamil"):
    """
    Test the voice detection API
    
    Args:
        audio_path: Path to MP3 audio file
        language: Language of the audio (Tamil, English, Hindi, Malayalam, Telugu)
    """
    print(f"\nTesting Voice Detection API...")
    print(f"Audio file: {audio_path}")
    print(f"Language: {language}")
    print("-" * 50)
    
    # Encode audio to Base64
    print("Encoding audio to Base64...")
    audio_base64 = encode_audio_to_base64(audio_path)
    print("✓ Audio encoded successfully")
    
    # Prepare request
    payload = {
        "language": language,
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Make API request
    print("\nSending request to API...")
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print("\nResponse:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                print("\n✓ Success!")
                print(f"  Classification: {result.get('classification')}")
                print(f"  Confidence: {result.get('confidenceScore')}")
                print(f"  Explanation: {result.get('explanation')}")
            else:
                print(f"\n✗ Error: {result.get('message')}")
        else:
            print(f"\n✗ Request failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API. Make sure the server is running.")
        print("  Start the server with: python main.py")
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_api.py <audio_file.mp3> [language]")
        print("\nExample:")
        print("  python test_api.py sample.mp3 Tamil")
        print("  python test_api.py sample.mp3 English")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "Tamil"
    
    # Validate language
    supported_languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
    if language not in supported_languages:
        print(f"Error: Unsupported language '{language}'")
        print(f"Supported languages: {', '.join(supported_languages)}")
        sys.exit(1)
    
    test_voice_detection(audio_file, language)

