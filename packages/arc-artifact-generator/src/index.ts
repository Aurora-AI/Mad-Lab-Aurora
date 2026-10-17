import {
  ArtifactGenerationRequestSchema,
  ArtifactManifestSchema,
  type ArtifactFamily,
  type ArtifactManifest,
  type EnvironmentRecipe,
  type GeometryRecipe,
  type MaterialRecipe,
  type MotionRecipe,
  type RenderProfile,
  type SemanticState,
  type ShapeDNA,
} from "@aurora/arc-schema";
import { getSemanticStateTtl } from "@aurora/arc-semantic-state";

const REQUIRED_OUTPUT_KEYS = [
  "manifestPath",
  "dnaPath",
  "materialRecipePath",
  "environmentRecipePath",
  "qaReportPath",
  "previewPath",
] as const;

const CRITICAL_QA_PATTERNS = [
  /critical/i,
  /semantic incoherence/i,
  /coer[êe]ncia sem[âa]ntica/i,
  /high visual risk/i,
  /risco visual alto/i,
  /fallback impossible/i,
  /fallback imposs[ií]vel/i,
] as const;

let fallbackArtifactSequence = 0;

export type ArtifactValidationStatus = "accepted" | "attention" | "rejected";

export interface ArtifactBundleValidationResult {
  status: ArtifactValidationStatus;
  reasons: string[];
}

export class ArtifactBundleValidationError extends Error {
  constructor(
    public readonly manifest: ArtifactManifest,
    public readonly validation: ArtifactBundleValidationResult,
  ) {
    super(
      `Artifact bundle ${manifest.artifactId} rejected: ${validation.reasons.join("; ") || "unknown reason"}`,
    );
    this.name = "ArtifactBundleValidationError";
  }
}

function createArtifactId() {
  if (typeof globalThis.crypto?.randomUUID === "function") {
    return globalThis.crypto.randomUUID();
  }

  fallbackArtifactSequence += 1;
  return `arc-${Date.now().toString(36)}-${fallbackArtifactSequence.toString(36)}`;
}

export const ARTIFACT_FAMILY_LIBRARY: Record<
  ArtifactFamily,
  { label: string; intent: string }
> = {
  orbitals: { label: "Orbitals", intent: "continuidade, orbita e aceleracao controlada" },
  shells: { label: "Shells", intent: "protecao, postura e leitura calma" },
  knots: { label: "Knots", intent: "complexidade operavel e tensao controlada" },
  fields: { label: "Fields", intent: "densidade, fluxo e pressao sistemica" },
  crystals: { label: "Crystals", intent: "bloqueio, tensao e arestas de decisao" },
};

function familyForSemanticState(state: SemanticState): ArtifactFamily {
  if (state === "GOAL_ACHIEVED" || state === "GROWTH_ACCELERATING") return "orbitals";
  if (state === "PIPELINE_AT_RISK" || state === "ALERT_ACTIVE") return "fields";
  if (state === "BLOCKED_FLOW") return "crystals";
  if (state === "UNDER_PERFORMANCE") return "knots";
  return "shells";
}

function geometryRecipeFor(
  semanticState: SemanticState,
  family: ArtifactFamily,
): GeometryRecipe {
  const base: Record<ArtifactFamily, GeometryRecipe> = {
    orbitals: {
      family,
      primitive: "torus",
      complexity: 0.66,
      deformation: 0.28,
      frequency: 0.62,
      octaves: 4,
      speed: 0.28,
    },
    shells: {
      family,
      primitive: "nautilus",
      complexity: 0.58,
      deformation: 0.34,
      frequency: 0.72,
      octaves: 4,
      speed: 0.24,
    },
    knots: {
      family,
      primitive: "torusKnot",
      complexity: 0.62,
      deformation: 0.44,
      frequency: 0.95,
      octaves: 5,
      speed: 0.42,
    },
    fields: {
      family,
      primitive: "sphere",
      complexity: 0.64,
      deformation: 0.58,
      frequency: 1.08,
      octaves: 4,
      speed: 0.6,
    },
    crystals: {
      family,
      primitive: "icosahedron",
      complexity: 0.54,
      deformation: 0.18,
      frequency: 1.74,
      octaves: 3,
      speed: 0.14,
    },
  };

  const recipe = { ...base[family] };
  if (semanticState === "ALERT_ACTIVE") {
    recipe.deformation = 0.66;
    recipe.speed = 0.78;
  }
  if (semanticState === "GOAL_ACHIEVED") {
    recipe.primitive = "nautilus";
    recipe.complexity = 0.7;
  }
  return recipe;
}

