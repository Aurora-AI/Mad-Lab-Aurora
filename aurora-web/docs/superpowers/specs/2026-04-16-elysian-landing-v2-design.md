# Design Spec — Elysian Landing v2.0
**Data:** 2026-04-16
**Status:** Aprovado
**Substitui:** `2026-04-14-elysian-institutional-design.md` (v1 mantida como referência)
**Audiência primária:** Google for Startups · Anthropic Programs · Investidores
**Audiência secundária:** Mercado geral · Imprensa

---

## 0. Princípio Central

Esta landing não é um site de empresa. É a prova física de que o que a Elysian diz — determinismo, auditabilidade, transparência — existe na forma como o próprio site foi construído.

A estrutura visual não decora a mensagem. **É a mensagem.**

---

## 1. Abordagem: Reconstrução Narrativa (Approach B)

A home é construída como uma narrativa linear. O arco emocional governa a arquitetura — não o inverso. O SovereignHeroWebGL permanece como ponto de entrada.

**Estrutura de navegação:** Híbrido
- `/` — Landing completa (storytelling scroll)
- `/lex` — Elysian Lex (stub)
- `/crm` — CRM / Silent Operator (stub)
- `/living-document` — Living Document (stub)

---

## 2. Sistema de Arco Emocional — O ScrollDriver

O coração técnico. Um componente `ScrollDriver.tsx` monta um GSAP ScrollTrigger no `#elysian-root` e interpola dois tokens CSS ao longo de todo o scroll:

```
--page-bg    #000000  →  #f0ebe3   (preto piano → marfim quente)
--page-text  #ffffff  →  #111111   (branco → quase-preto)
```

**Curva:** `power2.inOut`
- 0% → 35% do scroll: variação mínima (ainda parece noite)
- 35% → 70%: aceleração suave (amanhecer imperceptível)
- 70% → 100%: desaceleração (chegou em casa)

**Inversão de contraste:** ocorre quando `--page-bg` cruza luminosidade ~40% (aprox. na seção LivingDocument). Implementada via CSS `color-scheme` — sem JavaScript adicional, sem flash.

**Exceções fixas:**
- `SovereignHeroWebGL` → sempre `#000000` (ponto de partida imutável)
- `CallToAction` → sempre `#00FFEF` (único momento de cor pura)
- `Footer` → sempre `#1a1816` (fechamento suave)

**Scrub:** `1.5` — fluidez sem lag perceptível.

---

## 3. Sistema Tipográfico — Três Vozes

As vozes participam do arco. A tipografia viaja junto com o fundo.

### Voz I — Técnica
**`JetBrains Mono`** (já no projeto)
- Labels em CAPS: `[ DIAGNÓSTICO // 2026 ]`
- Números de seção: `01`, `02`...
- Hashes do Living Document
- Stats, micro-textos de dado
- Presente: forte nas seções escuras → some gradualmente

### Voz II — Editorial
**`Satoshi`** via Fontshare CDN (gratuita, equivalente a Neue Haas Grotesk)
- Corpo de texto em todo o site
- Navegação e labels de produto
- Headlines das seções de meio arco (04–05)
- Presente: do início ao fim — espinha invisível

### Voz III — Monumental
**`Cormorant`** via Google Fonts (gratuita, serifa francesa ultra-refinada)
- Aparece pela primeira vez na seção 06 (LivingDocument)
- Headlines de máximo peso emocional
- Citação do fundador (TheBuilder)
- Headline do CTA
- Escala: `10vw` a `16vw` / `line-height: 0.88` / `letter-spacing: -0.03em`

**Regra de escala:**
Cormorant em escala extrema com silêncio ao redor supera qualquer fonte premium
usada de forma convencional. O tamanho é o argumento.

### Atualizações em `index.css`

```css
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Cormorant:ital,wght@0,300;0,400;0,600;1,300;1,400&display=swap');

@theme {
  --font-display:   "Cormorant", serif;
  --font-body:      "Satoshi", sans-serif;
  --font-mono:      "JetBrains Mono", monospace;
}
```

---

## 4. Design System — Tokens

