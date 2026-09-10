import { create } from 'zustand';
import { isRTL } from '../i18n';

interface UIState {
  language: string;
  theme: 'dark' | 'light';
  activeTab: 'scene' | 'inspector' | 'copilot';
  isMobileDrawerOpen: boolean;
  setLanguage: (lang: string) => void;
  setTheme: (theme: 'dark' | 'light') => void;
  setActiveTab: (tab: 'scene' | 'inspector' | 'copilot') => void;
  setMobileDrawerOpen: (open: boolean) => void;
}

const getInitialLanguage = (): string => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('universal_3d_lang');
    if (saved) return saved;
  }
  return 'en';
};

export const useUIStore = create<UIState>((set) => ({
  language: getInitialLanguage(),
  theme: 'dark',
  activeTab: 'copilot',
  isMobileDrawerOpen: false,
  setLanguage: (language) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('universal_3d_lang', language);
      document.documentElement.lang = language;
      document.documentElement.dir = isRTL(language) ? 'rtl' : 'ltr';
    }
    set({ language });
  },
  setTheme: (theme) => set({ theme }),
  setActiveTab: (activeTab) => set({ activeTab }),
  setMobileDrawerOpen: (isMobileDrawerOpen) => set({ isMobileDrawerOpen }),
}));

