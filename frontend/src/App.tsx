import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/ui/Navbar';
import { LandingPage } from './pages/LandingPage';
import { CreatePage } from './pages/CreatePage';
import { StudioPage } from './pages/StudioPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { SettingsPage } from './pages/SettingsPage';
import { useUIStore } from './store/useUIStore';
import { isRTL } from './i18n';

export const App: React.FC = () => {
  const { language } = useUIStore();
  const isRtl = isRTL(language);

  return (
    <Router>
      <div className={`min-h-screen bg-dark-950 text-slate-100 flex flex-col font-sans ${isRtl ? 'rtl' : 'ltr'}`} dir={isRtl ? 'rtl' : 'ltr'}>
        <Navbar />
        <div className="flex-1 flex flex-col">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/create" element={<CreatePage />} />
            <Route path="/studio" element={<StudioPage />} />
            <Route path="/studio/:projectId" element={<StudioPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
