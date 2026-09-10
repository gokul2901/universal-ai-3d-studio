import React, { useState } from 'react';
import {
  Pointer, Move, RotateCw, Maximize2, Grid, Box, Sun,
  Layers, Play, Pause, Camera, Eye, Download, RefreshCw, Sparkles, Image as ImageIcon
} from 'lucide-react';
import { useSceneStore } from '../../store/useSceneStore';

interface SceneToolbarProps {
  onCaptureScreenshot: () => void;
  onExportGLB: () => void;
  onOpenRealisticModal?: () => void;
}

export const SceneToolbar: React.FC<SceneToolbarProps> = ({
  onCaptureScreenshot,
  onExportGLB,
  onOpenRealisticModal
}) => {
  const {
    transformMode, setTransformMode,
    explodedProgress, setExplodedProgress,
    cameraMode, setCameraMode,
    showGrid, toggleGrid,
    wireframe, toggleWireframe,
    isPlayingAnimation, toggleAnimation,
    currentScene
  } = useSceneStore();

  const [showCameraMenu, setShowCameraMenu] = useState(false);
  const [showExplodedSlider, setShowExplodedSlider] = useState(false);

  // Check if current scene or selected object has components for exploded view
  const canExplode = currentScene?.objects.some(obj => obj.components && obj.components.length > 0);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      document.exitFullscreen().catch(() => {});
    }
  };

  return (
    <div className="absolute top-4 left-4 z-20 flex flex-col gap-2">
      {/* Primary Transformation & View Bar */}
      <div className="flex items-center gap-1.5 p-1.5 glass-panel rounded-2xl shadow-2xl border border-white/10 backdrop-blur-xl">
        {/* Select */}
        <button
          onClick={() => setTransformMode('select')}
          title="Select Object (V)"
          className={`p-2.5 rounded-xl transition-all ${
            transformMode === 'select'
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/30'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <Pointer className="w-4 h-4" />
        </button>

        {/* Move */}
        <button
          onClick={() => setTransformMode('translate')}
          title="Translate / Move Gizmo (W)"
          className={`p-2.5 rounded-xl transition-all ${
            transformMode === 'translate'
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/30'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <Move className="w-4 h-4" />
        </button>

        {/* Rotate */}
        <button
          onClick={() => setTransformMode('rotate')}
          title="Rotate Gizmo (E)"
          className={`p-2.5 rounded-xl transition-all ${
            transformMode === 'rotate'
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/30'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <RotateCw className="w-4 h-4" />
        </button>

        {/* Scale */}
        <button
          onClick={() => setTransformMode('scale')}
          title="Scale Gizmo (R)"
          className={`p-2.5 rounded-xl transition-all ${
            transformMode === 'scale'
              ? 'bg-primary-500 text-white shadow-lg shadow-primary-500/30'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <Maximize2 className="w-4 h-4" />
        </button>

        <div className="w-px h-5 bg-white/10 mx-1" />

        {/* Exploded View Toggle */}
        <button
          onClick={() => setShowExplodedSlider(!showExplodedSlider)}
          title={canExplode ? "Exploded View Controls" : "No compound components to explode"}
          disabled={!canExplode}
          className={`p-2.5 rounded-xl transition-all ${
            showExplodedSlider || explodedProgress > 0
              ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30'
              : canExplode
              ? 'text-slate-300 hover:text-white hover:bg-white/5'
              : 'text-slate-600 cursor-not-allowed'
          }`}
        >
          <Layers className="w-4 h-4" />
        </button>

        {/* Play/Pause Animation */}
        <button
          onClick={toggleAnimation}
          title={isPlayingAnimation ? "Pause Animation" : "Play Animation"}
          className={`p-2.5 rounded-xl transition-all ${
            isPlayingAnimation
              ? 'text-accent-emerald hover:bg-white/5'
              : 'text-slate-400 hover:text-white hover:bg-white/5'
          }`}
        >
          {isPlayingAnimation ? <Play className="w-4 h-4 fill-current" /> : <Pause className="w-4 h-4" />}
        </button>

        {/* Wireframe */}
        <button
          onClick={toggleWireframe}
          title="Toggle Wireframe Mode"
          className={`p-2.5 rounded-xl transition-all ${
            wireframe
              ? 'bg-accent-cyan text-white shadow-lg shadow-accent-cyan/30'
              : 'text-slate-300 hover:text-white hover:bg-white/5'
          }`}
        >
          <Box className="w-4 h-4" />
        </button>

        {/* Grid */}
        <button
          onClick={toggleGrid}
          title="Toggle Floor Grid"
          className={`p-2.5 rounded-xl transition-all ${
            showGrid
              ? 'text-primary-400 bg-primary-500/10'
              : 'text-slate-500 hover:text-white hover:bg-white/5'
          }`}
        >
          <Grid className="w-4 h-4" />
        </button>

        <div className="w-px h-5 bg-white/10 mx-1" />

        {/* Camera Views dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowCameraMenu(!showCameraMenu)}
            title="Camera Perspective & Orthographic Angles"
            className={`p-2.5 rounded-xl transition-all ${
              cameraMode !== 'perspective'
                ? 'bg-purple-600 text-white'
                : 'text-slate-300 hover:text-white hover:bg-white/5'
            }`}
          >
            <Eye className="w-4 h-4" />
          </button>

          {showCameraMenu && (
            <div className="absolute top-12 left-0 w-36 glass-panel rounded-xl p-1.5 shadow-2xl border border-white/10 flex flex-col gap-1 z-30">
              <button
                onClick={() => { setCameraMode('perspective'); setShowCameraMenu(false); }}
                className={`text-left text-xs px-2.5 py-1.5 rounded-lg transition-colors ${cameraMode === 'perspective' ? 'bg-primary-500 text-white' : 'text-slate-300 hover:bg-white/5'}`}
              >
                Perspective
              </button>
              <button
                onClick={() => { setCameraMode('isometric'); setShowCameraMenu(false); }}
                className={`text-left text-xs px-2.5 py-1.5 rounded-lg transition-colors ${cameraMode === 'isometric' ? 'bg-primary-500 text-white' : 'text-slate-300 hover:bg-white/5'}`}
              >
                Isometric
              </button>
              <button
                onClick={() => { setCameraMode('front'); setShowCameraMenu(false); }}
                className={`text-left text-xs px-2.5 py-1.5 rounded-lg transition-colors ${cameraMode === 'front' ? 'bg-primary-500 text-white' : 'text-slate-300 hover:bg-white/5'}`}
              >
                Front View
              </button>
              <button
                onClick={() => { setCameraMode('top'); setShowCameraMenu(false); }}
                className={`text-left text-xs px-2.5 py-1.5 rounded-lg transition-colors ${cameraMode === 'top' ? 'bg-primary-500 text-white' : 'text-slate-300 hover:bg-white/5'}`}
              >
                Top View
              </button>
              <button
                onClick={() => { setCameraMode('side'); setShowCameraMenu(false); }}
                className={`text-left text-xs px-2.5 py-1.5 rounded-lg transition-colors ${cameraMode === 'side' ? 'bg-primary-500 text-white' : 'text-slate-300 hover:bg-white/5'}`}
              >
                Side View
              </button>
            </div>
          )}
        </div>

        {/* Realistic 8K Photographic Render Button */}
        {onOpenRealisticModal && (
          <button
            onClick={onOpenRealisticModal}
            title="Generate Ultra-Realistic 8K Photographic Image"
            className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-gradient-to-r from-accent-cyan/20 to-primary-500/20 hover:from-accent-cyan/30 hover:to-primary-500/30 text-accent-cyan border border-accent-cyan/40 text-xs font-semibold shadow-lg shadow-accent-cyan/10 transition-all cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5 text-accent-cyan animate-pulse" />
            <span className="hidden sm:inline">Realistic 8K Render</span>
          </button>
        )}

        {/* Screenshot */}
        <button
          onClick={onCaptureScreenshot}
          title="Capture High-Res Screenshot PNG"
          className="p-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-white/5 transition-all"
        >
          <Camera className="w-4 h-4" />
        </button>

        {/* Fullscreen */}
        <button
          onClick={toggleFullscreen}
          title="Toggle Fullscreen"
          className="p-2.5 rounded-xl text-slate-300 hover:text-white hover:bg-white/5 transition-all"
        >
          <Maximize2 className="w-4 h-4" />
        </button>
      </div>

      {/* Exploded View Slider Floating Popup */}
      {showExplodedSlider && canExplode && (
        <div className="p-3 glass-panel rounded-2xl shadow-2xl border border-white/10 w-72 backdrop-blur-xl animate-fade-in">
          <div className="flex items-center justify-between text-xs font-semibold text-slate-300 mb-2">
            <span className="flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-indigo-400" />
              Exploded View Expansion
            </span>
            <span className="font-mono text-indigo-400">
              {Math.round(explodedProgress * 100)}%
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={explodedProgress}
            onChange={(e) => setExplodedProgress(parseFloat(e.target.value))}
            className="w-full accent-indigo-500 h-1.5 bg-slate-700/80 rounded-lg cursor-pointer"
          />
          <div className="flex justify-between items-center mt-2 text-[11px] text-slate-400">
            <button
              onClick={() => setExplodedProgress(0)}
              className="hover:text-white px-2 py-0.5 rounded bg-white/5 transition-colors"
            >
              Assembled (0%)
            </button>
            <button
              onClick={() => setExplodedProgress(1)}
              className="hover:text-white px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-300 transition-colors"
            >
              Explode (100%)
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
