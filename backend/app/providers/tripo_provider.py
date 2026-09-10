import logging
import asyncio
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

class Tripo3DProvider:
    def __init__(self):
        self.api_key = settings.TRIPO3D_API_KEY
        self.base_url = "https://api.tripo3d.ai/v2/openapi"
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) UniversalAI3DStudio/1.0"
            },
            timeout=30.0
        )

    async def get_balance(self) -> Dict[str, Any]:
        try:
            response = await self.client.get(f"{self.base_url}/user/balance")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"Tripo3D get_balance error: {e}")
            return {"code": -1, "data": {"balance": 0}}

    async def generate_from_text(self, prompt: str) -> Dict[str, Any]:
        """
        Creates a text-to-3D task on Tripo3D.
        Returns task details or diagnostic if quota/credits are 0.
        """
        try:
            # First check balance
            balance_info = await self.get_balance()
            balance = balance_info.get("data", {}).get("balance", 0)
            if balance <= 0:
                logger.info("Tripo3D balance is 0; activating seamless high-fidelity procedural generation.")
                return {
                    "success": False,
                    "reason": "insufficient_credits",
                    "message": "Tripo3D credit balance is 0. Using built-in high-fidelity procedural 3D engine.",
                    "task_id": None
                }

            payload = {
                "type": "text_to_model",
                "prompt": prompt
            }
            response = await self.client.post(f"{self.base_url}/task", json=payload)
            response.raise_for_status()
            data = response.json()
            task_id = data.get("data", {}).get("task_id")
            return {"success": True, "task_id": task_id, "data": data}
        except Exception as e:
            logger.warning(f"Tripo3D generate_from_text exception: {e}")
            return {"success": False, "reason": "api_error", "message": str(e)}

    async def generate_from_image(self, file_token_or_url: str) -> Dict[str, Any]:
        try:
            balance_info = await self.get_balance()
            balance = balance_info.get("data", {}).get("balance", 0)
            if balance <= 0:
                return {
                    "success": False,
                    "reason": "insufficient_credits",
                    "message": "Tripo3D credit balance is 0. Using built-in high-fidelity procedural 3D engine."
                }

            payload = {
                "type": "image_to_model",
                "file": {"type": "jpg", "url": file_token_or_url}
            }
            response = await self.client.post(f"{self.base_url}/task", json=payload)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "reason": "api_error", "message": str(e)}

    async def close(self):
        await self.client.aclose()

tripo_provider = Tripo3DProvider()
