const components = [
  {
    name: 'Ozzmosis',
    what: 'Base tecnológica compartilhada',
    how: 'Um monorepo de bibliotecas, contratos de tipo e runtimes que todos os produtos Aurora consomem. Quando um contrato é atualizado aqui, todos os produtos herdam — sem divergência de versão, sem integração manual.',
  },
  {
    name: 'Aurora Conductor',
    what: 'Orquestrador de fluxos de IA',
    how: 'Traduz intenção de negócio em planos de execução auditáveis. Cada decisão que o Conductor toma é registrada com contexto, input, output e o agente responsável — rastreável do início ao fim.',
  },
  {
    name: 'Trustware',
    what: 'Contrato de confiança entre IA e decisão humana',
    how: 'Define o threshold de confiança necessário para cada tipo de ação. Abaixo do threshold, escala para humano. Acima, executa com log. Nenhum output de IA alcança um processo crítico sem passar por esse gate.',
  },
  {
    name: 'Alvaro Core',
    what: 'Núcleo de raciocínio determinista',
    how: 'Camada de raciocínio estruturado que força o modelo a seguir um roteiro lógico antes de produzir output. Reduz alucinações em fluxos jurídicos e comerciais onde a cadeia de raciocínio precisa ser verificável.',
  },
];

export default function TheMethod() {
  return (
    <section
      id="the-method"
      style={{
        padding: 'var(--section-py) var(--px)',
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
      }}
    >
      {/* Capítulo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: 'clamp(3rem, 6vw, 5rem)' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.35em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Capítulo 04
        </span>
        <div style={{ flex: 1, height: '1px', background: 'var(--page-text)', opacity: 0.05 }} />
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.25em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          O método
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 'clamp(3rem, 6vw, 5rem)', alignItems: 'start' }} className="method-grid">

        {/* Coluna texto */}
        <div>
          <h2
            style={{
              fontFamily: 'var(--font-display)',
              fontStyle: 'italic',
              fontSize: 'clamp(2.5rem, 5vw, 6rem)',
              fontWeight: 500,
              lineHeight: 0.95,
              letterSpacing: '-0.02em',
              color: 'var(--page-text)',
              marginBottom: 'clamp(1.5rem, 3vw, 2.5rem)',
            }}
          >
            Construído sobre
            <br />
            <span style={{ color: 'var(--page-text-soft)', opacity: 0.4 }}>protocolos.</span>
          </h2>

          <p
            style={{
              fontFamily: 'var(--font-mono)',
              fontSize: '0.9rem',
              color: 'var(--page-text-soft)',
              opacity: 0.7,
              lineHeight: 1.75,
              maxWidth: '52ch',
              marginBottom: 'clamp(2.5rem, 5vw, 4rem)',
            }}
          >
            Cada componente da Aurora tem uma função específica no contrato de confiabilidade. Não são ferramentas independentes — são camadas de um sistema onde cada uma verifica a anterior.
          </p>

          {/* Componentes */}
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            {components.map((c, i) => (
              <div
                key={c.name}
                style={{
                  borderTop: '1px solid var(--page-text)',
                  opacity: 0.2, /* Opacity applied to border container */
                  padding: '1.75rem 0',
                }}
              >
                <div style={{ opacity: 1 /* Reset opacity for content */ }}>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: '1rem', marginBottom: '0.75rem' }}>
                    <h4
                      style={{
                        fontFamily: 'var(--font-mono)',
                        fontWeight: 700,
                        fontSize: '0.75rem',
                        letterSpacing: '0.15em',
                        color: 'var(--color-elysian-signal)',
                        textTransform: 'uppercase',
                        margin: 0,
                      }}
                    >
                      {c.name}
                    </h4>
                    <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--page-text-soft)', opacity: 0.4, letterSpacing: '0.1em' }}>
                      — {c.what}
                    </span>
                  </div>
                  <p
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.85rem',
                      color: 'var(--page-text)',
                      opacity: 0.8,
                      lineHeight: 1.7,
                      margin: 0,
                    }}
                  >
                    {c.how}
                  </p>
                </div>
              </div>
            ))}
            <div style={{ borderTop: '1px solid var(--page-text)', opacity: 0.08 }} />
          </div>
        </div>

        {/* Coluna diagrama — fluxo real, não retângulos empilhados */}
        <div
          style={{
            border: '1px solid rgba(255,255,255,0.1)',
            padding: '2rem',
            background: 'rgba(255,255,255,0.015)',
            alignSelf: 'start',
            position: 'sticky',
            top: '2rem',
          }}
        >
          <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'rgba(255,255,255,0.3)', marginBottom: '1.5rem', letterSpacing: '0.2em' }}>
            FLUXO DE EXECUÇÃO SEGURA
          </div>

          {[
            { step: '01', label: 'Input recebido', sub: 'Usuário ou sistema externo', color: 'var(--page-text-soft)' },
            { step: '02', label: 'Conductor planeja', sub: 'Traduz intenção → plano auditável', color: 'var(--page-text-soft)' },
            { step: '03', label: 'Trustware avalia', sub: 'Confiança ≥ threshold → executa', color: 'var(--color-elysian-signal)' },
            { step: '04', label: 'Agente executa', sub: 'Alvaro Core garante raciocínio', color: 'var(--page-text-soft)' },
            { step: '05', label: 'Output selado', sub: 'SHA-256 · trilha imutável', color: 'var(--page-text-soft)' },
          ].map((s, idx, arr) => (
            <div key={s.step} style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', flexShrink: 0 }}>
                <div
                  style={{
                    width: 28,
                    height: 28,
                    border: `1px solid ${s.color === 'var(--color-elysian-signal)' ? 'var(--color-elysian-signal)' : 'var(--page-text)'}`,
                    opacity: s.color === 'var(--color-elysian-signal)' ? 1 : 0.2,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontFamily: 'var(--font-mono)',
                    fontSize: '0.55rem',
                    color: s.color === 'var(--color-elysian-signal)' ? 'var(--color-elysian-signal)' : 'var(--page-text)',
                    letterSpacing: '0.1em',
                  }}
                >
                  {s.step}
                </div>
                {idx < arr.length - 1 && (
                  <div style={{ width: 1, height: 28, background: 'var(--page-text)', opacity: 0.1, marginTop: 2 }} />
                )}
              </div>
              <div style={{ paddingTop: '0.35rem', paddingBottom: idx < arr.length - 1 ? '0.25rem' : 0 }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', color: s.step === '03' ? 'var(--page-text)' : 'var(--page-text-soft)', fontWeight: s.step === '03' ? 700 : 400, opacity: s.step === '03' ? 1 : 0.6 }}>
                  {s.label}
                </div>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--page-text-soft)', opacity: 0.4, marginTop: '0.2rem' }}>
                  {s.sub}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <style>{`
        @media (min-width: 1100px) {
          .method-grid { grid-template-columns: 1.2fr 0.8fr !important; }
        }
      `}</style>
    </section>
  );
}
