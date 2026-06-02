import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { LucideIcon, Box, Type, Layers, Activity, Sparkles, Layout, ChevronRight, Binary } from 'lucide-react';
import manifest from '@aurora-visual/manifest.json';

// Mapping categories to icons
const CategoryIcons: Record<string, LucideIcon> = {
  typography: Type,
  backgrounds: Layers,
  interactions: Activity,
  heroes: Sparkles,
  scenes: Box,
  sections: Layout,
  borders: Binary,
  navigation: ChevronRight
};

export default function ArsenalPage() {
  const [filter, setFilter] = useState<string | null>(null);

  const assets = manifest.assets;
  const categories = Object.keys(manifest.categories);

  const filteredAssets = filter 
    ? assets.filter(a => a.category === filter)
    : assets;

  return (
    <div className="min-h-screen pt-32 pb-24 px-[6vw] bg-[var(--page-bg)] text-[var(--page-text)]">
      {/* Header Section */}
      <div className="max-w-4xl mb-16">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <span className="font-mono text-[0.6rem] tracking-[0.4em] uppercase opacity-40 mb-4 block">
            [ Aurora Arsenal // v{manifest.version} ]
          </span>
          <h1 className="font-display italic text-6xl md:text-8xl leading-[0.9] tracking-tighter mb-8">
            Expansão do<br />Corpus Visual.
          </h1>
          <p className="font-body text-lg opacity-60 max-w-xl leading-relaxed">
            {manifest.description} Atualmente com {manifest.corpus_assets} ativos canônicos orquestrados para alta performance e impacto editorial.
          </p>
        </motion.div>
      </div>

      {/* Filter Bar */}
      <div className="flex flex-wrap gap-3 mb-12 border-b border-white/5 pb-8">
        <button 
          onClick={() => setFilter(null)}
          className={`px-6 py-2 rounded-full text-xs font-mono uppercase tracking-widest transition-all ${!filter ? 'bg-white text-black' : 'border border-white/10 hover:border-white/30'}`}
        >
          All Assets
        </button>
        {categories.map(cat => {
          const Icon = CategoryIcons[cat] || Box;
          return (
            <button 
              key={cat}
              onClick={() => setFilter(cat)}
              className={`flex items-center gap-2 px-6 py-2 rounded-full text-xs font-mono uppercase tracking-widest transition-all ${filter === cat ? 'bg-white text-black' : 'border border-white/10 hover:border-white/30'}`}
            >
              <Icon size={14} />
              {cat}
            </button>
          );
        })}
      </div>

      {/* Assets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <AnimatePresence mode="popLayout">
          {filteredAssets.map((asset, idx) => {
            const Icon = CategoryIcons[asset.category] || Box;
            return (
              <motion.div
                key={asset.id}
                layout
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.4, delay: idx * 0.05 }}
                className="group relative bg-[#0a0a0a] border border-white/5 rounded-2xl overflow-hidden hover:border-white/20 transition-colors"
              >
                {/* Visual Placeholder / Icon */}
                <div className="aspect-[16/10] bg-[#050505] flex items-center justify-center relative overflow-hidden">
                   <Icon size={48} className="opacity-10 group-hover:opacity-30 group-hover:scale-110 transition-all duration-700" />
                   
                   {/* Abstract background particles/lines simulation */}
                   <div className="absolute inset-0 opacity-20 pointer-events-none">
                      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-white/5 to-transparent" />
                   </div>
                   
                   <div className="absolute bottom-4 left-4 flex gap-1">
                      {asset.techniques?.slice(0, 3).map((t: string) => (
                        <span key={t} className="text-[10px] font-mono tracking-tighter px-2 py-0.5 rounded-sm bg-white/5 border border-white/10 uppercase">
                          {t}
                        </span>
                      ))}
                   </div>
                </div>

                {/* Content */}
                <div className="p-6">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-display text-xl tracking-tight">{asset.name}</h3>
                    <Icon size={16} className="opacity-30" />
                  </div>
                  <p className="text-xs font-mono opacity-40 uppercase tracking-widest mb-4">
                    {asset.id}
                  </p>
                  
                  <div className="flex items-center justify-between pt-4 border-t border-white/5 group-hover:border-white/10 transition-colors">
                    <span className="text-[10px] font-mono opacity-30 uppercase">
                      Origin: {asset.origin}
                    </span>
                    <button className="flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider group-hover:text-white text-white/50 transition-colors">
                      Explore Anatomy <ChevronRight size={12} />
                    </button>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>

      {/* Empty State */}
      {filteredAssets.length === 0 && (
        <div className="py-24 text-center opacity-40 font-mono text-sm uppercase tracking-[0.2em]">
          Nenhum ativo encontrado nesta categoria.
        </div>
      )}
    </div>
  );
}
