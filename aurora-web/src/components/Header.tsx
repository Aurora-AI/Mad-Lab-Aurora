import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const INK   = '#0D0A07';
const LIGHT = '#F3EDE3';

export default function Header() {
  const [scrolled,   setScrolled]   = useState(false);
  const [heroDark,   setHeroDark]   = useState(false);
  const location = useLocation();
  const isHome = location.pathname === '/';

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 50);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Listen for hero phase signal from AuroraHero GSAP timeline
  useEffect(() => {
    if (!isHome) return;
    const onPhase = (e: Event) => {
      setHeroDark((e as CustomEvent<boolean>).detail);
    };
    window.addEventListener('aurora:hero-phase-dark', onPhase);
    return () => window.removeEventListener('aurora:hero-phase-dark', onPhase);
  }, [isHome]);

  // On home, hero starts ivory (light) → header text must be dark until hero turns dark
  const textColor = isHome && !heroDark ? INK : 'var(--page-text)';
  const mutedText = isHome && !heroDark
    ? 'rgba(13,10,7,0.5)'
    : 'color-mix(in srgb, var(--page-text) 55%, transparent)';
  const bgColor   = scrolled
    ? (isHome && !heroDark
        ? 'rgba(243,237,227,0.92)'
        : 'color-mix(in srgb, var(--page-bg) 88%, transparent)')
    : 'transparent';

  const navLinks = [
    { label: 'Ecossistema', href: '#our-answer'   },
    { label: 'Produtos',    href: '#what-we-built' },
    { label: 'Método',      href: '#the-method'    },
    { label: 'Arsenal',     href: '/arsenal'       },
  ];

  const scrollTo = (id: string) => {
    if (id.startsWith('/')) {
      window.location.href = id;
      return;
    }
    if (location.pathname !== '/') {
      window.location.href = `/${id}`;
      return;
    }
    const el = document.querySelector(id);
    el?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <header
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 100,
        height: '64px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        paddingLeft: 'var(--px)',
        paddingRight: 'var(--px)',
        transition: 'background 0.4s ease, backdrop-filter 0.4s ease, border-color 0.4s ease, color 0.4s ease',
        background: scrolled ? `rgba(var(--page-bg-rgb), 0.92)` : 'transparent',
        backdropFilter: scrolled ? 'blur(12px)' : 'none',
        WebkitBackdropFilter: scrolled ? 'blur(12px)' : 'none',
        borderBottom: scrolled
          ? `1px solid rgba(var(--page-text-rgb), 0.08)`
          : '1px solid transparent',
      }}
    >
      {/* Wordmark */}
      <Link
        to="/"
        style={{
          fontFamily: 'var(--font-body)',
          fontWeight: 900,
          fontSize: '0.875rem',
          letterSpacing: '0.2em',
          color: 'var(--page-text)',
          textDecoration: 'none',
          textTransform: 'uppercase',
          transition: 'color 0.4s ease',
        }}
      >
        Aurora
      </Link>

      {/* Nav links */}
      <nav style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
        {navLinks.map(link => (
          <button
            key={link.label}
            onClick={() => scrollTo(link.href)}
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.68rem',
              letterSpacing: '0.12em',
              textTransform: 'uppercase',
              color: 'var(--page-text-soft)',
              opacity: 0.6,
              padding: 0,
              transition: 'opacity 0.2s ease, color 0.2s ease',
            }}
            onMouseEnter={e => { 
                e.currentTarget.style.color = 'var(--page-text)';
                e.currentTarget.style.opacity = '1';
            }}
            onMouseLeave={e => { 
                e.currentTarget.style.color = 'var(--page-text-soft)';
                e.currentTarget.style.opacity = '0.6';
            }}
          >
            {link.label}
          </button>
        ))}

        <button
          onClick={() => scrollTo('#cta')}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            background: 'var(--page-text)',
            color: 'var(--page-bg)',
            border: 'none',
            cursor: 'pointer',
            fontFamily: 'var(--font-body)',
            fontWeight: 700,
            fontSize: '0.72rem',
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
            padding: '0.55rem 1.25rem',
            transition: 'background 0.4s ease, color 0.4s ease, opacity 0.2s',
          }}
          onMouseEnter={e => { e.currentTarget.style.opacity = '0.8'; }}
          onMouseLeave={e => { e.currentTarget.style.opacity = '1'; }}
        >
          Agendar
        </button>
      </nav>
    </header>
  );
}
