import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Box, Globe, RotateCcw, RotateCw, Sparkles, FolderKanban, Settings as SettingsIcon, PlusCircle } from 'lucide-react';
import { SUPPORTED_LANGUAGES, t } from '../../i18n';
import { useUIStore } from '../../store/useUIStore';
import { useSceneStore } from '../../store/useSceneStore';
import { LanguageSelector } from './LanguageSelector';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const { language, setLanguage } = useUIStore();
  const { undo, redo, past, future } = useSceneStore();
  const isStudio = location.pathname.startsWith('/studio');

  return (
    <nav className="h-14 px-4 glass-panel border-b border-white/10 flex items-center justify-between z-30 sticky top-0 backdrop-blur-xl">
      {/* Brand */}
      <Link to="/" className="flex items-center gap-2.5 group">
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-primary-500 via-indigo-500 to-accent-cyan flex items-center justify-center shadow-lg shadow-primary-500/25 group-hover:scale-105 transition-transform">
          <Box className="w-4 h-4 text-white" />
        </div>
        <div>
          <span className="font-display font-extrabold text-sm tracking-wider text-white">
            UNIVERSAL AI 3D
          </span>
          <span className="hidden sm:inline-block text-[10px] font-mono text-primary-400 ml-1.5 px-1.5 py-0.5 rounded bg-primary-500/10 border border-primary-500/20">
            STUDIO
          </span>
        </div>
      </Link>

      {/* Main Navigation Links */}
      <div className="flex items-center gap-1 sm:gap-2">
        <Link
          to="/create"
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
            location.pathname === '/create'
              ? 'bg-primary-500 text-white shadow-md shadow-primary-500/20'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <PlusCircle className="w-3.5 h-3.5" />
          <span>{t('nav_create', language)}</span>
        </Link>

        <Link
          to="/studio"
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
            location.pathname.startsWith('/studio')
              ? 'bg-primary-500 text-white shadow-md shadow-primary-500/20'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>{t('nav_studio', language)}</span>
        </Link>

        <Link
          to="/projects"
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
            location.pathname === '/projects'
              ? 'bg-primary-500 text-white shadow-md shadow-primary-500/20'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <FolderKanban className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">{t('nav_projects', language)}</span>
        </Link>
      </div>

      {/* Right Controls: Undo/Redo (in Studio), Language Picker, Settings */}
      <div className="flex items-center gap-2">
        {isStudio && (
          <div className="hidden sm:flex items-center gap-1 mr-2 bg-dark-900/60 p-1 rounded-xl border border-white/5">
            <button
              onClick={undo}
              disabled={past.length === 0}
              title="Undo (Ctrl+Z)"
              className="p-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-white/10 disabled:opacity-30 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={redo}
              disabled={future.length === 0}
              title="Redo (Ctrl+Y)"
              className="p-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-white/10 disabled:opacity-30 transition-colors"
            >
              <RotateCw className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* 16 Languages Selector */}
        <LanguageSelector />

        {/* Settings Link */}
        <Link
          to="/settings"
          title="Studio Settings"
          className="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
        >
          <SettingsIcon className="w-4 h-4" />
        </Link>
      </div>
    </nav>
  );
};
