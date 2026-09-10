import React, { useState } from 'react';
import { ChevronDown, ChevronRight, Box, Layers, Sun, Globe, Eye, EyeOff } from 'lucide-react';
import { useSceneStore } from '../../store/useSceneStore';
import { useUIStore } from '../../store/useUIStore';
import { t } from '../../i18n';

export const SceneTree: React.FC = () => {
  const { currentScene, selectedObjectId, selectObject } = useSceneStore();
  const { language } = useUIStore();
  const [expandedNodes, setExpandedNodes] = useState<Record<string, boolean>>({
    root: true,
    env: true,
    lighting: true,
  });

  const toggleNode = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setExpandedNodes(prev => ({ ...prev, [id]: !prev[id] }));
  };

  if (!currentScene) {
    return (
      <div className="p-4 text-xs text-slate-500 italic text-center">
        No active 3D scene graph.
      </div>
    );
  }

  return (
    <div className="p-3 text-xs text-slate-300 font-mono select-none overflow-y-auto">
      {/* Root Scene Node */}
      <div
        onClick={() => selectObject(null)}
        className="flex items-center gap-1.5 py-1.5 px-2 rounded-lg hover:bg-white/5 cursor-pointer text-slate-200 font-semibold"
      >
        <span onClick={(e) => toggleNode('root', e)} className="p-0.5 hover:bg-white/10 rounded">
          {expandedNodes['root'] ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
        </span>
        <Globe className="w-3.5 h-3.5 text-primary-400" />
        <span className="truncate">{currentScene.title}</span>
      </div>

      {expandedNodes['root'] && (
        <div className="pl-4 border-l border-white/5 ml-3 mt-1 space-y-1">
          {/* Environment */}
          <div className="flex items-center gap-2 py-1 px-2 rounded hover:bg-white/5 text-slate-400">
            <Globe className="w-3 h-3 text-cyan-400" />
            <span>{t('env_label', language) || 'Environment'} ({currentScene.environment.sky_color})</span>
          </div>

          {/* Lighting */}
          <div className="flex items-center gap-2 py-1 px-2 rounded hover:bg-white/5 text-slate-400">
            <Sun className="w-3 h-3 text-amber-400" />
            <span>{t('lighting_label', language) || 'Lighting'} ({currentScene.lighting.length})</span>
          </div>

          {/* Scene Objects */}
          {currentScene.objects.map((obj) => {
            const isSelected = selectedObjectId === obj.id;
            const hasChildren = obj.components && obj.components.length > 0;
            const isExpanded = expandedNodes[obj.id] ?? true;

            return (
              <div key={obj.id} className="flex flex-col">
                <div
                  onClick={() => selectObject(obj.id)}
                  className={`flex items-center gap-1.5 py-1 px-2 rounded-lg cursor-pointer transition-colors ${
                    isSelected
                      ? 'bg-primary-500/20 text-white font-semibold border border-primary-500/40'
                      : 'hover:bg-white/5 text-slate-300'
                  }`}
                >
                  {hasChildren ? (
                    <span onClick={(e) => toggleNode(obj.id, e)} className="p-0.5 hover:bg-white/10 rounded">
                      {isExpanded ? <ChevronDown className="w-3 h-3 text-slate-400" /> : <ChevronRight className="w-3 h-3 text-slate-400" />}
                    </span>
                  ) : (
                    <span className="w-4" />
                  )}
                  <Box className={`w-3.5 h-3.5 ${isSelected ? 'text-primary-400' : 'text-slate-400'}`} />
                  <span className="truncate flex-1">{obj.name}</span>
                  <span className="text-[10px] text-slate-500 capitalize">{obj.geometry_type}</span>
                </div>

                {/* Sub-components */}
                {hasChildren && isExpanded && (
                  <div className="pl-5 border-l border-white/5 ml-3 my-0.5 space-y-0.5">
                    {obj.components!.map((comp) => (
                      <div
                        key={comp.id}
                        onClick={() => selectObject(obj.id)}
                        className="flex items-center gap-1.5 py-0.5 px-2 rounded hover:bg-white/5 text-slate-400 hover:text-slate-200 cursor-pointer text-[11px]"
                      >
                        <Layers className="w-3 h-3 text-indigo-400" />
                        <span className="truncate flex-1">{comp.name}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
