import { ArrowRight } from 'lucide-react';

const steps = [
  {
    num: '01',
    title: 'Diagnóstico de infraestrutura',
    desc: 'Conversa de 60 minutos com o fundador. Mapeamos sua operação atual de IA: o que está rodando, o que está falhando, e onde a ausência de governança está acumulando risco.',
  },
  {
    num: '02',
    title: 'Relatório de gaps',
    desc: 'Documento estruturado com os três principais pontos de falha identificados, a causa raiz de cada um, e qual componente da Aurora resolve cada problema.',
  },
  {
    num: '03',
    title: 'Proposta de arquitetura',
    desc: 'Se houver fit, propomos o escopo de implementação: quais sistemas, em qual ordem, com quais contratos de entrega e critérios de auditoria.',
  },
];

export default function CallToAction() {
  return (
    <section
      id="cta"
      style={{
        padding: 'var(--section-py) var(--px)',
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
        color: 'var(--page-text)',
      }}
    >
      {/* Capítulo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: 'clamp(3rem, 6vw, 5rem)', opacity: 1 /* Content reset */ }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.35em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Capítulo 08
        </span>
        <div style={{ flex: 1, height: '1px', background: 'var(--page-text)', opacity: 0.1 }} />
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.25em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          O próximo passo
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 'clamp(3rem, 6vw, 6rem)', alignItems: 'start' }} className="cta-grid">

        {/* Esquerda: headline + CTA */}
        <div>
          <h2
            style={{
              fontFamily: 'var(--font-display)',
              fontStyle: 'italic',
              fontSize: 'clamp(2.5rem, 6vw, 7rem)',
              fontWeight: 500,
              lineHeight: 0.92,
              letterSpacing: '-0.02em',
              color: 'var(--page-text)',
              marginBottom: 'clamp(1.5rem, 3vw, 2.5rem)',
            }}
          >
            O próximo passo
            <br />
            não é uma aposta.
            <br />
            <span style={{ color: 'var(--page-text-soft)', opacity: 0.3 }}>É uma decisão.</span>
          </h2>

          <p
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.9rem',
              color: 'var(--page-text-soft)',
              opacity: 0.7,
              lineHeight: 1.75,
              maxWidth: '44ch',
              marginBottom: 'clamp(2rem, 4vw, 3.5rem)',
            }}
          >
            Não vendemos software. Construímos infraestrutura. A conversa inicial não é um pitch — é um diagnóstico real da sua operação de IA e uma avaliação honesta se a Aurora resolve seu problema.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', alignItems: 'flex-start' }}>
            <a
              href="mailto:winhaski@gmail.com?subject=Diagnóstico Aurora — Infraestrutura de IA"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.75rem',
                background: 'var(--page-text)',
                color: 'var(--page-bg)',
                padding: '1.1rem 2.5rem',
                fontFamily: 'var(--font-body)',
                fontWeight: 900,
                fontSize: '0.85rem',
                letterSpacing: '0.15em',
                textTransform: 'uppercase',
                textDecoration: 'none',
                transition: 'opacity 0.2s',
              }}
              onMouseEnter={e => (e.currentTarget.style.opacity = '0.8')}
              onMouseLeave={e => (e.currentTarget.style.opacity = '1')}
            >
              Solicitar Diagnóstico
              <ArrowRight size={16} />
            </a>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'rgba(0,0,0,0.35)', letterSpacing: '0.1em' }}>
              Resposta em até 24h · Sem compromisso de contratação
            </span>
          </div>
        </div>

        {/* Direita: o que acontece */}
        <div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'rgba(0,0,0,0.3)', letterSpacing: '0.3em', textTransform: 'uppercase', marginBottom: '1.5rem' }}>
            O que acontece quando você entra em contato
          </div>

          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {steps.map((s, i) => (
              <div
                key={s.num}
                style={{
                  display: 'flex',
                  gap: '1.5rem',
                  padding: '1.75rem 0',
                  borderTop: '1px solid rgba(0,0,0,0.08)',
                  alignItems: 'flex-start',
                }}
              >
                <span
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.6rem',
                    color: 'rgba(0,0,0,0.25)',
                    letterSpacing: '0.15em',
                    flexShrink: 0,
                    marginTop: '0.2rem',
                  }}
                >
                  {s.num}
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <h4 style={{ fontFamily: 'var(--font-body)', fontWeight: 700, fontSize: '0.95rem', color: 'var(--page-text)', margin: 0, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    {s.title}
                  </h4>
                  <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--page-text-soft)', opacity: 0.6, lineHeight: 1.7, margin: 0 }}>
                    {s.desc}
                  </p>
                </div>
              </div>
            ))}
            <div style={{ borderTop: '1px solid rgba(0,0,0,0.08)' }} />
          </div>
        </div>
      </div>

      <style>{`
        @media (min-width: 1100px) {
          .cta-grid { grid-template-columns: 1fr 1fr !important; }
        }
      `}</style>
    </section>
  );
}
