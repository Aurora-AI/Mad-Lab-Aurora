import React, { useState, useRef, useCallback, useEffect } from 'react';
import { cn } from "@/lib/utils";

/**
 * ImageComparison (Vanilla React Implementation)
 * This version uses pure state and event listeners instead of animation libraries.
 * Ported to Aurora Visual Assets Corpus.
 */
export const ImageComparison = ({ 
    beforeImage, 
    afterImage, 
    altBefore = 'Before', 
    altAfter = 'After',
    className
}: {
    beforeImage: string;
    afterImage: string;
    altBefore?: string;
    altAfter?: string;
    className?: string;
}) => {
    const [sliderPosition, setSliderPosition] = useState(50);
    const [isDragging, setIsDragging] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    const handleMove = useCallback((clientX: number) => {
        if (!isDragging || !containerRef.current) return;
        
        const rect = containerRef.current.getBoundingClientRect();
        let newPosition = ((clientX - rect.left) / rect.width) * 100;
        newPosition = Math.max(0, Math.min(100, newPosition));
        
        setSliderPosition(newPosition);
    }, [isDragging]);

    const handleMouseDown = () => setIsDragging(true);
    const handleMouseUp = useCallback(() => setIsDragging(false), []);
    const handleMouseMove = (e: React.MouseEvent) => handleMove(e.clientX);
    
    const handleTouchStart = () => setIsDragging(true);
    const handleTouchEnd = () => setIsDragging(false);
    const handleTouchMove = (e: React.TouchEvent) => handleMove(e.touches[0].clientX);

    useEffect(() => {
        window.addEventListener('mouseup', handleMouseUp);
        return () => {
            window.removeEventListener('mouseup', handleMouseUp);
        };
    }, [handleMouseUp]);

    return (
        <div 
            ref={containerRef}
            className={cn(
                "relative w-full select-none rounded-xl overflow-hidden shadow-2xl",
                className
            )}
            onMouseMove={handleMouseMove}
            onMouseLeave={handleMouseUp}
            onTouchMove={handleTouchMove}
            onTouchEnd={handleTouchEnd}
        >
            {/* After Image (Top Layer) */}
            <div
                className="absolute top-0 left-0 h-full w-full overflow-hidden z-10"
                style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
            >
                <img
                    src={afterImage}
                    alt={altAfter}
                    className="h-full w-full object-cover object-left"
                    draggable="false"
                />
            </div>

            {/* Before Image (Bottom Layer) */}
            <img
                src={beforeImage}
                alt={altBefore}
                className="block h-full w-full object-cover object-left"
                draggable="false"
            />

            {/* Slider Handle */}
            <div
                className="absolute top-0 bottom-0 w-1.5 bg-white/80 cursor-ew-resize flex items-center justify-center z-20"
                style={{ left: `calc(${sliderPosition}% - 0.375rem)` }}
                onMouseDown={handleMouseDown}
                onTouchStart={handleTouchStart}
            >
                <div className={cn(
                    "bg-white rounded-full h-10 w-10 flex items-center justify-center shadow-md transition-all duration-200 ease-in-out",
                    isDragging ? "scale-110 shadow-xl" : ""
                )}>
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-zinc-700">
                        <polyline points="15 18 9 12 15 6"></polyline>
                        <polyline points="9 18 3 12 9 6" className="opacity-0"></polyline>
                        {/* Custom arrows for clarity */}
                        <path d="m18 8 4 4-4 4" />
                        <path d="m6 8-4 4 4 4" />
                    </svg>
                </div>
            </div>
        </div>
    );
};
