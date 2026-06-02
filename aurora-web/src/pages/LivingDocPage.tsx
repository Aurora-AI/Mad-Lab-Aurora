import React from 'react';

export default function LivingDocPage() {
  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '2rem var(--px)',
        paddingTop: '72px',
        background: 'var(--page-bg)',
        color: 'var(--page-text)',
        textAlign: 'center',
        gap: '1.5rem',
      }}
    >
      <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', letterSpacing: '0.35em', textTransform: 'uppercase', color: '#00FFEF' }}>
        [ LIVING DOCUMENT // TRUSTWARE ]
      </span>
      <h1 style={{ fontFamily: 'var(--font-display)', fontStyle: 'italic', fontSize: 'clamp(2.5rem, 6vw, 6rem)', lineHeight: 0.92, letterSpacing: '-0.025em', margin: 0 }}>
        Não é output.<br />É evidência auditável.
      </h1>
      <p style={{ fontFamily: 'var(--font-body)', fontSize: '1rem', color: 'color-mix(in srgb, var(--page-text) 55%, transparent)', maxWidth: '480px', lineHeight: 1.6 }}>
        Página do produto em construção. O Living Document é o ativo de confiança que materializa o Trustware.
      </p>
    </div>
  );
}
