import json
from fastapi import APIRouter, HTTPException
from app.schemas.scene_schema import ScenePlan

router = APIRouter(prefix="/export", tags=["export"])

@router.post("/scene-json")
async def export_scene_json(scene: ScenePlan):
    """Exports structured scene JSON for offline backup or 3D engine integration."""
    return {
        "success": True,
        "filename": f"{scene.title.replace(' ', '_').lower()}_scene.json",
        "scene": scene.dict()
    }
