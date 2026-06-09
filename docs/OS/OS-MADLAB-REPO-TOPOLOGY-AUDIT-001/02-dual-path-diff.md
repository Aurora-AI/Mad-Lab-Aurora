# M2 — Dual-Path Diff & Artifact Reconciliation

**OS:** OS-MADLAB-REPO-TOPOLOGY-AUDIT-AND-ENVIRONMENT-RECONCILIATION-20260609-001  
**Date:** 2026-06-09

---

## Summary

The two paths are **not symmetric**. They are different things:

| Canonical (`C:\Projetos\MadLabAurora`) | Accidental (`C:\Projetos\Aurora\MadLabAurora`) |
|---|---|
| Standalone git repo | Subdirectory inside the Aurora repo |
| ~20 root-level folders | 5 items total |
| Lab environment (full structure) | Staging area only |
| Branch: `main` | Lives under Aurora `feature/purga-debt-001` |
| Remote: `Mad-Lab-Aurora.git` via `origin` | Aurora repo has `madlab` remote → same target |

There are **no duplicate files** between the two paths — they contain entirely different content.  
The accidental path is a **transfer zone artifact**, not a fork or mirror.

---

## Artifact Classification

### Items in accidental path ONLY

| Item | Classification | Action |
|---|---|---|
| `factory/OS-MADLAB-BUILD-001/` (full m1–m7) | `COPY_TO_CANONICAL` | Copy to canonical `docs/OS/OS-MADLAB-BUILD-001/` after approval |
| `factory/OS-MADLAB-INTEGRATION-001-SCOPE.md` | `COPY_TO_CANONICAL` | Integration scope doc — belongs in canonical docs |
| `docs/OS/OS-019R-SCOPE-RECONCILIATION.md` | `COPY_TO_CANONICAL` | Reconciliation record — belongs in canonical Vault/docs |
| `docs/MANUAL_DA_AGENCIA.md` | `COPY_TO_CANONICAL` | Governance doc — belongs in canonical docs |
| `product-manifest.json` | `DIVERGENT_REVIEW_REQUIRED` | Path field is wrong (`C:/Projetos/Aurora/MadLabAurora`) — must be corrected before copying |
| `project-manifest.json` | `DIVERGENT_REVIEW_REQUIRED` | Review content vs canonical `project-manifest.json` before action |
| `.playwright-mcp/` | `QUARANTINE` | Runtime sandbox artifact — do not copy, review before delete |

### Items in canonical ONLY (no corresponding accidental item)

All canonical content is **canonical-only by design**. No merging required in this direction.

---

## BUILD-001 Artifact Location Status

All BUILD-001 artifacts (`m1`–`m7`, screenshots, components, CLOSURE, PROMOTION_APPROVAL_RECORD)  
exist **only in the accidental path** (`C:\Projetos\Aurora\MadLabAurora\factory\OS-MADLAB-BUILD-001\`).

They are **not present in the canonical repo** (`C:\Projetos\MadLabAurora`).

This means the BUILD-001 work was executed inside the Aurora repo, not inside MadLabAurora.  
The factory output needs to be migrated to the canonical location before any promotion gate.

---

## Checklist

- [x] nenhuma exclusão automática
- [x] nenhuma cópia automática sem matriz
- [x] artefatos BUILD-001 localizados — `C:\Projetos\Aurora\MadLabAurora\factory\OS-MADLAB-BUILD-001\`
- [x] Vault records localizados — `docs/OS/OS-019R-SCOPE-RECONCILIATION.md` no caminho acidental
- [x] screenshots/render bundles localizados — `factory/OS-MADLAB-BUILD-001/m6/`
