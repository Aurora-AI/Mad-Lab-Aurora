# Specification: Elysian Landing Page (Post-Hero Evolution)

## 1. Overview
The goal is to extend the 'Sovereign Hero' experience into a continuous narrative of high-fidelity institutional auditing. The sections following the Hero will abandon standard consumer web patterns in favor of a **'Forensic Laboratory'** layout—characterized by structural grids, raw data reveals, and technical monospaced reporting.

---

## 2. Layout Engine: The Aino Grid
All subsequent sections MUST adhere to the `AINO-TERMINAL-GRID` pattern:
- **Horizontal Locking**: Containers must align to a 12-column grid-unit (`--grid-unit`).
- **Vertical Locking**: Spacing between modules must be a multiple of the character height (`--cv`).
- **Typography**: Force `font-family: var(--font-mono)` for data-heavy sections.

---

## 3. Module Specification

### Section 02: THE FORENSIC AUDITOR (System Logs)
*A high-density textual section showcasing the algorithmic 'thought process' of Elysian.*
- **Visuals**: A recursive stream of system logs (e.g., "VALIDATING_CLAIM_0x7F...", "CORRELATING_JURISPRUDENCE...").
- **Interaction**: Auditor Focus (Pointer hover reveals clear text from a blurred background).
- **Goal**: Establish technical authority and transparency.

### Section 03: THE DATA SUBSTRATE (Artifact Matrix)
*An interactive gallery of high-conviction evidence.*
- **Visuals**: Use the `TECHNICAL-ASCII-REVEAL` pattern.
- **Content**: 3x3 or 4x4 grid of images representing settlement results, court documents, and strategy nodes.
- **Effect**: Hover reveals the "Underlying Data" (ASCII) of each artifact.

### Section 04: THE CONVICTION ENGINE (Metrics)
*Quantitative proof of Elysian's asymmetric advantage.*
- **Visuals**: Large-scale monospaced numbers mapping to settlement values and risk reductions.
- **Detail**: "Blinking" cursor animations and technical scanline overlays.
- **Layout**: 3 columns of data with strict `clinical-border-white` separators.

---

## 4. Interaction Guidelines
- **Scroll Physics**: Maintain `INSTITUTIONAL-SMOOTH-SCROLL` (1.2s inertia).
- **Navigation**: Persistent top bar with terminal coordinates (e.g., `ELYSIAN // LVL_02 // SYSTEM_READY`).
- **Micro-Motion**: Continuous background grain and 0.05 opacity grid texture.

---

## 5. Verification Gate
- All sections must maintain `100% lighthouse accessibility`.
- Font sizes must not drop below `11px` JetBrains Mono.
- Grid unit consistency is MANDATORY.
