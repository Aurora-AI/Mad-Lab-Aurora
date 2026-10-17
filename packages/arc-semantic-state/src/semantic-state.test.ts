import { describe, expect, it } from "vitest";
import type { OperationalState, SemanticState } from "@aurora/arc-schema";
import {
  deriveSemanticState,
  getFallbackSemanticState,
  getSemanticStateTtl,
  SEMANTIC_STATE_TTLS,
} from "./index";

function makeOperationalState(overrides: Partial<OperationalState> = {}): OperationalState {
  return {
    source: "chronos-test",
    measuredAt: "2026-03-19T00:00:00.000Z",
    pipelineHealth: 0.82,
    goalProgress: 0.56,
    activeAlerts: 0,
    exceptionCount: 0,
    humanReviewRequiredCount: 0,
    queueReadyCount: 2,
    followUpCount: 1,
    avgSafetyScore: 78,
    weightedForecast: 120000,
    notes: [],
    ...overrides,
  };
}

describe("arc-semantic-state", () => {
  it("derives NEUTRAL_OBSERVING when the system is effectively idle", () => {
    const result = deriveSemanticState(
      makeOperationalState({
        queueReadyCount: 0,
        weightedForecast: 0,
      }),
    );

    expect(result).toBe("NEUTRAL_OBSERVING");
  });

  it("prioritizes GOAL_ACHIEVED before alert or blocked heuristics", () => {
    const result = deriveSemanticState(
      makeOperationalState({
        goalProgress: 1,
        activeAlerts: 8,
        pipelineHealth: 0.1,
        humanReviewRequiredCount: 6,
      }),
    );

    expect(result).toBe("GOAL_ACHIEVED");
  });

  it("derives ALERT_ACTIVE when alert or human-review pressure is high", () => {
    const result = deriveSemanticState(
      makeOperationalState({
        activeAlerts: 4,
        pipelineHealth: 0.2,
      }),
    );

    expect(result).toBe("ALERT_ACTIVE");
  });

  it("derives BLOCKED_FLOW when pipeline health or safety is critically low", () => {
    const lowPipeline = deriveSemanticState(
      makeOperationalState({
        pipelineHealth: 0.2,
      }),
    );
    const lowSafety = deriveSemanticState(
      makeOperationalState({
        avgSafetyScore: 20,
      }),
    );

    expect(lowPipeline).toBe("BLOCKED_FLOW");
    expect(lowSafety).toBe("BLOCKED_FLOW");
  });

  it("derives PIPELINE_AT_RISK when there are exceptions or elevated review pressure", () => {
    const result = deriveSemanticState(
      makeOperationalState({
        pipelineHealth: 0.48,
        exceptionCount: 1,
      }),
    );

    expect(result).toBe("PIPELINE_AT_RISK");
  });

  it("derives UNDER_PERFORMANCE when progress stays low under follow-up load", () => {
    const result = deriveSemanticState(
      makeOperationalState({
        goalProgress: 0.2,
        followUpCount: 5,
        pipelineHealth: 0.7,
      }),
    );

    expect(result).toBe("UNDER_PERFORMANCE");
  });

  it("derives GROWTH_ACCELERATING when progress and pipeline are strong without human gate pressure", () => {
    const result = deriveSemanticState(
      makeOperationalState({
        goalProgress: 0.82,
        pipelineHealth: 0.9,
        humanReviewRequiredCount: 0,
      }),
    );

    expect(result).toBe("GROWTH_ACCELERATING");
  });

  it("falls back to STABLE_OPERATION when no stronger rule applies", () => {
    const result = deriveSemanticState(
      makeOperationalState({
        goalProgress: 0.6,
        pipelineHealth: 0.74,
        followUpCount: 2,
      }),
    );

    expect(result).toBe("STABLE_OPERATION");
  });

  it("exposes ttl for every semantic state and keeps NEUTRAL_OBSERVING as fallback", () => {
    const states = Object.keys(SEMANTIC_STATE_TTLS) as SemanticState[];

    for (const state of states) {
      expect(getSemanticStateTtl(state)).toBeGreaterThan(0);
    }

    expect(getFallbackSemanticState()).toBe("NEUTRAL_OBSERVING");
  });
});
