# Visual Debt Index (OS-MADLAB-03)

**OS ID:** `OS-MADLAB-VISUAL-DEBT-TRIAGE-20260527-003`  
**Fase:** Micro-Etapa 3 — Criar Design Debt Baseline  
**Data:** 28 de Maio de 2026  
**Status:** DÍVIDA BASELINEADA, NÃO RESOLVIDA, NÃO ALLOWLISTED  

---

## 1. Origem dos Dados

Este índice consolida as métricas brutas e logs coletados na **OS-MADLAB-02** (`OS-MADLAB-VISUAL-QUALITY-GATES-20260527-002`) por meio dos seguintes gates e relatórios:
*   **design-system-lint.ps1** (Lint de regras de design)
*   **motion-regression-check.js** (Scan estático de animações e cleanups)
*   **visual-performance-harness.js** / **performance-report.json** (Harness de scroll automatizado Puppeteer)

---

## 2. Totais e Métricas de Baseline Inicial

O baseline de partida oficial do Mad Lab Aurora é definido pelos seguintes totais:

*   **Desvios de Design System:** **1218 desvios** detectados no relatório bruto.
    *   *Nota de Triagem:* Destes 1218, **151 desvios reais** estão no código fonte ativo de produção, enquanto 1067 são falsos-positivos de pacotes npm externos em `node_modules` e pastas de compilação `dist/docs` gerados por uma falha de escape de barra invertida em regex no script.
*   **Alertas de Motion:** **52 alertas** de vazamento ou falta de reduced-motion detectados pelo check.
*   **Métricas de Performance Headless (CI):**
    *   *FPS Médio:* **22.86**
    *   *p95 Latência:* **130.6ms**
    *   *Condição:* Aprovado em modo CI permissivo sob a flag `--allow-slow-frames` devido ao ambiente de renderização por software SwiftShader sem aceleração física por GPU.

---

## 3. Agrupamentos e Distribuição

### 3.1 Por Subprojeto (Cores, Radii, Shadows - Código Ativo)
*   **ElysianCorp:** **80** desvios reais.
*   **aurora-web:** **71** desvios reais.
*   **AuroraCognitiveAssets:** **0** desvios.

### 3.2 Por Regra (Código Ativo)
*   **Border-Radius > 2px:** 38 casos.
*   **Cores Hardcoded (Hex/RGB/HSL):** 79 casos (sendo 27 Hex e 52 RGB/HSL).
*   **Shadows Proibidas:** 34 casos.

### 3.3 Por Arquivo (Top 10 Arquivos de Produção Mais Impactados)
1.  `\aurora-web\src\components\ui\hero-futuristic.tsx`: **15** desvios.
2.  `\ElysianCorp\src\components\sections\IntegrityGap.tsx`: **14** desvios.
3.  `\aurora-web\src\components\ElysianChat.tsx`: **14** desvios.
4.  `\ElysianCorp\src\components\sections\ControlFailure.tsx`: **14** desvios.
5.  `\ElysianCorp\src\components\ui\AssetCard.tsx`: **7** desvios.
6.  `\ElysianCorp\src\components\ui\background-paths.tsx`: **5** desvios.
7.  `\aurora-web\src\pages\ArsenalPage.tsx`: **5** desvios.
8.  `\aurora-web\src\components\sections\WhatWeBuilt.tsx`: **5** desvios.
9.  `\aurora-web\src\components\hero\HeroScene.tsx`: **5** desvios.
10. `\aurora-web\src\components\AuroraHero.tsx`: **5** desvios.

---

## 4. Estado de Governança na Micro-Etapa 3

Nesta micro-etapa, as seguintes restrições de estado foram rigorosamente seguidas:
*   **Exceções na Allowlist:** `NENHUMA`. O arquivo `.aurora/design-lint-allowlist.json` não foi criado nem alimentado nesta etapa.
*   **Baseline de Dívida:** `BASELINEADO`. O arquivo `.aurora/design-debt-baseline.json` foi criado contendo o limite congelado de 151 desvios de design reais (80 em `ElysianCorp` e 71 em `aurora-web`), excluindo 1067 falsos positivos.
*   **Alterações de Código:** `NENHUMA`. O script de linter `design-system-lint.ps1` não sofreu alterações e nenhum código visual de estilo nos subprojetos foi refatorado.
*   **Lógica Cognitiva:** Sem auto-repair, sem promoção de KIs para a memória global e sem auto-merges.

---

## 5. Classificação Detalhada de Alertas de Motion (Micro-Etapa 2)

