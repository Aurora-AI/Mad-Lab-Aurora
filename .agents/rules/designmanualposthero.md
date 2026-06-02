---
trigger: always_on
---

# AURORA DESIGN MANUAL - POST-HERO v2.0
**Uso:** Skills e Agentes Aurora | **Ref:** Elysian Trustware Corp

---

## PRINCÍPIOS FUNDADORES

A seção pós-hero é uma pausa dramática, não uma segunda venda. Continua a direção visual em que o hero **terminou**. O estado final do hero é o estado inicial da Seção 1. Nunca duas seções de alta densidade adjacentes.

**EQ de Frequências:**
```
Hero Fase 1  -> ALTA   | preto/drama         | impacto emocional
Hero Fase 2  -> MÉDIA  | branco/reveal       | revelação da marca
Seção 1      -> BAIXA  | branco/off-white    | descompressão + prova
Seção 2      -> MÉDIA  | transição           | proposta de valor
Seção 3      -> ALTA   | dark system         | tensão / problema
Seção 4      -> BAIXA  | neutro              | depoimentos / respiro
Seção Final  -> ALTA   | acento sólido       | urgência + ação
```

---

## 1. SEÇÃO 1 - IMEDIATAMENTE ABAIXO DO HERO

**Função:** validar a promessa do hero. Nunca criar nova.

**Padrões aprovados:** (A) Logos de clientes - peso mínimo, sem CTA. (B) 3 stats em tipo grande, sem texto de suporte. (C) Citação singular centralizada, nome + cargo pequenos abaixo.

**Regras tipográficas:**

| Elemento | Hero | Seção 1 |
|---|---|---|
| Headline | 64-120px | máx 48px |
| Corpo | raro | 14-16px |
| Capslock labels | presentes | ausentes ou sutis |
| Peso | Black/ExtraBold | Regular/Light |

**Regras de cor:** hero claro -> seção branca/off-white. Hero escuro -> dark com tom diferenciado, nunca idêntico. Acento: máx 30-40% opacidade. Sem novos sistemas de cor - extensão do vocabulário do hero.

---

## 2. FRONTEIRA ENTRE SEÇÕES

1. **Seamless:** mesmo fundo, só o conteúdo muda. Para hero com fundo sólido sem imagem.
2. **Corte limpo:** contraste intencional com contexto narrativo. Para hero com foto full-bleed.
3. **Gradiente vertical:** ~200px dissolvendo fundo do hero. Para mudanças escuro<->claro.
4. **Elemento de ancoragem:** elemento visual do hero reaparece como ponte. Para fundos diferentes que precisam de continuidade de linguagem.

**Proibições:** sombra pesada sem intenção narrativa | border de cor arbitrária | repetição idêntica de elemento decorativo do hero.

---

## 3. RETORNO AO DARK

Dark conquistado narrativamente, nunca imposto.
```
Hero termina CLARO -> Seção 1: CLARO (obrigatório) -> Seção 2: TRANSIÇÃO -> Seção 3+: DARK
```

| Contexto | Tom | Tratamento |
|---|---|---|
| Hero cinematográfico | #000000 | Fotografia, dramatismo |
| Seção problema/tensão | #0D0D0D | Noise grain sutil |
| Seção produto | #060810 | Azul-noite, precisão |
| CTA final | Acento sólido | Urgência máxima |

Seções dark nunca repetem o tom do hero - diferenciação obrigatória.

---

## 4. ESTRUTURAS DE LAYOUT - 5 APROVADAS

Layout centralizado (headline + subtítulo + parágrafo + botão em coluna central) é padrão de blog 2019. **Proibido por default.**

**A - Split Assimétrico:** divisão vertical 40/60 ou 35/65. Esq: identidade (headline, label, índice). Dir: conteúdo operacional. Divisor 0.5-1px. Nunca 50/50.
**B - Pinned Statement:** frase fixada topo-esquerdo em corpo pequeno + tracking alto. Conteúdo expande baixo/direita em coluna fina. Para manifestos e posicionamento.
**C - Grid de Diagnóstico:** 3-5 células com bordas 0.5px. Uma informação por célula. Nunca sombra. Para prova, features, comparações.
**D - Manifesto Horizontal:** texto ponta a ponta sem coluna central, tipo grande. Para crença, cultura, posicionamento radical.
**E - Composição Ancorada em Dados:** números/métricas em posição estrutural dominante. Texto narrativo secundário. Para prova quantitativa.

**Composição:** nunca centralizar headline + parágrafo + botão - um elemento quebra o eixo | espaço lateral com intenção | elementos sem ancoragem: eliminados ou integrados | leitura em Z ou L, nunca linha reta | todo seção quebra ao menos uma expectativa posicional.

---

