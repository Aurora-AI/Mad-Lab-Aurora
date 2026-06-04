'use client';

import React from 'react';

export const EthicalAnchor: React.FC = () => {
  return (
    <div
      style={{
        width: '100%',
        padding: '2rem var(--px)',
        background: '#fcfcfc',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        borderTop: '1px solid rgba(0,0,0,0.05)',
        borderBottom: '1px solid rgba(0,0,0,0.05)',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1.5rem',
          maxWidth: 'var(--max-width)',
          width: '100%',
        }}
      >
        <div style={{ flex: 1, height: '1px', background: 'linear-gradient(to right, transparent, rgba(0,0,0,0.1))' }} />
        <span
          style={{
            fontFamily: 'var(--font-mono, monospace)',
            fontSize: 'clamp(0.7rem, 1.2vw, 0.85rem)',
            letterSpacing: '0.3em',
            textTransform: 'uppercase',
            color: '#111',
            textAlign: 'center',
            fontWeight: 500,
          }}
        >
          Pessoas estão sempre em primeiro lugar
        </span>
        <div style={{ flex: 1, height: '1px', background: 'linear-gradient(to left, transparent, rgba(0,0,0,0.1))' }} />
      </div>
    </div>
  );
};

export default EthicalAnchor;
