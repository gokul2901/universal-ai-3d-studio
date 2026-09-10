from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.schemas.scene_schema import ScenePlan, SceneModificationAction, IntentType

class GenerateRequest(BaseModel):
    prompt: Optional[str] = None
    image_base64: Optional[str] = None
    audio_base64: Optional[str] = None
    language: str = "en"
    project_id: Optional[str] = None
    source: str = "text"  # text, image, voice, multimodal

class GenerationProgressStep(BaseModel):
    step: int
    name: str
    description: str
    status: str = "pending"  # pending, in_progress, completed

class GenerateResponse(BaseModel):
    success: bool
    project_id: str
    scene: ScenePlan
    detected_language: str
    intent: IntentType
    explanation: str
    realistic_image_url: Optional[str] = None
    enhanced_prompt: Optional[str] = None
    audio_url: Optional[str] = None
    tts_audio_base64: Optional[str] = None
    observed_from_image: List[str] = Field(default_factory=list)
    inferred_elements: List[str] = Field(default_factory=list)
    steps: List[GenerationProgressStep] = Field(default_factory=list)

class RealisticImageRequest(BaseModel):
    prompt: str
    style: str = "photorealistic"  # photorealistic, studio, cinematic, automotive, architectural, macro
    width: int = 1280
    height: int = 720
    seed: Optional[int] = None
    fetch_base64: bool = False

class RealisticImageResponse(BaseModel):
    success: bool
    image_url: str
    enhanced_prompt: str
    style: str
    image_base64: Optional[str] = None

class SceneModifyRequest(BaseModel):
    project_id: str
    instruction: str
    language: str = "en"
    current_scene: ScenePlan
    selected_object_id: Optional[str] = None

class SceneModifyResponse(BaseModel):
    success: bool
    scene: ScenePlan
    action_taken: SceneModificationAction
    explanation: str
    tts_audio_base64: Optional[str] = None

class SceneExplainRequest(BaseModel):
    project_id: Optional[str] = None
    target_type: str = "object"  # "object", "scene", "components"
    target_id: Optional[str] = None
    target_name: Optional[str] = None
    language: str = "en"
    context: Optional[Dict[str, Any]] = None

class SceneExplainResponse(BaseModel):
    success: bool
    title: str
    explanation: str
    purpose: str = ""
    characteristics: List[str] = Field(default_factory=list)
    is_estimated: bool = True
    language: str = "en"
    tts_audio_base64: Optional[str] = None

class STTRequest(BaseModel):
    audio_base64: str
    mime_type: str = "audio/webm"
    language_hint: Optional[str] = None

class STTResponse(BaseModel):
    success: bool
    transcription: str
    detected_language: str
    confidence: float = 0.95

class TTSRequest(BaseModel):
    text: str
    language: str = "en"

class TTSResponse(BaseModel):
    success: bool
    audio_base64: Optional[str] = None
    audio_format: str = "mp3"
    language: str = "en"
    fallback_used: bool = False

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

class TranslateResponse(BaseModel):
    success: bool
    translated_text: str
    target_language: str

class ProjectCreate(BaseModel):
    title: str
    prompt: Optional[str] = ""
    language: str = "en"
    scene: Optional[ScenePlan] = None

class ProjectResponse(BaseModel):
    id: str
    title: str
    prompt: str = ""
    language: str = "en"
    created_at: str
    updated_at: str
    thumbnail: Optional[str] = None
    scene: ScenePlan
