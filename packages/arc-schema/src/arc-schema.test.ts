import { describe, expect, it } from "vitest";

import {
  ARTIFACT_MANIFEST_JSON_SCHEMA,
  ArtifactGenerationRequestSchema,
  ArtifactManifestSchema,
  OperationalStateSchema,
  SHAPE_DNA_JSON_SCHEMA,
  ShapeDNASchema,
} from "./index";

describe("arc-schema", () => {
  it("validates a canonical OperationalState payload", () => {
    const parsed = OperationalStateSchema.parse({
      source: "chronos:briefing",
      measuredAt: "2026-03-20T09:00:00.000Z",
      pipelineHealth: 0.82,
      goalProgress: 0.51,
      activeAlerts: 0,
      exceptionCount: 1,
      humanReviewRequiredCount: 0,
      queueReadyCount: 12,
      followUpCount: 3,
      avgSafetyScore: 91,
      weightedForecast: 125000,
    });

    expect(parsed.notes).toEqual([]);
    expect(parsed.pipelineHealth).toBe(0.82);
  });

  it("rejects invalid OperationalState bounds", () => {
    expect(() =>
      OperationalStateSchema.parse({
        source: "chronos:briefing",
        measuredAt: "2026-03-20T09:00:00.000Z",
        pipelineHealth: 1.1,
        goalProgress: 0.51,
        activeAlerts: -1,
        exceptionCount: 1,
        humanReviewRequiredCount: 0,
        queueReadyCount: 12,
        followUpCount: 3,
        avgSafetyScore: 91,
        weightedForecast: 125000,
      }),
    ).toThrow();
  });

  it("applies the default render profile in ArtifactGenerationRequest", () => {
    const parsed = ArtifactGenerationRequestSchema.parse({
      brief: "Highlight pipeline resilience",
      semanticState: "STABLE_OPERATION",
    });

    expect(parsed.renderProfile).toBe("BALANCED");
  });

  it("validates ShapeDNA and rejects unsupported versions", () => {
    const valid = ShapeDNASchema.parse({
      version: "2.0",
      id: "shape_01",
      createdAt: "2026-03-20T09:00:00.000Z",
      intent: "Signal stable operations",
      semanticState: "STABLE_OPERATION",
      renderProfile: "BALANCED",
      confidence: 0.92,
      geometry: {
        family: "shells",
        primitive: "superellipse",
        complexity: 0.44,
        deformation: 0.12,
        frequency: 0.8,
        octaves: 4,
        speed: 0.2,
      },
      material: {
        paletteToken: "aurora-stable",
        colorA: "#0B1020",
        colorB: "#7CD1FF",
        colorRim: "#FFFFFF",
        metalness: 0.2,
        roughness: 0.45,
        clearcoat: 0.5,
        transmission: 0.1,
        ior: 1.2,
        iridescence: 0.08,
      },
      motion: {
        profile: "calm_float",
        rotationSpeed: 0.06,
        floatAmplitude: 0.03,
        floatFrequency: 0.22,
        turbulence: 0.15,
        mouseStrength: 0.04,
        scrollReactive: false,
      },
      environment: {
        hdri: "aurora-dome",
        hdriIntensity: 1.6,
        bloomIntensity: 0.22,
        vignetteStrength: 0.18,
        chromaticAberration: 0.001,
        depthOfFieldStrength: 0.12,
      },
      qaScore: 8.9,
      agentTrace: {
        architect: "alpha_architect",
        physicist: "beta_physicist",
        engineer: "gamma_engineer",
        critic: "delta_critic",
      },
    });

    expect(valid.qaIssues).toEqual([]);
    expect(valid.artifactRef).toBeNull();

    expect(() =>
      ShapeDNASchema.parse({
        ...valid,
        version: "1.0",
      }),
    ).toThrow();
  });

  it("validates ArtifactManifest with nested outputs and qa report", () => {
    const parsed = ArtifactManifestSchema.parse({
      manifestVersion: "1.0",
      artifactId: "artifact_01",
      generatedAt: "2026-03-20T09:05:00.000Z",
      brief: "Signal stable operations",
      semanticState: "STABLE_OPERATION",
      renderProfile: "BALANCED",
      family: "shells",
      ttlSeconds: 600,
      outputs: {
        manifestPath: "artifacts/arc/artifact_01/shape.manifest.json",
        dnaPath: "artifacts/arc/artifact_01/shape.dna.json",
        materialRecipePath: "artifacts/arc/artifact_01/material.recipe.json",
        environmentRecipePath: "artifacts/arc/artifact_01/environment.recipe.json",
        qaReportPath: "artifacts/arc/artifact_01/qa.report.json",
        previewPath: "artifacts/arc/artifact_01/preview.png",
      },
      shapeDNA: {
        version: "2.0",
        id: "shape_01",
        createdAt: "2026-03-20T09:00:00.000Z",
        intent: "Signal stable operations",
        semanticState: "STABLE_OPERATION",
        renderProfile: "BALANCED",
        confidence: 0.92,
        geometry: {
          family: "shells",
          primitive: "superellipse",
          complexity: 0.44,
          deformation: 0.12,
          frequency: 0.8,
          octaves: 4,
          speed: 0.2,
        },
        material: {
          paletteToken: "aurora-stable",
          colorA: "#0B1020",
          colorB: "#7CD1FF",
          colorRim: "#FFFFFF",
          metalness: 0.2,
          roughness: 0.45,
          clearcoat: 0.5,
          transmission: 0.1,
          ior: 1.2,
          iridescence: 0.08,
        },
        motion: {
          profile: "calm_float",
          rotationSpeed: 0.06,
          floatAmplitude: 0.03,
          floatFrequency: 0.22,
          turbulence: 0.15,
          mouseStrength: 0.04,
          scrollReactive: false,
        },
        environment: {
          hdri: "aurora-dome",
          hdriIntensity: 1.6,
          bloomIntensity: 0.22,
          vignetteStrength: 0.18,
          chromaticAberration: 0.001,
          depthOfFieldStrength: 0.12,
        },
        qaScore: 8.9,
        qaIssues: [],
        artifactRef: "artifact_01",
        agentTrace: {
          architect: "alpha_architect",
          physicist: "beta_physicist",
          engineer: "gamma_engineer",
          critic: "delta_critic",
        },
      },
      qaReport: {
        accepted: true,
        score: 8.9,
        issues: [],
        reviewer: "delta_critic",
      },
    });

    expect(parsed.outputs.modelPath).toBeNull();
  });

  it("keeps published JSON schema descriptors stable", () => {
    expect(SHAPE_DNA_JSON_SCHEMA.title).toBe("ShapeDNA");
    expect(SHAPE_DNA_JSON_SCHEMA.required).toEqual([
      "version",
      "id",
      "createdAt",
      "intent",
      "semanticState",
      "renderProfile",
    ]);

    expect(ARTIFACT_MANIFEST_JSON_SCHEMA.title).toBe("ArtifactManifest");
    expect(ARTIFACT_MANIFEST_JSON_SCHEMA.required).toEqual([
      "manifestVersion",
      "artifactId",
      "generatedAt",
      "brief",
      "semanticState",
    ]);
  });
});
