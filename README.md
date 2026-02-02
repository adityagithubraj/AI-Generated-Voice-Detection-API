# AI-Generated Voice Detection API

A secure REST API to detect whether a given voice sample is **AI-generated** or **Human**, supporting five Indian languages.

---

## 🚀 Problem Overview
Modern AI systems can generate highly realistic human-like voices, making it difficult to distinguish between real human speech and synthetic audio.

This project provides an API-based solution that analyzes voice samples and classifies them as:
- `AI_GENERATED`
- `HUMAN`

Supported across **Tamil, English, Hindi, Malayalam, and Telugu**.

---

## 🌍 Supported Languages (Fixed)
- Tamil
- English
- Hindi
- Malayalam
- Telugu

Each API request must contain **one audio file in one language**.

---

## 🧠 Features
- Accepts **Base64-encoded MP3 audio**
- Supports **single audio per request**
- Returns **classification + confidence score**
- JSON-based request & response
- **API Key protected** endpoints
- Language-aware detection

---

## 📦 API Specification

### Endpoint
```
POST /api/voice-detection
```

---

### 🔐 Authentication
All requests must include a valid API key in headers:

```
x-api-key: YOUR_SECRET_API_KEY
```

Requests without a valid API key will be rejected.

---

### 📥 Request Body

```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_ENCODED_MP3_AUDIO"
}
```

#### Request Fields
| Field | Description |
|------|------------|
| language | Tamil / English / Hindi / Malayalam / Telugu |
| audioFormat | Must be `mp3` |
| audioBase64 | Base64-encoded MP3 audio |

---

### 📤 Success Response

```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.91,
  "explanation": "Unnatural pitch consistency and robotic speech patterns detected"
}
```

#### Response Fields
| Field | Description |
|------|------------|
| status | success or error |
| language | Detected language |
| classification | AI_GENERATED or HUMAN |
| confidenceScore | Range: 0.0 – 1.0 |
| explanation | Short human-readable reason |

---

### ❌ Error Response

```json
{
  "status": "error",
  "message": "Invalid API key or malformed request"
}
```

---

## 📋 Input Rules
- Audio format: **MP3 only**
- Input must be **Base64 encoded**
- One audio file per request
- Audio must not be altered or pre-processed

---

## ⚖️ Classification Rules
- `AI_GENERATED` → Voice created using AI or synthetic systems
- `HUMAN` → Voice spoken by a real human

> Note: `voiceSource` field is intentionally removed to avoid redundancy.

---

## 🧪 Evaluation Process
- One Base64 MP3 is sent per request
- Language is one of the five supported
- API analyzes and classifies the audio
- JSON response is returned
- Multiple requests are made during evaluation

---

## 🏆 Evaluation Criteria
- 🎯 Accuracy of AI vs Human detection
- 🌍 Consistency across all supported languages
- 📦 Correct API request & response format
- ⚡ Reliability and response time
- 🧠 Quality of explanation

---

## 🚫 Rules & Constraints
- ❌ Hard-coded results are strictly prohibited
- ❌ Data misuse leads to disqualification
- ⚠️ External AI-detection APIs may be restricted
- ✅ Ethical and transparent AI usage is mandatory

---

## 📎 Sample Reference Audio
- Drive link: `sample voice 1.mp3`

---

## 📝 One-Line Summary
Build a secure REST API that accepts a Base64-encoded MP3 voice in Tamil, English, Hindi, Malayalam, or Telugu and accurately identifies whether it is **AI-generated** or **Human**.

---

## 📬 Contact
For queries or integration support, please contact the project maintainer.

