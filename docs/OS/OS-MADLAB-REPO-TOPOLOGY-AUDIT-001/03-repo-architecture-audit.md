# M3 — MadLabAurora Repo Architecture Audit

**OS:** OS-MADLAB-REPO-TOPOLOGY-AUDIT-AND-ENVIRONMENT-RECONCILIATION-20260609-001  
**Date:** 2026-06-09

---

## Repo Root Inventory

| Folder / File | Present | Notes |
|---|---|---|
| `.agents/` | ✓ | Agent configuration |
| `.aurora/` | ✓ | Aurora cognitive layer config |
| `.claude/` | ✓ | Claude Code settings |
| `.fallow/` | ✓ | Fallow/inactive area |
| `.git/` | ✓ | Canonical — own repo |
| `AGENTS.md` | ✓ | 7469 bytes — agent governance |
| `GEMINI.md` | ✓ | 8700 bytes — Gemini governance |
| `README.md` | ✓ | 689 bytes |
| `project-manifest.json` | ✓ | Skills list, project metadata |
| `creative-area-manifest.json` | ✓ | Creative area registry |
| `scripts/` | ✓ | `design-system-lint.ps1`, `hydration-integrity-check.js`, `validate-configs.ps1` |

## Key Subdirectories

| Subdirectory | Present | Assessment |
|---|---|---|
| `docs/Vault/` | ✓ | Has OS-Evidence, Token-Ledger, Decisions, KIs, Threads, Raw, Processed, Deltas, vault_manifest.json |
| `docs/OS/` | ✓ | OS records (this audit is written here) |
| `docs/brand/` | ✓ | Brand specs |
| `docs/specs/` | ✓ | Specifications |
| `ElysianCorp/` | ✓ | Astro project — full design system candidate with `src/`, `package.json`, `tailwind.config.mjs`, motion system, scripts |
| `aurora-web/` | ✓ | Vite/React project — has `src/`, `package.json`, Vercel config, Firebase config |
| `aurora-agents/` | ✓ | Agent definitions |
| `aurora-visual-assets/` | ✓ | Visual assets store |
| `AuroraCognitiveAssets/` | ✓ | Cognitive asset collection |
| `conductor/` | ✓ | Orchestration layer |
| `integrations/` | ✓ | Contains `open-design/` |
| `checkouts/` | ✓ | Checkout zone |
| `scratch/` | ✓ | Scratch/experimental area |
| `Referências/` | ✓ | Reference materials |
| `Banco de Texturas/` | ✓ | Texture bank |
| `WebGL-Scroll-Sync-main/` | ✓ | WebGL experiment |

## Expected Governance Structure vs Reality

| Expected | Present | Status |
|---|---|---|
| `vault/` (governance vault) | ✓ (as `docs/Vault/`) | PRESENT — different casing/path |
| OS Evidence | ✓ (`docs/Vault/OS-Evidence/`) | PRESENT |
| Skills | ✓ (`project-manifest.json` skills list) | PRESENT — via manifest, not folder |
| Scripts / gates | ✓ (`scripts/`) | PRESENT — 3 validation scripts |
| Design system | ✓ (`ElysianCorp/`) | PRESENT — full Astro project |
| Motion system | ✓ (`ElysianCorp/elysian-motion/`) | PRESENT |
| `transfer/` zone | ✗ | **ABSENT** — no explicit transfer/ready or transfer/rejected |
| `playground/` | ✗ | **ABSENT** — exploration done in `scratch/` |
| `governance/configs` | Partial | Scripts exist but no `governance/` folder |
| Quality gates | Partial | Scripts present, no formal gate records in canonical |
| Promotion package | ✗ | **BUILD-001 PROMOTION ARTIFACTS NOT IN CANONICAL** |

## Missing from Canonical

1. **`transfer/`** — no transfer zone in canonical. Transfer staging was done inside Aurora repo.
2. **`playground/`** — no explicit playground folder. `scratch/` may serve this function.
3. **BUILD-001 factory artifacts** — the entire `factory/OS-MADLAB-BUILD-001/` tree is absent.
4. **`product-manifest.json`** — exists only in accidental path (with wrong path field).

## Available Scripts

| Script | Purpose |
|---|---|
| `design-system-lint.ps1` | Design system lint/validation |
| `hydration-integrity-check.js` | SSR hydration integrity |
| `validate-configs.ps1` | Config validation |

## Checklist

- [x] estrutura real documentada
- [x] pastas ausentes listadas — `transfer/`, `playground/`, `governance/`
- [x] scripts disponíveis listados
- [x] dependências verificadas — ElysianCorp and aurora-web have `package.json` + `node_modules`
- [x] pontos de divergência com Aurora classificados
