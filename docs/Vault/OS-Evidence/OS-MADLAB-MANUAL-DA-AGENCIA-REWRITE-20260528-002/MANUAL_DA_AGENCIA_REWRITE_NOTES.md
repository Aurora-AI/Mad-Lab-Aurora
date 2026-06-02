# Notas de Reescrita — MANUAL_DA_AGENCIA.md

**OS ID:** `OS-MADLAB-MANUAL-DA-AGENCIA-REWRITE-20260528-002`  
**Data:** 28 de Maio de 2026  
**Status:** COMPILADO

---

## 1. Visão Geral das Modificações

O manual canônico `MANUAL_DA_AGENCIA.md` foi reescrito na versão 3.0.0 para assumir seu papel definitivo de **Constituição Central e Roteador da Pilha Documental**. 

Para evitar duplicações e assegurar uma única fonte da verdade (SSOT) no repositório, todos os detalhes puramente táticos de CSS, GLSL e especificações de tokens foram removidos do manual e roteados via links Markdown para seus respectivos sub-documentos, mantendo o manual central focado na governança criativa de alto nível, Gates de Qualidade e regras organizacionais.

---

## 2. Inventário de Remoções e Destinos (Linha de Custódia)

Abaixo estão justificadas e catalogadas todas as remoções relevantes efetuadas na reescrita:

| Conteúdo Original | Tipo de Alteração | Destino Canônico | Racional / Justificativa |
|---|---|---|---|
| **Dependências de pacotes npm** (Three.js, React R3F versions JSON) | 🔄 Movido / Roteado | `.aurora/domain-policy.json` | A especificação de dependências de software é um controle técnico de capabilities e compatibilidade de pacotes, escopo do manifesto JSON de domínio. |
| **Tokens de cores hexadecimais, opacidades e espaçamentos** | 🔄 Movido / Roteado | `docs/brand/ELYSIAN_BRAND_KIT_v1.1.md` | O Brand Kit Elysian é a única fonte da verdade (SSOT) corporativa para tokens de design de cores, opacidades e grids padrão. |
| **Três Vozes Tipográficas, seletores e tamanhos de fonte pós-hero** | 🔄 Movido / Roteado | `.agents/rules/designmanualposthero.md` | Os tamanhos de headlines, fontes monospace (Voz 2) e serifa display pós-hero são diretrizes táticas de composição de tela abaixo da dobra. |
| **Modelos de layout pós-hero** (Split vertical, Pinned layout e Grid de Diagnóstico) | 🔄 Movido / Roteado | `.agents/rules/designmanualposthero.md` | Pertencem ao escopo tático de interfaces abaixo da dobra, e não à constituição filosófica geral. |
| **Estrutura de pastas da library e Anatomy WebGL** | 🔄 Movido / Roteado | `docs/Vault/DESIGN_LIBRARY.md` | O catálogo físico de assets e a documentação técnica de Shaders (vertex/fragment) representam a biblioteca operacional de craft do desenvolvedor. |
| **Massa de colagens e referências a sites (Aino, Exo Ape, Lusion)** | 🔄 Movido / Roteado | `docs/Vault/OS-Evidence/OS-MADLAB-DOC-STACK-PREPARATION-20260528-001/DOC_STACK_INVENTORY.md` | As referências de terceiros foram declaradas fora do escopo normativo de autoridade criativa e catalogadas no inventário documental como corpus de inspiração. |

---

## 3. Invariantes Preservados (Intocáveis)

As seguintes lógicas centrais da Aurora foram preservadas em sua integridade de significados no manual constitucional:
*   **Camada Criativa:** A definição clara de que o Mad Lab Aurora não é um vertical, mas sim a camada criativa e de craft que apoia e governa as decisões visuais dos verticais abaixo dele.
*   **Regra Absoluta:** O lema de genericidade zero ("Não parecer IA").
*   **Os Dois Mundos:** A co-existência de autoridade e peso idênticos entre o luminoso (off-white, ar, Da Vinci) e o dark (tensão, máquina, Sabbath).
*   **A Física Visual Progressiva:** O Z-axis impossível e a luz em GPU continuam como a ambição máxima (linha de chegada) a ser alcançada à medida que as páginas evoluem de landing pages simples para sistemas complexos.
*   **Orçamento de Performance:** O target de 60fps em hardware mobile mediano e o repouso de silêncio de 0.8s antes de animações.
*   **Os Gates Criativos:** O papel supervisor de design e efeitos exercidos por `CEO-Design` e `CEO-Effects`.
