"use client";

import * as React from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";

// -------------------------------------------------------------------------
// 1. MARQUEE PRIMITIVE (Bundled for Portability)
// -------------------------------------------------------------------------
interface MarqueeProps {
  className?: string;
  reverse?: boolean;
  pauseOnHover?: boolean;
  children?: React.ReactNode;
  vertical?: boolean;
  repeat?: number;
  [key: string]: any;
}

function Marquee({
  className,
  reverse,
  pauseOnHover = false,
  children,
  vertical = false,
  repeat = 4,
  ...props
}: MarqueeProps) {
  return (
    <div
      {...props}
      className={cn(
        "group flex overflow-hidden p-2 [--duration:40s] [--gap:1rem] [flex-direction:row]",
        {
          "[flex-direction:column]": vertical,
        },
        className,
      )}
    >
      {Array(repeat)
        .fill(0)
        .map((_, i) => (
          <div
            key={i}
            className={cn("flex shrink-0 justify-around [gap:var(--gap)]", {
              "animate-marquee flex-row": !vertical,
              "animate-marquee-vertical flex-col": vertical,
              "[animation-direction:reverse]": reverse,
              "group-hover:[animation-play-state:paused]": pauseOnHover,
            })}
          >
            {children}
          </div>
        ))}
    </div>
  );
}

// -------------------------------------------------------------------------
// 2. MAIN COMPONENT
// -------------------------------------------------------------------------
const teamMembers = [
  {
    image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=800&auto=format&fit=crop",
    name: "Patrick Stewart",
    role: "CEO - Founder",
  },
  {
    image: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=800&auto=format&fit=crop",
    name: "Alena Rosser",
    role: "Director of Content",
  },
  {
    image: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=800&auto=format&fit=crop",
    name: "Fletch Skinner",
    role: "Tech Manager",
  },
  {
    image: "https://images.unsplash.com/photo-1560250097-0b93528c311a?q=80&w=800&auto=format&fit=crop",
    name: "Marc Spector",
    role: "Director of Content",
  },
  {
    image: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=800&auto=format&fit=crop",
    name: "Natalia Skinner",
    role: "Cnippet Researcher",
  },
  {
    image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=800&auto=format&fit=crop",
    name: "David Kim",
    role: "Engineering Lead",
  },
];

export function TeamSection() {
  return (
    <section className="relative w-full overflow-hidden bg-white py-12 md:py-24 dark:bg-background">
      {/* Background Decorator */}
      <div>
        <svg
          className="absolute right-0 bottom-0 text-neutral-200 dark:text-neutral-800 pointer-events-none"
          fill="none"
          height="154"
          viewBox="0 0 460 154"
          width="460"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g clipPath="url(#clip0_494_1104)">
            <path
              d="M-87.463 458.432C-102.118 348.092 -77.3418 238.841 -15.0744 188.274C57.4129 129.408 180.708 150.071 351.748 341.128C278.246 -374.233 633.954 380.602 548.123 42.7707"
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="40"
            />
          </g>
          <defs>
            <clipPath id="clip0_494_1104">
              <rect fill="white" height="154" width="460" />
            </clipPath>
          </defs>
        </svg>
      </div>

      <div className="relative z-10 mx-auto max-w-7xl">
        <div className="mx-auto mb-16 flex max-w-5xl flex-col items-center px-6 text-center lg:px-0">
          <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-600 text-white shadow-xl shadow-blue-500/20">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16.051 12.616a1 1 0 0 1 1.909.024l.737 1.452a1 1 0 0 0 .737.535l1.634.256a1 1 0 0 1 .588 1.806l-1.172 1.168a1 1 0 0 0-.282.866l.259 1.613a1 1 0 0 1-1.541 1.134l-1.465-.75a1 1 0 0 0-.912 0l-1.465.75a1 1 0 0 1-1.539-1.133l.258-1.613a1 1 0 0 0-.282-.866l-1.156-1.153a1 1 0 0 1 .572-1.822l1.633-.256a1 1 0 0 0 .737-.535z"/><path d="M8 15H7a4 4 0 0 0-4 4v2"/><circle cx="10" cy="7" r="4"/></svg>
          </div>

          <h2 className="relative mb-4 font-medium text-4xl text-neutral-900 tracking-tight sm:text-5xl dark:text-neutral-100">
            Creative Team Members
            <svg
              className="absolute -top-2 -right-8 -z-10 w-24 text-neutral-200 dark:text-neutral-700 opacity-50"
              fill="currentColor"
              height="86"
              viewBox="0 0 108 86"
              width="108"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M38.8484 16.236L15 43.5793L78.2688 15L18.1218 71L93 34.1172L70.2047 65.2739"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="28"
              />
            </svg>
          </h2>
          <p className="max-w-2xl text-neutral-600 dark:text-neutral-400">
            Connecting you with the most advanced tech solutions,
            empowering seamless communication through design.
          </p>
        </div>

        {/* The Marquee Team Grid */}
        <div className="relative w-full overflow-hidden">
          <div className="pointer-events-none absolute top-0 left-0 z-10 h-full w-32 bg-gradient-to-r from-white to-transparent dark:from-background" />
          <div className="pointer-events-none absolute top-0 right-0 z-10 h-full w-32 bg-gradient-to-l from-white to-transparent dark:from-background" />

          <Marquee className="[--gap:1.5rem]" pauseOnHover>
            {teamMembers.map((member) => (
              <div
                className="group flex w-64 shrink-0 flex-col"
                key={member.name}
              >
                <div className="relative h-92 w-full overflow-hidden rounded-3xl bg-neutral-100 dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700/50">
                  <Image
                    alt={member.name}
                    className="h-full w-full object-cover grayscale transition-all duration-500 group-hover:grayscale-0 group-hover:scale-105"
                    fill
                    src={member.image}
                  />
                  <div className="absolute bottom-4 left-4 right-4 rounded-2xl bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md p-4 border border-white/20 dark:border-neutral-800/50 transition-transform duration-500 group-hover:-translate-y-2">
                    <h3 className="font-bold text-neutral-900 dark:text-neutral-100 italic">
                      {member.name}
                    </h3>
                    <p className="text-neutral-500 text-xs dark:text-neutral-400 uppercase tracking-widest font-semibold">
                      {member.role}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </Marquee>
        </div>

        {/* Testimonial Section */}
        <div className="mx-auto mt-20 max-w-3xl px-6 text-center lg:px-0">
          <p className="mb-8 font-medium text-lg text-neutral-900 leading-relaxed md:text-xl dark:text-neutral-100">
            "The exceptional support from the team truly impressed us. We
            suggested a visual improvement, and their team implemented it with
            remarkable speed!"
          </p>
          <div className="flex flex-col items-center gap-3">
            <div className="relative h-14 w-14 overflow-hidden rounded-full border-2 border-primary/20 p-0.5">
              <Image
                alt="Natalia Kara"
                className="h-full w-full object-cover rounded-full"
                fill
                src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=800&auto=format&fit=crop"
              />
            </div>
            <div className="text-center">
              <p className="font-semibold text-neutral-900 dark:text-neutral-100">
                Natalia Kara
              </p>
              <p className="text-neutral-500 text-sm dark:text-neutral-400">
                CTO · Future Collection
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
