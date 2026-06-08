/**
 * AURORA FRONTEND FACTORY — FX Components
 *
 * Export index for @/components/fx
 *
 * Governance: OS-019-M0 — Mad Lab Theme Canonization & Z-Axis Capability Alignment
 *
 * Usage:
 *   import { ZAxisScrollContainer, LayerPortal } from '@/components/fx';
 *
 * Import contract (tsx_compiler.py):
 *   The compiler imports these components ONLY when they appear in the UI tree.
 *   An orphan import (imported but unused) is a P1 violation in the StoriesBuilderGate.
 */

export { ZAxisScrollContainer } from './ZAxisScrollContainer';
export type {
  ZAxisScrollContainerProps,
  ZAxisScrollQuality,
  ZAxisScrollModel,
  PerformanceBudget,
} from './ZAxisScrollContainer';

export { LayerPortal } from './LayerPortal';
export type { LayerPortalProps } from './LayerPortal';
