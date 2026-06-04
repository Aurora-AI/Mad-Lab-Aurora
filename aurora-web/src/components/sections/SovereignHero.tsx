import React, { useEffect, useState, useRef } from 'react';
import { motion } from 'framer-motion';

export const SovereignHero: React.FC<{ isLoaded?: boolean }> = ({ isLoaded = true }) => {
  const [mounted, setMounted] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isLoaded) {
      setMounted(true);
    }
  }, [isLoaded]);

  return (
    <section 
      ref={containerRef}
      className="relative w-full h-screen bg-parchment flex items-center px-(--px) overflow-hidden"
    >
      {/* Grid Background (Subtle) */}
      <div className="absolute inset-0 opacity-[0.03] pointer-events-none">
          <div className="w-full h-full" style={{ backgroundImage: 'radial-gradient(var(--color-ink) 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
      </div>

      <div className="container mx-auto">
        <div className="max-w-5xl">
          {/* Section ID / Label (Voz 2) */}
          <div className={`overflow-hidden mb-8`}>
            <motion.span 
              initial={{ y: "100%" }}
              animate={mounted ? { y: 0 } : {}}
              transition={{ duration: 0.8, ease: [0.33, 1, 0.68, 1], delay: 0.2 }}
              className="block font-mono text-[10px] text-aureate tracking-[0.4em] uppercase"
            >
              01 // THE SOVEREIGN FILTER
            </motion.span>
          </div>

          {/* Headline (Voz 1) */}
          <h1 className="font-display text-[clamp(48px,8vw,120px)] leading-[0.95] text-ink tracking-[-0.02em]">
            <div className="overflow-hidden">
              <motion.span
                initial={{ y: "100%" }}
                animate={mounted ? { y: 0 } : {}}
                transition={{ duration: 1.2, ease: [0.33, 1, 0.68, 1], delay: 0.4 }}
                className="block"
              >
                O Fim da Probabilidade.
              </motion.span>
            </div>
            <div className="overflow-hidden mt-2">
              <motion.span
                initial={{ y: "100%" }}
                animate={mounted ? { y: 0 } : {}}
                transition={{ duration: 1.2, ease: [0.33, 1, 0.68, 1], delay: 0.6 }}
                className="block italic font-light"
              >
                O Início do Determinismo Soberano.
              </motion.span>
            </div>
          </h1>

          {/* Subtext (Voz 3) */}
          <div className="mt-16 flex flex-col md:flex-row md:items-start gap-12">
            <div className="w-full md:w-1/3">
                 <motion.div
                    initial={{ scaleX: 0 }}
                    animate={mounted ? { scaleX: 1 } : {}}
                    transition={{ duration: 1, delay: 1 }}
                    className="h-px w-12 bg-aureate mb-6 origin-left"
                 />
                 <motion.p 
                    initial={{ opacity: 0 }}
                    animate={mounted ? { opacity: 0.8 } : {}}
                    transition={{ duration: 1.5, delay: 1.2 }}
                    className="font-editorial text-lg text-ink leading-relaxed"
                 >
                    A Aurora não é uma plataforma de automação. É uma infraestrutura de confiança para quem exige soberania técnica absoluta.
                 </motion.p>
            </div>
            
            <div className="flex-1 md:pl-20">
                <motion.div
                   initial={{ opacity: 0 }}
                   animate={mounted ? { opacity: 1 } : {}}
                   transition={{ duration: 1.5, delay: 1.5 }}
                   className="space-y-6"
                >
                    <p className="font-mono text-[11px] text-ink/40 uppercase tracking-widest leading-loose">
                        Protocol_Status: <span className="text-aureate shimmer">ACTIVE</span><br />
                        Integrity_Check: 100%<br />
                        Environment: Sovereign_Ink
                    </p>
                </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Optical Artifact */}
      <div className="absolute right-0 bottom-0 p-12 opacity-[0.03] font-mono text-[20vw] leading-none pointer-events-none select-none text-ink font-black">
        AU
      </div>
    </section>
  );
};

export default SovereignHero;
