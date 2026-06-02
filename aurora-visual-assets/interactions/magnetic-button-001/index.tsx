"use client"

import React, { useRef, useState } from "react"
import { motion, useSpring, useTransform } from "framer-motion"

export interface MagneticButtonProps {
  children: React.ReactNode
  distance?: number
  className?: string
  onClick?: () => void
}

/**
 * MagneticButton - A component that pulls towards the cursor using physics-based attraction.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function MagneticButton({ 
  children, 
  distance = 0.35, 
  className = "",
  onClick 
}: MagneticButtonProps) {
  const ref = useRef<HTMLDivElement>(null)

  // Spring physics configuration
  const springOptions = { damping: 15, stiffness: 150, mass: 0.1 }
  const x = useSpring(0, springOptions)
  const y = useSpring(0, springOptions)

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!ref.current) return
    const { clientX, clientY } = e
    const { height, width, left, top } = ref.current.getBoundingClientRect()
    
    // Calculate distance from element center
    const middleX = clientX - (left + width / 2)
    const middleY = clientY - (top + height / 2)

    // Pull strength
    x.set(middleX * distance)
    y.set(middleY * distance)
  }

  const handleMouseLeave = () => {
    x.set(0)
    y.set(0)
  }

  return (
    <motion.div
      ref={ref}
      style={{ x, y }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      className={`relative inline-block ${className}`}
    >
      {children}
    </motion.div>
  )
}
