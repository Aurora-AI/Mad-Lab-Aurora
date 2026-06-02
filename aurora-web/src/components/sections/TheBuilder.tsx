const convictions = [
  'IA sem governança não é inovação — é risco acumulado sem responsável.',
  'Velocidade de implementação sem arquitetura é dívida técnica paga com juros operacionais.',
  'O modelo não é o produto. A infraestrutura que o sustenta é.',
  'Auditabilidade não é feature — é pré-requisito para qualquer sistema crítico.',
];

export default function TheBuilder() {
  return (
    <section
      id="the-builder"
      style={{
        padding: 'var(--section-py) var(--px)',
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
      }}
    >
      {/* Capítulo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: 'clamp(3rem, 6vw, 5rem)' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.35em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Capítulo 07
        </span>
        <div style={{ flex: 1, height: '1px', background: 'var(--page-text)', opacity: 0.05 }} />
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.25em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Quem constrói
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 'clamp(3rem, 6vw, 6rem)', alignItems: 'start' }} className="builder-grid">

        {/* Identidade */}
        <div>
          <div style={{ marginBottom: '2rem' }}>
            <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.3em', color: 'var(--page-text-soft)', opacity: 0.5, textTransform: 'uppercase', display: 'block', marginBottom: '0.75rem' }}>
              Rodrigo Winhaski · Fundador · Aurora
            </span>
            <h2
              style={{
                fontFamily: 'var(--font-display)',
                fontStyle: 'italic',
                fontSize: 'clamp(2.5rem, 5vw, 5.5rem)',
                fontWeight: 500,
                lineHeight: 0.95,
                letterSpacing: '-0.02em',
                color: 'var(--page-text)',
                margin: 0,
              }}
            >
              O futuro é determinista.
              <br />
              <span style={{ color: 'var(--page-text-soft)', opacity: 0.4 }}>Construo sistemas que
              <br />tornam o erro improvável.</span>
            </h2>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', maxWidth: '52ch', marginBottom: 'clamp(2.5rem, 5vw, 4rem)' }}>
            <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--page-text-soft)', opacity: 0.7, lineHeight: 1.75, margin: 0 }}>
              Rodrigo construiu a Aurora a partir de uma experiência direta: implementar automações de IA em operações reais e ver o que acontece quando não há governança. Não em teoria — em produção, com consequências.
            </p>
            <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--page-text-soft)', opacity: 0.7, lineHeight: 1.75, margin: 0 }}>
              O resultado foi uma convicção: o problema não é o modelo de IA. O problema é a ausência de arquitetura ao redor dele. Sem contratos de confiabilidade, sem trilha de decisão, sem governança — qualquer modelo vai errar de forma invisível.
            </p>
            <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--page-text)', lineHeight: 1.75, margin: 0 }}>
              A Aurora é a resposta para esse problema. Não uma consultoria, não um SaaS genérico — um ecossistema construído componente por componente, com cada camada servindo ao princípio de que sistemas críticos exigem infraestrutura séria.
            </p>
          </div>
        </div>

        {/* Convicções — o que ele de fato acredita */}
        <div>
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'rgba(255,255,255,0.25)', letterSpacing: '0.3em', textTransform: 'uppercase', marginBottom: '1.5rem' }}>
            Convicções operacionais
          </div>

          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {convictions.map((c, i) => (
              <div
                key={i}
                style={{
                  padding: '1.5rem 0',
                  borderTop: '1px solid var(--page-text)',
                  opacity: 0.1, /* Border opacity */
                  display: 'flex',
                  gap: '1.25rem',
                  alignItems: 'flex-start',
                }}
              >
                <div style={{ display: 'flex', gap: '1.25rem', alignItems: 'flex-start', opacity: 1 /* Reset for kids */ }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'var(--page-text-soft)', opacity: 0.4, letterSpacing: '0.1em', flexShrink: 0, marginTop: '0.15rem' }}>
                    {String(i + 1).padStart(2, '0')}
                  </span>
                  <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.88rem', color: 'var(--page-text-soft)', opacity: 0.8, lineHeight: 1.65, margin: 0 }}>
                    {c}
                  </p>
                </div>
              </div>
            ))}
            <div style={{ borderTop: '1px solid var(--page-text)', opacity: 0.08 }} />
          </div>

          <div
            style={{
              marginTop: '2rem',
              padding: '1.5rem',
              border: '1px solid var(--page-text)',
              opacity: 0.1, /* Container opacity */
              background: 'rgba(0,0,0,0.02)',
            }}
          >
            <div style={{ opacity: 1 /* Content reset */ }}>
              <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'var(--page-text-soft)', opacity: 0.5, letterSpacing: '0.25em', textTransform: 'uppercase', marginBottom: '0.75rem' }}>
                Aurora Factory // MadLab Research Group
              </div>
              <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.78rem', color: 'var(--page-text-soft)', opacity: 0.7, lineHeight: 1.65, margin: 0 }}>
                Ecossistema independente. Sem investidor externo.
                <br />
                Sem agenda que não seja a do produto.
                <br />
                Construído em Curitiba, Brasil. Desde 2024.
              </p>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @media (min-width: 1100px) {
          .builder-grid { grid-template-columns: 1.1fr 0.9fr !important; }
        }
      `}</style>
    </section>
  );
}
