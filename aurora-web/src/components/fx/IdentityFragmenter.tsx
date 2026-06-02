import React, { useRef, useMemo } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

interface IdentityFragmenterProps {
  imageSrc?: string;
  slicesCount?: number;
  className?: string;
}

/**
 * IdentityFragmenter v2: Forensic Edition
 * Uses fixed diagonal slopes and staggered horizontal offsets for an editorial look.
 */
export const IdentityFragmenter: React.FC<IdentityFragmenterProps> = ({
  imageSrc = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop",
  slicesCount = 45,
  className = ""
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  const slices = useMemo(() => {
    const s = [];
    let currentTop = -20;
    const slopeOffset = 15;
    const totalWidth = 140;

    for (let i = 0; i < slicesCount; i++) {
        const width = Math.random() * (totalWidth / (slicesCount / 1.5)) + 1;
        const gap = Math.random() > 0.8 ? 0.5 : 0;
        
        const topStart = currentTop + gap;
        const topEnd = topStart + width;
        const bottomStart = topStart - slopeOffset;
        const bottomEnd = topEnd - slopeOffset;

        s.push({
            id: i,
            path: `polygon(${topStart}% 0%, ${topEnd}% 0%, ${bottomEnd}% 100%, ${bottomStart}% 100%)`,
            offsetX: (i % 2 === 0 ? 1 : -1) * (i % 3 === 0 ? 15 : 5),
            label: Math.random() > 0.85 ? `SEC_${(i * 7).toString(16).toUpperCase()}` : null
        });

        currentTop = topEnd;
        if (currentTop > 120) break;
    }
    return s;
  }, [slicesCount]);

  useGSAP(() => {
    if (!containerRef.current) return;

    const fragments = containerRef.current.querySelectorAll('.fragment-v2');
    const labels = containerRef.current.querySelectorAll('.fragment-label');

    const tl = gsap.timeline({ delay: 0.8 });

    tl.from(fragments, {
        opacity: 0,
        x: (i: number) => (i % 2 === 0 ? -120 : 120),
        duration: 2,
        stagger: {
            amount: 1.2,
            from: "center"
        },
        ease: "expo.out"
    });

    tl.from(labels, {
        opacity: 0,
        duration: 0.5,
        stagger: 0.1,
        ease: "steps(4)"
    }, "-=1");

    const onMouseMove = (e: MouseEvent) => {
        const { clientX, clientY } = e;
        const xPercent = (clientX / window.innerWidth - 0.5);
        const yPercent = (clientY / window.innerHeight - 0.5);

        gsap.to(fragments, {
            x: (i: number) => (i % 2 === 0 ? 1 : -1) * xPercent * 60 * (1 + i * 0.02),
            y: yPercent * 30,
            duration: 1.5,
            ease: "power2.out",
            overwrite: "auto"
        });
    };

    window.addEventListener('mousemove', onMouseMove);
    return () => window.removeEventListener('mousemove', onMouseMove);

  }, { scope: containerRef });

  return (
    <div 
        ref={containerRef} 
        className={`relative w-full h-full max-w-2xl mx-auto ${className}`}
        style={{ aspectRatio: "4/5", perspective: "1000px" }}
    >
        <div className="absolute inset-0 w-full h-full grayscale contrast-[1.2] brightness-[1.1]">
            {slices.map((slice) => (
                <div
                    key={slice.id}
                    className="fragment-v2 absolute inset-0 w-full h-full will-change-transform"
                    style={{
                        clipPath: slice.path,
                        zIndex: 10 + slice.id,
                        transform: `translateX(${slice.offsetX}px)`
                    }}
                >
                    <img 
                        src={imageSrc} 
                        alt=""
                        className="w-full h-full object-cover scale-105"
                    />
                    
                    {slice.label && (
                        <div className="fragment-label absolute top-1/4 left-1/2 -translate-x-1/2 font-mono text-[8px] text-aureate uppercase tracking-tighter mix-blend-difference pointer-events-none opacity-80">
                            {slice.label}
                        </div>
                    )}
                </div>
            ))}
        </div>

        <div className="absolute -inset-4 border border-ink/5 pointer-events-none" />
        <div className="absolute -top-6 -right-6 font-mono text-[9px] text-ink/40 uppercase">
            Sovereign_Identity_Scan // 0xAF04
        </div>
        
        <div className="absolute inset-0 pointer-events-none mix-blend-soft-light opacity-20 bg-[url('https://www.transparenttextures.com/patterns/pinstriped-dark.png')]" />
    </div>
  );
};
