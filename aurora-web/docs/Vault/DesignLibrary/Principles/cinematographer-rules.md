# Principle: Antigravity Cinematographer Rules
ID: CINEMATOGRAPHER-RULES
Source: Claude Library

## 1. Governance
The Cinematographer role is strictly additive. You receive a static design (Stitch) and add 'life' (motion/physics) without modifying the visual or structural integrity.

### Absolute Rules:
- **Zero Structure Modification**: Never change HTML hierarchy or CSS layout classes.
- **Design Preservation**: Never "improve" colors, fonts, or spacing.
- **Motion with Physics**: All animations must have perceived mass, gravity, and inertia.

---

## 2. Technical Stack
- **GSAP 3.12+**: Primary engine for all timelines and transforms.
- **ScrollTrigger**: Mandated for scroll-bound animations.
- **Lenis**: Mandatory for smooth-scroll synchronization (1.2s duration, power-10 decay).

---

## 3. Implementation Patterns

### Smooth Scroll Initialization
```javascript
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
});

gsap.ticker.add((time) => lenis.raf(time * 1000));
```

### Motion Intensity Gates
- **Desktop**: High-fidelity, multi-layer parallax allowed.
- **Mobile**: Simplified or disabled heavy effects (`window.innerWidth < 768`).
- **Accessibility**: Respect `prefers-reduced-motion`.

---

## 4. Quality Benchmark
Target **Studio Dialect** and **Exoape** standards for transitions and depth.
- Zero CLS (Cumulative Layout Shift).
- Consistent 60fps on standard hardware (Intel Iris Xe).
