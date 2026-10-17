import { generateArtifactBundle, validateArtifactBundle } from "@aurora/arc-artifact-generator";
import { ArcTelemetryStore, createArcTelemetryStore } from "@aurora/arc-observability";
import {
  ArtifactManifestSchema,
  type ArtifactManifest,
  type OperationalState,
  type RenderProfile,
  type SemanticState,
  type ShapeDNA,
} from "@aurora/arc-schema";
import {
  DEFAULT_RENDER_PROFILE,
  deriveSemanticState,
  getFallbackSemanticState,
  getSemanticStateTtl,
} from "@aurora/arc-semantic-state";

type ArtifactBundleGenerator = (input: {
  brief: string;
  semanticState: SemanticState;
  renderProfile?: RenderProfile;
  intent?: string;
}) => ArtifactManifest;

interface ResolveOptions {
  brief?: string;
  renderProfile?: RenderProfile;
  sourceKey?: string;
}

interface CacheEntry {
  expiresAt: number;
  resolution: ArcResolution;
}

export interface ArcResolution {
  semanticState: SemanticState;
  renderProfile: RenderProfile;
  sourceKey: string;
  cacheKey: string;
  artifact: ArtifactManifest;
  shapeDNA: ShapeDNA;
  cacheStatus: "hit" | "miss" | "fallback";
  fallbackUsed: boolean;
  generatedAt: string;
}

export interface ArcOrchestratorDiagnostics {
  cacheKeys: string[];
  latestKnownGoodKeys: string[];
  telemetry: ReturnType<ArcTelemetryStore["getSnapshot"]>;
}

export interface ArcOrchestratorDependencies {
  telemetry?: ArcTelemetryStore;
  artifactGenerator?: ArtifactBundleGenerator;
  now?: () => number;
  performanceNow?: () => number;
}

export interface ArcInvalidateFilters {
  semanticState?: SemanticState;
  sourceKey?: string;
  dropLatestKnownGood?: boolean;
}

const GLOBAL_SOURCE_KEY = "global";

function normalizeSourceKey(sourceKey?: string) {
  return sourceKey?.trim() || GLOBAL_SOURCE_KEY;
}

function buildCacheKey(
  semanticState: SemanticState,
  renderProfile: RenderProfile,
  sourceKey?: string,
) {
  return `${normalizeSourceKey(sourceKey)}:${semanticState}:${renderProfile}`;
}

function matchesFilters(
  resolution: ArcResolution,
  filters: ArcInvalidateFilters,
) {
  if (filters.semanticState && resolution.semanticState !== filters.semanticState) {
    return false;
  }
  if (filters.sourceKey && resolution.sourceKey !== normalizeSourceKey(filters.sourceKey)) {
    return false;
  }
  return true;
}

function assertOrchestratorArtifactValid(artifact: ArtifactManifest) {
  const parsed = ArtifactManifestSchema.parse(artifact);
  const validation = validateArtifactBundle(parsed);

  if (validation.status === "rejected") {
    throw new Error(
      `invalid_arc_artifact_bundle:${parsed.artifactId}:${validation.reasons.join("|") || "unknown"}`,
    );
  }

  return parsed;
}

export class ArcOrchestrator {
  private readonly cache = new Map<string, CacheEntry>();
  private readonly latestByKey = new Map<string, ArcResolution>();
  private readonly telemetry: ArcTelemetryStore;
  private readonly artifactGenerator: ArtifactBundleGenerator;
  private readonly now: () => number;
  private readonly performanceNow: () => number;

  constructor(dependencies: ArcOrchestratorDependencies = {}) {
    this.telemetry = dependencies.telemetry ?? createArcTelemetryStore();
    this.artifactGenerator = dependencies.artifactGenerator ?? generateArtifactBundle;
    this.now = dependencies.now ?? (() => Date.now());
    this.performanceNow =
      dependencies.performanceNow ??
      (() =>
        typeof globalThis.performance?.now === "function"
          ? globalThis.performance.now()
          : Date.now());
  }

  resolveFromOperationalState(
    input: OperationalState,
    options?: Omit<ResolveOptions, "sourceKey">,
  ) {
    const semanticState = deriveSemanticState(input);
    return this.resolveFromSemanticState(semanticState, {
      brief: options?.brief ?? `Operational state from ${input.source}`,
      renderProfile: options?.renderProfile,
      sourceKey: input.source,
    });
  }

