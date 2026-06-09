# Human Review Package — OS-019 / M4.1
## Mad Lab Theme — Z-Axis Tunnel Candidate (Reprocessado)

**Status:** `REVIEWABLE_CANDIDATE`
**Micro-etapa:** OS-019-M4.1
**Data:** 2026-06-08
**Branch:** `feature/purga-debt-001`

---

## ⚠️ Histórico de Revisão

| Revisão | Resultado | Motivo |
|---|---|---|
| M4 (primeira) | **REPROVADO** | RAW_HTML_RENDER — screenshot sem CSS aplicado |
| M4.1 (esta) | **Pendente** | CSS bundle corrigido, Style Integrity Gate passou |

---

## ⚠️ Instrução de Promoção

```
promotion_allowed: false
promotion_authorized: false
requires_promotion_approval_record: true
promotion_eligibility: HUMAN_REVIEW_REQUIRED
```

---

## O que foi corrigido em M4.1

| Problema M4 | Correção |
|---|---|
| Sem CSS — text-5xl, tracking, spacing | CSS bundle completo (24 classes obrigatórias) |
| AuroraButton = botão browser default | button reset + aurora-button styling |
| LayerPortal sem profundidade visual | aurora-layer-hero/mid/far: scale+opacity por Z |
| ZAxisScrollContainer sem perspectiva | perspective: 1200px + flex centrado |
| Space Grotesk não carrega offline | System font stack (Segoe UI / sans-serif) |
| HTML genérico sem Z-axis | Gerador HTML Z-axis aware (build_os019_html) |

---

## Screenshot

**Arquivo:** `8_rendered_screenshot.png`
**SHA256:** `18b03df1087a7c1766c193096ae0b389b123346238a2e6ab9cad0510247b873c`
**Viewport:** 1440×900 — Playwright offline

---

## Estrutura do Candidato

| Componente | CSS Class | Z | Scale | Opacity | Conteúdo |
|---|---|---|---|---|---|
| ZAxisScrollContainer | aurora-zaxis-container | root | — | — | perspective: 1200px |
| LayerPortal (hero) | aurora-layer-hero | z=0 | 1.0 | 1.0 | "Mad Lab Aurora" + CTA |
| LayerPortal (mid) | aurora-layer-mid | z=-800 | 0.85 | 0.8 | Narrativa |
| LayerPortal (far) | aurora-layer-far | z=-2000 | 0.6 | 0.5 | "Depth Horizon" |

---

## Contraste de Cores (WCAG AA)

| Token | Valor | Sobre | Contraste |
|---|---|---|---|
| text-primary | #0A0A0A | base-surface #FAFAF8 | ~19:1 ✓ |
| text-secondary | #555555 | base-surface #FAFAF8 | ~7.2:1 ✓ |
| editorial-warm | #7A6A52 | base-surface #FAFAF8 | 5.01:1 ✓ |

---

## Perceptual QA

| Métrica | Valor |
|---|---|
| Score | 100.0% |
| Decisão | approved |
| Style Integrity Gate | PASSED |
| Gate Matrix | 24/24 |

---

## Hashes para PromotionApprovalRecord

```json
{
  "screenshot_sha256": "18b03df1087a7c1766c193096ae0b389b123346238a2e6ab9cad0510247b873c",
  "qa_report_sha256":  "cecf5d6593c48685311ce0425600d172a86bdb2ae1706bb80316c07bb5c35743",
  "approved_by": "<nome do revisor>",
  "approval_source": "signed_file"
}
```

---

## Status Canônico

```
OS-019 — CANDIDATO REVISÁVEL REPROCESSADO (M4.1)
CSS: completo — Style Integrity Gate PASSED
Perceptual: approved / 100.0%
Promoção: BLOQUEADA — aguardando PromotionApprovalRecord
promotion_allowed: false
promotion_authorized: false
```
