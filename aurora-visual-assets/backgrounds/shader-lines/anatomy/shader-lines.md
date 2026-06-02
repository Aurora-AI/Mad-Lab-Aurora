# Anatomy: Shader Lines
**Asset ID:** backgrounds-shader-lines-001
**Origem:** external
**Fonte:** Código fornecido diretamente
**Autor:** External (Curated by Aurora)
**Ingerido em:** 2026-04-18
**Ingerido por:** agent-asset-ingestor v1.0.0
**OS de referência:** OS-CLAUDECODE-AURORA-VISUAL-ASSETS-20260418-003

---

## O que este ativo faz
Este ativo gera um background procedural de linhas digitais em movimento que cruzam a tela em um fluxo temporal. O efeito utiliza um "Mosaic Distortion" para criar um aspecto pixelado/editorial e uma série de loops harmônicos no fragment shader para gerar cores vibrantes e profundidade visual.

## Arquitetura de Componentes
- **ShaderAnimation (index.tsx)**: Componente principal que gerencia o ciclo de vida do Three.js, o carregamento dinâmico do script externo e a renderização do Full-Screen Quad.

## Fluxo de Dados
1. `useEffect` injeta a biblioteca Three.js r89.
2. `initThreeJS` configura a cena WebGL e os materiais de shader.
3. `requestAnimationFrame` atualiza o uniform `time`.
4. O fragment shader recalcula a cor de cada pixel baseado no `time` e na posição `uv` mosaico.

## Técnicas Utilizadas
| Técnica | Implementação | Padrão Aurora |
|---|---|---|
| Dynamic Script Loading | Injeção de script via DOM em `useEffect` | P033 (New) |
| Mosaic Distortion | `floor` em coordenadas UV escaladas | P034 (New) |
| Harmonic Loops | Loop for aninhado no shader para cor | P029 (Referenced) |

## Dependências e Requisitos
- React 18+
- Three.js (r89 carregado via CDN para evitar conflitos de versão local)

## Variáveis de Customização
| Variável | Localização | Valor padrão | Efeito |
|---|---|---|---|
| `fMosaicScal` | Fragment Shader | `vec2(4.0, 2.0)` | Intensidade da pixelização horizontal/vertical |
| `lineWidth` | Fragment Shader | `0.0008` | Espessura das linhas procedurais |
| `t` (time scale) | Fragment Shader | `time * 0.06` | Velocidade do fluxo das linhas |

## Adaptação para DNA Aurora

### Como adaptar para Dark Editorial:
- **Contraste**: O background já opera em preto puro, ideal para o DNA Aurora.
- **Micro-animação**: A velocidade pode ser reduzida (`t`) para uma presença mais sutil e editorial.
- **Tipografia**: Usar sobreposto a tipos `tracking-tighter` para criar profundidade.

### Conflitos com stack Aurora a resolver:
- O uso de r89 via CDN é uma solução temporária de portabilidade. Futuras versões nativas devem migrar para r128 local para consistência de governança.

## Limitações Conhecidas
- Dependência de rede para carregar o Three.js no primeiro mount.
- Performance em browsers legacy pode variar devido ao uso de `PlaneBufferGeometry`.

---

## VEREDITO CEO-EFFECTS
FILTRO DE TRANSPLANTE (CEO-Effects)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ativo:                 Shader Lines

PERGUNTA 1 — Intenção
  Este efeito pode ser descrito em uma frase
  sem mencionar a técnica?               [Sim]
  Descrição: "Um fluxo digital de energia pixelada."

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
Ativo:                 Shader Lines
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
Integrar os parâmetros de mosaico ao sistema de tokens da Aurora, permitindo que a granulação do efeito responda ao viewport ou à densidade da página via props.
