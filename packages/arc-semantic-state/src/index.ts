import {
  type OperationalState,
  OperationalStateSchema,
  type RenderProfile,
  type SemanticState,
} from "@aurora/arc-schema";

export const SEMANTIC_STATE_TTLS: Record<SemanticState, number> = {
  NEUTRAL_OBSERVING: 900,
  STABLE_OPERATION: 600,
  PIPELINE_AT_RISK: 120,
  ALERT_ACTIVE: 30,
  GOAL_ACHIEVED: 900,
  UNDER_PERFORMANCE: 180,
  GROWTH_ACCELERATING: 300,
  BLOCKED_FLOW: 45,
};

export const DEFAULT_RENDER_PROFILE: RenderProfile = "BALANCED";

export function deriveSemanticState(input: OperationalState): SemanticState {
  const state = OperationalStateSchema.parse(input);

  const isNeutral =
    state.activeAlerts === 0 &&
    state.exceptionCount === 0 &&
    state.humanReviewRequiredCount === 0 &&
    state.queueReadyCount === 0 &&
    state.followUpCount === 0 &&
    state.weightedForecast === 0;

  if (isNeutral) return "NEUTRAL_OBSERVING";
  if (state.goalProgress >= 1) return "GOAL_ACHIEVED";
  if (state.activeAlerts >= 4 || state.humanReviewRequiredCount >= 4) return "ALERT_ACTIVE";
  if (state.pipelineHealth <= 0.25 || state.avgSafetyScore < 35) return "BLOCKED_FLOW";
  if (state.pipelineHealth < 0.5 || state.exceptionCount > 0 || state.humanReviewRequiredCount > 1) {
    return "PIPELINE_AT_RISK";
  }
  if (state.goalProgress < 0.35 && state.followUpCount >= 4) return "UNDER_PERFORMANCE";
  if (state.goalProgress >= 0.78 && state.pipelineHealth >= 0.72 && state.humanReviewRequiredCount === 0) {
    return "GROWTH_ACCELERATING";
  }
  return "STABLE_OPERATION";
}

export function getSemanticStateTtl(state: SemanticState): number {
  return SEMANTIC_STATE_TTLS[state];
}

export function getFallbackSemanticState(): SemanticState {
  return "NEUTRAL_OBSERVING";
}
