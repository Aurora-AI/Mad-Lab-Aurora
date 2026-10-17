import { describe, expect, it } from "vitest";
import { generateArtifactBundle } from "@aurora/arc-artifact-generator";
import type { RenderProfile, SemanticState } from "@aurora/arc-schema";
import { ArcOrchestrator } from "./index";

function makeGenerator() {
  const calls: Array<{ semanticState: SemanticState; renderProfile: RenderProfile }> = [];
  let fail = false;
  let invalidBundleFor: SemanticState | null = null;

  const generator = (input: {
    brief: string;
    semanticState: SemanticState;
    renderProfile?: RenderProfile;
  }) => {
    if (fail) {
      throw new Error("forced_generation_failure");
    }

    const renderProfile = input.renderProfile ?? "BALANCED";
    calls.push({
      semanticState: input.semanticState,
      renderProfile,
    });

    const bundle = generateArtifactBundle({
      brief: input.brief,
      semanticState: input.semanticState,
      renderProfile,
    });

    if (invalidBundleFor === input.semanticState) {
      return {
        ...bundle,
        outputs: {
          ...bundle.outputs,
          previewPath: "",
        },
      };
    }

    return bundle;
  };

  return {
    calls,
    setFailing(next: boolean) {
      fail = next;
    },
    setInvalidBundleFor(next: SemanticState | null) {
      invalidBundleFor = next;
    },
    generator,
  };
}

