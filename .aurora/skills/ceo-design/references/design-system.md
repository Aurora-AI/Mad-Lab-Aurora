# Design System — Tokens Oficiais Aurora

**Versão:** 1.0.0  
**Skill:** ceo-design  
**Status:** 🟢 Production  
**Fonte canônica:** `docs/brand/ELYSIAN_BRAND_KIT_v1.1.md` Parte IX

> Este arquivo é um extrato de tokens para consumo rápido pelo CEO-Design.
> Para a fonte completa com justificativa filosófica, usar o Brand Kit v1.1.

---

## Tokens de Cor

```json
{
  "luminous": {
    "primary":   "#FFFFFF",
    "surface":   "#F8F7F3",
    "surface-2": "#F2F1ED",
    "border":    "#E8E7E2"
  },
  "dark": {
    "absolute":  "#000000",
    "deep":      "#0A0A0A",
    "technical": "#0D0D0D",
    "smoke":     "#1A1A1A"
  },
  "accent": {
    "emerald":        "#10B981",
    "emerald-hover":  "#059669",
    "emerald-muted":  "rgba(16,185,129,0.08)"
  },
  "text": {
    "primary":       "#0A0A0A",
    "on-dark":       "#F2F2F2",
    "on-dark-body":  "rgba(242,242,242,0.70)",
    "on-dark-meta":  "rgba(242,242,242,0.40)"
  },
  "vertical": {
    "creative":    "#D97706",
    "commercial":  "#4F46E5",
    "legal":       "#10B981"
  }
}
```

**Regra:** O off-white da Elysian é `#F8F7F3` (temperatura quente).
NUNCA substituir por `#FAFAFA` (frio demais) ou `#F5F5F5` (sem personalidade).

**Mad Lab Aurora:** Acento âmbar `#D97706` — aparece apenas como label técnico `STRATEGY: MAD LAB AURORA`.

---

## Tokens Tipográficos

```json
{
  "family": {
    "display":   "'Söhne', 'GT America', system-ui, sans-serif",
    "technical": "'JetBrains Mono', 'Space Mono', monospace"
  },
  "weight": {
    "light": 200, "book": 300, "medium": 500,
    "semibold": 600, "bold": 700, "extrabold": 800
  },
  "scale": {
    "hero-display": { "size": "clamp(80px,14vw,200px)", "weight": 800, "tracking": "-0.04em" },
    "display-l":    { "size": "72px",  "weight": 700, "tracking": "-0.03em" },
    "headline":     { "size": "40px",  "weight": 600, "tracking": "-0.02em" },
    "body":         { "size": "16px",  "weight": 300, "tracking": "0", "line-height": "1.65" },
    "technical":    { "size": "11px",  "weight": 500, "tracking": "0.18em", "transform": "uppercase" }
  }
}
```

---

## Tokens de Layout

```json
{
  "container-max":  "1280px",
  "columns":        12,
  "gutter":         "24px",
  "margin-desktop": "80px",
  "margin-mobile":  "24px",
  "baseline":       "8px",
  "golden-ratio":   1.618
}
```

---

## Tokens de Motion

```json
{
  "hero-transition":     "cubic-bezier(0.76, 0, 0.24, 1)",
  "section-enter":       "cubic-bezier(0.16, 1, 0.3, 1)",
  "hover":               "cubic-bezier(0.4, 0, 0.2, 1)",
  "rest-before-motion":  "0.8s",
  "hero-dark-duration":  "5s",
  "transition-duration": "2s"
}
```

---

## Tokens de Border Radius

```json
{
  "none": "0px",
  "sm":   "2px",
  "md":   "4px",
  "lg":   "8px"
}
```

**Regra:** border-radius acima de 8px é proibido em produtos premium Aurora.
Cards com border-radius acima de 12px + drop-shadow = sinal de genericidade.
