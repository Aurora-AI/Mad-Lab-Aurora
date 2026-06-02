import React, { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useLenis } from 'lenis/react';

gsap.registerPlugin(ScrollTrigger);

// Assembly sequence: chaos → explosion → head emerging → assembled
const FRAMES: { src: string; blend: React.CSSProperties['mixBlendMode'] }[] = [
  { src: '/assets/4.png',         blend: 'multiply' }, // fully scattered
  { src: '/assets/3.png',         blend: 'multiply' }, // slight grouping
  { src: '/assets/2.png',         blend: 'multiply' }, // energy burst
  { src: '/assets/5.png',         blend: 'multiply' }, // head emerging
  { src: '/assets/puzzle-pb.png', blend: 'normal'   }, // assembled (dark bg)
];

// ── Palette ──────────────────────────────────────────────────────────────
const PAPER  = '#F3EDE3';
const DARK   = '#0D0A07';
const INK    = '#0D0A07';
const LIGHT  = '#F3EDE3';
const RED    = '#B91C1C';

const INK50  = 'rgba(13,10,7,0.50)';
const INK28  = 'rgba(13,10,7,0.28)';
const INK14  = 'rgba(13,10,7,0.14)';
const INK08  = 'rgba(13,10,7,0.08)';

const PRODUCTS = [
  { name: 'Aurora CRM',     live: true  },
  { name: 'Elysian Lex',    live: false },
  { name: 'Living Doc',     live: false },
];

