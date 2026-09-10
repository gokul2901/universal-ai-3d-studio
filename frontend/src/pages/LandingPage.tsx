import React, { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, MeshDistortMaterial, Sphere, Torus, Box } from '@react-three/drei';
import {
  Sparkles, ArrowRight, Layers, Mic, Image, Wand2,
  Box as BoxIcon, Eye, Globe, Zap, Play, Cpu
} from 'lucide-react';
import * as THREE from 'three';
import { useSceneStore } from '../store/useSceneStore';
import { useUIStore } from '../store/useUIStore';
import { fetchDemoScenes } from '../services/api';
import { t } from '../i18n';

function FloatingHeroScene() {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y = state.clock.getElapsedTime() * 0.12;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Central High-Performance Sphere */}
      <Sphere args={[1.5, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial
          color="#6366f1"
          emissive="#3730a3"
          emissiveIntensity={0.3}
          roughness={0.25}
          metalness={0.7}
        />
      </Sphere>

      {/* Outer Torus */}
      <Torus args={[2.5, 0.12, 16, 48]} rotation={[1, 0.5, 0]}>
        <meshStandardMaterial
          color="#06b6d4"
          emissive="#0284c7"
          emissiveIntensity={0.5}
          roughness={0.2}
          metalness={0.8}
        />
      </Torus>

      {/* Floating Satellites */}
      <Box args={[0.6, 0.6, 0.6]} position={[-3, 1.5, -1]}>
        <meshStandardMaterial color="#ec4899" roughness={0.3} metalness={0.6} />
      </Box>

      <Sphere args={[0.5, 20, 20]} position={[3, -1.2, 1]}>
        <meshStandardMaterial color="#f59e0b" emissive="#d97706" emissiveIntensity={0.4} roughness={0.3} />
      </Sphere>

      <ambientLight intensity={0.8} />
      <directionalLight position={[5, 8, 5]} intensity={1.8} color="#ffffff" />
      <pointLight position={[-4, -4, -2]} intensity={2.0} color="#a855f7" />
    </group>
  );
}

