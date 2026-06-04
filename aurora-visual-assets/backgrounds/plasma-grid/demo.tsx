"use client"

import ShaderBackground from "./index"

export default function PlasmaGridDemo() {
  return (
    <div className="relative w-full h-screen bg-black overflow-hidden select-none">
      {/* Background Layer: Bare-Metal WebGL Grid */}
      <ShaderBackground className="absolute inset-0 opacity-80" />
      
      {/* Editorial Content Overlay */}
      <div className="relative z-10 w-full h-full flex flex-col items-center justify-center p-8">
        <div className="max-w-4xl w-full text-center space-y-8">
          <div className="inline-block px-4 py-1.5 rounded-full border border-white/10 bg-white/5 backdrop-blur-md">
            <span className="text-[10px] font-mono text-zinc-400 uppercase tracking-[0.3em]">
              System Protocol: WebGL 1.0 (Bare Metal)
            </span>
          </div>
          
          <h1 className="text-7xl md:text-9xl font-bold text-white tracking-tighter leading-none italic">
            NEON<br />
            <span className="text-white/10">STREAMS</span>
          </h1>
          
          <div className="flex items-center justify-center gap-12 font-mono text-[10px] text-zinc-500 uppercase tracking-widest pt-8 border-t border-white/5">
            <div className="flex flex-col gap-1 items-center">
              <span className="text-white/40">Efficiency</span>
              <span>100% Native</span>
            </div>
            <div className="flex flex-col gap-1 items-center">
              <span className="text-white/40">Resolution</span>
              <span>Dynamic Viewport</span>
            </div>
            <div className="flex flex-col gap-1 items-center">
              <span className="text-white/40">Pattern</span>
              <span>P031/P032</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Vignette & Grain */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_center,transparent_0%,black_100%)] opacity-60 z-20" />
    </div>
  )
}
