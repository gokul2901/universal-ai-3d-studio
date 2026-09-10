import json
import logging
import httpx
from typing import Dict, Any, Optional, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class GroqProvider:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) UniversalAI3DStudio/1.0"
            },
            timeout=40.0
        )

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "openai/gpt-oss-120b",
        temperature: float = 0.2,
        json_mode: bool = False
    ) -> str:
        try:
            payload: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
            }
            if json_mode:
                payload["response_format"] = {"type": "json_object"}

            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Groq chat_completion error: {e}")
            raise

    async def analyze_image(
        self,
        image_base64: str,
        prompt: str = "Analyze this image for 3D reconstruction and scene planning."
    ) -> Dict[str, Any]:
        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}" if not image_base64.startswith("data:") else image_base64
                            }
                        }
                    ]
                }
            ]
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": "llama-3.2-11b-vision-preview",
                    "messages": messages,
                    "temperature": 0.2
                }
            )
            response.raise_for_status()
            content = response.json()["choices"][0]["message"]["content"]
            return {"analysis": content, "provider": "groq_vision"}
        except Exception as e:
            logger.warning(f"Groq vision error, will use fallback: {e}")
            return {"analysis": f"Detected objects and spatial layout from uploaded image.", "provider": "vision_fallback"}

    async def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = "speech.webm",
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            files = {"file": (filename, audio_bytes, "audio/webm")}
            data = {"model": "whisper-large-v3"}
            if language:
                data["language"] = language

            response = await self.client.post(
                f"{self.base_url}/audio/transcriptions",
                files=files,
                data=data
            )
            response.raise_for_status()
            result = response.json()
            return {"text": result.get("text", ""), "success": True}
        except Exception as e:
            logger.error(f"Groq Whisper STT error: {e}")
            return {"text": "", "success": False, "error": str(e)}

    async def close(self):
        await self.client.aclose()

groq_provider = GroqProvider()
