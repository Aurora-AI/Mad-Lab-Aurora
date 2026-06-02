# Originality Transmutation Policy

## Objective
Prevent direct visual, textual, structural, brand, and asset copying while preserving reusable abstract design knowledge. A governança criativa garante que o sistema atue como analista forense e transmutador, nunca como copiador.

## Allowed Extraction
- layout ratios
- spacing philosophy
- typographic hierarchy
- motion grammar
- interaction patterns
- component behavior
- accessibility behavior
- performance budgets
- neutral colors (e.g. #FFFFFF, #000000, common grays)

## Forbidden Copy
- logos
- brand names
- exact marketing copy
- near-identical marketing copy
- preserved brand-specific wording patterns
- exact color identity when distinctive
- exact iconography
- proprietary assets
- exact composition match
- source-specific component names
- source-specific CSS class names
- exact layout fingerprint above similarity threshold
- exact timing/easing sequence above similarity threshold
- asset hash match
- remote asset reference reuse
- unchanged visual hierarchy when source is distinctive
- unchanged hero/call-to-action structure when source is distinctive
- copied CSS/JS bundles
- copied animation timelines

## Required Transformation Axes
Each extracted pattern must be transformed across multiple dimensions to ensure originality. The supported axes are:
- semantic
- visual
- structural
- motion
- brand
- interaction

### Transmutation Thresholds
- **Padrão comum:** mínimo 2 eixos.
- **Padrão distintivo:** mínimo 3 eixos.
- **Padrão altamente reconhecível:** mínimo 4 eixos ou bloqueio.

## Severity & Outcome Matrix
| Finding | Severity | Outcome |
| :--- | :---: | :--- |
| Logo/asset original reutilizado | P0 | block |
| Nome/marca original na saída | P0 | block |
| Texto idêntico ou quase idêntico | P0/P1 | block |
| Layout fingerprint muito próximo | P1 | pause/block |
| Motion timeline idêntica | P1 | pause/block |
| Paleta distintiva copiada | P1 | transform/block |
| Cor neutra igual | P3 | allow |
| Ratio/layout genérico similar | P3 | allow com nota |
