# DECISION RECORD: KOS Ingestion Architecture (Inbox)

## Context
The Tone Lab OS requires a system to organically grow without forcing the user to manually edit code, YAML files, or complex folder structures. Since the data is a living archive representing engineering projects, research, and physical equipment, the ingestion flow must be highly efficient, context-aware, and polymorphic.

## Architecture: "Capture → Structure → Relate → Validate → Render"

### 1. Universal Entry Point
- **Command Palette (`Ctrl+K`)**: Global access from anywhere in the OS.
- **Global Action Button**: Floating `[ + ]` action for mouse users.
- **Contextual Intelligence**: If the user invokes the Palette while viewing a specific Entity (e.g., `Marshall Origin 50C`), the system automatically infers this context and prepares to create a Relation, eliminating redundant data entry.

### 2. Dual-Mode Ingestion
- **Quick Capture**: For rapid data logging (e.g., pasting a link or a quick thought). Lands in the Inbox with `NEEDS REVIEW` status.
- **Structured Create**: Polymorphic forms based on the Entity type.

### 3. Polymorphic Schemas (MVP)
Initial types supported by the UI:
1. Equipment
2. Research
3. Project
4. Document
5. Purchase
6. Note

Each type renders an entirely different subset of fields in the `CreateEntityModal.tsx` while adhering to the core Ethereal Design System.

## Visual Rules (UX)
- Follows the ethereal/off-white scheme (`#F8F7F3`).
- Wide modals (`max-w-2xl` and `max-w-3xl`).
- Minimal borders (`border-neutral-200/60`).
- No 8-step wizards; progressive disclosure only.
