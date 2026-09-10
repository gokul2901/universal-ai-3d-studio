import { create } from 'zustand';

interface VoiceState {
  isRecording: boolean;
  audioTranscript: string;
  isTranscribing: boolean;
  isSpeaking: boolean;
  activeAudioText: string;
  setIsRecording: (val: boolean) => void;
  setAudioTranscript: (val: string) => void;
  setIsTranscribing: (val: boolean) => void;
  setIsSpeaking: (val: boolean) => void;
  setActiveAudioText: (val: string) => void;
}

export const useVoiceStore = create<VoiceState>((set) => ({
  isRecording: false,
  audioTranscript: '',
  isTranscribing: false,
  isSpeaking: false,
  activeAudioText: '',
  setIsRecording: (isRecording) => set({ isRecording }),
  setAudioTranscript: (audioTranscript) => set({ audioTranscript }),
  setIsTranscribing: (isTranscribing) => set({ isTranscribing }),
  setIsSpeaking: (isSpeaking) => set({ isSpeaking }),
  setActiveAudioText: (activeAudioText) => set({ activeAudioText }),
}));