```css
/* Cores absolutas */
--color-void:         #000000;   /* preto piano */
--color-marfim:       #f0ebe3;   /* branco quente — nunca #FFFFFF */
--color-text-light:   #ffffff;
--color-text-dark:    #111111;
--color-cyan:         #00FFEF;
--color-footer:       #1a1816;

/* Arco (computados pelo ScrollDriver) */
--page-bg:            var(--color-void);     /* interpolado */
--page-text:          var(--color-text-light); /* interpolado */

/* Tipografia */
--font-display:       "Cormorant", serif;
--font-body:          "Satoshi", sans-serif;
--font-mono:          "JetBrains Mono", monospace;

/* Espaçamento */
--px:                 8vw;        /* padding horizontal canônico */
--section-py:         clamp(80px, 10vw, 160px);

/* Motion */
--ease-monumental:    cubic-bezier(0.76, 0, 0.24, 1);
--ease-weight:        cubic-bezier(0.83, 0, 0.17, 1);
```

---

## 5. Componentes — Regras Transversais

**Botões:**
- `border-radius: 0` — sharp sempre
- Primary: `background: var(--page-text)` / `color: var(--page-bg)`
  (inverte automaticamente com o arco)
- Hover: directional fill, 400ms `ease-monumental`

**Labels `[ CAPS ]`:**
- `SectionLabel.tsx` — componente único
- `font-mono` · uppercase · `0.65rem` · `letter-spacing: 0.35em`
- Cor: herda `--page-text` com `opacity: 0.4`

**Cards de produto:**
- `border-radius: 0`
- Border: `1px solid color-mix(in srgb, var(--page-text) 12%, transparent)`
- Hover: left-border 2px cyan + background `var(--page-text) 4%`

**Dividers:**
- `1px solid color-mix(in srgb, var(--page-text) 10%, transparent)`

---

## 6. Estrutura de Blocos — 11 Seções

### 00 — HEADER (fixed)
- Height: `72px`
- Background inicial: `transparent`
- Após 50px scroll: `backdrop-blur(12px)` + `background: color-mix(in srgb, var(--page-bg) 85%, transparent)` + border-bottom `1px` sutil
- Left: `"ELYSIAN"` — Satoshi Semibold, `1rem`, `letter-spacing: -0.02em`
- Right: nav `Ecossistema · Produtos · Método` (Satoshi, `0.75rem`, uppercase) + botão `Agendar` (sharp, primary)
- O header muda de cor junto com o arco — sempre legível, nunca fixo em preto ou branco

---

### 01 — SOVEREIGN HERO (existente)
**Componente:** `SovereignHeroWebGL.tsx` — sem alterações
**Altura:** `100vh`
**Fundo:** sempre `#000000`
**Papel narrativo (CEO-Copy — Etapa 1):** A caixa preta personificada. O visitante sente antes de ler.
O scramble não é um efeito — é o diagnóstico.

---

### 02 — VOID STATEMENT (~80vh)
**Zona emocional:** Caos (scroll ~10–20%)
**Fundo:** `--page-bg` (ainda quase `#000000`)
**Texto:** `--page-text` (branco)

**Layout:**
- `SectionLabel`: `[ MERCADO BRASILEIRO DE IA // 2026 ]`
- Headline principal — Satoshi, `~10vw`, `line-height: 0.92`, `letter-spacing: -0.04em`:
  ```
  O mercado de IA
  cresceu em promessa.
  Vazio de infraestrutura.
  ```
- Rodapé da seção — full-width, border-top `1px white/10`:
  - Left (Mono, `white/30`): `"R$ 8B investidos em tecnologia corporativa em 2025"`
  - Right (Mono, cyan): `"Zero padrão de governança para IA crítica"`
- Número de seção: `02` — Mono, `8vw`, `white/06`, absolute bottom-right

**CEO-Copy — Dor Latente:**
Dor declarada: "ferramentas de IA são genéricas".
Dor latente: "não consigo auditar o que a IA fez — e isso me deixa vulnerável."
Esta seção nomeia o vazio sem ainda oferecer a solução.

---

### 03 — DIAGNOSIS (~70vh)
**Zona emocional:** Caos / início da virada (scroll ~20–32%)
**Fundo:** `--page-bg` (levíssima variação, imperceptível)

**Layout:**
- `SectionLabel`: `[ DIAGNÓSTICO ]`
- Headline — Satoshi Semibold, `~4.5vw`: `"Três sintomas. Uma causa."`
- Grid 3 colunas, border `1px page-text/10`, `padding: 48px`:

  | Col | Sintoma | Descrição |
  |-----|---------|-----------|
  | 01 | Automações que falham | Funcionam no demo. Quebram quando o processo fica sério. |
  | 02 | IA sem contrato | Nenhum modelo de confiança. Nenhuma trilha de decisão. |
  | 03 | Velocidade sem método | Lançam rápido. Sem governança, sem auditabilidade. |

