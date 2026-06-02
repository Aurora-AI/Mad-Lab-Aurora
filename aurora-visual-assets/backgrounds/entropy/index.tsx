'use client';

import * as React from 'react';
import { useEffect, useRef } from 'react';

/**
 * ID: backgrounds-entropy-001
 * Name: Entropy (Order vs Chaos)
 * Pattern: P016 (Entropy Particle Physics) + P017 (Canvas Proximity Networking)
 */

interface EntropyProps {
  className?: string;
  width?: number;
  height?: number;
  chaosIntensity?: number; // 0 to 1
}

export function Entropy({ 
  className = "", 
  width = 400, 
  height = 600,
  chaosIntensity = 0.5
}: EntropyProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const intensityRef = useRef(chaosIntensity);

  useEffect(() => {
    intensityRef.current = chaosIntensity;
  }, [chaosIntensity]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // High DPI / DPR Setup
    const dpr = window.devicePixelRatio || 1;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.scale(dpr, dpr);

    const particleColor = '#ffffff';

    class Particle {
      x: number;
      y: number;
      size: number;
      order: boolean;
      velocity: { x: number; y: number };
      originalX: number;
      originalY: number;
      influence: number;
      neighbors: Particle[];

      constructor(x: number, y: number, order: boolean) {
        this.x = x;
        this.y = y;
        this.originalX = x;
        this.originalY = y;
        this.size = 1.5;
        this.order = order;
        this.velocity = {
          x: (Math.random() - 0.5) * 2,
          y: (Math.random() - 0.5) * 2
        };
        this.influence = 0;
        this.neighbors = [];
      }

      update(w: number, h: number) {
        const intensity = intensityRef.current;

        if (this.order) {
          // Ordered particles affected by chaos
          const dx = this.originalX - this.x;
          const dy = this.originalY - this.y;

          const chaosInfluence = { x: 0, y: 0 };
          this.neighbors.forEach(neighbor => {
            if (!neighbor.order) {
              const distance = Math.hypot(this.x - neighbor.x, this.y - neighbor.y);
              const strength = Math.max(0, 1 - distance / 100);
              chaosInfluence.x += (neighbor.velocity.x * strength * intensity);
              chaosInfluence.y += (neighbor.velocity.y * strength * intensity);
              this.influence = Math.max(this.influence, strength * intensity);
            }
          });

          // Mix ordered motion back to home vs chaos impact
          this.x += dx * 0.05 * (1 - this.influence) + chaosInfluence.x * this.influence;
          this.y += dy * 0.05 * (1 - this.influence) + chaosInfluence.y * this.influence;

          this.influence *= 0.99;
        } else {
          // Chaos particles motion
          this.velocity.x += (Math.random() - 0.5) * 0.5 * intensity;
          this.velocity.y += (Math.random() - 0.5) * 0.5 * intensity;
          this.velocity.x *= 0.95;
          this.velocity.y *= 0.95;
          this.x += this.velocity.x;
          this.y += this.velocity.y;

          // Wrap/Bounce within the chaos zone (right half)
          if (this.x < w / 2 || this.x > w) this.velocity.x *= -1;
          if (this.y < 0 || this.y > h) this.velocity.y *= -1;
          this.x = Math.max(w / 2, Math.min(w, this.x));
          this.y = Math.max(0, Math.min(h, this.y));
        }
      }

      draw(ctx: CanvasRenderingContext2D) {
        const alpha = this.order ?
          0.6 - this.influence * 0.4 :
          0.4;
        ctx.fillStyle = `${particleColor}${Math.round(alpha * 255).toString(16).padStart(2, '0')}`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    const particles: Particle[] = [];
    const gridSizeX = 20;
    const gridSizeY = 30;
    const spacingX = width / gridSizeX;
    const spacingY = height / gridSizeY;

    for (let i = 0; i < gridSizeX; i++) {
      for (let j = 0; j < gridSizeY; j++) {
        const x = spacingX * i + spacingX / 2;
        const y = spacingY * j + spacingY / 2;
        const order = x < width / 2;
        particles.push(new Particle(x, y, order));
      }
    }

    function updateNeighbors() {
      particles.forEach(particle => {
        particle.neighbors = particles.filter(other => {
          if (other === particle) return false;
          const distance = Math.hypot(particle.x - other.x, particle.y - other.y);
          return distance < 80;
        });
      });
    }

    let time = 0;
    let animationId: number;
    
    function animate() {
      if (!ctx) return;
      ctx.clearRect(0, 0, width, height);

      if (time % 40 === 0) {
        updateNeighbors();
      }

      particles.forEach(particle => {
        particle.update(width, height);
        particle.draw(ctx);

        particle.neighbors.forEach(neighbor => {
          const distance = Math.hypot(particle.x - neighbor.x, particle.y - neighbor.y);
          if (distance < 40) {
            const alpha = 0.1 * (1 - distance / 40);
            ctx.strokeStyle = `${particleColor}${Math.round(alpha * 255).toString(16).padStart(2, '0')}`;
            ctx.beginPath();
            ctx.moveTo(particle.x, particle.y);
            ctx.lineTo(neighbor.x, neighbor.y);
            ctx.stroke();
          }
        });
      });

      // Axis Line (The Divide)
      ctx.strokeStyle = `${particleColor}22`;
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      ctx.moveTo(width / 2, 0);
      ctx.lineTo(width / 2, height);
      ctx.stroke();

      time++;
      animationId = requestAnimationFrame(animate);
    }

    animate();

    return () => {
      cancelAnimationFrame(animationId);
    };
  }, [width, height]);

  return (
    <div className={`relative bg-transparent flex items-center justify-center overflow-hidden ${className}`} style={{ width, height }}>
      <canvas
        ref={canvasRef}
        className="block"
      />
    </div>
  );
}

