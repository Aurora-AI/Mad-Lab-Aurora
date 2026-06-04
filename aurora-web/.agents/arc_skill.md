# Sovereign ARC Integration Skill (v2.0)

This skill provides instructions for the coded integration of the **Artifact Runtime Contract (ARC)** system into the Aurora ecosystem.

## Core Principles
1. **Deterministic Representation**: Artifacts must be derived from `OperationalState` through canonical `SemanticState` mappings.
2. **Device-Tier Degradation**: Rendering must adapt to the device profile (ULTRA, HIGH, BALANCED, LOW, DEGRADED).
3. **No LLM in Render**: Business logic and state derivation must be deterministic, never probabilistic.
4. **Boundary Isolation**: ARC components are boundaries that isolate operational complexity from visual representation.

## Semantic State Palette (Elysian Standards)
- **NEUTRAL_OBSERVING**: #09111B, #89A4BF, #D8E6F4 (Dark, stable, monitoring).
- **STABLE_OPERATION**: #08161E, #75D0B4, #D1FFF2 (Cyan/Green accents).
- **GOAL_ACHIEVED**: #160D03, #D8B15A, #FFF0B6 (Gold/Metallic high-tier).
- **ALERT_ACTIVE**: #180506, #FF6767, #FFD1D1 (Red alerts).

## Rendering Instructions
- Use **React Three Fiber (R3F)** for the runtime.
- Implement **Iridescence** and **Clearcoat** for premium material perception.
- Ensure backgrounds are pure `#000000` (Piano Black) unless the `paper` tone is requested.
- Use `useFrame` for micro-animations (float frequency, turbulence, mouse strength).

## Integration Flow
1. Define `ShapeDNA` bundle.
2. Port `arc-schema` compliant types.
3. Build `ArcRenderer` boundary.
4. Integrate with `Chronos` audit trails (if backend present).