- Cada célula: número Mono `0.7rem page-text/30`, título Satoshi Semibold uppercase `1rem`, descrição Satoshi Regular `0.9rem page-text/60`
- Hover: left-border 2px cyan, `background page-text/2`

---

### 04 — OUR ANSWER (~90vh)
**Zona emocional:** Virada imperceptível (scroll ~32–45%)
**Fundo:** `--page-bg` (shift sutil — o fundo está mudando mas o olho não percebe)

**Layout:**
- `SectionLabel`: `[ NOSSA RESPOSTA ]`
- Headline — Satoshi Semibold, `~4vw`: `"Um ecossistema. Quatro camadas."`
- Subtexto (max-width `540px`): `"Enquanto o mercado vendia peças isoladas, construímos um sistema. Cada camada tem uma função. Nenhuma existe sem a outra."`
- Grid 4 colunas, bordas `1px page-text/10`:

  | # | Nome | Papel |
  |---|------|-------|
  | 01 | AURORA GOVERNANCE | Direção estratégica, política de portfólio e governança. |
  | 02 | OZZMOSIS | A fábrica de capacidades reutilizáveis. A base que sustenta tudo. |
  | 03 | PRODUCTS | Sistemas especializados por domínio: comercial, jurídico e cognitivo. |
  | 04 | MADLAB | A camada criativa e institucional. Onde tecnologia encontra narrativa. |

---

### 05 — THE METHOD (~90vh)
**Zona emocional:** Virada imperceptível (scroll ~45–58%)
**Fundo:** `--page-bg` (ainda escuro mas notavelmente diferente do início)

**Layout:** assimétrico — coluna texto 55% · diagrama SVG 45%

- `SectionLabel`: `[ MÉTODO DE CONSTRUÇÃO ]`
- Headline — Satoshi Semibold, `~4vw`: `"Construído sobre contratos, não sobre improviso."`
- Body: `"Cada produto é sustentado por uma plataforma interna de capacidades reutilizáveis. APIs tipadas. Contratos explícitos. Governança de IA com auditabilidade embutida."`
- 4 componentes da plataforma (lista com dividers):

  | Componente | Papel |
  |-----------|-------|
  | **OZZMOSIS** | Fábrica de bibliotecas, contratos e runtimes compartilhados |
  | **AURORA CONDUCTOR** | Transforma intenção em plano e artefato executável |
  | **TRUSTWARE** | Contrato de confiabilidade entre produção e aprovação |
  | **ALVARO CORE** | Núcleo de raciocínio auditável para fluxos deterministas |

- Diagrama direito: 4 bandas horizontais empilhadas (SVG), bordas `1px`, labels internos, linhas finas conectando camadas, pontos cyan nas conexões. As bandas se revelam sequencialmente via `stroke-dashoffset` no scroll.

---

### 06 — LIVING DOCUMENT (~110vh)
**Zona emocional:** A Revelação — ponto âncora do argumento (scroll ~58–72%)
**Fundo:** `--page-bg` — aqui começa a inversão de contraste
**Tipografia:** PRIMEIRA aparição de Cormorant

**CEO-Copy — Etapa 4 (O Remédio):**
O visitante já sentiu a dor (seções 02–03), reconheceu a causa (04–05).
Aqui ele recebe a prova de que o remédio existe.
Esta seção não explica o Living Document — **demonstra**.

**Layout:**
- `SectionLabel`: `[ LIVING DOCUMENT // TRUSTWARE ]`
- Headline — **Cormorant** `12vw`, `line-height: 0.88`, `letter-spacing: -0.03em`:
  ```
  Não é output.
  É evidência
  auditável.
  ```
