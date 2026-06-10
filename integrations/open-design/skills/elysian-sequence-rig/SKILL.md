---
name: elysian-sequence-rig
description: Generates the GSAP ScrollTrigger + Lenis camera spine for the Elysian Cinematic Sequence. Outputs TypeScript React scaffold files — SequenceRig.tsx, CameraStage.tsx, WorldTone.tsx, HudTelemetry.tsx, useCameraProgress.ts.
class: A
risk: LOW
mode: generative / on-demand
trigger: explicit human request to scaffold SequenceRig or camera spine — e.g. "scaffold the sequence rig", "generate SequenceRig.tsx", "generate useCameraProgress.ts", "build the camera spine for Elysian"
promotion_gate: PROMOTION_ALLOWED
design_system: elysian
# SES validation 2026-06-10: ses_certification: certified | score: 85 | pass_rate: 1.0
---

# Elysian Sequence Rig

Generates the GSAP ScrollTrigger + Lenis camera spine for the Elysian Cinematic Sequence. Five TypeScript React files that form the scroll orchestration layer. Chambers handle their own R3F canvases — this rig owns the scroll contract only.

## Pre-flight (read before generating anything)

**MANDATORY:** Before writing a single line of TypeScript, read the following two files in full:

1. `integrations/open-design/design-systems/elysian/DESIGN.md` — color tokens, typography, spacing, motion rules.
2. Target repo's `src/lib/animations.ts` — learn the `getAnimationDefaults()` signature and return shape before implementing reduced-motion guards.

Every decision — timing, easing, world-tone mapping, HUD labels — must be grounded in those documents.

## Inputs

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `chamber_count` | `number` | `5` | Number of chambers in the sequence. Determines ScrollSpacer height and snap interval. |
| `snap` | `boolean` | `true` | When true, ScrollTrigger snap is set to `1 / (chamber_count - 1)`. When false, snap is disabled. |
| `target_file` | `"all"` \| `"SequenceRig"` \| `"CameraStage"` \| `"WorldTone"` \| `"HudTelemetry"` \| `"useCameraProgress"` | `"all"` | Which file(s) to generate. Use `"all"` to emit the full scaffold. |

## Outputs

format: tsx — TypeScript React (`.tsx` / `.ts`) files only. No HTML, no plain JS, no Astro components.

Five files, all placed under `src/components/sequence/`. When `target_file` is `"all"`, emit all five. Otherwise emit only the requested file.

**Placeholder prevention:** Não use placeholder, não omitir campos, não truncar output. Output must never contain `TODO`, `[INSERT NAME]`, `[INSERT COPY]`, `YourComponent`, `MyComponent`, Lorem Ipsum, or any generic stand-in identifier. All names, paths, and copy come from the skill spec or the inputs provided.

### 1. `useCameraProgress.ts`

Hook and context that tracks scroll progress and maps it to chambers and world tones.

**Exports (exact names, exact shapes):**

```ts
// Type: world colour state
export type WorldTone = 'dark' | 'light';

// Type: full camera progress payload
export type CameraProgress = {
  progress: number;        // 0–1, raw ScrollTrigger progress
  activeChamber: number;   // 0-indexed integer, 0 to chamber_count-1
  worldTone: WorldTone;    // derived from activeChamber via chamberToWorldTone
};

// Context
export const CameraProgressContext: React.Context<CameraProgress>;

// Hook — throws if used outside provider
export function useCameraProgress(): CameraProgress;

// Pure utility: map raw progress (0–1) to an integer chamber index
export function progressToChamber(progress: number, total: number): number;

// Pure utility: map a chamber index to its WorldTone
// World map (0-indexed): C0=light, C1=dark, C2=dark, C3=light, C4=dark
export function chamberToWorldTone(chamber: number): WorldTone;
```

World map (must be hardcoded as a lookup, not derived):

| Chamber | Index | WorldTone |
|---|---|---|
| C0 — Context | 0 | `light` |
| C1 — Governance | 1 | `dark` |
| C2 — Factory | 2 | `dark` |
| C3 — Truth | 3 | `light` |
| C4 — Category | 4 | `dark` |

