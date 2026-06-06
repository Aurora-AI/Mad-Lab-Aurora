import React from 'react';

export interface LayerPortalProps {
  depth: number; // The Z-index depth step of this layer (e.g., 0, 1000, 2000)
  scrollProgress?: number; // Inherited from parent (0 to 1)
  totalDepth?: number; // Total depth units of parent container
  quality?: 'low' | 'med' | 'high';
  children?: React.ReactNode;
}

export const LayerPortal: React.FC<LayerPortalProps> = ({
  depth,
  scrollProgress = 0,
  totalDepth = 5000,
  quality = 'med',
  children
}) => {
  // Translate depth layers safely.
  // We place each layer at its static Z position. 
  // The ZAxisScrollContainer handles moving the master viewport through the Z axis.
  // The absolute position of the layers stays static in the 3D space, meaning zero CLS.
  
  const layerZ = -depth;
  
  const style: React.CSSProperties = {
    position: 'absolute',
    width: '100%',
    height: '100%',
    top: 0,
    left: 0,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    // Apply translate3d for hardware acceleration and layout shift prevention
    transform: `translate3d(0, 0, ${layerZ}px)`,
    transformStyle: 'preserve-3d',
    willChange: quality === 'high' ? 'transform, opacity' : 'auto',
    contain: 'layout paint', // isolate layer rendering
  };

  // Dynamic opacity fade-out based on how close the layer is to the screen
  // If the viewport has scrolled past this layer, we fade it out
  const currentViewportZ = scrollProgress * totalDepth;
  
  // Calculate relative distance
  const relativeDistance = depth - currentViewportZ;
  
  let opacity = 1;
  if (relativeDistance < 0) {
    // Scroll past: fade out quickly
    opacity = Math.max(1 + relativeDistance / 500, 0);
  } else if (relativeDistance > 2000) {
    // Too far in the distance: fade out
    opacity = Math.max(1 - (relativeDistance - 2000) / 1000, 0);
  }

  const innerStyle: React.CSSProperties = {
    width: '100%',
    height: '100%',
    opacity: quality === 'low' ? 1.0 : opacity,
    transition: 'opacity 0.1s linear',
    pointerEvents: relativeDistance < -100 ? 'none' : 'auto', // disable interactions for passed layers
  };

  return (
    <div style={style}>
      <div style={innerStyle}>
        {children}
      </div>
    </div>
  );
};
