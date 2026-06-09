# OS-MADLAB-REPO-HARDENING-001 — M6: Workflow Architecture — Visual Synthesis Pipeline

**Data:** 2026-06-09  
**Etapa:** M6 de 6  
**Status:** FORMALIZADO  
**Autoridade:** Rodrigo Cesar Winhaski

---

## Mad Lab Visual Synthesis Workflow

Versão canônica do pipeline de produção visual do Mad Lab Aurora.  
Define papéis, responsabilidades, e o ponto de entrada de cada tecnologia.

---

## Os 9 Estágios

```
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1 — Intake & Routing                                     │
│  Responsável: Álvaro (Router/Delegator)                         │
│  Input: brief criativo, referências, objetivo de negócio        │
│  Output: roteamento para stage correto + contexto empacotado    │
│  REGRA: Álvaro APENAS roteia. Não decide estética.              │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2 — Current State Analysis                               │
│  Responsável: agente de análise (Mad Lab)                       │
│  Input: codebase atual, design tokens, componentes existentes   │
│  Output: mapa de estado atual com gaps identificados            │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3 — Human Direction                                      │
│  Responsável: Rodrigo Cesar Winhaski (humano)                   │
│  Input: mapa de estado atual + brief                            │
│  Output: direção criativa explícita (escrita, aprovada)         │
│  GATE HARD: sem direção humana, pipeline para.                  │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4 — Reference Intelligence                               │
│  Responsável: agente de pesquisa (Mad Lab)                      │
│  Input: direção criativa do Stage 3                             │
│  Output: referências visuais curadas, moodboard contextualizado │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 5 — Art Direction Synthesis                              │
│  Responsável: agente de síntese (Mad Lab)                       │
│  Input: referências do Stage 4 + direção do Stage 3             │
│  Output: art direction document (tokens, paleta, tipografia,    │
│          motion principles, component anatomy)                  │
│  NOTA: síntese, não criação autônoma. Baseada em human input.   │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 6 — Open Design Assembly                                 │
│  Responsável: integrations/open-design (Design Assembly Runtime)│
│  Input: art direction document do Stage 5                       │
│  Output: artefatos de design montados (Figma, tokens JSON,      │
│          component specs, motion specs)                         │
│  CONTRATO: veja seção "Contrato integrations/open-design"       │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 7 — Implementation Blueprint                             │
│  Responsável: agente de implementação (Mad Lab)                 │
│  Input: artefatos do Stage 6                                    │
│  Output: blueprint técnico (componentes TSX, hooks, tokens TS)  │
│  NOTA: blueprint apenas — implementação não ocorre aqui.        │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 8 — Human Approval Gate                                  │
│  Responsável: Rodrigo Cesar Winhaski (humano)                   │
│  Input: blueprint técnico + artefatos de design                 │
│  Output: aprovação explícita por escrito                        │
│  GATE HARD: implementação NUNCA começa sem aprovação humana.    │
└─────────────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 9 — Production Execution & Certification                 │
│  Responsável: agente de produção (Mad Lab) + QA gate            │
│  Input: blueprint aprovado                                      │
│  Output: código produção + Promotion Package (se aprovado)      │
│  NOTA: promotion_allowed somente após QA gate APPROVED.         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Contrato — integrations/open-design (Stage 6)

**Papel:** Design Assembly Runtime  
**Path no repo:** `integrations/open-design/`  
**Função:** Recebe art direction document e monta artefatos de design consumíveis pelo pipeline de implementação.

### O que integrations/open-design PODE fazer

| Ação | Autorizado |
|---|---|
| Montar tokens JSON a partir de art direction | ✅ |
| Gerar component specs (anatomy, states, variants) | ✅ |
| Exportar motion specs (durations, easings, sequences) | ✅ |
| Produzir Figma-ready structures | ✅ |
| Consumir direção criativa humana (Stage 3) | ✅ |

### O que integrations/open-design NÃO PODE fazer

| Ação | Proibido | Motivo |
|---|---|---|
| Decidir direção de arte autonomamente | ❌ | Stage 3 é gate humano |
| Escolher estética sem input do Stage 3 | ❌ | Violaria soberania criativa |
| Escrever código de implementação | ❌ | Stage 9 é responsabilidade separada |
| Avaliar qualidade final | ❌ | Stage 8 é gate humano |
| Aprovar seu próprio output | ❌ | Sem auto-aprovação |
| Promover artefatos para repo soberano | ❌ | Requer PromotionApprovalRecord |

### Interface de Entrada/Saída

```
INPUT (Stage 5 → Stage 6):
  art-direction-document.md ou art-direction-document.json
  Contém: color palette, typography scale, motion principles,
          component anatomy, spatial system, brand voice tokens

OUTPUT (Stage 6 → Stage 7):
  tokens/                  ← design tokens JSON
  component-specs/         ← anatomy + states + variants
  motion-specs/            ← durations, easings, sequences
  design-review-notes.md   ← observações para Stage 8
```

---

## Papel de Álvaro — Definição Canônica

**Álvaro é Router/Delegator. Nada mais.**

### Álvaro PODE

- Receber brief e contexto
- Rotear para o stage correto
- Empacotar contexto para agentes downstream
- Comunicar status entre stages

### Álvaro NUNCA FAZ

| Ação Proibida |
|---|
| Decidir direção de arte |
| Escolher estética |
| Escrever código visual |
| Avaliar qualidade final de design |
| Recriar runtime do Álvaro em outra ferramenta |
| Operar gateway MCP próprio |
| Instanciar Qdrant paralelo |
| Executar auto-healing produtivo |

**Fonte:** `.aurora/domain-policy.json` + DEC-MADLAB-PRODUCT-WORKSPACE-BOUNDARY-001

---

## Gates Obrigatórios

| Gate | Stage | Quem aprova |
|---|---|---|
| Human Direction | Stage 3 | Rodrigo Cesar Winhaski |
| Human Approval | Stage 8 | Rodrigo Cesar Winhaski |
| QA Gate | Stage 9 | qa-review (APPROVED ou APPROVED WITH CAVEATS) |
| Promotion Gate | Pós Stage 9 | PromotionApprovalRecord assinado |

Nenhum gate pode ser pulado. "Está quase pronto" não é aprovação.

---

## Status de implementação de integrations/open-design

```
current_state:   CONTRATO_FORMALIZADO
runtime_ready:   false
stage_6_active:  false
blocker:         OS-MADLAB-INTEGRATION-001 (congelada)
next_action:     aguardar descongelamento de INTEGRATION-001
```

`integrations/open-design` existe como ponto de contrato arquitetural.  
Implementação runtime só inicia após aprovação explícita de INTEGRATION-001.

---

## Encerramento M6

Com M6 concluído, os 6 micro-etapas de OS-MADLAB-REPO-HARDENING-001 estão documentados:

| Etapa | Status |
|---|---|
| M1 — Git Identity | ✅ (registrado em OS-MESH-AUDIT) |
| M2 — Product Workspace Boundary | ✅ DEC-MADLAB-PRODUCT-WORKSPACE-BOUNDARY-001 |
| M3 — Dependency Hardening | ✅ requirements.txt + pyproject.toml |
| M4 — Production Readiness Findings | ✅ 4 findings registrados (PRF-001 a PRF-004) |
| M5 — Accessibility Certification | ✅ 2 gaps identificados (ACF-001, ACF-002) |
| M6 — Workflow Architecture | ✅ Este documento |

**OS-MADLAB-REPO-HARDENING-001: DOCUMENTAÇÃO COMPLETA**  
Próximo: OS-MADLAB-INTEGRATION-001 (congelada — aguarda decisão de descongelamento)
