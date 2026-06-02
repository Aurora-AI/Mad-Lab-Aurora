"use client"

import React from "react"

export interface GooeyButtonProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
  color?: string
}

/**
 * GooeyButton - A button that uses SVG filters to create a liquid, morphing effect.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function GooeyButton({ 
  children, 
  className = "",
  onClick,
  color = "var(--page-text)"
}: GooeyButtonProps) {
  const filterId = "gooey-filter-aurora"

  return (
    <div className={`relative group ${className}`}>
      {/* SVG Filter Definition */}
      <svg className="absolute w-0 h-0 invisible" aria-hidden="true">
        <defs>
          <filter id={filterId}>
            <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
            <feColorMatrix 
              in="blur" 
              mode="matrix" 
              values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7" 
              result="goo" 
            />
            <feComposite in="SourceGraphic" in2="goo" operator="atop" />
          </filter>
        </defs>
      </svg>

      <div 
        className="flex items-center gap-2"
        style={{ filter: `url(#${filterId})` }}
      >
        <button
          onClick={onClick}
          className="relative px-8 py-4 bg-white text-black font-display italic text-sm rounded-full z-10 hover:scale-105 transition-transform"
        >
          {children}
        </button>
        
        {/* Gooey Blobs */}
        <div className="absolute top-1/2 left-full -translate-x-8 -translate-y-1/2 w-8 h-8 bg-white rounded-full opacity-0 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-500" />
        <div className="absolute top-1/2 right-full translate-x-8 -translate-y-1/2 w-6 h-6 bg-white rounded-full opacity-0 group-hover:opacity-100 group-hover:-translate-x-0 transition-all duration-700 delay-75" />
      </div>
    </div>
  )
}
