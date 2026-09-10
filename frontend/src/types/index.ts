export type IntentType =
  | "CREATE_SCENE"
  | "CREATE_OBJECT"
  | "VISUALIZE_CONCEPT"
  | "TRANSFORM_SCENE"
  | "MODIFY_SCENE"
  | "ADD_OBJECT"
  | "REMOVE_OBJECT"
  | "REPLACE_OBJECT"
  | "MOVE_OBJECT"
  | "RESIZE_OBJECT"
  | "CHANGE_MATERIAL"
  | "CHANGE_COLOR"
  | "CHANGE_STYLE"
  | "ANIMATE_OBJECT"
  | "ANIMATE_SCENE"
  | "EXPLODE_OBJECT"
  | "ASSEMBLE_OBJECT"
  | "EXPLAIN_OBJECT"
  | "EXPLAIN_SCENE"
  | "ANALYZE_OBJECT"
  | "COMPARE_OBJECTS"
  | "IDENTIFY_COMPONENTS"
  | "SHOW_COMPONENTS"
  | "SHOW_INTERNAL_STRUCTURE"
  | "SHOW_FRONT_VIEW"
  | "SHOW_TOP_VIEW"
  | "SHOW_SIDE_VIEW"
  | "SHOW_ISOMETRIC_VIEW"
  | "ZOOM_OBJECT"
  | "HIDE_OBJECT"
  | "SHOW_OBJECT"
  | "RESET_SCENE"
  | "TRANSLATE_EXPLANATION"
  | "GENERATE_EDUCATIONAL_VISUALIZATION";

export interface TransformData {
  position: [number, number, number];
  rotation: [number, number, number];
  scale: [number, number, number];
}

export interface MaterialData {
  color: string;
  roughness: number;
  metalness: number;
  transmission?: number;
  opacity?: number;
  emissive?: string;
  emissive_intensity?: number;
  wireframe?: boolean;
  name?: string;
}

export interface ComponentData {
  id: string;
  name: string;
  purpose?: string;
  description?: string;
  geometry_type: string;
  geometry_params?: Record<string, any>;
  transform: TransformData;
  material: MaterialData;
  explode_offset?: [number, number, number];
}

export interface AnimationData {
  type: "none" | "rotate" | "bounce" | "orbit" | "pulse" | "reciprocate";
  axis?: "x" | "y" | "z";
  speed?: number;
  amplitude?: number;
  is_playing?: boolean;
}

export interface SceneObjectData {
  id: string;
  name: string;
  category: string;
  purpose?: string;
  description?: string;
  geometry_type: string;
  geometry_params?: Record<string, any>;
  transform: TransformData;
  material: MaterialData;
  is_selectable?: boolean;
  is_visible?: boolean;
  is_estimated?: boolean;
  confidence?: number;
  components?: ComponentData[];
  animation?: AnimationData;
  asset_url?: string;
  source_provider?: string;
}

export interface EnvironmentData {
  sky_color: string;
  ground_color: string;
  fog_color?: string;
  fog_density?: number;
  show_grid?: boolean;
  show_axes?: boolean;
  ambient_color?: string;
  ambient_intensity?: number;
}

export interface LightData {
  type: "directional" | "point" | "spot" | "ambient";
  color: string;
  intensity: number;
  position?: [number, number, number];
  cast_shadow?: boolean;
}

export interface CameraData {
  position: [number, number, number];
  target: [number, number, number];
  fov?: number;
  mode?: "perspective" | "orthographic" | "isometric" | "front" | "top" | "side";
}

export interface ScenePlan {
  id: string;
  title: string;
  intent: IntentType;
  scene_type: string;
  user_prompt: string;
  language: string;
  observed_from_image?: string[];
  inferred_elements?: string[];
  environment: EnvironmentData;
  objects: SceneObjectData[];
  lighting: LightData[];
  camera: CameraData;
  realistic_image_url?: string;
  explanation_targets?: string[];
  version: number;
}

export interface GenerationProgressStep {
  step: number;
  name: string;
  description: string;
  status: "pending" | "in_progress" | "completed";
}

export interface GenerateResponse {
  success: boolean;
  project_id: string;
  scene: ScenePlan;
  detected_language: string;
  intent: IntentType;
  explanation: string;
  realistic_image_url?: string;
  enhanced_prompt?: string;
  observed_from_image: string[];
  inferred_elements: string[];
  steps: GenerationProgressStep[];
}

export interface RealisticImageResponse {
  success: boolean;
  image_url: string;
  enhanced_prompt: string;
  style: string;
  image_base64?: string;
}

export interface Project {
  id: string;
  title: string;
  prompt: string;
  language: string;
  created_at: string;
  updated_at: string;
  thumbnail?: string;
  realistic_image_url?: string;
  scene: ScenePlan;
}

export interface ChatMessage {
  id: string;
  sender: "user" | "ai" | "system";
  text: string;
  language?: string;
  timestamp: string;
  target_id?: string;
  purpose?: string;
  characteristics?: string[];
  audio_url?: string;
}
