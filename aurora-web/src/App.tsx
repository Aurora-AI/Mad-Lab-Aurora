import { useState, useCallback } from 'react';
import { BrowserRouter, Routes, Route, Outlet } from 'react-router-dom';
import { ReactLenis } from 'lenis/react';

import Preloader        from './components/Preloader';
import ScrollDriver     from './components/ScrollDriver';
import Header           from './components/Header';
import Footer           from './components/Footer';
import ElysianChat      from './components/ElysianChat';

import SovereignHero         from './components/sections/SovereignHero';
import RealityValidation     from './components/sections/RealityValidation';
import BlackBoxRevealed      from './components/sections/BlackBoxRevealed';
import ArchitecturalProtocol from './components/sections/ArchitecturalProtocol';
import FounderDensity        from './components/sections/FounderDensity';
import TheGateway            from './components/sections/TheGateway';

import LexPage        from './pages/LexPage';
import CRMPage        from './pages/CRMPage';
import LivingDocPage  from './pages/LivingDocPage';
import ArsenalPage    from './pages/ArsenalPage';
import GovernancePage from './pages/GovernancePage';

function PublicLayout() {
  return (
    <>
      <Header />
      <main>
        <Outlet />
      </main>
      <Footer />
      <ElysianChat />
    </>
  );
}

function LandingPage({ isLoaded }: { isLoaded: boolean }) {
  return (
    <>
      <SovereignHero isLoaded={isLoaded} />
      <RealityValidation />
      <BlackBoxRevealed />
      <ArchitecturalProtocol />
      <FounderDensity />
      <TheGateway />
    </>
  );
}

export default function App() {
  const [isLoaded, setIsLoaded] = useState(false);

  const handleLoadingComplete = useCallback(() => {
    setIsLoaded(true);
  }, []);

  return (
    <BrowserRouter>
      <div
        id="elysian-root"
        style={{ background: 'var(--page-bg)', color: 'var(--page-text)' }}
        className="relative min-h-screen overflow-x-hidden"
      >
        { !isLoaded && <Preloader key="elysian-preloader" onComplete={handleLoadingComplete} /> }
        
        <ReactLenis root options={{ lerp: 0.08 }}>
          <ScrollDriver />

          <div id="elysian-presentation-layer" className={`transition-opacity duration-1000 ${isLoaded ? 'opacity-100' : 'opacity-0'}`}>
            <Routes>
              {/* Public layout with Header, Footer, and Chat */}
              <Route element={<PublicLayout />}>
                <Route path="/"                 element={<LandingPage isLoaded={isLoaded} />} />
                <Route path="/lex"              element={<LexPage />} />
                <Route path="/crm"              element={<CRMPage />} />
                <Route path="/living-document"  element={<LivingDocPage />} />
                <Route path="/arsenal"          element={<ArsenalPage />} />
              </Route>

              {/* Full-bleed isolated dashboard */}
              <Route path="/governance"         element={<GovernancePage />} />
            </Routes>
          </div>
        </ReactLenis>
      </div>
    </BrowserRouter>
  );
}
