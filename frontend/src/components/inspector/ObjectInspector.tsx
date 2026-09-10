import React, { useState } from 'react';
import {
  Info, Sparkles, Trash2, Eye, EyeOff, Layers, Play,
  Copy, Edit3, ShieldAlert, Check
} from 'lucide-react';
import { useSceneStore } from '../../store/useSceneStore';
import { useAIStore } from '../../store/useAIStore';
import { explainTarget } from '../../services/api';
import { useUIStore } from '../../store/useUIStore';
import { t } from '../../i18n';

export const ObjectInspector: React.FC = () => {
  const { currentScene, selectedObjectId, deleteSelectedObject, updateObjectMaterial, setExplodedProgress } = useSceneStore();
  const { addMessage, setIsExplaining } = useAIStore();
  const { language } = useUIStore();
  const [copied, setCopied] = useState(false);

  if (!currentScene || !selectedObjectId) {
    return (
      <div className="p-4 text-center text-xs text-slate-500 italic">
        {t('no_selected_obj', language) || 'Select an object in the 3D viewport to inspect its properties and components.'}
      </div>
    );
  }

  const selectedObj = currentScene.objects.find((o) => o.id === selectedObjectId);
  if (!selectedObj) {
    return (
      <div className="p-4 text-center text-xs text-slate-500 italic">
        Object not found in active scene.
      </div>
    );
  }

  const handleExplain = async () => {
    setIsExplaining(true);
    try {
      const res = await explainTarget({
        target_name: selectedObj.name,
        category: selectedObj.category,
        language: language,
        context: {
          purpose: selectedObj.purpose,
          description: selectedObj.description,
          scene_title: currentScene.title,
        },
      });

      if (res.success) {
        addMessage({
          id: `explain_${Date.now()}`,
          sender: 'ai',
          text: `### ${res.title}\n\n${res.explanation}\n\n**Purpose:** ${res.purpose}`,
          language: res.language,
          timestamp: new Date().toLocaleTimeString(),
          target_id: selectedObj.id,
          purpose: res.purpose,
          characteristics: res.characteristics,
        });
      }
    } catch (e) {
      console.error('Explain error:', e);
    } finally {
      setIsExplaining(false);
    }
  };

  const handleColorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    updateObjectMaterial(selectedObj.id, e.target.value);
  };

  const hasComponents = selectedObj.components && selectedObj.components.length > 0;

  return (
    <div className="flex flex-col gap-4 p-4 text-xs text-slate-300 select-text">
      {/* Header with AI Estimated Badge */}
      <div className="flex items-start justify-between gap-2 border-b border-white/10 pb-3">
        <div>
          <h3 className="font-display font-semibold text-sm text-white">
            {selectedObj.name}
          </h3>
          <span className="text-[10px] text-primary-400 font-mono uppercase">
            {selectedObj.category}
          </span>
        </div>
        {selectedObj.is_estimated && (
          <span className="flex items-center gap-1 text-[10px] font-semibold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/20">
            <ShieldAlert className="w-3 h-3" />
            {t('ai_estimated', language)}
          </span>
        )}
      </div>

      {/* Description & Purpose */}
      <div className="flex flex-col gap-1.5 bg-dark-900/60 p-3 rounded-xl border border-white/5">
        <div className="text-[11px] font-semibold text-slate-400 flex items-center gap-1">
          <Info className="w-3 h-3 text-primary-400" />
          <span>{t('purpose_and_analysis', language)}</span>
        </div>
        <p className="text-[11px] text-slate-300 leading-relaxed">
          {selectedObj.purpose || selectedObj.description || 'Custom interactive 3D model component.'}
        </p>
      </div>

      {/* Transform Coordinates */}
      <div className="grid grid-cols-3 gap-2 bg-dark-900/60 p-2.5 rounded-xl border border-white/5 text-[11px] font-mono">
        <div>
          <span className="text-slate-500 text-[10px] block">{t('position', language) || 'Position'}</span>
          <span className="text-slate-200">
            {selectedObj.transform.position.map(n => n.toFixed(1)).join(', ')}
          </span>
        </div>
        <div>
          <span className="text-slate-500 text-[10px] block">{t('scale', language) || 'Scale'}</span>
          <span className="text-slate-200">
            {selectedObj.transform.scale.map(n => n.toFixed(1)).join(', ')}
          </span>
        </div>
        <div>
          <span className="text-slate-500 text-[10px] block">{t('geometry', language) || 'Geometry'}</span>
          <span className="text-indigo-300 capitalize">{selectedObj.geometry_type}</span>
        </div>
      </div>

      {/* Material Color Picker */}
      <div className="flex items-center justify-between bg-dark-900/60 p-2.5 rounded-xl border border-white/5">
        <span className="text-[11px] font-medium text-slate-300">{t('material_color', language)}</span>
        <div className="flex items-center gap-2">
          <input
            type="color"
            value={selectedObj.material.color || '#3b82f6'}
            onChange={handleColorChange}
            className="w-7 h-7 rounded-lg cursor-pointer bg-transparent border-0"
          />
          <span className="font-mono text-[11px] text-slate-400">
            {selectedObj.material.color || '#3b82f6'}
          </span>
        </div>
      </div>

      {/* Modular Components Breakdown (for exploded view) */}
      {hasComponents && (
        <div className="flex flex-col gap-1.5">
          <div className="text-[11px] font-semibold text-slate-300 flex items-center justify-between">
            <span className="flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-indigo-400" />
              {t('components', language)} ({selectedObj.components!.length})
            </span>
            <button
              onClick={() => setExplodedProgress(1)}
              className="text-[10px] text-indigo-400 hover:text-indigo-300 underline"
            >
              {t('explode_view', language) || 'Explode View'}
            </button>
          </div>
          <div className="flex flex-col gap-1">
            {selectedObj.components!.map((comp) => (
              <div
                key={comp.id}
                className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-dark-900/40 border border-white/5 text-[11px]"
              >
                <span className="text-slate-300">{comp.name}</span>
                <span className="text-[10px] font-mono text-slate-500 capitalize">{comp.geometry_type}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-2 pt-2 border-t border-white/10">
        <button
          type="button"
          onClick={handleExplain}
          className="flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-gradient-to-r from-primary-500/20 to-indigo-500/20 hover:from-primary-500/30 hover:to-indigo-500/30 border border-primary-500/40 text-primary-300 font-semibold transition-all shadow-sm"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>{t('explain_object', language)}</span>
        </button>

        <button
          type="button"
          onClick={deleteSelectedObject}
          className="flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 font-semibold transition-all"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>{t('delete', language)}</span>
        </button>
      </div>
    </div>
  );
};
