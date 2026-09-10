import re
import urllib.parse
import logging
import base64
import random
from typing import Dict, Any, Optional
import httpx
from app.providers.groq_provider import groq_provider

logger = logging.getLogger(__name__)

class RealisticImageService:
    """
    Synthesizes ultra-realistic 8K photographic visuals using the Flux/Photoreal engine
    with cinematic prompt enhancement and studio photography directives.
    """

    STYLE_PROMPTS = {
        "photorealistic": "ultra-realistic 8K UHD photography, shot on Hasselblad H6D-100c, 50mm f/1.8 lens, pristine studio softbox lighting, ray-traced reflections, hyper-detailed textures, photoreal, masterpiece, photorealistic",
        "studio": "award-winning commercial product photography, pure dark studio backdrop, dramatic rim light, caustic reflections, glossy polished finish, 8K ultra high resolution, cinematic depth of field",
        "cinematic": "cinematic film still, 35mm Panavision anamorphic lens, golden hour volumetric lighting, atmosphere, cinematic depth of field, photorealistic, Unreal Engine 5 render style, hyper-detailed",
        "automotive": "high-end automotive magazine photoshoot, studio key light reflection along body lines, metallic flake paint clearcoat, carbon fiber weave texture, wet asphalt reflections, 8K photoreal",
        "architectural": "Architectural Digest luxury interior photography, natural daylight stream, realistic marble and hardwood grain, soft ambient shadows, ultra wide-angle architectural perspective, photoreal 8K",
        "macro": "extreme macro photography, shallow depth of field, intricate micro-textures, precision craftsmanship, razor sharp focus, 8K resolution, photoreal",
        "3d_render": "award-winning Unreal Engine 5 photorealistic 3D CGI render, octane renderer, global illumination, physically based rendering PBR materials, 8K ultra high resolution, subsurface scattering, volumetric light shafts, hyper-detailed geometry, realistic bump maps, ambient occlusion, high dynamic range HDR environment lighting, masterpiece 3D visualization",
        "product_3d": "pristine 3D product visualization render, Blender Cycles photorealistic, studio HDRI lighting, glossy reflective surfaces, exact material micro-detail, floating object on pure white gradient, sharp focus, 8K professional CGI render, commercial quality",
        "sci_fi_3d": "futuristic Sci-Fi 3D CGI cinematic render, Unreal Engine 5 Lumen lighting, holographic emissive materials, volumetric neon glow, reflective metallic surfaces, dark atmospheric environment, 8K ultra-detailed"
    }

    NEGATIVE_DIRECTIVES = "avoid cartoon, avoid anime, avoid CGI toy, avoid low-poly, avoid flat colors, avoid plastic miniature, avoid blur, avoid watermark"

    async def enhance_prompt_for_realism(self, raw_prompt: str, style: str = "photorealistic") -> str:
        """
        Uses LLM prompt enhancement or specialized photography directives to generate an ultra-realistic photographic scene description.
        """
        if not raw_prompt or len(raw_prompt.strip()) < 3:
            raw_prompt = "Futuristic aerodynamic luxury vehicle in high-tech studio"

        style_suffix = self.STYLE_PROMPTS.get(style.lower(), self.STYLE_PROMPTS["photorealistic"])

        is_3d_style = style.lower() in ("3d_render", "product_3d", "sci_fi_3d")
        try:
            if is_3d_style:
                sys_msg = (
                    "You are a world-class 3D CGI artist specializing in Unreal Engine 5 and Blender Cycles photorealistic renders. "
                    "Transform the user's prompt into a cinematic 3D CGI render prompt with hyper-detailed descriptions of: "
                    "PBR materials (metalness, roughness, subsurface scattering), global illumination setup, HDRI environment lighting, "
                    "camera angle (35mm, f/2.8 depth of field), and geometric detail level. "
                    "Emphasize: photorealistic, NOT cartoon, NOT anime, NOT low-poly. Keep it under 60 words. Output ONLY the enhanced prompt."
                )
                user_msg = f"Create a photorealistic Unreal Engine 5 CGI render prompt for: {raw_prompt}"
            else:
                sys_msg = (
                    "You are an expert Hollywood cinematic visual artist and commercial photographer. "
                    "Transform the user's prompt into an ultra-detailed, photorealistic image generation prompt. "
                    "Describe exact lighting (softbox, rim light, ambient occlusion), camera specifications (Hasselblad 50mm, f/1.8), "
                    "tangible materials (carbon fiber, brushed aluminum, leather grain, glass caustics), and cinematic composition. "
                    "Never mention cartoons, low poly, or animations. Keep it under 60 words. Output ONLY the enhanced prompt."
                )
                user_msg = f"Create a photorealistic photographic prompt for: {raw_prompt}"
            enhanced = await groq_provider.chat_completion([
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": user_msg}
            ])
            if enhanced and len(enhanced.strip()) > 15:
                # Clean any quotes or prefixes
                cleaned = re.sub(r'^(Prompt:|Enhanced:|Here is:|"|\\\')', '', enhanced.strip()).strip().rstrip('"\\\'')
                return f"{cleaned}, {style_suffix}"
        except Exception as e:
            logger.warning(f"Groq prompt enhancement fallback: {e}")

        # High-fidelity photography template fallback
        return f"Hyperrealistic 8k photo of {raw_prompt.strip()}, {style_suffix}"

    def build_realistic_image_url(
        self,
        enhanced_prompt: str,
        width: int = 1280,
        height: int = 720,
        seed: Optional[int] = None
    ) -> str:
        """
        Builds a direct URL to the Flux Photoreal rendering engine.
        """
        if seed is None:
            seed = random.randint(10000, 999999)

        # Truncate to avoid URL length constraints while preserving key visual tokens
        prompt_segment = enhanced_prompt[:350]
        encoded = urllib.parse.quote(prompt_segment)
        return f"https://image.pollinations.ai/prompt/{encoded}?width={width}&height={height}&model=flux&nologo=true&seed={seed}"

    async def generate_realistic_image(
        self,
        prompt: str,
        style: str = "photorealistic",
        width: int = 1280,
        height: int = 720,
        seed: Optional[int] = None,
        fetch_base64: bool = False
    ) -> Dict[str, Any]:
        """
        Generates an ultra-realistic photographic image and returns metadata, enhanced prompt,
        and optionally Base64 data.
        """
        enhanced_prompt = await self.enhance_prompt_for_realism(prompt, style)
        image_url = self.build_realistic_image_url(enhanced_prompt, width, height, seed)

        image_b64 = None
        if fetch_base64:
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                async with httpx.AsyncClient(timeout=25.0) as client:
                    resp = await client.get(image_url, headers=headers)
                    if resp.status_code == 200 and resp.content:
                        image_b64 = f"data:image/jpeg;base64,{base64.b64encode(resp.content).decode('utf-8')}"
            except Exception as e:
                logger.warning(f"Failed to fetch image base64: {e}")

        return {
            "success": True,
            "image_url": image_url,
            "enhanced_prompt": enhanced_prompt,
            "style": style,
            "image_base64": image_b64
        }

realistic_image_service = RealisticImageService()
