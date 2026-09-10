import React, { useState } from 'react';
import {
  X,
  Download,
  Sparkles,
  RefreshCw,
  Camera,
  Layers,
  ExternalLink,
  ZoomIn,
  ZoomOut,
  Maximize2
} from 'lucide-react';
import { generateRealisticImage } from '../../services/api';

interface RealisticImageModalProps {
  isOpen: boolean;
  onClose: () => void;
  initialImageUrl?: string;
  initialPrompt?: string;
  initialEnhancedPrompt?: string;
}

const STYLES = [
  { id: '3d_render',       name: 'Unreal Engine 5 CGI',     icon: '🎮' },
  { id: 'product_3d',     name: '3D Product Render',        icon: '📦' },
  { id: 'sci_fi_3d',      name: 'Sci-Fi CGI',               icon: '🚀' },
  { id: 'photorealistic', name: 'Photorealistic 8K',        icon: '📸' },
  { id: 'studio',         name: 'Commercial Studio',        icon: '💡' },
  { id: 'cinematic',      name: 'Cinematic 35mm',           icon: '🎬' },
  { id: 'automotive',     name: 'Automotive Showcase',      icon: '🏎️' },
  { id: 'architectural',  name: 'Architectural Digest',     icon: '🏛️' },
  { id: 'macro',          name: 'Macro Detail',             icon: '🔍' },
];

