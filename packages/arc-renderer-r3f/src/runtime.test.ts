import { describe, expect, it } from "vitest";
import { generateArtifactBundle } from "@aurora/arc-artifact-generator";
import {
  buildRendererDiagnostics,
  detectRendererDeviceTier,
  resolveRendererVisualSignature,
  resolveEffectiveRenderProfile,
  resolveRendererRuntimeSnapshot,
  sceneSpecForProfile,
  shouldShowRendererDiagnostics,
} from "./runtime";

describe("arc-renderer runtime helpers", () => {
  it("detects high tier desktop devices", () => {
    expect(
      detectRendererDeviceTier({
        hardwareConcurrency: 12,
        deviceMemoryGb: 16,
        maxTouchPoints: 0,
        pixelRatio: 1.5,
        viewportWidth: 1440,
      }),
    ).toBe("desktop_high");
  });

  it("degrades profile on constrained or reduced-motion devices", () => {
    expect(
      resolveEffectiveRenderProfile("HIGH", {
        hardwareConcurrency: 4,
        deviceMemoryGb: 4,
        maxTouchPoints: 5,
        pixelRatio: 3,
        viewportWidth: 390,
      }),
    ).toBe("DEGRADED");

    expect(
      resolveEffectiveRenderProfile("BALANCED", {
        hardwareConcurrency: 6,
        deviceMemoryGb: 8,
        prefersReducedMotion: true,
      }),
    ).toBe("DEGRADED");
  });

  it("builds diagnostics with requested and effective profiles", () => {
    const artifact = generateArtifactBundle({
      brief: "renderer diagnostics",
      semanticState: "GROWTH_ACCELERATING",
      renderProfile: "HIGH",
    });

    const diagnostics = buildRendererDiagnostics(artifact, {
      hardwareConcurrency: 4,
      deviceMemoryGb: 4,
      maxTouchPoints: 2,
      pixelRatio: 2,
      viewportWidth: 768,
    });

    expect(diagnostics.artifactId).toBe(artifact.artifactId);
    expect(diagnostics.requestedProfile).toBe("HIGH");
    expect(diagnostics.effectiveProfile).toBe("LOW");
    expect(diagnostics.deviceTier).toBe("mobile_low");
    expect(diagnostics.renderable).toBe(true);
    expect(diagnostics.renderBlockedReason).toBeNull();
  });

  it("provides stable scene specs for every render profile", () => {
    expect(sceneSpecForProfile("HIGH")).toEqual({
      dpr: [1, 1.8],
      cameraZ: 4.8,
      fogFar: 12,
      scale: 1.06,
    });
    expect(sceneSpecForProfile("BALANCED")).toEqual({
      dpr: [1, 1.4],
      cameraZ: 5,
      fogFar: 11.2,
      scale: 1,
    });
    expect(sceneSpecForProfile("LOW")).toEqual({
      dpr: [1, 1.2],
      cameraZ: 5.1,
      fogFar: 10.5,
      scale: 0.98,
    });
    expect(sceneSpecForProfile("DEGRADED")).toEqual({
      dpr: [1, 1],
      cameraZ: 5.4,
      fogFar: 9.6,
      scale: 0.92,
    });
  });

  it("uses defensive defaults when device hints are absent", () => {
    expect(detectRendererDeviceTier({})).toBe("mobile_low");
    expect(resolveEffectiveRenderProfile("HIGH", {})).toBe("LOW");
  });

  it("builds diagnostics deterministically with partial hints", () => {
    const artifact = generateArtifactBundle({
      brief: "renderer defaults",
      semanticState: "STABLE_OPERATION",
      renderProfile: "BALANCED",
    });

    const diagnostics = buildRendererDiagnostics(artifact, {
      pixelRatio: 1.25,
    });

    expect(diagnostics.artifactId).toBe(artifact.artifactId);
    expect(diagnostics.semanticState).toBe("STABLE_OPERATION");
    expect(diagnostics.requestedProfile).toBe("BALANCED");
    expect(diagnostics.effectiveProfile).toBe("LOW");
    expect(diagnostics.deviceTier).toBe("mobile_low");
    expect(diagnostics.prefersReducedMotion).toBe(false);
    expect(diagnostics.pixelRatio).toBe(1.25);
    expect(diagnostics.renderable).toBe(true);
    expect(diagnostics.renderBlockedReason).toBeNull();
  });

  it("reports non-renderable diagnostics when artifact is missing", () => {
    const diagnostics = buildRendererDiagnostics(null, {
      pixelRatio: 1.4,
      prefersReducedMotion: true,
    });

    expect(diagnostics.artifactId).toBeNull();
    expect(diagnostics.semanticState).toBeNull();
    expect(diagnostics.requestedProfile).toBeNull();
    expect(diagnostics.effectiveProfile).toBeNull();
    expect(diagnostics.renderable).toBe(false);
    expect(diagnostics.renderBlockedReason).toBe("missing_artifact");
    expect(diagnostics.prefersReducedMotion).toBe(true);
    expect(diagnostics.pixelRatio).toBe(1.4);
  });

  it("returns an empty runtime snapshot for invalid artifacts", () => {
    const invalidArtifact = {
      artifactId: "broken",
      renderProfile: "HIGH",
    } as unknown as ReturnType<typeof generateArtifactBundle>;

    const snapshot = resolveRendererRuntimeSnapshot(invalidArtifact, {
      hardwareConcurrency: 8,
      deviceMemoryGb: 8,
      pixelRatio: 1.5,
    });

    expect(snapshot.artifact).toBeNull();
    expect(snapshot.sceneSpec).toBeNull();
    expect(snapshot.diagnostics.renderable).toBe(false);
    expect(snapshot.diagnostics.renderBlockedReason).toBe("invalid_artifact");
    expect(snapshot.diagnostics.deviceTier).toBe("desktop_high");
  });

  it("shows diagnostics only outside production when explicitly requested", () => {
    expect(
      shouldShowRendererDiagnostics(false, {
        nodeEnv: "development",
      }),
    ).toBe(false);

    expect(
      shouldShowRendererDiagnostics(true, {
        nodeEnv: "production",
      }),
    ).toBe(false);

    expect(
      shouldShowRendererDiagnostics(true, {
        nodeEnv: "development",
      }),
    ).toBe(true);
  });

  it("builds distinct visual signatures for critical semantic states", () => {
    const sharedHints = {
      hardwareConcurrency: 8,
      deviceMemoryGb: 8,
      maxTouchPoints: 0,
      pixelRatio: 1.5,
      viewportWidth: 1440,
    };

    const alertSignature = resolveRendererVisualSignature(
      generateArtifactBundle({
        brief: "alert signature",
        semanticState: "ALERT_ACTIVE",
        renderProfile: "HIGH",
      }),
      sharedHints,
    );
    const riskSignature = resolveRendererVisualSignature(
      generateArtifactBundle({
        brief: "risk signature",
        semanticState: "PIPELINE_AT_RISK",
        renderProfile: "HIGH",
      }),
      sharedHints,
    );
    const goalSignature = resolveRendererVisualSignature(
      generateArtifactBundle({
        brief: "goal signature",
        semanticState: "GOAL_ACHIEVED",
        renderProfile: "HIGH",
      }),
      sharedHints,
    );
    const blockedSignature = resolveRendererVisualSignature(
      generateArtifactBundle({
        brief: "blocked signature",
        semanticState: "BLOCKED_FLOW",
        renderProfile: "HIGH",
      }),
      sharedHints,
    );

    expect(alertSignature.renderable).toBe(true);
    expect(alertSignature.semanticState).toBe("ALERT_ACTIVE");
    expect(alertSignature.family).toBe("fields");
    expect(alertSignature.paletteToken).toBe("arc.alert");
    expect(alertSignature.motionProfile).toBe("volatile");
    expect(alertSignature.sceneKey).toBe("dpr:1-1.8|cameraZ:4.8|fogFar:12|scale:1.06");

    expect(riskSignature.semanticState).toBe("PIPELINE_AT_RISK");
    expect(riskSignature.family).toBe("fields");
    expect(riskSignature.paletteToken).toBe("arc.risk");
    expect(riskSignature.motionProfile).toBe("volatile");

    expect(goalSignature.semanticState).toBe("GOAL_ACHIEVED");
    expect(goalSignature.family).toBe("orbitals");
    expect(goalSignature.primitive).toBe("nautilus");
    expect(goalSignature.paletteToken).toBe("arc.goal");

    expect(blockedSignature.semanticState).toBe("BLOCKED_FLOW");
    expect(blockedSignature.family).toBe("crystals");
    expect(blockedSignature.primitive).toBe("icosahedron");
    expect(blockedSignature.motionProfile).toBe("balanced");

    expect(alertSignature.signatureKey).not.toBe(riskSignature.signatureKey);
    expect(alertSignature.signatureKey).not.toBe(goalSignature.signatureKey);
    expect(goalSignature.signatureKey).not.toBe(blockedSignature.signatureKey);
  });

  it("builds an auditable blocked signature when artifact cannot render", () => {
    const blocked = resolveRendererVisualSignature(null, {
      hardwareConcurrency: 2,
      deviceMemoryGb: 2,
      pixelRatio: 3,
      prefersReducedMotion: true,
    });

    expect(blocked.renderable).toBe(false);
    expect(blocked.renderBlockedReason).toBe("missing_artifact");
    expect(blocked.deviceTier).toBe("degraded");
    expect(blocked.signatureKey).toBe("blocked|missing_artifact|degraded|none|scene:none");
    expect(blocked.family).toBeNull();
    expect(blocked.sceneKey).toBeNull();
  });

  it("keeps critical semantic-state signatures unique across the renderer matrix", () => {
    const sharedHints = {
      hardwareConcurrency: 8,
      deviceMemoryGb: 8,
      maxTouchPoints: 0,
      pixelRatio: 1.5,
      viewportWidth: 1440,
    };
    const expectedFamilies = [
      { semanticState: "ALERT_ACTIVE", family: "fields" },
      { semanticState: "PIPELINE_AT_RISK", family: "fields" },
      { semanticState: "GOAL_ACHIEVED", family: "orbitals" },
      { semanticState: "BLOCKED_FLOW", family: "crystals" },
      { semanticState: "STABLE_OPERATION", family: "shells" },
      { semanticState: "NEUTRAL_OBSERVING", family: "shells" },
      { semanticState: "UNDER_PERFORMANCE", family: "knots" },
      { semanticState: "GROWTH_ACCELERATING", family: "orbitals" },
    ] as const;

    const signatures = expectedFamilies.map((entry) =>
      resolveRendererVisualSignature(
        generateArtifactBundle({
          brief: `${entry.semanticState} renderer matrix`,
          semanticState: entry.semanticState,
          renderProfile: "HIGH",
        }),
        sharedHints,
      ),
    );

    expect(new Set(signatures.map((signature) => signature.signatureKey)).size).toBe(
      expectedFamilies.length,
    );

    signatures.forEach((signature, index) => {
      expect(signature.renderable).toBe(true);
      expect(signature.semanticState).toBe(expectedFamilies[index].semanticState);
      expect(signature.family).toBe(expectedFamilies[index].family);
      expect(signature.requestedProfile).toBe("HIGH");
      expect(signature.effectiveProfile).toBe("HIGH");
      expect(signature.deviceTier).toBe("desktop_high");
    });
  });

  it("captures profile degradation without collapsing renderer identity", () => {
    const artifact = generateArtifactBundle({
      brief: "profile degradation matrix",
      semanticState: "STABLE_OPERATION",
      renderProfile: "HIGH",
    });

    const desktopHigh = resolveRendererVisualSignature(artifact, {
      hardwareConcurrency: 8,
      deviceMemoryGb: 8,
      maxTouchPoints: 0,
      pixelRatio: 1.5,
      viewportWidth: 1440,
    });
    const mobileLow = resolveRendererVisualSignature(artifact, {
      hardwareConcurrency: 4,
      deviceMemoryGb: 4,
      maxTouchPoints: 5,
      pixelRatio: 2,
      viewportWidth: 390,
    });
    const reducedMotion = resolveRendererVisualSignature(artifact, {
      hardwareConcurrency: 8,
      deviceMemoryGb: 8,
      maxTouchPoints: 0,
      pixelRatio: 1.5,
      viewportWidth: 1440,
      prefersReducedMotion: true,
    });

    expect(desktopHigh.semanticState).toBe("STABLE_OPERATION");
    expect(mobileLow.semanticState).toBe("STABLE_OPERATION");
    expect(reducedMotion.semanticState).toBe("STABLE_OPERATION");

    expect(desktopHigh.family).toBe("shells");
    expect(mobileLow.family).toBe("shells");
    expect(reducedMotion.family).toBe("shells");

    expect(desktopHigh.effectiveProfile).toBe("HIGH");
    expect(mobileLow.effectiveProfile).toBe("LOW");
    expect(reducedMotion.effectiveProfile).toBe("DEGRADED");

    expect(desktopHigh.sceneKey).not.toBe(mobileLow.sceneKey);
    expect(mobileLow.sceneKey).not.toBe(reducedMotion.sceneKey);
    expect(desktopHigh.signatureKey).not.toBe(mobileLow.signatureKey);
    expect(mobileLow.signatureKey).not.toBe(reducedMotion.signatureKey);
  });
});
