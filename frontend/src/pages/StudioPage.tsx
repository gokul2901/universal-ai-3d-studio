import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Layers, Info, MessageSquare, ChevronLeft, ChevronRight, Menu, X } from 'lucide-react';
import { ThreeDViewport } from '../components/3d/ThreeDViewport';
import { SceneTree } from '../components/scene/SceneTree';
import { ObjectInspector } from '../components/inspector/ObjectInspector';
import { AICopilot } from '../components/ai/AICopilot';
import { AnimationTimeline } from '../components/scene/AnimationTimeline';
import { useSceneStore } from '../store/useSceneStore';
import { useUIStore } from '../store/useUIStore';
import { getProjectById, fetchDemoScenes } from '../services/api';
import { t } from '../i18n';

export const StudioPage: React.FC = () => {
  const { projectId } = useParams<{ projectId?: string }>();
  const { currentScene, setScene } = useSceneStore();
  const { activeTab, setActiveTab, language } = useUIStore();

  const [leftTab, setLeftTab] = useState<'tree' | 'inspector'>('tree');
  const [isLeftPanelOpen, setIsLeftPanelOpen] = useState(true);
  const [isRightPanelOpen, setIsRightPanelOpen] = useState(true);
  const [isMobileDrawerOpen, setIsMobileDrawerOpen] = useState(false);

  // Initialize scene if not present or if navigating to specific project
  useEffect(() => {
    async function loadScene() {
      if (projectId) {
        try {
          const proj = await getProjectById(projectId);
          if (proj && proj.scene) {
            setScene(proj.scene);
            return;
          }
        } catch (e) {
          console.warn('Could not load specific project, falling back to demo.');
        }
      }

      if (!currentScene) {
        try {
          const demos = await fetchDemoScenes();
          if (demos.demos && demos.demos.length > 0) {
            setScene(demos.demos[0].scene);
          }
        } catch (e) {
          console.error('Failed to load demo scene', e);
        }
      }
    }
    loadScene();
  }, [projectId]);

  return (
    <div className="relative w-full h-[calc(100vh-3.5rem)] flex flex-col bg-dark-950 overflow-hidden select-none">
      {/* Workspace Area: Left Panel + Center Viewport + Right AI Copilot */}
      <div className="flex-1 flex relative overflow-hidden">
        {/* Left Side Panel (Scene Hierarchy & Object Inspector) */}
        {isLeftPanelOpen && (
          <aside className="w-72 sm:w-80 h-full glass-panel border-r border-white/10 flex flex-col z-20 shrink-0 backdrop-blur-xl transition-all">
            {/* Tab Headers */}
            <div className="flex items-center border-b border-white/10 bg-dark-950/60">
              <button
                type="button"
                onClick={() => setLeftTab('tree')}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 text-xs font-semibold transition-colors ${
                  leftTab === 'tree'
                    ? 'text-primary-400 border-b-2 border-primary-500 bg-primary-500/5'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                <span>{t('scene_tree_tab', language)}</span>
              </button>

              <button
                type="button"
                onClick={() => setLeftTab('inspector')}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 text-xs font-semibold transition-colors ${
                  leftTab === 'inspector'
                    ? 'text-primary-400 border-b-2 border-primary-500 bg-primary-500/5'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Info className="w-3.5 h-3.5" />
                <span>{t('inspector_tab', language)}</span>
              </button>
            </div>

            {/* Tab Content */}
            <div className="flex-1 overflow-y-auto">
              {leftTab === 'tree' ? <SceneTree /> : <ObjectInspector />}
            </div>
          </aside>
        )}

        {/* Center Viewport */}
        <main className="flex-1 relative h-full overflow-hidden bg-black">
          <ThreeDViewport />

          {/* Floating Collapsible Buttons */}
          <button
            type="button"
            onClick={() => setIsLeftPanelOpen(!isLeftPanelOpen)}
            title={isLeftPanelOpen ? "Collapse Left Panel" : "Expand Left Panel"}
            className={`absolute top-4 ${isLeftPanelOpen ? 'left-[19rem]' : 'left-4'} z-20 hidden md:flex items-center justify-center p-1.5 rounded-xl glass-panel border border-white/10 text-slate-400 hover:text-white transition-all`}
          >
            {isLeftPanelOpen ? <ChevronLeft className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
          </button>

          <button
            type="button"
            onClick={() => setIsRightPanelOpen(!isRightPanelOpen)}
            title={isRightPanelOpen ? "Collapse AI Copilot" : "Expand AI Copilot"}
            className={`absolute top-4 ${isRightPanelOpen ? 'right-[21rem]' : 'right-4'} z-20 hidden md:flex items-center justify-center p-1.5 rounded-xl glass-panel border border-white/10 text-slate-400 hover:text-white transition-all`}
          >
            {isRightPanelOpen ? <ChevronRight className="w-3.5 h-3.5" /> : <ChevronLeft className="w-3.5 h-3.5" />}
          </button>

          {/* Mobile Bottom Bar Trigger */}
          <div className="md:hidden absolute bottom-3 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2 glass-panel p-1 rounded-2xl border border-white/15">
            <button
              onClick={() => { setLeftTab('tree'); setIsMobileDrawerOpen(true); }}
              className="px-3 py-1.5 rounded-xl text-xs font-medium text-slate-300 hover:text-white bg-white/5"
            >
              {t('scene_tree_tab', language)}
            </button>
            <button
              onClick={() => { setLeftTab('inspector'); setIsMobileDrawerOpen(true); }}
              className="px-3 py-1.5 rounded-xl text-xs font-medium text-slate-300 hover:text-white bg-white/5"
            >
              {t('inspector_tab', language)}
            </button>
            <button
              onClick={() => { setActiveTab('copilot'); setIsMobileDrawerOpen(true); }}
              className="px-3 py-1.5 rounded-xl text-xs font-semibold text-primary-300 bg-primary-500/20"
            >
              {t('copilot_title', language)}
            </button>
          </div>
        </main>

        {/* Right Side Panel (AI Copilot) */}
        {isRightPanelOpen && (
          <aside className="w-80 sm:w-88 h-full glass-panel border-l border-white/10 flex flex-col z-20 shrink-0 backdrop-blur-xl transition-all">
            <AICopilot />
          </aside>
        )}
      </div>

      {/* Bottom Animation & Playback Timeline */}
      <AnimationTimeline />

      {/* Mobile Drawer */}
      {isMobileDrawerOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-black/70 backdrop-blur-md flex flex-col justify-end">
          <div className="glass-panel h-3/4 rounded-t-3xl border-t border-white/20 p-4 flex flex-col animate-slide-up">
            <div className="flex items-center justify-between pb-3 border-b border-white/10">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setLeftTab('tree')}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold ${leftTab === 'tree' ? 'bg-primary-500 text-white' : 'text-slate-400'}`}
                >
                  {t('scene_tree_tab', language)}
                </button>
                <button
                  onClick={() => setLeftTab('inspector')}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold ${leftTab === 'inspector' ? 'bg-primary-500 text-white' : 'text-slate-400'}`}
                >
                  {t('inspector_tab', language)}
                </button>
                <button
                  onClick={() => setActiveTab('copilot')}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold ${activeTab === 'copilot' ? 'bg-indigo-600 text-white' : 'text-slate-400'}`}
                >
                  {t('copilot_title', language)}
                </button>
              </div>
              <button
                onClick={() => setIsMobileDrawerOpen(false)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto pt-2">
              {activeTab === 'copilot' ? <AICopilot /> : leftTab === 'tree' ? <SceneTree /> : <ObjectInspector />}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
