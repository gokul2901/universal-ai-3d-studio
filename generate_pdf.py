import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))
        # Header
        self.drawString(54, letter[1] - 36, "Universal AI 3D Studio — Comprehensive Documentation")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 36, page_text)
        self.drawString(54, 36, "Confidential & Proprietary — Universal AI 3D Studio v1.0.0")
        self.line(54, 48, letter[0] - 54, 48)
        self.restoreState()

def generate_pdf(output_path="PROJECT_DOCUMENTATION.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#0f172a"),
        alignment=0,
        spaceAfter=12
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#475569"),
        spaceAfter=24
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#64748b")
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#334155"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        spaceAfter=4
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#e2e8f0"),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=8,
        leftIndent=10,
        rightIndent=10
    )

    story = []

    # ================= COVER PAGE =================
    story.append(Spacer(1, 40))
    story.append(Paragraph("UNIVERSAL AI 3D STUDIO", ParagraphStyle('Badge', fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor("#4f46e5"), spaceAfter=10)))
    story.append(Paragraph("Full Technical Architecture & Engineering Documentation", title_style))
    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor("#4f46e5"), spaceAfter=18))
    story.append(Paragraph("An end-to-end guide to the Multimodal 3D Scene Generation Engine, Photorealistic 8K CGI Pipeline, Three.js WebGL Viewport, and 16-Language Internationalization Architecture.", subtitle_style))
    
    story.append(Spacer(1, 80))
    
    metadata_table = Table([
        [Paragraph("<b>Version:</b> 1.0.0", meta_style), Paragraph("<b>Target Architecture:</b> Full-Stack WebGL + FastAPI", meta_style)],
        [Paragraph("<b>Author / Owner:</b> Gokulakrishnan (@gokul2901)", meta_style), Paragraph("<b>Repository:</b> github.com/gokul2901/universal-ai-3d-studio", meta_style)],
        [Paragraph("<b>Date:</b> September 2026", meta_style), Paragraph("<b>Tech Stack:</b> React 18, Three.js, FastAPI, Groq, Gemini", meta_style)]
    ], colWidths=[240, 260])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(metadata_table)
    story.append(PageBreak())

    # ================= SECTION 1 =================
    story.append(Paragraph("1. Executive Summary & Purpose", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("<b>Universal AI 3D Studio</b> is a general-purpose, multimodal 3D generation and real-time visualization platform. It empowers users to turn text prompts, reference images, and voice recordings into explodable, interactive 3D WebGL scenes and photorealistic 8K CGI visuals.", body_style))
    
    story.append(Paragraph("Key Capabilities:", h2_style))
    story.append(Paragraph("• <b>Multimodal Input Ingestion:</b> Supports text prompts, drag-and-drop reference images, and live microphone speech across 16 languages.", bullet_style))
    story.append(Paragraph("• <b>Deterministic 3D Scene Graph:</b> AI Orchestrator synthesizes structured Pydantic scene schemas (transforms, meshes, PBR materials, lighting).", bullet_style))
    story.append(Paragraph("• <b>Exploded View Inspection:</b> Interactive slider smoothly disassembles compound mechanical and architectural components along sub-part explode vectors.", bullet_style))
    story.append(Paragraph("• <b>Photorealistic 8K CGI Engine:</b> LLM prompt-engineering converts simple inputs into Unreal Engine 5 / Octane PBR render directives using Flux.", bullet_style))
    story.append(Paragraph("• <b>Zero-Configuration Resilience:</b> Resilient architecture with built-in in-memory fallbacks when external DB or cloud GPUs are unreachable.", bullet_style))
    
    story.append(Spacer(1, 12))

    # ================= SECTION 2 =================
    story.append(Paragraph("2. System Architecture & Component Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("The platform is structured into two decoupled tiers: a high-performance <b>React + Three.js</b> frontend single-page application and an asynchronous <b>FastAPI (Python 3.10+)</b> intelligence backend.", body_style))
    
    arch_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Key Responsibilities</b>", body_style)],
        [Paragraph("Frontend Client", body_style), Paragraph("React 18 + Vite + TS", body_style), Paragraph("Interactive UI, Zustand state stores, responsive Tailwind panels, 16-language i18n switching.", body_style)],
        [Paragraph("3D Viewport", body_style), Paragraph("Three.js + R3F + Drei", body_style), Paragraph("WebGL rendering, OrbitControls, TransformControls gizmo, exploded view interpolation, shadows.", body_style)],
        [Paragraph("API Gateway", body_style), Paragraph("FastAPI (Python 3.10+)", body_style), Paragraph("Async REST endpoints, CORS middleware, Pydantic validation, lifecycle handlers.", body_style)],
        [Paragraph("AI Orchestrator", body_style), Paragraph("Groq Llama-3.3 70B", body_style), Paragraph("Structured JSON scene synthesis, language detection, intent classification, copilot modifications.", body_style)],
        [Paragraph("Vision Engine", body_style), Paragraph("Google Gemini 2.5 Flash", body_style), Paragraph("Multimodal image deconstruction (sub-assemblies, bounding proportions, PBR materials).", body_style)],
        [Paragraph("CGI Generator", body_style), Paragraph("Pollinations Flux Engine", body_style), Paragraph("Photorealistic 8K render generation with technical UE5 / Octane prompt enhancements.", body_style)],
        [Paragraph("Storage Tier", body_style), Paragraph("MongoDB + In-Memory", body_style), Paragraph("Project persistence, scene caching, automatic in-memory fallback store.", body_style)],
    ]
    arch_table = Table(arch_data, colWidths=[100, 120, 280])
    arch_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(arch_table)
    story.append(PageBreak())

    # ================= SECTION 3 =================
    story.append(Paragraph("3. Multimodal Generation & 3D Scene Pipeline", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("The scene generation lifecycle transforms raw multimodal input into a fully realized interactive 3D WebGL scene through 7 orchestrated stages:", body_style))
    
    story.append(Paragraph("1. Audio Speech-to-Text: If microphone audio is received, voice_service.py transcribes the base64 audio.", bullet_style))
    story.append(Paragraph("2. Gemini Multimodal Analysis: Uploaded images are deconstructed into primary objects, component parts, and physical dimensions.", bullet_style))
    story.append(Paragraph("3. Intent & Language Detection: The AI Orchestrator identifies the user's language (Tamil, Hindi, English, Arabic, etc.) and intent.", bullet_style))
    story.append(Paragraph("4. Groq Scene Graph Synthesis: Llama-3.3 produces a deterministic JSON schema containing meshes, positions, rotations, scales, PBR materials, and explode vectors.", bullet_style))
    story.append(Paragraph("5. Asset Enrichment: Projects service matches keywords to pre-optimized GLB models (/models/racing_bike, car, luxury_watch) or procedural meshes.", bullet_style))
    story.append(Paragraph("6. Realistic CGI Synthesis: Generates a high-resolution 8K photographic render preview in parallel.", bullet_style))
    story.append(Paragraph("7. WebGL Instantiation: React Three Fiber mounts the scene with lighting, shadows, and interactive gizmos.", bullet_style))
    
    story.append(Paragraph("Sample ScenePlan Schema Representation:", h2_style))
    story.append(Paragraph("""{
  "title": "Ares-VII Mars Surface Research Station",
  "objects": [
    {
      "name": "Central Habitat Dome",
      "geometry": "sphere",
      "position": [0, 1.2, 0],
      "scale": [2.5, 1.8, 2.5],
      "material": { "color": "#e2e8f0", "roughness": 0.25, "metalness": 0.85 },
      "components": [
        { "name": "Airlock Pod", "geometry": "cylinder", "explode_vector": [1.5, 0, 0] },
        { "name": "Solar Array", "geometry": "box", "explode_vector": [-1.8, 0.5, 0] }
      ]
    }
  ]
}""", code_style))

    story.append(Spacer(1, 10))

    # ================= SECTION 4 =================
    story.append(Paragraph("4. Photorealistic 8K CGI Engine", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("The realistic image generator (image_generator.py) produces ultra-realistic visual renders to complement real-time WebGL models.", body_style))
    story.append(Paragraph("• <b>Technical Prompt Directives:</b> Automatically injects physical rendering terminology: 'Unreal Engine 5 photorealistic 3D CGI render, Octane renderer, Lumen Global Illumination, PBR roughness 0.15, subsurface scattering, 8K ultra high resolution'.", bullet_style))
    story.append(Paragraph("• <b>Style Presets:</b> 9 dedicated styles including 3D CGI Render (UE5), Product 3D (Blender Cycles), Hard-Surface Sci-Fi, Studio Commercial, Macro 100mm, Architectural Interior, Dynamic Automotive, and Cyberpunk.", bullet_style))
    story.append(Paragraph("• <b>Interactive Modal:</b> Includes instant zoom, download button, seed customization, and prompt refinement.", bullet_style))

    story.append(PageBreak())

    # ================= SECTION 5 =================
    story.append(Paragraph("5. 16-Language Internationalization & RTL Support", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("Universal AI 3D Studio features a fully comprehensive native dictionary and bidirectional layout engine:", body_style))
    
    lang_data = [
        [Paragraph("<b>Language</b>", body_style), Paragraph("<b>Code</b>", body_style), Paragraph("<b>Native Script</b>", body_style), Paragraph("<b>Direction</b>", body_style)],
        [Paragraph("English", body_style), Paragraph("en", body_style), Paragraph("English", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Tamil", body_style), Paragraph("ta", body_style), Paragraph("தமிழ்", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Hindi", body_style), Paragraph("hi", body_style), Paragraph("हिन्दी", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Bengali", body_style), Paragraph("bn", body_style), Paragraph("বাংলা", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Telugu", body_style), Paragraph("te", body_style), Paragraph("తెలుగు", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Marathi", body_style), Paragraph("mr", body_style), Paragraph("मराठी", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Malayalam", body_style), Paragraph("ml", body_style), Paragraph("മലയാളം", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Urdu", body_style), Paragraph("ur", body_style), Paragraph("اردو", body_style), Paragraph("<b>RTL (Right-to-Left)</b>", body_style)],
        [Paragraph("Arabic", body_style), Paragraph("ar", body_style), Paragraph("العربية", body_style), Paragraph("<b>RTL (Right-to-Left)</b>", body_style)],
        [Paragraph("Spanish / French / German", body_style), Paragraph("es / fr / de", body_style), Paragraph("Español / Français / Deutsch", body_style), Paragraph("LTR", body_style)],
        [Paragraph("Mandarin / Japanese / Russian", body_style), Paragraph("zh / ja / ru", body_style), Paragraph("中文 / 日本語 / Русский", body_style), Paragraph("LTR", body_style)]
    ]
    lang_table = Table(lang_data, colWidths=[130, 80, 160, 130])
    lang_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(lang_table)
    story.append(Spacer(1, 14))

    # ================= SECTION 6 =================
    story.append(Paragraph("6. REST API Reference", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    
    api_items = [
        ("POST /api/v1/generate", "Generates interactive 3D scene graph & realistic render from multimodal prompt."),
        ("POST /api/v1/generate/realistic-image", "Synthesizes 8K realistic render with specified style preset."),
        ("POST /api/v1/scene/action", "Applies natural language copilot actions to modify scene objects or materials."),
        ("GET /api/v1/projects", "Lists all saved 3D projects and demo presets."),
        ("GET /api/v1/projects/{id}", "Retrieves specific project scene graph."),
        ("POST /api/v1/voice/transcribe", "Decodes audio stream and returns transcribed text."),
        ("POST /api/v1/voice/tts", "Synthesizes multilingual audio stream from text prompt."),
        ("GET /api/v1/health", "System health check returning status of Groq, Gemini, Tripo3D, and GLM.")
    ]
    for endpoint, desc in api_items:
        story.append(Paragraph(f"<b><code>{endpoint}</code></b> — {desc}", bullet_style))

    story.append(Spacer(1, 14))

    # ================= SECTION 7 =================
    story.append(Paragraph("7. Local Development & Deployment Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0"), spaceAfter=10))
    story.append(Paragraph("Step 1: Start Backend Server", h2_style))
    story.append(Paragraph("""cd "c:\\Users\\HP\\Documents\\3D AI"
$env:PYTHONPATH = "backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload""", code_style))

    story.append(Paragraph("Step 2: Start Frontend Dev Server", h2_style))
    story.append(Paragraph("""cd "c:\\Users\\HP\\Documents\\3D AI\\frontend"
npm run dev""", code_style))

    story.append(Paragraph("Open <b>http://localhost:5173</b> in your browser to access the 3D Studio.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF Successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_pdf()
