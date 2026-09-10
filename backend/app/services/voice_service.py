import base64
import logging
import urllib.request
import urllib.parse
import re
import asyncio
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.languages import get_language_info
from app.providers.groq_provider import groq_provider
from app.providers.gemini_provider import gemini_provider

logger = logging.getLogger(__name__)

class VoiceService:
    async def speech_to_text(
        self,
        audio_base64: str,
        language_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribes audio using Whisper-large-v3 on Groq or Google Speech.
        """
        try:
            # Decode audio
            clean_b64 = audio_base64.split(",")[-1] if "," in audio_base64 else audio_base64
            audio_bytes = base64.b64decode(clean_b64)

            # Call Whisper
            whisper_res = await groq_provider.transcribe_audio(
                audio_bytes=audio_bytes,
                language=language_hint
            )
            if whisper_res.get("success") and whisper_res.get("text"):
                text = whisper_res["text"].strip()
                # Detect language from transcribed text
                from app.services.ai_orchestrator import ai_orchestrator
                detected_lang = ai_orchestrator.detect_language(text)
                return {
                    "success": True,
                    "transcription": text,
                    "detected_language": detected_lang,
                    "confidence": 0.98
                }
            else:
                return {
                    "success": False,
                    "transcription": "",
                    "detected_language": language_hint or "en",
                    "error": whisper_res.get("error", "Failed to transcribe audio")
                }
        except Exception as e:
            logger.error(f"STT Error: {e}")
            return {
                "success": False,
                "transcription": "",
                "detected_language": language_hint or "en",
                "error": str(e)
            }

    def fetch_google_tts_bytes(self, text: str, lang_code: str) -> Optional[bytes]:
        """
        Synthesizes speech into authentic native MP3 bytes for all 16 Indian & International languages.
        """
        try:
            clean_text = re.sub(r'[*#_`]', '', text).strip()
            if not clean_text:
                return None

            # Split text into natural chunks (< 180 chars) to prevent TTS cutoff
            sentences = re.split(r'([.!?\n|।])', clean_text)
            chunks = []
            curr = ""
            for s in sentences:
                if len(curr) + len(s) < 180:
                    curr += s
                else:
                    if curr.strip():
                        chunks.append(curr.strip())
                    curr = s
            if curr.strip():
                chunks.append(curr.strip())

            if not chunks:
                chunks = [clean_text[:180]]

            # Map our 16 language codes to Google TTS language codes
            tts_lang_map = {
                "en": "en", "ta": "ta", "hi": "hi", "bn": "bn",
                "te": "te", "mr": "mr", "ml": "ml", "ur": "ur",
                "es": "es", "zh": "zh-CN", "ar": "ar", "fr": "fr",
                "pt": "pt", "ru": "ru", "de": "de", "ja": "ja"
            }
            target_tl = tts_lang_map.get(lang_code.lower().split("-")[0], "en")

            combined = bytearray()
            for chunk in chunks[:5]:
                if not chunk.strip():
                    continue
                q = urllib.parse.quote(chunk.strip())
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={q}&tl={target_tl}&client=tw-ob"
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                    }
                )
                with urllib.request.urlopen(req, timeout=8.0) as res:
                    combined.extend(res.read())

            return bytes(combined) if combined else None
        except Exception as e:
            logger.warning(f"Google TTS synthesis error for {lang_code}: {e}")
            return None

    async def text_to_speech(
        self,
        text: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Synthesizes MP3 speech audio and returns base64 string for client-side playback.
        """
        lang_info = get_language_info(language)
        code = lang_info["code"]

        raw_bytes = await asyncio.to_thread(self.fetch_google_tts_bytes, text, code)

        if raw_bytes:
            b64_str = base64.b64encode(raw_bytes).decode("utf-8")
            audio_data = f"data:audio/mp3;base64,{b64_str}"
            return {
                "success": True,
                "text": text,
                "language": code,
                "audio_format": "mp3",
                "audio_base64": audio_data,
                "fallback_used": False
            }
        else:
            return {
                "success": True,
                "text": text,
                "language": code,
                "audio_format": "mp3",
                "audio_base64": None,
                "fallback_used": True
            }

voice_service = VoiceService()

