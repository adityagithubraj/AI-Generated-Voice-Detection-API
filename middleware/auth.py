"""
API Key authentication middleware
"""
from fastapi import HTTPException, Header, status
from typing import Annotated
import config


async def verify_api_key(x_api_key: Annotated[str | None, Header(alias="x-api-key")] = None) -> str:
    """
    Verify API key from request headers
    
    Args:
        x_api_key: API key from request header
        
    Raises:
        HTTPException: If API key is missing or invalid
        
    Returns:
        API key if valid
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Please provide x-api-key header."
        )
    
    # Normalize to avoid accidental whitespace/quote mismatches from clients or env files
    provided = x_api_key.strip()
    expected = str(config.API_KEY).strip()
    if provided != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return provided



