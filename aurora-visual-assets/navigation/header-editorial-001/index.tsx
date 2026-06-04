"use client"

import React from "react"
import { motion } from "framer-motion"

export interface HeaderEditorialProps {
  logo?: React.ReactNode
  links?: Array<{ label: string; href: string }>
  className?: string
}

/**
 * HeaderEditorial - A minimalist, high-typography header focused on hierarchy and silence.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function HeaderEditorial({
  logo = "AURORA",
  links = [
    { label: "Arsenal", href: "#" },
    { label: "Lab", href: "#" },
    { label: "Docs", href: "#" },
  ],
  className = ""
}: HeaderEditorialProps) {
  return (
    <header className={`w-full py-8 px-[var(--px)] flex items-center justify-between mix-blend-difference z-[100] ${className}`}>
      {/* Brand */}
      <motion.div
        initial={{ opacity: 0, x: -10 }}
        animate={{ opacity: 1, x: 0 }}
        className="font-display font-black text-xs uppercase tracking-[0.4em] text-white"
      >
        {typeof logo === "string" ? logo : logo}
      </motion.div>

      {/* Navigation */}
      <nav className="flex items-center gap-12">
        {links.map((link, idx) => (
          <motion.a
            key={link.label}
            href={link.href}
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + idx * 0.05 }}
            className="font-mono text-[9px] uppercase tracking-[0.15em] text-white/50 hover:text-white transition-colors relative group"
          >
            {link.label}
            <span className="absolute -bottom-1 left-0 w-0 h-[1px] bg-white transition-all duration-300 group-hover:w-full" />
          </motion.a>
        ))}
      </nav>

      {/* Visual Marker */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        className="hidden md:flex items-center gap-2"
      >
        <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse" />
        <span className="font-mono text-[8px] uppercase tracking-widest opacity-20">Live // HQ</span>
      </motion.div>
    </header>
  )
}
