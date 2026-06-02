# Pattern: Gravity Drag

## Overview
A high-fidelity interaction pattern where manual inputs (drag, mousemove, scroll) simulate physical mass and momentum. It ensures that elements feel heavy and deterministic, avoiding the "floaty" or "disconnected" feel of standard digital interactions.

## Visual Prompt Instructions
1. **Delta Normalization**: Convert user mouse/touch movement into a normalized percentage (0 to 1 or -100 to 0) relative to the interaction bounds.
2. **State Retention (The Golden Rule)**: Each new interaction MUST start from the precise position where the previous one finished. Use a persistence state to store the "Final Delta."
3. **Clamping Mechanism**: Strictly enforce min/max bounds using `Math.max` and `Math.min` to create the "Invisible Virtual Slider."
4. **Interpolated Target (The Gravity)**: Apply the calculated position to the element as a destination for an animation with a duration of **1200ms**. 
   - *Logic*: The element "chases" the target with natural deceleration.
   - *GSAP Config*: `duration: 1.2, ease: "power2.out"`.
5. **Coupled Parallax**: If the container moves, the internal content (images/text) should move in opposition using the same normalized variable to create depth.

## Implementation Fail-Patterns (BANNED)
- **Origin Reset**: Element jumping back to `0,0` on interaction start.
- **Dry Tracking**: 1:1 movement with the cursor without delay or damping.
- **Unbounded Drag**: Content sliding off-screen without physical constraints.

## Stitch-Specific Metadata
- **Keywords**: Kinetic Mass, Stateful Drag, Inertia Reach, Physical Bound, Damped Response.
- **Banned**: Instant move, linear scaling, stateless interactions.
