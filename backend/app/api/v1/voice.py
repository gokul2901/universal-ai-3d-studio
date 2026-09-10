from fastapi import APIRouter, HTTPException, Response
from typing import Dict, Any
from app.schemas.request_response import STTRequest, STTResponse, TTSRequest, TTSResponse, TranslateRequest, TranslateResponse
from app.services.voice_service import voice_service
from app.core.languages import SUPPORTED_LANGUAGES, get_language_info

router = APIRouter(tags=["voice"])

@router.get("/languages")
async def get_supported_languages():
    """Returns the central 16 supported languages with RTL flags and metadata."""
    return {
        "total": len(SUPPORTED_LANGUAGES),
        "languages": list(SUPPORTED_LANGUAGES.values())
    }

@router.post("/stt", response_model=STTResponse)
async def speech_to_text_endpoint(req: STTRequest):
    result = await voice_service.speech_to_text(
        audio_base64=req.audio_base64,
        language_hint=req.language_hint
    )
    return STTResponse(**result)

@router.post("/tts", response_model=TTSResponse)
async def text_to_speech_endpoint(req: TTSRequest):
    result = await voice_service.text_to_speech(
        text=req.text,
        language=req.language
    )
    return TTSResponse(**result)

@router.get("/tts/stream")
async def text_to_speech_stream_endpoint(text: str, language: str = "en"):
    raw_bytes = voice_service.fetch_google_tts_bytes(text, language)
    if raw_bytes:
        return Response(content=raw_bytes, media_type="audio/mpeg")
    raise HTTPException(status_code=500, detail="Failed to synthesize speech")


@router.post("/translate", response_model=TranslateResponse)
async def translate_text_endpoint(req: TranslateRequest):
    from app.providers.groq_provider import groq_provider
    target_info = get_language_info(req.target_language)
    prompt = f"Translate the following text accurately into {target_info['name']} ({target_info['native_name']}). Output ONLY the translated text without commentary:\n\n{req.text}"
    
    try:
        translated = await groq_provider.chat_completion(
            messages=[{"role": "user", "content": prompt}]
        )
        return TranslateResponse(
            success=True,
            translated_text=translated.strip(),
            target_language=req.target_language
        )
    except Exception as e:
        return TranslateResponse(
            success=False,
            translated_text=req.text,
            target_language=req.target_language
        )
