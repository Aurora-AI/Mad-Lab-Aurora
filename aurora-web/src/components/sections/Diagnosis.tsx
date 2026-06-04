const pains = [
  {
    num: '01',
    title: 'Automações que falham em produção',
    scenario:
      'Você implementou um agente de triagem de leads. Na semana 3, ele reclassificou 240 contratos ativos como leads frios e os inseriu em uma campanha de reativação. Nenhum log. Nenhum rollback. A equipe descobriu quando os clientes começaram a ligar.',
    causa: 'Ausência de contrato de confiabilidade entre o agente e o processo de negócio.',
  },
  {
    num: '02',
    title: 'Decisões de IA sem trilha',
    scenario:
      'O sistema aprovou automaticamente uma proposta de R$ 180.000. O cliente pediu justificativa. O gestor perguntou ao desenvolvedor. O desenvolvedor pediu ao modelo. O modelo não sabia. O output existia. O raciocínio, não.',
    causa: 'Ausência de auditabilidade estruturada — o modelo decide, mas não documenta.',
  },
  {
    num: '03',
    title: 'Velocidade que vira dívida',
    scenario:
      'Em 6 meses: 3 agentes construídos, 2 integrações feitas, 1 dashboard ao vivo. Em 12 meses: nenhum dos três em produção real, dois reescritos do zero, um abandonado. A aceleração sem método se transforma em retrabalho permanente.',
    causa: 'Ausência de arquitetura de governança — cada entrega é uma aposta isolada.',
  },
];

export default function Diagnosis() {
  return (
    <section
      id="diagnosis"
      style={{
        padding: 'var(--section-py) var(--px)',
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
      }}
    >
      {/* Capítulo */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1.5rem',
          marginBottom: 'clamp(3rem, 6vw, 5rem)',
        }}
      >
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.35em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Capítulo 02
        </span>
        <div style={{ flex: 1, height: '1px', background: 'var(--page-text)', opacity: 0.05 }} />
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.25em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Os sintomas
        </span>
      </div>

      <h2
        style={{
          fontFamily: 'var(--font-display)',
          fontStyle: 'italic',
          fontSize: 'clamp(2.5rem, 5vw, 6rem)',
          fontWeight: 500,
          lineHeight: 0.95,
          letterSpacing: '-0.02em',
          color: 'var(--page-text)',
          marginBottom: 'clamp(3rem, 6vw, 6rem)',
          maxWidth: '20ch',
        }}
      >
        Três cenários.<br />
        <span style={{ color: 'var(--page-text-soft)', opacity: 0.4 }}>Uma causa.</span>
      </h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0' }}>
        {pains.map((p, i) => (
          <div
            key={p.num}
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr',
              borderTop: `1px solid var(--page-text)`,
              opacity: i === 0 ? 0.2 : 0.08,
              padding: 'clamp(2rem, 4vw, 3.5rem) 0',
            }}
            className="diagnosis-row"
          >
            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1.5rem', opacity: 1 /* Reset opacity for children */ }} className="diagnosis-inner">
              {/* Header da linha */}
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '1.5rem' }}>
                <span
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.6rem',
                    color: 'var(--page-text-soft)',
                    opacity: 0.4,
                    letterSpacing: '0.2em',
                    flexShrink: 0,
                  }}
                >
                  {p.num}
                </span>
                <h3
                  style={{
                    fontFamily: 'var(--font-body)',
                    fontWeight: 700,
                    fontSize: 'clamp(1.2rem, 2.5vw, 2rem)',
                    textTransform: 'uppercase',
                    letterSpacing: '0.03em',
                    color: 'var(--page-text)',
                    margin: 0,
                  }}
                >
                  {p.title}
                </h3>
              </div>

              {/* Conteúdo em duas colunas */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem' }} className="diagnosis-cols">
                {/* Cenário real */}
                <p
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.88rem',
                    color: 'var(--page-text-soft)',
                    opacity: 0.7,
                    lineHeight: 1.8,
                    margin: 0,
                    paddingLeft: 'calc(0.6rem + 1.5rem + 1rem)',
                  }}
                >
                  {p.scenario}
                </p>

                {/* Causa raiz */}
                <div
                  style={{
                    borderLeft: `2px solid var(--color-elysian-signal)`,
                    paddingLeft: '1.25rem',
                    alignSelf: 'start',
                  }}
                >
                  <span
                    style={{
                      display: 'block',
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.55rem',
                      letterSpacing: '0.3em',
                      color: 'var(--color-elysian-signal)',
                      textTransform: 'uppercase',
                      marginBottom: '0.5rem',
                    }}
                  >
                    Causa raiz
                  </span>
                  <p
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.82rem',
                      color: 'var(--page-text)',
                      lineHeight: 1.6,
                      margin: 0,
                    }}
                  >
                    {p.causa}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
        <div style={{ borderTop: '1px solid var(--page-text)', opacity: 0.08 }} />
      </div>

      <style>{`
        @media (min-width: 900px) {
          .diagnosis-cols {
            grid-template-columns: 1.6fr 1fr !important;
          }
        }
      `}</style>
    </section>
  );
}
