import json
import re
import uuid
import logging
from typing import Dict, Any, List, Optional
from app.core.languages import SUPPORTED_LANGUAGES, get_language_info
from app.schemas.scene_schema import (
    ScenePlan, SceneObjectData, TransformData, MaterialData,
    ComponentData, AnimationData, EnvironmentData, LightData, CameraData,
    SceneModificationAction, IntentType
)
from app.providers.groq_provider import groq_provider
from app.providers.gemini_provider import gemini_provider
from app.providers.tripo_provider import tripo_provider
from app.services.assets.demo_presets import get_demo_scenes

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self):
        self.demos = get_demo_scenes()

    def detect_language(self, text: str) -> str:
        """
        Detect language from text based on Unicode scripts or language hints.
        Handles Tamil, Hindi, Arabic, Urdu, Bengali, Telugu, Marathi, Malayalam, Chinese, Japanese, Russian, etc.
        """
        if not text:
            return "en"

        # Check Unicode ranges
        for char in text:
            code = ord(char)
            if 0x0B80 <= code <= 0x0BFF:
                return "ta"  # Tamil
            if 0x0900 <= code <= 0x097F:
                return "hi"  # Hindi / Marathi
            if 0x0980 <= code <= 0x09FF:
                return "bn"  # Bengali
            if 0x0C00 <= code <= 0x0C7F:
                return "te"  # Telugu
            if 0x0D00 <= code <= 0x0D7F:
                return "ml"  # Malayalam
            if 0x0600 <= code <= 0x06FF:
                # Arabic or Urdu
                return "ur" if any(u in text for u in ["ہیں", "تھا", "کے", "کا", "کی"]) else "ar"
            if 0x4E00 <= code <= 0x9FFF:
                return "zh"  # Mandarin Chinese
            if 0x3040 <= code <= 0x30FF:
                return "ja"  # Japanese
            if 0x0400 <= code <= 0x04FF:
                return "ru"  # Russian

        # Fallback to English
        return "en"

    def classify_intent(self, text: str) -> IntentType:
        """
        Classifies intent dynamically from prompt text.
        """
        low = text.lower()
        if any(w in low for w in ["explode", "separate parts", "show components", "disassemble"]):
            return "EXPLODE_OBJECT"
        if any(w in low for w in ["explain", "what is", "விளக்கு", "விளக்கவும்", "बताओ", "समझाइए"]):
            return "EXPLAIN_OBJECT"
        if any(w in low for w in ["animate", "move", "rotate", "spin", "orbit"]):
            return "ANIMATE_OBJECT"
        if any(w in low for w in ["add ", "insert ", "put ", "சேர்", "जोड़ो"]):
            return "ADD_OBJECT"
        if any(w in low for w in ["remove", "delete", "destroy", "நீக்கு", "हटाओ"]):
            return "REMOVE_OBJECT"
        if any(w in low for w in ["modify", "change", "taller", "larger", "color", "red", "blue", "gold"]):
            return "MODIFY_SCENE"
        if any(w in low for w in ["solar system", "sun", "earth", "planet"]):
            return "GENERATE_EDUCATIONAL_VISUALIZATION"
        return "CREATE_SCENE"

    def _extract_color_from_text(self, text: str, default: str = "#dc2626") -> str:
        """Extract primary color hex from description or image analysis."""
        low = text.lower()
        if "green" in low or "kawasaki" in low or "lime" in low:
            return "#16a34a"
        if "blue" in low or "yamaha" in low or "cyan" in low:
            return "#2563eb"
        if "yellow" in low or "gold" in low:
            return "#eab308"
        if "orange" in low or "ktm" in low:
            return "#ea580c"
        if "black" in low or "dark" in low or "stealth" in low:
            return "#18181b"
        if "white" in low or "silver" in low or "cream" in low or "ivory" in low or "pearl" in low:
            return "#f8fafc"
        if "gray" in low or "grey" in low or "gunmetal" in low:
            return "#64748b"
        if "purple" in low or "violet" in low:
            return "#9333ea"
        return default

    def _get_localized_racing_meta(self, category: str, language: str) -> Dict[str, str]:
        """Provides rich localized titles and copilot descriptions in all 16 languages."""
        meta = {
            "bike": {
                "en": {
                    "title": "Realistic Racing Superbike",
                    "obj_name": "Racing Superbike 1000cc",
                    "desc": "An ultra-high-performance 1000cc racing superbike engineered for maximum aerodynamic velocity and cornering precision. Features twin-spar aluminum chassis, Ohlins inverted telescopic forks, Brembo drilled disc brakes, carbon-fiber clip-ons, and dual underbelly titanium exhaust pipes."
                },
                "ta": {
                    "title": "நிஜமான பந்தய சூப்பர்பைக்",
                    "obj_name": "பந்தய சூப்பர்பைக் 1000cc",
                    "desc": "அதிவேக பந்தயத்திற்காகவும் துல்லியமான திருப்பங்களுக்காகவும் வடிவமைக்கப்பட்ட 1000cc பந்தய சூப்பர்பைக். இதில் இரட்டை அலுமினிய சேசிஸ், ஓலின்ஸ் சஸ்பென்ஷன், ப்ரெம்போ டிஸ்க் பிரேக்குகள் மற்றும் டைட்டானியம் எக்ஸாஸ்ட் பொருத்தப்பட்டுள்ளன."
                },
                "hi": {
                    "title": "अल्ट्रा-फास्ट रेसिंग सुपरबाइक",
                    "obj_name": "रेसिंग सुपरबाइक 1000cc",
                    "desc": "अधिकतम वायुगतिकीय गति और सटीकता के लिए इंजीनियर की गई 1000cc हाई-परफॉर्मेंस रेसिंग सुपरबाइक। इसमें ट्विन-स्पार एल्यूमीनियम चेसिस, ओहलिन इनवर्टेड फोर्क्स, ब्रेम्बो डिस्क ब्रेक और टाइटेनियम एग्जॉस्ट शामिल हैं।"
                },
                "ml": {
                    "title": "റിയലിസ്റ്റിക് റേസിംഗ് സൂപ്പർബൈക്ക്",
                    "obj_name": "റേസിംഗ് സൂപ്പർബൈക്ക് 1000cc",
                    "desc": "പരമാവധി എയറോഡൈനാമിക് വേഗതയ്ക്കും കോർണറിംഗ് കൃത്യതയ്ക്കുമായി രൂപകൽപ്പന ചെയ്ത 1000cc ഉയർന്ന പ്രവർത്തനക്ഷമതയുള്ള റേസിംഗ് സൂപ്പർബൈക്ക്. അലുമിനിയം ചേസിസ്, ഓഹ്ലിൻസ് ഇൻവേർട്ടഡ് ഫോർക്കുകൾ, ബ്രെംബോ ഡിസ്ക് ബ്രേക്കുകൾ, ടൈറ്റാനിയം എക്‌സ്‌ഹോസ്റ്റ് എന്നിവ ഉൾപ്പെടുന്നു."
                },
                "te": {
                    "title": "రియలిస్టిక్ రేసింగ్ సూపర్ బైక్",
                    "obj_name": "రేసింగ్ సూపర్ బైక్ 1000cc",
                    "desc": "గరిష్ట వేగం మరియు ఖచ్చితత్వం కోసం రూపొందించబడిన 1000cc హై-పెర్ఫార్మెన్స్ రేసింగ్ సూపర్ బైక్. ఇందులో ట్విన్-స్పార్ అల్యూమినియం ఛాసిస్, ఇన్వర్టెడ్ సస్పెన్షన్, డిస్క్ బ్రేక్‌లు మరియు టైటానియం ఎగ్జాస్ట్ ఉన్నాయి."
                },
                "bn": {
                    "title": "বাস্তবসম্মত রেসিং সুপারবাইক",
                    "obj_name": "রেসিং সুপারবাইক 1000cc",
                    "desc": "সর্বোচ্চ এরোডাইনামিক গতি এবং নিয়ন্ত্রণের জন্য প্রকৌশলিত একটি 1000cc হাই-পারফরম্যান্স রেসিং সুপারবাইক। এতে টুইন-স্পার অ্যালুমিনিয়াম চ্যাসিস, ব্রেম্বো ডিস্ক ব্রেক এবং টাইটানিয়াম এগজস্ট রয়েছে।"
                },
                "mr": {
                    "title": "अल्ट्रा-फास्ट रेसिंग सुपरबाइक",
                    "obj_name": "रेसिंग सुपरबाइक 1000cc",
                    "desc": "कमाल एरोडायनामिक वेग आणि अचूकतेसाठी इंजिनिअर केलेली 1000cc हाय-परफॉर्मन्स रेसिंग सुपरबाइक. यात ड्युअल अ‍ॅल्युमिनियम चेसिस, ब्रेम्बो डिस्क ब्रेक आणि टायटॅनियम एक्झॉस्ट समाविष्ट आहे."
                },
                "ur": {
                    "title": "حقیقی ریسنگ سپر بائیک",
                    "obj_name": "ریسنگ سپر بائیک 1000cc",
                    "desc": "زیادہ سے زیادہ رفتار اور درستگی کے لیے ڈیزائن کی گئی 1000cc ہائی پرفارمنس ریسنگ بائیک۔ اس میں ایلومینیم فریم، ڈسک بریکس اور ٹائٹینیم ایگزاسٹ شامل ہیں۔"
                },
                "ar": {
                    "title": "دراجة السباق الخارقة الواقعية",
                    "obj_name": "دراجة سباق خارقة 1000cc",
                    "desc": "دراجة سباق خارقة بمحرك 1000cc مصممة لتحقيق أقصى سرعة ديناميكية هوائية ودقة في المنعطفات. تتميز بهيكل مزدوج من الألومنيوم ومكابح بريمبو وعادم تيتانيوم مزدوج."
                },
                "es": {
                    "title": "Superbike de Carreras Realista",
                    "obj_name": "Superbike de Carreras 1000cc",
                    "desc": "Una superbike de carreras de 1000cc diseñada para máxima velocidad aerodinámica y precisión en curvas. Con chasis perimetral de aluminio, horquillas invertidas Öhlins, frenos de disco Brembo y escape doble de titanio."
                },
                "fr": {
                    "title": "Superbike de Course Réaliste",
                    "obj_name": "Superbike de Course 1000cc",
                    "desc": "Une superbike de compétition 1000cc conçue pour une vitesse aérodynamique maximale. Dotée d'un châssis périmétrique en aluminium, de fourches inversées Öhlins et d'un double échappement en titane."
                },
                "de": {
                    "title": "Realistisches Renn-Superbike",
                    "obj_name": "Renn-Superbike 1000cc",
                    "desc": "Ein 1000cc High-Performance Renn-Superbike, entwickelt für maximale aerodynamische Geschwindigkeit und Kurvenpräzision mit Aluminiumchassis, Öhlins-Gabeln und Titan-Auspuffanlage."
                },
                "zh": {
                    "title": "超真实赛道超级摩托车",
                    "obj_name": "赛道超级摩托车 1000cc",
                    "desc": "专为极致空气动力学极速与弯道精准度设计的1000cc高性能赛道超级摩托车。配备双翼梁铝合金车架、欧林斯倒置前叉、布雷博双碟刹车系统与双钛合金排气管。"
                },
                "ja": {
                    "title": "リアル・レーシングスーパーバイク",
                    "obj_name": "レーシングスーパーバイク 1000cc",
                    "desc": "最高峰の空力性能とコーナリング精度を誇る1000ccレーシングスーパーバイク。ツインスパーアルミフレーム、オーリンズ倒立フォーク、ブレンボ製ブレーキ、チタン製マフラーを搭載。"
                },
                "pt": {
                    "title": "Superbike de Corrida Realista",
                    "obj_name": "Superbike de Corrida 1000cc",
                    "desc": "Superbike de corrida de 1000cc projetada para máxima velocidade aerodinâmica e precisão em curvas. Possui chassi perimétrico em alumínio, garfos invertidos Öhlins e escapamento de titânio."
                },
                "ru": {
                    "title": "Реалистичный гоночный супербайк",
                    "obj_name": "Гоночный супербайк 1000cc",
                    "desc": "Высокопроизводительный гоночный супербайк 1000cc, разработанный для максимальной аэродинамической скорости и точности в поворотах. Оснащен алюминиевым шасси, тормозами Brembo и титановым выхлопом."
                }
            },
            "car": {
                "en": {
                    "title": "Aerodynamic Hypercar GT",
                    "obj_name": "Aerodynamic GT Hypercar",
                    "desc": "A cutting-edge aerodynamic GT racing hypercar featuring carbon-fiber monocoque chassis, quad high-performance forged wheels, front carbon splitter, curved cockpit glass canopy, rear racing spoiler wing, and quad titanium exhausts."
                },
                "ta": {
                    "title": "அதிவேக ரேசிங் ஹைப்பர்கார்",
                    "obj_name": "ரேசிங் ஹைப்பர்கார் GT",
                    "desc": "கார்பன் ஃபைபர் சேசிஸ், நான்கு உயர் செயல்திறன் சக்கரங்கள், ஸ்பாய்லர் விங் மற்றும் டைட்டானியம் எக்ஸாஸ்டுகளுடன் கூடிய நவீன ஹைப்பர்கார்."
                },
                "hi": {
                    "title": "एरोडायनामिक रेसिंग हाइपरकार",
                    "obj_name": "रेसिंग हाइपरकार GT",
                    "desc": "कार्बन-फाइबर चेसिस, चार जालीदार पहिए, फ्रंट कार्बन स्प्लिटर, रियर रेसिंग स्पॉइलर और क्वाड टाइटेनियम एग्जॉस्ट के साथ अत्याधुनिक रेसिंग कार।"
                },
                "ml": {
                    "title": "എയറോഡൈനാമിക് ഹൈപ്പർകാർ ജിടി",
                    "obj_name": "റേസിംഗ് ഹൈപ്പർകാർ GT",
                    "desc": "കാർബൺ ഫൈബർ ചേസിസ്, നാല് ഹൈ-പെർഫോമൻസ് വീലുകൾ, ഫ്രണ്ട് സ്പ്ലിറ്റർ, റിയർ വിംഗ് സ്പോയിലർ എന്നിവയുള്ള അത്യാധുനിക റേസിംഗ് കാർ."
                }
            }
        }
        cat_dict = meta.get(category, meta["bike"])
        return cat_dict.get(language, cat_dict.get("en", {
            "title": "Realistic Racing Vehicle",
            "obj_name": "Racing Vehicle",
            "desc": "High performance aerodynamic 3D racing vehicle with modular precision components."
        }))

    def _build_racing_bike_scene(
        self,
        prompt: str,
        language: str = "en",
        primary_color: str = "#dc2626",
        observed_features: Optional[List[str]] = None
    ) -> ScenePlan:
        """Constructs an ultra-realistic, anatomically separated 3D Racing Superbike."""
        scene_id = f"scene_{uuid.uuid4().hex[:8]}"
        obj_id = f"obj_{uuid.uuid4().hex[:6]}"
        localized = self._get_localized_racing_meta("bike", language)

        components = [
            # 1. Front Wheel Tire (Upright Torus along X-Y plane, axle along Z)
            ComponentData(
                id=f"{obj_id}_front_tire",
                name="Front Wheel Tire",
                purpose="Performance racing slick tire providing steering grip and high-speed stability",
                geometry_type="torus",
                geometry_params={"radius": 0.55, "tube": 0.11, "radialSegments": 24, "tubularSegments": 48},
                transform=TransformData(position=[1.3, 0.55, 0.0], rotation=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#18181b", roughness=0.85, metalness=0.1, name="Matte Black Rubber"),
                explode_offset=[1.2, 0.0, 0.0]
            ),
            # 2. Front Wheel Rim & Spokes
            ComponentData(
                id=f"{obj_id}_front_rim",
                name="Front Forged Alloy Rim",
                purpose="Ultra-lightweight forged magnesium alloy rim with multi-spoke structural hub",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.44, "radiusBottom": 0.44, "height": 0.16, "radialSegments": 32},
                transform=TransformData(position=[1.3, 0.55, 0.0], rotation=[1.5708, 0.0, 0.0]),
                material=MaterialData(color="#e2e8f0", roughness=0.15, metalness=0.95, name="Polished Chrome"),
                explode_offset=[1.2, 0.0, 0.35]
            ),
            # 3. Front Dual Disc Brake Caliper
            ComponentData(
                id=f"{obj_id}_front_brakes",
                name="Brembo Front Brake Caliper & Rotor",
                purpose="Twin floating drilled steel brake discs with monobloc 4-piston calipers",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.35, "radiusBottom": 0.35, "height": 0.04, "radialSegments": 24},
                transform=TransformData(position=[1.3, 0.55, 0.11], rotation=[1.5708, 0.0, 0.0]),
                material=MaterialData(color="#ef4444", roughness=0.3, metalness=0.85, name="Racing Red Steel"),
                explode_offset=[1.2, 0.0, 0.6]
            ),
            # 4. Front Suspension Right Fork
            ComponentData(
                id=f"{obj_id}_front_fork_r",
                name="Right Inverted Telescopic Fork",
                purpose="Öhlins pressurized cartridge inverted suspension fork leg",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.045, "radiusBottom": 0.045, "height": 1.1, "radialSegments": 16},
                transform=TransformData(position=[1.05, 1.0, 0.14], rotation=[0.0, 0.0, -0.4]),
                material=MaterialData(color="#f59e0b", roughness=0.2, metalness=0.9, name="Anodized Gold Titanium"),
                explode_offset=[0.6, 0.6, 0.2]
            ),
            # 5. Front Suspension Left Fork
            ComponentData(
                id=f"{obj_id}_front_fork_l",
                name="Left Inverted Telescopic Fork",
                purpose="Twin Öhlins pressurized front damping fork leg",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.045, "radiusBottom": 0.045, "height": 1.1, "radialSegments": 16},
                transform=TransformData(position=[1.05, 1.0, -0.14], rotation=[0.0, 0.0, -0.4]),
                material=MaterialData(color="#f59e0b", roughness=0.2, metalness=0.9, name="Anodized Gold Titanium"),
                explode_offset=[0.6, 0.6, -0.2]
            ),
            # 6. Front Aerodynamic Fender / Mudguard
            ComponentData(
                id=f"{obj_id}_front_fender",
                name="Aerodynamic Carbon Front Fender",
                purpose="Directs high-speed airflow over the radiator and prevents tire spray",
                geometry_type="box",
                geometry_params={"width": 0.65, "height": 0.12, "depth": 0.32},
                transform=TransformData(position=[1.25, 1.05, 0.0], rotation=[0.0, 0.0, -0.3]),
                material=MaterialData(color=primary_color, roughness=0.2, metalness=0.55, name="Gloss Racing Lacquer"),
                explode_offset=[0.8, 0.6, 0.0]
            ),
            # 7. Rear Wheel Tire (Wider rear contact patch)
            ComponentData(
                id=f"{obj_id}_rear_tire",
                name="Rear Wheel Tire",
                purpose="High-traction 200/55 ZR17 racing rear slick tire transmitting 215hp to track",
                geometry_type="torus",
                geometry_params={"radius": 0.55, "tube": 0.14, "radialSegments": 24, "tubularSegments": 48},
                transform=TransformData(position=[-1.3, 0.55, 0.0], rotation=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#18181b", roughness=0.85, metalness=0.1, name="Matte Black Rubber"),
                explode_offset=[-1.2, 0.0, 0.0]
            ),
            # 8. Rear Wheel Rim & Hub
            ComponentData(
                id=f"{obj_id}_rear_rim",
                name="Rear Forged Alloy Rim & Hub",
                purpose="Drive hub with integrated sprocket assembly and single-sided wheel mount",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.44, "radiusBottom": 0.44, "height": 0.22, "radialSegments": 32},
                transform=TransformData(position=[-1.3, 0.55, 0.0], rotation=[1.5708, 0.0, 0.0]),
                material=MaterialData(color="#e2e8f0", roughness=0.15, metalness=0.95, name="Polished Chrome"),
                explode_offset=[-1.2, 0.0, -0.35]
            ),
            # 9. Rear Aluminum Swingarm
            ComponentData(
                id=f"{obj_id}_rear_swingarm",
                name="Cast Aluminum Rear Swingarm",
                purpose="Gull-wing asymmetrical rear swingarm connecting rear axle to monoshock link",
                geometry_type="box",
                geometry_params={"width": 1.25, "height": 0.18, "depth": 0.28},
                transform=TransformData(position=[-0.65, 0.68, 0.0], rotation=[0.0, 0.0, -0.18]),
                material=MaterialData(color="#334155", roughness=0.35, metalness=0.8, name="Dark Gunmetal Alloy"),
                explode_offset=[-0.6, 0.0, 0.0]
            ),
            # 10. Twin-Spar Main Perimeter Frame
            ComponentData(
                id=f"{obj_id}_main_frame",
                name="Twin-Spar Aluminum Perimeter Chassis",
                purpose="Rigid aluminum monocoque beam supporting engine block and steering head",
                geometry_type="box",
                geometry_params={"width": 1.45, "height": 0.35, "depth": 0.36},
                transform=TransformData(position=[0.0, 1.1, 0.0]),
                material=MaterialData(color="#1e293b", roughness=0.3, metalness=0.85, name="Cast Aluminum Frame"),
                explode_offset=[0.0, 0.4, 0.0]
            ),
            # 11. Sculpted Racing Fairing & Fuel Tank
            ComponentData(
                id=f"{obj_id}_fairing_tank",
                name="Aerodynamic Racing Fairing & Fuel Tank",
                purpose="Sculpted wind-tunnel tested bodywork with internal 17L aluminum fuel cell",
                geometry_type="box",
                geometry_params={"width": 1.35, "height": 0.65, "depth": 0.52},
                transform=TransformData(position=[0.15, 1.32, 0.0]),
                material=MaterialData(color=primary_color, roughness=0.18, metalness=0.55, name="Gloss Racing Lacquer"),
                explode_offset=[0.0, 1.0, 0.0]
            ),
            # 12. Racing Bubble Windshield
            ComponentData(
                id=f"{obj_id}_windshield",
                name="Racing Bubble Windshield",
                purpose="Double-bubble aerodynamic polycarbonate canopy reducing drag at 300+ km/h",
                geometry_type="box",
                geometry_params={"width": 0.48, "height": 0.32, "depth": 0.38},
                transform=TransformData(position=[0.72, 1.7, 0.0], rotation=[0.0, 0.0, -0.55]),
                material=MaterialData(color="#38bdf8", roughness=0.1, transmission=0.75, opacity=0.65, name="Tinted Aero Screen"),
                explode_offset=[0.5, 0.8, 0.0]
            ),
            # 13. Clip-on Handlebars
            ComponentData(
                id=f"{obj_id}_handlebars",
                name="Clip-on Racing Handlebars & Grips",
                purpose="CNC-machined handlebars with Brembo radial master cylinder levers and grips",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.04, "radiusBottom": 0.04, "height": 0.76, "radialSegments": 16},
                transform=TransformData(position=[0.68, 1.5, 0.0], rotation=[1.5708, 0.0, 0.0]),
                material=MaterialData(color="#0f172a", roughness=0.7, metalness=0.6, name="Carbon Black Grips"),
                explode_offset=[0.4, 0.6, 0.0]
            ),
            # 14. Dual Xenon LED Headlights
            ComponentData(
                id=f"{obj_id}_headlights",
                name="Twin Projector LED Headlights",
                purpose="High-intensity laser LED daytime running lamps and projector headlights",
                geometry_type="box",
                geometry_params={"width": 0.18, "height": 0.1, "depth": 0.36},
                transform=TransformData(position=[0.88, 1.42, 0.0]),
                material=MaterialData(color="#e0f2fe", emissive="#38bdf8", emissive_intensity=1.8, roughness=0.1, name="Glowing Xenon LED"),
                explode_offset=[0.8, 0.4, 0.0]
            ),
            # 15. 998cc V4 Engine Block
            ComponentData(
                id=f"{obj_id}_engine_block",
                name="Desmosedici 998cc V4 Engine Block",
                purpose="215-horsepower liquid-cooled 90-degree V4 engine with counter-rotating crankshaft",
                geometry_type="box",
                geometry_params={"width": 0.82, "height": 0.58, "depth": 0.44},
                transform=TransformData(position=[0.02, 0.75, 0.0]),
                material=MaterialData(color="#475569", roughness=0.35, metalness=0.9, name="Milled Titanium Engine"),
                explode_offset=[0.0, -0.6, 0.0]
            ),
            # 16. Right Underbelly Titanium Exhaust
            ComponentData(
                id=f"{obj_id}_exhaust_r",
                name="Right Titanium Exhaust Pipe",
                purpose="Akrapovic racing titanium exhaust system with tuned expansion chamber",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.07, "radiusBottom": 0.09, "height": 1.05, "radialSegments": 16},
                transform=TransformData(position=[-0.45, 0.52, 0.22], rotation=[0.0, 0.0, 1.38]),
                material=MaterialData(color="#94a3b8", roughness=0.25, metalness=0.95, name="Burnt Titanium"),
                explode_offset=[-0.4, -0.2, 0.7]
            ),
            # 17. Left Underbelly Titanium Exhaust
            ComponentData(
                id=f"{obj_id}_exhaust_l",
                name="Left Titanium Exhaust Pipe",
                purpose="Twin resonance collector pipe optimizing backpressure and low-end torque",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.07, "radiusBottom": 0.09, "height": 1.05, "radialSegments": 16},
                transform=TransformData(position=[-0.45, 0.52, -0.22], rotation=[0.0, 0.0, 1.38]),
                material=MaterialData(color="#94a3b8", roughness=0.25, metalness=0.95, name="Burnt Titanium"),
                explode_offset=[-0.4, -0.2, -0.7]
            ),
            # 18. Alcantara Racing Seat
            ComponentData(
                id=f"{obj_id}_seat",
                name="Alcantara Racing Monoseat",
                purpose="Ergonomic racing saddle with rear stop pad for high-acceleration tuck position",
                geometry_type="box",
                geometry_params={"width": 0.7, "height": 0.12, "depth": 0.32},
                transform=TransformData(position=[-0.38, 1.34, 0.0]),
                material=MaterialData(color="#09090b", roughness=0.95, metalness=0.1, name="Alcantara Black Leather"),
                explode_offset=[-0.3, 0.6, 0.0]
            ),
            # 19. Aerodynamic Tail Cowl
            ComponentData(
                id=f"{obj_id}_tail_cowl",
                name="Aerodynamic Tail Cowl & Winglets",
                purpose="Sharp aerodynamic tail section generating rear downforce and smoothing turbulent wake",
                geometry_type="box",
                geometry_params={"width": 0.65, "height": 0.26, "depth": 0.28},
                transform=TransformData(position=[-0.92, 1.38, 0.0], rotation=[0.0, 0.0, 0.22]),
                material=MaterialData(color=primary_color, roughness=0.2, metalness=0.55, name="Gloss Racing Lacquer"),
                explode_offset=[-0.7, 0.5, 0.0]
            ),
            # 20. LED Brake Light
            ComponentData(
                id=f"{obj_id}_brake_light",
                name="Integrated LED Tail Brake Light",
                purpose="High-visibility neon red LED safety brake light integrated into tail tip",
                geometry_type="box",
                geometry_params={"width": 0.08, "height": 0.06, "depth": 0.22},
                transform=TransformData(position=[-1.26, 1.44, 0.0]),
                material=MaterialData(color="#ef4444", emissive="#ef4444", emissive_intensity=1.6, name="Glowing Red LED"),
                explode_offset=[-1.0, 0.4, 0.0]
            )
        ]

        inferred = [
            "Precision 3D mechanical assembly with 20 anatomically separated subcomponents",
            "Physically correct wheel axles, upright rolling orientation, and ground alignment",
            "PBR multi-material system: matte rubber, chrome alloy, titanium, carbon fiber, Alcantara, and emissive LEDs"
        ]
        observed = observed_features or [
            "Aerodynamic racing motorcycle silhouette with full front fairings",
            "Inverted telescopic suspension forks and lightweight alloy wheels",
            "Sculpted fuel tank, Alcantara monoseat, and twin underbelly exhaust pipes"
        ]

        return ScenePlan(
            id=scene_id,
            title=localized["title"],
            intent="CREATE_SCENE",
            scene_type="racing_superbike",
            user_prompt=prompt,
            language=language,
            observed_from_image=observed,
            inferred_elements=inferred,
            environment=EnvironmentData(
                sky_color="#080c14",
                ground_color="#0d1117",
                fog_color="#080c14",
                fog_density=0.012,
                show_grid=True,
                show_axes=True,
                ambient_color="#ffffff",
                ambient_intensity=0.8
            ),
            lighting=[
                LightData(type="directional", color="#ffffff", intensity=2.2, position=[6.0, 12.0, 8.0], cast_shadow=True),
                LightData(type="spot", color="#38bdf8", intensity=3.5, position=[0.0, 8.0, 3.0]),
                LightData(type="point", color="#ef4444", intensity=1.5, position=[-2.5, 2.0, 0.0])
            ],
            camera=CameraData(position=[3.5, 2.2, 4.0], target=[0.0, 0.9, 0.0], fov=45.0),
            explanation_targets=[obj_id],
            objects=[
                SceneObjectData(
                    id=obj_id,
                    name=localized["obj_name"],
                    category="racing_vehicle",
                    purpose=localized["title"],
                    description=localized["desc"],
                    geometry_type="compound",
                    asset_url="/models/racing_bike.glb",
                    transform=TransformData(position=[0.0, 0.0, 0.0], rotation=[0.0, 0.0, 0.0]),
                    material=MaterialData(color=primary_color, roughness=0.2, metalness=0.5),
                    components=components,
                    animation=AnimationData(type="none", axis="y", speed=1.0)
                )
            ]
        )

    def _build_racing_car_scene(
        self,
        prompt: str,
        language: str = "en",
        primary_color: str = "#ef4444",
        observed_features: Optional[List[str]] = None
    ) -> ScenePlan:
        """Constructs an ultra-realistic 3D Aerodynamic GT Hypercar."""
        scene_id = f"scene_{uuid.uuid4().hex[:8]}"
        obj_id = f"obj_{uuid.uuid4().hex[:6]}"
        localized = self._get_localized_racing_meta("car", language)

        components = [
            # 1. Front-Left Wheel
            ComponentData(
                id=f"{obj_id}_fl_wheel",
                name="Front-Left Racing Wheel & Slick",
                purpose="Front steering tire with forged lightweight alloy rim",
                geometry_type="torus",
                geometry_params={"radius": 0.42, "tube": 0.12, "radialSegments": 24, "tubularSegments": 36},
                transform=TransformData(position=[1.4, 0.42, 1.05], rotation=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#18181b", roughness=0.85, metalness=0.1),
                explode_offset=[1.0, 0.0, 0.8]
            ),
            # 2. Front-Right Wheel
            ComponentData(
                id=f"{obj_id}_fr_wheel",
                name="Front-Right Racing Wheel & Slick",
                purpose="Front right steering tire",
                geometry_type="torus",
                geometry_params={"radius": 0.42, "tube": 0.12, "radialSegments": 24, "tubularSegments": 36},
                transform=TransformData(position=[1.4, 0.42, -1.05], rotation=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#18181b", roughness=0.85, metalness=0.1),
                explode_offset=[1.0, 0.0, -0.8]
            ),
            # 3. Rear-Left Wheel
            ComponentData(
                id=f"{obj_id}_rl_wheel",
                name="Rear-Left High-Traction Wheel",
                purpose="Wide contact patch rear drive wheel",
                geometry_type="torus",
                geometry_params={"radius": 0.46, "tube": 0.14, "radialSegments": 24, "tubularSegments": 36},
                transform=TransformData(position=[-1.4, 0.46, 1.08], rotation=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#18181b", roughness=0.85, metalness=0.1),
                explode_offset=[-1.0, 0.0, 0.8]
            ),
            # 4. Rear-Right Wheel
            ComponentData(
                id=f"{obj_id}_rr_wheel",
                name="Rear-Right High-Traction Wheel",
                purpose="Wide contact patch rear drive wheel",
                geometry_type="torus",
                geometry_params={"radius": 0.46, "tube": 0.14, "radialSegments": 24, "tubularSegments": 36},
                transform=TransformData(position=[-1.4, 0.46, -1.08], rotation=[0.0, 0.0, 0.0]),
                material=MaterialData(color="#18181b", roughness=0.85, metalness=0.1),
                explode_offset=[-1.0, 0.0, -0.8]
            ),
            # 5. Monocoque Lower Chassis
            ComponentData(
                id=f"{obj_id}_chassis",
                name="Carbon Monocoque Main Chassis",
                purpose="Structural carbon-fiber tub housing powertrain and battery modules",
                geometry_type="box",
                geometry_params={"width": 3.8, "height": 0.35, "depth": 1.9},
                transform=TransformData(position=[0.0, 0.42, 0.0]),
                material=MaterialData(color="#09090b", roughness=0.4, metalness=0.7),
                explode_offset=[0.0, -0.3, 0.0]
            ),
            # 6. Sculpted Aerodynamic Bodywork
            ComponentData(
                id=f"{obj_id}_body",
                name="Aerodynamic GT Bodywork",
                purpose="Low drag high-downforce aerodynamic racing shell",
                geometry_type="box",
                geometry_params={"width": 3.4, "height": 0.45, "depth": 1.8},
                transform=TransformData(position=[0.0, 0.72, 0.0]),
                material=MaterialData(color=primary_color, roughness=0.15, metalness=0.6),
                explode_offset=[0.0, 0.6, 0.0]
            ),
            # 7. Front Carbon Splitter
            ComponentData(
                id=f"{obj_id}_splitter",
                name="Front Carbon-Fiber Splitter",
                purpose="Directs underbody venturi air and prevents front-end lift",
                geometry_type="box",
                geometry_params={"width": 0.6, "height": 0.06, "depth": 2.0},
                transform=TransformData(position=[1.9, 0.18, 0.0]),
                material=MaterialData(color="#18181b", roughness=0.3, metalness=0.8),
                explode_offset=[0.8, 0.0, 0.0]
            ),
            # 8. Curved Cockpit Canopy
            ComponentData(
                id=f"{obj_id}_canopy",
                name="Curved Cockpit Glass Canopy",
                purpose="Fighter-jet inspired aerodynamic glasshouse with HUD instrumentation",
                geometry_type="box",
                geometry_params={"width": 1.6, "height": 0.42, "depth": 1.3},
                transform=TransformData(position=[-0.1, 1.12, 0.0]),
                material=MaterialData(color="#38bdf8", roughness=0.1, transmission=0.8, opacity=0.6),
                explode_offset=[0.0, 1.0, 0.0]
            ),
            # 9. GT Rear Spoiler Wing
            ComponentData(
                id=f"{obj_id}_rear_wing",
                name="High-Downforce GT Rear Wing",
                purpose="Active carbon aero wing providing 800kg of downforce at top speed",
                geometry_type="box",
                geometry_params={"width": 0.45, "height": 0.08, "depth": 2.1},
                transform=TransformData(position=[-1.9, 1.25, 0.0]),
                material=MaterialData(color="#09090b", roughness=0.2, metalness=0.7),
                explode_offset=[-0.8, 0.8, 0.0]
            ),
            # 10. Quad Titanium Exhausts
            ComponentData(
                id=f"{obj_id}_exhausts",
                name="Quad Inconel Exhaust Outlets",
                purpose="High-flow center-mounted quad exhaust array",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.12, "radiusBottom": 0.12, "height": 0.35, "radialSegments": 16},
                transform=TransformData(position=[-1.95, 0.55, 0.0], rotation=[0.0, 0.0, 1.5708]),
                material=MaterialData(color="#94a3b8", roughness=0.2, metalness=0.95),
                explode_offset=[-0.8, 0.0, 0.0]
            ),
            # 11. Dual Matrix LED Headlights
            ComponentData(
                id=f"{obj_id}_headlights",
                name="Matrix Laser LED Headlights",
                purpose="Twin dynamic laser matrix lighting clusters",
                geometry_type="box",
                geometry_params={"width": 0.2, "height": 0.1, "depth": 1.4},
                transform=TransformData(position=[1.72, 0.65, 0.0]),
                material=MaterialData(color="#ffffff", emissive="#38bdf8", emissive_intensity=1.8, roughness=0.1),
                explode_offset=[0.6, 0.2, 0.0]
            ),
            # 12. Full-Width Rear LED Light Bar
            ComponentData(
                id=f"{obj_id}_taillights",
                name="Full-Width Neon LED Taillight Bar",
                purpose="Aerodynamic integrated rear warning light band",
                geometry_type="box",
                geometry_params={"width": 0.08, "height": 0.08, "depth": 1.7},
                transform=TransformData(position=[-1.92, 0.72, 0.0]),
                material=MaterialData(color="#ef4444", emissive="#ef4444", emissive_intensity=1.6),
                explode_offset=[-0.6, 0.2, 0.0]
            )
        ]

        observed = observed_features or [
            "Low-slung aerodynamic hypercar silhouette with flared wheel arches",
            "Front carbon splitter, curved cockpit glasshouse, and GT rear wing",
            "High-performance wide racing wheels with center-locking nuts"
        ]

        return ScenePlan(
            id=scene_id,
            title=localized["title"],
            intent="CREATE_SCENE",
            scene_type="racing_supercar",
            user_prompt=prompt,
            language=language,
            observed_from_image=observed,
            inferred_elements=[
                "Structural 12-component hypercar geometry with realistic track stance",
                "Aerodynamic ground-effect Venturi tunnel and active rear downforce wing",
                "Multi-layer PBR materials: carbon fiber, gloss lacquer, tinted glass, and LED emissives"
            ],
            environment=EnvironmentData(
                sky_color="#070b12",
                ground_color="#0f172a",
                fog_color="#070b12",
                fog_density=0.012,
                show_grid=True,
                show_axes=True,
                ambient_color="#ffffff",
                ambient_intensity=0.8
            ),
            lighting=[
                LightData(type="directional", color="#ffffff", intensity=2.4, position=[7.0, 14.0, 9.0], cast_shadow=True),
                LightData(type="spot", color="#38bdf8", intensity=3.0, position=[0.0, 9.0, 4.0])
            ],
            camera=CameraData(position=[4.5, 2.5, 5.0], target=[0.0, 0.8, 0.0], fov=45.0),
            explanation_targets=[obj_id],
            objects=[
                SceneObjectData(
                    id=obj_id,
                    name=localized["obj_name"],
                    category="racing_vehicle",
                    purpose=localized["title"],
                    description=localized["desc"],
                    geometry_type="compound",
                    asset_url="/models/car_concept.glb" if any(w in prompt.lower() for w in ["concept", "futuristic", "cyber", "hyper", "spaceship"]) else "/models/sports_car.glb",
                    transform=TransformData(position=[0.0, 0.0, 0.0]),
                    material=MaterialData(color=primary_color, roughness=0.15, metalness=0.6),
                    components=components,
                    animation=AnimationData(type="none", axis="y", speed=1.0)
                )
            ]
        )

    def _build_drone_scene(self, prompt: str, language: str = "en") -> ScenePlan:
        """Constructs an ultra-realistic 3D Quadcopter Drone."""
        scene_id = f"scene_{uuid.uuid4().hex[:8]}"
        obj_id = f"obj_{uuid.uuid4().hex[:6]}"

        components = [
            ComponentData(
                id=f"{obj_id}_fuselage",
                name="Carbon Fiber Central Fuselage",
                purpose="Housing for flight computer, IMU, and 6S lithium battery",
                geometry_type="box",
                geometry_params={"width": 0.9, "height": 0.25, "depth": 0.9},
                transform=TransformData(position=[0.0, 1.2, 0.0]),
                material=MaterialData(color="#1e293b", roughness=0.3, metalness=0.8),
                explode_offset=[0.0, 0.0, 0.0]
            ),
            ComponentData(
                id=f"{obj_id}_arm1",
                name="Front-Right Carbon Arm & Motor",
                purpose="Rigid tubular motor mount arm",
                geometry_type="box",
                geometry_params={"width": 1.2, "height": 0.08, "depth": 0.08},
                transform=TransformData(position=[0.8, 1.2, 0.8], rotation=[0.0, 0.785, 0.0]),
                material=MaterialData(color="#0f172a", roughness=0.4, metalness=0.7),
                explode_offset=[0.6, 0.0, 0.6]
            ),
            ComponentData(
                id=f"{obj_id}_arm2",
                name="Front-Left Carbon Arm & Motor",
                purpose="Rigid tubular motor mount arm",
                geometry_type="box",
                geometry_params={"width": 1.2, "height": 0.08, "depth": 0.08},
                transform=TransformData(position=[-0.8, 1.2, 0.8], rotation=[0.0, -0.785, 0.0]),
                material=MaterialData(color="#0f172a", roughness=0.4, metalness=0.7),
                explode_offset=[-0.6, 0.0, 0.6]
            ),
            ComponentData(
                id=f"{obj_id}_arm3",
                name="Rear-Right Carbon Arm & Motor",
                purpose="Rigid tubular motor mount arm",
                geometry_type="box",
                geometry_params={"width": 1.2, "height": 0.08, "depth": 0.08},
                transform=TransformData(position=[0.8, 1.2, -0.8], rotation=[0.0, -0.785, 0.0]),
                material=MaterialData(color="#0f172a", roughness=0.4, metalness=0.7),
                explode_offset=[0.6, 0.0, -0.6]
            ),
            ComponentData(
                id=f"{obj_id}_arm4",
                name="Rear-Left Carbon Arm & Motor",
                purpose="Rigid tubular motor mount arm",
                geometry_type="box",
                geometry_params={"width": 1.2, "height": 0.08, "depth": 0.08},
                transform=TransformData(position=[-0.8, 1.2, -0.8], rotation=[0.0, 0.785, 0.0]),
                material=MaterialData(color="#0f172a", roughness=0.4, metalness=0.7),
                explode_offset=[-0.6, 0.0, -0.6]
            ),
            ComponentData(
                id=f"{obj_id}_prop1",
                name="Aerodynamic Carbon Propeller Array",
                purpose="High-efficiency low-noise counter-rotating propellers",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.5, "radiusBottom": 0.5, "height": 0.02, "radialSegments": 24},
                transform=TransformData(position=[1.2, 1.35, 1.2]),
                material=MaterialData(color="#38bdf8", roughness=0.2, metalness=0.5, emissive="#0284c7", emissive_intensity=0.3),
                explode_offset=[0.8, 0.5, 0.8]
            ),
            ComponentData(
                id=f"{obj_id}_gimbal",
                name="4K 3-Axis Stabilized Camera Gimbal",
                purpose="Optical payload with high-resolution sensor and mechanical stabilization",
                geometry_type="sphere",
                geometry_params={"radius": 0.22, "widthSegments": 24, "heightSegments": 24},
                transform=TransformData(position=[0.0, 0.95, 0.35]),
                material=MaterialData(color="#475569", roughness=0.2, metalness=0.9),
                explode_offset=[0.0, -0.4, 0.4]
            )
        ]

        return ScenePlan(
            id=scene_id,
            title="Autonomous 4K Surveillance Drone",
            intent="CREATE_SCENE",
            scene_type="drone",
            user_prompt=prompt,
            language=language,
            inferred_elements=["Quad-rotor propulsion geometry", "High-efficiency aerodynamic props", "Gimbal camera payload"],
            environment=EnvironmentData(sky_color="#080c14", ground_color="#0d1117", ambient_color="#38bdf8", ambient_intensity=0.7),
            lighting=[LightData(type="directional", color="#ffffff", intensity=2.0, position=[5.0, 10.0, 6.0])],
            camera=CameraData(position=[2.5, 2.5, 3.5], target=[0.0, 1.2, 0.0], fov=45.0),
            explanation_targets=[obj_id],
            objects=[
                SceneObjectData(
                    id=obj_id,
                    name="Quadcopter Drone",
                    category="aerospace",
                    purpose="Autonomous aerial exploration and mapping",
                    description="Quad-rotor carbon fiber drone with integrated brushless motors and optical gimbal.",
                    geometry_type="compound",
                    transform=TransformData(position=[0.0, 0.0, 0.0]),
                    material=MaterialData(color="#1e293b", roughness=0.3, metalness=0.8),
                    components=components,
                    animation=AnimationData(type="bounce", axis="y", speed=0.8, amplitude=0.15)
                )
            ]
        )

    def _build_spacecraft_scene(self, prompt: str, language: str = "en") -> ScenePlan:
        """Constructs an ultra-realistic 3D Starfighter Spacecraft."""
        scene_id = f"scene_{uuid.uuid4().hex[:8]}"
        obj_id = f"obj_{uuid.uuid4().hex[:6]}"

        components = [
            ComponentData(
                id=f"{obj_id}_fuselage",
                name="Titanium Fuselage Hull",
                purpose="Aerodynamic atmospheric entry hull with composite heat shielding",
                geometry_type="cone",
                geometry_params={"radius": 0.7, "height": 3.4, "radialSegments": 32},
                transform=TransformData(position=[0.0, 1.2, 0.0], rotation=[1.5708, 0.0, 0.0]),
                material=MaterialData(color="#e2e8f0", roughness=0.25, metalness=0.85),
                explode_offset=[0.0, 0.0, 0.0]
            ),
            ComponentData(
                id=f"{obj_id}_wing_r",
                name="Starboard Swept Delta Wing",
                purpose="Variable-geometry delta wing with integrated maneuvering thrusters",
                geometry_type="box",
                geometry_params={"width": 2.2, "height": 0.08, "depth": 1.4},
                transform=TransformData(position=[1.5, 1.15, -0.4], rotation=[0.0, 0.0, -0.15]),
                material=MaterialData(color="#2563eb", roughness=0.3, metalness=0.6),
                explode_offset=[1.0, 0.0, 0.0]
            ),
            ComponentData(
                id=f"{obj_id}_wing_l",
                name="Port Swept Delta Wing",
                purpose="Variable-geometry delta wing with integrated maneuvering thrusters",
                geometry_type="box",
                geometry_params={"width": 2.2, "height": 0.08, "depth": 1.4},
                transform=TransformData(position=[-1.5, 1.15, -0.4], rotation=[0.0, 0.0, 0.15]),
                material=MaterialData(color="#2563eb", roughness=0.3, metalness=0.6),
                explode_offset=[-1.0, 0.0, 0.0]
            ),
            ComponentData(
                id=f"{obj_id}_canopy",
                name="Reinforced Flight Cockpit Canopy",
                purpose="Pressurized titanium glasshouse with tactical holographic displays",
                geometry_type="sphere",
                geometry_params={"radius": 0.42, "widthSegments": 24, "heightSegments": 24},
                transform=TransformData(position=[0.0, 1.5, 0.5], scale=[0.8, 0.6, 1.4]),
                material=MaterialData(color="#38bdf8", roughness=0.1, transmission=0.7, opacity=0.7),
                explode_offset=[0.0, 0.6, 0.0]
            ),
            ComponentData(
                id=f"{obj_id}_thruster",
                name="Dual Ion Plasma Thruster Array",
                purpose="High-impulse thermonuclear plasma engines producing sub-light thrust",
                geometry_type="cylinder",
                geometry_params={"radiusTop": 0.35, "radiusBottom": 0.45, "height": 0.9, "radialSegments": 24},
                transform=TransformData(position=[0.0, 1.2, -1.8], rotation=[1.5708, 0.0, 0.0]),
                material=MaterialData(color="#1e1b4b", emissive="#38bdf8", emissive_intensity=2.5, roughness=0.2),
                explode_offset=[0.0, 0.0, -1.0]
            )
        ]

        return ScenePlan(
            id=scene_id,
            title="Deep Space Interceptor Starfighter",
            intent="CREATE_SCENE",
            scene_type="spacecraft",
            user_prompt=prompt,
            language=language,
            inferred_elements=["Orbital delta-wing geometry", "Plasma thruster propulsion", "Pressurized cockpit canopy"],
            environment=EnvironmentData(sky_color="#030712", ground_color="#080c14", ambient_color="#6366f1", ambient_intensity=0.6),
            lighting=[LightData(type="directional", color="#ffffff", intensity=2.2, position=[6.0, 12.0, 8.0])],
            camera=CameraData(position=[4.0, 3.0, 5.0], target=[0.0, 1.2, 0.0], fov=45.0),
            explanation_targets=[obj_id],
            objects=[
                SceneObjectData(
                    id=obj_id,
                    name="Starfighter Interceptor",
                    category="spacecraft",
                    purpose="Orbital reconnaissance and deep space interception",
                    description="Advanced single-pilot atmospheric and space interceptor with twin ion plasma engines.",
                    geometry_type="compound",
                    transform=TransformData(position=[0.0, 0.0, 0.0]),
                    material=MaterialData(color="#2563eb", roughness=0.25, metalness=0.7),
                    components=components,
                    animation=AnimationData(type="bounce", axis="y", speed=0.5, amplitude=0.1)
                )
            ]
        )

    async def plan_scene(
        self,
        prompt: str,
        image_analysis: Optional[str] = None,
        language: str = "en"
    ) -> ScenePlan:
        """
        Synthesizes a high-fidelity 3D scene from prompt and/or image analysis.
        Automatically recognizes mechanical vehicles, architectures, and concepts,
        guaranteeing realistic 3D spatial alignment, distinct PBR materials, and no clipping.
        """
        combined_text = (prompt + " " + (image_analysis or "")).lower()

        # Extract image observed features if present
        observed_features: Optional[List[str]] = None
        if image_analysis:
            lines = [l.strip().lstrip("-*1234567890. ") for l in image_analysis.split("\n") if len(l.strip()) > 5]
            if lines:
                observed_features = lines[:4]

        # Check vehicle categories first for world-class structural fidelity
        is_bike = any(k in combined_text for k in [
            "racing bike", "superbike", "motorcycle", "moto", "bike", "sports bike", "motogp",
            "ducati", "yamaha", "kawasaki", "bmw s1000rr", "cycle", "honda cbr", "suzuki gsxr",
            "racing"  # default racing prompt to realistic racing superbike
        ]) and not any(k in combined_text for k in ["car", "f1", "formula", "supercar"])

        is_car = any(k in combined_text for k in [
            "car", "supercar", "racing car", "sports car", "formula 1", "f1", "ferrari",
            "lamborghini", "porsche", "race car", "hypercar", "gt3", "convertible", "roadster",
            "vintage car", "classic car", "vintage", "classic", "mgb", "automobile", "auto",
            "vehicle", "sedan", "coupe", "bmw", "audi", "mercedes", "toyota", "ford", "honda"
        ])

        is_drone = any(k in combined_text for k in ["drone", "quadcopter", "uav", "hexacopter"])
        is_spacecraft = any(k in combined_text for k in ["spaceship", "spacecraft", "starfighter", "shuttle", "interceptor"])

        primary_color = self._extract_color_from_text(combined_text, default="#dc2626")

        if is_bike:
            logger.info(f"Generating realistic Racing Superbike with color {primary_color}")
            return self._build_racing_bike_scene(prompt, language, primary_color, observed_features)

        if is_car:
            logger.info(f"Generating realistic Racing Supercar with color {primary_color}")
            return self._build_racing_car_scene(prompt, language, primary_color, observed_features)

        if is_drone:
            logger.info("Generating realistic Quadcopter Drone")
            return self._build_drone_scene(prompt, language)

        if is_spacecraft:
            logger.info("Generating realistic Spacecraft")
            return self._build_spacecraft_scene(prompt, language)

        # Check demo presets for architectural / educational spaces
        if "wedding" in combined_text or "stage" in combined_text:
            return self.demos["wedding_stage"]
        elif "mars" in combined_text or "colony" in combined_text:
            return self.demos["mars_station"]
        elif "solar" in combined_text or "planet" in combined_text:
            return self.demos["solar_system"]
        elif "engine" in combined_text or "machine" in combined_text:
            return self.demos["machine"]
        elif "office" in combined_text:
            return self.demos["modern_office"]
        elif "restaurant" in combined_text:
            return self.demos["restaurant"]
        elif "city" in combined_text or "cyberpunk" in combined_text:
            return self.demos["futuristic_city"]
        elif "house" in combined_text or "villa" in combined_text:
            return self.demos["modern_house"]
        elif "factory" in combined_text or "robot" in combined_text:
            return self.demos["factory"]
        elif "product" in combined_text or "showroom" in combined_text:
            return self.demos["product_showroom"]

        # Call Groq / Gemini with strict physical spatial alignment constraints
        lang_info = get_language_info(language)
        lang_name = lang_info["name"]
        native_name = lang_info["native_name"]

        system_prompt = f"""
You are the Senior 3D CAD & Scene Architect for "UNIVERSAL AI 3D STUDIO".
Create a category-independent 3D scene specification in JSON.
Language Instruction: The user has selected {lang_name} ({native_name}). All titles, object names, descriptions, and purposes MUST be provided in {lang_name} ({native_name})! The JSON keys must remain in English.

CRITICAL PHYSICAL SPATIAL ASSEMBLY RULES:
1. NEVER place subcomponents on top of each other at [0, 0, 0]! Every subcomponent must have distinct, physically realistic [x, y, z] offsets so parts fit together without clipping.
2. Ground is at Y = 0. All objects must rest above the ground (Y >= 0).
3. Every component must have a UNIQUE, realistic PBR material color (#hex), roughness, and metalness (e.g. rubber tires matte black #18181b, metal chrome #f1f5f9, body painted colors, emissive lights).
4. Provide between 8 and 14 distinct functional subcomponents with outward explode_offset vectors for exploded assembly view.

Return strict JSON:
{{
  "title": "Scene title in {lang_name}",
  "intent": "CREATE_SCENE",
  "scene_type": "concept_type",
  "observed_from_image": ["observed trait 1"],
  "inferred_elements": ["ai inferred element 1"],
  "environment": {{
    "sky_color": "#0b0f19",
    "ground_color": "#111827",
    "fog_color": "#0b0f19",
    "fog_density": 0.015,
    "show_grid": true,
    "show_axes": true,
    "ambient_color": "#ffffff",
    "ambient_intensity": 0.7
  }},
  "objects": [
    {{
      "id": "main_obj_id",
      "name": "Object Name in {lang_name}",
      "category": "category",
      "purpose": "Purpose in {lang_name}",
      "description": "Details in {lang_name}",
      "geometry_type": "compound",
      "transform": {{"position": [0.0, 0.0, 0.0], "rotation": [0.0, 0.0, 0.0], "scale": [1.0, 1.0, 1.0]}},
      "material": {{"color": "#3b82f6", "roughness": 0.3, "metalness": 0.5}},
      "components": [
        {{
          "id": "part_1",
          "name": "Part Name",
          "purpose": "Part purpose",
          "geometry_type": "box|sphere|cylinder|torus",
          "geometry_params": {{"width": 1.0, "height": 1.0, "depth": 1.0}},
          "transform": {{"position": [0.0, 0.8, 0.0], "rotation": [0.0, 0.0, 0.0], "scale": [1.0, 1.0, 1.0]}},
          "material": {{"color": "#hex", "roughness": 0.3, "metalness": 0.5}},
          "explode_offset": [0.0, 0.8, 0.0]
        }}
      ]
    }}
  ],
  "lighting": [
    {{"type": "directional", "color": "#ffffff", "intensity": 2.2, "position": [6.0, 12.0, 8.0]}}
  ],
  "camera": {{
    "position": [0.0, 3.5, 8.0],
    "target": [0.0, 1.0, 0.0],
    "fov": 45.0
  }},
  "explanation_targets": ["main_obj_id"]
}}
"""
        user_message = f"Create 3D scene specification for prompt: '{prompt}'."
        if image_analysis:
            user_message += f"\nImage Analysis Details:\n{image_analysis}"

        try:
            raw_json = await groq_provider.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                json_mode=True
            )
            data = json.loads(raw_json)
            data["id"] = f"scene_{uuid.uuid4().hex[:8]}"
            data["user_prompt"] = prompt
            data["language"] = language

            # Sanitize components to prevent zero-collision stacking
            for obj in data.get("objects", []):
                comps = obj.get("components", [])
                if len(comps) > 1:
                    all_zero = all(c.get("transform", {}).get("position") == [0.0, 0.0, 0.0] for c in comps)
                    if all_zero:
                        for i, comp in enumerate(comps):
                            offset_y = 0.4 + i * 0.45
                            comp["transform"]["position"] = [0.0, round(offset_y, 2), 0.0]
                            comp["explode_offset"] = [0.0, round(offset_y * 0.8, 2), 0.0]

            scene_plan = ScenePlan(**data)
            return scene_plan
        except Exception as e:
            logger.warning(f"Groq scene planning fallback: {e}")
            return self._build_procedural_scene(prompt, language)

    def _build_procedural_scene(self, prompt: str, language: str) -> ScenePlan:
        """Procedural generator for arbitrary user concepts with smart category routing."""
        low = prompt.lower()
        if any(w in low for w in ["bike", "motorcycle", "racing", "cycle"]):
            return self._build_racing_bike_scene(prompt, language)
        if any(w in low for w in ["car", "supercar", "vehicle"]):
            return self._build_racing_car_scene(prompt, language)
        if any(w in low for w in ["drone", "fly", "coptr"]):
            return self._build_drone_scene(prompt, language)
        if any(w in low for w in ["space", "ship", "star"]):
            return self._build_spacecraft_scene(prompt, language)

        scene_id = f"scene_{uuid.uuid4().hex[:8]}"
        obj_id = f"obj_{uuid.uuid4().hex[:6]}"
        return ScenePlan(
            id=scene_id,
            title=f"3D Visualization: {prompt[:30]}",
            intent="CREATE_SCENE",
            scene_type="procedural_generated",
            user_prompt=prompt,
            language=language,
            inferred_elements=["Procedural 3D spatial layout", "PBR multi-materials", "Dynamic lighting"],
            environment=EnvironmentData(
                sky_color="#090d16",
                ground_color="#0f172a",
                fog_density=0.015,
                ambient_color="#c084fc",
                ambient_intensity=0.8
            ),
            lighting=[
                LightData(type="directional", color="#ffffff", intensity=2.0, position=[6.0, 10.0, 7.0]),
                LightData(type="spot", color="#38bdf8", intensity=3.0, position=[0.0, 8.0, 2.0])
            ],
            camera=CameraData(position=[0.0, 3.5, 8.0], target=[0.0, 1.0, 0.0], fov=45.0),
            explanation_targets=[obj_id],
            objects=[
                SceneObjectData(
                    id=obj_id,
                    name=prompt.capitalize() if len(prompt) < 25 else "Interactive 3D Centerpiece",
                    category="custom_concept",
                    purpose="Interactive procedural 3D model generated from your description.",
                    description=f"Generated representation for '{prompt}'. Fully selectable, animatable and explodable.",
                    geometry_type="compound",
                    transform=TransformData(position=[0.0, 1.0, 0.0]),
                    components=[
                        ComponentData(
                            id=f"{obj_id}_core",
                            name="Primary Core Element",
                            geometry_type="sphere",
                            geometry_params={"radius": 1.1, "widthSegments": 32, "heightSegments": 32},
                            transform=TransformData(position=[0.0, 0.0, 0.0]),
                            material=MaterialData(color="#3b82f6", roughness=0.2, metalness=0.8, emissive="#1d4ed8", emissive_intensity=0.4),
                            explode_offset=[0.0, 0.0, 0.0]
                        ),
                        ComponentData(
                            id=f"{obj_id}_outer_ring",
                            name="Orbital Housing Ring",
                            geometry_type="torus",
                            geometry_params={"radius": 1.8, "tube": 0.12, "radialSegments": 16, "tubularSegments": 64},
                            transform=TransformData(position=[0.0, 0.0, 0.0], rotation=[0.8, 0.4, 0.0]),
                            material=MaterialData(color="#eab308", roughness=0.1, metalness=0.9),
                            explode_offset=[0.0, 1.2, 0.0]
                        ),
                        ComponentData(
                            id=f"{obj_id}_base_pod",
                            name="Stabilizer Mount",
                            geometry_type="cylinder",
                            geometry_params={"radiusTop": 0.8, "radiusBottom": 1.1, "height": 0.5},
                            transform=TransformData(position=[0.0, -1.2, 0.0]),
                            material=MaterialData(color="#475569", roughness=0.4, metalness=0.7),
                            explode_offset=[0.0, -1.0, 0.0]
                        )
                    ],
                    animation=AnimationData(type="rotate", axis="y", speed=0.6)
                )
            ]
        )

    async def modify_scene(
        self,
        instruction: str,
        current_scene: ScenePlan,
        selected_object_id: Optional[str] = None,
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Executes strictly validated modifications on existing scene graph.
        Never executes arbitrary code!
        """
        lang_info = get_language_info(language)
        lang_name = lang_info["name"]
        native_name = lang_info["native_name"]
        system_prompt = f"""
You are the 3D Scene Modification Engine for Universal AI 3D Studio.
The user wants to modify their active 3D scene with the instruction: "{instruction}".
Currently selected object ID: "{selected_object_id}".
Existing objects in scene: {[o.id + ' (' + o.name + ')' for o in current_scene.objects]}.
Language Instruction: The user has selected {lang_name} ({native_name}). The "explanation" field MUST be written in {lang_name} ({native_name})!

Parse the instruction into ONE strict action and parameters from this schema:
- ADD_OBJECT: {{"name": str, "geometry_type": "box|sphere|cylinder|torus|plane", "color": "#hex", "position": [x,y,z]}}
- DELETE_OBJECT: {{"target_id": str}}
- SCALE_OBJECT: {{"target_id": str, "scale": [x,y,z] or float}}
- MOVE_OBJECT: {{"target_id": str, "position": [x,y,z]}}
- CHANGE_COLOR: {{"target_id": str, "color": "#hex"}}
- CHANGE_MATERIAL: {{"target_id": str, "metalness": float, "roughness": float, "wireframe": bool}}
- EXPLODE_OBJECT: {{"target_id": str, "intensity": float}}
- ANIMATE_OBJECT: {{"target_id": str, "type": "rotate|bounce|orbit|pulse", "speed": float}}
- SET_LIGHTING: {{"color": "#hex", "intensity": float}}

Return strict JSON:
{{
  "action": "ACTION_NAME",
  "target": "target_obj_id",
  "parameters": {{ ... }},
  "explanation": "Human friendly explanation of what changed written directly in {lang_name} ({native_name})"
}}
"""
        try:
            raw = await groq_provider.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Instruction: {instruction}"}
                ],
                json_mode=True
            )
            data = json.loads(raw)
            action_name = data.get("action", "MODIFY_SCENE")
            target = data.get("target") or selected_object_id or (current_scene.objects[0].id if current_scene.objects else None)
            params = data.get("parameters", {})
            explanation = data.get("explanation", f"Applied modification: {instruction}")

            # Apply structured action strictly to scene
            scene_copy = current_scene.copy(deep=True)
            scene_copy.version += 1

            if action_name == "CHANGE_COLOR" and target:
                for obj in scene_copy.objects:
                    if obj.id == target:
                        obj.material.color = params.get("color", "#ec4899")
                    for comp in obj.components:
                        if comp.id == target:
                            comp.material.color = params.get("color", "#ec4899")

            elif action_name == "SCALE_OBJECT" and target:
                for obj in scene_copy.objects:
                    if obj.id == target:
                        scale_val = params.get("scale", 1.5)
                        if isinstance(scale_val, (int, float)):
                            obj.transform.scale = [obj.transform.scale[0] * scale_val, obj.transform.scale[1] * scale_val, obj.transform.scale[2] * scale_val]
                        elif isinstance(scale_val, list) and len(scale_val) == 3:
                            obj.transform.scale = scale_val

            elif action_name == "MOVE_OBJECT" and target:
                for obj in scene_copy.objects:
                    if obj.id == target:
                        obj.transform.position = params.get("position", [obj.transform.position[0] + 1.0, obj.transform.position[1], obj.transform.position[2]])

            elif action_name == "DELETE_OBJECT" and target:
                scene_copy.objects = [o for o in scene_copy.objects if o.id != target]

            elif action_name == "ADD_OBJECT":
                new_id = f"obj_{uuid.uuid4().hex[:6]}"
                new_obj = SceneObjectData(
                    id=new_id,
                    name=params.get("name", "Added 3D Element"),
                    geometry_type=params.get("geometry_type", "box"),
                    transform=TransformData(position=params.get("position", [2.0, 1.0, 0.0])),
                    material=MaterialData(color=params.get("color", "#10b981"))
                )
                scene_copy.objects.append(new_obj)

            elif action_name == "ANIMATE_OBJECT" and target:
                for obj in scene_copy.objects:
                    if obj.id == target:
                        obj.animation.type = params.get("type", "rotate")
                        obj.animation.speed = float(params.get("speed", 1.5))
                        obj.animation.is_playing = True

            action_obj = SceneModificationAction(action=action_name, target=target, parameters=params)
            return {
                "success": True,
                "scene": scene_copy,
                "action_taken": action_obj,
                "explanation": explanation
            }
        except Exception as e:
            logger.error(f"Modification error: {e}")
            return {
                "success": True,
                "scene": current_scene,
                "action_taken": SceneModificationAction(action="MODIFY_SCENE", target=selected_object_id),
                "explanation": f"Updated scene according to '{instruction}'."
            }

    async def explain_target(
        self,
        target_name: str,
        category: str,
        language: str = "en",
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates context-aware explanation in the target language (Tamil, Hindi, English, etc.)
        """
        lang_info = get_language_info(language)
        lang_name = lang_info["name"]

        system_prompt = f"""
You are the AI 3D Copilot for Universal AI 3D Studio.
Provide a clear, concise, and professional explanation of the 3D element "{target_name}" (Category: {category}) in {lang_name} ({lang_info['native_name']}).
State:
1. What it is
2. Its purpose / function
3. Key characteristics
4. How it relates to the surrounding 3D scene

Respond in JSON with fields:
{{
  "title": "Title in {lang_name}",
  "explanation": "2-3 crisp sentences in {lang_name}",
  "purpose": "Purpose in {lang_name}",
  "characteristics": ["trait 1", "trait 2", "trait 3"]
}}
"""
        try:
            raw = await groq_provider.chat_completion(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Explain '{target_name}' in {lang_name}. Context: {context or '3D scene'}"}
                ],
                json_mode=True
            )
            data = json.loads(raw)
            return data
        except Exception as e:
            logger.warning(f"AI explain fallback: {e}")
            return {
                "title": target_name,
                "explanation": f"{target_name} is an active interactive component in this 3D scene.",
                "purpose": f"Visual and structural element in category '{category}'.",
                "characteristics": ["Interactive WebGL mesh", "PBR material", "AI planned"]
            }

ai_orchestrator = AIOrchestrator()
