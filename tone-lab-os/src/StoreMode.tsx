import { ArrowRight } from "lucide-react";
import { toneLabData } from "./data";

export function StoreMode({ onSelect }: { onSelect: (id: string) => void }) {
  return (
    <div className="min-h-screen bg-[#050505] text-white pt-16 px-12 pb-24 font-sans">
      <header className="mb-16 max-w-7xl mx-auto border-b border-gray-900 pb-8">
        <h1 className="text-6xl font-bold uppercase tracking-tight mb-8 text-white">Equipment</h1>
        
        {/* Primary Categories */}
        <nav className="flex gap-8 text-xs font-bold uppercase tracking-widest text-gray-500 mb-6">
          <a href="#" className="hover:text-white transition-colors">ALL</a>
          <a href="#" className="hover:text-white transition-colors">GUITARS</a>
          <a href="#" className="text-white border-b border-white pb-1">AMPLIFIERS</a>
          <a href="#" className="hover:text-white transition-colors">PEDALS</a>
          <a href="#" className="hover:text-white transition-colors">DIGITAL</a>
          <a href="#" className="hover:text-white transition-colors">CABINETS</a>
          <a href="#" className="hover:text-white transition-colors">STUDIO</a>
        </nav>

        {/* Secondary Categories (Amps) */}
        <nav className="flex gap-6 text-[10px] font-mono uppercase tracking-widest text-gray-600">
          <a href="#" className="hover:text-white transition-colors">ALL</a>
          <a href="#" className="hover:text-white transition-colors">HEADS</a>
          <a href="#" className="text-white">COMBOS</a>
          <a href="#" className="hover:text-white transition-colors">CABINETS</a>
          <a href="#" className="hover:text-white transition-colors">ACOUSTIC</a>
          <a href="#" className="hover:text-white transition-colors">REFERENCE</a>
        </nav>
      </header>

      <div className="max-w-7xl mx-auto grid grid-cols-3 gap-2">
        {toneLabData.map((item) => (
          <div 
            key={item.id} 
            onClick={() => onSelect(item.id)}
            className="bg-[#0a0a0a] group cursor-pointer overflow-hidden flex flex-col relative h-[550px] border border-gray-900 hover:border-gray-700 transition-colors"
          >
            {/* The Image Region */}
            <div className="flex-1 flex items-center justify-center relative overflow-hidden bg-gradient-to-b from-[#111] to-[#0a0a0a]">
              <div className="absolute inset-0 w-full h-full">
                 <img src={item.image} alt={item.name} className="w-full h-full object-cover opacity-60 group-hover:opacity-100 group-hover:scale-105 transition-all duration-700 ease-out" />
              </div>
            </div>

            {/* Information Region */}
            <div className="p-8 border-t border-gray-900 bg-[#080808]">
               <div className="flex justify-between items-start mb-2">
                 <h3 className="text-xl font-bold uppercase tracking-tight text-gray-100">{item.name}</h3>
                 <span className="text-[9px] font-mono bg-white text-black px-2 py-1 uppercase font-bold tracking-widest">{item.status}</span>
               </div>
               <span className="text-[11px] font-mono text-gray-500 uppercase tracking-widest block">{item.category} / {item.subCategory}</span>
            </div>

            {/* Hover overlay with Arrow */}
            <div className="absolute inset-0 border-2 border-transparent group-hover:border-gray-500 transition-colors pointer-events-none z-20"></div>
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-10 bg-black/50 p-4 rounded-full backdrop-blur-sm">
               <ArrowRight size={32} className="text-white" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