export const LandingPage: React.FC = () => {
  const navigate = useNavigate();
  const { setScene } = useSceneStore();
  const { language } = useUIStore();

  const handleLaunchDemo = async (demoKey?: string) => {
    try {
      const data = await fetchDemoScenes();
      const target = demoKey
        ? data.demos.find((d: any) => d.key === demoKey || d.id === demoKey)
        : data.demos[0];
      if (target) {
        setScene(target.scene);
        navigate(`/studio/${target.id}`);
      }
    } catch (e) {
      navigate('/studio');
    }
  };

  const featureCards = [
    { icon: <Wand2 className="w-5 h-5 text-indigo-400" />, title: "Text → 3D", desc: "Type natural descriptions to instantly architect complete 3D environments and compound objects." },
    { icon: <Image className="w-5 h-5 text-cyan-400" />, title: "Image → 3D", desc: "Upload photos or sketches. Multimodal Vision AI detects boundaries, spatial depth, and textures." },
    { icon: <Mic className="w-5 h-5 text-fuchsia-400" />, title: "Voice → 3D", desc: "Speak naturally in Tamil, Hindi, English, Arabic, and 12 other languages with live audio waveforms." },
    { icon: <Sparkles className="w-5 h-5 text-amber-400" />, title: "AI Scene Generation", desc: "Automatic generic scene planning generating lighting, PBR materials, cameras, and terrain." },
    { icon: <Cpu className="w-5 h-5 text-emerald-400" />, title: "AI 3D Copilot", desc: "Context-aware conversational assistant that understands active objects and explains engineering logic." },
    { icon: <Globe className="w-5 h-5 text-blue-400" />, title: "Multilingual Voice", desc: "Native Tamil, Hindi, Bengali, Telugu, Urdu, and international speech recognition and synthesis." },
    { icon: <Eye className="w-5 h-5 text-teal-400" />, title: "Object Inspector", desc: "Deep property analysis with explicit AI Estimated labels, material editors, and dimensions." },
    { icon: <Zap className="w-5 h-5 text-purple-400" />, title: "3D Animation", desc: "Rotational, bouncing, orbital, and reciprocating mechanics with a dedicated scrubbable timeline." },
    { icon: <Layers className="w-5 h-5 text-rose-400" />, title: "Exploded View", desc: "Smooth animated separation of compound mechanical assemblies with real-time expansion sliders." },
    { icon: <BoxIcon className="w-5 h-5 text-indigo-300" />, title: "Natural Language Editing", desc: "Say 'Make the pillar gold' or 'Add three spotlights' and watch your scene mutate instantly." }
  ];

  const demoItems = [
    { key: "wedding_stage", name: "Wedding Stage", desc: "Grand luxury mandap with floral arch, velvet sofa & chandeliers", tag: "Event Decor" },
    { key: "mars_station", name: "Mars Station", desc: "Ares-VII bio-domes, solar arrays, terrain & exploration rover", tag: "Sci-Fi Space" },
    { key: "solar_system", name: "Solar System", desc: "Sun with animated planets, orbital trails & cosmic lighting", tag: "Astronomy" },
    { key: "machine", name: "V-Twin Engine", desc: "Reciprocating piston block, cylinder heads & full exploded view", tag: "Engineering" },
    { key: "modern_office", name: "AI Startup Office", desc: "Curved executive desks, ultrawide monitors & neural server rack", tag: "Interior" },
    { key: "restaurant", name: "Luxury Bistro", desc: "Calacatta marble tables, ambient lighting & wine bar counter", tag: "Hospitality" },
    { key: "futuristic_city", name: "Cyberpunk City", desc: "Neon megastructures, towering spires & volumetric night fog", tag: "Architecture" },
    { key: "modern_house", name: "Modern Villa", desc: "Minimalist concrete cantilever pavilion & infinity landscape", tag: "Residential" },
    { key: "factory", name: "Robotic Factory", desc: "Articulated 6-axis robotic arms & automated assembly line", tag: "Industrial" },
    { key: "product_showroom", name: "Product Showroom", desc: "Holographic smartwatch on levitating magnetic pedestal", tag: "Showcase" }
  ];

  return (
    <div className="relative min-h-screen bg-dark-950 text-white overflow-hidden pb-24">
      {/* 3D Interactive Hero Canvas Background */}
      <div className="absolute top-0 left-0 right-0 h-[640px] pointer-events-none z-0 opacity-75">
        <Canvas
          dpr={[1, 1.25]}
          performance={{ min: 0.5 }}
          gl={{ powerPreference: 'high-performance', antialias: true, alpha: true, stencil: false }}
          camera={{ position: [0, 0, 7], fov: 45 }}
        >
          <FloatingHeroScene />
        </Canvas>
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-dark-950/70 to-dark-950" />
      </div>

      {/* Hero Content */}
      <div className="relative z-10 max-w-5xl mx-auto pt-24 px-6 text-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full glass-panel border border-primary-500/30 text-xs font-semibold text-primary-300 mb-6 shadow-xl shadow-primary-500/10 animate-fade-in">
          <Sparkles className="w-3.5 h-3.5 text-accent-cyan" />
          <span>Universal Multimodal AI 3D Platform</span>
        </div>

        <h1 className="font-display font-extrabold text-4xl sm:text-6xl md:text-7xl tracking-tight leading-[1.08] mb-6 text-transparent bg-clip-text bg-gradient-to-b from-white via-slate-100 to-slate-400">
          {t('hero_title_1', language)}<br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary-400 via-indigo-300 to-accent-cyan">
            {t('hero_title_2', language)}
          </span>
        </h1>

        <p className="max-w-2xl mx-auto text-sm sm:text-base text-slate-300 leading-relaxed mb-10 font-normal">
          {t('hero_subtitle', language)}
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-wrap items-center justify-center gap-4">
          <button
            onClick={() => navigate('/create')}
            className="flex items-center gap-2 px-8 py-3.5 rounded-2xl font-semibold text-sm bg-gradient-to-r from-primary-500 via-indigo-500 to-primary-600 hover:from-primary-600 hover:to-indigo-700 text-white shadow-xl shadow-primary-500/30 hover:scale-105 transition-all duration-300 group"
          >
            <span>{t('btn_create_3d', language)}</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </button>

          <button
            onClick={() => handleLaunchDemo()}
            className="flex items-center gap-2 px-7 py-3.5 rounded-2xl font-semibold text-sm glass-panel hover:bg-white/10 text-slate-200 border border-white/15 hover:border-white/30 transition-all duration-300"
          >
            <Play className="w-4 h-4 text-accent-cyan fill-current" />
            <span>{t('btn_try_demo', language)}</span>
          </button>
        </div>
      </div>

      {/* 10 Built-In Demo Showcase Section */}
      <div className="relative z-10 max-w-6xl mx-auto mt-28 px-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="font-display font-bold text-2xl text-white">
              {t('section_demos', language)}
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              {t('section_demos_sub', language)}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3.5">
          {demoItems.map((demo) => (
            <div
              key={demo.key}
              onClick={() => handleLaunchDemo(demo.key)}
              className="glass-card p-4 rounded-2xl cursor-pointer group flex flex-col justify-between border border-white/10 hover:border-primary-500/50"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-primary-500/10 text-primary-400 border border-primary-500/20">
                    {demo.tag}
                  </span>
                  <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-primary-400 group-hover:translate-x-1 transition-all" />
                </div>
                <h4 className="font-display font-semibold text-sm text-white group-hover:text-primary-300 transition-colors mb-1">
                  {demo.name}
                </h4>
                <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                  {demo.desc}
                </p>
              </div>
              <div className="mt-4 pt-2 border-t border-white/5 flex items-center gap-1.5 text-[10px] text-accent-cyan font-medium">
                <Play className="w-3 h-3 fill-current" />
                <span>{t('launch_in_3d', language)}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Feature Grid Section */}
      <div className="relative z-10 max-w-6xl mx-auto mt-28 px-6">
        <div className="text-center mb-12">
          <h2 className="font-display font-bold text-3xl text-white mb-2">
            {t('section_features', language)}
          </h2>
          <p className="text-xs text-slate-400 max-w-lg mx-auto">
            {t('section_features_sub', language)}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {featureCards.map((feat, i) => (
            <div key={i} className="glass-card p-5 rounded-2xl border border-white/10 flex flex-col gap-2.5">
              <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center">
                {feat.icon}
              </div>
              <h4 className="font-display font-semibold text-sm text-white">
                {feat.title}
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                {feat.desc}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
