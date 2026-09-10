import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, RefreshCw, Check, X, Volume2, Sparkles, Loader2 } from 'lucide-react';
import { useVoiceStore } from '../../store/useVoiceStore';
import { transcribeAudio } from '../../services/api';

interface VoiceRecorderProps {
  onTranscriptionComplete: (text: string, lang: string) => void;
  languageHint?: string;
}

export const VoiceRecorder: React.FC<VoiceRecorderProps> = ({
  onTranscriptionComplete,
  languageHint = 'en'
}) => {
  const { isRecording, setIsRecording, audioTranscript, setAudioTranscript } = useVoiceStore();
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
      if (audioContextRef.current) audioContextRef.current.close().catch(() => {});
    };
  }, []);

  const startWaveformVisualizer = (stream: MediaStream) => {
    const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
    audioContextRef.current = audioCtx;
    const analyser = audioCtx.createAnalyser();
    analyser.fftSize = 64;
    analyserRef.current = analyser;

    const source = audioCtx.createMediaStreamSource(stream);
    source.connect(analyser);

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const render = () => {
      animationFrameRef.current = requestAnimationFrame(render);
      analyser.getByteFrequencyData(dataArray);

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const barWidth = (canvas.width / bufferLength) * 2;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height * 0.85;
        ctx.fillStyle = `rgb(${99 + dataArray[i] / 2}, 102, 241)`;
        ctx.fillRect(x, (canvas.height - barHeight) / 2, barWidth - 1, barHeight);
        x += barWidth;
      }
    };
    render();
  };

  const startRecording = async () => {
    setErrorMsg(null);
    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      startWaveformVisualizer(stream);

      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorderRef.current = recorder;

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());
        if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
        await processAudio();
      };

      recorder.start(250);
      setIsRecording(true);
    } catch (err: any) {
      console.error('Microphone error:', err);
      setErrorMsg('Microphone access denied or unavailable. Please enable permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processAudio = async () => {
    setIsProcessing(true);
    try {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
      const reader = new FileReader();
      reader.readAsDataURL(audioBlob);
      reader.onloadend = async () => {
        const base64Audio = reader.result as string;
        try {
          const res = await transcribeAudio(base64Audio, languageHint);
          if (res.success && res.transcription) {
            setAudioTranscript(res.transcription);
            setShowConfirmModal(true);
          } else {
            setErrorMsg('Speech could not be recognized. Please speak clearly and try again.');
          }
        } catch (e: any) {
          setErrorMsg('Transcription service error. Please try again or type directly.');
        } finally {
          setIsProcessing(false);
        }
      };
    } catch (e) {
      setIsProcessing(false);
    }
  };

  const handleConfirm = () => {
    setShowConfirmModal(false);
    onTranscriptionComplete(audioTranscript, languageHint);
  };

  return (
    <div className="flex flex-col items-center">
      {/* Microphone Trigger Button */}
      {!isRecording && !isProcessing && (
        <button
          type="button"
          onClick={startRecording}
          title="Speak your prompt in Tamil, Hindi, English, etc."
          className="flex items-center gap-2 px-4 py-2.5 rounded-xl font-medium text-xs bg-slate-800/80 hover:bg-slate-700/80 text-white border border-white/10 shadow-lg hover:border-primary-500/50 transition-all group"
        >
          <Mic className="w-4 h-4 text-primary-400 group-hover:scale-110 transition-transform" />
          <span>Voice Command</span>
        </button>
      )}

      {/* Recording Waveform Active State */}
      {isRecording && (
        <div className="flex items-center gap-3 px-4 py-2 rounded-2xl glass-panel border border-primary-500/50 shadow-2xl shadow-primary-500/20 animate-pulse-slow">
          <div className="w-2.5 h-2.5 rounded-full bg-red-500 animate-ping" />
          <span className="text-xs font-semibold text-primary-300">Listening...</span>
          <canvas ref={canvasRef} width={120} height={24} className="rounded" />
          <button
            type="button"
            onClick={stopRecording}
            className="px-3 py-1 text-xs font-medium rounded-lg bg-red-500/20 text-red-300 hover:bg-red-500/30 transition-colors"
          >
            Done
          </button>
        </div>
      )}

      {/* Processing Spinner */}
      {isProcessing && (
        <div className="flex items-center gap-2 text-xs text-primary-300 px-4 py-2 rounded-xl glass-panel">
          <Loader2 className="w-4 h-4 animate-spin text-primary-400" />
          <span>Transcribing multilingual speech...</span>
        </div>
      )}

      {/* Error Message */}
      {errorMsg && (
        <p className="mt-2 text-[11px] text-red-400 bg-red-500/10 px-3 py-1 rounded-lg border border-red-500/20">
          {errorMsg}
        </p>
      )}

      {/* Confirmation Modal (Rule 41: Do not auto-generate after accidental mic input) */}
      {showConfirmModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md">
          <div className="glass-panel p-5 rounded-3xl border border-white/15 max-w-md w-full shadow-2xl animate-fade-in">
            <div className="flex items-center gap-2 mb-3 text-primary-400 text-xs font-semibold uppercase tracking-wider">
              <Sparkles className="w-4 h-4" />
              <span>Voice Transcription</span>
            </div>
            <p className="text-xs text-slate-400 mb-2">You said:</p>
            <div className="p-3.5 rounded-xl bg-dark-900/90 border border-white/10 text-sm font-medium text-white mb-5 italic">
              "{audioTranscript}"
            </div>
            <div className="flex items-center justify-end gap-2">
              <button
                type="button"
                onClick={() => { setShowConfirmModal(false); startRecording(); }}
                className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs text-slate-300 hover:text-white hover:bg-white/5 transition-colors"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Record Again</span>
              </button>
              <button
                type="button"
                onClick={() => setShowConfirmModal(false)}
                className="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
              >
                <X className="w-3.5 h-3.5" />
                <span>Cancel</span>
              </button>
              <button
                type="button"
                onClick={handleConfirm}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-gradient-to-r from-primary-500 to-indigo-600 hover:from-primary-600 hover:to-indigo-700 text-white shadow-lg shadow-primary-500/30 transition-all"
              >
                <Check className="w-3.5 h-3.5" />
                <span>Use & Generate</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
