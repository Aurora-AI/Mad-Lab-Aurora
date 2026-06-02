# Effect: Spiral Vortex Menu
ID: SPIRAL-VORTEX-MENU
Source: Claude Library

## 1. Concept
An immersive navigation pattern where menu items are positioned along a 3D spiral or vortex, rotating around the Z-axis based on scroll or mouse position.

---

## 2. Implementation

### Trigonometric Positioning
```javascript
const items = document.querySelectorAll('.vortex-item');
const totalItems = items.length;

items.forEach((item, index) => {
  const angle = (index / totalItems) * Math.PI * 2;
  const radius = 300;
  const x = Math.cos(angle) * radius;
  const y = Math.sin(angle) * radius;
  const z = (index / totalItems) * -500; // Recedes into depth

  gsap.set(item, { x, y, z, rotationZ: angle * (180 / Math.PI) });
});
```

### Motion Trigger
```javascript
gsap.to('.vortex-container', {
  rotationZ: 360,
  z: 500, // Moves toward camera
  scrollTrigger: {
    trigger: '.vortex-wrapper',
    scrub: 1.5,
  }
});
```

---

## 3. Best Practices
- **Depth**: Use `perspective: 1000px` on the parent container.
- **Opacity**: Fade items as they recede into the Z-axis (`opacity: 1 - progress`).
- **Interaction**: Add a magnetic hover effect to the individual nodes for high-conviction selection.
