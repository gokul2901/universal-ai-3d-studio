import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Universal AI 3D Studio"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # API Keys loaded from .env or environment
    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GLM_API_KEYS: str = ""
    TRIPO3D_API_KEY: str = ""
    
    # Database
    MONGODB_URI: str = "mongodb://127.0.0.1:27017"
    DATABASE_NAME: str = "universal_3d_studio"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    
    # Storage
    UPLOAD_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
    ASSET_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")

settings = Settings()
