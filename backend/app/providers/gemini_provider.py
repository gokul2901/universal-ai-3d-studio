import json
import logging
import httpx
from typing import Dict, Any, Optional, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiProvider:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.client = httpx.AsyncClient(
            headers={"User-Agent": "UniversalAI3DStudio/1.0"},
            timeout=45.0
        )

    async def generate_content(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        model: str = "gemini-2.5-flash"
    ) -> str:
        try:
            url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
            contents = [{"role": "user", "parts": [{"text": prompt}]}]
            payload: Dict[str, Any] = {"contents": contents}
            if system_instruction:
                payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates and "content" in candidates[0]:
                parts = candidates[0]["content"].get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return ""
        except Exception as e:
            logger.error(f"Gemini generate_content error: {e}")
            raise

    async def analyze_multimodal(
        self,
        image_base64: str,
        prompt: str,
        mime_type: str = "image/jpeg",
        model: str = "gemini-2.5-flash"
    ) -> str:
        try:
            url = f"{self.base_url}/models/{model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inlineData": {
                                    "mimeType": mime_type,
                                    "data": image_base64.split(",")[-1] if "," in image_base64 else image_base64
                                }
                            }
                        ]
                    }
                ]
            }
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            logger.error(f"Gemini multimodal analysis error: {e}")
            raise

    async def close(self):
        await self.client.aclose()

gemini_provider = GeminiProvider()
