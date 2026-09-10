import React, { useRef, useState, Suspense, Component } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, Environment, ContactShadows } from '@react-three/drei';
import * as THREE from 'three';
import { useSceneStore } from '../../store/useSceneStore';
import { SceneObject } from './SceneObject';
import { TransformController } from './TransformController';
import { CameraController } from './CameraController';
import { SceneToolbar } from './SceneToolbar';
import { RealisticImageModal } from '../ai/RealisticImageModal';
import { Loader2, AlertTriangle, RefreshCw } from 'lucide-react';

// Top-level Canvas error boundary — prevents complete black screen on Three.js crash
class CanvasErrorBoundary extends Component<
  { children: React.ReactNode },
  { hasError: boolean; errorMsg: string }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false, errorMsg: '' };
  }
  static getDerivedStateFromError(error: any) {
    return { hasError: true, errorMsg: error?.message || 'Unknown render error' };
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="w-full h-full flex flex-col items-center justify-center bg-dark-950 text-white gap-4 p-8">
          <div className="w-14 h-14 rounded-2xl bg-red-500/20 border border-red-500/40 flex items-center justify-center">
            <AlertTriangle className="w-7 h-7 text-red-400" />
          </div>
          <div className="text-center max-w-xs">
            <h3 className="font-semibold text-base mb-1">3D Viewport Error</h3>
            <p className="text-xs text-slate-400 mb-4">{this.state.errorMsg}</p>
            <button
              onClick={() => this.setState({ hasError: false, errorMsg: '' })}
              className="flex items-center gap-2 mx-auto px-4 py-2 rounded-xl bg-primary-500/20 hover:bg-primary-500/30 border border-primary-500/40 text-primary-300 text-xs font-semibold transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Retry
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}

interface ThreeDViewportProps {
  onCaptureScreenshot?: () => void;
}

