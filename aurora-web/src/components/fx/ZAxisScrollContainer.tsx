import React, { useRef, useEffect, useState } from 'react';

export interface PerformanceBudget {
  desktopFps: number;
  mobileFps: number;
  maxLayers: number;
}

export interface FallbackOptions {
  mobile: 'reduced_depth' | 'static_sections';
  reducedMotion: 'static_depth_sections' | 'fade_sections';
}

export interface ZAxisScrollContainerProps {
  enabled?: boolean;
  quality?: 'low' | 'med' | 'high';
  reducedMotion?: boolean;
  depth?: number;
  scrollAxis?: 'vertical_input_to_z' | 'horizontal_input_to_z';
  performanceBudget?: PerformanceBudget;
  fallback?: FallbackOptions;
  children?: React.ReactNode;
}

export const ZAxisScrollContainer: React.FC<ZAxisScrollContainerProps> = ({
  enabled = true,
  quality = 'med',
  reducedMotion = false,
  depth = 5000,
  scrollAxis = 'vertical_input_to_z',
  performanceBudget = { desktopFps: 60, mobileFps: 30, maxLayers: 5 },
  fallback = { mobile: 'reduced_depth', reducedMotion: 'static_depth_sections' },
  children
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [scrollProgress, setScrollProgress] = useState(0); // 0 to 1
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    // Detect mobile
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  useEffect(() => {
    if (!enabled) return;

    // Determine fallbacks
    const isReduced = reducedMotion || (typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

    if (isMobile && fallback.mobile === 'static_sections') {
      return; // Do not bind scroll listener, fallback to natural flow
    }
    if (isReduced && fallback.reducedMotion === 'static_depth_sections') {
      return; // Fallback to static depth stacking without active scroll binding
    }

    const handleScroll = () => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const scrolled = window.scrollY;
      const totalHeight = containerRef.current.scrollHeight - window.innerHeight;
      
      if (totalHeight <= 0) return;
      const progress = Math.min(Math.max(scrolled / totalHeight, 0), 1);
      setScrollProgress(progress);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, [enabled, isMobile, reducedMotion, fallback]);

  // CSS custom properties for hardware acceleration
  // We avoid mutating top/left/height/width/margin to prevent CLS.
  const containerStyle: React.CSSProperties = {
    position: 'relative',
    width: '100%',
    // High quality sets active hardware-acceleration hints
    perspective: quality === 'low' ? 'none' : '1000px',
    perspectiveOrigin: '50% 50%',
    overflow: 'hidden',
    contain: 'layout paint', // prevents browser reflow of unrelated page elements
  };

  // If mobile static fallback is triggered, render as standard flow
  if (isMobile && fallback.mobile === 'static_sections') {
    return (
      <div ref={containerRef} style={{ position: 'relative', width: '100%' }}>
        {children}
      </div>
    );
  }

  // Pass scroll state downstream using React Context or CSS variables
  const currentZTranslate = -scrollProgress * depth;

  const innerStyle: React.CSSProperties = {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    // Hardware accelerated translation & transform hints
    transform: `translate3d(0, 0, ${currentZTranslate}px)`,
    transformStyle: 'preserve-3d',
    willChange: quality === 'high' ? 'transform' : 'auto',
    contain: 'layout paint',
  };

  // Dummy scroll spacer to enable native scrollbar movement
  const spacerStyle: React.CSSProperties = {
    height: `${depth / 5 + window.innerHeight}px`,
    width: '100%',
    pointerEvents: 'none',
  };

  return (
    <div ref={containerRef} style={containerStyle}>
      <div style={innerStyle}>
        {React.Children.map(children, (child) => {
          if (React.isValidElement(child)) {
            return React.cloneElement(child as React.ReactElement<any>, {
              scrollProgress,
              totalDepth: depth,
              quality,
            });
          }
          return child;
        })}
      </div>
      <div style={spacerStyle} />
    </div>
  );
};
