import React, { useState, useRef, useEffect } from 'react';
import { Globe, ChevronDown, Check } from 'lucide-react';
import { SUPPORTED_LANGUAGES, LanguageMeta } from '../../i18n';
import { useUIStore } from '../../store/useUIStore';

export const LanguageSelector: React.FC = () => {
  const { language, setLanguage } = useUIStore();
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentLang = SUPPORTED_LANGUAGES.find((l) => l.code === language) || SUPPORTED_LANGUAGES[0];

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const selectLanguage = (code: string) => {
    setLanguage(code);
    setIsOpen(false);
  };

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Trigger Button */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 bg-[#0d1322] hover:bg-[#161f36] px-3 py-1.5 rounded-xl border border-white/15 text-xs text-slate-200 transition-all shadow-md group"
      >
        <Globe className="w-3.5 h-3.5 text-primary-400 shrink-0 group-hover:rotate-12 transition-transform" />
        <span className="font-medium max-w-[120px] truncate text-left">
          {currentLang.name} — <span className="text-primary-300 font-normal">{currentLang.nativeName}</span>
        </span>
        <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform duration-200 shrink-0 ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Floating Custom Dropdown Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 max-h-96 overflow-y-auto bg-[#0a0f1d] border border-white/15 rounded-2xl shadow-2xl p-2 z-50 backdrop-blur-2xl animate-fade-in divide-y divide-white/10">
          {/* Indian Languages Section */}
          <div className="pb-2">
            <div className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-primary-400">
              Indian Languages
            </div>
            <div className="space-y-0.5 mt-1">
              {SUPPORTED_LANGUAGES.filter((l) => l.category === 'Indian').map((l) => {
                const isSelected = l.code === language;
                return (
                  <button
                    key={l.code}
                    type="button"
                    onClick={() => selectLanguage(l.code)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs text-left transition-colors ${
                      isSelected
                        ? 'bg-primary-500/25 text-white font-semibold border border-primary-500/40'
                        : 'text-slate-200 hover:bg-white/10 hover:text-white'
                    }`}
                  >
                    <div className="flex flex-col">
                      <span className="text-white font-medium">{l.name}</span>
                      <span className="text-[11px] text-primary-300">{l.nativeName}</span>
                    </div>
                    {isSelected && <Check className="w-4 h-4 text-primary-400" />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* International Languages Section */}
          <div className="pt-2">
            <div className="px-2.5 py-1 text-[10px] font-bold uppercase tracking-wider text-accent-cyan">
              International Languages
            </div>
            <div className="space-y-0.5 mt-1">
              {SUPPORTED_LANGUAGES.filter((l) => l.category === 'International').map((l) => {
                const isSelected = l.code === language;
                return (
                  <button
                    key={l.code}
                    type="button"
                    onClick={() => selectLanguage(l.code)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs text-left transition-colors ${
                      isSelected
                        ? 'bg-primary-500/25 text-white font-semibold border border-primary-500/40'
                        : 'text-slate-200 hover:bg-white/10 hover:text-white'
                    }`}
                  >
                    <div className="flex flex-col">
                      <span className="text-white font-medium">{l.name}</span>
                      <span className="text-[11px] text-accent-cyan/80">{l.nativeName}</span>
                    </div>
                    {isSelected && <Check className="w-4 h-4 text-primary-400" />}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