  resolveFromSemanticState(
    semanticState: SemanticState,
    options?: ResolveOptions,
  ): ArcResolution {
    const renderProfile = options?.renderProfile ?? DEFAULT_RENDER_PROFILE;
    const sourceKey = normalizeSourceKey(options?.sourceKey);
    const cacheKey = buildCacheKey(semanticState, renderProfile, sourceKey);
    const now = this.now();
    const cached = this.cache.get(cacheKey);

    if (cached && cached.expiresAt > now) {
      this.telemetry.record({ kind: "cache_hit", semanticState, renderProfile });
      return {
        ...cached.resolution,
        cacheStatus: "hit",
        fallbackUsed: false,
      };
    }

    this.telemetry.record({ kind: "cache_miss", semanticState, renderProfile });
    const startedAt = this.performanceNow();

    try {
      const artifact = assertOrchestratorArtifactValid(
        this.artifactGenerator({
          brief: options?.brief ?? `ARC bundle for ${semanticState}`,
          semanticState,
          renderProfile,
        }),
      );
      const resolution: ArcResolution = {
        semanticState,
        renderProfile,
        sourceKey,
        cacheKey,
        artifact,
        shapeDNA: artifact.shapeDNA,
        cacheStatus: "miss",
        fallbackUsed: false,
        generatedAt: artifact.generatedAt,
      };
      const ttl = getSemanticStateTtl(semanticState) * 1000;
      this.cache.set(cacheKey, { expiresAt: now + ttl, resolution });
      this.latestByKey.set(cacheKey, resolution);
      this.telemetry.record({ kind: "artifact_generated", semanticState, renderProfile });
      this.telemetry.record({
        kind: "generation",
        semanticState,
        renderProfile,
        durationMs: this.performanceNow() - startedAt,
      });
      return resolution;
    } catch (error) {
      const fallback = this.latestByKey.get(cacheKey);
      this.telemetry.record({
        kind: "error",
        semanticState,
        renderProfile,
        message: error instanceof Error ? error.message : String(error),
      });
      if (fallback) {
        this.telemetry.record({ kind: "fallback", semanticState, renderProfile });
        return {
          ...fallback,
          cacheStatus: "fallback",
          fallbackUsed: true,
        };
      }

      const fallbackState = getFallbackSemanticState();
      const fallbackCacheKey = buildCacheKey(fallbackState, renderProfile, sourceKey);
      const artifact = assertOrchestratorArtifactValid(
        this.artifactGenerator({
          brief: options?.brief ?? `Fallback ARC bundle for ${fallbackState}`,
          semanticState: fallbackState,
          renderProfile,
        }),
      );
      const resolution: ArcResolution = {
        semanticState: fallbackState,
        renderProfile,
        sourceKey,
        cacheKey: fallbackCacheKey,
        artifact,
        shapeDNA: artifact.shapeDNA,
        cacheStatus: "fallback",
        fallbackUsed: true,
        generatedAt: artifact.generatedAt,
      };
      this.latestByKey.set(fallbackCacheKey, resolution);
      this.telemetry.record({ kind: "fallback", semanticState: fallbackState, renderProfile });
      return resolution;
    }
  }

  invalidate(filters?: SemanticState | ArcInvalidateFilters) {
    if (!filters) {
      this.cache.clear();
      this.latestByKey.clear();
      return;
    }

    const normalizedFilters: ArcInvalidateFilters =
      typeof filters === "string" ? { semanticState: filters } : filters;

    for (const [key, entry] of this.cache.entries()) {
      if (matchesFilters(entry.resolution, normalizedFilters)) {
        this.cache.delete(key);
      }
    }

    if (normalizedFilters.dropLatestKnownGood) {
      for (const [key, resolution] of this.latestByKey.entries()) {
        if (matchesFilters(resolution, normalizedFilters)) {
          this.latestByKey.delete(key);
        }
      }
    }
  }

  getLatestKnownGood(options: {
    semanticState: SemanticState;
    renderProfile?: RenderProfile;
    sourceKey?: string;
  }) {
    const renderProfile = options.renderProfile ?? DEFAULT_RENDER_PROFILE;
    const cacheKey = buildCacheKey(options.semanticState, renderProfile, options.sourceKey);
    return this.latestByKey.get(cacheKey) ?? null;
  }

  getDiagnostics(): ArcOrchestratorDiagnostics {
    return {
      cacheKeys: [...this.cache.keys()],
      latestKnownGoodKeys: [...this.latestByKey.keys()],
      telemetry: this.telemetry.getSnapshot(),
    };
  }

  getTelemetrySnapshot() {
    return this.telemetry.getSnapshot();
  }
}

export function createArcOrchestrator(dependencies?: ArcOrchestratorDependencies) {
  return new ArcOrchestrator(dependencies);
}
