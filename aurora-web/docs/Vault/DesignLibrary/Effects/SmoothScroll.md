# Effect: Institutional Smooth Scroll

- **ID**: `INSTITUTIONAL-SMOOTH-SCROLL`
- **Vibes**: Premium, Editorial, Heavy, High-Gravity
- **Status**: S-Tier / User Experience

## Overview
The 'Signature' Aurora scroll experience. Designed to mimic the tactile feel of heavy, high-quality editorial paper, this effect removes the jitter of standard browser scrolling and replaces it with high-inertia, mathematically eased motion. It is essential for "Institutional" vibes where every interaction must feel deliberate.

## Physics & Easing

1. **The 'Aino' Easing**:
   - Logic: `(t) => Math.min(1, 1.001 - Math.pow(2, -10 * t))`.
   - Result: A rapidly accelerating start with a long, graceful tail-off (exponential decay).
2. **Timing Components**:
   - **Duration**: 1.2s (Long enough to be felt, short enough not to lag).
   - **Multiplier**: 1x for wheel, 2x for touch (compensates for fingertip friction).
3. **Synchronization**:
   - Integrated into the global `requestAnimationFrame` (RAF) loop to ensure zero-stutter on displays above 60Hz.

## Visual Prompt Instructions (for Generation)
1. "Set the interface to a high-inertia 1.2s institutional scroll."
2. "Apply a power-10 exponential decay to all viewport movement."
3. "Synchronize the scroll engine with hardware-accelerated RAF."

## Implementation Notes
- **Library**: `lenis`.
- **Component**: `SmoothScroll.tsx`.

## Source Attribution
- **Origin**: Studio Freight / Adapted for Aurora by Jay E
