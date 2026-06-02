# Effect: Virtual Track Inertia

## Overview
A luxury gallery interaction that employs an "Invisible Virtual Slider." It decouples the drag start-point from fixed coordinates, allowing fluid navigation across a horizontal track with internal image depth (parallax).

## Technical Implementation (Blueprint)

### 1. Structural CSS
```css
#image-track {
    display: flex;
    gap: 4vmin;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(0%, -50%); /* Base position */
    user-select: none; /* Prevent selection during drag */
}

#image-track > .image {
    width: 40vmin;
    height: 56vmin;
    object-fit: cover;
    object-position: 100% center; /* Start point for parallax */
}
```

### 2. Interaction Logic (JS/TS)
```javascript
window.onmousedown = e => track.dataset.mouseDownAt = e.clientX;

window.onmousemove = e => {
    if(track.dataset.mouseDownAt === "0") return;

    const mouseDelta = parseFloat(track.dataset.mouseDownAt) - e.clientX,
          maxDelta = window.innerWidth / 2;

    const percentage = (mouseDelta / maxDelta) * -100,
          nextPercentageUnconstrained = parseFloat(track.dataset.prevPercentage) + percentage;

    const nextPercentage = Math.max(Math.min(nextPercentageUnconstrained, 0), -100);

    track.dataset.percentage = nextPercentage;

    // Smoothed Movement (The 1200ms Inertia)
    track.animate({
        transform: `translate(${nextPercentage}%, -50%)`
    }, { duration: 1200, fill: "forwards" });

    // Inverse Parallax Coupling
    for(const image of track.getElementsByClassName("image")) {
        image.animate({
            objectPosition: `${100 + nextPercentage}% center`
        }, { duration: 1200, fill: "forwards" });
    }
}

window.onmouseup = () => {
    track.dataset.mouseDownAt = "0";
    track.dataset.prevPercentage = track.dataset.percentage;
}
```

## Core Directives
1. **The 1200ms Rule**: Always use `animate()` with a 1.2s duration to simulate mass.
2. **Inverse Offset**: Image `objectPosition` must be calculated as `Percentage + 100` to ensure counter-movement relative to the track.
3. **Draggable Guard**: All images MUST have `draggable="false"`.

## Stitch Metadata
- **ID**: `VIRTUAL-TRACK-INERTIA`
- **Keywords**: Invisible Slider, Kinetic Drag, Buffered Parallax, Heavy Gallery.
- **Banned**: 1:1 cursor adhesion, jumpy resets, browser-default image dragging.
