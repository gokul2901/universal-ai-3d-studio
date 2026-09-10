from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

IntentType = Literal[
    "CREATE_SCENE", "CREATE_OBJECT", "VISUALIZE_CONCEPT", "TRANSFORM_SCENE",
    "MODIFY_SCENE", "ADD_OBJECT", "REMOVE_OBJECT", "REPLACE_OBJECT",
    "MOVE_OBJECT", "RESIZE_OBJECT", "CHANGE_MATERIAL", "CHANGE_COLOR", "CHANGE_STYLE",
    "ANIMATE_OBJECT", "ANIMATE_SCENE", "EXPLODE_OBJECT", "ASSEMBLE_OBJECT",
    "EXPLAIN_OBJECT", "EXPLAIN_SCENE", "ANALYZE_OBJECT", "COMPARE_OBJECTS",
    "IDENTIFY_COMPONENTS", "SHOW_COMPONENTS", "SHOW_INTERNAL_STRUCTURE",
    "SHOW_FRONT_VIEW", "SHOW_TOP_VIEW", "SHOW_SIDE_VIEW", "SHOW_ISOMETRIC_VIEW",
    "ZOOM_OBJECT", "HIDE_OBJECT", "SHOW_OBJECT", "RESET_SCENE",
    "TRANSLATE_EXPLANATION", "GENERATE_EDUCATIONAL_VISUALIZATION"
]

class TransformData(BaseModel):
    position: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    rotation: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    scale: List[float] = Field(default_factory=lambda: [1.0, 1.0, 1.0])

class MaterialData(BaseModel):
    color: str = "#3b82f6"
    roughness: float = 0.4
    metalness: float = 0.2
    transmission: float = 0.0
    opacity: float = 1.0
    emissive: str = "#000000"
    emissive_intensity: float = 0.0
    wireframe: bool = False
    name: Optional[str] = "PBR_Material"

class ComponentData(BaseModel):
    id: str
    name: str
    purpose: str = ""
    description: str = ""
    geometry_type: str = "box"  # box, sphere, cylinder, cone, torus, etc.
    geometry_params: Dict[str, Any] = Field(default_factory=dict)
    transform: TransformData = Field(default_factory=TransformData)
    material: MaterialData = Field(default_factory=MaterialData)
    explode_offset: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])

class AnimationData(BaseModel):
    type: Literal["none", "rotate", "bounce", "orbit", "pulse", "reciprocate"] = "none"
    axis: Literal["x", "y", "z"] = "y"
    speed: float = 1.0
    amplitude: float = 1.0
    is_playing: bool = True

class SceneObjectData(BaseModel):
    id: str
    name: str
    category: str = "general"
    purpose: str = ""
    description: str = ""
    geometry_type: str = "box"  # box, sphere, cylinder, plane, torus, compound, glb, tripo
    geometry_params: Dict[str, Any] = Field(default_factory=dict)
    transform: TransformData = Field(default_factory=TransformData)
    material: MaterialData = Field(default_factory=MaterialData)
    is_selectable: bool = True
    is_visible: bool = True
    is_estimated: bool = True
    confidence: float = 0.95
    components: List[ComponentData] = Field(default_factory=list)
    animation: AnimationData = Field(default_factory=AnimationData)
    asset_url: Optional[str] = None
    source_provider: str = "procedural"  # procedural, tripo3d, asset_library

class EnvironmentData(BaseModel):
    sky_color: str = "#0b0f19"
    ground_color: str = "#111827"
    fog_color: str = "#0b0f19"
    fog_density: float = 0.015
    show_grid: bool = True
    show_axes: bool = True
    ambient_color: str = "#ffffff"
    ambient_intensity: float = 0.7

class LightData(BaseModel):
    type: Literal["directional", "point", "spot", "ambient"] = "directional"
    color: str = "#ffffff"
    intensity: float = 1.5
    position: List[float] = Field(default_factory=lambda: [5.0, 10.0, 7.0])
    cast_shadow: bool = True

class CameraData(BaseModel):
    position: List[float] = Field(default_factory=lambda: [0.0, 4.0, 10.0])
    target: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    fov: float = 45.0
    mode: Literal["perspective", "orthographic", "isometric", "front", "top", "side"] = "perspective"

class ScenePlan(BaseModel):
    id: str
    title: str = "Universal 3D Scene"
    intent: IntentType = "CREATE_SCENE"
    scene_type: str = "user_defined"
    user_prompt: str = ""
    language: str = "en"
    observed_from_image: Optional[List[str]] = Field(default_factory=list)
    inferred_elements: Optional[List[str]] = Field(default_factory=list)
    environment: EnvironmentData = Field(default_factory=EnvironmentData)
    objects: List[SceneObjectData] = Field(default_factory=list)
    lighting: List[LightData] = Field(default_factory=lambda: [
        LightData(type="directional", color="#ffffff", intensity=1.8, position=[6.0, 12.0, 8.0]),
        LightData(type="ambient", color="#8b5cf6", intensity=0.4, position=[0.0, 5.0, 0.0])
    ])
    camera: CameraData = Field(default_factory=CameraData)
    realistic_image_url: Optional[str] = None
    explanation_targets: List[str] = Field(default_factory=list)
    version: int = 1

class SceneModificationAction(BaseModel):
    action: Literal[
        "ADD_OBJECT", "DELETE_OBJECT", "SCALE_OBJECT", "MOVE_OBJECT", "ROTATE_OBJECT",
        "CHANGE_MATERIAL", "CHANGE_COLOR", "EXPLODE_OBJECT", "ASSEMBLE_OBJECT",
        "ANIMATE_OBJECT", "SET_CAMERA_VIEW", "SET_LIGHTING", "RESET_SCENE"
    ]
    target: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
