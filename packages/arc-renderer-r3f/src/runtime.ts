import {
  ArtifactManifestSchema,
  type ArtifactManifest,
  type RenderProfile,
} from "@aurora/arc-schema";

export type RendererDeviceTier =
  | "desktop_high"
  | "desktop_balanced"
  | "mobile_low"
  | "degraded";

export interface RendererDeviceHints {
  hardwareConcurrency?: number;
  deviceMemoryGb?: number;
  maxTouchPoints?: number;
  pixelRatio?: number;
  viewportWidth?: number;
  prefersReducedMotion?: boolean;
}

export interface ArcRendererDiagnostics {
  artifactId: string | null;
  semanticState: string | null;
  requestedProfile: RenderProfile | null;
  effectiveProfile: RenderProfile | null;
  deviceTier: RendererDeviceTier;
  prefersReducedMotion: boolean;
  pixelRatio: number;
  renderable: boolean;
  renderBlockedReason: "missing_artifact" | "invalid_artifact" | null;
}

export interface ArcRendererRuntimeSnapshot {
  artifact: ArtifactManifest | null;
  diagnostics: ArcRendererDiagnostics;
  sceneSpec: SceneSpec | null;
}

export interface RendererVisualSignature {
  signatureKey: string;
  renderable: boolean;
  renderBlockedReason: ArcRendererDiagnostics["renderBlockedReason"];
  semanticState: string | null;
  family: string | null;
  primitive: string | null;
  paletteToken: string | null;
  motionProfile: string | null;
  hdri: string | null;
  requestedProfile: RenderProfile | null;
  effectiveProfile: RenderProfile | null;
  deviceTier: RendererDeviceTier;
  sceneKey: string | null;
}

export interface SceneSpec {
  dpr: [number, number];
  cameraZ: number;
  fogFar: number;
  scale: number;
}

export interface RendererDiagnosticsVisibilityOptions {
  nodeEnv?: string;
}

export function detectRendererDeviceTier(
  hints: RendererDeviceHints,
): RendererDeviceTier {
  const hardwareConcurrency = hints.hardwareConcurrency ?? 4;
  const deviceMemoryGb = hints.deviceMemoryGb ?? 4;
  const maxTouchPoints = hints.maxTouchPoints ?? 0;
  const pixelRatio = hints.pixelRatio ?? 1;
  const viewportWidth = hints.viewportWidth ?? 1280;
  const prefersReducedMotion = hints.prefersReducedMotion ?? false;
  const touchFirst = maxTouchPoints > 0 || viewportWidth < 820;

  if (
    prefersReducedMotion ||
    hardwareConcurrency <= 2 ||
    deviceMemoryGb <= 2 ||
    pixelRatio > 2.75
  ) {
    return "degraded";
  }

  if (touchFirst || hardwareConcurrency <= 4 || deviceMemoryGb <= 4) {
    return "mobile_low";
  }

  if (hardwareConcurrency >= 8 && deviceMemoryGb >= 8 && pixelRatio <= 2) {
    return "desktop_high";
  }

  return "desktop_balanced";
}

export function resolveEffectiveRenderProfile(
  requestedProfile: RenderProfile,
  hints: RendererDeviceHints,
): RenderProfile {
  const tier = detectRendererDeviceTier(hints);

  if (tier === "degraded") return "DEGRADED";
  if (tier === "mobile_low") {
    if (requestedProfile === "HIGH") return "LOW";
    if (requestedProfile === "BALANCED") return "LOW";
    return requestedProfile === "DEGRADED" ? "DEGRADED" : requestedProfile;
  }
  if (tier === "desktop_balanced" && requestedProfile === "HIGH") {
    return "BALANCED";
  }
  return requestedProfile;
}

export function sceneSpecForProfile(profile: RenderProfile): SceneSpec {
  switch (profile) {
    case "HIGH":
      return { dpr: [1, 1.8], cameraZ: 4.8, fogFar: 12, scale: 1.06 };
    case "LOW":
      return { dpr: [1, 1.2], cameraZ: 5.1, fogFar: 10.5, scale: 0.98 };
    case "DEGRADED":
      return { dpr: [1, 1], cameraZ: 5.4, fogFar: 9.6, scale: 0.92 };
    case "BALANCED":
    default:
      return { dpr: [1, 1.4], cameraZ: 5, fogFar: 11.2, scale: 1 };
  }
}

export function shouldShowRendererDiagnostics(
  diagnosticsRequested: boolean,
  options: RendererDiagnosticsVisibilityOptions = {},
) {
  if (!diagnosticsRequested) {
    return false;
  }

  return options.nodeEnv !== "production";
}

