import { ScenePlan, GenerateResponse, Project, RealisticImageResponse } from "../types";

const API_BASE = "http://127.0.0.1:8000/api/v1";

export async function checkBackendHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return await res.json();
}

export async function fetchLanguages() {
  const res = await fetch(`${API_BASE}/languages`);
  return await res.json();
}

export async function fetchDemoScenes() {
  const res = await fetch(`${API_BASE}/scene/demos`);
  return await res.json();
}

export async function generateRealisticImage(params: {
  prompt: string;
  style?: string;
  width?: number;
  height?: number;
  seed?: number;
}): Promise<RealisticImageResponse> {
  const res = await fetch(`${API_BASE}/generate/realistic-image`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Realistic image generation failed: ${err}`);
  }
  return await res.json();
}

export async function generate3DScene(params: {
  prompt?: string;
  image_base64?: string;
  audio_base64?: string;
  language?: string;
  project_id?: string;
}): Promise<GenerateResponse> {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Generation failed: ${err}`);
  }
  return await res.json();
}

export async function modify3DScene(params: {
  project_id: string;
  instruction: string;
  language: string;
  current_scene: ScenePlan;
  selected_object_id?: string | null;
}) {
  const res = await fetch(`${API_BASE}/scene/modify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Scene modification failed: ${err}`);
  }
  return await res.json();
}

export async function explainTarget(params: {
  target_name: string;
  category: string;
  language: string;
  context?: any;
}) {
  const res = await fetch(`${API_BASE}/scene/explain`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  return await res.json();
}

export async function transcribeAudio(audioBase64: string, languageHint?: string) {
  const res = await fetch(`${API_BASE}/stt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ audio_base64: audioBase64, language_hint: languageHint }),
  });
  return await res.json();
}

export async function synthesizeSpeech(text: string, language: string = "en"): Promise<{ success: boolean; audio_base64?: string }> {
  const res = await fetch(`${API_BASE}/tts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language }),
  });
  return await res.json();
}

export function getTTSStreamUrl(text: string, language: string = "en"): string {
  return `${API_BASE}/tts/stream?text=${encodeURIComponent(text)}&language=${encodeURIComponent(language)}`;
}

export async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${API_BASE}/projects`);
  return await res.json();
}

export async function getProjectById(id: string): Promise<Project> {
  const res = await fetch(`${API_BASE}/projects/${id}`);
  return await res.json();
}

export async function saveProject(project: {
  title: string;
  prompt?: string;
  language?: string;
  scene?: ScenePlan;
}) {
  const res = await fetch(`${API_BASE}/projects`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(project),
  });
  return await res.json();
}

export async function deleteProject(id: string) {
  const res = await fetch(`${API_BASE}/projects/${id}`, {
    method: "DELETE",
  });
  return await res.json();
}
