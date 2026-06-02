# Sovereign UI Audit Protocol — Aurora Web

This protocol defines the technical and visual compliance standards for the Aurora web application, enforced via the Chrome DevTools MCP Audit Loop.

## 1. Performance Sovereignty (Stability)
- **Target Frame Rate**: 60 FPS (Stable).
- **Critical Threshold**: 45 FPS (Warning), 30 FPS (Critical Failure).
- **Audit Logic**: Measured during the Scroll Convergence phase of the 3D Hero.
- **Remediation**: If performance fails, the `arc-runtime-orchestrator` must scale down post-processing (`bokehScale`, `Vignette`) until stability is restored.

## 2. Visual Integrity (Fidelity)
- **Palette Compliance**:
    - Light Mode: `#FFFFFF` (Surface), `#B91C1C` (Callout).
    - Dark Mode: `#0D0A07` (Surface), `#B91C1C` (Callout).
- **Assembly Precision**: Puzzle pieces must align with a Euclidean distance error of < 0.01 relative to the target normalized coordinates.
- **Edge Integrity**: Computed styles for `boxGeometry` edges must maintain `-a----` attributes to prevent mesh stretching.

## 3. Accessibility & Governance
- **Contrast Ratios**: Minimum 4.5:1 for all text elements over dynamic 3D backgrounds.
- **Event Veil Traces**: No fragmented pieces should remain visible beyond the 100% assembly progress point (Opacity must be 0 for all background fragments).

## 4. Audit Frequency
- **Continuous**: FPS and Draw Calls monitoring during development.
- **Gate-Checked**: Full visual regression audit on every `Service Order` completion.

---
**Audit Level: S-Tier (Dark Editorial)**
**Compliance Version: 2026.04.17**
