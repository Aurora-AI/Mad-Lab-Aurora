# ANTIGRAVITY_REFERENCE_DESIGN_SYSTEM_v0.1

## Core Identity
- **Estilo:** Clean futurista, editorial, técnico e silencioso.
- **Base Visual:** Branco/cinza claro com contraste preto suave.
- **Sensação:** Laboratório premium, sistema inteligente, baixa fricção.
- **Evitar:** Dashboard denso, cards pesados, bordas fortes, excesso de ícones.

---

## 1. Cores e Tokens de Paleta
```css
:root {
  --ag-white: #FFFFFF;
  --ag-grey-10: #F8F9FC;
  --ag-grey-20: #EFF2F7;
  --ag-grey-50: #E6EAF0;
  --ag-grey-100: #E1E6EC;
  --ag-grey-200: #CDD4DC;
  --ag-grey-300: #B2BBC5;
  --ag-grey-800: #45474D;
  --ag-grey-900: #2F3034;
  --ag-grey-1000: #212226;
  --ag-grey-1200: #121317;

  --ag-blue: #3279F9;

  --ag-surface: var(--ag-white);
  --ag-surface-soft: var(--ag-grey-10);
  --ag-surface-raised: var(--ag-grey-20);
  --ag-text: var(--ag-grey-1200);
  --ag-text-muted: var(--ag-grey-800);
  --ag-outline: rgba(33, 34, 38, 0.06);
}
```

---

## 2. Tipografia e Escala
```css
:root {
  --ag-font-display: "Google Sans Flex", "Inter", system-ui, sans-serif;
  --ag-font-code: "Google Sans Code", "DM Mono", "JetBrains Mono", monospace;

  --ag-h1-size: clamp(64px, 8vw, 124px);
  --ag-h1-line: 0.98;
  --ag-h1-tracking: -0.02em;

  --ag-h2-size: clamp(42px, 5vw, 72px);
  --ag-h2-line: 1;

  --ag-body-size: 17.5px;
  --ag-body-line: 1.45;

  --ag-caption-size: 12.5px;
  --ag-caption-line: 1.24;
}
```

---

## 3. Espaçamento
```css
:root {
  --ag-space-xs: 8px;
  --ag-space-sm: 12px;
  --ag-space-md: 24px;
  --ag-space-lg: 40px;
  --ag-space-xl: 64px;
  --ag-space-2xl: 96px;
  --ag-space-3xl: 140px;
}
```

---

## 4. Superfícies
```css
.ag-surface {
  background: rgba(255, 255, 255, 0.78);
  border: 1px solid rgba(33, 34, 38, 0.06);
  border-radius: 28px;
  backdrop-filter: blur(16px);
}

.ag-surface-soft {
  background: #F8F9FC;
  border-radius: 32px;
}

.ag-floating {
  box-shadow:
    0 30px 80px rgba(18, 19, 23, 0.06),
    0 1px 0 rgba(255, 255, 255, 0.8) inset;
}
```

---

## 5. Botões
```css
.ag-button-primary {
  min-height: 48px;
  padding: 12px 24px;
  border-radius: 999px;
  background: #121317;
  color: #FFFFFF;
  font-family: var(--ag-font-display);
  font-weight: 500;
  letter-spacing: 0.01em;
}

.ag-button-secondary {
  min-height: 48px;
  padding: 12px 24px;
  border-radius: 999px;
  background: rgba(183, 191, 217, 0.10);
  color: #121317;
  backdrop-filter: blur(8px);
}

.ag-button-secondary:hover {
  background: #EFF2F7;
}
```

---

## 6. Links com Seta
```css
.ag-arrow-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: opacity 0.2s ease;
}

.ag-arrow-link::after {
  content: "→";
  transition: transform 0.3s ease;
}

.ag-arrow-link:hover::after,
.ag-arrow-link:focus-visible::after {
  transform: translateX(50%);
}
```

---

## 7. Background Atmosférico
```css
.ag-background {
  background:
    radial-gradient(circle at 20% 10%, rgba(50, 121, 249, 0.08), transparent 28%),
    radial-gradient(circle at 80% 20%, rgba(183, 191, 217, 0.18), transparent 26%),
    linear-gradient(180deg, #FFFFFF 0%, #F8F9FC 100%);
}
```

---

## 8. Motion Policy
- **Movimento Permitido:**
  - Microdeslocamento de seta em links.
  - Blur/opacity suave.
  - Partículas ou campo vivo apenas em hero/destaque.
  - Transform/opacity preferencialmente.
- **Movimento Proibido:**
  - Animação ornamental.
  - Glow agressivo.
  - Looping chamativo.
  - Movimento que dificulte a leitura.

---

## 9. Componentes-base e Estrutura
- **Header:** Fixo, baixo, transparente, com logo e navegação mínima.
- **Hero:** Grande, editorial, com fundo vivo (se aplicável).
- **Cards:** Borda quase invisível, raio grande, sombra leve.
- **CTA:** Pill buttons (botões arredondados).
- **Code/Technical Blocks:** Fonte monoespaçada, contraste alto, mas sem dominar a página.
- **Carousel Controls:** Botões arredondados dentro de cápsula tonal.

---

## 10. Layout Canônico
```txt
Left Action Rail + Conversational Bottom Chat Bar + Volumetric Canvas
```

### Estrutura Visual:
```txt
┌─────────────────────────────────────────────┐
│  Campo visual / conteúdo / objetos vivos     │
│                                             │
│  [Hero / decisão / cards / intenção]         │
│                                             │
│                                             │
├─────────────────────────────────────────────┤
│  Barra de chat fixa inferior                 │
└─────────────────────────────────────────────┘
```

- **Lateral Esquerda:** Ações, navegação, menu, histórico, governança.
- **Barra de Chat Inferior (Regras):**
  - Substitui barra de endereço móvel.
  - Posição: `bottom fixed`.
  - Altura: 64px a 35vh.
  - Raio: pill quando vazio / painel expandido no texto longo.
  - Escala de fonte responsiva ao volume de texto.
- **Regra de Proporção:**
  - Texto curto -> barra compacta.
  - Texto médio -> barra cresce verticalmente.
  - Texto longo -> barra vira painel inferior com scroll interno.
  - Nunca cobre o CTA ou o campo de decisão sem transição clara.
