import React, { useRef, useEffect } from 'react';
import { TransformControls } from '@react-three/drei';
import { useThree } from '@react-three/fiber';
import * as THREE from 'three';
import { useSceneStore } from '../../store/useSceneStore';

export const TransformController: React.FC = () => {
  const { scene } = useThree();
  const { selectedObjectId, transformMode, updateObjectTransform } = useSceneStore();
  const controlsRef = useRef<any>(null);

  useEffect(() => {
    if (!controlsRef.current || !selectedObjectId || transformMode === 'select') return;

    const targetObject = scene.getObjectByName(selectedObjectId);
    if (targetObject) {
      controlsRef.current.attach(targetObject);
    } else {
      controlsRef.current.detach();
    }
  }, [selectedObjectId, transformMode, scene]);

  if (transformMode === 'select' || !selectedObjectId) {
    return null;
  }

  const mode = transformMode === 'translate' ? 'translate' : transformMode === 'rotate' ? 'rotate' : 'scale';

  return (
    <TransformControls
      ref={controlsRef}
      mode={mode}
      size={0.75}
      onMouseUp={() => {
        if (!controlsRef.current || !selectedObjectId) return;
        const obj = scene.getObjectByName(selectedObjectId);
        if (obj) {
          updateObjectTransform(
            selectedObjectId,
            [obj.position.x, obj.position.y, obj.position.z],
            [obj.rotation.x, obj.rotation.y, obj.rotation.z],
            [obj.scale.x, obj.scale.y, obj.scale.z]
          );
        }
      }}
    />
  );
};
