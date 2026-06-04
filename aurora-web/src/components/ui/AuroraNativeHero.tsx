'use client';

import React, { useRef, useEffect, useState } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { Canvas } from '@react-three/fiber';
import { AuroraHeroScene } from './AuroraHeroScene';

if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

interface AuroraNativeHeroProps {
  className?: string;
  isLoaded?: boolean;
}

/**
 * AuroraNativeHero — Sovereign Clarity Prototype
 * Conceito: Minimalismo, Espaço em Branco, Caos -> Elysian
 */
export const AuroraNativeHero: React.FC<AuroraNativeHeroProps> = ({
  className = '',
  isLoaded = false
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [canAnimate, setCanAnimate] = useState(false);

  useEffect(() => {
    if (isLoaded) {
      const timer = setTimeout(() => {
        setCanAnimate(true);
      }, 800); // Regra do Silêncio: 0.8s de repouso obrigatório
      return () => clearTimeout(timer);
    }
  }, [isLoaded]);

  useEffect(() => {
    if (!containerRef.current) return;

    const st = ScrollTrigger.create({
      trigger: containerRef.current,
      start: 'top top',
      end: '+=400%',
      scrub: 1,
      pin: true,
      onUpdate: (self) => {
        if (canAnimate) {
          setScrollProgress(self.progress);
        }
      },
    });

    return () => {
      st.kill();
    };
  }, [canAnimate]);

  return (
    <section
      ref={containerRef}
      className={`aurora-native-hero ${className} select-none`}
      style={{
        position: 'relative',
        height: '400vh',
        overflowX: 'hidden',
        background: 'var(--page-bg)',
        zIndex: 1,
      }}
    >
      {/* Background WebGL Fixado */}
        <div style={{ 
          position: 'fixed', 
          top: 0,
          left: 0,
          width: '100%',
          height: '100vh',
          opacity: canAnimate ? 1 : 0, 
          transition: 'opacity 2.5s var(--ease-monumental)',
          zIndex: 1,
          pointerEvents: 'none'
        }}>
          <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
            <AuroraHeroScene progress={scrollProgress} />
          </Canvas>
        </div>

      {/* Overlay de Conteúdo (Clareza) */}
      <div
        style={{
          position: 'relative',
          zIndex: 3,
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '0 2rem',
          textAlign: 'center',
          opacity: Math.max(0, (scrollProgress - 0.7) * 5),
          pointerEvents: scrollProgress > 0.7 ? 'auto' : 'none',
          transition: 'opacity 0.8s var(--ease-gravity)',
        }}
      >
        <h2
          style={{
            fontSize: 'clamp(0.8rem, 1.5vw, 1rem)',
            fontWeight: 400,
            letterSpacing: '0.4em',
            textTransform: 'uppercase',
            color: 'var(--color-aureate-weight)',
            marginBottom: '1.5rem',
            fontFamily: 'var(--font-mono, monospace)',
          }}
        >
          Sovereign Transparency
        </h2>
        <p
          style={{
            fontSize: 'clamp(1.5rem, 4vw, 3.5rem)',
            maxWidth: '25ch',
            lineHeight: 1.1,
            color: 'var(--page-text)',
            fontFamily: 'var(--font-display)',
            fontStyle: 'italic',
          }}
        >
          Onde outros vêem caos,<br />nós codificamos herança.
        </p>
      </div>

      {/* Profundidade Impossível (Vignette com temperatura) */}
      <div 
        style={{
          position: 'fixed',
          inset: 0,
          background: 'radial-gradient(circle at center, transparent 0%, rgba(10, 10, 12, 0.8) 100%)',
          pointerEvents: 'none',
          zIndex: 2
        }}
      />
    </section>
  );
};

export default AuroraNativeHero;