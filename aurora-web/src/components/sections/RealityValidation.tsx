import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { IdentityFragmenter } from '../fx/IdentityFragmenter';

gsap.registerPlugin(ScrollTrigger);

export const RealityValidation: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const leftRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Pinning logic for editorial feel
      ScrollTrigger.create({
        trigger: containerRef.current,
        start: "top top",
        end: "bottom bottom",
        pin: leftRef.current,
        pinSpacing: false,
        scrub: true,
      });
    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <section 
      ref={containerRef}
      className="relative w-full bg-parchment overflow-hidden border-t border-ink/5"
    >
      <div className="flex flex-col md:flex-row min-h-[200vh]">
        {/* Left: Argumentation (40%) */}
        <div 
          ref={leftRef}
          className="w-full md:w-[40%] h-screen flex flex-col justify-center p-8 md:p-20 z-10"
        >
          <span className="font-mono text-[10px] text-aureate tracking-[0.4em] mb-8 uppercase">
            02 // REALITY VALIDATION
          </span>
          <h2 className="font-display text-5xl md:text-7xl text-ink leading-[1.1] mb-10">
            A Verdade não é <br />
            <span className="italic font-light">relativa</span>, <br />
            é binária.
          </h2>
          <div className="space-y-8 max-w-md">
            <p className="font-editorial text-lg text-ink/80 leading-relaxed">
                No vácuo entre o dado bruto e a decisão estratégica, o Elysian Lex reconstrói a cadeia de custódia com precisão atômica. 
            </p>
            
            {/* Stats Grid */}
            <div className="grid grid-cols-2 gap-8 py-8 border-t border-ink/10">
                <div>
                    <span className="block font-display text-4xl text-ink">99.9%</span>
                    <span className="font-mono text-[9px] text-ink/40 uppercase tracking-widest">Factual Integrity</span>
                </div>
                <div>
                    <span className="block font-display text-4xl text-ink">0.0ms</span>
                    <span className="font-mono text-[9px] text-ink/40 uppercase tracking-widest">Hallucination Delta</span>
                </div>
            </div>
          </div>
        </div>

        {/* Right: The Evidence (60%) */}
        <div className="w-full md:w-[60%] relative">
          <div className="sticky top-0 w-full h-screen flex items-center justify-center p-8 md:p-20">
            <div className="w-full h-[70vh] relative group">
              <IdentityFragmenter 
                imageSrc="https://images.unsplash.com/photo-1589829545856-d10d557cf95f?q=80&w=2070&auto=format&fit=crop" 
              />
              
              {/* Technical Overlays */}
              <div className="absolute bottom-10 left-10 font-mono text-[9px] text-ink/30 space-y-2 pointer-events-none">
                <div>HASH: 0x82f...a12</div>
                <div>SEC: ELYSIAN_CORE_V2</div>
              </div>
            </div>
          </div>
          
          {/* Scroll spacer to allow pinning duration */}
          <div className="h-screen"></div>
        </div>
      </div>
    </section>
  );
};

export default RealityValidation;
