"use client"

import { LayeredText } from "./index"

export default function LayeredTextDemo() {
  return (
    <div className="relative w-full min-h-screen bg-zinc-950 flex flex-col items-center justify-center p-24">
      {/* Editorial Grid Background */}
      <div className="absolute inset-0 z-0 opacity-10" 
        style={{ 
          backgroundImage: `linear-gradient(#ffffff 1px, transparent 1px), linear-gradient(90deg, #ffffff 1px, transparent 1px)`,
          backgroundSize: '40px 40px'
        }} 
      />

      {/* Header Context */}
      <div className="absolute top-24 left-24 z-10 flex items-center gap-4">
        <div className="w-12 h-[1px] bg-white/40" />
        <p className="text-[11px] font-mono text-white/40 uppercase tracking-[0.4em]">
          Isometric Projection / v1.20.0
        </p>
      </div>

      {/* Main Component */}
      <div className="relative z-10">
        <LayeredText 
          className="scale-90 md:scale-100"
          fontSize="8vw"
          fontSizeMd="40px"
          lineHeight={100}
        />
      </div>

      {/* Bottom Metadata */}
      <div className="absolute bottom-24 right-24 z-10 text-right space-y-2">
        <p className="text-[10px] font-mono text-white/20 uppercase tracking-widest">
          Brutalist Type Stack
        </p>
        <p className="text-[10px] font-mono text-white/10 uppercase tracking-widest">
          Aurora Visual Assets Library
        </p>
      </div>

      {/* Noise Overlay */}
      <div className="absolute inset-0 pointer-events-none bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-[0.03] z-20" />
    </div>
  )
}
