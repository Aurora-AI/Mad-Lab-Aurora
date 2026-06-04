'use client';

import { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';

/**
 * ID: backgrounds-spiral-001
 * Name: Spiral Animation (Kinetic Wormhole)
 * Pattern: P018 (3D-to-2D Perspective Projection) + P019 (GSAP-Driven Canvas State)
 */

class Vector2D {
  constructor(public x: number, public y: number) {}
}

class Vector3D {
  constructor(public x: number, public y: number, public z: number) {}
}

class AnimationController {
  private timeline: gsap.core.Timeline;
  private time = 0;
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private size: number;
  private stars: Star[] = [];
  
  private readonly changeEventTime = 0.32;
  private readonly cameraZ = -400;
  private readonly cameraTravelDistance = 3400;
  private readonly startDotYOffset = 28;
  private readonly viewZoom = 100;
  private readonly numberOfStars = 5000;
  private readonly trailLength = 80;
  
  constructor(canvas: HTMLCanvasElement, ctx: CanvasRenderingContext2D, size: number) {
    this.canvas = canvas;
    this.ctx = ctx;
    this.size = size;
    this.timeline = gsap.timeline({ repeat: -1 });
    
    this.createStars();
    this.setupTimeline();
  }
  
  private createStars() {
    for (let i = 0; i < this.numberOfStars; i++) {
      this.stars.push(new Star(this.cameraZ, this.cameraTravelDistance));
    }
  }
  
  private setupTimeline() {
    this.timeline.to(this, {
      time: 1,
      duration: 15,
      repeat: -1,
      ease: "none",
      onUpdate: () => this.render()
    });
  }
  
  public ease(p: number, g: number): number {
    if (p < 0.5) return 0.5 * Math.pow(2 * p, g);
    else return 1 - 0.5 * Math.pow(2 * (1 - p), g);
  }
  
  public easeOutElastic(x: number): number {
    const c4 = (2 * Math.PI) / 4.5;
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    return Math.pow(2, -8 * x) * Math.sin((x * 8 - 0.75) * c4) + 1;
  }
  
  public map(value: number, s1: number, st1: number, s2: number, st2: number): number {
    return s2 + (st2 - s2) * ((value - s1) / (st1 - s1));
  }
  
  public constrain(v: number, min: number, max: number): number {
    return Math.min(Math.max(v, min), max);
  }
  
  public lerp(s: number, e: number, t: number): number {
    return s * (1 - t) + e * t;
  }
  
  public spiralPath(p: number): Vector2D {
    p = this.constrain(1.2 * p, 0, 1);
    p = this.ease(p, 1.8);
    const turns = 6;
    const theta = 2 * Math.PI * turns * Math.sqrt(p);
    const r = 170 * Math.sqrt(p);
    return new Vector2D(r * Math.cos(theta), r * Math.sin(theta) + this.startDotYOffset);
  }
  
  public rotate(v1: Vector2D, v2: Vector2D, p: number, orient: boolean): Vector2D {
    const mid = new Vector2D((v1.x + v2.x) / 2, (v1.y + v2.y) / 2);
    const dx = v1.x - mid.x;
    const dy = v1.y - mid.y;
    const angle = Math.atan2(dy, dx);
    const o = orient ? -1 : 1;
    const r = Math.sqrt(dx * dx + dy * dy);
    const bounce = Math.sin(p * Math.PI) * 0.05 * (1 - p);
    return new Vector2D(
      mid.x + r * (1 + bounce) * Math.cos(angle + o * Math.PI * this.easeOutElastic(p)),
      mid.y + r * (1 + bounce) * Math.sin(angle + o * Math.PI * this.easeOutElastic(p))
    );
  }
  
  public showProjectedDot(position: Vector3D, sizeFactor: number) {
    const t2 = this.constrain(this.map(this.time, this.changeEventTime, 1, 0, 1), 0, 1);
    const zPos = this.cameraZ + this.ease(Math.pow(t2, 1.2), 1.8) * this.cameraTravelDistance;
    
    if (position.z > zPos) {
      const depth = position.z - zPos;
      const x = this.viewZoom * position.x / depth;
      const y = this.viewZoom * position.y / depth;
      const sw = 400 * sizeFactor / depth;
      
      this.ctx.lineWidth = sw;
      this.ctx.beginPath();
      this.ctx.arc(x, y, 0.5, 0, Math.PI * 2);
      this.ctx.fill();
    }
  }
  
  public render() {
    this.ctx.fillStyle = 'black';
    this.ctx.fillRect(0, 0, this.size, this.size);
    
    this.ctx.save();
    this.ctx.translate(this.size / 2, this.size / 2);
    
    const t1 = this.constrain(this.map(this.time, 0, this.changeEventTime + 0.25, 0, 1), 0, 1);
    const t2 = this.constrain(this.map(this.time, this.changeEventTime, 1, 0, 1), 0, 1);
    
    this.ctx.rotate(-Math.PI * this.ease(t2, 2.7));
    this.drawTrail(t1);
    
    this.ctx.fillStyle = 'white';
    for (const star of this.stars) {
      star.render(t1, this);
    }
    
    this.ctx.restore();
  }
  
  private drawTrail(t1: number) {
    for (let i = 0; i < this.trailLength; i++) {
      const f = this.map(i, 0, this.trailLength, 1.1, 0.1);
      const sw = (1.3 * (1 - t1) + 3.0 * Math.sin(Math.PI * t1)) * f;
      this.ctx.fillStyle = 'white';
      const pathTime = t1 - 0.00015 * i;
      const pos = this.spiralPath(pathTime);
      const rotated = this.rotate(pos, new Vector2D(pos.x + 5, pos.y + 5), Math.sin(this.time * Math.PI * 2) * 0.5 + 0.5, i % 2 === 0);
      this.ctx.beginPath();
      this.ctx.arc(rotated.x, rotated.y, sw / 2, 0, Math.PI * 2);
      this.ctx.fill();
    }
  }
  
  public destroy() {
    this.timeline.kill();
  }
}

class Star {
  private dx: number;
  private dy: number;
  private spiralLocation: number;
  private strokeWeightFactor: number;
  private z: number;
  private angle: number;
  private distance: number;
  private rotationDirection: number;
  private expansionRate: number;
  private finalScale: number;
  
  constructor(cameraZ: number, cameraTravelDistance: number) {
    this.angle = Math.random() * Math.PI * 2;
    this.distance = 30 * Math.random() + 15;
    this.rotationDirection = Math.random() > 0.5 ? 1 : -1;
    this.expansionRate = 1.2 + Math.random() * 0.8;
    this.finalScale = 0.7 + Math.random() * 0.6;
    this.dx = this.distance * Math.cos(this.angle);
    this.dy = this.distance * Math.sin(this.angle);
    this.spiralLocation = (1 - Math.pow(1 - Math.random(), 3.0)) / 1.3;
    this.z = (0.5 * cameraZ) + Math.random() * (cameraTravelDistance + cameraZ - 0.5 * cameraZ);
    this.z = this.z * 0.7 + (cameraTravelDistance / 2) * 0.3 * this.spiralLocation;
    this.strokeWeightFactor = Math.pow(Math.random(), 2.0);
  }
  
  render(p: number, controller: AnimationController) {
    const spiralPos = controller.spiralPath(this.spiralLocation);
    const q = p - this.spiralLocation;
    if (q > 0) {
      const progress = controller.constrain(4 * q, 0, 1);
      let easing = progress < 0.3 ? controller.lerp(progress, Math.pow(progress, 2), progress / 0.3) :
                   progress < 0.7 ? controller.lerp(Math.pow(progress, 2), controller.easeOutElastic(progress), (progress - 0.3) / 0.4) :
                   controller.easeOutElastic(progress);
      
      let screenX, screenY;
      if (progress < 0.3) {
        screenX = controller.lerp(spiralPos.x, spiralPos.x + this.dx * 0.3, easing / 0.3);
        screenY = controller.lerp(spiralPos.y, spiralPos.y + this.dy * 0.3, easing / 0.3);
      } else if (progress < 0.7) {
        const midT = (progress - 0.3) / 0.4;
        const curve = Math.sin(midT * Math.PI) * this.rotationDirection * 1.5;
        const bx = spiralPos.x + this.dx * 0.3;
        const by = spiralPos.y + this.dy * 0.3;
        const tx = spiralPos.x + this.dx * 0.7;
        const ty = spiralPos.y + this.dy * 0.7;
        screenX = controller.lerp(bx, tx, midT) + (-this.dy * 0.4 * curve) * midT;
        screenY = controller.lerp(by, ty, midT) + (this.dx * 0.4 * curve) * midT;
      } else {
        const finT = (progress - 0.7) / 0.3;
        const bx = spiralPos.x + this.dx * 0.7;
        const by = spiralPos.y + this.dy * 0.7;
        const tDist = this.distance * this.expansionRate * 1.5;
        const sAngle = this.angle + (1.2 * this.rotationDirection) * finT * Math.PI;
        screenX = controller.lerp(bx, spiralPos.x + tDist * Math.cos(sAngle), finT);
        screenY = controller.lerp(by, spiralPos.y + tDist * Math.sin(sAngle), finT);
      }
      
      const v3d = new Vector3D((this.z - controller['cameraZ']) * screenX / controller['viewZoom'], (this.z - controller['cameraZ']) * screenY / controller['viewZoom'], this.z);
      const sizeMult = progress < 0.6 ? 1.0 + progress * 0.2 : 1.2 * (1.0 - (progress - 0.6) / 0.4) + this.finalScale * ((progress - 0.6) / 0.4);
      controller.showProjectedDot(v3d, 8.5 * this.strokeWeightFactor * sizeMult);
    }
  }
}

export function SpiralAnimation() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationRef = useRef<AnimationController | null>(null);
  const [dims, setDims] = useState({ w: 0, h: 0 });

  useEffect(() => {
    const resize = () => setDims({ w: window.innerWidth, h: window.innerHeight });
    resize();
    window.addEventListener('resize', resize);
    return () => window.removeEventListener('resize', resize);
  }, []);

  useEffect(() => {
    if (!canvasRef.current || dims.w === 0) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const size = Math.max(dims.w, dims.h);
    canvas.width = size * dpr;
    canvas.height = size * dpr;
    canvas.style.width = `${dims.w}px`;
    canvas.style.height = `${dims.h}px`;
    ctx.scale(dpr, dpr);

    animationRef.current = new AnimationController(canvas, ctx, size);
    return () => animationRef.current?.destroy();
  }, [dims]);

  return (
    <div className="relative w-full h-full overflow-hidden bg-black">
      <canvas ref={canvasRef} className="absolute inset-0 block" />
    </div>
  );
}