export function buildRendererDiagnostics(
  artifact: ArtifactManifest | null | undefined,
  hints: RendererDeviceHints,
): ArcRendererDiagnostics {
  const deviceTier = detectRendererDeviceTier(hints);
  const prefersReducedMotion = hints.prefersReducedMotion ?? false;
  const pixelRatio = hints.pixelRatio ?? 1;

  if (!artifact) {
    return {
      artifactId: null,
      semanticState: null,
      requestedProfile: null,
      effectiveProfile: null,
      deviceTier,
      prefersReducedMotion,
      pixelRatio,
      renderable: false,
      renderBlockedReason: "missing_artifact",
    };
  }

  const parsed = ArtifactManifestSchema.safeParse(artifact);
  if (!parsed.success) {
    return {
      artifactId: null,
      semanticState: null,
      requestedProfile: null,
      effectiveProfile: null,
      deviceTier,
      prefersReducedMotion,
      pixelRatio,
      renderable: false,
      renderBlockedReason: "invalid_artifact",
    };
  }

  const effectiveProfile = resolveEffectiveRenderProfile(
    parsed.data.renderProfile,
    hints,
  );

  return {
    artifactId: parsed.data.artifactId,
    semanticState: parsed.data.semanticState,
    requestedProfile: parsed.data.renderProfile,
    effectiveProfile,
    deviceTier,
    prefersReducedMotion,
    pixelRatio,
    renderable: true,
    renderBlockedReason: null,
  };
}

export function resolveRendererRuntimeSnapshot(
  artifact: ArtifactManifest | null | undefined,
  hints: RendererDeviceHints,
): ArcRendererRuntimeSnapshot {
  const diagnostics = buildRendererDiagnostics(artifact, hints);

  if (!artifact || !diagnostics.renderable || !diagnostics.effectiveProfile) {
    return {
      artifact: null,
      diagnostics,
      sceneSpec: null,
    };
  }

  const parsed = ArtifactManifestSchema.safeParse(artifact);
  if (!parsed.success) {
    return {
      artifact: null,
      diagnostics: {
        ...diagnostics,
        renderable: false,
        renderBlockedReason: "invalid_artifact",
        effectiveProfile: null,
      },
      sceneSpec: null,
    };
  }

  return {
    artifact: parsed.data,
    diagnostics,
    sceneSpec: sceneSpecForProfile(diagnostics.effectiveProfile),
  };
}

function buildSceneKey(sceneSpec: SceneSpec | null): string | null {
  if (!sceneSpec) {
    return null;
  }

  return [
    `dpr:${sceneSpec.dpr[0]}-${sceneSpec.dpr[1]}`,
    `cameraZ:${sceneSpec.cameraZ}`,
    `fogFar:${sceneSpec.fogFar}`,
    `scale:${sceneSpec.scale}`,
  ].join("|");
}

export function resolveRendererVisualSignature(
  artifact: ArtifactManifest | null | undefined,
  hints: RendererDeviceHints,
): RendererVisualSignature {
  const runtimeSnapshot = resolveRendererRuntimeSnapshot(artifact, hints);
  const { diagnostics, sceneSpec } = runtimeSnapshot;
  const sceneKey = buildSceneKey(sceneSpec);

  if (!runtimeSnapshot.artifact) {
    const signatureKey = [
      "blocked",
      diagnostics.renderBlockedReason ?? "unknown",
      diagnostics.deviceTier,
      diagnostics.effectiveProfile ?? "none",
      sceneKey ?? "scene:none",
    ].join("|");

    return {
      signatureKey,
      renderable: false,
      renderBlockedReason: diagnostics.renderBlockedReason,
      semanticState: diagnostics.semanticState,
      family: null,
      primitive: null,
      paletteToken: null,
      motionProfile: null,
      hdri: null,
      requestedProfile: diagnostics.requestedProfile,
      effectiveProfile: diagnostics.effectiveProfile,
      deviceTier: diagnostics.deviceTier,
      sceneKey,
    };
  }

  const { artifact: parsedArtifact } = runtimeSnapshot;
  const signatureKey = [
    parsedArtifact.semanticState,
    parsedArtifact.family,
    parsedArtifact.shapeDNA.geometry.primitive,
    parsedArtifact.shapeDNA.material.paletteToken,
    parsedArtifact.shapeDNA.motion.profile,
    parsedArtifact.shapeDNA.environment.hdri,
    diagnostics.requestedProfile,
    diagnostics.effectiveProfile,
    diagnostics.deviceTier,
    sceneKey,
  ].join("|");

  return {
    signatureKey,
    renderable: true,
    renderBlockedReason: diagnostics.renderBlockedReason,
    semanticState: parsedArtifact.semanticState,
    family: parsedArtifact.family,
    primitive: parsedArtifact.shapeDNA.geometry.primitive,
    paletteToken: parsedArtifact.shapeDNA.material.paletteToken,
    motionProfile: parsedArtifact.shapeDNA.motion.profile,
    hdri: parsedArtifact.shapeDNA.environment.hdri,
    requestedProfile: diagnostics.requestedProfile,
    effectiveProfile: diagnostics.effectiveProfile,
    deviceTier: diagnostics.deviceTier,
    sceneKey,
  };
}
