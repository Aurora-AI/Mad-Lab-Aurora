"use client"

import React, { useRef } from "react"
import { motion, useScroll, useTransform } from "framer-motion"

export interface RevealTextProps {
  text: string
  className?: string
}

/**
 * RevealText - A component that reveals text opacity and position based on scroll progress.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function RevealText({ text, className = "" }: RevealTextProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"]
  })

  // Multiple words splitting logic
  const words = text.split(" ")

  return (
    <div ref={containerRef} className={`relative py-24 ${className}`}>
      <div className="flex flex-wrap gap-4 justify-center items-center">
        {words.map((word, i) => {
          const start = i / words.length
          const end = start + (1 / words.length)
          
          // eslint-disable-next-line react-hooks/rules-of-hooks
          const opacity = useTransform(scrollYProgress, [start, end], [0.1, 1])
          // eslint-disable-next-line react-hooks/rules-of-hooks
          const y = useTransform(scrollYProgress, [start, end], [20, 0])

          return (
            <motion.span
              key={i}
              style={{ opacity, y }}
              className="font-display italic text-6xl md:text-8xl tracking-tighter text-white"
            >
              {word}
            </motion.span>
          )
        })}
      </div>
    </div>
  )
}
