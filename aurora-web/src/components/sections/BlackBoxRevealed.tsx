import React from 'react';
import { ScramblePortrait } from '../fx/ScramblePortrait';

export const BlackBoxRevealed: React.FC = () => {
  const cards = [
    {
      title: "Kernel Ozzmosis",
      desc: "Orquestração soberana de agentes sem dependência de provedores de nuvem.",
      id: "OZ_01",
      img: "https://images.unsplash.com/photo-1639322537228-f710d846310a?q=80&w=2032&auto=format&fit=crop"
    },
    {
      title: "Trustware Gates",
      desc: "Validação determinística de cada saída via Pydantic e schemas de integridade.",
      id: "TW_04",
      img: "https://images.unsplash.com/photo-1558494949-ef010cbdcc51?q=80&w=2070&auto=format&fit=crop"
    }
  ];

  return (
    <section className="relative w-full py-32 bg-stone border-t border-ink/5">
      <div className="container mx-auto px-8 md:px-20">
        <div className="flex flex-col md:flex-row justify-between items-end mb-20 gap-8">
            <div className="max-w-2xl">
                <span className="font-mono text-[10px] text-aureate tracking-[0.4em] mb-6 block uppercase">
                    03 // THE BLACK BOX REVEALED
                </span>
                <h2 className="font-display text-5xl md:text-6xl text-ink leading-tight">
                    O Fim da Caixa Preta. <br />
                    <span className="italic font-light text-aureate">Arquitetura Soberana</span>.
                </h2>
            </div>
            <p className="font-mono text-[11px] text-ink/40 max-w-[280px] uppercase tracking-wider text-right hidden md:block">
                Desvendando o motor de orquestração que torna o alucinação impossível.
            </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-ink/10 border border-ink/10">
            {cards.map((card, i) => (
                <div key={i} className="bg-parchment p-12 md:p-16 group hover:bg-parchment/80 transition-colors duration-700 overflow-hidden">
                    <div className="flex justify-between items-start mb-12">
                        <h3 className="font-display text-3xl text-ink">{card.title}</h3>
                        <span className="font-mono text-[10px] text-aureate border border-aureate/30 px-2 py-1">{card.id}</span>
                    </div>
                    <p className="font-editorial text-lg text-ink/70 leading-relaxed max-w-sm mb-16">
                        {card.desc}
                    </p>
                    
                    {/* Visual: Scramble Effect */}
                    <div className="w-full aspect-video grayscale opacity-80 group-hover:opacity-100 transition-opacity duration-1000">
                        <ScramblePortrait imageSrc={card.img} />
                    </div>
                </div>
            ))}
        </div>
      </div>
    </section>
  );
};

export default BlackBoxRevealed;
