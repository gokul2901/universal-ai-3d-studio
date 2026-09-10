import React, { useState } from 'react';
import { Settings as SettingsIcon, Globe, Volume2, Moon, Sun, Cpu, Eye, ShieldCheck } from 'lucide-react';
import { SUPPORTED_LANGUAGES, t } from '../i18n';
import { useUIStore } from '../store/useUIStore';
import { LanguageSelector } from '../components/ui/LanguageSelector';

export const SettingsPage: React.FC = () => {
  const { language, setLanguage, theme, setTheme } = useUIStore();
  const [quality3D, setQuality3D] = useState<'high' | 'medium' | 'low'>('high');
  const [autoPlayTTS, setAutoPlayTTS] = useState(true);
  const [showAiEstimates, setShowAiEstimates] = useState(true);
  const [reduceMotion, setReduceMotion] = useState(false);

  return (
    <div className="min-h-screen bg-dark-950 text-white p-6 sm:p-10 max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center gap-3 mb-8">
        <div className="w-10 h-10 rounded-2xl bg-primary-500/10 text-primary-400 flex items-center justify-center border border-primary-500/20 shadow-md">
          <SettingsIcon className="w-5 h-5" />
        </div>
        <div>
          <h1 className="font-display font-bold text-2xl sm:text-3xl text-white">
            {t('settings_title', language)}
          </h1>
          <p className="text-xs text-slate-400">
            {t('settings_subtitle', language)}
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {/* Language Selection (16 languages) */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <Globe className="w-4 h-4 text-primary-400" />
              <div>
                <h4 className="text-sm font-semibold text-white">{t('lang_pref_title', language)}</h4>
                <p className="text-[11px] text-slate-400">{t('lang_pref_desc', language)}</p>
              </div>
            </div>
            <LanguageSelector />
          </div>
        </div>

        {/* 3D Render Quality */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <Cpu className="w-4 h-4 text-accent-cyan" />
              <div>
                <h4 className="text-sm font-semibold text-white">{t('fidelity_title', language)}</h4>
                <p className="text-[11px] text-slate-400">{t('fidelity_desc', language)}</p>
              </div>
            </div>
            <div className="flex items-center gap-1 bg-dark-900/80 p-1 rounded-xl border border-white/10">
              {(['high', 'medium', 'low'] as const).map((q) => (
                <button
                  key={q}
                  type="button"
                  onClick={() => setQuality3D(q)}
                  className={`px-3 py-1 rounded-lg text-xs font-medium capitalize transition-colors ${
                    quality3D === q ? 'bg-primary-500 text-white' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Voice & TTS */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <Volume2 className="w-4 h-4 text-fuchsia-400" />
              <div>
                <h4 className="text-sm font-semibold text-white">{t('tts_toggle_title', language)}</h4>
                <p className="text-[11px] text-slate-400">{t('tts_toggle_desc', language)}</p>
              </div>
            </div>
            <input
              type="checkbox"
              checked={autoPlayTTS}
              onChange={(e) => setAutoPlayTTS(e.target.checked)}
              className="w-4 h-4 accent-primary-500 cursor-pointer rounded"
            />
          </div>
        </div>

        {/* AI Confidence & Inferred Label */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <ShieldCheck className="w-4 h-4 text-amber-400" />
              <div>
                <h4 className="text-sm font-semibold text-white">{t('badges_title', language)}</h4>
                <p className="text-[11px] text-slate-400">{t('badges_desc', language)}</p>
              </div>
            </div>
            <input
              type="checkbox"
              checked={showAiEstimates}
              onChange={(e) => setShowAiEstimates(e.target.checked)}
              className="w-4 h-4 accent-primary-500 cursor-pointer rounded"
            />
          </div>
        </div>

        {/* Reduce Motion */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 flex flex-col gap-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <Eye className="w-4 h-4 text-emerald-400" />
              <div>
                <h4 className="text-sm font-semibold text-white">{t('reduce_motion_title', language)}</h4>
                <p className="text-[11px] text-slate-400">{t('reduce_motion_desc', language)}</p>
              </div>
            </div>
            <input
              type="checkbox"
              checked={reduceMotion}
              onChange={(e) => setReduceMotion(e.target.checked)}
              className="w-4 h-4 accent-primary-500 cursor-pointer rounded"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
