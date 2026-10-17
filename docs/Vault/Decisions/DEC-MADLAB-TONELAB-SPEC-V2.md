# TONE LAB OS - Architecture & Presentation SPEC
**Version:** 2.0
**Domain:** Knowledge Operating System (KOS)

## 1. Core Principles
Tone Lab OS is not a Headless CMS. It is a **Knowledge Operating System** designed to register knowledge, relate entities, track states, store evidence, and support project evolution.

The system relies on a polymorphic architecture divided into two layers:
- **Layer 1: Entity Type** (What it is: Equipment, Plugin, Circuit, Measurement, Project).
- **Layer 2: Presentation Template** (How it is rendered: Store Catalog, Dossier, Engineering Schematic).

## 2. The Dual-Mode Equipment UX
The Equipment module utilizes a strict psychological transition between "Discovery" and "Engineering".

### A. Equipment Store Mode (Before the Click)
**Function:** Visual discovery, filtering, and catalog navigation.
**Inspiration:** Marshall's official retail site.
**Visual Rules:**
- Dark Theme (`#050505` to `#000000`).
- Large product images without rounded corners.
- Minimal typography. Uppercase labels.
- Tight grids (minimal gap).
- **Data displayed:** Image, Name, Category, Status (e.g., PLANNED, OWNED). No technical specs.

**Navigation Structure:**
`ALL | GUITARS | AMPLIFIERS | PEDALS | DIGITAL | CABINETS | STUDIO`
*(Sub-categories appear below dynamically).*

### B. Tone Lab Detail Mode (After the Click)
**Function:** Technical dossier, project registration, and knowledge base.
**Visual Rules:**
- Ethereal Theme (Off-white/Glassmorphism).
- Technical typography (Serif for reading, Monospace for data).
- Data-dense: Tables, diagrams, linked documents.

**Mandatory Navigation Element:**
To maintain spatial awareness, the Detail Mode must always feature a top-level breadcrumb and back button.
`<- BACK TO EQUIPMENT | EQUIPMENT / AMPLIFIERS / COMBOS / MARSHALL ORIGIN 50C`

## 3. The Detail Shell Architecture
The Detail Mode is not a single rigid template for all equipment. It operates as a **Common Shell + Specialized Modules**.

### The Common Shell (All Equipment)
- **Header:** ID, Name, Status, Role.
- **Intro:** What it is, Why it is in the Tone Lab, Project Role.
- **Specifications:** Technical verified table.
- **Project Use:** Primary role, practical use cases, related equipment.
- **Signal Path:** Visual representation of its position in the audio chain.
- **Related Entities:** Projects, Presets, Research, Documents, Decisions, History.

### Specialized Modules (Injected based on Category)
- **Guitars:** Pickups, electronics, hardware, setup constraints.
- **Amps:** Tubes, topology, power specs, speaker, FX loop.
- **Pedals:** Circuit analysis, clipping stages, controls, power draw.
- **Digital:** DSP load, routing capabilities, MIDI mapping, I/O limits.

## 4. Universal Relationships (The Graph)
Every entity in the OS can link to anything else.
An *Equipment* (Origin 50C) connects to a *Project* (Tone Factory Phase 1), which connects to a *Preset* (Marshall Crunch), which traces back to a *Research* doc (Origin vs Modeler 4CM).
