'use client';
/**
 * AURORA FRONTEND FACTORY — FX COMPONENT
 * LayerPortal
 *
 * Responsibility:
 *   Positions content layers in Z-axis depth using GPU-safe transforms.
 *   Each layer occupies a specific depth position within the tunnel context.
 *   This component controls POSITION and VISIBILITY — not structure or layout.
 *
 * Governance:
 *   - OS-019-M0: Mad Lab Theme Canonization & Z-Axis Capability Alignment
 *   - Zero Layout Shift guarantee: only transform, opacity, clip-path used.
 *   - PROHIBITED animations: top, left, height, width, margin, padding.
 *   - contain: layout paint is mandatory to isolate reflow.
 *   - will-change is restricted to 'transform' only when visible in viewport.
 *   - prefers-reduced-motion: all transforms disabled when active.
 *
 * Depth model:
 *   Each layer receives a z-position (e.g., -1000px = 1000px behind viewer).
 *   Scale and opacity are derived from depth to simulate natural perspective fog.
 *   The further a layer, the smaller and more transparent it appears.
 */

import React, { ReactNode, useId } from 'react';

export interface LayerPortalProps {
  /**
   * Absolute Z-axis position for this layer (in pixels).
   * Negative = further away. 0 = at viewer plane. Positive = in front.
   * Example: -1000 places the layer 1000px behind the viewer.
   */
  zPosition: number;
  /**
   * Visual scale factor for this layer.
   * Derived from depth: 1.0 = full size, 0.5 = half size.
   * Must be between 0.1 and 1.0.
   */
  scaleFactor: number;
  /**
   * Maximum opacity limit for this layer (0.0–1.0).
   * Layers deeper in the tunnel can have lower maximum opacity to simulate fog.
   */
  opacityLimit?: number;
  /**
   * Whether the layer is currently within the visible depth range.
   * Hidden layers skip will-change to reduce GPU pressure.
   */
  visible?: boolean;
  /**
   * When true, disables all transforms and renders at natural position.
   * Required for prefers-reduced-motion compliance.
   */
  reducedMotion?: boolean;
  children: ReactNode;
  className?: string;
  /** Test / QA identifier for this layer. */
  layerId?: string;
}

/**
 * LayerPortal
 *
 * Places content at a specific depth position within a Z-axis tunnel context.
 * Parent MUST be a ZAxisScrollContainer or any element with `transformStyle: preserve-3d`.
 *
 * Zero Layout Shift contract:
 *   - Uses only `transform: translate3d()`, `scale`, `opacity`.
 *   - Does not animate `top`, `left`, `height`, `margin`, or `padding`.
 *   - `position: absolute` removes from flow — does not cause reflow.
 *   - `contain: layout paint` prevents internal layout from escaping.
 */
export function LayerPortal({
  zPosition,
  scaleFactor,
  opacityLimit = 1.0,
  visible = true,
  reducedMotion = false,
  children,
  className,
  layerId,
}: LayerPortalProps) {
  const generatedId = useId();
  const id = layerId ?? `layer-portal-${generatedId}`;

  // Reduced motion: render at natural position, no 3D transform
  if (reducedMotion) {
    return (
      <div
        id={id}
        className={className}
        data-fx="layer-portal"
        data-z-position={zPosition}
        data-reduced-motion="true"
        data-visible={String(visible)}
        style={{
          // Absolute position removes from document flow — zero reflow
          position: 'absolute',
          inset: 0,
          opacity: opacityLimit,
          // contain prevents internal changes from triggering parent layout
          contain: 'layout paint',
        }}
      >
        {children}
      </div>
    );
  }

  // Clamp scaleFactor to prevent extreme distortions
  const clampedScale = Math.max(0.1, Math.min(1.0, scaleFactor));

  // Opacity decreases with depth to simulate perspective fog
  // Layers at z=0 are fully visible; layers at extreme negative z fade out
  const depthOpacityModifier = zPosition < 0
    ? Math.max(0.05, 1 + zPosition / 5000)
    : 1.0;
  const resolvedOpacity = Math.min(opacityLimit, depthOpacityModifier);

  return (
    <div
      id={id}
      className={className}
      data-fx="layer-portal"
      data-z-position={zPosition}
      data-scale={clampedScale}
      data-visible={String(visible)}
      style={{
        // Absolute position removes this layer from document flow — zero CLS
        position: 'absolute',
        inset: 0,
        // GPU-safe transforms only:
        //   translate3d(0,0,z) → depth position
        //   scale → perspective-correct sizing
        // PROHIBITED: top, left, height, width, margin, padding
        transform: `translate3d(0, 0, ${zPosition}px) scale(${clampedScale})`,
        transformOrigin: '50% 50%',
        opacity: resolvedOpacity,
        // Restricted will-change: only applied when layer is visible
        // Avoids GPU memory pressure for off-screen layers
        willChange: visible ? 'transform' : 'auto',
        // contain: layout paint isolates reflow — mandatory for zero CLS
        contain: 'layout paint',
        // clip-path is allowed for visual masking (no layout impact)
        // Uncomment when specific masking is needed:
        // clipPath: 'inset(0)',
      }}
    >
      {children}
    </div>
  );
}
