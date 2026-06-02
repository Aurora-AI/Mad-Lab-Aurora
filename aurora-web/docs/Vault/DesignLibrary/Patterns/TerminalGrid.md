# Pattern: Aino Terminal Grid

- **ID**: `AINO-TERMINAL-GRID`
- **Vibes**: Technical, Structured, Brutalist, Deterministic
- **Status**: S-Tier / Foundation

## Overview
The 'Lost' Aino Engine layout system. Unlike standard pixel-based grids, this pattern derives the entire layout from the dimensions of a single monospace character. It ensures that typography and UI elements are mathematically locked to a character-cell system, providing a "Forensic" and highly technical aesthetic.

## Logic & Mathematics

1. **Character Dimension Measurement**:
   - A hidden `'0'` character in the project's primary monospace font (e.g., JetBrains Mono) is measured at runtime.
   - Variables exported to CSS:
     - `--ch`: Precise character width.
     - `--cv`: Precise character height.
2. **Viewport Calculation**:
   - `--cols`: Floor of `(window.innerWidth / --ch)`.
   - Allows for layouts that respond to character-count rather than standard media queries.
3. **The 'Logical' Grid Unit (`--grid-unit`)**:
   - Defined as `4 * --ch`.
   - This unit is used for all padding, margins, and standard component widths.
   - Ensures that an element is always a multiple of character widths.

## Visual Prompt Instructions (for Generation)
1. "Lock the viewport to 80 columns of monospaced data."
2. "Derive all padding from a 4-character margin."
3. "Align all visual borders to the boundaries of character cells."

## Implementation Notes
- **Hook**: `useTerminalGrid.ts`.
- **CSS**: Uses native CSS `calc()` with `--ch` and `--grid-unit`.

## Source Attribution
- **Origin**: Aino / Optimized for Aurora by Jay E
