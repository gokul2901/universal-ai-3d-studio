# Universal AI 3D Studio

> *"Anything you imagine. Visualized in interactive 3D."*

**Universal AI 3D Studio** is a general-purpose, multimodal AI-powered 3D visualization and generation platform. It is intent-driven and category-independent, transforming text, images, and voice across 16 languages into explodable, interactive 3D WebGL scenes.

---

## Key Features

- **Universal Input**: Describe anything using text prompts, reference images, voice commands, or follow-up conversations.
- **AI Scene Planner**: Generic schema generator outputting transforms, compound meshes, PBR materials, dynamic lighting, and camera setups.
- **Provider Abstraction**: Plug-and-play architecture supporting Groq Llama-3.3, Google Gemini, Zhipu GLM, and Tripo3D API, with automatic fallback to high-fidelity procedural 3D synthesis.
- **Interactive Three.js / R3F Engine**:
  - Real-time WebGL rendering with PBR shaders and dynamic shadows.
  - Interactive raycasting object selection & highlight.
  - Transform gizmo controls (Translate, Rotate, Scale).
  - Exploded view slider separating compound components outward.
  - Multi-angle camera switcher (Perspective, Isometric, Front, Top, Side).
  - Animation timeline with scrub bar and speed controls (0.5x, 1x, 2x).
  - High-res Screenshot PNG & structured Scene JSON export.
- **AI 3D Copilot**: Context-aware assistant supporting natural language 3D editing and multilingual explanations.
- **16 Supported Languages**:
  - **Indian**: Tamil (`ta`), Hindi (`hi`), Bengali (`bn`), Telugu (`te`), Marathi (`mr`), Malayalam (`ml`), Urdu (`ur`).
  - **International**: English (`en`), Spanish (`es`), Mandarin (`zh`), Arabic (`ar`), French (`fr`), Portuguese (`pt`), Russian (`ru`), German (`de`), Japanese (`ja`).
  - Native **RTL (Right-to-Left)** support for Arabic and Urdu.
- **Voice UX**: Live canvas audio waveform visualizer and multilingual Text-to-Speech player.
- **10 Instant Demonstrations**:
  1. Grand Luxury Wedding Stage
  2. Ares-VII Mars Surface Research Station
  3. Interactive Solar System
  4. V-Twin Mechanical Engine (with Exploded View)
  5. Modern AI Startup Office
  6. Luxury Bistro Restaurant
  7. Cyberpunk Metropolis
  8. Modern Minimalist Villa
  9. Smart Robotics Assembly Factory
  10. Holographic Product Showroom

---

## Project Structure

```
universal-ai-3d-studio/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # Endpoints: /generate, /scene, /projects, /voice, /export
│   │   ├── core/            # Config, central 16-languages metadata
│   │   ├── db/              # Motor/MongoDB connection with memory fallback
│   │   ├── providers/       # Groq, Gemini, Tripo3D, GLM providers
│   │   ├── schemas/         # Pydantic generic scene specification & actions
│   │   ├── services/        # AI orchestrator, voice service, 10 demo presets
│   │   └── main.py          # FastAPI application
│   ├── tests/               # Pytest automated test suite
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── 3d/          # Viewport, SceneObject, Toolbar, Transform, Camera
│   │   │   ├── ai/          # AICopilot, ChatMessage, GenerationProgress
│   │   │   ├── inspector/   # ObjectInspector with AI Estimated badges
│   │   │   ├── scene/       # SceneTree, AnimationTimeline
│   │   │   ├── upload/      # ImageUploader with drag-and-drop
│   │   │   ├── voice/       # VoiceRecorder with waveform, TTSPlayer
│   │   │   └── ui/          # Navbar, AppShell
│   │   ├── pages/           # LandingPage, CreatePage, StudioPage, ProjectsPage, SettingsPage
│   │   ├── store/           # Zustand state management
│   │   ├── services/        # Typed API service layer
│   │   └── i18n/            # 16-language dictionaries & RTL engine
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- (Optional) MongoDB local or Atlas (defaults to local `mongodb://127.0.0.1:27017`)

### 2. Backend Setup
```bash
# Set Python path and install requirements
pip install -r backend/requirements.txt

# Run backend tests
$env:PYTHONPATH="backend"; python -m pytest backend/tests/test_api.py -v

# Start FastAPI server (runs on http://127.0.0.1:8000)
$env:PYTHONPATH="backend"; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install

# Run Vite dev server (runs on http://127.0.0.1:5173)
npm run dev
```

Open [http://127.0.0.1:5173](http://127.0.0.1:5173) to explore the 3D Studio!