### 2. `CameraStage.tsx`

The pinned viewport container. Manages its own CSS depending on motion preference.

**Required behaviour:**

- **Normal motion:** `position: fixed; width: 100%; height: 100vh; top: 0; left: 0; overflow: hidden`. `id="camera-stage"` on the root element (ScrollTrigger targets this id).
- **`prefers-reduced-motion: reduce`:** `position: relative; height: auto`. The stage becomes a normal block so chambers stack vertically without pinning.
- Apply `will-change: transform` **only** while a GSAP tween is actively running on this element. Remove it once the tween completes.
- Children are rendered as-is. CameraStage does not manage R3F.

**Signature:**

```tsx
interface CameraStageProps {
  children: React.ReactNode;
}
export function CameraStage({ children }: CameraStageProps): JSX.Element;
```

### 3. `WorldTone.tsx`

Listens to `worldTone` from `useCameraProgress()` and drives a GSAP body background transition.

**Required behaviour:**

- On `worldTone` change, run:
  ```ts
  gsap.to(document.body, {
    backgroundColor: worldTone === 'dark' ? '#000000' : '#F8F7F3',
    duration: 1.8,
    ease: 'expo.inOut',
  });
  ```
- Under `prefers-reduced-motion: reduce`: use `duration: 0.01` (instant swap, no animation).
- Must read `getAnimationDefaults()` from `../../lib/animations` to determine whether motion is reduced. Do not use a raw `matchMedia` call if `getAnimationDefaults()` already exposes `prefersReducedMotion`.
- No visible DOM output. Returns `null`.

**Signature:**

```tsx
export function WorldTone(): null;
```

### 4. `HudTelemetry.tsx`

Fixed-position header HUD. Reads `activeChamber` and `worldTone` from context.

**Required behaviour:**

- `position: fixed; top: 34px; left: 34px; z-index: 1000`.
- Renders the chamber label from the lookup below using `activeChamber`.
- `worldTone === 'dark'` → label color `var(--silver-technical)` (`#9CA3AF`).
- `worldTone === 'light'` → label color `rgba(26, 26, 23, 0.4)` (ink/40).
- Typography: JetBrains Mono, 13px, uppercase, letter-spacing 0.18em (`.t-mono` token class).

**Chamber labels (exact strings, 0-indexed):**

```ts
const CHAMBER_LABELS = [
  'STAGE: CONTEXT',
  'STAGE: GOVERNANCE',
  'STAGE: FACTORY',
  'STAGE: TRUTH',
  'STAGE: CATEGORY',
] as const;
```

**Signature:**

```tsx
export function HudTelemetry(): JSX.Element;
```

### 5. `SequenceRig.tsx`

Root orchestrator. Initialises Lenis, registers ScrollTrigger, pins the stage, and optionally enables snap.

**Required behaviour (normal motion):**

1. `gsap.registerPlugin(ScrollTrigger)` — called **once**, at module level, not inside any hook or effect.
2. On mount (`useEffect` with `[]` deps, not re-registered on re-renders):
   - Initialise `Lenis` with `{ lerp: 0.08, smoothWheel: true }`.
   - Wire Lenis RAF to GSAP ticker: `gsap.ticker.add((time) => lenis.raf(time * 1000))`.
   - Create `ScrollTrigger` with:
     ```ts
     ScrollTrigger.create({
       trigger: '#camera-stage',
       start: 'top top',
       end: `+=${chamber_count * 100}vh`,
       pin: '#camera-stage',
       scrub: 1,
       snap: snap ? 1 / (chamber_count - 1) : false,
       onUpdate: (self) => { /* update CameraProgress context */ },
     });
     ```
   - Render a `<ScrollSpacer>` div with `height: ${chamber_count * 100}vh`.
3. On unmount: call `lenis.destroy()` and `ScrollTrigger.getAll().forEach(t => t.kill())`.