Na Micro-Etapa 2, todos os **52 alertas de motion** detectados pelo `motion-regression-check.js` foram triados e classificados de acordo com critérios objetivos de severidade e estabilidade operacional.

### 5.1 Critério Objetivo de Severidade

*   **P0 (Crítico):** Risco real de travamento de aba, vazamento crítico de recursos de GPU no rendering loop, ou loops infinitos de animação sem cancelamento no thread principal, causando degradação imediata do frame-rate (FPS) e gargalos de performance perceptíveis.
*   **P1 (Importante):** Ausência provável de cleanup de ciclo de vida (ex.: missing Three.js `.dispose()`, GSAP `revert()`/`kill()`, ou `cancelAnimationFrame()`), gerando acúmulo lento de memória (leaks) que pode degradar a estabilidade sob uso prolongado.
*   **P2 (Acessibilidade):** Ausência da diretiva `@media (prefers-reduced-motion: reduce)` ou hooks de mídia equivalentes em componentes que executam animações ativas, descumprindo os padrões mínimos de acessibilidade visual.
*   **P3 (Tolerado):** Alertas tolerados, falsos positivos gerados pelo linter estático (ex.: elementos declarativos auto-geridos pelo React Three Fiber, objetos CPU-bound sem alocação em GPU), ou arquivos de documentação/estilos legados que não impactam a produção.

---

### 5.2 Tabela de Triage e Classificação dos 52 Alertas

