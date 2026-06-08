'use client';
/**
 * SYNTHESIZED BY AURORA FRONTEND FACTORY
 * SPEC_ID: SPEC-OS019-MAD-LAB-001
 * TRUSTWARE CERTIFIED
 * FX: Z-axis tunnel — prefers-reduced-motion via useReducedMotion (fail-closed)
 */

import React from 'react';
import { AuroraButton } from '@/components/core';
import { AuroraHeading } from '@/components/core';
import { LayerPortal } from '@/components/fx';
import { ZAxisScrollContainer } from '@/components/fx';

/**
 * useReducedMotion — reads prefers-reduced-motion from the system at runtime.
 * Fail-closed: returns true (motion disabled) when the media query API is unavailable (SSR).
 * OS-019 / Mad Lab Theme — accessibility contract.
 */
function useReducedMotion(): boolean {
  const [reducedMotion, setReducedMotion] = React.useState<boolean>(() => {
    if (typeof window === 'undefined') return true;
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  });
  React.useEffect(() => {
    if (typeof window === 'undefined') return;
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)');
    const onChange = (e: MediaQueryListEvent) => setReducedMotion(e.matches);
    mq.addEventListener('change', onChange);
    return () => mq.removeEventListener('change', onChange);
  }, []);
  return reducedMotion;
}

export default function SynthesizedPage() {
  // prefers-reduced-motion — read once on mount, reactive to system changes.
  // Fail-closed: returns true (no motion) when window is unavailable (SSR).
  const systemReducedMotion = useReducedMotion();
  return (
    <ZAxisScrollContainer enabled quality="high" depth={3000} scrollAxis="vertical_input_to_z" performanceBudget={{"targetFps": 60, "maxLayers": 8}} fallback="static_depth_sections" reducedMotion={systemReducedMotion} className="w-full min-h-screen bg-base-surface">
      <LayerPortal zPosition={0} scaleFactor={1.0} opacityLimit={1.0} visible reducedMotion={systemReducedMotion}>
        <AuroraHeading className="text-5xl font-bold text-text-primary tracking-tight">
          Mad Lab Aurora
        </AuroraHeading>
        <AuroraButton variant="primary" className="mt-8 px-10 py-4">
          Explorar o Sistema
        </AuroraButton>
      </LayerPortal>
      <LayerPortal zPosition={-800} scaleFactor={0.85} opacityLimit={0.8} visible reducedMotion={systemReducedMotion}>
        <div className="text-2xl text-text-secondary font-sans max-w-2xl text-center">
          A fabrica cognitiva que materializa produto a partir de fisica de profundidade.
        </div>
      </LayerPortal>
      <LayerPortal zPosition={-2000} scaleFactor={0.6} opacityLimit={0.5} visible reducedMotion={systemReducedMotion}>
        <div className="text-lg text-editorial-warm tracking-widest uppercase">
          Depth Horizon — Aurora Factory
        </div>
      </LayerPortal>
    </ZAxisScrollContainer>
  );
}
