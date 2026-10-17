# Cinematic Synthesis Engine

O Synthesis Engine é o template e o protocolo operacional que permite aos agentes compilarem uma lista de primitivas selecionadas em especificações técnicas executáveis e integradas.

---

## 1. Processo de Síntese

Ao receber um briefing visual, o agente deve seguir este fluxo de síntese:

1. **Análise de Frequência e DNA:** Selecionar 1 primitiva principal de cada dimensão relevante no catálogo de primitivas.
2. **Definição de Restrições:** Verificar limites de performance (`performance_budget`) e restrições de acessibilidade (`prefers_reduced_motion`).
3. **Consolidação de Espec:** Fundir as propriedades das primitivas (por exemplo, combinar o easing do `MOT-002` com o timing e delays do `NAR-001`).
4. **Geração do Output:** Produzir o documento estruturado conforme o template abaixo.

---

## 2. Template do Synthesis Report

```markdown
# Cinematic Synthesis Report — [Nome do Componente/Seção]

## 1. Primitivas Selecionadas
- **Motion:** [ID] - [Nome]
- **Camera:** [ID] - [Nome]
- **Composition:** [ID] - [Nome]
- **Lighting:** [ID] - [Nome]
- **Interaction:** [ID] - [Nome]
- **Atmosphere:** [ID] - [Nome]
- **Transition:** [ID] - [Nome]
- **Narrative:** [ID] - [Nome]

## 2. Storyboard Narrativo
- **Fase 1 — Silêncio e Peso (0.0s - 0.8s):** [Ação conceitual respeitando NAR-001]
- **Fase 2 — Emergência e Revelação (0.8s - 2.5s):** [Como a câmera e o movimento principal entram em cena]
- **Fase 3 — Foco e Interação (2.5s+):** [Como o usuário interage e como a atmosfera reage]

## 3. Motion & GSAP Spec (Executável)
- **Timeline:** [Estrutura de encadeamento GSAP]
- **Código/Parâmetros:**
  ```javascript
  // Configuração canônica GSAP
  gsap.timeline({
    scrollTrigger: {
      trigger: "[seletor]",
      start: "top 85%",
      end: "top 20%",
      scrub: false
    }
  })
  // [Adicionar staggers e easings baseados em MOT/TRN/INT]
  ```

## 4. WebGL / Three.js Spec (se aplicável)
- **Câmera & Lente:** [Configuração baseada em CAM]
- **Iluminação & Sombras:** [Configuração baseada em LGT]
- **Shaders / Noise:** [Configuração baseada em ATM/TRN]
- **Performance Budget:** [Frame rate e draw call limits]

## 5. Art Direction Prompt (Geração de Assets)
- **Prompt (EN):** [Prompt técnico para Midjourney/Stable Diffusion baseado nas primitivas de luz/matéria]
- **Negative Prompt (EN):** [Negative prompt baseado nas regras do DNA]
- **Fallback:** [Qual o fallback estático/CSS?]

## 6. Acessibilidade (Reduced Motion)
- **Comportamento Alternativo:** [Como as primitivas se comportam se prefers-reduced-motion for true]
```
