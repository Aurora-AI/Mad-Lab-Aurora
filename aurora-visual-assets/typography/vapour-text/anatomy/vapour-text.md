# Anatomy: Vapour Text Effect
**Asset ID:** typography-vapour-text-001
**Origem:** external
**Fonte:** Código fornecido diretamente
**Autor:** External (Curated by Aurora)
**Ingerido em:** 2026-04-18
**Ingerido por:** agent-asset-ingestor v1.0.0
**OS de referência:** OS-CLAUDECODE-AURORA-VISUAL-ASSETS-20260418-003

---

## O que este ativo faz
Este componente cria um efeito cinematográfico de "vaporização" de texto. As letras se dissolvem em partículas que flutuam e se dissipam no espaço vago, seguidas pela reconstrução (fade-in) do próximo texto na sequência. É uma peça de tipografia cinética de alto impacto para cabeçalhos editoriais.

## Arquitetura de Componentes
- **VaporizeTextCycle (index.tsx)**: Orquestrador principal que gerencia o estado da animação (`static` -> `vaporizing` -> `fadingIn` -> `waiting`), o sistema de partículas e o Canvas.
- **SeoElement**: Componente utilitário que mantém o texto acessível para motores de busca enquanto a versão visual é renderizada no Canvas.

## Fluxo de Dados
1. `renderCanvas` desenha o texto invisível para amostragem.
2. `createParticles` extrai os dados de pixel do texto e gera objetos `Particle`.
3. `updateParticles` aplica física de dissipação cada frame durante a fase `vaporizing`.
4. `setCurrentTextIndex` alterna o conteúdo para o próximo ciclo de reconstrução.

## Técnicas Utilizadas
| Técnica | Implementação | Padrão Aurora |
|---|---|---|
| Canvas Pixel Sampling | Extração de `imageData.data` para mapear partículas | P035 (New) |
| Particle Physics (Vapour) | Vetores de velocidade com damping e random spread | P014 (Referenced) |
| Phase-Based Text Cycle | Máquina de estados para coordenar fumaça e reveal | P036 (New) |
| SEO Mirroring | Renderização de tag HTML oculta com `texts.join` | P021 (Referenced) |

## Dependências e Requisitos
- React 18+
- Suporte a `CanvasRenderingContext2D` e `IntersectionObserver`.

## Variáveis de Customização
| Variável | Localização | Valor padrão | Efeito |
|---|---|---|---|
| `texts` | Props | `["Next.js", "React"]` | Lista de strings para o ciclo |
| `spread` | Props | `5` | Intensidade da dispersão das partículas |
| `density` | Props | `5` | Densidade visual do vapor |
| `direction` | Props | `"left-to-right"` | Direção da onda de vaporização |

## Adaptação para DNA Aurora

### Como adaptar para Dark Editorial:
- **Tipografia Serifa**: Substituir `sans-serif` por uma fonte serifada elegante (ex: Bodoni ou uma fonte Aurora custom) para o look editorial.
- **Ritmo**: Aumentar `waitDuration` para permitir que o leitor absorva a palavra antes da dissolução.
- **Velocidade**: Reduzir `vaporizeDuration` para um efeito mais "explosivo" ou aumentar para algo mais "líquido/etéreo".

### Conflitos com stack Aurora a resolver:
- Nenhum. O componente é autocontido e usa APIs nativas do browser.

## Limitações Conhecidas
- Consumo de CPU aumenta com o tamanho da fonte (mais partículas para calcular).
- Renderização em Canvas pode ter aliasing se o `globalDpr` não for calculado corretamente em telas ultra-wide.

---

## VEREDITO CEO-EFFECTS
FILTRO DE TRANSPLANTE (CEO-Effects)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ativo:                 Vapour Text Effect

PERGUNTA 1 — Intenção
  Este efeito pode ser descrito em uma frase
  sem mencionar a técnica?               [Sim]
  Descrição: "Palavras que se dissipam como fumaça no escuro."

PERGUNTA 2 — Narrativa
  Se removido, o visitante perde algo
  além do visual?                        [Sim]

PERGUNTA 3 — Física
  O movimento tem gravidade real?        [Flutua]

PERGUNTA 4 — Silêncio
  O que não se move está trabalhando?    [Sim]

PERGUNTA 5 — Permanência
  Em 2 anos: datado ou inevitável?       [Inevitável]

PERGUNTA 6 — Performance
  60fps sem GPU dedicada (Intel Iris Xe)?[Sim]

VEREDITO CEO-EFFECTS:
  [X] APROVADO — alinha com Dark Editorial
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---

## VEREDITO CEO-DESIGN
FILTRO DE STRESS ESTRUTURAL (CEO-Design)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ativo:                 Vapour Text Effect
DNA do Projeto:        Dark Editorial

TESTE 1 — Colapso Utilitário (16px P&B)
  A forma/silhueta sobrevive?            [Sim]

TESTE 2 — Silêncio Tipográfico
  Tipografia compete com o efeito?       [Não compete]

TESTE 3 — Gancho de Casaco
  É suporte estrutural ou decoração?     [Suporte]

TESTE 4 — Auditoria Geométrica Booleana
  Formas derivam de primitivas exatas?   [Sim]

TESTE 5 — Holding Space
  O símbolo mantém autoridade isolado?   [Sim]

TESTE 6 — DNA Compartilhado
  Consistência stroke weight + tipografia?[Sim]

TESTE 7 — Alinhamento ao DNA do Projeto
  Reforça Dark Editorial sem desvio?     [Sim]

VEREDITO CEO-DESIGN:
  [X] RESISTENTE — passa todos os filtros relevantes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---

## Próxima Evolução Aurora-Native
Adicionar suporte a gradientes dinâmicos nas partículas, permitindo que a fumaça mude de cor durante a dispersão baseada na luz da página.