- Divider `1px page-text/10`
- Grid 2 colunas:

  **Coluna esquerda — O Documento Vivo:**
  ```
  ┌─────────────────────────────────┐
  │  DOCUMENTO VIVO                 │
  │  ──────────────────────         │
  │  CASO: Trabalhista #0482        │
  │  PRAZO: 14 dias                 │
  │  STATUS: URGENTE                │
  │                                 │
  │  █ ANÁLISE T-22.1               │
  │  Fundamentação: Art. 477...     │
  │  EMV: R$ 42.000                 │
  │  Cenário Favorável: 68%         │
  └─────────────────────────────────┘
  ```
  Fonte: Mono. Cada linha digita-se no scroll (progressivo, cursor pisca uma vez).

  **Coluna direita — Trilha de Auditoria:**
  ```
  ┌───────────────────────────────┐
  │  TRILHA DE AUDITORIA          │
  │                               │
  │  v1  ████ a3f9d2c...          │
  │  v2  ████ 7bc2e91...          │
  │  v3  ████ 1e04f8a... ◀        │
  │                               │
  │  [ VERSÃO ATUAL ]             │
  │  SHA-256 verificado           │
  │  Fonte: DataJud               │
  │  Agente: Elysian v1.2         │
  └───────────────────────────────┘
  ```
  Uma linha SVG cyan (`1px`, `stroke-dashoffset`) conecta os três hashes de cima a baixo. Seta `◀` aponta para v3.

- Citação — Satoshi italic, `1.1rem`, `page-text/65`:
  `"Enquanto o mercado entrega respostas, nós entregamos provas."`

**Animação de scroll (CEO-Effects — sequência de 4 fases):**
```
FASE 1 (0–25% da seção)
  Label + headline Cormorant: mask-wipe bottom→top
  0.8s, power2.out. Silêncio 400ms antes do painel.

FASE 2 (25–65%)
  Documento constrói linha a linha
  Cursor pisca uma vez por linha — não em loop
  Hashes da trilha aparecem sequencialmente:
  v1 → 300ms → v2 → 300ms → v3

FASE 3 (65–85%)
  Linha SVG cyan desenha-se conectando os hashes
  stroke-dashoffset, 0.6s, ease-in-out
  "Você está aqui" materializa no raciocínio, não no texto

FASE 4 (85–100%)
  Citação: fade + translateY(16px → 0), 0.5s, power2.out
```

**Por que esta seção vence com Google/Anthropic:**

| Elemento visual | O que o avaliador conclui |
|-----------------|--------------------------|
| Hash SHA-256 visível | Governança técnica real |
| Trilha append-only | Auditabilidade como arquitetura |
| Fonte DataJud + versão do agente | Rastreabilidade de dados e modelo |
| EMV + cenários probabilísticos | Output determinístico, não alucinação |

---

### 07 — WHAT WE'VE BUILT (~80vh)
**Zona emocional:** A Revelação continua (scroll ~72–82%)
**Fundo:** `--page-bg` — notavelmente mais quente agora

- `SectionLabel`: `[ PORTFÓLIO // 2026 ]`
- Headline — Satoshi Semibold, `~5vw`: `"Não é visão. É o que já existe."`
- 3 cards full-width, sem gap, border `1px page-text/10` entre eles:

  **Card 1 — Aurora CRM**
  - Tag: `OPERAÇÕES COMERCIAIS`
  - Status: `[ ATIVO ]` — dot cyan + texto cyan, Mono
  - Nome: Satoshi Semibold, `2rem`
  - Desc: "Operação comercial e execução outbound. Da proposta ao relacionamento, com automação, governança e integração nativa com WhatsApp."

  **Card 2 — Elysian Lex**
  - Tag: `INTELIGÊNCIA JURÍDICA`
  - Status: `[ EM DESENVOLVIMENTO ]` — `page-text/40`, Mono
  - Nome: Satoshi Semibold, `2rem`
  - Desc: "Inteligência legal aplicada a workflows jurídicos. Análise, suporte operacional e governança com auditabilidade estruturada."

  **Card 3 — Living Document**
  - Tag: `INFRAESTRUTURA DE CONFIANÇA`
  - Status: `[ EM DESENVOLVIMENTO ]` — `page-text/40`, Mono
  - Nome: Satoshi Semibold, `2rem`
  - Desc: "O estado persistente de verdade auditável. Não um arquivo — um ativo de confiança com identidade criptográfica e trilha forense completa."

- Reveal: sequential left→right, 120ms stagger, mask-wipe

---

### 08 — THE BUILDER (~80vh)
**Zona emocional:** Casa (scroll ~82–92%)
**Fundo:** `--page-bg` — marfim quente. A seção mais humana.

**CEO-Copy — Etapa 3/4 (humanização):**
O argumento técnico foi feito. Aqui o visitante encontra a pessoa.
Não é bio — é declaração de convicção. Sem foto — a tipografia carrega todo o peso.

**Layout:** full-width, tipográfico puro. Espaço nulo como instrumento.

