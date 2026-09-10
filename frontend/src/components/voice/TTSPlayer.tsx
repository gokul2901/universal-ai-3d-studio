import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, Square, RotateCcw, Volume2, Loader2 } from 'lucide-react';
import { SUPPORTED_LANGUAGES } from '../../i18n';
import { getTTSStreamUrl } from '../../services/api';

interface TTSPlayerProps {
  text: string;
  language?: string;
  autoPlay?: boolean;
}

const BCP47_MAP: Record<string, string> = {
  en: 'en-US',
  ta: 'ta-IN',
  hi: 'hi-IN',
  bn: 'bn-IN',
  te: 'te-IN',
  mr: 'mr-IN',
  ml: 'ml-IN',
  ur: 'ur-PK',
  es: 'es-ES',
  zh: 'zh-CN',
  ar: 'ar-SA',
  fr: 'fr-FR',
  pt: 'pt-BR',
  ru: 'ru-RU',
  de: 'de-DE',
  ja: 'ja-JP',
};

export const TTSPlayer: React.FC<TTSPlayerProps> = ({
  text,
  language = 'en',
  autoPlay = false
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [isLoadingAudio, setIsLoadingAudio] = useState(false);

  const audioRef = useRef<HTMLAudioElement | null>(null);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  const langMeta = SUPPORTED_LANGUAGES.find(l => l.code === language) || SUPPORTED_LANGUAGES[0];

  useEffect(() => {
    return () => {
      stop();
    };
  }, []);

  const fallbackBrowserSpeech = () => {
    if (!('speechSynthesis' in window) || !text) return;
    try {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utteranceRef.current = utterance;

      const targetTag = BCP47_MAP[langMeta.code] || langMeta.code;
      utterance.lang = targetTag;
      utterance.rate = 0.95;

      const voices = window.speechSynthesis.getVoices();
      const matchingVoice = voices.find(v =>
        v.lang.toLowerCase() === targetTag.toLowerCase() ||
        v.lang.toLowerCase().startsWith(langMeta.code.toLowerCase())
      );
      if (matchingVoice) utterance.voice = matchingVoice;

      utterance.onstart = () => {
        setIsLoadingAudio(false);
        setIsPlaying(true);
        setIsPaused(false);
      };
      utterance.onend = () => {
        setIsPlaying(false);
        setIsPaused(false);
      };
      utterance.onerror = () => {
        setIsPlaying(false);
        setIsPaused(false);
        setIsLoadingAudio(false);
      };

      window.speechSynthesis.speak(utterance);
    } catch (e) {
      setIsPlaying(false);
      setIsPaused(false);
      setIsLoadingAudio(false);
    }
  };

  const speak = () => {
    if (!text.trim()) return;

    stop();
    setIsLoadingAudio(true);

    try {
      // 1. High-fidelity native speech via backend MP3 stream
      const streamUrl = getTTSStreamUrl(text, langMeta.code);
      const audio = new Audio(streamUrl);
      audioRef.current = audio;

      audio.onplay = () => {
        setIsLoadingAudio(false);
        setIsPlaying(true);
        setIsPaused(false);
      };

      audio.onpause = () => {
        setIsPlaying(false);
        setIsPaused(true);
      };

      audio.onended = () => {
        setIsPlaying(false);
        setIsPaused(false);
      };

      audio.onerror = (e) => {
        console.warn('Backend TTS stream encountered error, using browser synthesis fallback.', e);
        fallbackBrowserSpeech();
      };

      audio.play().catch((err) => {
        console.warn('Audio play prevented or failed, trying browser synthesis:', err);
        fallbackBrowserSpeech();
      });
    } catch (err) {
      fallbackBrowserSpeech();
    }
  };

  const pause = () => {
    if (audioRef.current && isPlaying) {
      audioRef.current.pause();
      setIsPaused(true);
      setIsPlaying(false);
    } else if ('speechSynthesis' in window && isPlaying) {
      window.speechSynthesis.pause();
      setIsPaused(true);
      setIsPlaying(false);
    }
  };

  const resume = () => {
    if (audioRef.current && isPaused) {
      audioRef.current.play().catch(() => speak());
      setIsPaused(false);
      setIsPlaying(true);
    } else if ('speechSynthesis' in window && isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
      setIsPlaying(true);
    } else {
      speak();
    }
  };

  const stop = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    setIsPlaying(false);
    setIsPaused(false);
    setIsLoadingAudio(false);
  };

  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl glass-panel border border-white/10 text-xs w-fit shadow-md">
      <div className={`p-1 rounded-lg ${isPlaying ? 'bg-primary-500/20 text-primary-400 animate-pulse' : 'text-slate-400'}`}>
        <Volume2 className="w-3.5 h-3.5" />
      </div>

      <span className="text-[11px] text-slate-300 font-medium mr-1">
        {isLoadingAudio
          ? `Loading Voice (${langMeta.name})...`
          : isPlaying
          ? `Speaking in ${langMeta.name}...`
          : `Voice (${langMeta.name})`}
      </span>

      {/* Play / Pause Toggle */}
      {isLoadingAudio ? (
        <Loader2 className="w-3.5 h-3.5 animate-spin text-primary-400" />
      ) : !isPlaying ? (
        <button
          type="button"
          onClick={resume}
          title={`Play ${langMeta.name} explanation audio`}
          className="p-1 rounded-md text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
        >
          <Play className="w-3.5 h-3.5 fill-current text-primary-400" />
        </button>
      ) : (
        <button
          type="button"
          onClick={pause}
          title="Pause audio"
          className="p-1 rounded-md text-slate-300 hover:text-white hover:bg-white/10 transition-colors"
        >
          <Pause className="w-3.5 h-3.5" />
        </button>
      )}

      {/* Stop */}
      <button
        type="button"
        onClick={stop}
        title="Stop speech"
        className="p-1 rounded-md text-slate-400 hover:text-red-400 hover:bg-white/10 transition-colors"
      >
        <Square className="w-3 h-3 fill-current" />
      </button>

      {/* Replay */}
      <button
        type="button"
        onClick={speak}
        title="Replay from beginning"
        className="p-1 rounded-md text-slate-400 hover:text-primary-300 hover:bg-white/10 transition-colors"
      >
        <RotateCcw className="w-3 h-3" />
      </button>
    </div>
  );
};

