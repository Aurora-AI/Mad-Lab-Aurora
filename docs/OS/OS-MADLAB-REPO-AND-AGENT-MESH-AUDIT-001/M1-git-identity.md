# M1 — Git / Path Identity

**OS:** OS-MADLAB-REPO-AND-AGENT-MESH-AUDIT-001  
**Date:** 2026-06-09  
**Method:** Direct shell execution (not delegated — deterministic commands)

---

## Git Identity

| Field | Value |
|---|---|
| Remote origin | https://github.com/Aurora-AI/Mad-Lab-Aurora.git |
| Active branch | docs/os-topology-audit-and-repo-analysis |
| Main branch | main (origin/main @ 1071b93) |
| Working tree | CLEAN — zero uncommitted changes |
| Tracked files | 1,697 |

## Ignored Content (local-only, not part of repo)

Categories present on disk but excluded by .gitignore:
- `node_modules/` (all subdirectories)
- `dist/` (aurora-web/dist 33 MB, ElysianCorp/dist 29 MB)
- `.playwright-mcp/` (Playwright capture logs)
- `.pytest_cache/`
- `.vscode/settings.json`
- `.claude/settings.local.json`
- `*.log` files (service logs in AuroraCognitiveAssets OS-Evidence)
- `aurora-visual-assets/node_modules/`

## Canonical Path Confirmed

```
C:\Projetos\MadLabAurora  ← SSOT
```

Scripts use this path. Only README.md still references the old location.

## Correction to Prior Audit

The previous analysis mixed local-ignored content with tracked repo content.
This audit uses only `git ls-files` output as ground truth.
