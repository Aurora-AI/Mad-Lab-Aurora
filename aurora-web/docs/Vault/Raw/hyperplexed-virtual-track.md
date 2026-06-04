# Ingestion: Hyperplexed Virtual Track Logic

**Source**: Hyperplexed (Camille Tribute)
**Archetype**: S-Tier Interaction / Kinetic Gallery
**Core Challenge**: Decoupling raw mouse movement from fixed screen coordinates to create an "Invisible Virtual Slider."

---

## 1. Technical Logic Extraction

### Interaction Start (MouseDown)
- **Action**: Track the initial `X` position.
- **State Persistence**: Store `mouseDownAt = clientX`.

### Active Movement (MouseMove)
1. **Delta Calculation**: `mouseDelta = mouseDownAt - clientX`. (The distance moved from the start point).
2. **Maximum Reach**: Define `maxDelta = window.innerWidth / 2`.
3. **Normalization**: `percentage = (mouseDelta / maxDelta) * -100`.
4. **Cumulative Progress**: `nextPercentage = prevPercentage + percentage`.
5. **Clamping**: `const next = Math.max(Math.min(nextPercentage, 0), -100)`.

### Transition & Smoothing
- **The Butter Factor**: Replace direct `style.transform` with `element.animate()`.
- **Config**: `{ duration: 1200, fill: "forwards" }`.

### Composite Effect (Inverse Parallax)
- **Constraint**: To give the images internal movement relative to the track:
- **Formula**: `image.animate({ objectPosition: `${next + 100}% center` }, { duration: 1200, fill: "forwards" })`.

---

## 2. Failure Prevention (Anti-Patterns)
- **Draggable Default**: Mandatory `draggable="false"` on images to prevent browser interference.
- **Stateless Jump**: Failure to store `prevPercentage` on `MouseUp` results in the track jumping back to zero on every click.
- **Dry Tracking**: Updating without the 1200ms easing kills the "luxury" feel.

---

## 3. Cognitive Insights
- The "Invisible Slider" allows for interaction starting ANYWHERE on the screen, maximizing user ergonomics and providing a sense of omnipresent control.
- Parallax coupling ensures the UI feels like a physical layer with depth rather than a static 2D plane.
