# Cinematic Synthesis Report — Elysian Portal Hero Section

**ID do Report:** SYN-MADLAB-ELYSIAN-HERO-001  
**Data:** 14 de Junho de 2026  
**Status:** Validade de QA Aprovada

---

## 1. Primitivas Selecionadas
- **Motion:** `MOT-001` (Orbital Drift) + `MOT-002` (Proximity Attraction)
- **Camera:** `CAM-001` (Slow Forward Push) + `CAM-003` (Multi-Layer Parallax Depth)
- **Composition:** `COM-001` (Split Assimétrico) + `COM-004` (Liquid Glass Surface)
- **Lighting:** `LGT-001` (Volumetric Side Light) + `LGT-002` (Amber Spotlight)
- **Interaction:** `INT-001` (Cursor Inertial Response)
- **Atmosphere:** `ATM-001` (Analog Halftone Grain) + `ATM-002` (Warm Obsidian Darkness)
- **Transition:** `TRN-001` (Weighted Page Transition)
- **Narrative:** `NAR-001` (Regra do Silêncio 0.8s) + `NAR-003` (EQ de Frequências)

---

## 2. Storyboard Narrativo

- **Fase 1 — Silêncio e Peso (0.0s - 0.8s):**  
  A tela carrega em escuridão vulcânica total (`ATM-002`, cor `#0A0A0A`) com uma sutil textura de grão analógico (`ATM-001`, opacidade 2%). Nenhuma animação ou movimento ocorre durante esse período (regra absoluta `NAR-001`). O visitante sente a pausa cênica e o peso editorial.

- **Fase 2 — Emergência e Revelação (0.8s - 2.5s):**  
  A câmera virtual inicia um avanço lento e constante pelo eixo Z (`CAM-001`). Paralelamente, um feixe de luz lateral volumétrico quente (`LGT-001`, cor âmbar `#D4AF37`) intersecta o lado esquerdo da tela, revelando o Split Assimétrico (`COM-001`). O título principal em Voz 1 Display (serifa editorial pesada) surge com um stagger reveal suave (`MOT-003`).

- **Fase 3 — Foco e Interação (2.5s+):**  
  Do lado direito (60% do split), emerge o console principal sustentado por uma superfície translúcida de vidro líquido (`COM-004`, bordas de 0.5px). As partículas suspensas na névoa de fundo orbitam lentamente (`MOT-001`) em resposta tridimensional às camadas de parallax (`CAM-003`). Ao mover o cursor sobre o console, os cards de vidro e a luz do holofote reagem com inércia física (`INT-001`, lerp 0.06).

---

## 3. Motion & GSAP Spec (Executável)

### Timeline de Revelação
```javascript
// GSAP Timeline com Easing de Gravidade
const tl = gsap.timeline({ delay: 0.8 }); // NAR-001 (0.8s silêncio)

// Fase 2: Entrada da luz e esqueleto do Split
tl.to(".volumetric-light-overlay", {
  opacity: 0.7,
  duration: 1.5,
  ease: "power2.inOut"
})
.to(".asymmetric-divider", {
  scaleY: 1,
  duration: 1.2,
  ease: "power3.inOut"
}, "-=1.0")

// Revelação da Tipografia Display (Voz 1)
.from(".display-headline span", {
  y: 50,
  opacity: 0,
  duration: 0.8,
  stagger: 0.1, // MOT-003
  ease: "cubic-bezier(0.16, 1, 0.3, 1)" // Section enter curve
}, "-=0.8")

// Fase 3: Aparição dos painéis de vidro translúcido
.from(".liquid-glass-console", {
  backdropFilter: "blur(0px)",
  borderColor: "rgba(255,255,255,0.0)",
  opacity: 0,
  duration: 1.0,
  ease: "power2.out"
}, "-=0.5");
```

### Inércia do Cursor (Mouse Follow)
```javascript
// INT-001: Cursor Inertial Response (lerp 0.06)
const cursor = { x: 0, y: 0 };
const target = { x: 0, y: 0 };

window.addEventListener("mousemove", (e) => {
  target.x = (e.clientX - window.innerWidth / 2) * 0.05;
  target.y = (e.clientY - window.innerHeight / 2) * 0.05;
});

// Loop de Renderização
gsap.ticker.add(() => {
  cursor.x += (target.x - cursor.x) * 0.06; // Lerp 0.06
  cursor.y += (target.y - cursor.y) * 0.06;
  
  gsap.set(".liquid-glass-console", {
    x: cursor.x,
    y: cursor.y,
    rotateY: cursor.x * 0.1,
    rotateX: -cursor.y * 0.1
  });
});
```

---

## 4. WebGL / Three.js Spec
- **Geometria & Malhas:** Plano de partículas para o fundo (`BufferGeometry` com 3000 vértices max). Rotação orbital lenta baseada em `MOT-001` (`mesh.rotation.y += 0.0008`).
- **Câmera:** `PerspectiveCamera` (FOV 45, Near 0.1, Far 100). Posição Z sincronizada com o scroll (`CAM-001`).
- **Post-processing:**
  - `EffectComposer`
  - Pass 1: `RenderPass`
  - Pass 2: `BokehPass` (`CAM-002` - foco a 15.0, maxBlur 0.015, abertura 0.025 para profundidade editorial).

---

## 5. Art Direction Prompt
- **Prompt (EN):** `A brutalist forensic technical console with a single rectangular glass card layout on a textured warm obsidian dark stone table. A narrow volumetric amber tungsten spotlight casts low-key chiaroscuro shadows from above. Monoline 1px coordinates, tactile raw noise grain background, anamorphic 35mm lens, F/1.8, bokeh focus on the glass edges, cinematic atmosphere, editorial post-hero design.`
- **Negative Prompt (EN):** `CGI render, neon glow, cyber brain, humanoid robot, glowing lines, bright blue hologram, generic charts, plain background.`
- **Fallback:** Cor sólida `#0D0D0D` com linha de borda de 1px cinza em opacidade 30%.

---

## 6. Acessibilidade (Reduced Motion)
Caso `prefers-reduced-motion` seja verdadeiro:
- Desativar a sincronização de scroll no eixo Z da câmera (`CAM-001`).
- Definir escala estática fixa de zoom na imagem.
- Desativar o deslocamento inercial por cursor (`INT-001`).
- Desativar o loop de rotação orbital de partículas (`MOT-001`).
- Renderizar a estrutura de split de forma estática com opacidade total no frame 0.
