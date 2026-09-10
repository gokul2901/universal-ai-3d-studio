import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, FastForward, Activity } from 'lucide-react';
import { useSceneStore } from '../../store/useSceneStore';

export const AnimationTimeline: React.FC = () => {
  const { isPlayingAnimation, toggleAnimation, animationSpeed, setAnimationSpeed, currentScene, selectedObjectId } = useSceneStore();
  const [currentTime, setCurrentTime] = useState(0);

  const activeObj = currentScene?.objects.find(o => o.id === selectedObjectId) || currentScene?.objects[0];
  const hasAnimation = activeObj?.animation && activeObj.animation.type !== 'none';

  useEffect(() => {
    let interval: any;
    if (isPlayingAnimation) {
      interval = setInterval(() => {
        setCurrentTime((prev) => (prev >= 20 ? 0 : prev + 0.1 * animationSpeed));
      }, 100);
    }
    return () => clearInterval(interval);
  }, [isPlayingAnimation, animationSpeed]);

  const formatTime = (seconds: number) => {
    const s = Math.floor(seconds);
    const ms = Math.floor((seconds - s) * 10);
    return `00:${s.toString().padStart(2, '0')}.${ms}`;
  };

  const handleSpeedCycle = () => {
    if (animationSpeed === 1.0) setAnimationSpeed(1.5);
    else if (animationSpeed === 1.5) setAnimationSpeed(2.0);
    else if (animationSpeed === 2.0) setAnimationSpeed(0.5);
    else setAnimationSpeed(1.0);
  };

  return (
    <div className="flex items-center justify-between px-4 py-2 glass-panel border-t border-white/10 text-xs backdrop-blur-xl">
      {/* Play Controls & Time */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={toggleAnimation}
          title={isPlayingAnimation ? "Pause Timeline" : "Play Timeline"}
          className="p-1.5 rounded-lg bg-primary-500/20 hover:bg-primary-500/30 text-primary-400 border border-primary-500/30 transition-all"
        >
          {isPlayingAnimation ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5 fill-current" />}
        </button>

        <button
          type="button"
          onClick={() => setCurrentTime(0)}
          title="Restart Animation"
          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/5 transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" />
        </button>

        <span className="font-mono text-[11px] text-slate-300 w-16">
          {formatTime(currentTime)}
        </span>
      </div>

      {/* Scrub Bar */}
      <div className="flex-1 max-w-md mx-6 flex items-center gap-2">
        <input
          type="range"
          min="0"
          max="20"
          step="0.1"
          value={currentTime}
          onChange={(e) => setCurrentTime(parseFloat(e.target.value))}
          className="w-full accent-primary-500 h-1.5 bg-slate-700/70 rounded-lg cursor-pointer"
        />
        <span className="font-mono text-[11px] text-slate-500">00:20.0</span>
      </div>

      {/* Target & Speed Control */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
          <Activity className="w-3.5 h-3.5 text-indigo-400" />
          <span className="truncate max-w-[120px]">
            {activeObj ? `${activeObj.name} (${activeObj.animation?.type || 'static'})` : 'Global Scene'}
          </span>
        </div>

        <button
          type="button"
          onClick={handleSpeedCycle}
          title="Toggle playback speed"
          className="px-2 py-0.5 rounded-md font-mono text-[10px] bg-white/5 hover:bg-white/10 text-slate-300 border border-white/10 transition-colors"
        >
          {animationSpeed}x
        </button>
      </div>
    </div>
  );
};
