# Anatomy: Layered Text Effect
**Asset ID:** typography-layered-text-001
**Origem:** external
**Fonte:** Código fornecido via 21st.dev
**Autor:** External (Curated by Aurora)
**Ingerido em:** 2026-04-18
**Ingerido por:** agent-asset-ingestor v1.0.0
**OS de referência:** OS-CLAUDECODE-AURORA-VISUAL-ASSETS-20260418-004

---

## O que este ativo faz
Cria um efeito de empilhamento isométrico de texto usando distorções de CSS (`skew`, `scaleY`) e animação de troca de camadas via GSAP. No hover, as linhas de texto "sobem", revelando a camada inferior (`bottom`) e criando uma sensação de profundidade mecânica e brutalista.

## Arquitetura de Componentes
- **LayeredText (index.tsx)**: Componente principal que gerencia o estado da animação através de uma `gsap.timeline`. Utiliza `calculateTranslateX` para criar o desalinhamento geométrico que gera a ilusão 3D.

## Fluxo de Dados
1. O componente recebe um array de `lines` com propriedades `top` e `bottom`.
2. O `useEffect` inicializa a timeline do GSAP, direcionando os parágrafos internos de cada item da lista.
3. Eventos de mouse (`mouseenter`/`mouseleave`) disparam o `play()` e `reverse()` da timeline.

## Técnicas Utilizadas
| Técnica | Implementação | Padrão Aurora |
|---|---|---|
| Sheared Isometric Stacking | Uso alternado de `skew(60deg, -30deg)` e `skew(0deg, -30deg)` | P037 (New) |
| Vertical Layer Swap | GSAP `timeline.to` com `stagger` e deslocamento no eixo Y | P038 (New) |
| Geometric Offset Mapping | Cálculo de `translateX` baseado na distância do centro | P039 (New) |

## Dependências e Requisitos
- React 18+
- GSAP 3.x

## Variáveis de Customização
| Variável | Localização | Valor padrão | Efeito |
|---|---|---|---|
| `lines` | Props | Strings de "INFINITE" a "ACHIEVEMENT" | O conteúdo textual do stack |
| `fontSize` | Props | `72px` | Tamanho da fonte em desktops |
| `lineHeight` | Props | `60` | Altura de cada "fatia" do stack |

## Adaptação para DNA Aurora

### Como adaptar para Dark Editorial:
- **Cor de Destaque**: Adicionar um `hover:text-aurora-accent` sutil nos parágrafos para guiar o olhar.
- **Tipografia**: O componente pede uma fonte heavy (Inter Black ou similar) para manter a integridade da distorção isométrica.
- **Micro-interação**: O `stagger` de 0.08s cria um efeito de "cascata" que reforça o peso editorial.

### Conflitos com stack Aurora a resolver:
- **GSAP Instance**: Garantir que a timeline seja morta no unmount para evitar memory leaks em navegações de página (SPA).

## Limitações Conhecidas
- O efeito de distorção (`skew`) pode dificultar a leitura de textos muito longos.
- O layout é dependente de `window.innerWidth` para determinar o deslocamento Y na inicialização, o que pode exigir um re-render se o resize for drástico (o componente atual mata a timeline no unmount, mas não observa resize via timeline dinâmica).

---

## VEREDITO CEO-EFFECTS
FILTRO DE TRANSPLANTE (CEO-Effects)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ativo:                 Layered Text Effect

PERGUNTA 1 — Intenção
  Este efeito pode ser descrito em uma frase
  sem mencionar a técnica?               [Sim]
  Descrição: "Um empilhamento físico de palavras que deslizam ao toque."

PERGUNTA 2 — Narrativa
  Se removido, o visitante perde algo
   além do visual?                       [Sim]

PERGUNTA 3 — Física
  O movimento tem gravidade real?        [Brutalista/Mecânico]

PERGUNTA 4 — Silêncio
  O que não se move está trabalhando?    [Sim]

PERGUNTA 5 — Permanência
  Em 2 anos: datado ou inevitável?       [Inevitável]

PERGUNTA 6 — Performance
  60fps sem GPU dedicada (Intel Iris Xe)?[Sim]

VEREDITO CEO-EFFECTS:
  [X] APROVADO — alinha com Dark Editorial Brutalist
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

---

## VEREDITO CEO-DESIGN
FILTRO DE STRESS ESTRUTURAL (CEO-Design)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ativo:                 Layered Text Effect
DNA do Projeto:        Dark Editorial

TESTE 1 — Colapso Utilitário (16px P&B)
  A forma/silhueta sobrevive?            [Sim]

TESTE 2 — Silêncio Tipográfico
  Tipografia compete com o efeito?       [É a alma do efeito]

TESTE 3 — Gancho de Casaco
  É suporte estrutural ou decoração?     [Suporte]

TESTE 4 — Auditoria Geométrica Booleana
  Formas derivam de primitivas exatas?   [Sim - Isometria]

TESTE 5 — Holding Space
  O símbolo mantém autoridade isolado?   [Sim]

TESTE 6 — DNA Compartilhado
  Consistência stroke weight + tipografia?[Sim]

TESTE 7 — Alinhamento ao DNA do Projeto
  Reforça Dark Editorial sem desvio?     [Sim]

VEREDITO CEO-DESIGN:
  [X] RESISTENTE — passa todos os filtros relevantes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
