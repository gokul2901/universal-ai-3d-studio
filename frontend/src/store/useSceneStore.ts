import { create } from 'zustand';
import { ScenePlan, SceneObjectData } from '../types';

interface SceneState {
  currentScene: ScenePlan | null;
  selectedObjectId: string | null;
  transformMode: 'select' | 'translate' | 'rotate' | 'scale';
  explodedProgress: number; // 0.0 to 1.0
  cameraMode: 'perspective' | 'isometric' | 'top' | 'front' | 'side';
  showGrid: boolean;
  showAxes: boolean;
  wireframe: boolean;
  isPlayingAnimation: boolean;
  animationSpeed: number;
  
  // History for Undo / Redo
  past: ScenePlan[];
  future: ScenePlan[];

  setScene: (scene: ScenePlan) => void;
  selectObject: (id: string | null) => void;
  setTransformMode: (mode: 'select' | 'translate' | 'rotate' | 'scale') => void;
  setExplodedProgress: (val: number) => void;
  setCameraMode: (mode: 'perspective' | 'isometric' | 'top' | 'front' | 'side') => void;
  toggleGrid: () => void;
  toggleWireframe: () => void;
  toggleAnimation: () => void;
  setAnimationSpeed: (speed: number) => void;
  
  // Modifiers
  updateObjectTransform: (id: string, position?: [number, number, number], rotation?: [number, number, number], scale?: [number, number, number]) => void;
  updateObjectMaterial: (id: string, color: string) => void;
  deleteSelectedObject: () => void;
  
  // Undo / Redo
  undo: () => void;
  redo: () => void;
}

export const useSceneStore = create<SceneState>((set, get) => ({
  currentScene: null,
  selectedObjectId: null,
  transformMode: 'select',
  explodedProgress: 0.0,
  cameraMode: 'perspective',
  showGrid: true,
  showAxes: true,
  wireframe: false,
  isPlayingAnimation: true,
  animationSpeed: 1.0,
  past: [],
  future: [],

  setScene: (scene: ScenePlan) => {
    const { currentScene, past } = get();
    set({
      currentScene: scene,
      selectedObjectId: scene.objects.length > 0 ? scene.objects[0].id : null,
      explodedProgress: 0.0,
      past: currentScene ? [...past.slice(-20), currentScene] : past,
      future: [],
    });
  },

  selectObject: (selectedObjectId) => set({ selectedObjectId }),
  setTransformMode: (transformMode) => set({ transformMode }),
  setExplodedProgress: (explodedProgress) => set({ explodedProgress }),
  setCameraMode: (cameraMode) => set({ cameraMode }),
  toggleGrid: () => set((state) => ({ showGrid: !state.showGrid })),
  toggleWireframe: () => set((state) => ({ wireframe: !state.wireframe })),
  toggleAnimation: () => set((state) => ({ isPlayingAnimation: !state.isPlayingAnimation })),
  setAnimationSpeed: (animationSpeed) => set({ animationSpeed }),

  updateObjectTransform: (id, position, rotation, scale) => {
    const { currentScene, past } = get();
    if (!currentScene) return;
    
    const newObjects = currentScene.objects.map((obj) => {
      if (obj.id === id) {
        return {
          ...obj,
          transform: {
            position: position || obj.transform.position,
            rotation: rotation || obj.transform.rotation,
            scale: scale || obj.transform.scale,
          },
        };
      }
      return obj;
    });

    const updatedScene = { ...currentScene, objects: newObjects, version: currentScene.version + 1 };
    set({
      currentScene: updatedScene,
      past: [...past.slice(-20), currentScene],
      future: [],
    });
  },

  updateObjectMaterial: (id, color) => {
    const { currentScene, past } = get();
    if (!currentScene) return;

    const newObjects = currentScene.objects.map((obj) => {
      if (obj.id === id) {
        return {
          ...obj,
          material: { ...obj.material, color },
          components: obj.components?.map(c => ({ ...c, material: { ...c.material, color } }))
        };
      }
      return obj;
    });

    const updatedScene = { ...currentScene, objects: newObjects, version: currentScene.version + 1 };
    set({
      currentScene: updatedScene,
      past: [...past.slice(-20), currentScene],
      future: [],
    });
  },

  deleteSelectedObject: () => {
    const { currentScene, selectedObjectId, past } = get();
    if (!currentScene || !selectedObjectId) return;

    const newObjects = currentScene.objects.filter((obj) => obj.id !== selectedObjectId);
    const updatedScene = { ...currentScene, objects: newObjects, version: currentScene.version + 1 };
    set({
      currentScene: updatedScene,
      selectedObjectId: newObjects.length > 0 ? newObjects[0].id : null,
      past: [...past.slice(-20), currentScene],
      future: [],
    });
  },

  undo: () => {
    const { past, currentScene, future } = get();
    if (past.length === 0 || !currentScene) return;

    const previous = past[past.length - 1];
    const newPast = past.slice(0, past.length - 1);
    set({
      currentScene: previous,
      past: newPast,
      future: [currentScene, ...future],
      selectedObjectId: previous.objects.length > 0 ? previous.objects[0].id : null,
    });
  },

  redo: () => {
    const { future, currentScene, past } = get();
    if (future.length === 0 || !currentScene) return;

    const next = future[0];
    const newFuture = future.slice(1);
    set({
      currentScene: next,
      past: [...past, currentScene],
      future: newFuture,
      selectedObjectId: next.objects.length > 0 ? next.objects[0].id : null,
    });
  },
}));
