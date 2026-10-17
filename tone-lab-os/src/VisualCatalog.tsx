import { SlidersHorizontal, ArrowRight } from "lucide-react";

export function VisualCatalog() {
  const assets = [
    { name: "Origin 50C", category: "British", priority: "P1", status: "Owned" },
    { name: "Studio JTM", category: "Vintage", priority: "P3", status: "Planned" },
    { name: "Ampero II", category: "Modeler", priority: "P1", status: "Owned" }
  ];

  return (
    <div className="min-h-screen bg-ethereal text-charcoal p-12">
      <header className="mb-12 max-w-7xl mx-auto flex justify-between items-end border-b border-gray-300 pb-8">
        <div>
          <h1 className="text-5xl font-bold uppercase tracking-tight text-black mb-2">Equipment</h1>
          <p className="text-gray-500 text-sm font-mono uppercase tracking-widest">Visual Asset Catalog</p>
        </div>
        <div className="flex gap-4">
          <button className="flex items-center gap-2 text-xs uppercase font-bold tracking-widest border border-gray-300 bg-white/50 px-6 py-3 hover:bg-black hover:text-white transition-colors">
            <SlidersHorizontal size={14} /> Filters
          </button>
        </div>
      </header>

      <div className="max-w-7xl mx-auto grid grid-cols-3 gap-8">
        {assets.map((item, i) => (
          <div key={i} className="bg-white/60 backdrop-blur-2xl border border-white rounded-[24px] overflow-hidden flex flex-col relative h-[500px] shadow-[0_8px_32px_rgba(0,0,0,0.04)] group cursor-pointer">
            
            {/* Editorial Header */}
            <div className="px-8 pt-8 pb-4 flex justify-between items-start">
              <div>
                <h3 className="text-2xl font-bold uppercase tracking-tight text-black">{item.name}</h3>
                <span className="text-[10px] font-mono text-gray-500 uppercase tracking-widest block mt-1">{item.category}</span>
              </div>
              <span className="text-[10px] font-mono bg-black text-white px-2 py-1 uppercase">{item.status}</span>
            </div>

            {/* Strategic Dark Point (The Image Area) */}
            <div className="flex-1 mx-8 mb-8 bg-[#111] rounded-[16px] flex items-center justify-center relative overflow-hidden group-hover:shadow-2xl transition-all duration-500">
              <div className="w-32 h-32 border border-gray-800 flex items-center justify-center text-gray-700 rotate-45 group-hover:rotate-0 transition-all duration-500">
                 [ FOTO ]
              </div>
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex items-end p-6">
                 <div className="w-full flex justify-between items-center">
                   <span className="text-xs uppercase font-mono text-white">Priority {item.priority}</span>
                   <ArrowRight size={20} className="text-white" />
                 </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