- Overline: Mono uppercase `page-text/40`, `0.65rem`: `RODRIGO // FUNDADOR · AURORA FACTORY`
- Citação — **Cormorant** italic, `~6vw`, `line-height: 1.0`, `letter-spacing: -0.025em`, full-width, max-width `900px`:
  ```
  "O futuro é determinista.
  Construímos sistemas que tornam
  o erro matematicamente improvável."
  ```
- Body — Satoshi Regular, `1rem`, `page-text/60`, `line-height: 1.6`, max-width `560px`:
  `"Rodrigo construiu a Aurora a partir de uma convicção: sistemas de IA precisam de método, governança e arquitetura — não apenas de um bom modelo. Do código à narrativa institucional, cada camada do ecossistema foi desenhada para durar."`
- Footer: divider `1px` + Mono `page-text/30` `0.65rem`: `AURORA FACTORY // MADLAB RESEARCH GROUP`

---

### 09 — CALL TO ACTION (~60vh)
**Zona emocional:** Energia (CTA) — fixo em `#00FFEF`, fora do arco
**Texto:** sempre `#000000`

**CEO-Copy — Etapa 5 (A compra é inevitável):**
O visitante que chegou até aqui já decidiu. O CTA apenas confirma.

- Headline — **Cormorant**, `~5.5vw`, `line-height: 0.92`, `letter-spacing: -0.02em`, black:
  `"Vamos conversar sobre o que estamos construindo."`
- Subtexto — Satoshi Regular, `1.1rem`, `black/70`:
  `"Se você está avaliando parceiros, investimentos ou programas de aceleração — esta é a conversa certa."`
- Botão primário — `Agendar uma conversa →` — black bg, white text, sharp, `px-10 py-5`. Hover: bg-white, text-black.
- Secundário — Mono, `black/50`, `0.75rem`: `"ou escreva para contato@elysian.ai.br"`
- Número de seção: `09` — Mono, `8vw`, `black/08`, absolute bottom-right

---

### 10 — FOOTER (~80px)
**Fundo:** `#1a1816` — fechamento suave, não tensão
- Border-top: `1px white/10`
- Left: `"ELYSIAN"` — Satoshi Semibold, `1rem`, white
- Center: `Ecossistema · Produtos · Método · Agendar` — Mono uppercase, `white/30`, `0.65rem`
- Right: `"© 2026 Aurora Factory / MadLab Research Group"` — Mono, `white/20`, `0.65rem`

---

## 7. ElysianChat — Agente de Vendas

### Identidade
- Persona: especialista Elysian — conhece todos os produtos, ICP, objeções comuns, preços
- Domínio restrito: fala exclusivamente sobre Elysian, seus produtos e o mercado que serve
- Função: qualificar lead → educar → capturar contato → agendar conversa

### Widget
- Posição: `fixed bottom-6 right-6`, `z-50`
- Estado fechado: círculo `56px`, `background: #000`, border `1px white/20`
  - Centro: `"E"` em Satoshi Semibold, `1.1rem`, white
  - Aparece após o hero (scroll > `100vh`)
  - Entrada: fade + scale `0.8 → 1`, 400ms
- Estado aberto: painel lateral `380px × 520px`, `border-radius: 0`
  - Header: `"Elysian"` + `[×]` para fechar
  - Área de chat com scroll interno
  - Input + botão sharp na base

### Stack
- `@google/genai` (Gemini 2.0 Flash — já no projeto)
- Firebase Firestore — persiste conversas e captura leads
- System prompt: persona Elysian + contexto de todos os produtos + guia de qualificação
  - Captura: nome → necessidade → tamanho/contexto → email → CTA para agendar
- Fallback offline: formulário simples de contato

### System Prompt (esqueleto)
```
Você é o especialista Elysian. Representa uma empresa que constrói infraestrutura 
cognitiva com determinismo, governança e auditabilidade — na contramão do mercado 
de IA genérico.

Produtos:
- Aurora CRM: operação comercial com WhatsApp, automação e governança [ATIVO]
- Elysian Lex: inteligência jurídica com auditabilidade estruturada [EM DEV]
- Living Document: evidência auditável com hash chain e rastreabilidade [EM DEV]

Sua função: entender a necessidade do visitante, educá-lo sobre como a Elysian 
resolve seu problema específico, e convidá-lo a agendar uma conversa.

Não fale sobre nada fora do ecossistema Elysian/Aurora.
Não cite concorrentes pelo nome.
Capture: nome → contexto/necessidade → email → proposta de agendamento.
```

