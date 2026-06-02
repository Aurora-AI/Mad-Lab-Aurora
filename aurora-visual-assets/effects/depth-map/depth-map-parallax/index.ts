import * as THREE from 'three/webgpu';
import { texture, uv, uniform, vec2, float, vec4 } from 'three/tsl';

/**
 * DepthMapMaterial (P001)
 * Standard Aurora implementation for Depth Map Parallax using TSL.
 * 
 * Refatorado para resiliência industrial (Seal: AURORA_TRUSTWARE)
 * 
 * @author Aurora Factory
 * @version 1.0.1
 * @pattern P001
 */
export class DepthMapMaterial extends THREE.NodeMaterial {
  map: THREE.Texture | null = null;
  depthMap: THREE.Texture | null = null;
  uMouse = uniform(vec2(0, 0));
  uIntensity = uniform(0.05);

  constructor() {
    super();
    this.transparent = true;
    this.name = 'DepthMapMaterial';
  }

  setup() {
    const vUv = uv();
    
    // Check for accessibility preference (Safe intensity)
    const isReducedMotion = typeof window !== 'undefined' 
      ? window.matchMedia('(prefers-reduced-motion: reduce)').matches 
      : false;
      
    const effectiveIntensity = isReducedMotion ? float(0) : this.uIntensity;
    
    // Fallback safe nodes (Prevents runtime crashes if textures are null)
    // In TSL, we check if the texture mapping exists.
    const depthNode = this.depthMap 
      ? texture(this.depthMap, vUv).r 
      : float(0);
    
    // P001 Core: Displacement calculation
    const displacement = this.uMouse.mul(depthNode).mul(effectiveIntensity);
    const displacedUv = vUv.add(displacement);
    
    // Final texture with fallback
    const finalTexture = this.map 
      ? texture(this.map, displacedUv) 
      : vec4(0, 0, 0, 1);
    
    return finalTexture;
  }
}
