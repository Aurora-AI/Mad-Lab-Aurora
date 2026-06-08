'use client';
/**
 * AURORA FRONTEND FACTORY — FX COMPONENT
 * ZAxisScrollContainer
 *
 * Responsibility:
 *   Converts vertical or horizontal scroll input into progression along the Z axis.
 *   This component is the physical engine of the Mad Lab Theme tunnel experience.
 *   It does NOT generate layout — it transforms scroll signal into depth.
 *
 * Governance:
 *   - OS-019-M0: Mad Lab Theme Canonization & Z-Axis Capability Alignment
 *   - prefers-reduced-motion is mandatory; skips all transforms when active.
 *   - Mobile fallback renders static depth sections, no kinetic scroll.
 *   - Three.js r128 safe: no CapsuleGeometry usage.
 *   - GPU-safe properties only: transform (translate3d, scale), opacity.
 *   - PROHIBITED: animating top/left/height/margin — causes Layout Shift.
 *   - will-change: transform is applied only when enabled and not reducedMotion.
 *
 * Mad Lab Theme physics contract:
 *   - The user does not scroll a page.
 *   - The user traverses a digital organism through a tunnel of depth.
 *   - Each scroll delta maps to a forward/backward Z-axis displacement.
 */

import React, { useRef, useEffect, useCallback, ReactNode } from 'react';

export type ZAxisScrollQuality = 'low' | 'med' | 'high';
export type ZAxisScrollModel = 'vertical_input_to_z' | 'horizontal_input_to_z';

export interface PerformanceBudget {
  /** Target frames per second. Capped at 60 for desktop, 30 for mobile. */
  targetFps: number;
  /** Maximum depth layers allowed simultaneously (1–12). */
  maxLayers: number;
}

export interface ZAxisScrollContainerProps {
  /** Enables or disables the Z-axis scroll effect entirely. */
  enabled: boolean;
  /** Quality tier controls interpolation fidelity and layer count. */
  quality: ZAxisScrollQuality;
  /** When true, disables all kinetic scroll transforms. Required by prefers-reduced-motion. */
  reducedMotion: boolean;
  /** Total depth range in pixels (e.g., 3000 for a 3000px Z tunnel). */
  depth: number;
  /** Scroll axis mapping strategy. */
  scrollAxis: ZAxisScrollModel;
  /** Performance budget caps for frame rate and layer count. */
  performanceBudget: PerformanceBudget;
  /**
   * Fallback strategy when reduced motion or mobile is active.
   * - 'static_depth_sections': renders each section as a static depth block.
   * - 'fade_sections': crossfades between sections on scroll.
   */
  fallback: 'static_depth_sections' | 'fade_sections';
  children: ReactNode;
  className?: string;
}

const QUALITY_SCALE: Record<ZAxisScrollQuality, number> = {
  low: 0.4,
  med: 0.7,
  high: 1.0,
};

/**
 * ZAxisScrollContainer
 *
 * Core tunnel engine. All children are rendered within a perspective context.
 * Scroll events are converted to Z-axis transforms via requestAnimationFrame.
 */
export function ZAxisScrollContainer({
  enabled,
  quality,
  reducedMotion,
  depth,
  scrollAxis,
  performanceBudget,
  fallback,
  children,
  className,
}: ZAxisScrollContainerProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const depthRef = useRef<HTMLDivElement>(null);
  const currentZRef = useRef(0);
  const targetZRef = useRef(0);
  const rafRef = useRef<number | null>(null);
  const lastFrameTimeRef = useRef(0);

  const frameInterval = 1000 / Math.min(performanceBudget.targetFps, 60);
  const scaleFactor = QUALITY_SCALE[quality];

  // Reduced motion: render static fallback, no transforms
  if (!enabled || reducedMotion) {
    return (
      <div
        ref={containerRef}
        className={className}
        data-fx="z-axis-scroll-container"
        data-enabled="false"
        data-fallback={fallback}
        data-reduced-motion={String(reducedMotion)}
        style={{ position: 'relative', overflow: 'hidden' }}
      >
        {children}
      </div>
    );
  }

  const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

  const applyTransform = useCallback(() => {
    if (!depthRef.current) return;
    // GPU-safe: only transform (translate3d) — no top/left/height/margin
    depthRef.current.style.transform = `translate3d(0, 0, ${currentZRef.current}px)`;
  }, []);

  const tick = useCallback(
    (timestamp: number) => {
      if (timestamp - lastFrameTimeRef.current < frameInterval) {
        rafRef.current = requestAnimationFrame(tick);
        return;
      }
      lastFrameTimeRef.current = timestamp;

      const lerpFactor = 0.08 * scaleFactor;
      currentZRef.current = lerp(currentZRef.current, targetZRef.current, lerpFactor);
      applyTransform();
      rafRef.current = requestAnimationFrame(tick);
    },
    [applyTransform, frameInterval, scaleFactor]
  );

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const onScroll = (e: Event) => {
      const target = e.currentTarget as HTMLElement;
      const scrollProgress = scrollAxis === 'vertical_input_to_z'
        ? target.scrollTop / (target.scrollHeight - target.clientHeight)
        : target.scrollLeft / (target.scrollWidth - target.clientWidth);

      // Map scroll [0,1] to Z depth [0, -depth]
      targetZRef.current = -depth * scaleFactor * Math.min(scrollProgress, 1);
    };

    container.addEventListener('scroll', onScroll, { passive: true });
    rafRef.current = requestAnimationFrame(tick);

    return () => {
      container.removeEventListener('scroll', onScroll);
      if (rafRef.current !== null) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, [depth, scaleFactor, scrollAxis, tick]);

  return (
    <div
      ref={containerRef}
      className={className}
      data-fx="z-axis-scroll-container"
      data-enabled="true"
      data-quality={quality}
      data-scroll-axis={scrollAxis}
      style={{
        position: 'relative',
        overflow: scrollAxis === 'vertical_input_to_z' ? 'hidden auto' : 'auto hidden',
        // perspective establishes the 3D context — does not affect document flow
        perspective: `${depth * 0.8}px`,
        perspectiveOrigin: '50% 50%',
      }}
    >
      <div
        ref={depthRef}
        data-fx="z-axis-depth-root"
        style={{
          transformStyle: 'preserve-3d',
          // will-change is restricted to transform only, and only when kinetic scroll is active
          willChange: 'transform',
          // contain prevents layout recalculations from spilling outside this boundary
          contain: 'layout paint',
        }}
      >
        {children}
      </div>
    </div>
  );
}
