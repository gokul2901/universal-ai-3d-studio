import logging
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class GLMProvider:
    def __init__(self):
        self.api_key = settings.GLM_API_KEYS
        self.base_url = "https://open.bigmodel.cn/api/paas/v4"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "Mozilla/5.0 UniversalAI3DStudio/1.0"
            },
            verify=False,  # Avoid local Windows CA certificate issues
            timeout=30.0
        )

    async def chat_completion(self, messages: list, model: str = "glm-4") -> str:
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.3
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            logger.warning(f"GLM chat_completion error: {e}")
            raise

    async def close(self):
        await self.client.aclose()

glm_provider = GLMProvider()
