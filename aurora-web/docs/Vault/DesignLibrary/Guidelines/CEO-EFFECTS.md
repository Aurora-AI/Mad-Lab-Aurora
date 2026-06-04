# Strategic Guidance: CEO-Effects

## Overview
The **CEO-Effects** (or its operational extension, the `motion-state-controller`) is the architect of the "feel" (vibe) of the Aurora factory surfaces. This role ensures that every interaction adheres to the **Dark Editorial** DNA: high gravitas, deterministic motion, and physical weight.

## Core Directives

### 1. The Physics of Inevitability
Motion in Aurora is not "animated"; it is "physically inevitable." 
- **Rule**: Never use linear or CSS-standard easings for primary structural elements.
- **Goal**: Use **Damped Spring Physics** or **Interpolated Smoothing** (LERP) as the default mediator between input and output.

### 2. State Retention (Drag Memory)
A hallmark of S-Tier design is that the interface remembers everything.
- **Fail Pattern**: If the user drags a slider and releases it, clicking it again should NOT reset the position to zero.
- **Directive**: All manual interactions must implement **State Persistence**. The "delta" of the interaction must be cumulative.

### 3. The Inverse Parallax Theorem
To achieve depth in horizontal tracks, internal assets must move in opposition to the container progress.
- **Formula**: `AssetPosition = (ContainerProgress + 100)%`.
- **Effect**: Creates a "porthole" effect where images slide into frame with more velocity than the track itself.

### 4. Invisible Slider Mapping
Interaction start-points should be relative, not absolute.
- **Directive**: Record `startX` on `mousedown`. Calculate the delta relative to that dynamic point. This allows the user to trigger the effect from any coordinate on the viewport.

### 5. Normalization & Constraints (The Invisible Slider)
Every user interaction (mouse delta, scroll, drag) must be normalized into a `0.0` to `1.0` (or `0` to `-100%`) range before being applied.
- **Technique**: Use double clamping (`Math.max(low, Math.min(high, value))`) to define the interaction bounds.

### 4. Intentional Weight
Weight is simulated through **time-shifted response**.
- **The 1200ms Target**: Structural elements should take approximately 1.2 seconds to reach their final destination after an interaction, using strong deceleration (`power2.out` or similar).

## Ontology of Errors (To be Audited by Reflexion)
- **Dryness**: 1:1 cursor-following without mass.
- **Amnesia**: Loss of state between interactions.
- **Float**: Elements having no friction or damping.
- **Jitter**: High-frequency updates without smoothing.

## References
- [Patterns: Gravity Drag](file:///c:/Aurora/MadLabAurora/aurora-web/docs/Vault/DesignLibrary/Patterns/gravity-drag.md)
- [Effects: Emotional Physics](file:///c:/Aurora/MadLabAurora/aurora-web/docs/Vault/DesignLibrary/Effects/emotional-physics.md)
