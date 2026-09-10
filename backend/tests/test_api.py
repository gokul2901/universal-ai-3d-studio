import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["providers"]["groq"] is True

@pytest.mark.asyncio
async def test_languages_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/languages")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 16
        codes = [l["code"] for l in data["languages"]]
        assert "ta" in codes
        assert "hi" in codes
        assert "en" in codes
        assert "ar" in codes

@pytest.mark.asyncio
async def test_demo_scenes():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/scene/demos")
        assert response.status_code == 200
        data = response.json()
        assert len(data["demos"]) == 10

@pytest.mark.asyncio
async def test_generate_endpoint_mock_prompt():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "prompt": "Create a futuristic Mars research station",
            "language": "en"
        }
        response = await client.post("/api/v1/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["scene"]["objects"]) > 0
        assert "realistic_image_url" in data["scene"]

@pytest.mark.asyncio
async def test_realistic_image_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "prompt": "Luxury sports car in high-tech studio",
            "style": "photorealistic"
        }
        response = await client.post("/api/v1/generate/realistic-image", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "image_url" in data
        assert "https://image.pollinations.ai/prompt/" in data["image_url"]
        assert "enhanced_prompt" in data
