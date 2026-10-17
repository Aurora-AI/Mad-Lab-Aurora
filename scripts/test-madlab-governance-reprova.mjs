#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');
const gateScript = path.join(__dirname, 'check-madlab-governance.mjs');

const filesToCopy = [
  'docs/AGENTS/DOCTRINE.md',
  'AGENTS.md',
  'GEMINI.md',
  'CLAUDE.md',
  'docs/Vault/Decisions/DEC-MADLAB-AGENTIC-MESH-001.md',
  'docs/Vault/Decisions/DEC-MADLAB-AGENTIC-PIVOT-002.md',
  '.aurora/domain-policy.json',
  '.aurora/toolbelt-consumer.json',
  'project-manifest.json',
  '.agents/rules/designmanualposthero.md',
  '.aurora/skills/agentic-web-architect/SKILL.md',
  '.aurora/skills/b2b-ai-outbound-architect/SKILL.md',
  '.aurora/skills/qa-review/SKILL.md',
  '.aurora/skills/ceo-web/SKILL.md',
  '.aurora/skills/ceo-copy/SKILL.md',
  '.aurora/skills/ceo-design/SKILL.md',
  '.aurora/skills/ceo-effects/SKILL.md',
  '.aurora/skills/ceo-3d/SKILL.md',
  '.aurora/skills/ceo-art-direction/SKILL.md',
  '.aurora/skills/cinematic-grammar/SKILL.md',
  '.aurora/skills/taste-design/SKILL.md',
  '.aurora/skills/design-md/SKILL.md',
  '.aurora/skills/ceo-critique-theater/SKILL.md',
  'docs/brand/MANUAL_DA_AGENCIA.md',
  'docs/brand/mad-lab-aurora-dna-v2.1.0.md'
];

function createSandbox() {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'madlab-reprova-'));
  for (const rel of filesToCopy) {
    const src = path.join(repoRoot, rel);
    const dst = path.join(tmpDir, rel);
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
  }
  return tmpDir;
}

function runGate(targetRoot) {
  return spawnSync(process.execPath, [gateScript, '--root', targetRoot], {
    encoding: 'utf8'
  });
}

const scenarios = [
  {
    name: 'S1_DOCTRINE_DRIFT_IN_GEMINI_MD',
    expectedCode: 'DOCTRINE_DRIFT',
    sabotage(dir) {
      const p = path.join(dir, 'GEMINI.md');
      const content = fs.readFileSync(p, 'utf8').replace('document.modelContext', 'DRIFTED_TOKEN');
      fs.writeFileSync(p, content, 'utf8');
    }
  },
  {
    name: 'S2_DEPRECATED_SKILL_REACTIVATED',
    expectedCode: 'DEPRECATION_MISSING',
    sabotage(dir) {
      const p = path.join(dir, '.aurora/skills/ceo-design/SKILL.md');
      const content = fs
        .readFileSync(p, 'utf8')
        .replace('deprecated: true', 'deprecated: false')
        .replace('status: deprecated', 'status: active');
      fs.writeFileSync(p, content, 'utf8');
    }
  },
  {
    name: 'S3_APPEND_ONLY_VIOLATION_FILE_DELETED',
    expectedCode: 'APPEND_ONLY_VIOLATION',
    sabotage(dir) {
      fs.unlinkSync(path.join(dir, 'docs/brand/MANUAL_DA_AGENCIA.md'));
    }
  },
  {
    name: 'S4_DEPRECATED_NAVIGATOR_MODEL_CONTEXT_USED',
    expectedCode: 'DEPRECATED_WEBMCP_API',
    sabotage(dir) {
      const p = path.join(dir, '.aurora/skills/agentic-web-architect/SKILL.md');
      fs.appendFileSync(p, '\n// Sabotage: navigator.modelContext.registerTool({})\n', 'utf8');
    }
  },
  {
    name: 'S5_LEGACY_POST_HERO_DARK_RULE_RESTORED',
    expectedCode: 'LEGACY_RULE_ACTIVE',
    sabotage(dir) {
      const p = path.join(dir, '.agents/rules/designmanualposthero.md');
      fs.appendFileSync(p, '\n# AURORA DESIGN MANUAL - POST-HERO v2.0\nHero termina CLARO -> Seção 1: CLARO\n', 'utf8');
    }
  },
  {
    name: 'S6_DOMAIN_POLICY_CONSTITUTION_REVERTED',
    expectedCode: 'DOMAIN_POLICY_INVALID',
    sabotage(dir) {
      const p = path.join(dir, '.aurora/domain-policy.json');
      const dp = JSON.parse(fs.readFileSync(p, 'utf8'));
      dp.constitution_ref = 'docs/brand/MANUAL_DA_AGENCIA.md';
      fs.writeFileSync(p, JSON.stringify(dp, null, 2), 'utf8');
    }
  }
];

let failed = 0;

// Step 0: Verify clean repository passes (EXIT=0)
const cleanRes = runGate(repoRoot);
if (cleanRes.status !== 0) {
  console.error('[reprova] FAIL: Clean repository did not pass governance gate!');
  console.error(cleanRes.stderr || cleanRes.stdout);
  process.exit(1);
}
console.log('[reprova] PASS: Baseline clean repository exited with EXIT=0');

// Step 1..N: Verify every adversarial sabotage scenario forces EXIT=1 with the expected error code
for (const scenario of scenarios) {
  const sandbox = createSandbox();
  try {
    scenario.sabotage(sandbox);
    const res = runGate(sandbox);
    const combinedOutput = `${res.stdout}\n${res.stderr}`;
    if (res.status !== 1 || !combinedOutput.includes(scenario.expectedCode)) {
      console.error(
        `[reprova] FAIL: Scenario ${scenario.name} expected EXIT=1 with [${scenario.expectedCode}], got EXIT=${res.status}`
      );
      console.error(combinedOutput);
      failed += 1;
    } else {
      console.log(
        `[reprova] PASS: Scenario ${scenario.name} -> forced EXIT=1 with [${scenario.expectedCode}]`
      );
    }
  } finally {
    fs.rmSync(sandbox, { recursive: true, force: true });
  }
}

if (failed > 0) {
  console.error(`[reprova] FAILED: ${failed}/${scenarios.length} sabotage scenarios did not trigger EXIT=1`);
  process.exit(1);
}

console.log(`[reprova] ALL ${scenarios.length} ADVERSARIAL SABOTAGE SCENARIOS PASSED (forced EXIT=1 as expected).`);
