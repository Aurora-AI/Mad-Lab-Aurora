# Anatomy: SovereignHeroWebGL (sovereign-hero-webgl-001)

## Visual Identity
- **Concept**: The "Sovereign Shift" — from digital noise (scramble) to physical sovereignty (3D assembly).
- **Aesthetic**: `Dark Technical` / `Industrial HDR`.
- **Palette**:
  - `BLACK`: #000000 (Pure background)
  - `GOLD`: (Dynamic emissive via shader)
  - `WHITE`: #FFFFFF (High-contrast typography)

## Technical Orchestration
- **Dual Pipeline**:
  - **Pipeline A (2D WebGL)**: Fragment shader processing a character scramble grid with mouse-reactive reveal.
  - **Pipeline B (3D R3F)**: `Piece-based` displacement using custom vertex shaders for explosive assembly.
- **Preloader**: Synchronized countdown (2.4s) before WebGL context activation.
- **Dynamic Reveal**:
  - Phase 1: Interactive hover reveal of background text.
  - Phase 2: Timed reveal of the global interface.

## Governance Tokens
- `governance_type`: Hybrid (Raw WebGL + R3F).
- `audit_standard`: CEO-Effects (Flicker coherence & HDR mapping).
- `design_system`: Aurora Industrial.

## Implementation Notes
> [!IMPORTANT]
> This component requires a GLB model at `/assets/models/puzzle.glb` in the host application.
> It uses `Lay Grotesk` as the primary display font.
