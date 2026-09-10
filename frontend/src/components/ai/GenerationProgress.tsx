import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, CheckCircle2, Loader2 } from 'lucide-react';
import { useAIStore } from '../../store/useAIStore';

export const GenerationProgress: React.FC = () => {
  const { isGenerating, currentStep } = useAIStore();

  const stages = [
    { title: "Analyzing multimodal input", subtitle: "Extracting prompts, visual anchors, and audio signals" },
    { title: "Understanding spatial intent", subtitle: "Identifying geometry categories and language requirements" },
    { title: "Planning 3D scene graph", subtitle: "Synthesizing generic transforms and relational boundaries" },
    { title: "Synthesizing PBR assets", subtitle: "Configuring roughness, metalness, and procedural shaders" },
    { title: "Building compound hierarchy", subtitle: "Assembling modular sub-components for exploded views" },
    { title: "Calibrating spatial lighting", subtitle: "Configuring directional shadows, ambient fill, and HDR mood" },
    { title: "Your 3D world is ready", subtitle: "Entering interactive WebGL studio..." }
  ];

  if (!isGenerating) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-xl p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="w-full max-w-md p-6 glass-panel rounded-3xl border border-white/15 shadow-2xl flex flex-col items-center text-center"
      >
        <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-tr from-primary-500 to-accent-cyan flex items-center justify-center mb-5 shadow-xl shadow-primary-500/20">
          <Sparkles className="w-8 h-8 text-white animate-pulse" />
        </div>

        <h3 className="font-display font-bold text-xl text-white mb-1">
          Architecting 3D Universe
        </h3>
        <p className="text-xs text-slate-400 mb-6">
          AI-native generative pipeline active
        </p>

        {/* 7-Step Progress List */}
        <div className="w-full space-y-2.5 text-left mb-4">
          {stages.map((stage, idx) => {
            const isDone = currentStep > idx;
            const isCurrent = currentStep === idx;

            return (
              <div
                key={idx}
                className={`flex items-center gap-3 p-2 rounded-xl transition-all ${
                  isCurrent
                    ? 'bg-primary-500/10 border border-primary-500/30'
                    : isDone
                    ? 'opacity-60'
                    : 'opacity-25'
                }`}
              >
                <div className="shrink-0">
                  {isDone ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : isCurrent ? (
                    <Loader2 className="w-4 h-4 text-primary-400 animate-spin" />
                  ) : (
                    <div className="w-4 h-4 rounded-full border border-slate-600" />
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <p className={`text-xs font-medium truncate ${isCurrent ? 'text-white' : 'text-slate-300'}`}>
                    {stage.title}
                  </p>
                  {isCurrent && (
                    <p className="text-[10px] text-primary-300 truncate">
                      {stage.subtitle}
                    </p>
                  )}
                </div>
                <span className="font-mono text-[10px] text-slate-500">
                  0{idx + 1}
                </span>
              </div>
            );
          })}
        </div>
      </motion.div>
    </div>
  );
};
