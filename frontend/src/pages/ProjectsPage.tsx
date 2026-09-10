import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, Box, Calendar, Trash2, Copy, ExternalLink, Sparkles, FolderKanban } from 'lucide-react';
import { Project } from '../types';
import { fetchProjects, deleteProject, saveProject } from '../services/api';
import { useSceneStore } from '../store/useSceneStore';
import { useUIStore } from '../store/useUIStore';
import { t } from '../i18n';

export const ProjectsPage: React.FC = () => {
  const navigate = useNavigate();
  const { setScene } = useSceneStore();
  const { language } = useUIStore();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  const loadProjects = async () => {
    setLoading(true);
    try {
      const data = await fetchProjects();
      setProjects(data);
    } catch (e) {
      console.error('Projects fetch error:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleOpenProject = (proj: Project) => {
    setScene(proj.scene);
    navigate(`/studio/${proj.id}`);
  };

  const handleDuplicate = async (proj: Project, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await saveProject({
        title: `${proj.title} (Copy)`,
        prompt: proj.prompt,
        language: proj.language,
        scene: { ...proj.scene, title: `${proj.title} (Copy)` }
      });
      loadProjects();
    } catch (err) {
      console.error('Duplicate error:', err);
    }
  };

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!window.confirm('Delete this 3D project?')) return;
    try {
      await deleteProject(id);
      setProjects(prev => prev.filter(p => p.id !== id));
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  return (
    <div className="min-h-screen bg-dark-950 text-white p-6 sm:p-10 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <FolderKanban className="w-5 h-5 text-primary-400" />
            <h1 className="font-display font-bold text-2xl sm:text-3xl text-white">
              {t('projects_title', language)}
            </h1>
          </div>
          <p className="text-xs text-slate-400">
            {t('projects_subtitle', language)}
          </p>
        </div>

        <button
          onClick={() => navigate('/create')}
          className="flex items-center gap-2 px-5 py-2.5 rounded-2xl font-semibold text-xs bg-gradient-to-r from-primary-500 to-indigo-600 hover:from-primary-600 hover:to-indigo-700 text-white shadow-lg shadow-primary-500/25 transition-all"
        >
          <Plus className="w-4 h-4" />
          <span>{t('new_project_btn', language)}</span>
        </button>
      </div>

      {/* Projects Grid */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3].map((n) => (
            <div key={n} className="glass-panel p-5 rounded-3xl h-48 animate-pulse border border-white/5" />
          ))}
        </div>
      ) : projects.length === 0 ? (
        <div className="glass-panel p-12 rounded-3xl border border-white/10 text-center max-w-md mx-auto">
          <Box className="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <h3 className="font-display font-semibold text-lg text-white mb-1">
            {t('no_projects', language)}
          </h3>
          <p className="text-xs text-slate-400 mb-5">
            {t('no_projects_desc', language)}
          </p>
          <button
            onClick={() => navigate('/create')}
            className="px-5 py-2 rounded-xl text-xs font-semibold bg-primary-500 hover:bg-primary-600 text-white transition-colors"
          >
            {t('create_scene_btn', language)}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((proj) => {
            const photorealImg = proj.realistic_image_url || proj.scene?.realistic_image_url;
            return (
              <div
                key={proj.id}
                onClick={() => handleOpenProject(proj)}
                className="glass-card p-5 rounded-3xl cursor-pointer group flex flex-col justify-between border border-white/10 hover:border-primary-500/40 relative overflow-hidden"
              >
                <div>
                  {photorealImg ? (
                    <div className="relative w-full h-32 rounded-2xl overflow-hidden mb-3.5 border border-white/10 group-hover:border-primary-500/30 transition-colors">
                      <img
                        src={photorealImg}
                        alt={proj.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute top-2 right-2 px-2 py-0.5 rounded-full text-[9px] font-bold bg-dark-950/80 backdrop-blur text-accent-cyan border border-accent-cyan/30 uppercase tracking-wider">
                        Photoreal 8K
                      </div>
                      <div className="absolute top-2 left-2 flex items-center gap-1">
                        <button
                          type="button"
                          onClick={(e) => handleDuplicate(proj, e)}
                          title="Duplicate Project"
                          className="p-1 rounded-lg bg-dark-950/70 text-slate-300 hover:text-white hover:bg-dark-950 transition-colors"
                        >
                          <Copy className="w-3 h-3" />
                        </button>
                        <button
                          type="button"
                          onClick={(e) => handleDelete(proj.id, e)}
                          title="Delete Project"
                          className="p-1 rounded-lg bg-dark-950/70 text-slate-300 hover:text-red-400 hover:bg-dark-950 transition-colors"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-between mb-3">
                      <div className="w-9 h-9 rounded-xl bg-primary-500/10 text-primary-400 flex items-center justify-center border border-primary-500/20 group-hover:scale-105 transition-transform">
                        <Box className="w-4 h-4" />
                      </div>
                      <div className="flex items-center gap-1">
                        <button
                          type="button"
                          onClick={(e) => handleDuplicate(proj, e)}
                          title="Duplicate Project"
                          className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
                        >
                          <Copy className="w-3.5 h-3.5" />
                        </button>
                        <button
                          type="button"
                          onClick={(e) => handleDelete(proj.id, e)}
                          title="Delete Project"
                          className="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  )}

                  <h3 className="font-display font-semibold text-base text-white group-hover:text-primary-300 transition-colors mb-1 truncate">
                    {proj.title}
                  </h3>
                  <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
                    {proj.prompt || 'Synthesized 3D Scene'}
                  </p>
                </div>

              <div className="pt-3 border-t border-white/5 flex items-center justify-between text-[11px] text-slate-500">
                <span className="flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  {new Date(proj.created_at).toLocaleDateString()}
                </span>
                <span className="text-primary-400 font-medium group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                  Open <ExternalLink className="w-3 h-3" />
                </span>
              </div>
            </div>
          );
        })}
        </div>
      )}
    </div>
  );
};