---

## 8. Motion — Parâmetros Canônicos (CEO-Effects)

```
Scroll reveal geral:    mask-wipe bottom→top, 0.6s, power2.out, stagger 80ms
Header transition:      opacity + blur, 300ms, linear
Product cards reveal:   sequential, 120ms stagger, mask-wipe
Living Document:        ver Fase 1–4 na seção 06
Architecture diagram:   stroke-dashoffset por camada, 200ms stagger
CTA headline:           split por palavra, translateY + opacity, 60ms stagger
Chat widget entrada:     scale 0.8→1 + opacity, 400ms, power2.out

Easing padrão:          power2.out (saída natural com peso)
Easing de entrada:      power2.inOut (gravidade real)
Mouse follow / lerp:    0.06 (suave, nunca snap)

PROIBIDO:
  bounce, elastic, back  — comunicam leveza. Dark Editorial não é leve.
  parallax decorativo    — sem narrativa = ruído
  animações em loop      — exceto cursores de documento (pisca 1×, some)
```

---

## 9. Arquitetura de Arquivos

```
src/
├── App.tsx                         ← ReactLenis + ScrollDriver + Router + Chat
├── index.css                       ← tokens atualizados + Satoshi + Cormorant
│
├── components/
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── ScrollDriver.tsx             ← GSAP ScrollTrigger governa --page-bg
│   ├── SectionLabel.tsx             ← [ LABEL ] padronizado
│   ├── ElysianChat.tsx              ← widget + painel lateral
│   │
│   └── sections/
│       ├── VoidStatement.tsx        ← seção 02
│       ├── Diagnosis.tsx            ← seção 03
│       ├── OurAnswer.tsx            ← seção 04
│       ├── TheMethod.tsx            ← seção 05
│       ├── LivingDocument.tsx       ← seção 06 (âncora central)
│       ├── WhatWeBuilt.tsx          ← seção 07
│       ├── TheBuilder.tsx           ← seção 08
│       └── CallToAction.tsx         ← seção 09
│
├── hooks/
│   └── useScrollProgress.ts        ← lê progresso normalizado do scroll
│
└── pages/
    ├── LexPage.tsx                  ← stub /lex
    ├── CRMPage.tsx                  ← stub /crm
    └── LivingDocPage.tsx            ← stub /living-document
```

**Componentes existentes mantidos sem alteração:**
- `SovereignHeroWebGL.tsx`
- `Preloader.tsx`
- `firebase.ts`

---

## 10. Copy — Palavras Proibidas e Obrigatórias

**Obrigatórias (ou parafraseadas próximas):**
- `infraestrutura cognitiva` (não "software", não "soluções")
- `governança embutida`
- `contratos tipados` / `APIs tipadas`
- `auditabilidade`
- `plataforma própria`
- `determinismo`
- `evidência auditável`

**Proibidas:**
- "desenvolvemos soluções digitais"
- "fazemos IA para empresas"
- "plataforma inovadora"
- "transformação digital"
- "ecossistema robusto"
- qualquer palavra que soe como pitch deck

**Honestidade de status obrigatória:**
- CRM: `[ ATIVO ]`
- Elysian Lex: `[ EM DESENVOLVIMENTO ]`
- Living Document: `[ EM DESENVOLVIMENTO ]`

---

## 11. Dependências a Adicionar

```bash
npm install react-router-dom gsap       # roteamento + ScrollTrigger
```

`gsap` já é dependência do projeto — confirmar versão.
`react-router-dom` a adicionar (v6).

---

## 12. Critério de Conclusão

A landing está concluída quando:
- [ ] ScrollDriver interpola `--page-bg` e `--page-text` ao longo do scroll completo
- [ ] Todos os 10 blocos estão implementados e responsivos (mobile/desktop)
- [ ] SovereignHeroWebGL e Preloader integram sem quebrar
- [ ] LivingDocument anima corretamente em scroll (4 fases)
- [ ] ElysianChat abre/fecha, envia mensagens via Gemini, persiste em Firebase
- [ ] Rotas `/lex`, `/crm`, `/living-document` existem como stubs funcionais
- [ ] `prefers-reduced-motion` desativa animações pesadas
- [ ] Build sem erros TypeScript: `npm run check` passa
- [ ] Verificação visual no localhost antes de declarar pronto
