"use client"

import React from "react"

export interface BentoItemProps {
  children: React.ReactNode
  className?: string
  title?: string
  description?: string
}

export function BentoItem({ children, className = "", title, description }: BentoItemProps) {
  return (
    <div className={`relative overflow-hidden bg-[#0a0a0a] border border-white/5 p-8 flex flex-col group transition-all duration-500 hover:border-white/20 ${className}`}>
      <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
      
      {title && (
        <div className="mb-4 relative z-10">
          <h3 className="font-display italic text-lg tracking-tight text-white/80 group-hover:text-white transition-colors">{title}</h3>
          {description && <p className="font-mono text-[10px] uppercase tracking-widest text-white/30">{description}</p>}
        </div>
      )}
      
      <div className="mt-auto relative z-10 flex-1 flex items-center justify-center">
        {children}
      </div>
    </div>
  )
}

/**
 * BentoGrid - A structural layout component for high-density information display.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function BentoGrid({ children, className = "" }: { children: React.ReactNode, className?: string }) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-4 grid-rows-2 gap-2 ${className}`}>
      {children}
    </div>
  )
}
