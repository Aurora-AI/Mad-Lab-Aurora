# PATTERN: Cinematic Sequential (Sticky Scroll)

## Overview
A high-authority navigation architecture that controls the user's focus through a "Monolithic" sticky scroll interaction. Designed for High-Ticket/Forensic luxury interfaces where attention must be focused on one pilar at a time.

## Visual Prompt Instructions
When implementing this pattern, follow these semantic rules:

1. **Sticky Anchor (The Gravitas)**:
   - Fix one half of the viewport (or a background container) at `100vh`.
   - Trapped elements remain locked as the user scrolls, creating a stable point of reference.

2. **Sequential Narrative (The Script)**:
   - Floating text blocks must have a height exceeding `100vh` to force a "stay" time on each section.
   - Use cross-fades or semantic state changes (e.g., active/inactive) triggered by viewport entry.

3. **Motion Physics (S-Tier)**:
   - Use aggressive **Staggered Orchestration**.
   - Timing: Long durations (1000ms+) with a Deep Easing curve: `cubic-bezier(1, 0, 0, 1)`.
   - Scale: Visual assets should resolve from `scale(1.05)` to `scale(1.0)` upon activation.

4. **Branding Accents**:
   - Backgrounds should feature massive, low-opacity (5%) editorial numbering (e.g., "01").
   - Spacing must be calculated via `vw/vh` (e.g., `py-[10vh]`) to maintain editorial whitespace regardless of screen size.

## Stitch-Specific Metadata
- **Vibe Keywords**: Monolithic, Forensic, Cinematic, Gravitas, Authoritative.
- **Banned**: Bento Grids, Side-by-side Cards, Fast linear animations.
