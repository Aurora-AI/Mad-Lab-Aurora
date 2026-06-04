const layers = [
  {
    num: '01',
    name: 'Aurora Governance',
    role: 'O que a IA pode e não pode decidir',
    desc: 'Define os contratos de autoridade de cada agente — quais decisões ele executa autonomamente, quais escalam para humano, e quais são vetadas. Sem governança, cada automação é uma decisão sem dono.',
  },
  {
    num: '02',
    name: 'Ozzmosis',
    role: 'A fábrica de componentes compartilhados',
    desc: 'Biblioteca de contratos, tipos e runtimes reutilizados por todos os produtos Aurora. O que foi testado uma vez funciona em todos. Nenhuma duplicação, nenhuma incompatibilidade silenciosa entre sistemas.',
  },
  {
    num: '03',
    name: 'Products',
    role: 'Sistemas especializados por domínio',
    desc: 'Aurora CRM para operações comerciais com WhatsApp e outbound. Elysian Lex para inteligência jurídica com auditabilidade forense. Living Document para estado persistente e verificável de qualquer processo.',
  },
  {
    num: '04',
    name: 'MadLab',
    role: 'Tecnologia com presença institucional',
    desc: 'A camada onde os sistemas ganham identidade, narrativa e superfície pública. Onde você está agora. Cada produto Aurora tem uma presença institucional à altura da seriedade da infraestrutura que carrega.',
  },
];

export default function OurAnswer() {
  return (
    <section
      id="our-answer"
      style={{
        padding: 'var(--section-py) var(--px)',
        background: 'var(--page-bg)',
        borderTop: '1px solid rgba(var(--page-text-rgb), 0.1)',
      }}
    >
      {/* Capítulo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: 'clamp(3rem, 6vw, 5rem)' }}>
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.35em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          Capítulo 03
        </span>
        <div style={{ flex: 1, height: '1px', background: 'var(--page-text)', opacity: 0.05 }} />
        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.6rem', letterSpacing: '0.25em', color: 'var(--page-text-soft)', opacity: 0.3, textTransform: 'uppercase' }}>
          A resposta
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
          marginBottom: 'clamp(0.75rem, 2vw, 1.5rem)',
        }}
      >
        Um ecossistema.
        <br />
        <span style={{ color: 'var(--page-text-soft)', opacity: 0.4 }}>Quatro camadas.</span>
      </h2>

      <p
        style={{
          fontFamily: 'var(--font-mono)',
          fontSize: '0.9rem',
          color: 'var(--page-text-soft)',
          opacity: 0.7,
          maxWidth: '56ch',
          lineHeight: 1.75,
          marginBottom: 'clamp(3rem, 6vw, 5rem)',
        }}
      >
        Enquanto o mercado vende ferramentas isoladas, a Aurora constrói um sistema integrado onde cada camada sustenta a próxima. Não é uma pilha de SaaS — é uma arquitetura com contrato entre as partes.
      </p>

      {/* Tabela de camadas — Basement-style */}
      <div style={{ border: '1px solid var(--page-text)', opacity: 0.1 }}>
        {layers.map((layer, i) => (
          <div
            key={layer.num}
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr',
              borderBottom: i < layers.length - 1 ? '1px solid var(--page-text)' : 'none',
              transition: 'background 0.3s',
            }}
            className="layer-row"
            onMouseEnter={e => (e.currentTarget.style.background = 'rgba(0,0,0,0.03)')}
            onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
          >
            {/* Barra de header da linha */}
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '1.5rem',
                padding: '0.85rem 1.5rem',
                borderBottom: '1px solid var(--page-text)',
                background: 'rgba(0,0,0,0.015)',
              }}
            >
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.55rem', color: 'var(--page-text-soft)', opacity: 0.4, letterSpacing: '0.2em' }}>
                LAYER_{layer.num}
              </span>
              <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.75rem', fontWeight: 700, color: 'var(--page-text)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
                {layer.name}
              </span>
              <span style={{ marginLeft: 'auto', fontFamily: 'var(--font-mono)', fontSize: '0.6rem', color: 'var(--page-text-soft)', opacity: 0.4, letterSpacing: '0.1em' }}>
                {layer.role}
              </span>
            </div>

            {/* Corpo da linha */}
            <div style={{ padding: 'clamp(1.5rem, 3vw, 2.5rem) 1.5rem' }}>
              <p
                style={{
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.88rem',
                  color: 'var(--page-text-soft)',
                  opacity: 0.8,
                  lineHeight: 1.75,
                  margin: 0,
                  maxWidth: '72ch',
                }}
              >
                {layer.desc}
              </p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
