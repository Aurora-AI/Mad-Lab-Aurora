import React, { useEffect, useState } from 'react';
import { ElysianScene } from './ElysianScene';

const ElysianHero: React.FC<{ isLoaded?: boolean }> = ({ isLoaded = true }) => {
  const [mounted, setMounted] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);

  useEffect(() => {
    if (isLoaded) {
      setMounted(true);
    }
    
    const handleScroll = () => {
      const progress = window.scrollY / window.innerHeight;
      setScrollProgress(progress);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isLoaded]);

  return (
    <section className="relative w-full h-[200vh] bg-[var(--page-bg)] overflow-hidden">
      {/* Camada WebGL Fixa */}
      <div className="sticky top-0 w-full h-screen">
        {isLoaded && <ElysianScene scrollProgress={scrollProgress} />}
        
        {/* Overlay Editorial */}
        <div className="relative z-10 w-full h-full flex flex-col justify-center px-[var(--px)]">
          <div className="grid grid-cols-12 gap-6 w-full">
            
            {/* Metadata / Eyebrow */}
            <div className={`col-span-12 mb-8 transition-all duration-[1200ms] ease-vogue delay-[800ms] ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
              <span className="font-mono text-[10px] uppercase tracking-[0.3em] text-elysian-ink-soft">
                Protocolo Institutional // 2026 // Elysian Corp
              </span>
            </div>

            {/* Headline Monumental - Vogue Style */}
            <h1 className={`col-span-12 md:col-span-10 lg:col-span-8 font-vogue text-[clamp(64px,12vw,180px)] font-light leading-[0.85] tracking-[-0.04em] text-elysian-ink transition-all duration-[1800ms] ease-vogue delay-[1000ms] ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
              O campo não precisa de mais <em className="italic text-elysian-signal">IA.</em><br />
              Precisa de menos dúvida.
            </h1>

            {/* Subtexto Editorial */}
            <div className={`col-span-12 md:col-span-6 mt-12 transition-all duration-[1200ms] ease-vogue delay-[1400ms] ${mounted ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
              <p className="font-body text-lg md:text-xl text-elysian-ink-soft leading-relaxed max-w-[52ch]">
                Auditoria determinística para ambientes que não aceitam probabilidade como resposta. A soberania dos dados em sua forma mais pura.
              </p>
              
              <div className="mt-12 flex items-center gap-8">
                <button className="group relative overflow-hidden bg-elysian-ink text-elysian-parchment px-10 py-4 font-mono text-[11px] uppercase tracking-[0.2em] transition-transform active:scale-95">
                  <span className="relative z-10">Iniciar Protocolo</span>
                  <div className="absolute inset-0 bg-elysian-signal transform translate-y-full transition-transform group-hover:translate-y-0" />
                </button>
                
                <div className="h-px w-24 bg-elysian-signal/30 hidden md:block" />
              </div>
            </div>

          </div>
        </div>

        {/* Indicador de Profundidade / Scroll */}
        <div className="absolute right-12 bottom-12 flex flex-col items-end gap-4">
          <span className="font-mono text-[9px] uppercase tracking-[0.4em] text-elysian-ink/20 transform rotate-90 origin-right translate-y-12">
            Depth Analysis: {(scrollProgress * 100).toFixed(1)}%
          </span>
          <div className="w-px h-24 bg-elysian-ink/10 relative overflow-hidden">
            <div 
              className="absolute top-0 left-0 w-full bg-elysian-signal transition-all duration-300"
              style={{ height: `${Math.min(scrollProgress * 100, 100)}%` }}
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default ElysianHero;