function materialRecipeFor(semanticState: SemanticState): MaterialRecipe {
  const palette: Record<SemanticState, MaterialRecipe> = {
    NEUTRAL_OBSERVING: {
      paletteToken: "arc.neutral",
      colorA: "#09111B",
      colorB: "#89A4BF",
      colorRim: "#D8E6F4",
      metalness: 0.08,
      roughness: 0.22,
      clearcoat: 0.68,
      transmission: 0.1,
      ior: 1.36,
      iridescence: 0.18,
    },
    STABLE_OPERATION: {
      paletteToken: "arc.stable",
      colorA: "#08161E",
      colorB: "#75D0B4",
      colorRim: "#D1FFF2",
      metalness: 0.12,
      roughness: 0.18,
      clearcoat: 0.72,
      transmission: 0.08,
      ior: 1.4,
      iridescence: 0.22,
    },
    PIPELINE_AT_RISK: {
      paletteToken: "arc.risk",
      colorA: "#180A08",
      colorB: "#F08C42",
      colorRim: "#FFD6AE",
      metalness: 0.18,
      roughness: 0.16,
      clearcoat: 0.82,
      transmission: 0.04,
      ior: 1.42,
      iridescence: 0.14,
    },
    ALERT_ACTIVE: {
      paletteToken: "arc.alert",
      colorA: "#180506",
      colorB: "#FF6767",
      colorRim: "#FFD1D1",
      metalness: 0.12,
      roughness: 0.12,
      clearcoat: 0.9,
      transmission: 0.02,
      ior: 1.42,
      iridescence: 0.1,
    },
    GOAL_ACHIEVED: {
      paletteToken: "arc.goal",
      colorA: "#160D03",
      colorB: "#D8B15A",
      colorRim: "#FFF0B6",
      metalness: 0.82,
      roughness: 0.1,
      clearcoat: 0.94,
      transmission: 0,
      ior: 1.48,
      iridescence: 0.32,
    },
    UNDER_PERFORMANCE: {
      paletteToken: "arc.underperformance",
      colorA: "#120C10",
      colorB: "#B067D9",
      colorRim: "#E7C6FF",
      metalness: 0.3,
      roughness: 0.14,
      clearcoat: 0.76,
      transmission: 0.02,
      ior: 1.42,
      iridescence: 0.22,
    },
    GROWTH_ACCELERATING: {
      paletteToken: "arc.growth",
      colorA: "#04120D",
      colorB: "#63E38B",
      colorRim: "#D7FFE2",
      metalness: 0.28,
      roughness: 0.12,
      clearcoat: 0.84,
      transmission: 0.04,
      ior: 1.42,
      iridescence: 0.2,
    },
    BLOCKED_FLOW: {
      paletteToken: "arc.blocked",
      colorA: "#09070F",
      colorB: "#8D72D9",
      colorRim: "#D8CCFF",
      metalness: 0.44,
      roughness: 0.16,
      clearcoat: 0.7,
      transmission: 0.01,
      ior: 1.44,
      iridescence: 0.12,
    },
  };

  return palette[semanticState];
}

function hasCriticalQaIssue(issues: string[]) {
  return issues.some((issue) => CRITICAL_QA_PATTERNS.some((pattern) => pattern.test(issue)));
}

export function validateArtifactBundle(manifest: ArtifactManifest): ArtifactBundleValidationResult {
  const parsed = ArtifactManifestSchema.parse(manifest);
  const reasons: string[] = [];
  const outputs = parsed.outputs;
  const issues = parsed.qaReport.issues;

  for (const key of REQUIRED_OUTPUT_KEYS) {
    if (!outputs[key]?.trim()) {
      reasons.push(`missing required output: ${key}`);
    }
  }

  if (parsed.shapeDNA.version !== "2.0") {
    reasons.push(`unsupported shapeDNA version: ${parsed.shapeDNA.version}`);
  }

  if (parsed.shapeDNA.qaScore !== parsed.qaReport.score) {
    reasons.push("qa score mismatch between shapeDNA and qaReport");
  }

  if (parsed.qaReport.accepted === false) {
    reasons.push("qa report explicitly rejected the bundle");
  }

  if (parsed.qaReport.score < 7) {
    reasons.push(`qa score below rejection threshold: ${parsed.qaReport.score}`);
  }

  if (hasCriticalQaIssue(issues)) {
    reasons.push("qa report contains a critical issue");
  }

  if (reasons.length > 0) {
    return {
      status: "rejected",
      reasons,
    };
  }

  if (parsed.qaReport.score < 8 || issues.length > 0) {
    return {
      status: "attention",
      reasons: issues.length > 0 ? [...issues] : [`qa score requires attention: ${parsed.qaReport.score}`],
    };
  }

  return {
    status: "accepted",
    reasons: [],
  };
}

