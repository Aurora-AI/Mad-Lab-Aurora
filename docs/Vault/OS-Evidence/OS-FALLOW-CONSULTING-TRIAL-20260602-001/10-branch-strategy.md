# Branch Strategy — Option 2

Base branch: `backup/workspace-snapshot-20260602`

## Goal
Split remediation into small, reviewable branches so each fix class can be validated independently before merge.

## Branch 1 — Local utility resolution
**Branch name:** `fix/aurora-visual-assets-local-utils`

**Scope:**
- Resolve the 9 `@/lib/utils` imports in standalone `aurora-visual-assets` packages.
- Decide per package whether to add a local `lib/utils.ts` or replace the alias with a package-local path.

**Package cluster:**
- `aurora-visual-assets/backgrounds/background-paths`
- `aurora-visual-assets/backgrounds/plasma-grid`
- `aurora-visual-assets/borders/neon-button`
- `aurora-visual-assets/heroes/hero-davincho`
- `aurora-visual-assets/interactions/image-comparison`
- `aurora-visual-assets/interactions/image-comparison-slider`
- `aurora-visual-assets/interactions/motion-footer`
- `aurora-visual-assets/interactions/stacked-panels`
- `aurora-visual-assets/interactions/team-marquee`

**Acceptance:**
- Each package resolves `cn` without depending on a missing root alias.
- Fallow unresolved import count drops by 9.

## Branch 2 — Archived asset path cleanup
**Branch name:** `fix/webgl-scroll-sync-asset-paths`

**Scope:**
- Review `docs/Vault/Assets/webgl-scroll-sync-001` references.
- Decide whether they are intentionally archived references or stale paths.

**Acceptance:**
- References are either corrected or explicitly documented as archived/no-action.

## Branch 3 — Post-fix validation harness
**Branch name:** `chore/fallow-postfix-validation`

**Scope:**
- Re-run Fallow after the first two branches land.
- Record delta in `health`, `dead-code`, `dupes`, and unresolved imports.

**Acceptance:**
- New evidence shows the delta from the current baseline.

## Execution Order
1. Land Branch 1.
2. Land Branch 2.
3. Run validation branch.
4. Reassess whether duplicate cleanup deserves its own branch or should stay separate.

## Risk Notes
- Keep each branch under one concern to avoid mixing alias fixes with archive cleanup.
- Do not introduce shared abstractions unless multiple packages already share a proven runtime boundary.
- Preserve the backup snapshot branch untouched as the rollback baseline.
