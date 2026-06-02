# EFFECT: Particle Image Form (Kinetic Reconstruction)

## Overview
A high-fidelity visual reconstruction effect where images are formed by thousands of individual kinetic particles. These particles respond to user interaction (mouse/touch) and environmental noise before settling into a deterministic form.

## Visual Prompt Instructions
When implementing this effect, follow these semantic rules:

1. **Particle Density (The Budget)**:
   - Use a massive budget of particles (~8000 for high-end contexts).
   - Each particle represents a pixel or a sampling point of the source image.

2. **Kinetic Behavior (The Physics)**:
   - Damping: `0.93` (High enough to avoid chaotic jitter, low enough for fluid motion).
   - Speed/Spring: `0.02` (A slow, purposeful drift towards the target position).
   - Noise: Suble atmospheric noise (`noiseAmp: 0.12`) to keep the "Living" quality even when settled.

3. **Interaction**:
   - Particles should repel or disperse upon mouse approach (`mouseRadius: 2.8`).
   - The "Gravity" of the target shape should eventually pull them back into absolute alignment.

4. **Atmosphere**:
   - Best used for "Truth" reveals or loading transitions.
   - Pair with off-black backgrounds and monochromatic particle colors for a premium effect.

## Stitch-Specific Metadata
- **Vibe Keywords**: Living, Kinetic, Algorithmic, Reconstructed, Molecular.
- **Banned**: 2D Image fades, Low-resolution transitions, Linear reveal bars.
