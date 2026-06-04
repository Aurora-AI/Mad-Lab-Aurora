# Design System: Aurora Institutional — Protocol Sovereign (v2.1.1)

## 1. Visual Theme & Atmosphere

**Light Editorial (Parchment & Ink).** Uma postura de autoridade institucional absoluta. O design abandona o "dramatismo dark" em favor da "solidez documental". A interface deve evocar a sensação de um certificado de segurança, um tratado diplomático ou um blueprint de engenharia de alta precisão.

- **Arquitetura (Institutional Grid):** Grids assimétricos (40/60, 35/65) com divisores de 0.5px. O espaço negativo não é apenas "branco", é "espaço de pensamento".
- **Materialidade (High Grammage):** Uso de texturas de papel (grain sutil) e tipografia que parece "impressa" no fundo, não apenas flutuando sobre ele.
- **Autoridade (The Filter):** Hierarquia tipográfica que privilegia a legibilidade e o peso editorial. Headlines massivas em serif contrastando com metadados técnicos em mono.

## 2. Color Palette & Roles (The Parchment & Ink Protocol)

**O uso de Dark Mode/Preto Puro está PROIBIDO por mandato institucional.**

- **Parchment Memory** (#F4F1EA) — Fundo primário. Sugere papel de alta gramatura, longevidade e solidez documental.
- **Deep Obsidian** (#1A1A17) — Tipografia primária (Ink). Uma versão levemente quente do preto, para evitar o contraste "digital" agressivo.
- **Aureate Weight** (#C5A059) — Acento institucional. Usado estritamente para labels técnicos (Voz 2), ícones de 0.5px e realces de autoridade.
- **Whisper Structure** (rgba(26, 26, 23, 0.08)) — Linhas de grade, divisores e grids assimétricos. Estrutura invisível mas presente.

## 3. Typography (The Three Voices)

- **Voz 1 (Display):** *Cormorant Garamond* (Italic/Bold). Monumental e autoritária. Escala 64-120px. Para headlines que filtram e estabelecem o claim central.
- **Voz 2 (Técnica):** *DM Mono* (Regular, Capslock, Tracking 0.2em). Para metadados, refs de OS, timestamps e labels de seção. Sugere precisão técnica e "Trustware".
- **Voz 3 (Editorial):** *EB Garamond* (Regular). Para parágrafos de argumentação densa. Escala 18-22px. Nunca bold em corpo de texto.
- **Banned:** `Inter`, `Roboto`, `Arial` e fontes de sistema genéricas.

## 4. Layout Principles (Credency v1)

- **Split Assimétrico:** Divisão vertical 40/60 ou 35/65. Conteúdo identidade à esquerda, conteúdo operacional à direita.
- **Pinned Statement:** Frases de impacto fixadas ou deslocadas que ancoram a leitura.
- **Grid de Diagnóstico:** Células limpas com bordas de 0.5px. Uma unidade de inteligência por célula.
- **Max-Width:** 1440px rigoroso para preservar a tensão editorial em telas ultra-wide.

## 5. Motion & Interaction

- **Regra do Silêncio (0.8s):** Todo componente possui um estado de repouso inicial antes da revelação.
- **Sovereign Reveal:** Transições suaves baseadas em `clip-path`, `opacity` e deslocamentos sutis de 20px. Sem "bouncing" ou efeitos elásticos.
- **Hardware Acceleration:** Uso mandatório de `transform: translate3d` e `will-change`.
- **Counter Animation:** Números e métricas técnicas devem animar ao entrar no viewport (Voz 2).

## 6. Anti-Patterns (BANNED)

- **Dark Mode:** Terminantemente proibido para este projeto.
- **Gradientes SaaS:** Proibidos.
- **Botões com Sombra:** Proibidos. Usar apenas bordas finas ou preenchimento sólido.
- **Border-radius alto:** Máximo 4px para elementos premium. Cards devem preferir bordas retas com divisores.
- **Placeholder Images:** Proibido. Usar WebGL real ou imagens geradas de alta densidade.
