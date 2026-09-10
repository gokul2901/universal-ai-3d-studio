import React, { useEffect, useRef } from 'react';
import { useThree, useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useSceneStore } from '../../store/useSceneStore';

export const CameraController: React.FC = () => {
  const { camera } = useThree();
  const { cameraMode, currentScene } = useSceneStore();
  const targetPos = useRef(new THREE.Vector3(0, 4, 10));
  const targetLook = useRef(new THREE.Vector3(0, 1, 0));

  useEffect(() => {
    const sceneCam = currentScene?.camera;
    const defaultPos = sceneCam?.position || [0, 4, 10];
    const defaultTarget = sceneCam?.target || [0, 1, 0];

    targetLook.current.set(defaultTarget[0], defaultTarget[1], defaultTarget[2]);

    switch (cameraMode) {
      case 'isometric':
        targetPos.current.set(10, 10, 10);
        break;
      case 'top':
        targetPos.current.set(0, 15, 0.001);
        break;
      case 'front':
        targetPos.current.set(0, 2, 11);
        break;
      case 'side':
        targetPos.current.set(12, 2, 0);
        break;
      case 'perspective':
      default:
        targetPos.current.set(defaultPos[0], defaultPos[1], defaultPos[2]);
        break;
    }
  }, [cameraMode, currentScene]);

  useFrame(() => {
    // Smooth camera interpolation
    camera.position.lerp(targetPos.current, 0.05);
  });

  return null;
};
