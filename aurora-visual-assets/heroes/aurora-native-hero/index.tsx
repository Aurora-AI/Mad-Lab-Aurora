'use client';

import React, { useRef, useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import Lenis from 'lenis';

// Register GSAP plugins
if (typeof window !== 'undefined') {
  gsap.registerPlugin(ScrollTrigger);
}

interface AuroraNativeHeroProps {
  headline?: string;
  sublines?: string[];
  ctaLabel?: string;
  ctaHref?: string;
  className?: string;
}

/**
 * AuroraNativeHero — Primeiro Ativo Aurora-Native
 * Conceito: "A fábrica se revela"
 * Padrões: P006, P008, P010, P015, P040, P042, P045
 */
export const AuroraNativeHero: React.FC<AuroraNativeHeroProps> = ({
  headline = 'Aurora',
  sublines = [
    'A fábrica não abre — ela emerge.',
    'Silêncio editorial como decisão de design.',
    'Onde a técnica encontra o peso do metal.'
  ],
  ctaLabel = 'Conheça a fábrica',
  ctaHref = '#',
  className = ''
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const pinRef = useRef<HTMLDivElement>(null);
  const headlineRef = useRef<HTMLHeadingElement>(null);
  const sublinesRef = useRef<HTMLDivElement>(null);
  const dividerRef = useRef<HTMLDivElement>(null);
  const ctaRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current || !pinRef.current) return;

    // P045: Reduce Motion check
    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    // P010: Lenis-GSAP Synchronization Bridge
    const lenis = new Lenis();
    lenis.on('scroll', ScrollTrigger.update);
    
    const tickerCb = (time: number) => {
      lenis.raf(time * 1000);
    };
    gsap.ticker.add(tickerCb);
    gsap.ticker.lagSmoothing(0);

    // Split headline into characters for P015
    const chars = headlineRef.current?.querySelectorAll('.aurora-native-hero__char');
    const sublineEls = sublinesRef.current?.querySelectorAll('.aurora-native-hero__subline');
    const ctaElements = ctaRef.current?.children;

    // Master Timeline — 500vh ScrollTrigger
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: containerRef.current,
        start: 'top top',
        end: '+=500%',
        scrub: 1.6, // Física real no controle do visitante
        pin: true,
        anticipatePin: 1,
      }
    });

    // FRAME 0: Silêncio inicial (0% - 15%)
    // Mantido via design (CSS)

    // FRAME 1: Headline emerge (15% - 35%) — P015 + P042
    if (chars) {
      tl.from(chars, {
        opacity: 0,
        y: 40,
        stagger: 0.04,
        duration: 1.2,
        ease: 'elastic.out(1, 0.8)', // P042: Spring real
      }, 0.15);
    }

    // FRAME 2: Sublines cross-fade (35% - 60%) — P008
    if (sublineEls) {
      tl.from(sublineEls, {
        opacity: 0,
        stagger: 0.3,
        duration: 0.8,
        ease: 'none',
      }, 0.35);
    }

    // FRAME 3: Curtain reveal (55% - 75%) — P006
    if (dividerRef.current) {
      tl.from(dividerRef.current, {
        clipPath: 'inset(100% 0 0 0)',
        duration: 1,
        ease: 'power2.inOut',
      }, 0.55);
    }

    // FRAME 4: CTA emerge (75% - 90%) — P040 + P042
    if (ctaElements) {
      tl.from(ctaElements, {
        opacity: 0,
        y: 20,
        stagger: 0.15,
        duration: 1,
        ease: 'elastic.out(1, 0.6)',
      }, 0.75);
    }

    // FRAME 5: Estado final (90% - 100%)
    // Silêncio preservado

    return () => {
      lenis.destroy();
      gsap.ticker.remove(tickerCb);
      ScrollTrigger.getAll().forEach(st => st.kill());
    };
  }, [headline]);

  const headlineChars = headline.split('');

  return (
    <section 
      ref={containerRef} 
      className={`aurora-native-hero ${className}`}
      style={{
        position: 'relative',
        height: '500vh',
        overflowX: 'hidden',
        background: 'var(--color-background, #0a0a0a)'
      }}
    >
      <div 
        ref={pinRef} 
        className="aurora-native-hero__pin"
        style={{
          position: 'sticky',
          top: 0,
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          padding: '0 clamp(1.5rem, 5vw, 6rem)',
        }}
      >
        {/* FRAME 1 — Headline */}
        <h1 
          ref={headlineRef}
          className="aurora-native-hero__headline" 
          aria-label={headline}
          style={{
            fontSize: 'clamp(3rem, 10vw, 9rem)',
            fontWeight: 700,
            letterSpacing: '-0.03em',
            lineHeight: 0.95,
            color: 'var(--color-foreground, #f5f5f0)',
            margin: 0,
            overflow: 'hidden'
          }}
        >
          {headlineChars.map((char, i) => (
            <span 
              key={i} 
              className="aurora-native-hero__char" 
              aria-hidden
              style={{ display: 'inline-block', willChange: 'transform, opacity' }}
            >
              {char === ' ' ? '\u00A0' : char}
            </span>
          ))}
        </h1>

        {/* FRAME 2 — Sublines */}
        <div 
          ref={sublinesRef}
          className="aurora-native-hero__sublines"
          style={{
            marginTop: 'clamp(1.5rem, 3vw, 3rem)',
            maxWidth: '52ch',
          }}
        >
          {sublines.map((line, i) => (
            <p 
              key={i} 
              className="aurora-native-hero__subline"
              style={{
                fontSize: 'clamp(1rem, 1.8vw, 1.25rem)',
                lineHeight: 1.6,
                color: 'var(--color-foreground-muted, #888)',
                margin: '0 0 0.5rem',
                willChange: 'opacity'
              }}
            >
              {line}
            </p>
          ))}
        </div>

        {/* FRAME 3 — Divider curtain */}
        <div 
          ref={dividerRef}
          className="aurora-native-hero__divider" 
          aria-hidden
          style={{
            width: 'clamp(3rem, 8vw, 6rem)',
            height: '1px',
            background: 'var(--color-foreground, #f5f5f0)',
            margin: 'clamp(2rem, 4vw, 4rem) 0',
            willChange: 'clip-path'
          }}
        />

        {/* FRAME 4 — CTA */}
        <div 
          ref={ctaRef}
          className="aurora-native-hero__cta"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}
        >
          <a 
            href={ctaHref} 
            className="aurora-native-hero__cta-button"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              fontSize: 'clamp(0.875rem, 1.2vw, 1rem)',
              fontWeight: 500,
              color: 'var(--color-foreground, #f5f5f0)',
              textDecoration: 'none',
              borderBottom: '1px solid currentColor',
              paddingBottom: '0.25rem',
              width: 'fit-content',
              willChange: 'transform, opacity',
            }}
          >
            {ctaLabel}
          </a>
          <span 
            className="aurora-native-hero__cta-support"
            style={{
              fontSize: 'clamp(0.75rem, 1vw, 0.875rem)',
              color: 'var(--color-foreground-muted, #888)',
              willChange: 'transform, opacity'
            }}
          >
            Production First. Sem atalhos.
          </span>
        </div>
      </div>

      <style jsx>{`
        .aurora-native-hero__cta-button {
          transition: opacity 0.2s ease;
        }
        .aurora-native-hero__cta-button:hover {
          opacity: 0.6;
        }
      `}</style>
    </section>
  );
};

export default AuroraNativeHero;
