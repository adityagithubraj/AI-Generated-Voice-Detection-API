# Swagger/OpenAPI Documentation Guide

##  Accessing Swagger UI

The API includes comprehensive Swagger/OpenAPI documentation that can be accessed in two ways:

### 1. Swagger UI (Interactive)
**URL:** `http://localhost:8000/docs`

This provides an interactive interface where you can:
- View all available endpoints
- See request/response schemas
- Test API endpoints directly
- View examples and descriptions
- Authenticate with your API key

### 2. ReDoc (Alternative Documentation)
**URL:** `http://localhost:8000/redoc`

This provides a clean, readable documentation format.

### 3. OpenAPI JSON Schema
**URL:** `http://localhost:8000/openapi.json`

This returns the raw OpenAPI schema in JSON format, useful for API clients and code generation.

##  Authentication in Swagger

When testing endpoints in Swagger UI:

1. Click the **"Authorize"** button at the top right
2. Enter your API key in the `ApiKeyAuth` field (get it from your `.env` file or environment variables)
3. Click **"Authorize"** to save
4. Now you can test protected endpoints directly from Swagger UI

##  Features Included

### Enhanced Documentation
-  Detailed endpoint descriptions
-  Request/response examples
-  Field descriptions and constraints
-  Error response examples
-  Tag-based organization
-  Security scheme documentation

### Endpoints Documented
- **GET /** - Root endpoint (public)
- **GET /health** - Health check (public)
- **POST /api/voice-detection** - Voice detection (protected, requires API key)

### Request/Response Examples
Each endpoint includes:
- Example request bodies
- Example success responses
- Example error responses
- Field descriptions and types

##  Testing with Swagger UI

1. Start the server:
   ```bash
   python main.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/docs
   ```

3. Click on **"POST /api/voice-detection"** to expand it

4. Click **"Try it out"** button

5. Fill in the request:
   - `language`: Select from dropdown (Tamil, English, Hindi, Malayalam, Telugu)
   - `audioFormat`: "mp3"
   - `audioBase64`: Paste your Base64-encoded MP3 audio

6. Click **"Execute"** to send the request

7. View the response below with classification results

## Notes

- Health endpoints (`/` and `/health`) are public and don't require authentication
- Only `/api/voice-detection` requires API key authentication
- All examples in Swagger are interactive and can be tested directly
- The API key can be set globally using the "Authorize" button