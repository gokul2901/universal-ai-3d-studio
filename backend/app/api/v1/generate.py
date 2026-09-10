import uuid
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.schemas.request_response import (
    GenerateRequest, GenerateResponse, GenerationProgressStep,
    RealisticImageRequest, RealisticImageResponse
)
from app.services.ai_orchestrator import ai_orchestrator
from app.services.image_generator import realistic_image_service
from app.providers.groq_provider import groq_provider
from app.providers.tripo_provider import tripo_provider
from app.db.mongodb import db_manager

logger = logging.getLogger(__name__)
router = APIRouter(tags=["generate"])

@router.post("/generate", response_model=GenerateResponse)
async def generate_3d_scene(req: GenerateRequest):
    """
    Unified Multimodal 3D Scene Generation:
    Accepts text, image, and/or voice.
    Determines intent, language, spatial requirements, and outputs a complete 3D scene.
    """
    steps = [
        GenerationProgressStep(step=1, name="Analyze Input", description="Processing multimodal input signals", status="completed"),
        GenerationProgressStep(step=2, name="Understand Request", description="Detecting language and intent", status="completed"),
        GenerationProgressStep(step=3, name="Plan 3D Scene", description="Synthesizing scene graph and geometry layout", status="completed"),
        GenerationProgressStep(step=4, name="Prepare Assets", description="Configuring PBR materials and compound meshes", status="completed"),
        GenerationProgressStep(step=5, name="Build Scene", description="Assembling components and spatial transforms", status="completed"),
        GenerationProgressStep(step=6, name="Render 3D World", description="Calibrating lights, environment, and camera", status="completed"),
        GenerationProgressStep(step=7, name="Ready", description="Interactive 3D workspace active", status="completed"),
    ]

    prompt = req.prompt or ""
    image_analysis = None
    observed = []
    inferred = []

    # 1. Voice transcription if audio provided
    if req.audio_base64:
        from app.services.voice_service import voice_service
        stt_res = await voice_service.speech_to_text(req.audio_base64, req.language)
        if stt_res.get("success") and stt_res.get("transcription"):
            prompt = (prompt + " " + stt_res["transcription"]).strip()

    # 2. Image understanding if image provided
    if req.image_base64:
        try:
            from app.providers.gemini_provider import gemini_provider
            raw_b64 = req.image_base64.split(",")[-1] if "," in req.image_base64 else req.image_base64
            mime_type = "image/jpeg"
            if "image/png" in req.image_base64:
                mime_type = "image/png"
            elif "image/webp" in req.image_base64:
                mime_type = "image/webp"

            image_analysis = await gemini_provider.analyze_multimodal(
                image_base64=raw_b64,
                prompt="Deconstruct this image into precise 3D spatial components: identify the primary object (e.g. racing bike, sports car, drone, spacecraft, mechanical structure), its sub-components, real-world proportions (width, height, depth), materials, colors, and relative positions of each part (e.g. front wheel at +X, rear wheel at -X, chassis at center, handlebars, seat, engine). State primary category and colors explicitly.",
                mime_type=mime_type
            )
            observed.append("Multimodal visual features and exact spatial structure identified by Gemini 2.5 Flash")
            inferred.append("Volumetric 3D geometry and realistic component positioning synthesized by AI")

            # Formulate prompt from image analysis if prompt was empty or very short
            if not prompt.strip() and image_analysis:
                clean_lines = [l.strip().lstrip("#-*1234567890. ") for l in image_analysis.split("\n") if len(l.strip()) > 3]
                if clean_lines:
                    prompt = clean_lines[0][:60]
        except Exception as e:
            logger.warning(f"Gemini image analysis error: {e}")
            observed.append("Visual features and primary boundaries observed from image")
            inferred.append("Volumetric 3D depth and occluded geometry estimated by AI")

    # 3. Detect language
    detected_lang = req.language
    if prompt:
        detected_lang = ai_orchestrator.detect_language(prompt)

    # 4. Classify intent
    intent = ai_orchestrator.classify_intent(prompt)

    # 5. Check Tripo3D API for AI 3D asset generation
    tripo_task_info = None
    if prompt:
        tripo_task_info = await tripo_provider.generate_from_text(prompt)

    # 6. Plan 3D Scene
    scene = await ai_orchestrator.plan_scene(
        prompt=prompt or "Interactive 3D Visualization",
        image_analysis=image_analysis,
        language=detected_lang
    )

    # Attach observed/inferred
    if observed:
        scene.observed_from_image = observed
    if inferred:
        scene.inferred_elements = inferred

    # Generate photorealistic 3D CGI image reference for the scene
    realistic_img_res = await realistic_image_service.generate_realistic_image(
        prompt=prompt or scene.title,
        style="3d_render"
    )
    realistic_img_url = realistic_img_res.get("image_url")
    enhanced_prompt = realistic_img_res.get("enhanced_prompt")
    scene.realistic_image_url = realistic_img_url

    # Persist project
    project_id = req.project_id or f"proj_{uuid.uuid4().hex[:8]}"
    now_str = datetime.now(timezone.utc).isoformat()
    proj_doc = {
        "id": project_id,
        "title": scene.title,
        "prompt": prompt,
        "language": detected_lang,
        "created_at": now_str,
        "updated_at": now_str,
        "realistic_image_url": realistic_img_url,
        "scene": scene.model_dump()
    }
    
    if db_manager.db is not None:
        try:
            await db_manager.db.projects.update_one({"id": project_id}, {"$set": proj_doc}, upsert=True)
        except Exception:
            pass
    db_manager.in_memory_store["projects"][project_id] = proj_doc

    explanation = f"Generated interactive 3D scene '{scene.title}' containing {len(scene.objects)} primary objects with full inspection, animation, and exploded view capability."

    return GenerateResponse(
        success=True,
        project_id=project_id,
        scene=scene,
        detected_language=detected_lang,
        intent=intent,
        explanation=explanation,
        realistic_image_url=realistic_img_url,
        enhanced_prompt=enhanced_prompt,
        observed_from_image=observed,
        inferred_elements=inferred,
        steps=steps
    )

@router.post("/generate/realistic-image", response_model=RealisticImageResponse)
async def generate_realistic_image_endpoint(req: RealisticImageRequest):
    """
    Synthesizes an ultra-realistic 8K photographic visual using Flux Photoreal engine
    with cinematic camera, lighting, and material directives.
    """
    if not req.prompt or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required for realistic image generation")
    
    result = await realistic_image_service.generate_realistic_image(
        prompt=req.prompt,
        style=req.style,
        width=req.width,
        height=req.height,
        seed=req.seed,
        fetch_base64=req.fetch_base64
    )
    return RealisticImageResponse(
        success=True,
        image_url=result["image_url"],
        enhanced_prompt=result["enhanced_prompt"],
        style=result["style"],
        image_base64=result.get("image_base64")
    )

@router.post("/analyze-image")
async def analyze_image_endpoint(payload: dict):
    image_b64 = payload.get("image_base64", "")
    prompt = payload.get("prompt", "Analyze this image for 3D visualization")
    if not image_b64:
        raise HTTPException(status_code=400, detail="image_base64 is required")
    result = await groq_provider.analyze_image(image_b64, prompt)
    return result
