export type SemanticState =
  | "NEUTRAL_OBSERVING"
  | "STABLE_OPERATION"
  | "PIPELINE_AT_RISK"
  | "ALERT_ACTIVE"
  | "GOAL_ACHIEVED"
  | "UNDER_PERFORMANCE"
  | "GROWTH_ACCELERATING"
  | "BLOCKED_FLOW";

export type RenderProfile = "ULTRA" | "HIGH" | "BALANCED" | "LOW" | "DEGRADED";

export interface GeometryRecipe {
  primitive: "torus" | "torusKnot" | "sphere" | "icosahedron" | "nautilus";
  complexity: number;
  deformation: number;
  frequency: number;
  octaves: number;
  speed: number;
}

export interface MaterialRecipe {
  paletteToken: string;
  colorA: string;
  colorB: string;
  colorRim: string;
  metalness: number;
  roughness: number;
  clearcoat: number;
  transmission: number;
  ior: number;
  iridescence: number;
}

export interface MotionRecipe {
  rotationSpeed: number;
  floatAmplitude: number;
  floatFrequency: number;
  turbulence: number;
  mouseStrength: number;
}

export interface ShapeDNA {
  version: string;
  id: string;
  semanticState: SemanticState;
  renderProfile?: RenderProfile;
  geometry: GeometryRecipe;
  material: MaterialRecipe;
  motion: MotionRecipe;
}

export interface ArtifactManifest {
  artifactId: string;
  semanticState: SemanticState;
  shapeDNA: ShapeDNA;
}
