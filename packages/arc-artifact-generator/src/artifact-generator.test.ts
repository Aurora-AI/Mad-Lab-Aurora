import { mkdtemp, readFile, rm, stat, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { ArtifactManifestSchema } from "@aurora/arc-schema";
import {
  ARTIFACT_FAMILY_LIBRARY,
  ArtifactBundleValidationError,
  generateArtifactBundle,
  validateArtifactBundle,
} from "./index";
import { persistArtifactBundle } from "./persistence";

const tempDirs: string[] = [];

afterEach(async () => {
  await Promise.all(
    tempDirs.splice(0).map((dir) => rm(dir, { recursive: true, force: true })),
  );
});

describe("arc-artifact-generator", () => {
  it("generates a valid artifact bundle contract", () => {
    const bundle = generateArtifactBundle({
      brief: "Chronos pipeline under human review pressure",
      semanticState: "PIPELINE_AT_RISK",
      renderProfile: "BALANCED",
    });

    expect(() => ArtifactManifestSchema.parse(bundle)).not.toThrow();
    expect(bundle.outputs.manifestPath).toMatch(/^artifacts\/arc\//);
    expect(bundle.outputs.previewPath.endsWith("preview.png")).toBe(true);
    expect(bundle.shapeDNA.version).toBe("2.0");
    expect(validateArtifactBundle(bundle)).toEqual({ status: "accepted", reasons: [] });
  });

  it("keeps the initial ARC family catalog stable", () => {
    expect(ARTIFACT_FAMILY_LIBRARY).toEqual({
      orbitals: { label: "Orbitals", intent: "continuidade, orbita e aceleracao controlada" },
      shells: { label: "Shells", intent: "protecao, postura e leitura calma" },
      knots: { label: "Knots", intent: "complexidade operavel e tensao controlada" },
      fields: { label: "Fields", intent: "densidade, fluxo e pressao sistemica" },
      crystals: { label: "Crystals", intent: "bloqueio, tensao e arestas de decisao" },
    });
  });

  it("maps semantic states to the expected initial visual families", () => {
    expect(
      generateArtifactBundle({
        brief: "Goal achieved",
        semanticState: "GOAL_ACHIEVED",
      }).family,
    ).toBe("orbitals");
    expect(
      generateArtifactBundle({
        brief: "Growth accelerating",
        semanticState: "GROWTH_ACCELERATING",
      }).family,
    ).toBe("orbitals");
    expect(
      generateArtifactBundle({
        brief: "Pipeline risk",
        semanticState: "PIPELINE_AT_RISK",
      }).family,
    ).toBe("fields");
    expect(
      generateArtifactBundle({
        brief: "Alert active",
        semanticState: "ALERT_ACTIVE",
      }).family,
    ).toBe("fields");
    expect(
      generateArtifactBundle({
        brief: "Blocked flow",
        semanticState: "BLOCKED_FLOW",
      }).family,
    ).toBe("crystals");
    expect(
      generateArtifactBundle({
        brief: "Under performance",
        semanticState: "UNDER_PERFORMANCE",
      }).family,
    ).toBe("knots");
    expect(
      generateArtifactBundle({
        brief: "Stable operation",
        semanticState: "STABLE_OPERATION",
      }).family,
    ).toBe("shells");
    expect(
      generateArtifactBundle({
        brief: "Neutral observing",
        semanticState: "NEUTRAL_OBSERVING",
      }).family,
    ).toBe("shells");
  });

  it("keeps critical recipe overrides stable for alert, goal and degraded profiles", () => {
    const alertBundle = generateArtifactBundle({
      brief: "Alert pressure",
      semanticState: "ALERT_ACTIVE",
      renderProfile: "BALANCED",
    });
    const goalBundle = generateArtifactBundle({
      brief: "Goal celebration",
      semanticState: "GOAL_ACHIEVED",
      renderProfile: "HIGH",
    });
    const degradedBundle = generateArtifactBundle({
      brief: "Degraded stability",
      semanticState: "STABLE_OPERATION",
      renderProfile: "DEGRADED",
    });

    expect(alertBundle.shapeDNA.geometry.deformation).toBe(0.66);
    expect(alertBundle.shapeDNA.geometry.speed).toBe(0.78);
    expect(goalBundle.shapeDNA.geometry.primitive).toBe("nautilus");
    expect(goalBundle.shapeDNA.geometry.complexity).toBe(0.7);
    expect(degradedBundle.shapeDNA.environment.hdriIntensity).toBe(1.4);
    expect(degradedBundle.shapeDNA.environment.chromaticAberration).toBe(0);
    expect(degradedBundle.shapeDNA.environment.depthOfFieldStrength).toBe(0.12);
  });

  it("persists manifest, dna, recipes, qa and preview files to disk", async () => {
    const bundle = generateArtifactBundle({
      brief: "Stage artifact persistence contract",
      semanticState: "STABLE_OPERATION",
      renderProfile: "HIGH",
    });
    const rootDir = await mkdtemp(join(tmpdir(), "arc-artifact-generator-"));
    tempDirs.push(rootDir);

    const result = await persistArtifactBundle(bundle, { rootDir });

    expect(result.writtenFiles).toHaveLength(6);

    const manifestPath = resolve(rootDir, bundle.outputs.manifestPath);
    const dnaPath = resolve(rootDir, bundle.outputs.dnaPath);
    const previewPath = resolve(rootDir, bundle.outputs.previewPath);

    const manifestContent = JSON.parse(await readFile(manifestPath, "utf-8"));
    const dnaContent = JSON.parse(await readFile(dnaPath, "utf-8"));
    const previewStats = await stat(previewPath);

    expect(manifestContent.artifactId).toBe(bundle.artifactId);
    expect(dnaContent.id).toBe(bundle.shapeDNA.id);
    expect(previewStats.size).toBeGreaterThan(0);
    expect(result.manifest.outputs.modelPath).toBeNull();
  });

  it("persists an explicit preview asset instead of the placeholder", async () => {
    const bundle = generateArtifactBundle({
      brief: "Custom preview asset",
      semanticState: "GOAL_ACHIEVED",
      renderProfile: "HIGH",
    });
    const rootDir = await mkdtemp(join(tmpdir(), "arc-artifact-generator-"));
    tempDirs.push(rootDir);
    const customPreview = Buffer.from([
      0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x41, 0x55, 0x52, 0x4f, 0x52, 0x41,
    ]);

    await persistArtifactBundle(bundle, {
      rootDir,
      previewPngBytes: customPreview,
    });

    const previewPath = resolve(rootDir, bundle.outputs.previewPath);
    const previewContent = await readFile(previewPath);

    expect(Buffer.compare(previewContent, customPreview)).toBe(0);
  });

  it("imports an optional model.glb into the persisted bundle contract", async () => {
    const bundle = generateArtifactBundle({
      brief: "Optional glb import",
      semanticState: "GROWTH_ACCELERATING",
      renderProfile: "BALANCED",
    });
    const rootDir = await mkdtemp(join(tmpdir(), "arc-artifact-generator-"));
    tempDirs.push(rootDir);
    const modelSourcePath = resolve(rootDir, "source.model.glb");
    const modelBytes = Buffer.from("glTF-AURORA", "utf-8");

    await writeFile(modelSourcePath, modelBytes);

    const result = await persistArtifactBundle(bundle, {
      rootDir,
      modelGlbSourcePath: modelSourcePath,
    });

    expect(result.manifest.outputs.modelPath).toMatch(/model\.glb$/);
    expect(result.writtenFiles).toHaveLength(7);

    const modelPath = resolve(rootDir, result.manifest.outputs.modelPath!);
    const persistedManifestPath = resolve(rootDir, bundle.outputs.manifestPath);
    const persistedModelBytes = await readFile(modelPath);
    const persistedManifest = JSON.parse(await readFile(persistedManifestPath, "utf-8"));

    expect(Buffer.compare(persistedModelBytes, modelBytes)).toBe(0);
    expect(persistedManifest.outputs.modelPath).toBe(result.manifest.outputs.modelPath);
  });

  it("rejects a bundle with qa score mismatch", () => {
    const bundle = generateArtifactBundle({
      brief: "QA mismatch contract",
      semanticState: "ALERT_ACTIVE",
      renderProfile: "BALANCED",
    });

    const invalidBundle = {
      ...bundle,
      qaReport: {
        ...bundle.qaReport,
        score: bundle.qaReport.score - 1,
      },
    };

    expect(validateArtifactBundle(invalidBundle).status).toBe("rejected");
    expect(() => ArtifactManifestSchema.parse(invalidBundle)).not.toThrow();
  });

  it("rejects a bundle missing a required output path during persistence", async () => {
    const bundle = generateArtifactBundle({
      brief: "Missing preview path",
      semanticState: "STABLE_OPERATION",
      renderProfile: "LOW",
    });
    const rootDir = await mkdtemp(join(tmpdir(), "arc-artifact-generator-"));
    tempDirs.push(rootDir);

    const invalidBundle = {
      ...bundle,
      outputs: {
        ...bundle.outputs,
        previewPath: "",
      },
    };

    await expect(persistArtifactBundle(invalidBundle, { rootDir })).rejects.toBeInstanceOf(
      ArtifactBundleValidationError,
    );
  });

  it("rejects conflicting binary asset sources during persistence", async () => {
    const bundle = generateArtifactBundle({
      brief: "Conflicting preview sources",
      semanticState: "STABLE_OPERATION",
      renderProfile: "LOW",
    });
    const rootDir = await mkdtemp(join(tmpdir(), "arc-artifact-generator-"));
    tempDirs.push(rootDir);
    const previewSourcePath = resolve(rootDir, "preview.png");

    await writeFile(previewSourcePath, Buffer.from("preview", "utf-8"));

    await expect(
      persistArtifactBundle(bundle, {
        rootDir,
        previewPngBytes: Buffer.from("inline-preview", "utf-8"),
        previewPngSourcePath: previewSourcePath,
      }),
    ).rejects.toThrow("binary asset cannot use inline bytes and source path at the same time");
  });

  it("rejects a bundle with a critical issue", () => {
    const bundle = generateArtifactBundle({
      brief: "Critical semantic drift",
      semanticState: "BLOCKED_FLOW",
      renderProfile: "BALANCED",
    });

    const invalidBundle = {
      ...bundle,
      qaReport: {
        ...bundle.qaReport,
        accepted: false,
        score: 6.8,
        issues: ["critical: semantic incoherence detected"],
      },
    };

    const validation = validateArtifactBundle(invalidBundle);
    expect(validation.status).toBe("rejected");
    expect(validation.reasons).toContain("qa report contains a critical issue");
  });
});
