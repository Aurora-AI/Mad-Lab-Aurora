"use client"

import React, { useRef, useState } from "react"
import { motion, useSpring } from "framer-motion"

export interface MagneticCardProps {
  title: string
  category: string
  className?: string
}

function Card({ title, category, mouseX, mouseY }: any) {
  const ref = useRef<HTMLDivElement>(null)
  
  // Spring options for smooth magnetic pull
  const springOptions = { damping: 20, stiffness: 150, mass: 0.1 }
  const x = useSpring(0, springOptions)
  const y = useSpring(0, springOptions)

  React.useEffect(() => {
    if (!ref.current) return
    const rect = ref.current.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2
    
    // Magnetic pull logic
    const distanceX = mouseX - centerX
    const distanceY = mouseY - centerY
    const distance = Math.sqrt(distanceX ** 2 + distanceY ** 2)
    
    if (distance < 300) {
      const power = (300 - distance) / 300
      x.set(distanceX * power * 0.2)
      y.set(distanceY * power * 0.2)
    } else {
      x.set(0)
      y.set(0)
    }
  }, [mouseX, mouseY, x, y])

  return (
    <motion.div
      ref={ref}
      style={{ x, y }}
      className="p-6 bg-[#0a0a0a] border border-white/5 h-48 flex flex-col justify-between group"
    >
      <span className="font-mono text-[8px] uppercase tracking-[0.4em] opacity-20 group-hover:opacity-100 transition-opacity">
        {category}
      </span>
      <h4 className="font-display italic text-2xl tracking-tighter text-white/50 group-hover:text-white transition-colors">
        {title}
      </h4>
    </motion.div>
  )
}

/**
 * MagneticCards - A grid of elements that move locally towards the cursor.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function MagneticCards({ items = [] }: { items?: Array<{title: string, category: string}> }) {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 })

  const handleMouseMove = (e: React.MouseEvent) => {
    setMousePos({ x: e.clientX, y: e.clientY })
  }

  return (
    <div 
      onMouseMove={handleMouseMove}
      className="grid grid-cols-1 md:grid-cols-3 gap-4 p-8 bg-black/50"
    >
      {items.map((item, idx) => (
        <Card key={idx} {...item} mouseX={mousePos.x} mouseY={mousePos.y} />
      ))}
    </div>
  )
}
