import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { ArtifactManifestSchema, type ArtifactManifest } from "@aurora/arc-schema";
import { ArtifactBundleValidationError, validateArtifactBundle } from "./index";

const TRANSPARENT_PNG_BASE64 =
  "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4////fwAJ+wP9KobjigAAAABJRU5ErkJggg==";

export interface ArtifactBundleWriteResult {
  manifest: ArtifactManifest;
  writtenFiles: string[];
}

export interface PersistArtifactBundleOptions {
  rootDir?: string;
  previewPngBytes?: Uint8Array;
  previewPngSourcePath?: string;
  modelGlbBytes?: Uint8Array;
  modelGlbSourcePath?: string;
}

function jsonBuffer(value: unknown) {
  return Buffer.from(`${JSON.stringify(value, null, 2)}\n`, "utf-8");
}

async function resolveBinaryAsset(options: {
  inlineBytes?: Uint8Array;
  sourcePath?: string;
  fallbackBytes?: Uint8Array;
}) {
  if (options.inlineBytes && options.sourcePath) {
    throw new Error("binary asset cannot use inline bytes and source path at the same time");
  }

  if (options.inlineBytes) {
    return Buffer.from(options.inlineBytes);
  }

  if (options.sourcePath) {
    return readFile(resolve(options.sourcePath));
  }

  return Buffer.from(options.fallbackBytes ?? new Uint8Array());
}

function withOptionalModelPath(
  manifest: ArtifactManifest,
  hasModelAsset: boolean,
): ArtifactManifest {
  if (!hasModelAsset) {
    return manifest;
  }

  const artifactDir = dirname(manifest.outputs.manifestPath).replace(/\\/g, "/");
  return ArtifactManifestSchema.parse({
    ...manifest,
    outputs: {
      ...manifest.outputs,
      modelPath: `${artifactDir}/model.glb`,
    },
  });
}

async function buildArtifactFiles(
  manifest: ArtifactManifest,
  options: PersistArtifactBundleOptions,
) {
  const previewContent = await resolveBinaryAsset({
    inlineBytes: options.previewPngBytes,
    sourcePath: options.previewPngSourcePath,
    fallbackBytes: Buffer.from(TRANSPARENT_PNG_BASE64, "base64"),
  });
  const modelContent =
    manifest.outputs.modelPath === null
      ? null
      : await resolveBinaryAsset({
          inlineBytes: options.modelGlbBytes,
          sourcePath: options.modelGlbSourcePath,
        });

  return [
    {
      relativePath: manifest.outputs.manifestPath,
      content: jsonBuffer(manifest),
    },
    {
      relativePath: manifest.outputs.dnaPath,
      content: jsonBuffer(manifest.shapeDNA),
    },
    {
      relativePath: manifest.outputs.materialRecipePath,
      content: jsonBuffer(manifest.shapeDNA.material),
    },
    {
      relativePath: manifest.outputs.environmentRecipePath,
      content: jsonBuffer(manifest.shapeDNA.environment),
    },
    {
      relativePath: manifest.outputs.qaReportPath,
      content: jsonBuffer(manifest.qaReport),
    },
    {
      relativePath: manifest.outputs.previewPath,
      content: previewContent,
    },
    ...(manifest.outputs.modelPath && modelContent
      ? [
          {
            relativePath: manifest.outputs.modelPath,
            content: modelContent,
          },
        ]
      : []),
  ];
}

export async function persistArtifactBundle(
  manifest: ArtifactManifest,
  options: PersistArtifactBundleOptions = {},
): Promise<ArtifactBundleWriteResult> {
  const parsed = ArtifactManifestSchema.parse(manifest);
  const persistedManifest = withOptionalModelPath(
    parsed,
    Boolean(options.modelGlbBytes || options.modelGlbSourcePath),
  );
  const validation = validateArtifactBundle(persistedManifest);
  if (validation.status === "rejected") {
    throw new ArtifactBundleValidationError(persistedManifest, validation);
  }
  const rootDir = resolve(options.rootDir ?? process.cwd());
  const files = await buildArtifactFiles(persistedManifest, options);
  const writtenFiles: string[] = [];

  for (const file of files) {
    const absolutePath = resolve(rootDir, file.relativePath);
    const parentDir = dirname(absolutePath);
    await mkdir(parentDir, { recursive: true });
    await writeFile(absolutePath, file.content);
    writtenFiles.push(absolutePath);
  }

  return {
    manifest: persistedManifest,
    writtenFiles,
  };
}
