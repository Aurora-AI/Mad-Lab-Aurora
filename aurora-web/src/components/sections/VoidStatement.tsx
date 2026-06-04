
export default function VoidStatement() {
  return (
    <section
      id="void-statement"
      style={{
        padding: 'var(--section-py) var(--px)',
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
        position: 'relative',
      }}
    >
      {/* Capítulo I */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1.5rem',
          marginBottom: 'clamp(3rem, 6vw, 5rem)',
        }}
      >
        <span
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            letterSpacing: '0.35em',
            color: 'var(--page-text-soft)',
            opacity: 0.3,
            textTransform: 'uppercase',
          }}
        >
          Capítulo 01
        </span>
        <div style={{ flex: 1, height: '1px', background: 'var(--page-text)', opacity: 0.05 }} />
        <span
          style={{
            fontFamily: 'var(--font-mono)',
            fontSize: '0.6rem',
            letterSpacing: '0.25em',
            color: 'var(--page-text-soft)',
            opacity: 0.3,
            textTransform: 'uppercase',
          }}
        >
          O diagnóstico
        </span>
      </div>

      {/* Tese principal — este é o headline, não um rodapé */}
      <h2
        style={{
          fontFamily: 'var(--font-display)',
          fontStyle: 'italic',
          fontSize: 'clamp(2.8rem, 7vw, 8rem)',
          fontWeight: 500,
          lineHeight: 0.92,
          letterSpacing: '-0.02em',
          color: 'var(--page-text)',
          maxWidth: '18ch',
          margin: '0 0 clamp(2.5rem, 5vw, 4rem) 0',
        }}
      >
        O mercado de IA
        <br />
        cresceu em promessa.
        <br />
        <span style={{ color: 'var(--page-text-soft)', opacity: 0.4 }}>
          Vazio de infraestrutura.
        </span>
      </h2>

      {/* Três parágrafos — argumento real, não decoração */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: 'clamp(2rem, 4vw, 4rem)',
          maxWidth: '1000px',
        }}
      >
        <div style={{ borderTop: '2px solid var(--page-text)', opacity: 0.1, paddingTop: '1.5rem' }}>
          <p
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.9rem',
              color: 'var(--page-text-soft)',
              lineHeight: 1.75,
              margin: 0,
            }}
          >
            R$ 8 bilhões investidos em tecnologia corporativa no Brasil em 2025.
            A maior parte foi em licenças de SaaS, pilotos de IA e consultorias
            de transformação digital.
          </p>
        </div>

        <div style={{ borderTop: '2px solid var(--page-text)', opacity: 0.1, paddingTop: '1.5rem' }}>
          <p
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.9rem',
              color: 'var(--page-text-soft)',
              lineHeight: 1.75,
              margin: 0,
            }}
          >
            Desse total, menos de 3% foi direcionado a governança, auditabilidade
            e infraestrutura de confiança para sistemas de IA em operação crítica.
          </p>
        </div>

        <div style={{ borderTop: '2px solid var(--color-elysian-signal)', paddingTop: '1.5rem' }}>
          <p
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.9rem',
              color: 'var(--page-text)',
              lineHeight: 1.75,
              margin: 0,
            }}
          >
            O resultado: empresas com IA em produção, sem contrato de
            confiabilidade, sem trilha de decisão, sem responsável quando
            o sistema erra.
          </p>
        </div>
      </div>
    </section>
  );
}
