# Root Cause Note — Unresolved Imports

## Conclusão
The 14 unresolved imports are real, not a parser artifact.

## Evidence
- `@/lib/utils` appears in 9 standalone component packages under `aurora-visual-assets/`.
- There is no `lib/utils.ts` inside `aurora-visual-assets/` or inside the affected package roots.
- A matching utility exists only in `ElysianCorp/src/lib/utils.ts`, which is not in the import resolution scope of those standalone packages.

## Impact
- The affected packages cannot resolve `cn` locally.
- The current import pattern is a copied template that assumes a utility module that was never scaffolded into these package roots.

## Recommended Fix Shape
1. Add a local `lib/utils.ts` to each standalone package that uses `@/lib/utils`, or
2. Normalize the component packages to consume a shared utility package with a real package alias, or
3. Replace the alias imports with a package-local relative import if the package is intentionally standalone.

## Priority
- First fix the 9 `@/lib/utils` cases.
- Then decide whether the `docs/Vault/Assets/webgl-scroll-sync-001` references are intentionally archived or stale.