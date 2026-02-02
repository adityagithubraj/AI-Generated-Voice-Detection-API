"""
AI-Generated Voice Detection API
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from typing import Annotated
import config
from models.request_models import VoiceDetectionRequest, VoiceDetectionResponse
from middleware.auth import verify_api_key
from utils.audio_processor import decode_base64_audio, save_temp_audio
from utils.voice_detector import VoiceDetector
import os

# Initialize FastAPI app with enhanced Swagger/OpenAPI documentation
app = FastAPI(
    title="AI-Generated Voice Detection API",
    description="""
    ## 🎯 AI-Generated Voice Detection API
    
    A secure REST API to detect whether a voice sample is **AI-generated** or **Human**.
    
    ### 🌍 Supported Languages
    - Tamil
    - English
    - Hindi
    - Malayalam
    - Telugu
    
    ### 🔐 Authentication
    All requests require a valid API key in the `x-api-key` header.
    
    ### 📋 Features
    - Accepts Base64-encoded MP3 audio files
    - Returns classification with confidence score
    - Provides human-readable explanations
    - Supports multiple Indian languages
    
    ### 📝 Usage
    1. Encode your MP3 audio file to Base64
    2. Send a POST request to `/api/voice-detection`
    3. Include your API key in the `x-api-key` header
    4. Receive classification results with confidence score
    """,
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
    tags_metadata=[
        {
            "name": "Voice Detection",
            "description": "Endpoints for detecting AI-generated vs Human voices",
        },
        {
            "name": "Health",
            "description": "Health check and status endpoints",
        },
    ],
)

# Initialize voice detector
voice_detector = VoiceDetector()


@app.get(
    "/",
    tags=["Health"],
    summary="Root endpoint",
    description="Returns API information and supported languages",
    response_description="API information"
)
async def root():
    """
    Root endpoint that returns API information
    
    Returns basic information about the API including:
    - API name and version
    - List of supported languages
    """
    return {
        "message": "AI-Generated Voice Detection API",
        "version": "1.0.0",
        "supported_languages": config.SUPPORTED_LANGUAGES
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Check if the API is running and healthy",
    response_description="Health status"
)
async def health_check():
    """
    Health check endpoint
    
    Use this endpoint to verify that the API is running correctly.
    Returns a simple status indicator.
    """
    return {"status": "healthy"}


@app.post(
    "/api/voice-detection",
    response_model=VoiceDetectionResponse,
    tags=["Voice Detection"],
    summary="Detect AI-generated vs Human voice",
    description="""
    Analyze a voice sample and determine if it is AI-generated or Human.
    
    **Requirements:**
    - Audio must be MP3 format
    - Audio must be Base64 encoded
    - Language must be one of the supported languages
    - Valid API key required in header
    
    **Response includes:**
    - Classification (AI_GENERATED or HUMAN)
    - Confidence score (0.0 to 1.0)
    - Human-readable explanation
    """,
    response_description="Voice detection results with classification and confidence",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successful detection",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "language": "Tamil",
                        "classification": "AI_GENERATED",
                        "confidenceScore": 0.91,
                        "explanation": "Unnatural pitch consistency and robotic speech patterns detected"
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized - Invalid or missing API key",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Invalid API key"
                    }
                }
            }
        },
        422: {
            "description": "Validation error - Invalid request format",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Invalid audio data: Invalid Base64 encoding"
                    }
                }
            }
        }
    }
)
async def detect_voice(
    request: VoiceDetectionRequest,
    api_key: Annotated[str, Depends(verify_api_key)]
) -> VoiceDetectionResponse:
    """
    Detect if voice is AI-generated or Human
    
    This endpoint analyzes audio features including:
    - Pitch consistency and variation
    - Spectral characteristics
    - MFCC patterns
    - Energy variations
    - Zero crossing rates
    
    **Example Request:**
    ```json
    {
        "language": "Tamil",
        "audioFormat": "mp3",
        "audioBase64": "BASE64_ENCODED_MP3_AUDIO"
    }
    ```
    
    Args:
        request: Voice detection request with audio and language
        api_key: Verified API key from dependency (automatically validated)
        
    Returns:
        VoiceDetectionResponse with classification results including:
        - status: "success" or "error"
        - language: Detected language
        - classification: "AI_GENERATED" or "HUMAN"
        - confidenceScore: Confidence level (0.0 to 1.0)
        - explanation: Human-readable reason for classification
    """
    temp_audio_path = None
    
    try:
        # Validate language
        if request.language not in config.SUPPORTED_LANGUAGES:
            return VoiceDetectionResponse(
                status="error",
                message=f"Unsupported language. Supported languages: {', '.join(config.SUPPORTED_LANGUAGES)}"
            )
        
        # Validate audio format
        if request.audioFormat != "mp3":
            return VoiceDetectionResponse(
                status="error",
                message=f"Unsupported audio format. Only MP3 is supported."
            )
        
        # Decode Base64 audio
        try:
            audio_bytes = decode_base64_audio(request.audioBase64)
        except ValueError as e:
            return VoiceDetectionResponse(
                status="error",
                message=f"Invalid audio data: {str(e)}"
            )
        
        # Check audio size
        audio_size_mb = len(audio_bytes) / (1024 * 1024)
        if audio_size_mb > config.MAX_AUDIO_SIZE_MB:
            return VoiceDetectionResponse(
                status="error",
                message=f"Audio file too large. Maximum size: {config.MAX_AUDIO_SIZE_MB}MB"
            )
        
        # Save to temporary file
        temp_audio_path = save_temp_audio(audio_bytes, request.audioFormat)
        
        # Detect voice
        try:
            classification, confidence, explanation = voice_detector.detect(
                temp_audio_path, 
                request.language
            )
        except Exception as e:
            return VoiceDetectionResponse(
                status="error",
                message=f"Error processing audio: {str(e)}"
            )
        
        # Return success response
        return VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=round(confidence, 2),
            explanation=explanation
        )
        
    except Exception as e:
        return VoiceDetectionResponse(
            status="error",
            message=f"Unexpected error: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.unlink(temp_audio_path)
            except:
                pass


# Custom OpenAPI schema with security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add security scheme for API key
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "x-api-key",
            "description": "API Key for authentication. Include your API key in the header as: x-api-key: YOUR_API_KEY"
        }
    }
    # Apply security only to protected endpoints (voice detection)
    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            if method in ["post", "get", "put", "delete", "patch"]:
                # Only apply security to /api/voice-detection endpoint
                if "/api/voice-detection" in path:
                    operation["security"] = [{"ApiKeyAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