describe("arc-orchestrator", () => {
  it("returns miss on first resolve and hit on repeated resolve with the same source", () => {
    const fake = makeGenerator();
    const orchestrator = new ArcOrchestrator({
      artifactGenerator: fake.generator,
      now: () => 10,
      performanceNow: (() => {
        let tick = 0;
        return () => ++tick;
      })(),
    });

    const first = orchestrator.resolveFromSemanticState("STABLE_OPERATION", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });
    const second = orchestrator.resolveFromSemanticState("STABLE_OPERATION", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });

    expect(first.cacheStatus).toBe("miss");
    expect(second.cacheStatus).toBe("hit");
    expect(fake.calls).toHaveLength(1);
    expect(second.cacheKey).toBe(first.cacheKey);
  });

  it("partitions cache by sourceKey and invalidates only the targeted segment", () => {
    const fake = makeGenerator();
    let now = 100;
    const orchestrator = new ArcOrchestrator({
      artifactGenerator: fake.generator,
      now: () => now,
      performanceNow: (() => {
        let tick = 0;
        return () => ++tick;
      })(),
    });

    orchestrator.resolveFromSemanticState("PIPELINE_AT_RISK", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });
    orchestrator.resolveFromSemanticState("PIPELINE_AT_RISK", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-b",
    });

    orchestrator.invalidate({
      semanticState: "PIPELINE_AT_RISK",
      sourceKey: "chronos-a",
    });

    now += 1;

    const afterInvalidateA = orchestrator.resolveFromSemanticState("PIPELINE_AT_RISK", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });
    const stillCachedB = orchestrator.resolveFromSemanticState("PIPELINE_AT_RISK", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-b",
    });

    expect(afterInvalidateA.cacheStatus).toBe("miss");
    expect(stillCachedB.cacheStatus).toBe("hit");
    expect(fake.calls).toHaveLength(3);
  });

  it("expires cache entries after semantic-state TTL and regenerates the bundle", () => {
    const fake = makeGenerator();
    let now = 0;
    const orchestrator = new ArcOrchestrator({
      artifactGenerator: fake.generator,
      now: () => now,
      performanceNow: (() => {
        let tick = 0;
        return () => ++tick;
      })(),
    });

    const first = orchestrator.resolveFromSemanticState("ALERT_ACTIVE", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });

    now = 29_000;
    const beforeExpiry = orchestrator.resolveFromSemanticState("ALERT_ACTIVE", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });

    now = 30_001;
    const afterExpiry = orchestrator.resolveFromSemanticState("ALERT_ACTIVE", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });

    expect(first.cacheStatus).toBe("miss");
    expect(beforeExpiry.cacheStatus).toBe("hit");
    expect(afterExpiry.cacheStatus).toBe("miss");
    expect(fake.calls).toHaveLength(2);
    expect(afterExpiry.cacheKey).toBe(first.cacheKey);
    expect(afterExpiry.artifact.artifactId).not.toBe(first.artifact.artifactId);
  });

  it("can invalidate the latest known good for only one source segment", () => {
    const fake = makeGenerator();
    let now = 50;
    const orchestrator = new ArcOrchestrator({
      artifactGenerator: fake.generator,
      now: () => now,
      performanceNow: (() => {
        let tick = 0;
        return () => ++tick;
      })(),
    });

    orchestrator.resolveFromSemanticState("STABLE_OPERATION", {
      renderProfile: "HIGH",
      sourceKey: "chronos-a",
    });
    orchestrator.resolveFromSemanticState("STABLE_OPERATION", {
      renderProfile: "HIGH",
      sourceKey: "chronos-b",
    });

    orchestrator.invalidate({
      semanticState: "STABLE_OPERATION",
      sourceKey: "chronos-a",
      dropLatestKnownGood: true,
    });

    expect(
      orchestrator.getLatestKnownGood({
        semanticState: "STABLE_OPERATION",
        renderProfile: "HIGH",
        sourceKey: "chronos-a",
      }),
    ).toBeNull();
    expect(
      orchestrator.getLatestKnownGood({
        semanticState: "STABLE_OPERATION",
        renderProfile: "HIGH",
        sourceKey: "chronos-b",
      }),
    ).not.toBeNull();

    now += 1;
    fake.setInvalidBundleFor("STABLE_OPERATION");

    const resolution = orchestrator.resolveFromSemanticState("STABLE_OPERATION", {
      renderProfile: "HIGH",
      sourceKey: "chronos-a",
    });

    expect(resolution.cacheStatus).toBe("fallback");
    expect(resolution.fallbackUsed).toBe(true);
    expect(resolution.semanticState).toBe("NEUTRAL_OBSERVING");
  });

  it("falls back to the latest known good bundle when generation fails after invalidation", () => {
    const fake = makeGenerator();
    let now = 1_000;
    const orchestrator = new ArcOrchestrator({
      artifactGenerator: fake.generator,
      now: () => now,
      performanceNow: (() => {
        let tick = 0;
        return () => ++tick;
      })(),
    });

    const baseline = orchestrator.resolveFromSemanticState("STABLE_OPERATION", {
      renderProfile: "HIGH",
      sourceKey: "chronos-a",
    });

    orchestrator.invalidate({
      semanticState: "STABLE_OPERATION",
      sourceKey: "chronos-a",
    });

    fake.setFailing(true);
    now += 1;

    const fallback = orchestrator.resolveFromSemanticState("STABLE_OPERATION", {
      renderProfile: "HIGH",
      sourceKey: "chronos-a",
    });

    expect(fallback.cacheStatus).toBe("fallback");
    expect(fallback.fallbackUsed).toBe(true);
    expect(fallback.artifact.artifactId).toBe(baseline.artifact.artifactId);
    expect(
      orchestrator.getLatestKnownGood({
        semanticState: "STABLE_OPERATION",
        renderProfile: "HIGH",
        sourceKey: "chronos-a",
      })?.artifact.artifactId,
    ).toBe(baseline.artifact.artifactId);
  });

  it("falls back to the latest known good bundle when a custom generator emits an invalid bundle", () => {
    const fake = makeGenerator();
    let now = 2_000;
    const orchestrator = new ArcOrchestrator({
      artifactGenerator: fake.generator,
      now: () => now,
      performanceNow: (() => {
        let tick = 0;
        return () => ++tick;
      })(),
    });

    const baseline = orchestrator.resolveFromSemanticState("PIPELINE_AT_RISK", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });

    orchestrator.invalidate({
      semanticState: "PIPELINE_AT_RISK",
      sourceKey: "chronos-a",
    });

    fake.setInvalidBundleFor("PIPELINE_AT_RISK");
    now += 1;

    const fallback = orchestrator.resolveFromSemanticState("PIPELINE_AT_RISK", {
      renderProfile: "BALANCED",
      sourceKey: "chronos-a",
    });

    expect(fallback.cacheStatus).toBe("fallback");
    expect(fallback.artifact.artifactId).toBe(baseline.artifact.artifactId);
    expect(
      orchestrator.getLatestKnownGood({
        semanticState: "PIPELINE_AT_RISK",
        renderProfile: "BALANCED",
        sourceKey: "chronos-a",
      })?.artifact.artifactId,
    ).toBe(baseline.artifact.artifactId);
  });

  it("uses the semantic fallback path when the primary bundle is invalid and no latest known good exists", () => {
    const fake = makeGenerator();
    const orchestrator = new ArcOrchestrator({
      artifactGenerator: fake.generator,
      now: () => 3_000,
      performanceNow: (() => {
        let tick = 0;
        return () => ++tick;
      })(),
    });

    fake.setInvalidBundleFor("ALERT_ACTIVE");

    const resolution = orchestrator.resolveFromSemanticState("ALERT_ACTIVE", {
      renderProfile: "HIGH",
      sourceKey: "chronos-a",
    });

    expect(resolution.cacheStatus).toBe("fallback");
    expect(resolution.fallbackUsed).toBe(true);
    expect(resolution.semanticState).not.toBe("ALERT_ACTIVE");
  });
});