| ID | Subprojeto | Arquivo | Alerta / Regra Detectada | Severidade | Justificativa | Ação Recomendada | Backlog |
|---|---|---|---|:---:|---|---|:---:|
| 1 | ElysianCorp | `docs/brand/Elysian Design System/colors_and_type.css` | Missing prefers-reduced-motion fallback | **P3** | Arquivo de documentação estática, não carregado no runtime da aplicação em produção. | Nenhuma (Falso positivo de escopo). | Monitoramento |
| 2 | ElysianCorp | `src/components/cursor/MagneticCursor.tsx` | Missing prefers-reduced-motion fallback | **P2** | Efeito físico de lag no cursor customizado sem tratamento para redução de movimento. | Adicionar verificação de `prefers-reduced-motion` para desativar o magnetismo e posicionamento diferido. | Backlog imediato |
| 3 | ElysianCorp | `src/components/fx/IdentityFragmenter.tsx` | Missing prefers-reduced-motion fallback | **P2** | Animação complexa de fragmentação gráfica sem alternativa estática para acessibilidade. | Desabilitar efeitos de fragmentação espacial quando `prefers-reduced-motion` estiver ativo. | Backlog imediato |
| 4 | ElysianCorp | `src/components/fx/ScramblePortrait.tsx` | Missing prefers-reduced-motion fallback | **P2** | Embaralhamento de caracteres que pode causar desconforto cognitivo e fadiga visual. | Exibir o texto final estabilizado imediatamente se o usuário preferir movimentos reduzidos. | Backlog imediato |
| 5 | ElysianCorp | `src/components/hero/ConcaveScene.tsx` | Missing prefers-reduced-motion fallback | **P2** | Movimentação 3D flutuante e contínua do Hero sem fallback de acessibilidade. | Congelar posições de flutuação de câmera/objetos sob `prefers-reduced-motion`. | Backlog imediato |
| 6 | ElysianCorp | `src/components/hero/ExoFluidHero.tsx` | Missing prefers-reduced-motion fallback | **P2** | Simulação complexa de dinâmica de fluidos rodando em Canvas sem override de acessibilidade. | Pausar a simulação e renderizar um frame estático de fundo sob `prefers-reduced-motion`. | Backlog imediato |
| 7 | ElysianCorp | `src/components/hero/GazeForensicHero.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transições espaciais de alta velocidade baseadas em rastreamento ocular sem fallback. | Suavizar/reduzir velocidades ou congelar em estado final sob `prefers-reduced-motion`. | Backlog imediato |
| 8 | ElysianCorp | `src/components/hero/HeroContent.tsx` | Missing prefers-reduced-motion fallback | **P2** | Entradas de texto em slide-in e rotações suaves sem tratamento de movimento reduzido. | Substituir transições de translação espacial por transições de opacidade linear direta (fade). | Backlog imediato |
| 9 | ElysianCorp | `src/components/sections/AuditTrail.tsx` | Missing prefers-reduced-motion fallback | **P2** | Deslocamento parallax acoplado ao scroll da página sem tratamento de acessibilidade. | Desativar o cálculo de parallax no scroll quando `prefers-reduced-motion` for ativo. | Backlog imediato |
| 10 | ElysianCorp | `src/components/sections/ControlFailure.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transições de layout e fade/deslocamento de cards sem bypass de acessibilidade. | Sobrescrever estilos de animação para entrada direta sem deslocamento. | Backlog imediato |
| 11 | ElysianCorp | `src/components/sections/ForensicFooter.tsx` | Missing prefers-reduced-motion fallback | **P2** | Entrada dinâmica do rodapé com escala e translação sem fallback de movimento. | Remover deslocamentos espaciais na entrada da seção para acessibilidade. | Backlog imediato |
| 12 | ElysianCorp | `src/components/sections/IntegrityGap.tsx` | Missing prefers-reduced-motion fallback | **P2** | Deslocamentos significativos de blocos de texto que podem causar desalinhamento cognitivo. | Desativar translações na transição dos cards, limitando o efeito a fade simples. | Backlog imediato |
| 13 | ElysianCorp | `src/components/sections/SectionConversion.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transição de slide lateral no formulário de conversão sem fallback de movimento. | Exibir o formulário em sua posição final instantaneamente sob `prefers-reduced-motion`. | Backlog imediato |
| 14 | ElysianCorp | `src/components/sections/SectionGap.tsx` | Missing prefers-reduced-motion fallback | **P2** | Deslocamento e escalas na abertura de quebra sem fallback de acessibilidade. | Desativar transformações e exibir layout fixo e estático. | Backlog imediato |
| 15 | ElysianCorp | `src/components/sections/SectionMechanism.tsx` | Missing prefers-reduced-motion fallback | **P2** | Animações contínuas de fluxos gráficos e diagramas sem fallback de movimento. | Fixar diagramas em seu estado lógico final sem movimento sob `prefers-reduced-motion`. | Backlog imediato |
| 16 | ElysianCorp | `src/components/sections/SectionValidation.tsx` | Missing prefers-reduced-motion fallback | **P2** | Entrada com escala em checks de validação sem tratamento de acessibilidade. | Exibir ícones de sucesso instantaneamente sem delays ou transições de escala. | Backlog imediato |
| 17 | ElysianCorp | `src/components/sections/TrustwareAnswer.tsx` | Missing prefers-reduced-motion fallback | **P2** | Revelação de seções informativas com slide-up sem fallback de movimento. | Desativar deslocamento espacial e manter apenas fade linear simples. | Backlog imediato |
| 18 | ElysianCorp | `src/components/sections/TrustwareArchitecture.tsx` | Missing prefers-reduced-motion fallback | **P2** | Pulso elétrico e efeitos de dados activos no diagrama sem tratamento de acessibilidade. | Parar animações de pulsação e oscilação de linhas conectivas. | Backlog imediato |
| 19 | ElysianCorp | `src/components/sections/TrustwareClients.tsx` | Missing prefers-reduced-motion fallback | **P2** | Carrossel de marcas com rolagem infinita e contínua sem controle de acessibilidade. | Pausar a animação de rolagem contínua quando `prefers-reduced-motion` for ativo. | Backlog imediato |
| 20 | ElysianCorp | `src/components/sections/TrustwareFounder.tsx` | Missing prefers-reduced-motion fallback | **P2** | Revelação espacial da seção biográfica do fundador sem bypass de movimento. | Desativar translações na entrada da seção. | Backlog imediato |
| 21 | ElysianCorp | `src/components/sections/TrustwareMoat.tsx` | Missing prefers-reduced-motion fallback | **P2** | Contadores numéricos que incrementam via JS sem fallback de acessibilidade. | Mostrar o número inteiro final instantaneamente, sem contagem regressiva/progressiva. | Backlog imediato |
| 22 | ElysianCorp | `src/components/sections/TrustwarePortfolio.tsx` | Missing prefers-reduced-motion fallback | **P2** | Entrada com escala e rotação na grade de cartões sem fallback de movimento. | Remover transformações dinâmicas dos cartões de portfólio. | Backlog imediato |
| 23 | ElysianCorp | `src/components/sections/TrustwareReality.tsx` | Missing prefers-reduced-motion fallback | **P2** | Fundo interativo que se desloca baseado no mouse sem fallback de acessibilidade. | Desativar o movimento reativo do mouse sob `prefers-reduced-motion`. | Backlog imediato |
| 24 | ElysianCorp | `src/components/ui/HalideLanding.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transições globais de layout e fade/deslocamento de cards sem bypass de acessibilidade. | Sobrescrever transições de posição por fade direto sob `prefers-reduced-motion`. | Backlog imediato |
| 25 | ElysianCorp | `src/components/ui/Header.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transição de revelação e escala no menu de navegação sem fallback de movimento. | Substituir transição por aparecimento instantâneo sem escala. | Backlog imediato |
| 26 | ElysianCorp | `src/components/ui/ShowcaseNavigation.tsx` | Unclean GSAP lifecycle | **P3** | Tween único de `scrollTo` disparado exclusivamente sob clique do usuário; sem loops ou timelines ativas. | Nenhuma ação crítica. Pode ser encapsulado em useGSAP para conformidade estrita futuramente. | Monitoramento |
| 27 | ElysianCorp | `src/components/ui/ShowcaseNavigation.tsx` | Missing prefers-reduced-motion fallback | **P2** | Rolagem suave da página acionada por botões sem alternativa de pulo instantâneo. | Usar salto direto (jump) sem animação de scroll caso movimento reduzido seja ativo. | Backlog imediato |
| 28 | ElysianCorp | `src/styles/globals.css` | Missing prefers-reduced-motion fallback | **P2** | Folha de estilo de produção com animações de CSS declaradas sem overrides de acessibilidade. | Adicionar uma regra global `@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }`. | Backlog imediato |
| 29 | ElysianCorp | `src/styles/tokens.css` | Missing prefers-reduced-motion fallback | **P2** | Definição de tokens temporais de animação sem tratamento de acessibilidade. | Declarar durações zeradas de animação sob bloco de redução de movimento. | Backlog imediato |
| 30 | aurora-web | `src/components/ARC/ArcPuzzlePiece.tsx` | ThreeJS memory leak risk | **P1** | Instanciação de `new THREE.BufferGeometry()` dentro de `useMemo` sem cleanup ao desmontar. | Adicionar useEffect para invocar explicitamente `geometry.dispose()` na desmontagem. | Backlog imediato |
| 31 | aurora-web | `src/components/ARC/ArcPuzzlePiece.tsx` | Unclean GSAP lifecycle | **P0** | Instanciação de Tween GSAP a cada frame na `useFrame` (60/s). Causa churn extremo de Garbage Collector e lag. | Remover o Tween GSAP do looping de frames. Usar interpolação manual (lerp) ou ler valor sob useEffect. | Backlog imediato |
| 32 | aurora-web | `src/components/ARC/ArcPuzzlePiece.tsx` | Missing prefers-reduced-motion fallback | **P2** | Explosão 3D e rotação caótica de peças sem fallback de movimento reduzido. | Forçar progresso final da explosão em 100% ou desabilitar rotações caóticas. | Backlog imediato |
| 33 | aurora-web | `src/components/AuroraHero.tsx` | Missing prefers-reduced-motion fallback | **P2** | Efeitos de layout e transições de entrada do hero sem fallback de acessibilidade. | Desativar transições de posição espacial, aplicando apenas opacidade direta. | Backlog imediato |
| 34 | aurora-web | `src/components/elysian/ElysianScene.tsx` | ThreeJS memory leak risk | **P3** | Linter detectou `new THREE.Object3D()`, mas Object3D é CPU-bound e não aloca buffers na GPU, não possuindo método dispose. | Falso positivo gerado pela regra estática de linter. | Monitoramento |
| 35 | aurora-web | `src/components/ElysianChat.tsx` | Missing prefers-reduced-motion fallback | **P2** | Lista de chat animando novos balões com translação e fade sem fallback. | Apresentar novas mensagens de chat diretamente sem translação de entrada. | Backlog imediato |
| 36 | aurora-web | `src/components/Footer.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transições de hover em links do rodapé sem fallback de movimento. | Desativar efeitos de translação e escalas dinâmicas sob reduced motion. | Backlog imediato |
| 37 | aurora-web | `src/components/fx/IdentityFragmenter.tsx` | Missing prefers-reduced-motion fallback | **P2** | Shaders de distorção de glitch contínuos que podem provocar estresse visual. | Desabilitar efeitos de fragmentação de tela sob `prefers-reduced-motion`. | Backlog imediato |
| 38 | aurora-web | `src/components/fx/ScramblePortrait.tsx` | Missing prefers-reduced-motion fallback | **P2** | Animação de decodificação de texto de alto contraste sem fallback de movimento. | Renderizar o texto limpo estático imediatamente se reduzido for ativado. | Backlog imediato |
| 39 | aurora-web | `src/components/Header.tsx` | Missing prefers-reduced-motion fallback | **P2** | Entrada com escala no cabeçalho sem fallback de movimento. | Substituir por exibição estática sem transição espacial. | Backlog imediato |
| 40 | aurora-web | `src/components/hero/materials/useEdgePreservingMaterial.ts` | ThreeJS memory leak risk | **P1** | Instanciação de `MeshStandardMaterial` via `useMemo` em custom hook sem chamada de cleanup `.dispose()`. | Adicionar retorno de cleanup para descartar materiais quando o hook for desmontado ou a textura mudar. | Backlog imediato |
| 41 | aurora-web | `src/components/hero/PuzzleGroup.tsx` | ThreeJS memory leak risk | **P1** | Depende de `useEdgePreservingMaterial` no laço map, herdando o leak de descarte de materiais do hook. | Corrigir e aplicar o cleanup no hook `useEdgePreservingMaterial` conforme mapeado. | Backlog imediato |
| 42 | aurora-web | `src/components/hero/PuzzleGroup.tsx` | Missing prefers-reduced-motion fallback | **P2** | Montagem das peças controlada por ScrollTrigger sem fallback de movimento. | Montar as peças diretamente no ponto focal caso reduced-motion esteja ativo. | Backlog imediato |
| 43 | aurora-web | `src/components/sections/ArchitecturalProtocol.tsx` | Missing cancelAnimationFrame | **P1** | Loop de animação finito (2s) de contador numérico sem chamada de `cancelAnimationFrame` em cleanup do hook. | Armazenar o ID da request e invocar `cancelAnimationFrame(id)` no cleanup do useEffect. | Backlog imediato |
| 44 | aurora-web | `src/components/sections/CallToAction.tsx` | Missing prefers-reduced-motion fallback | **P2** | Animações de translação e entrada na chamada de ação sem fallback. | Substituir translações por fade de opacidade estático direto. | Backlog imediato |
| 45 | aurora-web | `src/components/sections/OurAnswer.tsx` | Missing prefers-reduced-motion fallback | **P2** | Entrada de conteúdo com translação espacial sem fallback de acessibilidade. | Desativar translações na entrada de conteúdo, exibindo instantaneamente. | Backlog imediato |
| 46 | aurora-web | `src/components/sections/RealityValidation.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transição de fade-in com deslocamento de blocos de texto sem fallback. | Substituir transições por fade simples sem alteração de posição. | Backlog imediato |
| 47 | aurora-web | `src/components/sections/WhatWeBuilt.tsx` | Missing prefers-reduced-motion fallback | **P2** | Efeitos de hover com escala e translação na grade sem fallback de acessibilidade. | Desabilitar efeitos de hover com translação/escala sob reduced-motion. | Backlog imediato |
| 48 | aurora-web | `src/components/SovereignHeroWebGL.tsx` | Missing prefers-reduced-motion fallback | **P2** | Renderização 3D intensa de fundo sem controle para desativar/pausar. | Interromper o loop do Canvas WebGL caso o usuário prefira movimento reduzido. | Backlog imediato |
| 49 | aurora-web | `src/components/ui/AuroraHeroScene.tsx` | ThreeJS memory leak risk | **P3** | Alerta estático devido ao uso de `THREE`, mas todos os materiais/geometrias são declarativos em JSX e limpos pelo R3F. | Falso positivo gerado pela regra estática de linter. | Monitoramento |
| 50 | aurora-web | `src/components/ui/AuroraNativeHero.tsx` | Missing prefers-reduced-motion fallback | **P2** | Transições de layout e fade com deslocamento do hero nativo sem fallback. | Exibir o layout em estado final de forma estática imediata. | Backlog imediato |
| 51 | aurora-web | `src/components/ui/hero-futuristic.tsx` | ThreeJS memory leak risk | **P1** | Instanciação de `ScannerMaterial` (TSL node material) via `useMemo` sem chamada de `.dispose()` na desmontagem. | Adicionar cleanup no useEffect/useMemo correspondente para descartar o ScannerMaterial criado. | Backlog imediato |
| 52 | aurora-web | `src/components/ui/hero-futuristic.tsx` | Missing prefers-reduced-motion fallback | **P2** | Efeito ativo de scanline e ruído constante no shader sem fallback de movimento. | Congelar o tempo do shader (`timeNode = 0`) quando `prefers-reduced-motion` for detectado. | Backlog imediato |

---

## 6. Próxima Ação Recomendada

A Micro-Etapa 3 foi concluída e o gate de parada acionado. O próximo passo da Ordem de Serviço será a **Micro-Etapa 4 — Criar Allowlist Governada**, para estruturar as exceções legítimas e intencionais de design system no arquivo `.aurora/design-lint-allowlist.json`.
