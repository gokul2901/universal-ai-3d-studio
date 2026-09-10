from fastapi import APIRouter
from app.api.v1 import projects, generate, scene, voice, export

api_router = APIRouter()
api_router.include_router(generate.router)
api_router.include_router(scene.router)
api_router.include_router(projects.router, prefix="/projects")
api_router.include_router(voice.router)
api_router.include_router(export.router)
