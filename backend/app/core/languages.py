"""
Universal AI 3D Studio - Central 16 Languages Configuration
Covers Indian Languages: Tamil, Hindi, Bengali, Telugu, Marathi, Malayalam, Urdu
International Languages: English, Spanish, Mandarin, Arabic, French, Portuguese, Russian, German, Japanese
Includes BCP-47 codes, RTL directions, native script names, and STT/TTS mappings.
"""

from typing import Dict, Any

SUPPORTED_LANGUAGES: Dict[str, Dict[str, Any]] = {
    "en": {
        "code": "en",
        "name": "English",
        "native_name": "English",
        "category": "International",
        "direction": "ltr",
        "stt": "en-US",
        "tts": "en-US-Standard-C",
        "greeting": "What would you like to create in 3D?"
    },
    "ta": {
        "code": "ta",
        "name": "Tamil",
        "native_name": "தமிழ்",
        "category": "Indian",
        "direction": "ltr",
        "stt": "ta-IN",
        "tts": "ta-IN-Standard-A",
        "greeting": "நீங்கள் என்ன 3D வடிவத்தை உருவாக்க விரும்புகிறீர்கள்?"
    },
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "native_name": "हिन्दी",
        "category": "Indian",
        "direction": "ltr",
        "stt": "hi-IN",
        "tts": "hi-IN-Standard-A",
        "greeting": "आप क्या 3D दृश्य बनाना चाहते हैं?"
    },
    "bn": {
        "code": "bn",
        "name": "Bengali",
        "native_name": "বাংলা",
        "category": "Indian",
        "direction": "ltr",
        "stt": "bn-IN",
        "tts": "bn-IN-Standard-A",
        "greeting": "আপনি কোন 3D মডেল তৈরি করতে চান?"
    },
    "te": {
        "code": "te",
        "name": "Telugu",
        "native_name": "తెలుగు",
        "category": "Indian",
        "direction": "ltr",
        "stt": "te-IN",
        "tts": "te-IN-Standard-A",
        "greeting": "మీరు ఏ 3D మోడల్‌ను రూపొందించాలనుకుంటున్నారు?"
    },
    "mr": {
        "code": "mr",
        "name": "Marathi",
        "native_name": "मराठी",
        "category": "Indian",
        "direction": "ltr",
        "stt": "mr-IN",
        "tts": "mr-IN-Standard-A",
        "greeting": "तुम्हाला कोणते 3D मॉडेल तयार करायचे आहे?"
    },
    "ml": {
        "code": "ml",
        "name": "Malayalam",
        "native_name": "മലയാളം",
        "category": "Indian",
        "direction": "ltr",
        "stt": "ml-IN",
        "tts": "ml-IN-Standard-A",
        "greeting": "ഏത് 3D മോഡലാണ് നിങ്ങൾ നിർമ്മിക്കാൻ ആഗ്രഹിക്കുന്നത്?"
    },
    "ur": {
        "code": "ur",
        "name": "Urdu",
        "native_name": "اردو",
        "category": "Indian",
        "direction": "rtl",
        "stt": "ur-PK",
        "tts": "ur-PK-Standard-A",
        "greeting": "آپ کون سا 3D ماڈل بنانا چاہتے ہیں؟"
    },
    "es": {
        "code": "es",
        "name": "Spanish",
        "native_name": "Español",
        "category": "International",
        "direction": "ltr",
        "stt": "es-ES",
        "tts": "es-ES-Standard-A",
        "greeting": "¿Qué te gustaría crear en 3D?"
    },
    "zh": {
        "code": "zh",
        "name": "Mandarin Chinese",
        "native_name": "中文",
        "category": "International",
        "direction": "ltr",
        "stt": "zh-CN",
        "tts": "cmn-CN-Standard-A",
        "greeting": "你想在 3D 中创建什么？"
    },
    "ar": {
        "code": "ar",
        "name": "Arabic",
        "native_name": "العربية",
        "category": "International",
        "direction": "rtl",
        "stt": "ar-XA",
        "tts": "ar-XA-Standard-A",
        "greeting": "ماذا تريد أن تصنع في نموذج ثلاثي الأبعاد؟"
    },
    "fr": {
        "code": "fr",
        "name": "French",
        "native_name": "Français",
        "category": "International",
        "direction": "ltr",
        "stt": "fr-FR",
        "tts": "fr-FR-Standard-A",
        "greeting": "Que souhaitez-vous créer en 3D ?"
    },
    "pt": {
        "code": "pt",
        "name": "Portuguese",
        "native_name": "Português",
        "category": "International",
        "direction": "ltr",
        "stt": "pt-BR",
        "tts": "pt-BR-Standard-A",
        "greeting": "O que você gostaria de criar em 3D?"
    },
    "ru": {
        "code": "ru",
        "name": "Russian",
        "native_name": "Русский",
        "category": "International",
        "direction": "ltr",
        "stt": "ru-RU",
        "tts": "ru-RU-Standard-A",
        "greeting": "Что вы хотите создать в 3D?"
    },
    "de": {
        "code": "de",
        "name": "German",
        "native_name": "Deutsch",
        "category": "International",
        "direction": "ltr",
        "stt": "de-DE",
        "tts": "de-DE-Standard-A",
        "greeting": "Was möchten Sie in 3D erstellen?"
    },
    "ja": {
        "code": "ja",
        "name": "Japanese",
        "native_name": "日本語",
        "category": "International",
        "direction": "ltr",
        "stt": "ja-JP",
        "tts": "ja-JP-Standard-A",
        "greeting": "3Dで何を作成したいですか？"
    }
}

def get_language_info(lang_code: str) -> Dict[str, Any]:
    code = lang_code.lower().split("-")[0].strip()
    return SUPPORTED_LANGUAGES.get(code, SUPPORTED_LANGUAGES["en"])