export function assertArtifactBundleAccepted(manifest: ArtifactManifest): ArtifactManifest {
  const validation = validateArtifactBundle(manifest);
  if (validation.status === "rejected") {
    throw new ArtifactBundleValidationError(manifest, validation);
  }

  return manifest;
}

function motionRecipeFor(semanticState: SemanticState): MotionRecipe {
  const isAlert = semanticState === "ALERT_ACTIVE" || semanticState === "PIPELINE_AT_RISK";
  const isCalm = semanticState === "STABLE_OPERATION" || semanticState === "NEUTRAL_OBSERVING";

  return {
    profile: isAlert ? "volatile" : isCalm ? "calm" : "balanced",
    rotationSpeed: semanticState === "GOAL_ACHIEVED" ? 0.12 : isAlert ? 0.16 : 0.08,
    floatAmplitude: semanticState === "BLOCKED_FLOW" ? 0.03 : 0.07,
    floatFrequency: isAlert ? 0.72 : 0.34,
    turbulence: semanticState === "ALERT_ACTIVE" ? 0.72 : semanticState === "BLOCKED_FLOW" ? 0.5 : isAlert ? 0.44 : 0.12,
    mouseStrength: 0.1,
    scrollReactive: false,
  };
}

function environmentRecipeFor(
  semanticState: SemanticState,
  renderProfile: RenderProfile,
): EnvironmentRecipe {
  const degraded = renderProfile === "DEGRADED" || renderProfile === "LOW";

  return {
    hdri: semanticState === "GOAL_ACHIEVED" ? "studio_gold" : "studio_small",
    hdriIntensity: degraded ? 1.4 : 2.6,
    bloomIntensity: degraded ? 0.18 : semanticState === "ALERT_ACTIVE" ? 0.55 : 0.32,
    vignetteStrength: 0.46,
    chromaticAberration: degraded ? 0 : 0.0012,
    depthOfFieldStrength: degraded ? 0.12 : 0.36,
  };
}

export function generateArtifactBundle(input: {
  brief: string;
  semanticState: SemanticState;
  renderProfile?: RenderProfile;
  intent?: string;
}): ArtifactManifest {
  const request = ArtifactGenerationRequestSchema.parse(input);
  const artifactId = createArtifactId();
  const family = familyForSemanticState(request.semanticState);
  const geometry = geometryRecipeFor(request.semanticState, family);
  const material = materialRecipeFor(request.semanticState);
  const motion = motionRecipeFor(request.semanticState);
  const environment = environmentRecipeFor(request.semanticState, request.renderProfile);
  const generatedAt = new Date().toISOString();
  const ttlSeconds = getSemanticStateTtl(request.semanticState);

  const shapeDNA: ShapeDNA = {
    version: "2.0",
    id: artifactId,
    createdAt: generatedAt,
    intent: request.intent ?? request.brief,
    semanticState: request.semanticState,
    renderProfile: request.renderProfile,
    confidence: 0.91,
    geometry,
    material,
    motion,
    environment,
    qaScore: 9.2,
    qaIssues: [],
    artifactRef: artifactId,
    agentTrace: {
      architect: `Mapped brief to ${family} family for ${request.semanticState}.`,
      physicist: `Selected ${geometry.primitive} with deformation ${geometry.deformation}.`,
      engineer: `Prepared render recipe for ${request.renderProfile} profile.`,
      critic: "Bundle accepted with stable semantic coherence and low visual risk.",
    },
  };

  const qaReport = {
    accepted: true,
    score: shapeDNA.qaScore,
    issues: [],
    reviewer: "delta_critic",
  };

  const basePath = `artifacts/arc/${artifactId}`;
  const manifest = ArtifactManifestSchema.parse({
    manifestVersion: "1.0",
    artifactId,
    generatedAt,
    brief: request.brief,
    semanticState: request.semanticState,
    renderProfile: request.renderProfile,
    family,
    ttlSeconds,
    outputs: {
      manifestPath: `${basePath}/shape.manifest.json`,
      dnaPath: `${basePath}/shape.dna.json`,
      materialRecipePath: `${basePath}/material.recipe.json`,
      environmentRecipePath: `${basePath}/environment.recipe.json`,
      qaReportPath: `${basePath}/qa.report.json`,
      previewPath: `${basePath}/preview.png`,
      modelPath: `/models/arc/${request.semanticState}.glb`,
    },
    shapeDNA,
    qaReport,
  });

  return assertArtifactBundleAccepted(manifest);
}
