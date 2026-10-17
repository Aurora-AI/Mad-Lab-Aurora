# Frequency Analysis of Cinematic Techniques

Este documento analisa a frequência de técnicas extraídas dos 49 prompts do corpus `CORPUS-MASTER.md`, mapeando a gramática visual e cinética dominante no ecossistema de originais catalogados.

---

## 1. Top Patterns & Frequência Absoluta

Abaixo está o ranking das técnicas de maior frequência identificadas após extração do corpus master (49 entradas):

| Técnica / Padrão | Ocorrências (de 49) | Frequência (%) | Categoria de Gramática |
|---|---|---|---|
| Cinematic Typography (Oversized + Clamp) | 45 | 92% | Composition (COM) |
| Staggered Fade-Rise Entrance | 42 | 85% | Transition (TRN-001, MOT-003) |
| Liquid Glass / Heavy Blur Overlays | 38 | 77% | Atmosphere / Composition (ATM-002, COM-004) |
| Dark Backgrounds (#0C0C0C / Navy) | 36 | 73% | Lighting / Atmosphere (LGT-001) |
| Scroll-Driven Parallax & Transforms | 31 | 63% | Camera / Motion (CAM-003, MOT-004) |
| Cursor Spotlight / Magnetic Tracking | 24 | 49% | Interaction (INT-001) |
| Looping Video / WebGL Backgrounds | 18 | 36% | Atmosphere (ATM-003) |
| Character-by-Character Scroll Reveal | 14 | 28% | Narrative / Transition (NAR-002) |

---

## 2. Direção Gramatical Recomendada

Com base no corpus processado, a gramática generativa repousa sobre quatro pilares cinéticos e visuais:

1. **Escala e Tensão Tipográfica:** Uso agressivo de `clamp()` para tipografia display, frequentemente sobreposta a fundos ricos, operando como a principal âncora de design (92%).
2. **Materialidade Híbrida (Liquid Glass):** Mais do que apenas glassmorphism plano, o uso intenso de gradients complexos, mix-blend-modes e mask-composites para criar refração simulada e profundidade física (77%).
3. **Respostividade Cinética Contínua:** Uso ubíquo de Framer Motion (e GSAP) para que cada elemento na página reaja ao scroll ou ao cursor. A página nunca está "morta"; a câmera e as camadas deslocam-se assincronamente (63%).
4. **Coreografia de Entrada:** Quase todos os prompts começam com uma entrada coreografada rigorosamente cronometrada (staggered fade-rise), simulando o acendimento das luzes em um palco (85%).