export default function AuroraHero() {
  const sectionRef  = useRef<HTMLElement>(null);
  const stickyRef   = useRef<HTMLDivElement>(null);
  const headlineRef = useRef<HTMLHeadingElement>(null);
  const subtextRef  = useRef<HTMLParagraphElement>(null);
  const frameRefs   = useRef<(HTMLImageElement | null)[]>([]);
  const progressRef = useRef<HTMLDivElement>(null);

  const lenis = useLenis();

  // Sync Lenis smooth scroll with GSAP ScrollTrigger
  useEffect(() => {
    if (!lenis) return;
    lenis.on('scroll', ScrollTrigger.update);
    return () => { lenis.off('scroll', ScrollTrigger.update); };
  }, [lenis]);

  useEffect(() => {
    const section  = sectionRef.current;
    const sticky   = stickyRef.current;
    const headline = headlineRef.current;
    const subtext  = subtextRef.current;
    if (!section || !sticky) return;

    const frames = frameRefs.current.filter(Boolean) as HTMLImageElement[];
    if (frames.length !== FRAMES.length) return;

    // ── Initial states ────────────────────────────────────────────────────
    gsap.set(frames, { opacity: 0 });
    gsap.set(frames[0], { scale: 1.06, opacity: 0 });

    // ── Entry animation (load, not scroll) ───────────────────────────────
    const reveals = sticky.querySelectorAll<HTMLElement>('[data-hero-reveal]');
    gsap.set(reveals, { y: 52, opacity: 0 });

    // Frame 0 — chaos image enters first, behind the text
    gsap.to(frames[0], {
      scale: 1, opacity: 1,
      duration: 1.8, ease: 'power3.out', delay: 0.15,
    });

    // Text content staggers in after
    gsap.to(reveals, {
      y: 0, opacity: 1,
      duration: 1.1, ease: 'power4.out',
      stagger: 0.09, delay: 0.45,
    });

    // ── Signal header about hero phase (light vs dark) ───────────────────
    const emitPhase = (isDark: boolean) => {
      window.dispatchEvent(new CustomEvent('aurora:hero-phase-dark', { detail: isDark }));
    };
    emitPhase(false); // initial: light

    // ── Scroll-driven timeline ────────────────────────────────────────────
    // Section is 500vh tall; inner div is CSS sticky — GSAP maps scroll to timeline.
    // Timeline positions (unit = seconds, scrub normalises them to scroll distance):
    //
    //   0.0 → 0.4   frame 0 only (chaos visible, page is ivory)
    //   0.4 → 0.9   frame 0→1 cross-fade
    //   0.9 → 1.1   frame 1 only
    //   1.1 → 1.6   frame 1→2 cross-fade
    //   1.2 → 2.0   bg: ivory → dark  (overlaps frame 2 appearing)
    //   1.6 → 2.1   frame 2 only (energy burst — bg going dark)
    //   2.1 → 2.6   frame 2→3 cross-fade (bg now fully dark)
    //   2.6 → 2.9   frame 3 only
    //   2.9 → 3.4   frame 3→4 cross-fade (puzzle-pb assembles in dark)
    //   3.4+        assembled state holds

    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: section,
        start: 'top top',
        end: 'bottom bottom',
        scrub: 1.6,
        onUpdate: (self) => {
          // Signal header when hero bg turns dark (bg transition starts at ~35% progress)
          emitPhase(self.progress > 0.35);
        },
        onLeaveBack: () => emitPhase(false),
        onLeave: () => emitPhase(true),
      },
      defaults: { ease: 'none' },
    });

    // Frame 0 → 1
    tl.to(frames[0], { opacity: 0, duration: 0.5 }, 0.4)
      .to(frames[1], { opacity: 1, duration: 0.5 }, 0.4);

    // Frame 1 → 2
    tl.to(frames[1], { opacity: 0, duration: 0.5 }, 1.1)
      .to(frames[2], { opacity: 1, duration: 0.5 }, 1.1);

    // Background: ivory → dark (starts as frame 2 becomes visible)
    tl.to(sticky, { backgroundColor: DARK, duration: 0.8 }, 1.2);

    // Text colours transition as bg goes dark
    if (headline) tl.to(headline, { color: LIGHT, duration: 0.7 }, 1.3);
    if (subtext)  tl.to(subtext,  { color: 'rgba(243,237,227,0.65)', duration: 0.7 }, 1.3);

    const mutedEls = sticky.querySelectorAll<HTMLElement>('[data-muted]');
    tl.to(mutedEls, { color: 'rgba(243,237,227,0.32)', duration: 0.7 }, 1.3);

    // Nav border and product strip border also soften
    const dividers = sticky.querySelectorAll<HTMLElement>('[data-divider]');
    tl.to(dividers, { borderColor: 'rgba(243,237,227,0.10)', duration: 0.7 }, 1.3);

    // CTA buttons invert for dark bg
    const ctaPrimary = sticky.querySelector<HTMLElement>('[data-cta-primary]');
    const ctaGhost   = sticky.querySelector<HTMLElement>('[data-cta-ghost]');
    if (ctaPrimary) tl.to(ctaPrimary, { backgroundColor: LIGHT, color: DARK, duration: 0.6 }, 1.3);
    if (ctaGhost)   tl.to(ctaGhost,   { color: 'rgba(243,237,227,0.45)', borderColor: 'rgba(243,237,227,0.15)', duration: 0.6 }, 1.3);

    // Frame 2 → 3
    tl.to(frames[2], { opacity: 0, duration: 0.5 }, 2.1)
      .to(frames[3], { opacity: 1, duration: 0.5 }, 2.1);

    // Frame 3 → 4 (puzzle-pb — assembled, dark bg, normal blend)
    tl.to(frames[3], { opacity: 0, duration: 0.5 }, 2.9)
      .to(frames[4], { opacity: 1, duration: 0.5 }, 2.9);

    // Progress bar fills as you scroll
    if (progressRef.current) {
      tl.fromTo(
        progressRef.current,
        { scaleY: 0, transformOrigin: 'top center' },
        { scaleY: 1, duration: 3.4 },
        0
      );
    }

    return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
  }, []);

  return (
    <section
      ref={sectionRef}
      style={{ height: '500vh', position: 'relative' }}
    >
      <div
        ref={stickyRef}
        style={{
          position: 'sticky',
          top: 0,
          height: '100dvh',
          backgroundColor: PAPER,
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
        }}
      >

        {/* ── Hero body — 2 column grid ──────────────────────────────── */}
        <div
          className="aurora-hero-grid"
          style={{
            flex: 1,
            display: 'grid',
            gridTemplateColumns: '55% 45%',
            minHeight: 0,
            paddingTop: '64px',
          }}
        >

          {/* ── Left: Text content ───────────────────────────────────── */}
          <div style={{
            padding: 'clamp(2.5rem, 4.5vw, 5.5rem) var(--px) clamp(2rem, 3vw, 3.5rem)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            overflow: 'hidden',
          }}>

            {/* Top group: eyebrow + headline */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'clamp(1.5rem, 2.5vw, 2.5rem)' }}>

              {/* Eyebrow */}
              <div
                data-hero-reveal
                data-muted
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                }}
              >
                <span style={{
                  width: 5, height: 5,
                  background: RED,
                  display: 'inline-block',
                  flexShrink: 0,
                }} />
                <span style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.6rem',
                  letterSpacing: '0.28em',
                  color: INK50,
                  textTransform: 'uppercase',
                }}>
                  Aurora · Ecossistema de IA Governada
                </span>
              </div>

              {/* Headline */}
              <h1
                ref={headlineRef}
                data-hero-reveal
                style={{
                  fontFamily: 'var(--font-display)',
                  fontStyle: 'italic',
                  fontWeight: 500,
                  fontSize: 'clamp(3rem, 5.5vw, 7.5rem)',
                  lineHeight: 0.96,
                  letterSpacing: '-0.03em',
                  color: INK,
                  margin: 0,
                }}
              >
                Quando tudo<br />
                se fragmenta,{' '}
                <em style={{ color: RED, fontStyle: 'italic' }}>nós</em>
                <br />
                <span style={{ color: INK28 }}>construímos.</span>
              </h1>
            </div>

            {/* Bottom group: subtext + CTAs + product strip */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'clamp(1.25rem, 2vw, 2rem)' }}>

              {/* Subtext */}
              <p
                ref={subtextRef}
                data-hero-reveal
                style={{
                  fontFamily: 'var(--font-body)',
                  fontSize: 'clamp(0.875rem, 0.95vw, 1rem)',
                  color: INK50,
                  lineHeight: 1.7,
                  maxWidth: '46ch',
                  margin: 0,
                  borderLeft: `2px solid ${RED}`,
                  paddingLeft: '1.25rem',
                }}
              >
                Automação com contrato de confiabilidade.
                Decisões de IA com trilha de auditoria completa.
                Sistemas que sobrevivem ao primeiro contato
                com a realidade operacional.
              </p>

              {/* CTAs */}
              <div
                data-hero-reveal
                style={{ display: 'flex', gap: '0.875rem', alignItems: 'center', flexWrap: 'wrap' }}
              >
                <a
                  href="#cta"
                  data-cta-primary
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.6rem',
                    background: INK,
                    color: PAPER,
                    padding: '0.9rem 1.75rem',
                    fontFamily: 'var(--font-body)',
                    fontWeight: 700,
                    fontSize: '0.78rem',
                    letterSpacing: '0.1em',
                    textTransform: 'uppercase',
                    textDecoration: 'none',
                    transition: 'opacity 0.2s',
                  }}
                  onMouseEnter={e => { (e.currentTarget as HTMLAnchorElement).style.opacity = '0.8'; }}
                  onMouseLeave={e => { (e.currentTarget as HTMLAnchorElement).style.opacity = '1'; }}
                >
                  Agendar Diagnóstico <span aria-hidden>→</span>
                </a>

                <a
                  href="#what-we-built"
                  data-cta-ghost
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.4rem',
                    color: INK28,
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.68rem',
                    letterSpacing: '0.18em',
                    textTransform: 'uppercase',
                    textDecoration: 'none',
                    border: `1px solid ${INK14}`,
                    padding: '0.9rem 1.25rem',
                    transition: 'color 0.2s, border-color 0.2s',
                  }}
                  onMouseEnter={e => {
                    const el = e.currentTarget as HTMLAnchorElement;
                    el.style.color = INK;
                    el.style.borderColor = INK;
                  }}
                  onMouseLeave={e => {
                    const el = e.currentTarget as HTMLAnchorElement;
                    el.style.color = INK28;
                    el.style.borderColor = INK14;
                  }}
                >
                  Ver os sistemas
                </a>
              </div>

              {/* Product status strip */}
              <div
                data-hero-reveal
                data-divider
                style={{
                  display: 'flex',
                  gap: '2rem',
                  paddingTop: '1.25rem',
                  borderTop: `1px solid ${INK08}`,
                  flexWrap: 'wrap',
                }}
              >
                {PRODUCTS.map(p => (
                  <div key={p.name} style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.58rem',
                    letterSpacing: '0.08em',
                    textTransform: 'uppercase',
                  }}>
                    <span style={{
                      width: 4, height: 4,
                      borderRadius: '50%',
                      background: p.live ? RED : INK14,
                      flexShrink: 0,
                    }} />
                    <span data-muted style={{
                      color: p.live ? 'rgba(13,10,7,0.7)' : INK28,
                    }}>
                      {p.name}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* ── Right: Puzzle assembly ────────────────────────────────── */}
          <div style={{
            position: 'relative',
            overflow: 'hidden',
          }}>

            {/* Scroll progress line — left edge of the column */}
            <div style={{
              position: 'absolute',
              left: 0,
              top: '12%',
              bottom: '12%',
              width: 1,
              background: INK08,
              zIndex: 10,
            }}>
              <div
                ref={progressRef}
                style={{
                  width: '100%',
                  height: '100%',
                  background: RED,
                  transform: 'scaleY(0)',
                  transformOrigin: 'top center',
                }}
              />
            </div>

            {/* Frame stack — all absolutely centered, cross-fading via GSAP */}
            {FRAMES.map((frame, i) => (
              <img
                key={frame.src}
                ref={el => { frameRefs.current[i] = el; }}
                src={frame.src}
                alt=""
                aria-hidden
                draggable={false}
                style={{
                  position: 'absolute',
                  top: '50%',
                  left: '52%',
                  transform: 'translate(-50%, -50%)',
                  width: '92%',
                  height: '92%',
                  objectFit: 'contain',
                  mixBlendMode: frame.blend,
                  opacity: 0,
                  userSelect: 'none',
                  pointerEvents: 'none',
                }}
              />
            ))}

            {/* Scroll hint — bottom right corner */}
            <div style={{
              position: 'absolute',
              bottom: '2.5rem',
              right: '2rem',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '0.75rem',
              zIndex: 5,
            }}>
              <span data-muted style={{
                fontFamily: 'var(--font-mono)',
                fontSize: '0.52rem',
                letterSpacing: '0.22em',
                color: INK28,
                textTransform: 'uppercase',
                writingMode: 'vertical-rl',
                transform: 'rotate(180deg)',
              }}>
                Role para montar
              </span>
              <div style={{
                width: 1,
                height: '3rem',
                background: `linear-gradient(to bottom, ${INK28}, transparent)`,
              }} />
            </div>

            {/* Frame counter — top right */}
            <div style={{
              position: 'absolute',
              top: '1.5rem',
              right: '1.5rem',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.55rem',
              letterSpacing: '0.15em',
              color: INK28,
              zIndex: 5,
            }}>
              <span data-muted>01 — 09</span>
            </div>
          </div>
        </div>

        {/* ── Bottom strip ───────────────────────────────────────────── */}
        <div
          data-divider
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '0.875rem var(--px)',
            borderTop: `1px solid ${INK08}`,
            flexShrink: 0,
          }}
        >
          <span data-muted style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.55rem',
            letterSpacing: '0.22em',
            color: INK28,
            textTransform: 'uppercase',
          }}>
            Role para descobrir
          </span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span data-muted style={{
              width: 4, height: 4,
              borderRadius: '50%',
              background: RED,
              display: 'inline-block',
            }} />
            <span data-muted style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.55rem',
              letterSpacing: '0.12em',
              color: INK28,
            }}>
              Aurora · 2026
            </span>
          </div>
        </div>
      </div>

      {/* ── Responsive overrides ────────────────────────────────────── */}
      <style>{`
        /* Tablet: reduce headline size */
        @media (max-width: 900px) {
          .aurora-hero-grid {
            grid-template-columns: 1fr 1fr !important;
          }
        }

        /* Mobile: stack columns */
        @media (max-width: 680px) {
          .aurora-hero-grid {
            grid-template-columns: 1fr !important;
            grid-template-rows: auto 45vw;
          }
          .aurora-hero-grid > div:first-child {
            padding-top: 2rem !important;
            padding-bottom: 1.5rem !important;
          }
        }

        @media (max-width: 480px) {
          .aurora-hero-grid > div:first-child h1 {
            font-size: clamp(2.6rem, 12vw, 4rem) !important;
          }
        }
      `}</style>
    </section>
  );
}
