# Effect: Sovereign Hero (Noise to Truth Reveal)

- **ID**: `SOVEREIGN-HERO-NOISE`
- **Vibes**: Forensic, Cinematic, Institutional, Dark Editorial
- **Status**: S-Tier / Production Ready

## Overview
A high-fidelity WebGL transition designed to represent the emergence of "Truth" from algorithmic complexity. It utilizes a dual-texture shader approach to blend a chaotic scramble state (characters) into a stable typographic signal (identity), creating a narrative of "Clarity through Auditor Intervention."

## Visual Logic & Physics

1. **Dual Texture Architecture**:
   - **Texture A (Chaos)**: A dynamic map of pseudo-random monospaced characters rendered offscreen.
   - **Texture B (Signal)**: High-contrast typography and branding elements.
2. **Transition Field (FBM)**:
   - Uses Fractal Brownian Motion (FBM) to modulate the opacity gradient between textures.
   - Creates a non-linear, "dissolving" boundary that feels organic and non-digital.
3. **Temporal Reveal**:
   - Duration: 5000ms.
   - Easing: `easeOutCubic`.
   - Start: 100% Scramble.
   - End: 90% Typography / 10% Residual Noise.
4. **Mouse-Reactive Auditor Focus**:
   - A circular "magnifying" field (260px radius) linked to the pointer coordinates.
   - The field locally overrides the global progress, forcing a 100% signal reveal within its radius.
   - Creates the tactile sensation of "Auditing" the noise.

## Implementation Notes (Agent Specific)
- **Shader**: Fragment shader uses `max(globalReveal, mouseReveal)` logic.
- **Blending**: `mix(color, textTex.rgb, textMix * textTex.a)`.
- **Performance**: High (runs in a single draw call once textures are cached).

## Source Attribution
- **Origin**: Elysian / MadLab Aurora
- **Author**: Comandante (Optimized by Jay E)