**Reduced-motion path (from `getAnimationDefaults()`):**

- Skip all Lenis init, skip all ScrollTrigger.create.
- Render `children` as stacked `<section>` elements with `min-height: 100vh; overflow: hidden`.
- Each child is wrapped in its own section. No pinning.

**Signature:**

```tsx
interface SequenceRigProps {
  children: React.ReactNode;
  chamberCount?: number;   // default 5
  snap?: boolean;          // default true
}
export function SequenceRig({ children, chamberCount = 5, snap = true }: SequenceRigProps): JSX.Element;
```

## Invariants (apply to every generated file)

These rules are non-negotiable. Violating any of them makes the output incorrect.

1. **`getAnimationDefaults()` import** — every file that makes motion decisions must import `getAnimationDefaults` from `../../lib/animations` and read it before branching. No raw `window.matchMedia('(prefers-reduced-motion: reduce)')` calls.
2. **`will-change` scope** — apply `will-change` only to elements that are actively being animated by a live GSAP tween. Remove it (`will-change: auto`) in the `onComplete` callback. Never apply it globally or to static elements.
3. **`gsap.registerPlugin(ScrollTrigger)`** — appears once, at module level in `SequenceRig.tsx` only. No other file calls it.
4. **R3F isolation** — `SequenceRig`, `CameraStage`, `WorldTone`, and `HudTelemetry` must not import from `@react-three/fiber`, `@react-three/drei`, or `three`. R3F canvases are the responsibility of individual chamber components.

## Anti-Patterns — BANNED

These patterns must not appear in any generated file.

| Category | Banned pattern | Reason |
|---|---|---|
| **Astro integration** | `client:visible` per chamber | Defeats the single-rig model; creates multiple independent ScrollTrigger instances |
| **React** | `useEffect` with ScrollTrigger registration in its deps array or called on every render | Causes duplicate triggers and memory leaks |
| **CSS** | `height: 100vh` on the stage without `overflow: hidden` in normal-motion mode | Stage bleeds, content visible outside pin |
| **Three.js** | `import * from 'three'`, `import { ... } from 'three'` | Use `@react-three/fiber` and `@react-three/drei` only |
| **Scroll** | `scroll-snap-type` in CSS | ScrollTrigger owns snapping; CSS snap creates conflicts |
| **Copy** | `TODO`, `[INSERT]`, `YourComponent`, `MyComponent`, placeholder strings | Output must be production-ready scaffold, not a template shell |
| **Motion** | Bounce easing, spring overshoot, `animation-timing-function: spring(...)` | Violates Elysian motion canon |

## Pre-flight checklist

Before returning any file, verify:

- [ ] `DESIGN.md` was read before generation started
- [ ] `src/lib/animations.ts` was read — `getAnimationDefaults()` signature confirmed
- [ ] `gsap.registerPlugin(ScrollTrigger)` appears once, module-level, in `SequenceRig.tsx` only
- [ ] `useCameraProgress` world map matches: C0=light, C1=dark, C2=dark, C3=light, C4=dark
- [ ] `chamberToWorldTone` uses a hardcoded lookup array, not a computed formula
- [ ] `CameraStage` has `id="camera-stage"` on root element
- [ ] `WorldTone` transitions use `duration: 1.8` / `ease: 'expo.inOut'` (or `duration: 0.01` under reduced-motion)
- [ ] `HudTelemetry` CHAMBER_LABELS array has exactly 5 entries, exact strings
- [ ] `SequenceRig` `ScrollSpacer` height is `${chamberCount * 100}vh`
- [ ] Reduced-motion path skips Lenis + ScrollTrigger, renders stacked sections
- [ ] No R3F imports in rig files
- [ ] No `css scroll-snap-type`
- [ ] No placeholder strings in output

## References

- [DESIGN.md](file:///C:/Projetos/MadLabAurora/integrations/open-design/design-systems/elysian/DESIGN.md) — Elysian Design System tokens, typography, spacing, motion rules. **MANDATORY read before generating any scaffold.**
