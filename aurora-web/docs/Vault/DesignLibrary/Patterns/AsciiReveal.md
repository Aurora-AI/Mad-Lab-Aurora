# Pattern: Forensic ASCII Reveal
ID: TECHNICAL-ASCII-REVEAL / X-RAY-ASCII-REVEAL
Source: MadLab Aurora

## 1. Concept
A modular forensic engine for revealing the "Data Substrate." It supports two primary modes:
1. **Mode A: Cinematic (Temporal)**: A 1.8s time-based transition from image to ASCII.
2. **Mode B: X-Ray (Spatial)**: An interactive flashlight reveal where the mouse reveals the code layer locally.

---

## 2. Modes

### Mode A: Cinematic Transition
- **Trigger**: Hover / In-View.
- **Easing**: `cubic-bezier(0.76, 0, 0.24, 1)`.
- **Motion**: 1.8s fade + blur deconstruction.

### Mode B: X-Ray Flashlight (NEW)
- **Mechanism**: Dynamic CSS `mask-image` tracking the pointer.
- **Property**: `radial-gradient(circle 150px at var(--mouse-x) var(--mouse-y), black 0%, transparent 100%)`.
- **Psychology**: Encourages active exploration and 'de-scrambling' of the evidence.

---

## 3. Implementation (Mode B)

### CSS
```css
.ascii-overlay {
  -webkit-mask-image: radial-gradient(circle 150px at var(--mouse-x) var(--mouse-y), black 0%, transparent 100%);
  mask-image: radial-gradient(circle 150px at var(--mouse-x) var(--mouse-y), black 0%, transparent 100%);
}
```

### Handler
```javascript
const handleMouseMove = (e) => {
  const { left, top } = ref.current.getBoundingClientRect();
  ref.current.style.setProperty('--mouse-x', `${e.clientX - left}px`);
  ref.current.style.setProperty('--mouse-y', `${e.clientY - top}px`);
};
```

---

## 4. Best Practices
- **Font**: Mandatory Monospace (6pt-8pt).
- **Inertia**: Add a slight lag to the CSS cursor variables for a more organic feel.
- **Contrast**: The ASCII layer should be high-contrast (White on Black) for maximum impact.
