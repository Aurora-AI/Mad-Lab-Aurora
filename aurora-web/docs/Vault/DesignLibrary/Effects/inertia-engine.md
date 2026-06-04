# Effect: Inertia Engine

## Overview
A structural scroll behavior that decouples raw mouse input from viewport movement to simulate physical mass, friction, and "gravitas." This ensures the interface doesn't feel "floaty" or "disconnected," but rather like a heavy, high-precision instrument.

## Visual Prompt Instructions
1. **Engine Selection**: Implemented via Lenis or GSAP ScrollSmoother.
2. **Physics Configuration**:
   - **LERP (Linear Interpolation)**: Calibrated at `0.08` to `0.1`. Lower values increase "perceived mass."
   - **Friction**: High initial friction to prevent "slippery" navigation.
3. **Motion Coupling**: All parallax or scroll-triggered animations MUST be synced to this engine's scroll progress to prevent jitter.
4. **Behavior**: Scrolling should feel "smooth but heavy." There is a subtle start-up and a natural, damped decay when the user stops scrolling.
5. **Hardware**: Ensure hardware acceleration (`will-change: transform`) is applied to the scrolling substrate.

## Stitch-Specific Metadata
- **Keywords**: Smooth Scroll, Virtual Scroll, Deep Scroll, Kinetic Friction, Damped Motion.
- **Banned**: Native jumpy scroll, high-frequency kinetic scroll, 1:1 mouse tracking.
