---
name: cinematic-grammar
version: 1.0.0
status: deprecated
deprecated: true
deprecated_by: OS-MADLAB-AGENTIC-PIVOT-20261016-001
updated: 2026-10-16
description: Skill de infraestrutura criativa transversal que define a gramática cinematográfica e cinética para o Mad Lab Aurora. Organiza técnicas e efeitos em primitivas reutilizáveis que alimentam os agentes de Art Direction, Design e Effects.
classification: A - S-Tier
domain: creative-grammar
---

# Cinematic Grammar

Esta skill funciona como o **repertório canônico e estruturado** de primitivas cinéticas e cinematográficas do Mad Lab Aurora. Ela descontrói efeitos complexos em 8 dimensões analíticas reutilizáveis, garantindo que os agentes gerem interfaces com peso físico, intenção narrativa e rigor técnico.

---

## 1. As 8 Dimensões da Gramática

Qualquer cena, hero, animação ou interação no ecossistema Aurora deve ser expressa como uma combinação de primitivas nas seguintes dimensões:

1. **Motion (Movimento):** Dinâmica de movimentação de objetos geométricos ou partículas.
2. **Camera (Câmera):** Enquadramento virtual, foco (DOF), lentes e deslocamento de perspectiva.
3. **Composition (Composição):** Organização espacial, divisores, eixos e grids pós-hero.
4. **Lighting (Iluminação):** Estilo de luz, contraste (chiaroscuro), feixes e temperatura.
5. **Interaction (Interação):** Resposta cinética a estímulos do visitante (mouse, scroll, hover).
6. **Atmosphere (Atmosfera):** Textura de fundo, grão analógico, névoa e densidade visual.
7. **Transition (Transição):** Fluxos de entrada de elementos e mudança de contextos de página.
8. **Narrative (Narrativa):** Ritmo de entrega da informação, regra do silêncio e pacing cênico.

---

## 2. Contrato de Schema de Primitiva (YAML)

Todas as primitivas armazenadas em `primitives/{dimensao}.md` devem seguir o seguinte schema:

```yaml
- id: [DIM]-[SEQ]              # ex: MOT-001, CAM-002
  name: [Nome da Primitiva]
  dimension: [Nome da dimensão]
  intent: [Qual o objetivo cognitivo/narrativo?]
  emotion: [[vetor de emoções]]  # ex: [suspense, authority, precision]
  cost: [low | medium | high]
  mobile: [allowed | restricted | reduced]
  anti_ai_score: [1-10]          # Medida de complexidade e craft humano
  dna_status: [approved | rejected | conditional]
  dna_condition: "[Condição de uso de acordo com o DNA Visual]"
  anti_pattern: "[Como esta técnica se torna barata ou clichê]"
  references: [[arquivos de referência ou links]]
  source_assets: [[IDs dos assets que usam esta técnica]]
  gsap_spec: "[Especificações de timing, curves e easing GSAP]"
  three_js_config: "[Especificações WebGL/Three.js se aplicável]"
  performance_budget: "[Budget de frame rate e GPU]"
  prefers_reduced_motion: "[Comportamento alternativo para acessibilidade]"
```

---

## 3. Protocolo de Extração (`/extract-grammar`)

O comando `/extract-grammar` é executado pelo agente para ingerir referências externas ou prompts brutos e catalogá-los em primitivas reutilizáveis.

### Sintaxe do Comando
```text
/extract-grammar --source [url_ou_nome] --prompt [conteudo_do_prompt_ou_referencia]
```

### Fluxo de Execução
Ao receber o comando, siga rigidamente estes passos:

1. **Persistência Raw:** 
   - Salve o prompt original em `.aurora/skills/cinematic-grammar/raw-vault/MS-[SEQ].md` (ex: `MS-001.md` para MotionSites).
   - O cabeçalho do arquivo deve conter:
     ```yaml
     ---
     source: [source_name]
     url: [url_da_fonte]
     date_collected: [AAAA-MM-DD]
     tags: [[tags]]
     ---
     ```

2. **Decomposição e Filtro:**
   - Extraia as técnicas descritas no prompt nas 8 dimensões.
   - Para cada técnica identificada, cruze com o arquivo `references/dna-filter.md`:
     - **Se APROVADO:** Mapear para uma primitiva existente ou estruturar uma nova com `dna_status: approved`.
     - **Se REJEITADO:** Descartar a técnica e registrar a justificativa no log do chat.
     - **Se CONDICIONAL:** Adicionar a técnica com `dna_status: conditional` e explicitar os parâmetros obrigatórios em `dna_condition`.

3. **Gravação no Catálogo:**
   - Adicione a nova primitiva formatada em YAML ao final do arquivo `.aurora/skills/cinematic-grammar/primitives/{dimensao}.md` correspondente.
   - Mantenha a ordenação incremental de IDs (`MOT-004`, `CAM-004`, etc.).

4. **Atualização de Frequência:**
   - Inspecione a primitiva criada e incremente o contador no arquivo `references/frequency-analysis.md` se aplicável.


---

## 4. Protocolo de Síntese

Para compor um novo spec técnico a partir de primitivas:

1. **Seleção:** Escolher 1-2 primitivas por dimensão de acordo com o briefing cromático e a temperatura exigida para a seção.
2. **Geração de Storyboard:** Descrever a evolução visual da seção ao longo do tempo ou scroll.
3. **Geração de Specs:** Consolidar as especificações técnicas (`gsap_spec`, `three_js_config`, `performance_budget`) em um formato legível por `ceo-effects` e `site-builder`.
