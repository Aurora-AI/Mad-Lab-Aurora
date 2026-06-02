import React, { useEffect, useRef, useState } from 'react';
import { motion, useInView } from 'framer-motion';

const Counter = ({ value, suffix = "" }: { value: number; suffix?: string }) => {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (isInView) {
      let start = 0;
      const end = value;
      const duration = 2;
      let startTime: number | null = null;

      const animate = (currentTime: number) => {
        if (!startTime) startTime = currentTime;
        const progress = Math.min((currentTime - startTime) / (duration * 1000), 1);
        setCount(Math.floor(progress * (end - start) + start));
        if (progress < 1) requestAnimationFrame(animate);
      };
      requestAnimationFrame(animate);
    }
  }, [isInView, value]);

  return <span ref={ref}>{count}{suffix}</span>;
};

export const ArchitecturalProtocol: React.FC = () => {
  const protocols = [
    { label: "Anthropic Claude 3.5", status: "Sovereign Override" },
    { label: "AWS Activate S-Tier", status: "Compute Isolated" },
    { label: "Google Startup Hub", status: "Trusted Partner" },
    { label: "Microsoft for Startups", status: "Enterprise Verified" }
  ];

  return (
    <section className="relative w-full py-32 bg-parchment border-t border-ink/5">
      <div className="container mx-auto px-8 md:px-20">
        <div className="flex flex-col md:flex-row gap-20">
            <div className="w-full md:w-1/3">
                <span className="font-mono text-[10px] text-aureate tracking-[0.4em] mb-6 block uppercase">
                    04 // ARCHITECTURAL PROTOCOL
                </span>
                <h2 className="font-display text-4xl md:text-5xl text-ink leading-tight mb-8">
                    Credenciamento <br /> Técnico de <br /> <span className="italic font-light">Alta Alavancagem</span>.
                </h2>
                <p className="font-editorial text-lg text-ink/70 leading-relaxed">
                    Nossa infraestrutura é construída sobre os maiores provedores de tecnologia do mundo, mas governada por protocolos de soberania local que garantem a custódia total do ativo.
                </p>
            </div>

            <div className="flex-1">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 mb-20">
                    <div className="p-8 border border-ink/5 bg-stone/30 relative overflow-hidden group">
                        <span className="font-mono text-[9px] text-ink/40 uppercase tracking-widest block mb-4">Precision Rate</span>
                        <div className="font-display text-6xl text-ink">
                            <Counter value={99} suffix="%" />
                        </div>
                        <div className="absolute top-0 right-0 w-16 h-16 bg-aureate/5 -translate-y-8 translate-x-8 rotate-45" />
                    </div>
                    <div className="p-8 border border-ink/5 bg-stone/30 relative overflow-hidden group">
                        <span className="font-mono text-[9px] text-ink/40 uppercase tracking-widest block mb-4">Latency Audit</span>
                        <div className="font-display text-6xl text-ink">
                            <Counter value={120} suffix="ms" />
                        </div>
                        <div className="absolute top-0 right-0 w-16 h-16 bg-aureate/5 -translate-y-8 translate-x-8 rotate-45" />
                    </div>
                </div>

                <div className="space-y-4">
                    <h4 className="font-mono text-[10px] text-ink/40 uppercase tracking-[0.3em] mb-6">Stack Certificada</h4>
                    {protocols.map((p, i) => (
                        <div key={i} className="flex justify-between items-center py-4 border-b border-ink/5 group cursor-default">
                            <span className="font-display text-xl text-ink group-hover:translate-x-2 transition-transform duration-500">{p.label}</span>
                            <span className="font-mono text-[9px] text-aureate uppercase tracking-tighter opacity-0 group-hover:opacity-100 transition-opacity duration-500">{p.status}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
      </div>
    </section>
  );
};

export default ArchitecturalProtocol;
