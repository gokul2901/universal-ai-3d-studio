import React, { useRef, Suspense, Component } from 'react';
import { useFrame } from '@react-three/fiber';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { SceneObjectData, ComponentData, MaterialData } from '../../types';
import { useSceneStore } from '../../store/useSceneStore';

interface SceneObjectProps {
  objectData: SceneObjectData;
}

// Error boundary to catch GLB load failures (KTX2, Draco, network errors)
// so the 3D canvas doesn't go black
class GLTFErrorBoundary extends Component<
  { children: React.ReactNode; fallback: React.ReactNode },
  { hasError: boolean }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  componentDidCatch(error: any) {
    console.warn('[GLTFErrorBoundary] GLB load failed, using procedural fallback:', error?.message);
  }
  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}

function RealisticGLTFModel({
  url,
  color,
  roughness,
  metalness,
  wireframe
}: {
  url: string;
  color?: string;
  roughness?: number;
  metalness?: number;
  wireframe?: boolean;
}) {
  // Load without Draco path — avoids KTX2Loader requirement for standard GLBs
  const gltf = useGLTF(url);
  const scene = React.useMemo(() => {
    const cloned = gltf.scene.clone(true);
    cloned.traverse((node: any) => {
      if (node.isMesh) {
        node.castShadow = true;
        node.receiveShadow = true;
        if (wireframe && node.material) {
          node.material.wireframe = true;
        }
        if (color && node.material) {
          const matName = (node.material.name || node.name || '').toLowerCase();
          if (
            matName.includes('body') ||
            matName.includes('paint') ||
            matName.includes('car_body') ||
            matName.includes('exterior')
          ) {
            node.material = node.material.clone();
            node.material.color = new THREE.Color(color);
            if (roughness !== undefined) node.material.roughness = roughness;
            if (metalness !== undefined) node.material.metalness = metalness;
          }
        }
      }
    });
    return cloned;
  }, [gltf.scene, color, roughness, metalness, wireframe]);

  return <primitive object={scene} />;
}

// Procedural fallback mesh shown when GLB can't be loaded
function FallbackMesh({ color = '#64748b' }: { color?: string }) {
  return (
    <mesh castShadow receiveShadow>
      <boxGeometry args={[1.5, 1.5, 1.5]} />
      <meshStandardMaterial color={color} roughness={0.4} metalness={0.3} />
    </mesh>
  );
}


function RenderGeometry({ type, params }: { type: string; params?: Record<string, any> }) {
  const p = params || {};
  switch (type.toLowerCase()) {
    case 'sphere': {
      const radius = p.radius ?? (p.width ? p.width / 2 : 1);
      return <sphereGeometry args={[radius, p.widthSegments || 32, p.heightSegments || 32]} />;
    }
    case 'cylinder': {
      const radius = p.radius ?? (p.width ? p.width / 2 : 0.5);
      const rTop = p.radiusTop ?? radius;
      const rBottom = p.radiusBottom ?? radius;
      const height = p.height ?? (p.depth ? p.depth : 1.5);
      return <cylinderGeometry args={[rTop, rBottom, height, p.radialSegments || 32]} />;
    }
    case 'cone': {
      const radius = p.radius ?? (p.width ? p.width / 2 : 1);
      const height = p.height ?? 2;
      return <coneGeometry args={[radius, height, p.radialSegments || 32]} />;
    }
    case 'torus': {
      const radius = p.radius ?? (p.width ? p.width / 2 : 0.55);
      const tube = p.tube ?? (p.thickness ?? (p.height ? p.height / 3 : 0.12));
      return <torusGeometry args={[radius, tube, p.radialSegments || 24, p.tubularSegments || 48]} />;
    }
    case 'plane':
      return <planeGeometry args={[p.width || 4, p.height || p.depth || 4]} />;
    case 'box':
    default:
      return <boxGeometry args={[p.width || 1.5, p.height || 1.5, p.depth || 1.5]} />;
  }
}

function RenderMaterial({
  mat,
  wireframe
}: {
  mat: MaterialData;
  wireframe: boolean;
}) {
  // Preserve pristine PBR colors (rubber, chrome, gloss paint). Selection is shown by ground ring halo.
  const emissiveColor = mat.emissive || '#000000';
  const emissiveIntensity = mat.emissive_intensity || 0;

  return (
    <meshStandardMaterial
      color={mat.color || '#94a3b8'}
      roughness={mat.roughness ?? 0.3}
      metalness={mat.metalness ?? 0.2}
      wireframe={wireframe || mat.wireframe}
      emissive={emissiveColor}
      emissiveIntensity={emissiveIntensity}
      transparent={(mat.opacity !== undefined && mat.opacity < 1) || (mat.transmission !== undefined && mat.transmission > 0)}
      opacity={mat.opacity ?? 1.0}
    />
  );
}

