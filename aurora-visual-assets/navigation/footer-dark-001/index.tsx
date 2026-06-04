"use client"

import React from "react"

/**
 * FooterDark - A minimalist, high-contrast footer with editorial spacing.
 * Part of the Aurora Visual Arsenal // Expansion 1.0.
 */
export function FooterDark() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="w-full bg-[#050505] border-t border-white/5 py-24 px-[var(--px)]">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between gap-16">
        {/* Left Side: Brand & Mission */}
        <div className="flex-1">
          <div className="font-display italic text-5xl tracking-tighter mb-8 text-white">
            Aurora.
          </div>
          <p className="font-mono text-[10px] uppercase tracking-widest text-white/30 leading-relaxed max-w-xs">
            Architecting the next generation of visual sovereignty through agentic engineering and dark editorial aesthetics.
          </p>
        </div>

        {/* Right Side: Links Grid */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-12 flex-[2]">
          <div className="flex flex-col gap-6">
            <span className="font-mono text-[8px] uppercase tracking-[0.4em] opacity-20">Arsenal</span>
            <ul className="flex flex-col gap-3 font-mono text-[10px] uppercase tracking-widest opacity-60">
              <li className="hover:opacity-100 cursor-pointer transition-opacity">Visual Components</li>
              <li className="hover:opacity-100 cursor-pointer transition-opacity">Motion Library</li>
              <li className="hover:opacity-100 cursor-pointer transition-opacity">Lab Reports</li>
            </ul>
          </div>
          <div className="flex flex-col gap-6">
            <span className="font-mono text-[8px] uppercase tracking-[0.4em] opacity-20">Connect</span>
            <ul className="flex flex-col gap-3 font-mono text-[10px] uppercase tracking-widest opacity-60">
              <li className="hover:opacity-100 cursor-pointer transition-opacity">X // Twitter</li>
              <li className="hover:opacity-100 cursor-pointer transition-opacity">Discord HQ</li>
              <li className="hover:opacity-100 cursor-pointer transition-opacity">GitHub Vault</li>
            </ul>
          </div>
          <div className="flex flex-col gap-6">
            <span className="font-mono text-[8px] uppercase tracking-[0.4em] opacity-20">Legal</span>
            <ul className="flex flex-col gap-3 font-mono text-[10px] uppercase tracking-widest opacity-60">
              <li className="hover:opacity-100 cursor-pointer transition-opacity">Privacy Policy</li>
              <li className="hover:opacity-100 cursor-pointer transition-opacity">Service Protocol</li>
            </ul>
          </div>
        </div>
      </div>

      <div className="mt-24 pt-12 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="font-mono text-[8px] uppercase tracking-[0.5em] opacity-10">
          © {currentYear} Aurora // MadLab Factory
        </div>
        <div className="flex gap-4">
           <div className="w-1 h-1 rounded-full bg-blue-500" />
           <span className="font-mono text-[8px] uppercase tracking-widest opacity-20 text-blue-500/50">All systems operational</span>
        </div>
      </div>
    </footer>
  )
}
