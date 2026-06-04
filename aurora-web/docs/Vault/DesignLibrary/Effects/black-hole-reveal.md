# Effect: Black Hole Reveal
ID: BLACK-HOLE-REVEAL
Source: Claude Library

## 1. Concept
A cinematic transition that simulates a 'singular' reveal through an expanding and contracting radial clip-mask, synchronized with scroll progress and cursor position.

---

## 2. Implementation

### CSS Architecture
```css
.reveal-container {
  clip-path: circle(0% at center);
  mask-image: radial-gradient(circle at center, black 100%, transparent 100%);
  transition: clip-path 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}
```

### GSAP Logic
```javascript
gsap.to('.reveal-container', {
  clipPath: 'circle(150% at center)',
  scrollTrigger: {
    trigger: '.reveal-container',
    start: 'top 60%',
    end: 'bottom top',
    scrub: true,
  }
});
```

---

## 3. Best Practices
- **Performance**: High (uses GPU-accelerated clip-path).
- **Aesthetic**: Use for section entries or large-scale artifact reveals.
- **Micro-Motion**: Add a slight scale-up on the background image to simulate depth during the expansion.
