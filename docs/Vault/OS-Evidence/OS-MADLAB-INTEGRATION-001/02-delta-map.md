# OS-MADLAB-INTEGRATION-001 — M2: Source/Destination Delta Map

**Data:** 2026-06-09  
**Status:** CONCLUÍDA  

---

## Identificação de Origem e Destino

| Dimensão         | Origem (Mad Lab)                          | Destino (Elysian-Corp soberano)              |
|------------------|-------------------------------------------|----------------------------------------------|
| **Path**         | `C:\Projetos\MadLabAurora\aurora-web\`    | `C:\Projetos\MadLabAurora\ElysianCorp\`      |
| **Repo**         | Mad Lab (não soberano)                    | `Aurora-AI/Elysian-Corp` (soberano)          |
| **Framework**    | **Vite + React SPA**                      | **Astro + React Islands**                    |
| **Entry point**  | `src/main.tsx` → `App.tsx`                | `src/pages/index.astro`                      |
| **Roteamento**   | react-router-dom (SPA client-side)        | Astro file-based routing (SSG)               |
| **Deploy**       | Vercel (framework: vite)                  | Vercel (framework: astro)                    |
| **Vercel config**| `aurora-web/vercel.json` (implícito)      | `ElysianCorp/vercel.json` (astro explícito)  |

---

## Delta: Componentes

### Origem — aurora-web/src/components/

```
ARC/
AuroraHero.tsx
Diagnosis.tsx
ElysianChat.tsx          ← proxy /api/chat (server-side Gemini)
Footer.tsx
Header.tsx
Preloader.tsx            ← useReducedMotion() aplicado
ScrollDriver.tsx
SectionLabel.tsx
SovereignHeroWebGL.tsx
elysian/
fx/
hero/
sections/
ui/
```

### Destino — ElysianCorp/src/components/

```
cursor/
  MagneticCursor
fx/
  IdentityFragmenter.tsx
  ScramblePortrait.tsx
hero/
  CinemaHero.astro
  ConcaveScene.tsx
  ExoFluidHero.tsx
  ForensicCodeCascade.tsx
  GazeForensicHero.tsx        ← hero ativo em index.astro
  HeroContent.tsx
  IndustrialGrid.tsx
  ScrambleBackground.tsx
motion/
  MotionViewer (Remotion)
sections/
  AuditTrail, ControlFailure, ForensicFooter, IntegrityGap,
  SectionConversion, SectionGap, SectionMechanism, SectionValidation,
  TrustwareAnswer, TrustwareArchitecture, TrustwareClients,
  TrustwareFounder, TrustwareMoat, TrustwarePortfolio, TrustwareReality
ui/
  Header
