"use client";

import * as React from "react";
import { useRef } from "react";
import Image from "next/image";
import { motion, useScroll, useTransform } from "framer-motion";
import { cn } from "./lib/utils";

/**
 * ID: heroes-davincho-001
 * Name: Davincho Parallax Hero
 * Pattern: P010 (Scroll-Driven Transform Parallax) + P011 (Typography Mix-Blend Difference)
 */

export function DavinchoHero() {
  const container = useRef<HTMLDivElement>(null);
  
  const { scrollYProgress } = useScroll({
    offset: ["start end", "end start"],
    target: container,
  });

  // Parallax subtle movement for the background image
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "20%"]);
  
  return (
    <div className="mx-2 mt-4 mb-32 overflow-hidden rounded-[2.5rem] bg-white dark:bg-neutral-950">
      <div
        className="relative flex h-[85vh] items-center justify-center overflow-hidden"
        ref={container}
        style={{ clipPath: "polygon(0% 0, 100% 0%, 100% 100%, 0 100%)" }}
      >
        {/* Editorial Text Layer */}
        <div className="relative z-10 flex h-full w-full flex-col justify-between p-8 md:p-20 text-white mix-blend-difference">
          <p className="w-full md:w-[50vw] self-end text-right text-lg md:text-[2vw] uppercase tracking-tighter font-light leading-tight">
            Beauty and quality need the right time to be conceived and realised
            even in a world that is in too much of a hurry.
          </p>
          
          <div className="flex flex-col">
            <h1 className="text-[12vw] md:text-[10vw] font-black uppercase tracking-tighter leading-[0.8] mb-4">
              AESTHETICS<br/>
              OF SILENCE
            </h1>
            <p className="text-sm md:text-base uppercase tracking-[0.3em] font-semibold opacity-80">
              Scroll to explore the parallax depth
            </p>
          </div>
        </div>

        {/* Parallax Image Background Layer */}
        <div className="absolute top-[-20vh] left-0 h-[130vh] w-full">
          <motion.div className="relative h-full w-full" style={{ y }}>
            <Image
              alt="Background Cinematic Editorial"
              className="grayscale brightness-[0.7] contrast-[1.1]"
              fill
              priority
              src="https://images.unsplash.com/photo-1492619375914-88005aa9e8fb?q=80&w=2000&auto=format&fit=crop"
              style={{ objectFit: "cover" }}
            />
          </motion.div>
        </div>
      </div>
    </div>
  );
}