export const SceneObject: React.FC<SceneObjectProps> = ({ objectData }) => {
  const groupRef = useRef<THREE.Group>(null);
  const { selectedObjectId, selectObject, explodedProgress, wireframe, isPlayingAnimation, animationSpeed } = useSceneStore();
  const isSelected = selectedObjectId === objectData.id;

  // Real-time procedural animations
  useFrame((state, delta) => {
    if (!groupRef.current || !isPlayingAnimation) return;

    const anim = objectData.animation;
    if (anim && anim.type !== 'none') {
      const speed = (anim.speed || 1.0) * animationSpeed;
      const t = state.clock.getElapsedTime() * speed;

      if (anim.type === 'rotate') {
        const axis = anim.axis || 'y';
        if (axis === 'x') groupRef.current.rotation.x += delta * speed;
        else if (axis === 'z') groupRef.current.rotation.z += delta * speed;
        else groupRef.current.rotation.y += delta * speed;
      } else if (anim.type === 'bounce') {
        const amp = anim.amplitude || 0.2;
        groupRef.current.position.y = objectData.transform.position[1] + Math.sin(t * 3) * amp;
      } else if (anim.type === 'pulse') {
        const scaleBase = objectData.transform.scale[0];
        const s = scaleBase * (1 + Math.sin(t * 4) * 0.08);
        groupRef.current.scale.set(s, s, s);
      } else if (anim.type === 'orbit') {
        const radius = anim.amplitude || Math.hypot(objectData.transform.position[0], objectData.transform.position[2]) || 5;
        groupRef.current.position.x = Math.cos(t) * radius;
        groupRef.current.position.z = Math.sin(t) * radius;
      }
    }
  });

  const handleClick = (e: any) => {
    e.stopPropagation();
    selectObject(objectData.id);
  };

  const pos = objectData.transform.position || [0, 0, 0];
  const rot = objectData.transform.rotation || [0, 0, 0];
  const scl = objectData.transform.scale || [1, 1, 1];

  const hasComponents = objectData.components && objectData.components.length > 0;

  return (
    <group
      ref={groupRef}
      name={objectData.id}
      position={[pos[0], pos[1], pos[2]]}
      rotation={[rot[0], rot[1], rot[2]]}
      scale={[scl[0], scl[1], scl[2]]}
      onClick={handleClick}
    >
      {/* If object has an ultra-realistic 3D GLB model */}
      {objectData.asset_url && explodedProgress <= 0.05 ? (
        <GLTFErrorBoundary fallback={<FallbackMesh color={objectData.material?.color} />}>
          <Suspense fallback={<FallbackMesh color={objectData.material?.color} />}>
            <RealisticGLTFModel
              url={objectData.asset_url}
              color={objectData.material?.color}
              roughness={objectData.material?.roughness}
              metalness={objectData.material?.metalness}
              wireframe={wireframe}
            />
          </Suspense>
        </GLTFErrorBoundary>
      ) : hasComponents ? (
        objectData.components!.map((comp: ComponentData) => {
          const compPos = comp.transform?.position || [0, 0, 0];
          const compRot = comp.transform?.rotation || [0, 0, 0];
          const compScl = comp.transform?.scale || [1, 1, 1];
          const explode = comp.explode_offset || [0, 0, 0];

          // Interpolate exploded offset along outward vector
          const explodedX = compPos[0] + explode[0] * explodedProgress;
          const explodedY = compPos[1] + explode[1] * explodedProgress;
          const explodedZ = compPos[2] + explode[2] * explodedProgress;

          return (
            <mesh
              key={comp.id}
              name={comp.id}
              position={[explodedX, explodedY, explodedZ]}
              rotation={[compRot[0], compRot[1], compRot[2]]}
              scale={[compScl[0], compScl[1], compScl[2]]}
              castShadow
              receiveShadow
            >
              <RenderGeometry type={comp.geometry_type} params={comp.geometry_params} />
              <RenderMaterial mat={comp.material} wireframe={wireframe} />
            </mesh>
          );
        })
      ) : (
        /* Standard single mesh */
        <mesh castShadow receiveShadow>
          <RenderGeometry type={objectData.geometry_type} params={objectData.geometry_params} />
          <RenderMaterial mat={objectData.material} wireframe={wireframe} />
        </mesh>
      )}

      {/* Modern cybernetic selection ring with subtle pulse glow on ground */}
      {isSelected && (
        <group position={[0, -0.04, 0]}>
          <mesh rotation={[-Math.PI / 2, 0, 0]}>
            <ringGeometry args={[2.0, 2.06, 64]} />
            <meshBasicMaterial color="#38bdf8" transparent opacity={0.8} side={THREE.DoubleSide} />
          </mesh>
          <mesh rotation={[-Math.PI / 2, 0, 0]}>
            <circleGeometry args={[2.0, 64]} />
            <meshBasicMaterial color="#38bdf8" transparent opacity={0.06} side={THREE.DoubleSide} />
          </mesh>
        </group>
      )}
    </group>
  );
};
