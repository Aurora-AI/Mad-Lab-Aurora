"use client"

import React, { useState } from "react"
import type { LucideIcon } from "lucide-react"

export interface FluidMenuItemProps {
  children?: React.ReactNode
  onClick?: () => void
  disabled?: boolean
  icon?: React.ReactNode
  isActive?: boolean
}

export function FluidMenuItem({ 
  children, 
  onClick, 
  disabled = false, 
  icon, 
  isActive = false 
}: FluidMenuItemProps) {
  return (
    <button
      className={`relative block w-full h-16 text-center group transition-all duration-300
        ${disabled ? "opacity-30 cursor-not-allowed" : "opacity-70 hover:opacity-100"}
        ${isActive ? "bg-white/10" : ""}
      `}
      role="menuitem"
      onClick={!disabled ? onClick : undefined}
      disabled={disabled}
    >
      <span className="flex items-center justify-center h-full">
        {icon && (
          <span className="h-6 w-6 transition-all duration-300 group-hover:scale-110">
            {icon}
          </span>
        )}
        {children && <span className="ml-2 font-mono text-[10px] uppercase tracking-widest">{children}</span>}
      </span>
    </button>
  )
}

export interface FluidMenuProps {
  children: React.ReactNode
  className?: string
  accentColor?: string
}

/**
 * FluidMenu - A vertical navigation expansion with circular reveal physics.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function FluidMenu({ 
  children, 
  className = "",
  accentColor = "var(--page-text)"
}: FluidMenuProps) {
  const [isExpanded, setIsExpanded] = useState(false)
  const childrenArray = React.Children.toArray(children)

  return (
    <div className={`relative w-[64px] ${className}`} data-expanded={isExpanded}>
      <div className="relative">
        {/* Toggle / First Item */}
        <div 
          className="relative w-16 h-16 bg-[#0a0a0a] border border-white/10 cursor-pointer rounded-full group will-change-transform z-50 flex items-center justify-center transition-all duration-500 hover:border-white/30"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <div className="relative w-6 h-6 flex items-center justify-center">
             <span className={`absolute w-full h-0.5 bg-current transition-all duration-500 ${isExpanded ? 'rotate-45' : '-translate-y-1'}`} />
             <span className={`absolute w-full h-0.5 bg-current transition-all duration-500 ${isExpanded ? '-rotate-45' : 'translate-y-1'}`} />
          </div>
        </div>

        {/* Expansion Items */}
        {childrenArray.map((child, index) => (
          <div 
            key={index} 
            className="absolute top-0 left-0 w-16 h-16 bg-[#0f0f0f] border border-white/5 will-change-transform flex items-center justify-center"
            style={{
              transform: `translateY(${isExpanded ? (index + 1) * 64 : 0}px)`,
              opacity: isExpanded ? 1 : 0,
              zIndex: 40 - index,
              clipPath: "circle(50% at 50% 50%)",
              transition: `transform ${isExpanded ? '500ms' : '400ms'} cubic-bezier(0.19, 1, 0.22, 1) ${isExpanded ? index * 50 : 0}ms,
                         opacity ${isExpanded ? '400ms' : '200ms'} ${isExpanded ? index * 50 : 0}ms`,
            }}
          >
            {child}
          </div>
        ))}
      </div>
    </div>
  )
}