export const RealisticImageModal: React.FC<RealisticImageModalProps> = ({
  isOpen,
  onClose,
  initialImageUrl,
  initialPrompt = 'Futuristic high-tech concept',
  initialEnhancedPrompt,
}) => {
  const [imageUrl, setImageUrl] = useState<string>(initialImageUrl || '');
  const [prompt, setPrompt] = useState<string>(initialPrompt);
  const [enhancedPrompt, setEnhancedPrompt] = useState<string>(initialEnhancedPrompt || '');
  const [selectedStyle, setSelectedStyle] = useState<string>('3d_render');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [zoom, setZoom] = useState<number>(1);
  const [isFullView, setIsFullView] = useState<boolean>(false);

  // Sync initial values when opened
  React.useEffect(() => {
    if (initialImageUrl) setImageUrl(initialImageUrl);
    if (initialPrompt) setPrompt(initialPrompt);
    if (initialEnhancedPrompt) setEnhancedPrompt(initialEnhancedPrompt);
  }, [initialImageUrl, initialPrompt, initialEnhancedPrompt]);

  // If no initial image when opened, generate immediately
  React.useEffect(() => {
    if (isOpen && !imageUrl && prompt) {
      handleGenerate('3d_render');
    }
  }, [isOpen]);

  const handleGenerate = async (styleToUse = selectedStyle) => {
    if (!prompt.trim()) return;
    setIsLoading(true);
    try {
      const res = await generateRealisticImage({
        prompt,
        style: styleToUse,
        width: 1280,
        height: 720,
        seed: Math.floor(Math.random() * 1000000),
      });
      if (res.success && res.image_url) {
        setImageUrl(res.image_url);
        setEnhancedPrompt(res.enhanced_prompt);
      }
    } catch (e) {
      console.error('Realistic generation error:', e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = async () => {
    if (!imageUrl) return;
    try {
      const resp = await fetch(imageUrl);
      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `realistic_render_${Date.now()}.jpg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch {
      window.open(imageUrl, '_blank');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-dark-950/80 backdrop-blur-xl animate-fade-in">
      <div className="relative w-full max-w-5xl bg-dark-900 border border-white/15 rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh]">
        
        {/* Modal Top Bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-white/10 bg-dark-950/60">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-accent-cyan/20 to-primary-500/20 border border-accent-cyan/30 flex items-center justify-center text-accent-cyan shadow-lg">
              <Camera className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="font-display font-bold text-lg text-white">Ultra-Realistic AI 3D & Photographic Render</h2>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 uppercase">
                  Photoreal 8K
                </span>
              </div>
              <p className="text-xs text-slate-400">Unreal Engine 5 CGI, Blender renders & Hasselblad studio photography synthesis with ray-tracing</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {imageUrl && (
              <>
                <button
                  type="button"
                  onClick={() => setZoom((prev) => (prev >= 2 ? 1 : prev + 0.5))}
                  title="Toggle Zoom"
                  className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 hover:text-white transition-colors border border-white/10"
                >
                  {zoom > 1 ? <ZoomOut className="w-4 h-4" /> : <ZoomIn className="w-4 h-4" />}
                </button>
                <button
                  type="button"
                  onClick={handleDownload}
                  title="Download 8K Photographic Render"
                  className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-primary-500/20 hover:bg-primary-500/30 text-primary-300 hover:text-primary-200 border border-primary-500/30 text-xs font-semibold transition-all shadow-md"
                >
                  <Download className="w-4 h-4" />
                  <span className="hidden sm:inline">Save Image</span>
                </button>
              </>
            )}
            <button
              type="button"
              onClick={onClose}
              className="p-2 rounded-xl bg-white/5 hover:bg-white/10 text-slate-400 hover:text-white transition-colors border border-white/10 ml-2"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Body */}
        <div className="flex-1 overflow-y-auto p-6 flex flex-col gap-5">
          
          {/* Main Visual Display Area */}
          <div className="relative w-full aspect-video rounded-2xl bg-dark-950 border border-white/10 overflow-hidden flex items-center justify-center shadow-inner group">
            {isLoading ? (
              <div className="flex flex-col items-center gap-3 p-8 text-center">
                <div className="relative">
                  <div className="w-14 h-14 rounded-full border-2 border-primary-500/30 border-t-accent-cyan animate-spin" />
                  <Sparkles className="w-6 h-6 text-accent-cyan absolute inset-0 m-auto animate-pulse" />
                </div>
                <p className="font-semibold text-sm text-white">Synthesizing Photorealistic 8K Imagery...</p>
                <p className="text-xs text-slate-400 max-w-md">Simulating studio lighting caustics, cinematic depth-of-field, and ray-traced reflections</p>
              </div>
            ) : imageUrl ? (
              <div className="relative w-full h-full overflow-auto flex items-center justify-center">
                <img
                  src={imageUrl}
                  alt={prompt}
                  style={{ transform: `scale(${zoom})`, transformOrigin: 'center center', transition: 'transform 0.25s ease' }}
                  className="max-w-full max-h-full object-contain select-none"
                />
                <div className="absolute bottom-3 right-3 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <a
                    href={imageUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1 px-3 py-1.5 rounded-lg bg-dark-950/80 backdrop-blur border border-white/20 text-xs text-white hover:text-accent-cyan transition-colors"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    <span>Open Full 8K</span>
                  </a>
                </div>
              </div>
            ) : (
              <div className="text-center p-8">
                <Camera className="w-12 h-12 text-slate-600 mx-auto mb-2" />
                <p className="text-sm text-slate-300">Click Generate to synthesize an ultra-realistic photographic render.</p>
              </div>
            )}
          </div>

          {/* Photography Styles Bar */}
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-2 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-primary-400" />
              <span>Photography Lighting & Aesthetic Preset:</span>
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
              {STYLES.map((st) => (
                <button
                  key={st.id}
                  type="button"
                  onClick={() => {
                    setSelectedStyle(st.id);
                    handleGenerate(st.id);
                  }}
                  disabled={isLoading}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium border transition-all text-left ${
                    selectedStyle === st.id
                      ? 'bg-primary-500/20 border-primary-500/60 text-white shadow-md shadow-primary-500/10'
                      : 'bg-dark-950/60 border-white/10 text-slate-400 hover:text-slate-200 hover:border-white/20'
                  }`}
                >
                  <span className="text-sm">{st.icon}</span>
                  <span className="truncate">{st.name}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Prompt Editor & Regeneration Control */}
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="flex-1">
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your photographic scene..."
                className="w-full bg-dark-950 border border-white/15 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-primary-500/60 transition-colors"
              />
            </div>
            <button
              type="button"
              onClick={() => handleGenerate()}
              disabled={isLoading || !prompt.trim()}
              className="flex items-center justify-center gap-2 px-6 py-2.5 rounded-xl font-semibold text-xs sm:text-sm bg-gradient-to-r from-accent-cyan/80 to-primary-500 hover:from-accent-cyan hover:to-primary-600 text-dark-950 shadow-lg shadow-accent-cyan/20 transition-all disabled:opacity-50 cursor-pointer"
            >
              <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>Generate Realistic Image</span>
            </button>
          </div>

          {/* Enhanced AI Photography Directives Box */}
          {enhancedPrompt && (
            <div className="p-3.5 rounded-xl bg-dark-950/60 border border-white/10 text-xs">
              <div className="flex items-center gap-1.5 text-[11px] font-semibold text-accent-cyan mb-1">
                <Sparkles className="w-3.5 h-3.5" />
                <span>AI Cinematic Directives (Ray Tracing & Optics):</span>
              </div>
              <p className="text-slate-400 leading-relaxed italic">{enhancedPrompt}</p>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};
