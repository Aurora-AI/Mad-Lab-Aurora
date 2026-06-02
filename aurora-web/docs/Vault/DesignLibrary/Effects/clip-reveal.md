# Effect: Clip Reveal

## Overview
A high-precision mechanical reveal pattern where elements emerge from a hidden substrate using viewport clipping and aggressive temporal acceleration. This is a signature "S-Tier" effect that avoids the generic "soft fade-in" and instead creates a sense of physical weight and mechanical precision.

## Visual Prompt Instructions
1. **Container Setup**: The parent container of the target element must have `overflow: hidden`.
2. **Initial State**: The element is translated vertically by 100% of its height (`translateY(100%)`).
3. **Trigger**: Animation activates on scroll entry or page load.
4. **Motion Signature**: 
   - **Properties**: `transform` (never animate opacity for this effect).
   - **Physics**: Use a cubic-bezier ease-in-out: `cubic-bezier(1, 0, 0, 1)`.
   - **Behavior**: The element starts slow, undergoes "violent" acceleration, and comes to an abrupt, precise stop at `0%`.
5. **Secondary Orchestration**: When revealing multiple elements, apply a staggered delay of `0.1s` per line or component to create a "waterfall" emergence.

## Stitch-Specific Metadata
- **Keywords**: Clip Path, Mask Reveal, Mechanical Emergence, Staggered Reveal, Inertia Stop.
- **Banned**: Smooth fade, opacity: 0 to 1, bounce/overshoot (keep it deterministic).
