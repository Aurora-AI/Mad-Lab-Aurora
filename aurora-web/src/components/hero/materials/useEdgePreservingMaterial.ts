import { useMemo } from 'react';
import * as THREE from 'three';

export function useEdgePreservingMaterial(texture: THREE.Texture) {
  const faceMaterial = useMemo(() => {
    return new THREE.MeshStandardMaterial({
      map: texture,
      transparent: true,
      roughness: 0.6,
      metalness: 0.0,
      emissive: new THREE.Color(0x222222),
      emissiveIntensity: 0.2,
      side: THREE.DoubleSide,
      depthWrite: true,
    });
  }, [texture]);

  const edgeMaterial = useMemo(() => {
    return new THREE.MeshStandardMaterial({
      color: 0x1a1a1a,
      roughness: 0.8,
      metalness: 0.0,
      emissive: new THREE.Color(0x2a2a2a),
      emissiveIntensity: 0.4,
    });
  }, []);

  // Ordem das faces do BoxGeometry: +X, -X, +Y, -Y, +Z, -Z
  const materialsArray = useMemo(() => {
    return [
      edgeMaterial, edgeMaterial, // Lados direito/esquerdo
      edgeMaterial, edgeMaterial, // Topo/base
      faceMaterial, faceMaterial, // Frente/trás
    ];
  }, [faceMaterial, edgeMaterial]);

  return materialsArray;
}
