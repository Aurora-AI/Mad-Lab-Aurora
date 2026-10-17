import { describe, expect, it } from "vitest";

import { ArcTelemetryStore, createArcTelemetryStore } from "./index";

describe("ArcTelemetryStore", () => {
  it("tracks counters, distributions and average generation time", () => {
    const store = new ArcTelemetryStore();

    store.record({
      kind: "cache_hit",
      semanticState: "STABLE_OPERATION",
      renderProfile: "BALANCED",
    });
    store.record({
      kind: "cache_miss",
      semanticState: "PIPELINE_AT_RISK",
      renderProfile: "HIGH",
    });
    store.record({
      kind: "fallback",
      semanticState: "ALERT_ACTIVE",
      renderProfile: "DEGRADED",
    });
    store.record({
      kind: "artifact_generated",
      semanticState: "GOAL_ACHIEVED",
      renderProfile: "HIGH",
    });
    store.record({
      kind: "generation",
      semanticState: "GOAL_ACHIEVED",
      renderProfile: "HIGH",
      durationMs: 100,
    });
    store.record({
      kind: "generation",
      semanticState: "GOAL_ACHIEVED",
      renderProfile: "HIGH",
      durationMs: 50,
    });

    const snapshot = store.getSnapshot();

    expect(snapshot.totalRequests).toBe(6);
    expect(snapshot.cacheHits).toBe(1);
    expect(snapshot.cacheMisses).toBe(1);
    expect(snapshot.fallbacks).toBe(1);
    expect(snapshot.artifactsGenerated).toBe(1);
    expect(snapshot.errors).toBe(0);
    expect(snapshot.averageGenerationMs).toBe(75);
    expect(snapshot.bySemanticState.STABLE_OPERATION).toBe(1);
    expect(snapshot.bySemanticState.PIPELINE_AT_RISK).toBe(1);
    expect(snapshot.bySemanticState.ALERT_ACTIVE).toBe(1);
    expect(snapshot.bySemanticState.GOAL_ACHIEVED).toBe(3);
    expect(snapshot.byRenderProfile.BALANCED).toBe(1);
    expect(snapshot.byRenderProfile.DEGRADED).toBe(1);
    expect(snapshot.byRenderProfile.HIGH).toBe(4);
  });

  it("records lastError and counts errors", () => {
    const store = createArcTelemetryStore();

    store.record({
      kind: "error",
      semanticState: "BLOCKED_FLOW",
      renderProfile: "LOW",
      message: "artifact_generation_failed",
    });
    store.record({
      kind: "error",
      semanticState: "UNDER_PERFORMANCE",
      renderProfile: "LOW",
    });

    const snapshot = store.getSnapshot();

    expect(snapshot.totalRequests).toBe(2);
    expect(snapshot.errors).toBe(2);
    expect(snapshot.lastError).toBe("unknown_error");
    expect(snapshot.bySemanticState.BLOCKED_FLOW).toBe(1);
    expect(snapshot.bySemanticState.UNDER_PERFORMANCE).toBe(1);
    expect(snapshot.byRenderProfile.LOW).toBe(2);
  });

  it("returns defensive copies from getSnapshot", () => {
    const store = createArcTelemetryStore();

    store.record({
      kind: "cache_hit",
      semanticState: "NEUTRAL_OBSERVING",
      renderProfile: "LOW",
    });

    const snapshot = store.getSnapshot();
    snapshot.bySemanticState.NEUTRAL_OBSERVING = 999;
    snapshot.byRenderProfile.LOW = 999;

    const nextSnapshot = store.getSnapshot();

    expect(nextSnapshot.bySemanticState.NEUTRAL_OBSERVING).toBe(1);
    expect(nextSnapshot.byRenderProfile.LOW).toBe(1);
  });

  it("resets counters, averages and last error", () => {
    const store = createArcTelemetryStore();

    store.record({
      kind: "generation",
      semanticState: "GROWTH_ACCELERATING",
      renderProfile: "HIGH",
      durationMs: 30,
    });
    store.record({
      kind: "error",
      semanticState: "GROWTH_ACCELERATING",
      renderProfile: "HIGH",
      message: "transient_failure",
    });

    store.reset();

    expect(store.getSnapshot()).toEqual({
      totalRequests: 0,
      cacheHits: 0,
      cacheMisses: 0,
      fallbacks: 0,
      artifactsGenerated: 0,
      errors: 0,
      averageGenerationMs: 0,
      bySemanticState: {
        NEUTRAL_OBSERVING: 0,
        STABLE_OPERATION: 0,
        PIPELINE_AT_RISK: 0,
        ALERT_ACTIVE: 0,
        GOAL_ACHIEVED: 0,
        UNDER_PERFORMANCE: 0,
        GROWTH_ACCELERATING: 0,
        BLOCKED_FLOW: 0,
      },
      byRenderProfile: {
        HIGH: 0,
        BALANCED: 0,
        LOW: 0,
        DEGRADED: 0,
      },
      lastError: null,
    });
  });
});
