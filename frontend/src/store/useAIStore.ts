import { create } from 'zustand';
import { ChatMessage, GenerationProgressStep } from '../types';

interface AIState {
  messages: ChatMessage[];
  isGenerating: boolean;
  currentStep: number;
  generationSteps: GenerationProgressStep[];
  isExplaining: boolean;
  lastExplanation: string;
  addMessage: (msg: ChatMessage) => void;
  setIsGenerating: (val: boolean) => void;
  setCurrentStep: (step: number) => void;
  setGenerationSteps: (steps: GenerationProgressStep[]) => void;
  setIsExplaining: (val: boolean) => void;
  setLastExplanation: (text: string) => void;
  clearMessages: () => void;
}

export const useAIStore = create<AIState>((set) => ({
  messages: [
    {
      id: 'welcome',
      sender: 'ai',
      text: 'Welcome to Universal AI 3D Studio. I can generate any 3D environment, inspect components, explode mechanical structures, or modify geometry with natural language commands.',
      timestamp: new Date().toLocaleTimeString(),
    }
  ],
  isGenerating: false,
  currentStep: 0,
  generationSteps: [],
  isExplaining: false,
  lastExplanation: '',
  addMessage: (msg) => set((state) => ({ messages: [...state.messages, msg] })),
  setIsGenerating: (isGenerating) => set({ isGenerating }),
  setCurrentStep: (currentStep) => set({ currentStep }),
  setGenerationSteps: (generationSteps) => set({ generationSteps }),
  setIsExplaining: (isExplaining) => set({ isExplaining }),
  setLastExplanation: (lastExplanation) => set({ lastExplanation }),
  clearMessages: () => set({ messages: [] }),
}));
