"use client"

import React from "react"

/**
 * NoiseGrain - A subtle animated texture overlay using SVG filters.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function NoiseGrain({ opacity = 0.05, className = "" }) {
  const filterId = "noise-grain-filter"

  return (
    <div className={`pointer-events-none fixed inset-0 z-[50] ${className}`}>
      <svg className="h-full w-full" xmlns="http://www.w3.org/2000/svg">
        <filter id={filterId}>
          <feTurbulence 
            type="fractalNoise" 
            baseFrequency="0.65" 
            numOctaves="3" 
            stitchTiles="stitch" 
          />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect 
          width="100%" 
          height="100%" 
          filter={`url(#${filterId})`} 
          className="opacity-[var(--grain-opacity)]"
          style={{ "--grain-opacity": opacity } as React.CSSProperties}
        />
      </svg>
      
      {/* Animation Overlay (Optional via CSS) */}
      <div className="absolute inset-0 bg-transparent animate-grain mix-blend-overlay pointer-events-none" />
      
      <style jsx>{`
        @keyframes grain {
          0%, 100% { transform: translate(0, 0); }
          10% { transform: translate(-5%, -10%); }
          20% { transform: translate(-15%, 5%); }
          30% { transform: translate(7%, -25%); }
          40% { transform: translate(-5%, 25%); }
          50% { transform: translate(-15%, 10%); }
          60% { transform: translate(15%, 0%); }
          70% { transform: translate(0%, 15%); }
          80% { transform: translate(3%, 35%); }
          90% { transform: translate(-10%, 10%); }
        }
        .animate-grain {
          animation: grain 8s steps(10) infinite;
        }
      `}</style>
    </div>
  )
}
