# Option A Backlog — Unresolved Imports

## Priority 1
- Resolve the 9 occurrences of `@/lib/utils`.
- Check whether the alias is configured in the target project tsconfig / build setup.
- If the alias is valid, verify the shared utility module exists in the checkout before changing imports.

## Priority 2
- Verify the 5 `docs/Vault/Assets/webgl-scroll-sync-001` asset references.
- Confirm whether those imports are expected static-asset references or stale paths from an archived demo.

## Priority 3
- Re-run Fallow after the import resolution pass.
- Keep the same evidence capture flow so the delta is comparable to the current trial.