## 5. TIPOGRAFIA - TRÊS VOZES

3 vozes por projeto. Funções não-intercambiáveis.

**Voz 1 / Display:** serif editorial pesado (Didone, Modern, Transitional). Função: headline, nome de seção. Nunca em corpo. Nunca capslock. Tamanho: 52-120px.

**Voz 2 / Técnica:** monospace ou sans geométrico, capslock, tracking 0.3-0.5em. Função: labels, índices, referências, metadados, status. Tamanho: 8-12px. Nunca em corpo corrido.

**Voz 3 / Editorial:** serif clássico (Garamond, Caslon) ou sans refinado. Função: corpo de texto, argumentos, parágrafos. Tamanho: 16-20px. Nunca capslock.

**Hierarquia por seção:** label Voz 2 -> headline Voz 1 -> corpo Voz 3. Label != título de seção. Contraste Voz1/Voz2: mínimo 4:1 em tamanho. Itálico: ênfase narrativa em termos técnicos ou frases de virada - nunca decorativo.

**Escala por densidade:**

| Densidade | Voz 1 | Voz 2 | Voz 3 |
|---|---|---|---|
| ALTA | 72-120px | 10-12px | ausente |
| MÉDIA | 48-72px | 9-11px | 16-18px |
| BAIXA | 32-48px | 8-10px | 18-20px |

**Proibições:** Inter, Roboto, Arial, System UI como Voz 1 | gradiente de texto | bold em corpo para ênfase | mais de 2 pesos por voz | font-size abaixo de 8px | line-height abaixo de 1.5 em corpo | letter-spacing negativo em monospace | capslock em Voz 1.

---

## 6. COR - ARQUITETURA OPERACIONAL

