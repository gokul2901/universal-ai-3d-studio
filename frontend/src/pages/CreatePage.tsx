import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, Wand2, Lightbulb, Globe, Camera, Layers, Box } from 'lucide-react';
import { ImageUploader } from '../components/upload/ImageUploader';
import { VoiceRecorder } from '../components/voice/VoiceRecorder';
import { GenerationProgress } from '../components/ai/GenerationProgress';
import { RealisticImageModal } from '../components/ai/RealisticImageModal';
import { generate3DScene, generateRealisticImage } from '../services/api';
import { useSceneStore } from '../store/useSceneStore';
import { useAIStore } from '../store/useAIStore';
import { useUIStore } from '../store/useUIStore';
import { SUPPORTED_LANGUAGES, t, isRTL } from '../i18n';

export const CreatePage: React.FC = () => {
  const navigate = useNavigate();
  const { setScene } = useSceneStore();
  const { isGenerating, setIsGenerating, currentStep, setCurrentStep, addMessage } = useAIStore();
  const { language, setLanguage } = useUIStore();

  const [prompt, setPrompt] = useState('');
  const [imageBase64, setImageBase64] = useState<string | null>(null);
  const [rotatingPromptIdx, setRotatingPromptIdx] = useState(0);
  const [generationMode, setGenerationMode] = useState<'dual' | 'photo' | '3d'>('dual');
  const [realisticResultUrl, setRealisticResultUrl] = useState<string | null>(null);
  const [showPhotoModal, setShowPhotoModal] = useState(false);

  const samplePrompts = [
    "Create a futuristic city with flying vehicles and neon skyscrapers.",
    "Transform this empty stage into a luxury wedding stage with floral arches.",
    "Create a 3D solar system and explain each planet.",
    "Turn this room into a modern luxury AI startup office.",
    "Show the internal components of this machine with exploded view.",
    "Create a futuristic Mars research station with bio-domes and rover.",
    "Design a fine dining luxury restaurant with Calacatta marble tables.",
    "Create an interactive product showroom with a floating luxury smartwatch."
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setRotatingPromptIdx((prev) => (prev + 1) % samplePrompts.length);
    }, 4500);
    return () => clearInterval(timer);
  }, []);

  const handleGenerate = async (overridePrompt?: string) => {
    const textPrompt = overridePrompt || prompt;
    if (!textPrompt.trim() && !imageBase64) return;

    setIsGenerating(true);
    setCurrentStep(0);

    // If photorealistic image only mode
    if (generationMode === 'photo') {
      try {
        const res = await generateRealisticImage({
          prompt: textPrompt,
          style: 'photorealistic',
          width: 1280,
          height: 720,
        });
        setIsGenerating(false);
        if (res.success && res.image_url) {
          setRealisticResultUrl(res.image_url);
          setShowPhotoModal(true);
        }
        return;
      } catch (err: any) {
        setIsGenerating(false);
        alert('Photo generation failed. Please try again.');
        return;
      }
    }

    // Simulate progressive step updates through the 7 stages
    const stepInterval = setInterval(() => {
      setCurrentStep(Math.min(6, currentStep + 1));
    }, 600);

    try {
      const res = await generate3DScene({
        prompt: textPrompt,
        image_base64: imageBase64 || undefined,
        language: language,
      });

      clearInterval(stepInterval);
      setCurrentStep(6);

      if (res.success && res.scene) {
        setScene(res.scene);
        addMessage({
          id: `gen_${Date.now()}`,
          sender: 'ai',
          text: `Successfully synthesized **${res.scene.title}** with ${res.scene.objects.length} 3D objects and ultra-realistic 8K visual render!`,
          timestamp: new Date().toLocaleTimeString(),
        });

        setTimeout(() => {
          setIsGenerating(false);
          navigate(`/studio/${res.project_id}`);
        }, 800);
      }
    } catch (err: any) {
      clearInterval(stepInterval);
      setIsGenerating(false);
      alert('Generation encountered an issue. Using local fallback.');
      navigate('/studio');
    }
  };

  const isRtlLang = isRTL(language);

  return (
    <div className={`min-h-screen bg-dark-950 text-white p-6 sm:p-10 flex flex-col items-center justify-center relative ${isRtlLang ? 'rtl' : 'ltr'}`}>
      <GenerationProgress />

      <div className="w-full max-w-2xl flex flex-col items-center">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass-panel border border-primary-500/30 text-xs font-semibold text-primary-300 mb-3 shadow-lg">
            <Sparkles className="w-3.5 h-3.5 text-accent-cyan" />
            <span>Universal Multimodal Visual Generator</span>
          </div>
          <h1 className="font-display font-extrabold text-3xl sm:text-4xl text-white mb-2">
            {t('create_title', language)}
          </h1>
          <p className="text-xs sm:text-sm text-slate-400">
            Synthesize interactive 3D spaces or ultra-realistic 8K photographic visuals
          </p>
        </div>

        {/* Mode Selector Tabs */}
        <div className="w-full grid grid-cols-3 gap-2 mb-4 p-1.5 bg-dark-900/80 border border-white/10 rounded-2xl backdrop-blur-xl">
          <button
            type="button"
            onClick={() => setGenerationMode('dual')}
            className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-semibold transition-all ${
              generationMode === 'dual'
                ? 'bg-gradient-to-r from-primary-500 to-indigo-600 text-white shadow-md shadow-primary-500/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Dual: 3D + 8K Photo</span>
          </button>
          <button
            type="button"
            onClick={() => setGenerationMode('photo')}
            className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-semibold transition-all ${
              generationMode === 'photo'
                ? 'bg-gradient-to-r from-accent-cyan to-teal-500 text-dark-950 shadow-md shadow-accent-cyan/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Camera className="w-3.5 h-3.5" />
            <span>Realistic 8K Photo Only</span>
          </button>
          <button
            type="button"
            onClick={() => setGenerationMode('3d')}
            className={`flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl text-xs font-semibold transition-all ${
              generationMode === '3d'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <Box className="w-3.5 h-3.5" />
            <span>3D Scene Only</span>
          </button>
        </div>

        {/* Main Creation Card */}
        <div className="w-full glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 shadow-2xl flex flex-col gap-6">
          {/* Reference Image Uploader */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-2">
              {t('drag_drop_title', language)}
            </label>
            <ImageUploader
              onImageSelected={(b64) => setImageBase64(b64)}
              onImageRemoved={() => setImageBase64(null)}
              selectedImageBase64={imageBase64}
            />
          </div>

          {/* Prompt Composer */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <label className="block text-xs font-semibold text-slate-300">
                {t('prompt_label', language)}
              </label>
              <button
                type="button"
                onClick={() => setPrompt(samplePrompts[rotatingPromptIdx])}
                className="flex items-center gap-1 text-[11px] text-primary-400 hover:text-primary-300 transition-colors"
              >
                <Lightbulb className="w-3.5 h-3.5" />
                <span className="truncate max-w-[220px]">Suggest: "{samplePrompts[rotatingPromptIdx].slice(0, 24)}..."</span>
              </button>
            </div>
            <textarea
              rows={4}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={t('prompt_placeholder', language)}
              className="w-full bg-dark-900/90 border border-white/10 rounded-2xl p-4 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-primary-500/60 transition-colors resize-none leading-relaxed"
            />
          </div>

          {/* Action Row: Voice Recorder, Language Selector, Generate Button */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-white/10">
            <div className="flex items-center gap-3">
              {/* Voice Button */}
              <VoiceRecorder
                onTranscriptionComplete={(text) => {
                  setPrompt(text);
                  handleGenerate(text);
                }}
                languageHint={language}
              />

              {/* Language Indicator */}
              <div className="hidden sm:flex items-center gap-1.5 px-3 py-2 rounded-xl bg-dark-900 border border-white/10 text-xs text-slate-300">
                <Globe className="w-3.5 h-3.5 text-primary-400" />
                <span>{SUPPORTED_LANGUAGES.find(l => l.code === language)?.name || 'English'}</span>
              </div>
            </div>

            {/* Generate Button */}
            <button
              type="button"
              onClick={() => handleGenerate()}
              disabled={(!prompt.trim() && !imageBase64) || isGenerating}
              className="flex items-center gap-2 px-6 py-3 rounded-2xl font-semibold text-xs sm:text-sm bg-gradient-to-r from-primary-500 to-indigo-600 hover:from-primary-600 hover:to-indigo-700 disabled:opacity-40 text-white shadow-xl shadow-primary-500/30 transition-all cursor-pointer"
            >
              <Wand2 className="w-4 h-4" />
              <span>{t('generate_btn', language)}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Realistic 8K Photographic Render Modal */}
      <RealisticImageModal
        isOpen={showPhotoModal}
        onClose={() => setShowPhotoModal(false)}
        initialImageUrl={realisticResultUrl || undefined}
        initialPrompt={prompt}
      />
    </div>
  );
};