```

### Delta Classificado

| Componente origem      | Estado no destino         | Ação                                       |
|------------------------|---------------------------|--------------------------------------------|
| `ElysianChat.tsx`      | AUSENTE                   | Candidato para promoção via Promotion Package |
| `Preloader.tsx`        | AUSENTE                   | Candidato — avaliar fit com Astro SSG      |
| `SovereignHeroWebGL.tsx`| AUSENTE                  | Candidato — avaliar compatibilidade WebGL  |
| `AuroraHero.tsx`       | AUSENTE                   | Verificar se GazeForensicHero substitui    |
| `ScrollDriver.tsx`     | AUSENTE                   | Verificar se Lenis/GSAP do destino cobre   |
| `Header.tsx`           | PRESENTE (destino tem ui/Header) | Delta de feature — verificar paridade |
| `Footer.tsx`           | PRESENTE (ForensicFooter) | Delta de feature — verificar paridade      |
| `useScrollProgress`    | Não mapeado no destino    | Verificar equivalente                      |
| `useTerminalGrid`      | Não mapeado no destino    | Verificar se usado no destino              |

---

## Delta: Rotas / Páginas

| Origem (SPA routes)         | Destino (Astro pages)          | Status        |
|-----------------------------|--------------------------------|---------------|
| `/` (App.tsx root)          | `src/pages/index.astro`        | ✅ equivalente |
| Rotas dinâmicas (se houver) | `src/pages/[slug].astro`       | A verificar   |
| `halide-demo.astro`         | destino only                   | Não na origem |
| `wave-demo.astro`           | destino only                   | Não na origem |

---

## Delta: Assets

| Origem (`aurora-web/public/`)  | Destino (`ElysianCorp/public/`) | Ação            |
|--------------------------------|---------------------------------|-----------------|
| `hero_bg.png`                  | Verificar presença              | Mapear          |
| `fonts/`                       | Verificar presença              | Mapear          |
| `assets/`                      | `src/assets/`                   | Verificar paths |

---

## Delta: APIs

| Endpoint      | Origem                       | Destino                         | Status           |
|---------------|------------------------------|---------------------------------|------------------|
| `/api/chat`   | `aurora-web/api/chat.ts`     | AUSENTE em ElysianCorp          | **Candidato P0** |
| Firebase      | `src/firebase.ts` na origem  | Não mapeado no destino          | A verificar      |

---

## Delta: Env Vars

| Variável          | Origem                           | Destino                         | Status    |
|-------------------|----------------------------------|---------------------------------|-----------|
| `GEMINI_API_KEY`  | Vercel (server-side, Encrypted)  | Não configurada em ElysianCorp  | P0 — deve ser configurada server-side antes de deploy |
| `VITE_*`          | AUSENTE (removida em 1ec058a)    | Não deve existir                | ✅ OK      |

---

## Delta: Dependências Críticas

| Lib               | Origem | Destino | Observação                              |
|-------------------|--------|---------|------------------------------------------|
| `framer-motion`   | ✅     | ✅      | Alinhado                                 |
| `three` / R3F     | ✅     | ✅      | Alinhado                                 |
| `gsap`            | ✅     | ✅      | Alinhado                                 |
| `lenis`           | ✅     | ❌      | Ausente no destino — substituído por?    |
| `@google/genai`   | ✅     | ❌      | Ausente — necessário para ElysianChat    |
| `firebase`        | ✅     | ❌      | Ausente no destino                       |
| `remotion`        | ❌     | ✅      | Destino only (MotionViewer)              |
| `astro`           | ❌     | ✅      | Framework diferente                      |
| `react-router-dom`| ✅     | ❌      | Não necessário em Astro                  |

---

## Delta: Design System / Tokens

| Dimensão         | Origem                      | Destino                          |
|------------------|-----------------------------|----------------------------------|
| Tokens CSS       | Tailwind (config implícito) | `src/styles/tokens.css` + `globals.css` |
| Open Design      | `integrations/open-design/` | Design Assembly Runtime — NÃO produtivo |
| Design System    | Tailwind inline             | `tailwind.config.mjs` explícito  |

---

## Delta: Motion / Reduced-Motion

| Componente             | Origem                     | Destino                          |
|------------------------|----------------------------|----------------------------------|
| `Preloader.tsx`        | `useReducedMotion()` ✅     | Ausente no destino               |
| `useScrollProgress.ts` | media query guard ✅        | Não mapeado no destino           |
| Motion geral           | framer-motion              | framer-motion + GSAP + Remotion  |

---

## Riscos Identificados

| Risco                                                | Severidade | Nota                                    |
|------------------------------------------------------|------------|-----------------------------------------|
| `/api/chat` ausente no destino                       | P0         | Chat quebra sem proxy server-side       |
| `GEMINI_API_KEY` não configurada em ElysianCorp Vercel| P0        | Deploy silenciosamente quebrado          |
| Framework mismatch (Vite SPA → Astro Islands)        | P1         | Componentes precisam de `client:load`   |
| `lenis` ausente no destino                           | P1         | Scroll behavior pode divergir           |
| `@google/genai` ausente no destino                   | P1         | Dep necessária para ElysianChat         |
| Preloader sem destino mapeado                        | P2         | Avaliar fit com Astro page transitions  |
| Assets paths distintos (`public/` vs `src/assets/`) | P2         | Verificar antes de mover               |

---

## Classificação Open Design

```
integrations/open-design/ → Design Assembly Runtime
NÃO é runtime produtivo.
NÃO deve ser copiado para ElysianCorp.
Serve como referência de tokens e padrões para o Promotion Package.
```

---

## Próxima Etapa

**Micro-Etapa 3 — Next.js Integration Plan**

> Nota: o destino usa **Astro**, não Next.js. O nome "Next.js Integration Plan" na OS refere-se
> à integração técnica controlada — a arquitetura alvo é Astro Islands, não uma migração para Next.js.
