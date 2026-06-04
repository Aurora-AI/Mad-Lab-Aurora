import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer
      style={{
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
        padding: '3rem var(--px)',
        display: 'flex',
        flexDirection: 'column',
        gap: '4rem',
      }}
    >
      <div style={{ opacity: 1 /* Content reset */ }}>
      <div className="flex justify-between items-start flex-wrap gap-8">
        <div className="flex flex-col gap-4">
          <Link
            to="/"
            style={{
              fontFamily: 'var(--font-body)',
              fontWeight: 900,
              fontSize: '1.25rem',
              letterSpacing: '-0.04em',
              color: 'var(--page-text)',
              textDecoration: 'none',
            }}
          >
            ELYSIAN
          </Link>
          <div className="flex items-center gap-2">
            <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--color-elysian-signal)', opacity: 0.8 }} className="animate-pulse" />
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--page-text-soft)', opacity: 0.5, letterSpacing: '0.2rem', textTransform: 'uppercase' }}>Factory Operational</span>
          </div>
        </div>

        <nav
          style={{
            display: 'flex',
            gap: '3rem',
          }}
        >
          {['Ecossistema', 'Produtos', 'Método', 'Diretrizes'].map(item => (
            <span 
              key={item} 
              style={{ 
                cursor: 'pointer',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.65rem',
                color: 'var(--page-text-soft)',
                opacity: 0.5,
                transition: 'opacity 0.3s ease, color 0.3s ease',
                letterSpacing: '0.1em'
              }}
              onMouseEnter={e => {
                e.currentTarget.style.color = 'var(--color-elysian-signal)';
                e.currentTarget.style.opacity = '1';
              }}
              onMouseLeave={e => {
                e.currentTarget.style.color = 'var(--page-text-soft)';
                e.currentTarget.style.opacity = '0.5';
              }}
            >
              {item}
            </span>
          ))}
        </nav>
      </div>

      <div
        className="flex justify-between items-end flex-wrap gap-4 pt-8"
        style={{ borderTop: '1px solid rgba(255,255,255,0.03)' }}
      >
        <div className="flex flex-col gap-1">
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '9px', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase', letterSpacing: '0.3em' }}>Audit Note</span>
          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '10px', color: 'var(--page-text-soft)', opacity: 0.5 }}>
            Build: 0x7E3A_2026 // Hash: 9f8ea...2d31 // Synchronized: {new Date().toLocaleDateString('pt-BR')}
          </span>
        </div>

        <span
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            color: 'var(--page-text-soft)',
            opacity: 0.3,
            letterSpacing: '0.2em'
          }}
        >
          AURORA FACTORY // MADLAB // © 2026
        </span>
      </div>
    </div>
    </footer>
  );
}
