"""
Pydantic models for API request/response
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Literal


class VoiceDetectionRequest(BaseModel):
    """Request model for voice detection API"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "language": "Tamil",
                "audioFormat": "mp3",
                "audioBase64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQAAAAA="
            }
        }
    )
    
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"] = Field(
        ..., 
        description="Language of the audio (Tamil, English, Hindi, Malayalam, or Telugu)",
        examples=["Tamil", "English", "Hindi"]
    )
    audioFormat: Literal["mp3"] = Field(
        ..., 
        description="Audio format (must be mp3)",
        examples=["mp3"]
    )
    audioBase64: str = Field(
        ..., 
        description="Base64-encoded MP3 audio file. The audio should be encoded in Base64 format.",
        examples=["UklGRiQAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQAAAAA="]
    )
    
    @field_validator('audioBase64')
    @classmethod
    def validate_base64(cls, v: str) -> str:
        """Validate Base64 string"""
        if not v or len(v) == 0:
            raise ValueError("audioBase64 cannot be empty")
        # Basic Base64 validation
        try:
            import base64
            base64.b64decode(v, validate=True)
        except Exception:
            raise ValueError("Invalid Base64 encoding")
        return v


class VoiceDetectionResponse(BaseModel):
    """Response model for voice detection API"""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "success",
                    "language": "Tamil",
                    "classification": "AI_GENERATED",
                    "confidenceScore": 0.91,
                    "explanation": "Unnatural pitch consistency and robotic speech patterns detected"
                },
                {
                    "status": "success",
                    "language": "English",
                    "classification": "HUMAN",
                    "confidenceScore": 0.87,
                    "explanation": "Natural speech patterns with expected variations detected"
                },
                {
                    "status": "error",
                    "message": "Invalid API key"
                }
            ]
        }
    )
    
    status: Literal["success", "error"] = Field(
        ..., 
        description="Status of the request",
        examples=["success", "error"]
    )
    language: str | None = Field(
        None, 
        description="Detected language",
        examples=["Tamil", "English", "Hindi"]
    )
    classification: Literal["AI_GENERATED", "HUMAN"] | None = Field(
        None, 
        description="Classification result: AI_GENERATED for synthetic voices, HUMAN for natural human speech",
        examples=["AI_GENERATED", "HUMAN"]
    )
    confidenceScore: float | None = Field(
        None, 
        ge=0.0, 
        le=1.0, 
        description="Confidence score ranging from 0.0 (low confidence) to 1.0 (high confidence)",
        examples=[0.91, 0.87, 0.75]
    )
    explanation: str | None = Field(
        None, 
        description="Human-readable explanation of the classification result",
        examples=["Unnatural pitch consistency and robotic speech patterns detected", 
                 "Natural speech patterns with expected variations detected"]
    )
    message: str | None = Field(
        None, 
        description="Error message if status is error",
        examples=["Invalid API key", "Invalid audio data: Invalid Base64 encoding"]
    )

