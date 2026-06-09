# M1 — Repository Identity Preflight

**OS:** OS-MADLAB-REPO-TOPOLOGY-AUDIT-AND-ENVIRONMENT-RECONCILIATION-20260609-001  
**Date:** 2026-06-09  
**Author:** Audit execution

---

## Canonical Path

| Field | Value |
|---|---|
| Path | `C:\Projetos\MadLabAurora` |
| `git rev-parse --show-toplevel` | `C:/Projetos/MadLabAurora` |
| Branch | `main` |
| Remote `origin` | `https://github.com/Aurora-AI/Mad-Lab-Aurora.git` |
| Git status | `m ElysianCorp` / `?? open-design/` |
| Verdict | **CANONICAL REPO — has own `.git`** |

### Root structure (canonical)

```
.agents/          .aurora/         .claude/         .fallow/
.git/             .gitignore       .pytest_cache/   .vscode/
AGENTS.md         AuroraCognitiveAssets/
Banco de Texturas/  ElysianCorp/   GEMINI.md        README.md
Referências/      WebGL-Scroll-Sync-main/
aurora-agents/    aurora-visual-assets/  aurora-web/
checkouts/        conductor/       creative-area-manifest.json
docs/             integrations/    open-design/
project-manifest.json  scratch/    scripts/
```

---

## Accidental Path

| Field | Value |
|---|---|
| Path | `C:\Projetos\Aurora\MadLabAurora` |
| `git rev-parse --show-toplevel` | `C:/Projetos/Aurora` ← **AURORA repo root** |
| Branch (Aurora repo) | `feature/purga-debt-001` |
| Remote `origin` (Aurora repo) | `https://github.com/Aurora-AI/Aurora.git` |
| Remote `madlab` (Aurora repo) | `https://github.com/Aurora-AI/Mad-Lab-Aurora.git` |
| Verdict | **NOT a separate repo — is a subdirectory inside the Aurora repo** |

### Root structure (accidental — 5 items only)

```
.playwright-mcp/
docs/
factory/
product-manifest.json
project-manifest.json
```

---

## Critical Finding

`C:\Projetos\Aurora\MadLabAurora` is **NOT a clone or competing copy** of the MadLab repo.  
It is a **staging/transfer subdirectory** created inside the Aurora repo (`C:\Projetos\Aurora`)  
while the Aurora repo was on branch `feature/purga-debt-001`.

The Aurora repo's `madlab` remote points to Mad-Lab-Aurora.git — this was the mechanism for  
cross-repo artifact staging. The subdirectory contains:
- `factory/OS-MADLAB-BUILD-001/` — complete BUILD-001 artifact set (m1–m7, screenshots, components)
- `factory/OS-MADLAB-INTEGRATION-001-SCOPE.md` — integration scope doc (frozen)
- `docs/OS/OS-019R-SCOPE-RECONCILIATION.md` — OS-019R reconciliation record
- `docs/MANUAL_DA_AGENCIA.md` — agency manual
- `product-manifest.json` — classifies MadLabAurora as `creative-branch` with path pointing to accidental location

The `product-manifest.json` contains `"path": "C:/Projetos/Aurora/MadLabAurora"` — this is the path error.

---

## Checklist

- [x] repo canônico identificado — `C:\Projetos\MadLabAurora`
- [x] caminho errado classificado — subdirectório dentro do repo Aurora, não clone separado
- [x] branch/remotes documentados — ambos os caminhos
- [x] git status dos dois caminhos registrado
- [x] nenhuma movimentação feita
