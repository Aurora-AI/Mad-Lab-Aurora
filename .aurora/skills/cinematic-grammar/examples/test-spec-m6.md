# Cinematic Synthesis Report — Test Generative Original (M6)

## 1. Primitivas Selecionadas (Agnostic / React + Framer Motion + Tailwind)

- **Weight Score:** 9 (Clímax de Hero)
- **Composition:** COM-005 (Oversized Typography + Clamp)
- **Transition/Motion:** TRN-001 (Staggered Fade-Rise) + MOT-004 (Scroll-Driven Parallax)
- **Atmosphere:** ATM-002 (Liquid Glass / Heavy Blur)
- **Lighting:** LGT-001 (Dark Backgrounds / #0C0C0C Navy)
- **Interaction:** INT-001 (Magnetic Tracking no CTA)

## 2. Storyboard Narrativo

- **Fase 1 — Silêncio e Peso (0.0s - 0.5s):** 
  A tela carrega em #0C0C0C puro com um ruído fractal sutil e muito lento no background (z-index: 0). Tudo é silencioso.
- **Fase 2 — Emergência e Revelação (0.5s - 2.0s):** 
  Um texto colossal "ARCHITEKTUR" emerge de baixo para cima (`translateY(40px) -> 0`), mas com uma máscara Liquid Glass cobrindo os 30% inferiores da tela. Cada letra do título tem um delay (`stagger 0.1s`).
- **Fase 3 — Foco e Interação (2.0s+):** 
  Um CTA de Liquid Glass aparece suavemente abaixo do texto. Quando o usuário move o mouse, o CTA atua como um imã (Magnetic Tracking) e o ruído fractal no background rotaciona levemente baseado na posição X/Y do cursor (Parallax sutil).
- **Fase 4 — Scroll Departure:**
  Ao dar scroll, a tipografia "ARCHITEKTUR" sofre parallax negativo (desce enquanto a tela sobe) e desvanece (`opacity -> 0`), revelando a Seção 2.

## 3. Motion & Framer Motion Spec (Executável)

- **Framer Motion Setup:**
  ```javascript
  import { motion, useScroll, useTransform } from "framer-motion";

  // Parallax do Scroll
  const { scrollYProgress } = useScroll();
  const yParallax = useTransform(scrollYProgress, [0, 1], [0, 300]);
  const opacityParallax = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  // Staggered Fade-Rise Variants
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1, delayChildren: 0.5, ease: [0.25, 0.1, 0.25, 1] }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 40, filter: "blur(8px)" },
    show: { opacity: 1, y: 0, filter: "blur(0px)", transition: { duration: 0.8 } }
  };
  ```

## 4. UI / CSS Spec (Tailwind)

- **Root:** `bg-[#0C0C0C] min-h-screen overflow-hidden text-white`
- **Typography:** `<motion.h1 style={{ y: yParallax, opacity: opacityParallax }} className="text-[clamp(4rem,15vw,18rem)] font-black uppercase tracking-tighter leading-none mix-blend-difference">`
- **Liquid Glass Mask / CTA:**
  ```css
  .liquid-glass {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.15);
  }
  ```

## 5. Art Direction Prompt (Asset Generation)

- **Prompt (EN):** Raw architectural brutalism, abstract 3D geometric masses floating in dark void, cinematic chiaroscuro lighting, subtle glowing coral edges, extremely dark navy background, minimal noise, high end editorial rendering --ar 16:9 --style raw
- **Negative Prompt (EN):** generic neon, purple gradients, bright, cartoony, low poly, symmetry
- **Fallback:** Um background `linear-gradient` muito escuro com ruído SVG (FractalNoise) em overlay.