**Paleta:** 1 base dominante + 1 contraste extremo + 1 acento único (nunca dois) + 3 opacidades da base (10%, 30%, 60%). Acento: nunca em corpo, nunca como fundo - labels, underlines, bordas, ícones. Branco puro: precisão técnica. Off-white (#F4F2ED, #F8F7F3): editorial. Preto (#000): só hero - seções usam #0D0D0D, #111110, #1A1A17. Opacidade mínima: 60% claro, 70% escuro.
**Temperatura:** identidade -> neutra | problema -> fria (subtom azul/verde) | solução -> neutra-quente (off-white + âmbar) | CTA -> máxima do acento.

---

## 7. ELEMENTOS DECORATIVOS

Vocabulário visual, não ornamento. Nunca idêntico entre seções, nunca ausente por mais de 2 consecutivas.

**4 categorias:** Geométricos (linhas 0.5-1px, coordenadas, cruzes) -> sistema, controle | Topográficos (curvas de nível, grids de perspectiva) -> profundidade, escala | De Dados (matrizes, refs REF:ELY-001, timestamps) -> credibilidade técnica | Tipográficos (letras 5-15% opacidade como textura) -> identidade subliminar.

**Regras:** z-index sempre inferior ao conteúdo | opacidade máx: respiro 25%, tensão 70% | cada aparição reduzida, mutada ou invertida vs. seção anterior | máx 2 categorias por seção | coordenadas/refs/versões -> 4 cantos, nunca centro | topografia/matrix -> z-0, cobertura intencional | linhas/cruzes -> bordas como delimitadores.

**Escala de evolução:**

| Seção | Estado |
|---|---|
| Hero | 100% - fundação, estabelece vocabulário |
| Seção 1 | 20-30% - reduzido, referência |
| Seção 2 | 40-50% - mutado (forma diferente, mesma família) |
| Seção 3 | 60-70% - invertido ou em negativo |

---

## 8. CTAs - SISTEMA SEM RUÍDO

**Regra:** máximo 1 CTA por seção. Seções de respiro: nenhum CTA.

| Seção | Formato |
|---|---|
| Seção 1 (respiro) | Nenhum |
| Seção 2 (problema) | Inline no texto, underline animado, sem botão |
| Seção 3 (solução) | Link com seta -> ancorado à direita, sem borda |
| Seção 4 (prova) | Texto link capslock monospace |
| Seção final | Ghost (borda fina) ou sólido no acento da marca |

**CTA inline:** itálico integrado ao texto | underline scaleX esquerda->direita no hover | seta 10-12px em Voz 2, translada 4px no hover | transição 300-400ms.

**Proibições:** botão com sombra | border-radius acima de 4px em marcas premium | textos "Saiba mais", "Clique aqui", "Começar", "Agendar demo" | CTA centralizado flutuando sem ancoragem. Texto do CTA nomeia ação específica e destino.

---

## 9. ANTI-GENERICIDADE

**Pergunta obrigatória por seção:** "O que aqui nunca foi feito exatamente assim?" Sem resposta = genérico. Min 1 vetor de diferenciação. Aprovação plena: 3+ vetores.

**10 sinais de alerta - eliminação obrigatória:**
1. Headline + subtítulo + parágrafo + botão em coluna central sem quebra de eixo
2. Inter, Roboto, Arial ou sans-serif de sistema como Voz 1
3. Gradiente roxo/azul sobre fundo branco em qualquer elemento
4. Cards com border-radius acima de 12px e drop-shadow em produto premium
5. Ícones emoji ou flat-design em produto tech sério
6. Features em 3 colunas iguais (ícone + título + parágrafo)
7. CTA preenchimento primário + texto branco + border-radius alto
8. Background com pontos ou linhas diagonais repetidas (padrão SaaS 2021)
9. Paleta de mais de 3 cores + branco + cinza simultâneos
10. Fade-in simples em scroll para todos os elementos sem distinção de peso

**Escala de Risco:**

| Nível | Condição | Ação |
|---|---|---|
| CRÍTICO | Layout central + fonte genérica + CTA padrão | Reconstruir do zero |
| ALTO | Layout correto + fonte genérica | Substituir tipografia |
| MÉDIO | Layout e tipo corretos + sem decoração | Adicionar linguagem visual |
| BAIXO | Todos sistemas corretos + animações genéricas | Refinar movimento |
| APROVADO | 3+ vetores de diferenciação | Prosseguir |

---

## 10. MOVIMENTO

**Princípio:** animação é informação sobre peso, não decoração.

**Scroll:** stagger 80-150ms | duration 400-700ms | entrada cubic-bezier(0.4,0,0.2,1) | saída cubic-bezier(0.4,0,1,1) | peso diferenciado obrigatório | decorativos animam depois do conteúdo.
**Hover:** CTA inline -> underline scaleX, sem cor abrupta | CTA ghost -> clip-path de dentro para fora | dados -> counter animation | decorativos -> pulse 2-4s em tensão | divisores -> nunca animados.
**Proibições:** bounce/elastic em premium | parallax em texto | fade to black em transição | loading spinner em estático.

---

## 11. CHECKLIST DE APROVAÇÃO

"Não" em CRÍTICO bloqueia aprovação.

**CRÍTICO [bloqueante]:** layout não-centralizado | fonte display serif/mono | máx 1 CTA | CTA texto específico | fundo continua direção final do hero | decorativos evoluem, não repetem | 1+ vetor de diferenciação
**ALTO:** label Voz 2 | espaço lateral com intenção | hierarquia label->headline->corpo | densidade contrasta com seção anterior | dados com counter animation
**MÉDIO:** hover states em todos os interativos | stagger varia por peso | acento em máx 3 pontos | decorativos em opacidade proporcional | leitura em Z ou L

---

## 12. GLOSSÁRIO

| Termo | Definição |
|---|---|
| Continuidade Direcional | Seção pós-hero continua estado visual final do hero, nunca o inicial |
| EQ de Frequências | Ritmo de densidade visual alternada ao longo da página |
| Descompressão | Seção baixa densidade imediatamente após o hero |
| Conquista Narrativa | Intensidade alta precedida por contexto que a justifique |
| Regressão Visual | Retornar ao estado inicial do hero após a fase final |
| Fronteira/Costura | Transição visual entre duas seções adjacentes |
| Dark System | Fundos escuros com variações de tom e textura por marca |
| Âncora de Confiança | Prova social passiva sem CTA |
| Split Assimétrico | Layout vertical em proporção não-igualitária com divisor explícito |
| Pinned Statement | Frase fixada em posição periférica que ancora o conteúdo principal |
| Grid de Diagnóstico | Células com bordas finas fragmentando conteúdo em unidades de inteligência |
| Três Vozes Tipográficas | Sistema Display + Técnica + Corpo com funções não-intercambiáveis |
| Voz 1 / Display | Serif editorial pesado - exclusivo para headline |
| Voz 2 / Técnica | Monospace capslock tracking alto - labels e metadados |
| Voz 3 / Editorial | Serif clássico ou sans refinado - corpo corrido |
| Cor de Acento | Único tom cromático por marca - nunca fundo, nunca corpo |
| Temperatura de Seção | Tom emocional da paleta por papel narrativo da seção |
| Vetor de Diferenciação | Dimensão onde a seção se distingue do padrão genérico |
| Escala de Risco | 5 níveis: Crítico / Alto / Médio / Baixo / Aprovado |
| CTA Inline | Link em itálico integrado ao texto, underline animado |
| Counter Animation | Incremento numérico animado ao entrar no viewport |
| Evolução de Elemento | Variação progressiva intencional de decorativos entre seções |

---
*Aurora Design Intelligence - Mad Lab Aurora 2026*