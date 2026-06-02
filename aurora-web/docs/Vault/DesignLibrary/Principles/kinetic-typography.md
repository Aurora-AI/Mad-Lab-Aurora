# Principle: Kinetic Typography
ID: KINETIC-TYPOGRAPHY
Source: Arsenal / Jay E

## 1. Concept
Premium text entry logic that breaks blocks into individual characters or words, animating them with high-acceleration easing (Expo) and calculated inertia to create a cinematic "agência cara" (expensive agency) aesthetic.

---

## 2. Implementation

### Fatiamento (SplitType)
```javascript
import SplitType from 'split-type';
const text = new SplitType('.kinetic-text', { types: 'chars, words' });
```

### Motion Sequence (GSAP)
```javascript
gsap.from(text.chars, {
  y: 100,             // Comes from bottom
  opacity: 0,
  rotationZ: 10,      // Pre-roll torsion
  stagger: 0.02,      // Hyper-fast domino effect
  duration: 1.2,
  ease: 'expo.out',   // Aggressive acceleration curve
});
```

---

## 3. Best Practices
- **Stagger**: Keep between `0.01` and `0.03` for the "high-end" vibe.
- **Easing**: `expo.out` or `power4.out` is mandatory. Avoid `linear` or `sine`.
- **Inertia**: Always combine with a minor rotation or scale to simulate physical weight.
- **Accessibility**: Revert the split if the user has `prefers-reduced-motion` active.