export const ThreeDViewport: React.FC<ThreeDViewportProps> = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const { currentScene, showGrid, showAxes, selectObject } = useSceneStore();
  const [showRealisticModal, setShowRealisticModal] = useState(false);

  const handleCaptureScreenshot = () => {
    if (!canvasRef.current) return;
    try {
      const dataUrl = canvasRef.current.toDataURL('image/png');
      const link = document.createElement('a');
      link.download = `${(currentScene?.title || 'universal_3d').replace(/\s+/g, '_').toLowerCase()}_render.png`;
      link.href = dataUrl;
      link.click();
    } catch (e) {
      console.error('Screenshot error:', e);
    }
  };

  const handleExportGLB = () => {
    // Scene JSON backup export
    if (!currentScene) return;
    const jsonStr = JSON.stringify(currentScene, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.download = `${currentScene.title.replace(/\s+/g, '_').toLowerCase()}_scene.json`;
    link.href = url;
    link.click();
    URL.revokeObjectURL(url);
  };

  const env = currentScene?.environment || {
    sky_color: '#06080e',
    ground_color: '#0b0f19',
    fog_density: 0.015,
    ambient_color: '#ffffff',
    ambient_intensity: 0.8
  };

  const lights = currentScene?.lighting || [
    { type: 'directional', color: '#ffffff', intensity: 2.0, position: [6, 12, 8] },
    { type: 'ambient', color: '#818cf8', intensity: 0.4 }
  ];

  return (
    <div
      className="relative w-full h-full overflow-hidden bg-dark-950 select-none"
      onClick={() => selectObject(null)}
    >
      {/* Floating 3D Toolbar */}
      <SceneToolbar
        onCaptureScreenshot={handleCaptureScreenshot}
        onExportGLB={handleExportGLB}
        onOpenRealisticModal={() => setShowRealisticModal(true)}
      />

      {/* R3F Canvas — wrapped in error boundary to prevent black screen */}
      <CanvasErrorBoundary>
        <Canvas
          ref={canvasRef}
          dpr={[1, 1.5]}
          performance={{ min: 0.5 }}
          gl={{
            preserveDrawingBuffer: true,
            antialias: true,
            alpha: true,
            powerPreference: 'high-performance',
            toneMapping: THREE.ACESFilmicToneMapping,
            toneMappingExposure: 1.15
          }}
          shadows
          camera={{ position: [0, 4, 10], fov: 45 }}
          className="w-full h-full"
        >
          <color attach="background" args={[env.sky_color]} />
          <fog attach="fog" args={[env.fog_color || env.sky_color, 12, 38]} />

          {/* Dynamic Lights from Scene Planner */}
          {lights.map((l, idx) => {
            if (l.type === 'directional') {
              return (
                <directionalLight
                  key={idx}
                  color={l.color}
                  intensity={l.intensity}
                  position={l.position || [5, 10, 5]}
                  castShadow
                  shadow-mapSize-width={1024}
                  shadow-mapSize-height={1024}
                  shadow-bias={-0.0001}
                />
              );
            } else if (l.type === 'spot') {
              return (
                <spotLight
                  key={idx}
                  color={l.color}
                  intensity={l.intensity}
                  position={l.position || [0, 8, 4]}
                  angle={0.6}
                  penumbra={0.5}
                  castShadow
                />
              );
            } else if (l.type === 'point') {
              return (
                <pointLight
                  key={idx}
                  color={l.color}
                  intensity={l.intensity}
                  position={l.position || [0, 3, 0]}
                />
              );
            } else {
              return (
                <ambientLight
                  key={idx}
                  color={l.color}
                  intensity={l.intensity}
                />
              );
            }
          })}

          {/* Ground Plane Grid */}
          {showGrid && (
            <Grid
              position={[0, -0.01, 0]}
              args={[30, 30]}
              cellSize={0.8}
              cellThickness={0.7}
              cellColor="#1e293b"
              sectionSize={4}
              sectionThickness={1.2}
              sectionColor="#334155"
              fadeDistance={25}
              fadeStrength={1.5}
            />
          )}

          {/* Axes Helper */}
          {showAxes && <primitive object={new THREE.AxesHelper(3)} position={[0, 0.01, 0]} />}

          <Suspense fallback={null}>
            {/* Studio HDR Environment for Photorealistic Metallic & Dielectric Reflections */}
            <Environment preset="city" />

            {/* Soft Ground Contact Shadows */}
            <ContactShadows
              position={[0, -0.015, 0]}
              opacity={0.65}
              scale={22}
              blur={1.8}
              far={6}
            />

            {/* Render Scene Objects */}
            {currentScene?.objects.map((obj) => (
              <SceneObject key={obj.id} objectData={obj} />
            ))}

            {/* Gizmo Controls */}
            <TransformController />

            {/* Animated Camera Mode Handler */}
            <CameraController />
          </Suspense>

          {/* Orbit Controls */}
          <OrbitControls
            makeDefault
            enableDamping
            dampingFactor={0.05}
            maxPolarAngle={Math.PI / 2 - 0.01}
            minDistance={1.5}
            maxDistance={40}
          />
        </Canvas>
      </CanvasErrorBoundary>

      {/* Realistic 8K Photographic Render Modal */}
      <RealisticImageModal
        isOpen={showRealisticModal}
        onClose={() => setShowRealisticModal(false)}
        initialImageUrl={currentScene?.realistic_image_url}
        initialPrompt={currentScene?.user_prompt || currentScene?.title}
      />

      {/* Empty State Overlay */}
      {(!currentScene || currentScene.objects.length === 0) && (
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none p-6 text-center">
          <div className="p-4 rounded-3xl glass-panel border border-white/10 max-w-sm pointer-events-auto">
            <div className="w-12 h-12 rounded-2xl bg-primary-500/20 text-primary-400 flex items-center justify-center mx-auto mb-3">
              <Loader2 className="w-6 h-6 animate-spin" />
            </div>
            <h3 className="font-display font-semibold text-lg text-white mb-1">
              Your 3D Workspace is Ready
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Describe any scene, upload a reference image, or choose a preset demo to populate your interactive world.
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

