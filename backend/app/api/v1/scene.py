from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.schemas.scene_schema import ScenePlan
from app.schemas.request_response import (
    SceneModifyRequest, SceneModifyResponse,
    SceneExplainRequest, SceneExplainResponse
)
from app.services.ai_orchestrator import ai_orchestrator
from app.services.assets.demo_presets import get_demo_scenes

router = APIRouter(prefix="/scene", tags=["scene"])

@router.get("/demos")
async def get_all_demos():
    """Returns all 10 built-in demonstration scenes."""
    demos = get_demo_scenes()
    return {
        "demos": [
            {
                "id": scene.id,
                "key": key,
                "title": scene.title,
                "scene_type": scene.scene_type,
                "prompt": scene.user_prompt,
                "objects_count": len(scene.objects),
                "scene": scene
            }
            for key, scene in demos.items()
        ]
    }

@router.post("/plan", response_model=ScenePlan)
async def plan_scene_endpoint(payload: dict):
    prompt = payload.get("prompt", "")
    language = payload.get("language", "en")
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    return await ai_orchestrator.plan_scene(prompt=prompt, language=language)

@router.post("/modify", response_model=SceneModifyResponse)
async def modify_scene_endpoint(req: SceneModifyRequest):
    """
    Executes validated modifications on active scene graph using strict schema.
    """
    result = await ai_orchestrator.modify_scene(
        instruction=req.instruction,
        current_scene=req.current_scene,
        selected_object_id=req.selected_object_id,
        language=req.language
    )
    return SceneModifyResponse(**result)

@router.post("/explain", response_model=SceneExplainResponse)
async def explain_scene_endpoint(req: SceneExplainRequest):
    """
    Generates AI explanations in the selected/detected language (Tamil, Hindi, etc.)
    """
    target_name = req.target_name or "Scene Element"
    category = (req.context or {}).get("category", "general")
    explanation_data = await ai_orchestrator.explain_target(
        target_name=target_name,
        category=category,
        language=req.language,
        context=str(req.context)
    )

    return SceneExplainResponse(
        success=True,
        title=explanation_data.get("title", target_name),
        explanation=explanation_data.get("explanation", ""),
        purpose=explanation_data.get("purpose", ""),
        characteristics=explanation_data.get("characteristics", []),
        is_estimated=True,
        language=req.language
    )
