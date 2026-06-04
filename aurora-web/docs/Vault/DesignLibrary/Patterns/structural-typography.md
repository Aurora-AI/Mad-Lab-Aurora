# Pattern: Structural Typography

## Overview
A typographic architecture where font scaling is derived directly from the viewport geometry, ensuring a deterministic "Locked-in" layout across all resolutions. Unlike standard responsive typography (breakpoints), Structural Typography scales linearly, maintaining the same visual aspect ratio.

## Visual Prompt Instructions
1. **Dynamic Scaling**: Use Viewport Width (`vw`) units for all headline sizes.
   - Example Headings: `10vw`, `12vw`, or `15vw`.
   - Scaling: Linear scale without manual media query jumps.
2. **Negative Tracking**: Apply tight negative letter-spacing for large display type.
   - Values: `-0.02em` to `-0.05em`.
   - Formula: The larger the font-size, the tighter the tracking.
3. **Weight Over Size**: Control hierarchy through weight (Thin/Black) and specific color roles (Zinc-950 vs Zinc-400) rather than just size.
4. **Substrate Alignment**: Large text should be used as a structural grid element (e.g., spanning exactly 50% or 100% of the viewport).
5. **Rendering**: Strictly enforce `-webkit-font-smoothing: antialiased` for high-fidelity text rendering on dark backgrounds.

## Stitch-Specific Metadata
- **Keywords**: Viewport Type, Linear Scale, Negative Kerning, Structural Headlines, Locked Layout.
- **Banned**: 16px breakpoints, loose letter-spacing, center-aligned block text (use asymmetric or justified focus).
