import { z } from "zod";

export const SemanticStateSchema = z.enum([
  "NEUTRAL_OBSERVING",
  "STABLE_OPERATION",
  "PIPELINE_AT_RISK",
  "ALERT_ACTIVE",
  "GOAL_ACHIEVED",
  "UNDER_PERFORMANCE",
  "GROWTH_ACCELERATING",
  "BLOCKED_FLOW",
]);

export type SemanticState = z.infer<typeof SemanticStateSchema>;

export const RenderProfileSchema = z.enum(["HIGH", "BALANCED", "LOW", "DEGRADED"]);
export type RenderProfile = z.infer<typeof RenderProfileSchema>;

export const ArtifactFamilySchema = z.enum([
  "orbitals",
  "shells",
  "knots",
  "fields",
  "crystals",
]);
export type ArtifactFamily = z.infer<typeof ArtifactFamilySchema>;

export const OperationalStateSchema = z.object({
  source: z.string(),
  measuredAt: z.string(),
  pipelineHealth: z.number().min(0).max(1),
  goalProgress: z.number().min(0).max(1),
  activeAlerts: z.number().int().nonnegative(),
  exceptionCount: z.number().int().nonnegative(),
  humanReviewRequiredCount: z.number().int().nonnegative(),
  queueReadyCount: z.number().int().nonnegative(),
  followUpCount: z.number().int().nonnegative(),
  avgSafetyScore: z.number().min(0).max(100),
  weightedForecast: z.number().nonnegative(),
  notes: z.array(z.string()).default([]),
});

export type OperationalState = z.infer<typeof OperationalStateSchema>;

export const GeometryRecipeSchema = z.object({
  family: ArtifactFamilySchema,
  primitive: z.string(),
  complexity: z.number().min(0).max(1),
  deformation: z.number().min(0).max(1),
  frequency: z.number().min(0.1).max(2.5),
  octaves: z.number().int().min(2).max(6),
  speed: z.number().min(0).max(1.5),
});
export type GeometryRecipe = z.infer<typeof GeometryRecipeSchema>;

export const MaterialRecipeSchema = z.object({
  paletteToken: z.string(),
  colorA: z.string(),
  colorB: z.string(),
  colorRim: z.string(),
  metalness: z.number().min(0).max(1),
  roughness: z.number().min(0).max(1),
  clearcoat: z.number().min(0).max(1),
  transmission: z.number().min(0).max(1),
  ior: z.number().min(1).max(2.5),
  iridescence: z.number().min(0).max(1),
});
export type MaterialRecipe = z.infer<typeof MaterialRecipeSchema>;

export const MotionRecipeSchema = z.object({
  profile: z.string(),
  rotationSpeed: z.number().min(0).max(0.3),
  floatAmplitude: z.number().min(0).max(0.2),
  floatFrequency: z.number().min(0).max(1),
  turbulence: z.number().min(0).max(1),
  mouseStrength: z.number().min(0).max(0.25),
  scrollReactive: z.boolean(),
});
export type MotionRecipe = z.infer<typeof MotionRecipeSchema>;

export const EnvironmentRecipeSchema = z.object({
  hdri: z.string(),
  hdriIntensity: z.number().min(0).max(5),
  bloomIntensity: z.number().min(0).max(1.5),
  vignetteStrength: z.number().min(0).max(1),
  chromaticAberration: z.number().min(0).max(0.005),
  depthOfFieldStrength: z.number().min(0).max(1),
});
export type EnvironmentRecipe = z.infer<typeof EnvironmentRecipeSchema>;

export const ShapeDNASchema = z.object({
  version: z.literal("2.0"),
  id: z.string(),
  createdAt: z.string(),
  intent: z.string(),
  semanticState: SemanticStateSchema,
  renderProfile: RenderProfileSchema,
  confidence: z.number().min(0).max(1),
  geometry: GeometryRecipeSchema,
  material: MaterialRecipeSchema,
  motion: MotionRecipeSchema,
  environment: EnvironmentRecipeSchema,
  qaScore: z.number().min(0).max(10),
  qaIssues: z.array(z.string()).default([]),
  artifactRef: z.string().nullable().default(null),
  agentTrace: z.object({
    architect: z.string(),
    physicist: z.string(),
    engineer: z.string(),
    critic: z.string(),
  }),
});
export type ShapeDNA = z.infer<typeof ShapeDNASchema>;

export const QaReportSchema = z.object({
  accepted: z.boolean(),
  score: z.number().min(0).max(10),
  issues: z.array(z.string()).default([]),
  reviewer: z.string(),
});
export type QaReport = z.infer<typeof QaReportSchema>;

export const ArtifactOutputsSchema = z.object({
  manifestPath: z.string(),
  dnaPath: z.string(),
  materialRecipePath: z.string(),
  environmentRecipePath: z.string(),
  qaReportPath: z.string(),
  previewPath: z.string(),
  modelPath: z.string().nullable().default(null),
});
export type ArtifactOutputs = z.infer<typeof ArtifactOutputsSchema>;

export const ArtifactManifestSchema = z.object({
  manifestVersion: z.literal("1.0"),
  artifactId: z.string(),
  generatedAt: z.string(),
  brief: z.string(),
  semanticState: SemanticStateSchema,
  renderProfile: RenderProfileSchema,
  family: ArtifactFamilySchema,
  ttlSeconds: z.number().int().positive(),
  outputs: ArtifactOutputsSchema,
  shapeDNA: ShapeDNASchema,
  qaReport: QaReportSchema,
});
export type ArtifactManifest = z.infer<typeof ArtifactManifestSchema>;

export const ArtifactGenerationRequestSchema = z.object({
  brief: z.string().min(1),
  semanticState: SemanticStateSchema,
  renderProfile: RenderProfileSchema.default("BALANCED"),
  intent: z.string().optional(),
});
export type ArtifactGenerationRequest = z.infer<typeof ArtifactGenerationRequestSchema>;

export const SHAPE_DNA_JSON_SCHEMA = {
  $schema: "https://json-schema.org/draft/2020-12/schema",
  title: "ShapeDNA",
  type: "object",
  required: ["version", "id", "createdAt", "intent", "semanticState", "renderProfile"],
} as const;

export const ARTIFACT_MANIFEST_JSON_SCHEMA = {
  $schema: "https://json-schema.org/draft/2020-12/schema",
  title: "ArtifactManifest",
  type: "object",
  required: ["manifestVersion", "artifactId", "generatedAt", "brief", "semanticState"],
} as const;
