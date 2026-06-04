export default function LivingDocument() {
  return (
    <section
      id="living-document"
      style={{
        padding: 'var(--section-py) var(--px)',
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
      }}
    >
      {/* Capítulo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: 'clamp(3rem, 6vw, 5rem)' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.35em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Capítulo 05
        </span>
        <div style={{ flex: 1, height: '1px', background: 'var(--page-text)', opacity: 0.05 }} />
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.25em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          A âncora
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 'clamp(3rem, 6vw, 6rem)', alignItems: 'start' }} className="ld-grid">

        {/* Texto */}
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
            Não é output.
            <br />
            <span style={{ color: 'var(--page-text-soft)', opacity: 0.4 }}>É evidência.</span>
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', maxWidth: '52ch' }}>
            <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--page-text-soft)', opacity: 0.7, lineHeight: 1.75, margin: 0 }}>
              Todo sistema de IA produz outputs. A maioria deles desaparece: sem contexto, sem versão, sem rastreabilidade. Quando algo dá errado, o output sumiu — e com ele, qualquer possibilidade de entender o que aconteceu.
            </p>
            <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--page-text-soft)', opacity: 0.7, lineHeight: 1.75, margin: 0 }}>
              Living Document é a resposta da Aurora para esse problema: um estado persistente de verdade auditável. Cada análise, cada decisão, cada versão de um documento produzido pelos sistemas Aurora é selada criptograficamente e armazenada com trilha forense completa.
            </p>
            <p style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--page-text)', opacity: 1, lineHeight: 1.75, margin: 0 }}>
              Não é um arquivo que se salva. É um ativo de confiança que prova o que aconteceu, quando aconteceu, e com que nível de certeza o sistema operou.
            </p>
          </div>

          {/* Propriedades do protocolo */}
          <div style={{ marginTop: 'clamp(2rem, 4vw, 3.5rem)', display: 'flex', flexDirection: 'column', gap: '0' }}>
            {[
              { prop: 'Identidade', val: 'Hash SHA-256 gerado no momento da criação' },
              { prop: 'Versionamento', val: 'Cada alteração cria uma nova versão imutável' },
              { prop: 'Cadeia de custódia', val: 'Trilha forense completa de todos os agentes envolvidos' },
              { prop: 'Verificação', val: 'Trustware seal em todo output antes de persistir' },
            ].map((item) => (
              <div
                key={item.prop}
                style={{
                  display: 'grid',
                  gridTemplateColumns: '140px 1fr',
                  gap: '1.5rem',
                  padding: '1rem 0',
                  borderTop: '1px solid var(--page-text)',
                  opacity: 0.1, /* Opacity on the border container */
                  alignItems: 'baseline',
                }}
              >
                <div style={{ display: 'contents', opacity: 1 /* Reset for kids */ }}>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.65rem', color: 'var(--color-elysian-signal)', letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                    {item.prop}
                  </span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.82rem', color: 'var(--page-text-soft)', opacity: 0.8, lineHeight: 1.5 }}>
                    {item.val}
                  </span>
                </div>
              </div>
            ))}
            <div style={{ borderTop: '1px solid var(--page-text)', opacity: 0.08 }} />
          </div>
        </div>

        {/* Painel visual — comparação antes/depois */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>

          {/* Sem Living Document */}
          <div style={{ border: '1px solid var(--page-text)', opacity: 0.2, padding: '1.5rem' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'var(--page-text-soft)', opacity: 0.5, letterSpacing: '0.25em', marginBottom: '1rem' }}>
              SEM LIVING DOCUMENT
            </div>
            {['output_final_v3.docx', 'análise_revisada.pdf', 'contrato_aprovado_final2.docx'].map(f => (
              <div key={f} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.5rem 0', borderTop: '1px solid var(--page-text)', opacity: 0.3 }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.7rem' }}>—</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem' }}>{f}</span>
              </div>
            ))}
            <div style={{ marginTop: '1rem', fontFamily: 'var(--font-mono)', fontSize: '0.62rem', color: 'var(--page-text-soft)', opacity: 0.4, lineHeight: 1.5 }}>
              Sem versão. Sem autor. Sem contexto.<br />Sem como provar o que aconteceu.
            </div>
          </div>

          {/* Com Living Document */}
          <div style={{ border: '1px solid var(--page-text)', opacity: 0.6, padding: '1.5rem' }}>
            <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'var(--color-elysian-signal)', letterSpacing: '0.25em', marginBottom: '1rem' }}>
              COM LIVING DOCUMENT
            </div>
            {[
              { id: 'LD_2026_0312_001', label: 'Análise Contrato Civil', status: 'SEALED' },
              { id: 'LD_2026_0312_002', label: 'Revisão Cláusula 7.3', status: 'SEALED' },
              { id: 'LD_2026_0312_003', label: 'Output Final Aprovado', status: 'ACTIVE' },
            ].map(doc => (
              <div key={doc.id} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.65rem 0', borderTop: '1px solid var(--page-text)', opacity: 0.4 }}>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', flexShrink: 0 }}>{doc.id}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.72rem', color: 'var(--page-text)', flex: 1 }}>{doc.label}</span>
                <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: doc.status === 'ACTIVE' ? 'var(--color-elysian-signal)' : 'var(--page-text-soft)', letterSpacing: '0.1em' }}>
                  {doc.status}
                </span>
              </div>
            ))}
            <div style={{ marginTop: '1rem', fontFamily: 'var(--font-mono)', fontSize: '0.62rem', color: 'var(--page-text-soft)', opacity: 0.6, lineHeight: 1.5 }}>
              Identidade criptográfica. Cadeia de custódia.<br />Prova de o que aconteceu e quando.
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @media (min-width: 1100px) {
          .ld-grid { grid-template-columns: 1.2fr 0.8fr !important; }
        }
      `}</style>
    </section>
  );
}
