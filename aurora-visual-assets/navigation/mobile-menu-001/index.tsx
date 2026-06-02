"use client"

import React, { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Menu, X, ArrowRight } from "lucide-react"

/**
 * MobileMenu - A high-fidelity mobile navigation overlay with staggered entry physics.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false)

  const menuItems = [
    { name: "Produtos", href: "#" },
    { name: "Laboratório", href: "#" },
    { name: "Manifesto", href: "#" },
    { name: "Arsenal", href: "#" },
  ]

  return (
    <div className="md:hidden">
      <button
        onClick={() => setIsOpen(true)}
        className="p-2 text-[var(--page-text)] opacity-70 hover:opacity-100 transition-all duration-300"
      >
        <Menu size={24} />
      </button>

      <AnimatePresence>
        {isOpen && (
          <>
            {/* Backdrop */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
              className="fixed inset-0 z-[190] bg-black/80 backdrop-blur-sm"
            />

            {/* Menu Panel */}
            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", damping: 30, stiffness: 200 }}
              className="fixed inset-y-0 right-0 z-[200] w-full max-w-sm bg-[#050505] border-l border-white/5 p-8 flex flex-col shadow-2xl"
            >
              <div className="flex justify-between items-center mb-16">
                <span className="font-mono text-[8px] uppercase tracking-[0.5em] opacity-30">
                  [ Aurora // Mobile Nav ]
                </span>
                <button 
                  onClick={() => setIsOpen(false)}
                  className="p-2 text-white/40 hover:text-white transition-colors"
                >
                  <X size={24} />
                </button>
              </div>

              <nav className="flex flex-col gap-2">
                {menuItems.map((item, idx) => (
                  <motion.a
                    key={item.name}
                    href={item.href}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 + idx * 0.08 }}
                    className="group flex items-center justify-between py-5 border-b border-white/[0.03] last:border-0"
                  >
                    <span className="font-display italic text-4xl tracking-tighter transition-all duration-500 group-hover:pl-2 group-hover:text-white text-white/70">
                      {item.name}
                    </span>
                    <ArrowRight size={20} className="opacity-0 group-hover:opacity-100 -translate-x-4 group-hover:translate-x-0 transition-all duration-500 text-white/40" />
                  </motion.a>
                ))}
              </nav>

              <div className="mt-auto pt-12">
                 <div className="grid grid-cols-2 gap-8 border-t border-white/5 pt-12">
                   <div className="flex flex-col gap-3">
                     <span className="font-mono text-[8px] uppercase tracking-widest opacity-20">Support</span>
                     <span className="text-[10px] font-mono opacity-50 hover:opacity-100 transition-opacity cursor-pointer">lex@aurora.is</span>
                   </div>
                   <div className="flex flex-col gap-3">
                     <span className="font-mono text-[8px] uppercase tracking-widest opacity-20">Factory</span>
                     <span className="text-[10px] font-mono opacity-50 hover:opacity-100 transition-opacity cursor-pointer">MadLab // HQ</span>
                   </div>
                 </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  )
}
