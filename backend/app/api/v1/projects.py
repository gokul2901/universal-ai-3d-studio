import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from app.schemas.request_response import ProjectCreate, ProjectResponse
from app.schemas.scene_schema import ScenePlan
from app.db.mongodb import db_manager
from app.services.assets.demo_presets import get_demo_scenes

router = APIRouter(tags=["projects"])

def _enrich_scene_assets(scene_data: dict):
    if not scene_data or not isinstance(scene_data, dict):
        return
    title = (scene_data.get("title") or "").lower()
    prompt = (scene_data.get("user_prompt") or "").lower()
    for obj in scene_data.get("objects", []):
        name = (obj.get("name") or "").lower()
        cat = (obj.get("category") or "").lower()
        if not obj.get("asset_url"):
            if any(k in name or k in cat or k in title or k in prompt for k in ["car", "hypercar", "supercar", "ferrari", "vehicle", "auto", "roadster", "convertible"]):
                obj["asset_url"] = "/models/sports_car.glb"
            elif any(k in name or k in cat or k in title or k in prompt for k in ["bike", "motorcycle", "bicycle", "cycle"]):
                obj["asset_url"] = "/models/racing_bike.glb"
            elif any(k in name or k in cat or k in title or k in prompt for k in ["watch", "smartwatch", "clock", "timepiece"]):
                obj["asset_url"] = "/models/luxury_watch.glb"

@router.get("", response_model=List[ProjectResponse])
async def list_projects():
    projects_list = []
    
    # Try MongoDB
    if db_manager.db is not None:
        try:
            cursor = db_manager.db.projects.find().sort("updated_at", -1)
            async for doc in cursor:
                doc["id"] = str(doc.get("_id", doc.get("id")))
                if "scene" in doc:
                    _enrich_scene_assets(doc["scene"])
                projects_list.append(ProjectResponse(**doc))
            if projects_list:
                return projects_list
        except Exception:
            pass

    # From memory store or initialize with demos
    if not db_manager.in_memory_store["projects"]:
        demos = get_demo_scenes()
        now_str = datetime.now(timezone.utc).isoformat()
        for key, demo_scene in demos.items():
            proj = ProjectResponse(
                id=demo_scene.id,
                title=demo_scene.title,
                prompt=demo_scene.user_prompt,
                language=demo_scene.language,
                created_at=now_str,
                updated_at=now_str,
                scene=demo_scene
            )
            db_manager.in_memory_store["projects"][proj.id] = proj.dict()

    return [ProjectResponse(**p) for p in db_manager.in_memory_store["projects"].values()]

@router.post("", response_model=ProjectResponse)
async def create_project(req: ProjectCreate):
    proj_id = f"proj_{uuid.uuid4().hex[:8]}"
    now_str = datetime.now(timezone.utc).isoformat()
    
    scene = req.scene
    if not scene:
        from app.services.ai_orchestrator import ai_orchestrator
        scene = ai_orchestrator._build_procedural_scene(req.prompt or req.title, req.language)
    
    proj_data = {
        "id": proj_id,
        "title": req.title,
        "prompt": req.prompt or "",
        "language": req.language,
        "created_at": now_str,
        "updated_at": now_str,
        "scene": scene.dict() if hasattr(scene, "dict") else scene
    }

    if db_manager.db is not None:
        try:
            await db_manager.db.projects.insert_one(dict(proj_data))
        except Exception:
            pass
            
    db_manager.in_memory_store["projects"][proj_id] = proj_data
    return ProjectResponse(**proj_data)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    if db_manager.db is not None:
        try:
            doc = await db_manager.db.projects.find_one({"id": project_id})
            if doc:
                doc["id"] = str(doc.get("_id", doc.get("id")))
                if "scene" in doc:
                    _enrich_scene_assets(doc["scene"])
                return ProjectResponse(**doc)
        except Exception:
            pass

    proj = db_manager.in_memory_store["projects"].get(project_id)
    if proj and "scene" in proj:
        _enrich_scene_assets(proj["scene"])
    if not proj:
        # Check demos
        demos = get_demo_scenes()
        for key, demo_scene in demos.items():
            if demo_scene.id == project_id or key == project_id:
                now_str = datetime.utcnow().isoformat()
                return ProjectResponse(
                    id=demo_scene.id,
                    title=demo_scene.title,
                    prompt=demo_scene.user_prompt,
                    language=demo_scene.language,
                    created_at=now_str,
                    updated_at=now_str,
                    scene=demo_scene
                )
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse(**proj)

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    if db_manager.db is not None:
        try:
            await db_manager.db.projects.delete_one({"id": project_id})
        except Exception:
            pass
    db_manager.in_memory_store["projects"].pop(project_id, None)
    return {"success": True, "message": f"Project {project_id} deleted"}
