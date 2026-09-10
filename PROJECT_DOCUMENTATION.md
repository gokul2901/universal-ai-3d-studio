# 📘 Universal AI 3D Studio — Comprehensive Engineering & Learning Manual

---

## 📑 Table of Contents
1. [Executive Summary & Purpose](#1-executive-summary--purpose)
2. [Full-Stack Architecture & System Design](#2-full-stack-architecture--system-design)
3. [Technology Stack & Library Breakdown](#3-technology-stack--library-breakdown)
4. [Multimodal 3D Scene Generation Engine](#4-multimodal-3d-scene-generation-engine)
5. [Photorealistic 8K CGI Generation Pipeline](#5-photorealistic-8k-cgi-generation-pipeline)
6. [Frontend & Three.js Viewport Implementation](#6-frontend--threejs-viewport-implementation)
7. [Internationalization & RTL Engine (16 Languages)](#7-internationalization--rtl-engine-16-languages)
8. [Backend API Reference & Data Contracts](#8-backend-api-reference--data-contracts)
9. [Database & Persistence Strategy](#9-database--persistence-strategy)
10. [Local Development, Deployment & Docker](#10-local-development-deployment--docker)
11. [Troubleshooting & Gotchas](#11-troubleshooting--gotchas)

---

## 1. Executive Summary & Purpose

### What is Universal AI 3D Studio?
**Universal AI 3D Studio** is an open, multimodal AI platform that allows anyone—from developers and 3D designers to non-technical users—to generate interactive, physically rendered 3D scenes and photorealistic CGI visuals from text prompts, reference images, or voice input.

### Real-World Use Cases
- **Architectural & Interior Pre-visualization**: Rapidly prototype rooms, minimalist villas, and event venues.
- **Mechanical & Engineering Visualization**: Generate compound mechanical assemblies with exploded view inspection.
- **Product Design & E-Commerce**: Showcase 3D interactive product models with customizable PBR materials (metalness, roughness, clearcoat, emissive).
- **Educational & Scientific Simulation**: Interactive astronomical models (Solar System) and aerospace habitats (Mars Station).
- **Multilingual 3D Creation**: Native voice and text interaction across 16 global and regional languages with zero language barrier.

---

## 2. Full-Stack Architecture & System Design

```
+-------------------------------------------------------------------------+
|                              CLIENT TIER                                |
|  React 18 + Vite + Three.js / React Three Fiber + TailwindCSS           |
|                                                                         |
|  [3D Canvas Viewport]  [AI 3D Copilot]  [8K CGI Modal]  [Voice UX]      |
|  - PBR Shaders         - Scene Chat     - Style Selector - STT Visualizer|
|  - Gizmo Controls      - Actions Apply  - 8K Download   - TTS Player    |
|  - Exploded Slider     - Realtime Log   - Prompt Edit    - 16 Lang i18n |
+------------------------------------+------------------------------------+
                                     | REST (JSON / Multipart / Audio)
                                     v
+------------------------------------+------------------------------------+
|                              SERVER TIER                                |
|  FastAPI (Python 3.10+) Async Microservice Architecture                  |
|                                                                         |
|  [Core API Routes]     [AI Orchestrator]        [Realistic CGI Svc]     |
|  - /api/v1/generate    - Language Detection     - Groq CGI Enhancer     |
|  - /api/v1/scene       - Intent Classification  - Pollinations / Flux   |
|  - /api/v1/projects    - Gemini Vision Analysis - 9 Technical Presets   |
|  - /api/v1/voice       - Scene Graph Synthesis  - Subsurface / Lighting |
|  - /api/v1/export      - Tripo3D API Connector  - HDR Environment Plan  |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
|                         PERSISTENCE & ASSETS                            |
|  MongoDB Database / Resilient In-Memory Fallback Store                  |
|  Pre-loaded Optimized GLB Assets (/models/racing_bike, car, watch, etc.)|
+-------------------------------------------------------------------------+
```

---

## 3. Technology Stack & Library Breakdown

### Frontend
- **React 18 (TypeScript)**: Single Page Application with component modularity.
- **Three.js (`three`)**: Core WebGL rendering engine.
- **React Three Fiber (`@react-three/fiber`)**: Declarative Three.js scene graph in React.
- **Drei (`@react-three/drei`)**: Production helpers including `OrbitControls`, `TransformControls`, `Environment`, `ContactShadows`, `Float`.
- **Zustand**: Fast, boilerplate-free state management for 3D scene graph, UI layout, voice, and AI copilot state.
- **Lucide React**: Vector icons for modern dark-mode glassmorphism UI.
- **Tailwind CSS**: Custom color palette, blur filters, and responsive design.

### Backend
- **FastAPI**: Modern, asynchronous Python web framework with auto-generated OpenAPI documentation.
- **Pydantic v2**: High-performance request/response data validation and typing.
- **Groq SDK (Llama-3.3-70B-Versatile)**: Low-latency LLM reasoning for JSON scene planning and technical CGI prompt enhancement.
- **Google GenAI / Gemini 2.5 Flash**: Multimodal vision analysis deconstructing uploaded images into sub-components and spatial dimensions.
- **HTTPX**: Async HTTP client for external AI API calls.
- **Motor**: Async MongoDB driver with automatic memory fallback.
- **gTTS & Whisper**: Speech synthesis and voice transcription.

---

## 4. Multimodal 3D Scene Generation Engine

### Step-by-Step Generation Lifecycle

1. **Multimodal Ingestion**:
   - Accepts text prompt (any language), uploaded reference image (JPEG/PNG/WebP base64), or microphone audio recording.
2. **Speech-to-Text (STT)**:
   - If audio is sent, it is decoded and converted to text using Google Speech Recognition / Whisper.
3. **Multimodal Spatial Deconstruction**:
   - If an image is provided, Gemini 2.5 Flash analyzes the image:
     - Identifies primary object category.
     - Deconstructs distinct sub-parts (e.g. chassis, wheels, handlebars, lenses).
     - Estimates real-world scale, proportions, and PBR material properties.
4. **Language & Intent Classification**:
   - AI Orchestrator identifies the user's language and whether the prompt is a **New Scene**, **Modification**, or **Inquiry**.
5. **3D Scene Graph Synthesis (Groq Llama-3.3)**:
   - Synthesizes a structured `ScenePlan` JSON containing:
     - `objects`: Array of meshes (primitive shapes or GLB links) with `position`, `rotation`, `scale`.
     - `components`: Sub-parts with individual `explode_vector` for exploded view visualization.
     - `material`: Physical properties (`color`, `roughness`, `metalness`, `clearcoat`, `transmission`, `emissive`).
     - `lights`: Ambient and directional light configurations.
     - `camera`: Optimal focal point, FOV, and initial position.
6. **WebGL Scene Instantiation**:
   - React Three Fiber reads the `ScenePlan` and builds the interactive 3D scene in real-time.

---

## 5. Photorealistic 8K CGI Generation Pipeline

While interactive WebGL provides real-time manipulation, users often require **photorealistic, magazine-quality 3D renders** for marketing, presentations, and product showcases.

### The Realistic CGI Engine Architecture
- **Enhancement Service**: Located at `backend/app/services/image_generator.py`.
- **Groq LLM Prompt Engineering**: Takes simple user prompts and enriches them with technical rendering directives:
  - *Engine*: Unreal Engine 5, Octane Render, Blender Cycles.
  - *Lighting*: Global Illumination (Lumen GI), HDR 32-bit environment lighting, volumetric god rays.
  - *Materials*: Physically Based Rendering (PBR), subsurface scattering (SSS), micro-surface roughness, metallic clearcoat.
- **Image Generation Engine**: Uses the high-performance **Flux Photoreal** model via Pollinations API.
- **9 Specialized Style Presets**:
  1. `3d_render` (Default): Unreal Engine 5 CGI Masterpiece
  2. `product_3d`: Blender Cycles Studio Lighting Product Shot
  3. `sci_fi_3d`: Hard-Surface Sci-Fi CGI Render
  4. `cinematic`: Arri Alexa 65mm Anamorphic Film
  5. `studio_product`: Hasselblad 100MP High-Key Commercial
  6. `macro`: 100mm Macro Lens with Micro Surface Detail
  7. `architectural`: Architectural Digest Interior Photography
  8. `automotive`: TopGear Dynamic Car Rig Photography
  9. `cyberpunk`: Neon-lit Rain Reflections & Volumetric Haze

---

## 6. Frontend & Three.js Viewport Implementation

### 1. Viewport Architecture (`ThreeDViewport.tsx`)
- Wrapped in a custom `CanvasErrorBoundary` to prevent WebGL or shader errors from causing black screen crashes.
- Integrates `Environment preset="city"` and `ContactShadows` for realistic ground reflections and soft contact shadows.

### 2. Mesh Rendering & Fallback (`SceneObject.tsx`)
- Renders primitive geometries (Boxes, Spheres, Cylinders, Toruses, Cones, Planes).
- Renders external `.glb` models with standard Three.js loaders.
- Features `GLTFErrorBoundary` with a neutral fallback mesh (`#64748b`) if a remote model fails to download.

### 3. Interactive Tools
- **Transform Gizmo**: Translate, Rotate, and Scale any selected object in the 3D scene.
- **Exploded View Slider**: Smoothly interpolates `explodedFactor` from 0.0 to 2.0 to expand sub-assemblies along their respective `explode_vector`.
- **Camera Presets**: Perspective, Isometric, Front, Top, and Side views.
- **Snapshot & Export**: Instant high-res PNG download and structured Scene JSON export.

---

## 7. Internationalization & RTL Engine (16 Languages)

### Supported Languages
| Code | Language | Script Direction | Region |
|---|---|---|---|
| `en` | English | LTR | Global |
| `ta` | Tamil (தமிழ்) | LTR | India / Sri Lanka |
| `hi` | Hindi (हिन्दी) | LTR | India |
| `bn` | Bengali (বাংলা) | LTR | India / Bangladesh |
| `te` | Telugu (తెలుగు) | LTR | India |
| `mr` | Marathi (मराठी) | LTR | India |
| `ml` | Malayalam (മലയാളം) | LTR | India |
| `ur` | Urdu (اردو) | **RTL** | India / Pakistan |
| `ar` | Arabic (العربية) | **RTL** | Middle East |
| `es` | Spanish (Español) | LTR | Global |
| `fr` | French (Français) | LTR | Global |
| `de` | German (Deutsch) | LTR | Europe |
| `pt` | Portuguese (Português) | LTR | Global |
| `ru` | Russian (Русский) | LTR | Global |
| `zh` | Mandarin (中文) | LTR | Asia |
| `ja` | Japanese (日本語) | LTR | Asia |

### RTL Implementation
- Automatic `document.documentElement.dir = 'rtl'` injection when Arabic or Urdu is selected.
- Tailwind CSS logical padding/margin and dynamic layout flipping.

---

## 8. Backend API Reference & Data Contracts

### 1. `POST /api/v1/generate`
Generates a complete 3D scene from multimodal input.
- **Request Body**:
  ```json
  {
    "prompt": "futuristic sports car",
    "image_base64": null,
    "audio_base64": null,
    "language": "en"
  }
  ```
- **Response**: `GenerateResponse` containing `project_id`, `scene` (full scene graph), `realistic_image_url`, `enhanced_prompt`, and `steps`.

### 2. `POST /api/v1/generate/realistic-image`
Generates an ultra-realistic 8K CGI visual.
- **Request Body**:
  ```json
  {
    "prompt": "hyper-realistic mechanical watch interior",
    "style": "product_3d",
    "width": 1280,
    "height": 720,
    "seed": 42
  }
  ```
- **Response**: `RealisticImageResponse` with direct `image_url` and `enhanced_prompt`.

### 3. `POST /api/v1/scene/action`
Applies AI Copilot natural language modifications to the current active scene.
- **Actions Supported**: `add_object`, `remove_object`, `modify_material`, `change_color`, `explode_view`, `transform_object`, `change_lighting`.

### 4. `POST /api/v1/voice/transcribe` & `POST /api/v1/voice/tts`
Handles bidirectional audio speech-to-text and text-to-speech.

---

## 9. Database & Persistence Strategy

- **Primary Storage**: MongoDB (`projects` collection) via asynchronous `motor` driver.
- **Resilient Fallback**: If MongoDB is not running locally, the server activates an automatic **In-Memory Dictionary Store**, allowing 100% of features to work seamlessly out-of-the-box without requiring a running database server.

---

## 10. Local Development, Deployment & Docker

### 1. Running Locally
```powershell
# Backend (Port 8000)
cd "c:\Users\HP\Documents\3D AI"
$env:PYTHONPATH = "backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend (Port 5173)
cd "c:\Users\HP\Documents\3D AI\frontend"
npm run dev
```

### 2. Running with Docker Compose
```bash
docker-compose up --build
```

---

## 11. Troubleshooting & Gotchas

1. **Draco / KTX2 Texture Warning**:
   - If loading external GLB models with Three.js, ensure `useGLTF(url)` is invoked directly without unconfigured DRACO paths to prevent Three.js loader crashes.
2. **Environment Variables**:
   - Keep your `.env` file in the root directory.
   - Never commit `.env` with actual keys to public repositories (protected by `.gitignore`).
3. **CORS Configuration**:
   - Backend CORS origins are configured in `backend/app/core/config.py` allowing `http://localhost:5173`, `http://127.0.0.1:5173`, and `http://localhost:3000`.

---
*Documentation generated for Universal AI 3D Studio (Version 1.0.0).*
