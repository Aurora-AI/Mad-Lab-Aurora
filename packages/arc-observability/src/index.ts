import type { RenderProfile, SemanticState } from "@aurora/arc-schema";

export interface ArcTelemetryEvent {
  kind:
    | "generation"
    | "cache_hit"
    | "cache_miss"
    | "fallback"
    | "render_profile"
    | "artifact_generated"
    | "error";
  semanticState: SemanticState;
  renderProfile: RenderProfile;
  durationMs?: number;
  message?: string;
}

export interface ArcTelemetrySnapshot {
  totalRequests: number;
  cacheHits: number;
  cacheMisses: number;
  fallbacks: number;
  artifactsGenerated: number;
  errors: number;
  averageGenerationMs: number;
  bySemanticState: Record<SemanticState, number>;
  byRenderProfile: Record<RenderProfile, number>;
  lastError: string | null;
}

function buildSemanticStateCounter(): Record<SemanticState, number> {
  return {
    NEUTRAL_OBSERVING: 0,
    STABLE_OPERATION: 0,
    PIPELINE_AT_RISK: 0,
    ALERT_ACTIVE: 0,
    GOAL_ACHIEVED: 0,
    UNDER_PERFORMANCE: 0,
    GROWTH_ACCELERATING: 0,
    BLOCKED_FLOW: 0,
  };
}

function buildRenderProfileCounter(): Record<RenderProfile, number> {
  return {
    HIGH: 0,
    BALANCED: 0,
    LOW: 0,
    DEGRADED: 0,
  };
}

export class ArcTelemetryStore {
  private totalGenerationMs = 0;
  private generationCount = 0;
  private snapshot: ArcTelemetrySnapshot = {
    totalRequests: 0,
    cacheHits: 0,
    cacheMisses: 0,
    fallbacks: 0,
    artifactsGenerated: 0,
    errors: 0,
    averageGenerationMs: 0,
    bySemanticState: buildSemanticStateCounter(),
    byRenderProfile: buildRenderProfileCounter(),
    lastError: null,
  };

  record(event: ArcTelemetryEvent) {
    this.snapshot.totalRequests += 1;
    this.snapshot.bySemanticState[event.semanticState] += 1;
    this.snapshot.byRenderProfile[event.renderProfile] += 1;

    if (event.kind === "cache_hit") this.snapshot.cacheHits += 1;
    if (event.kind === "cache_miss") this.snapshot.cacheMisses += 1;
    if (event.kind === "fallback") this.snapshot.fallbacks += 1;
    if (event.kind === "artifact_generated") this.snapshot.artifactsGenerated += 1;
    if (event.kind === "error") {
      this.snapshot.errors += 1;
      this.snapshot.lastError = event.message ?? "unknown_error";
    }
    if (event.kind === "generation" && typeof event.durationMs === "number") {
      this.generationCount += 1;
      this.totalGenerationMs += event.durationMs;
      this.snapshot.averageGenerationMs = this.totalGenerationMs / this.generationCount;
    }
  }

  getSnapshot(): ArcTelemetrySnapshot {
    return {
      ...this.snapshot,
      bySemanticState: { ...this.snapshot.bySemanticState },
      byRenderProfile: { ...this.snapshot.byRenderProfile },
    };
  }

  reset() {
    this.totalGenerationMs = 0;
    this.generationCount = 0;
    this.snapshot = {
      totalRequests: 0,
      cacheHits: 0,
      cacheMisses: 0,
      fallbacks: 0,
      artifactsGenerated: 0,
      errors: 0,
      averageGenerationMs: 0,
      bySemanticState: buildSemanticStateCounter(),
      byRenderProfile: buildRenderProfileCounter(),
      lastError: null,
    };
  }
}

export function createArcTelemetryStore() {
  return new ArcTelemetryStore();
}
