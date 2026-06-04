"use client";

import React from 'react';
import { cn } from '@/lib/utils';
import { VariantProps, cva } from "class-variance-authority";

/**
 * ID: borders-neon-button-001
 * Name: Neon Button (Glimmer Edge)
 * Pattern: P022 (Gradient Border Glimmer / Edge Glow)
 */

const buttonVariants = cva(
    "relative group border text-foreground mx-auto text-center rounded-full transition-all duration-300",
    {
        variants: {
            variant: {
                default: "bg-blue-500/5 hover:bg-blue-500/10 border-blue-500/20 hover:border-blue-500/40",
                solid: "bg-blue-600 hover:bg-blue-500 text-white border-transparent hover:border-white/20",
                ghost: "border-transparent bg-transparent hover:border-zinc-700 hover:bg-white/5",
            },
            size: {
                default: "px-7 py-1.5 text-sm",
                sm: "px-4 py-1 text-xs",
                lg: "px-10 py-3 text-base font-medium",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    }
);

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> { 
    neon?: boolean;
    glowColor?: string; 
}

const NeonButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, neon = true, size, variant, children, glowColor = "blue", ...props }, ref) => {
        
        // Dynamic color mapping for Aurora consistency
        const colorClasses = glowColor === "blue" 
            ? "dark:via-blue-500 via-blue-600" 
            : "dark:via-zinc-400 via-zinc-500";

        return (
            <button
                className={cn(buttonVariants({ variant, size }), className)}
                ref={ref}
                {...props}
            >
                {/* Top Glimmer */}
                <span className={cn(
                    "absolute h-px opacity-0 group-hover:opacity-100 transition-all duration-500 ease-in-out inset-x-0 -top-px bg-gradient-to-r w-3/4 mx-auto from-transparent to-transparent hidden", 
                    colorClasses,
                    neon && "block"
                )} />
                
                {children}

                {/* Bottom Glimmer (Static Glow) */}
                <span className={cn(
                    "absolute group-hover:opacity-60 transition-all duration-500 ease-in-out inset-x-0 h-px -bottom-px bg-gradient-to-r w-3/4 mx-auto from-transparent to-transparent hidden opacity-30", 
                    colorClasses,
                    neon && "block"
                )} />
            </button>
        );
    }
)

NeonButton.displayName = 'NeonButton';

export { NeonButton as Button, buttonVariants };
