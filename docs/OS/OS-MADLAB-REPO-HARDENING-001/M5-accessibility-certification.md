# OS-MADLAB-REPO-HARDENING-001 — M5: Accessibility Certification

**Data:** 2026-06-09  
**Etapa:** M5 de 6  
**Status:** AUDITADO — CORREÇÕES PENDENTES  
**Escopo:** prefers-reduced-motion gaps em componentes de animação

---

## Auditoria de Cobertura

| Componente | Tecnologia | prefers-reduced-motion | Status |
|---|---|---|---|
| `ZAxisScrollContainer.tsx:53` | matchMedia direto | ✅ Implementado | PASS |
| `Preloader.tsx` | Framer Motion | ❌ Ausente | FAIL |
| `useScrollProgress.ts` | scroll listener raw | ❌ Ausente | FAIL |
| `ScrollDriver.tsx` | — | nenhuma animação direta | N/A |
| `SovereignHeroWebGL.tsx` | WebGL | nenhuma animação CSS/JS reduzível | N/A |

**Resultado:** 1/3 componentes com animação cobertos (33%).

---

## ACF-001 — Preloader sem fallback de reduced-motion

**Arquivo:** `aurora-web/src/components/Preloader.tsx`  
**Linha crítica:** 51, 68-69, 77-78

**Problema atual:**
```tsx
// Linha 68-69: barra de progresso anima 2.8s sem condicional
animate={{ x: "0%" }}
transition={{ duration: 2.8, ease: "easeInOut" }}
```

Framer Motion suporta `useReducedMotion()` hook nativamente. Sem ele, usuários com `prefers-reduced-motion: reduce` recebem animações completas.

**Correção exigida:**
```tsx
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';

// dentro do componente:
const shouldReduceMotion = useReducedMotion();

// na barra de progresso:
transition={{ 
  duration: shouldReduceMotion ? 0 : 2.8, 
  ease: "easeInOut" 
}}

// nos fade-ins:
transition={{ delay: shouldReduceMotion ? 0 : 0.2 }}
```

---

## ACF-002 — useScrollProgress sem pausa em reduced-motion

**Arquivo:** `aurora-web/src/hooks/useScrollProgress.ts`  
**Problema:** Hook atualiza `progress` a cada evento de scroll sem checagem. Componentes que usam este hook (ex: ScrollDriver, ZAxisScrollContainer) podem usar o valor para acionar animações que deveriam ser desabilitadas.

**Nota:** `ZAxisScrollContainer` já checa `prefers-reduced-motion` e pula as transformações 3D. O gap é que `useScrollProgress` continua emitindo updates desnecessários, e outros consumidores futuros do hook podem não ter a mesma proteção.

**Correção recomendada (non-breaking):**
```ts
// Adicionar ao hook:
const prefersReducedMotion = 
  typeof window !== 'undefined' 
    ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
    : false;

// Exportar junto com progress:
return { progress, prefersReducedMotion };
```

Consumidores existentes continuam funcionando; novos consumidores têm o flag disponível.

---

## Conformidade WCAG

| Critério | Aplicação | Status |
|---|---|---|
| WCAG 2.1 SC 2.3.3 (AAA) — Animation from Interactions | useScrollProgress → ZAxisScrollContainer | PASS (ZAxis já cobre) |
| WCAG 2.1 SC 2.3.3 — Preloader animation | Preloader.tsx | FAIL |
| WCAG 2.1 SC 1.4.3 — Contrast | Fora de escopo desta etapa | N/A |

**Nível exigido pelo produto:** AA mínimo / AAA desejável para motion.

---

## Prioridades

```
ACF-001 — Preloader: P2 (impacta first impression, não bloqueia core UX)
ACF-002 — useScrollProgress: P3 (proteção preventiva para futuros consumidores)
```

Nenhum dos dois é bloqueador de merge imediato, mas devem ser resolvidos antes de qualquer release candidata.

---

## Próxima Etapa

**M6 — Workflow Architecture: Visual Synthesis Pipeline**  
Formalizar o Mad Lab Visual Synthesis Workflow (9 estágios) e o contrato de integrations/open-design como Design Assembly Runtime.
