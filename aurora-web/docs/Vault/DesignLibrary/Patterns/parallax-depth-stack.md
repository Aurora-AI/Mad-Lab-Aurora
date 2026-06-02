# Pattern: Parallax Depth Stack
ID: PARALLAX-DEPTH-STACK
Source: Claude Library

## 1. Concept
A multi-layered scroll architecture where elements at different Z-depths move at different speeds, creating a perceived 3D space during vertical navigation.

---

## 2. Implementation

### Data Attributes
Assign different speeds to layers:
```html
<div class="parallax-layer" data-speed="0.1">Background</div>
<div class="parallax-layer" data-speed="0.5">Middle</div>
<div class="parallax-layer" data-speed="1.2">Foreground</div>
```

### GSAP Initialization
```javascript
gsap.utils.toArray('.parallax-layer').forEach(layer => {
  const speed = layer.getAttribute('data-speed');
  
  gsap.to(layer, {
    yPercent: -100 * speed,
    ease: 'none',
    scrollTrigger: {
      trigger: layer,
      start: 'top bottom',
      end: 'bottom top',
      scrub: true,
    }
  });
});
```

---

## 3. Best Practices
- **Inertia**: Always use with `INSTITUTIONAL-SMOOTH-SCROLL` for weighted motion.
- **Occlusion**: Ensure foreground elements don't obscure critical information at their peak speed.
- **Reference**: Follow the **Exoape** philosophy of 'subtle depth' rather than aggressive motion.
