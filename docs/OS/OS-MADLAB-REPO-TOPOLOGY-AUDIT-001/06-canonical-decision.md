# M6 — Canonical Closure & Next Decision

**OS:** OS-MADLAB-REPO-TOPOLOGY-AUDIT-AND-ENVIRONMENT-RECONCILIATION-20260609-001  
**Date:** 2026-06-09

---

## Audit Summary

### Findings

| # | Finding | Severity |
|---|---|---|
| 1 | BUILD-001 artifacts generated inside Aurora repo, not canonical MadLab | HIGH |
| 2 | `product-manifest.json` path points to wrong location | HIGH |
| 3 | No transfer zone exists in canonical repo | MEDIUM |
| 4 | Aurora repo has `madlab` remote — created ambiguity | MEDIUM |
| 5 | Motion components (3 hooks) absent from canonical ElysianCorp | MEDIUM |
| 6 | QA gate records absent from canonical (scripts exist but no formal records) | LOW |
| 7 | `playground/` not formalized (scratch/ serves partial function) | LOW |

### What is correct

- Canonical repo `C:\Projetos\MadLabAurora` is the SSOT — confirmed own `.git`, branch `main`, `origin → Mad-Lab-Aurora.git`
- Vault and OS Evidence system is functional — 20+ evidence files
- Token Ledger is functional — dated entries
- Design system (ElysianCorp) is a full Astro project
- BUILD-001 quality is valid — all gates passed, `REVIEWABLE_CANDIDATE`
- No Aurora package coupling found in dependencies

### What is not correct

- BUILD-001 exists in the wrong repo
- product-manifest.json embeds the wrong path
- No migration has occurred yet

---

## Decision

Based on audit evidence, the next OS is:

**Option E: OS-MADLAB-REPO-HARDENING-001 before integration**

Rationale:
- BUILD-001 artifacts must migrate to canonical before integration can proceed
- product-manifest.json must be corrected
- Transfer zone must be established
- Motion components must be placed in canonical ElysianCorp
- Only after hardening is complete can OS-MADLAB-INTEGRATION-001 be opened safely

Options A–D from the plan are not selected:
- A (fix structure before product) — partially correct, but not granular enough
- B (migrate BUILD-001) — this is a sub-task of hardening, not an OS on its own
- C (reject BUILD-001) — NOT correct: BUILD-001 is valid, not rejected
- D (open INTEGRATION-001) — NOT ready: canonical state is not clean

---

## OS Status Registry

| OS | Status |
|---|---|
| OS-019R | CONCLUÍDA |
| OS-MADLAB-BUILD-001 | FECHADA — REVIEWABLE_CANDIDATE |
| OS-MADLAB-REPO-TOPOLOGY-AUDIT-001 | CONCLUÍDA (this document) |
| OS-MADLAB-INTEGRATION-001 | CONGELADA |
| **OS-MADLAB-REPO-HARDENING-001** | **PRÓXIMA OS** |

---

## OS-MADLAB-REPO-HARDENING-001 Scope (to be opened)

Objectives:
1. Migrate `C:\Projetos\Aurora\MadLabAurora\factory\` → `C:\Projetos\MadLabAurora\docs\OS\` (with reconciliation matrix approval)
2. Migrate docs from accidental path to canonical
3. Correct `product-manifest.json` path field
4. Establish `transfer/ready/` and `transfer/rejected/` zones in canonical
5. Place BUILD-001 motion hooks into canonical `ElysianCorp/`
6. Remove MadLabAurora subdirectory from Aurora repo (after migration verified)
7. Document Aurora repo `madlab` remote — decide if it should be removed or retained

---

## Frase Canônica

> Antes de promover o tema, precisamos provar que o laboratório está no lugar certo, íntegro e governado.  
> O laboratório está funcionalmente governado mas fisicamente no lugar errado.  
> A próxima OS o move para o lugar certo.
