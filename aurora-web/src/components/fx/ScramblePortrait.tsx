import React, { useRef, useEffect, useState } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

interface ScramblePortraitProps {
  imageSrc?: string;
  gridDensity?: number;
  className?: string;
}

const CHARSET = " .:-=+*#%@∅◊§⌬≡∞∂αβγδεζθλμπσφψωΣΔΦΨΩ";

export const ScramblePortrait: React.FC<ScramblePortraitProps> = ({
  imageSrc = "https://images.unsplash.com/photo-1551288049-bbbda536339a?q=80&w=2070&auto=format&fit=crop",
  gridDensity = 200,
  className = ""
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [imageLoaded, setImageLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement | null>(null);

  useEffect(() => {
    const img = new Image();
    img.src = imageSrc;
    img.onload = () => {
      imgRef.current = img;
      setImageLoaded(true);
    };
  }, [imageSrc]);

  useGSAP(() => {
    if (!imageLoaded || !canvasRef.current || !imgRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    const img = imgRef.current;
    
    const buffer = document.createElement('canvas');
    const bCtx = buffer.getContext('2d', { willReadFrequently: true });
    if (!bCtx) return;

    const render = (revealProgress: number) => {
        const dpr = window.devicePixelRatio || 1;
        const w = containerRef.current?.offsetWidth || 500;
        const h = (w * img.height) / img.width;
        
        canvas.width = w * dpr;
        canvas.height = h * dpr;
        ctx.scale(dpr, dpr);
        
        canvas.style.width = `${w}px`;
        canvas.style.height = `${h}px`;

        buffer.width = gridDensity;
        buffer.height = Math.round(gridDensity * (img.height / img.width));

        bCtx.drawImage(img, 0, 0, buffer.width, buffer.height);
        const imgData = bCtx.getImageData(0, 0, buffer.width, buffer.height).data;

        ctx.clearRect(0, 0, w, h);
        
        const cellW = w / buffer.width;
        const cellH = h / buffer.height;

        ctx.font = `${cellW * 1.2}px 'DM Mono', monospace`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        for (let y = 0; y < buffer.height; y++) {
            for (let x = 0; x < buffer.width; x++) {
                const idx = (y * buffer.width + x) * 4;
                const r = imgData[idx];
                const g = imgData[idx + 1];
                const b = imgData[idx + 2];
                let lum = (r * 0.299 + g * 0.587 + b * 0.114) / 255;
                lum = Math.pow(lum, 1.4);

                const isRevealed = (x / buffer.width) + (Math.random() * 0.15) < revealProgress;
                
                if (lum < 0.08) continue; 

                let char = " ";
                if (isRevealed) {
                    const charIdx = Math.min(Math.floor(lum * CHARSET.length), CHARSET.length - 1);
                    char = CHARSET[charIdx];
                } else {
                    char = CHARSET[Math.floor(Math.random() * (CHARSET.length - 1))];
                }

                const isGold = (r > 160 && g > 130 && r > b * 1.5);
                
                ctx.fillStyle = isGold 
                    ? `rgba(197, 160, 89, ${isRevealed ? 1 : 0.4})` 
                    : `rgba(26, 26, 23, ${lum * (isRevealed ? 0.9 : 0.2)})`;

                ctx.fillText(char, x * cellW + cellW / 2, y * cellH + cellH / 2);
            }
        }
    };

    const state = { progress: 0 };

    gsap.to(state, {
        progress: 1.2,
        duration: 3,
        delay: 0.8,
        ease: "power2.inOut",
        onUpdate: () => render(state.progress)
    });

    render(0);

  }, [imageLoaded, gridDensity]);

  return (
    <div 
        ref={containerRef} 
        className={`relative w-full h-auto cursor-crosshair ${className}`}
    >
        <canvas 
            ref={canvasRef} 
            className="w-full h-full block mix-blend-multiply"
        />
        
        <div className="absolute -bottom-4 right-0 font-mono text-[8px] uppercase tracking-widest text-ink/40">
            ASCII_PORTRAIT_RECONSTRUCTION // LVL_09
        </div>
    </div>
  );
};
