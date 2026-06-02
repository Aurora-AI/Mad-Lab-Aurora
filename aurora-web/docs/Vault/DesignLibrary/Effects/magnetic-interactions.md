# Effect: Magnetic Interactions
ID: MAGNETIC-INTERACTIONS
Source: Claude Library

## 1. Concept
A sophisticated mouse-following pattern where elements (buttons, icons, or text) are 'pulled' toward the cursor with simulated magnetic inertia, returning to their original position with physical easing.

---

## 2. Implementation

### Event Handling
```javascript
const element = document.querySelector('.magnetic');

element.addEventListener('mousemove', (e) => {
  const rect = element.getBoundingClientRect();
  const x = (e.clientX - rect.left - rect.width / 2) * 0.3;
  const y = (e.clientY - rect.top - rect.height / 2) * 0.3;

  gsap.to(element, {
    x, y,
    duration: 0.3,
    ease: 'power2.out'
  });
});

element.addEventListener('mouseleave', () => {
  gsap.to(element, {
    x: 0, y: 0,
    duration: 0.6,
    ease: 'elastic.out(1, 0.3)'
  });
});
```

---

## 3. Best Practices
- **Padding**: Ensure the magnetic element has enough transparent padding so the target area isn't too small.
- **Intensity**: Use a multiplier between `0.2` and `0.4` to keep the effect subtle and premium.
- **Combined Effects**: Often used in conjunction with a `Custom Cursor` that scales up on magnetic elements.
