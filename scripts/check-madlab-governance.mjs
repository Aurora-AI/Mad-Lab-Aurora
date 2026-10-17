#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function parseArgs(argv) {
  let root = path.resolve(__dirname, '..');
  for (let i = 2; i < argv.length; i += 1) {
    if (argv[i] === '--root' && argv[i + 1]) {
      root = path.resolve(argv[i + 1]);
      i += 1;
    }
  }
  return { root };
}

const START_MARKER = '<!-- DOCTRINE:START -->';
const END_MARKER = '<!-- DOCTRINE:END -->';

function extractDoctrineBlock(content) {
  const startIdx = content.indexOf(START_MARKER);
  const endIdx = content.indexOf(END_MARKER);
  if (startIdx === -1 || endIdx === -1 || endIdx <= startIdx) {
    return null;
  }
  return content.slice(startIdx, endIdx + END_MARKER.length).replace(/\r\n/g, '\n');
}

function extractFrontmatter(content) {
  const normalized = content.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) {
    return null;
  }
  const endIdx = normalized.indexOf('\n---\n', 4);
  if (endIdx === -1) {
    return null;
  }
  return normalized.slice(4, endIdx);
}

function extractMeshContractJson(content) {
  const normalized = content.replace(/\r\n/g, '\n');
  const match = normalized.match(/##\s+Mesh Contract[\s\S]*?```json\s*\n([\s\S]*?)\n```/);
  if (!match) {
    return null;
  }
  return JSON.parse(match[1]);
}

export function runGovernanceCheck(rootDir) {
  const errors = [];
  const checks = [];

  const resolveRoot = (relPath) => path.join(rootDir, relPath);

  // 1. Doctrine Synchronization & Physical Paths
  const doctrineRel = 'docs/AGENTS/DOCTRINE.md';
  const doctrinePath = resolveRoot(doctrineRel);
  if (!fs.existsSync(doctrinePath)) {
    errors.push(`[DOCTRINE_MISSING] Missing ${doctrineRel}`);
  } else {
    const doctrineContent = fs.readFileSync(doctrinePath, 'utf8');
    const canonicalBlock = extractDoctrineBlock(doctrineContent);
    if (!canonicalBlock) {
      errors.push(`[DOCTRINE_MARKERS_MISSING] Missing DOCTRINE markers in ${doctrineRel}`);
    } else {
      for (const mirrorRel of ['AGENTS.md', 'GEMINI.md', 'CLAUDE.md']) {
        const mirrorPath = resolveRoot(mirrorRel);
        if (!fs.existsSync(mirrorPath)) {
          errors.push(`[MIRROR_MISSING] Missing ${mirrorRel}`);
          continue;
        }
        const mirrorBlock = extractDoctrineBlock(fs.readFileSync(mirrorPath, 'utf8'));
        if (mirrorBlock !== canonicalBlock) {
          errors.push(`[DOCTRINE_DRIFT] ${mirrorRel} diverges from ${doctrineRel}`);
        }
      }
      checks.push('doctrine-sync');
    }

    const requiredLocalRefs = [
      'docs/Vault/Decisions/DEC-MADLAB-AGENTIC-MESH-001.md',
      'docs/Vault/Decisions/DEC-MADLAB-AGENTIC-PIVOT-002.md',
      '.aurora/domain-policy.json',
      '.aurora/toolbelt-consumer.json',
      '.agents/rules/designmanualposthero.md'
    ];
    for (const ref of requiredLocalRefs) {
      if (!fs.existsSync(resolveRoot(ref))) {
        errors.push(`[LOCAL_REF_MISSING] Referenced file does not exist on disk: ${ref}`);
      }
    }
    checks.push('local-refs-exist');
  }

  // 2. Active Agentic Web & Outbound Skills + Updated Active Skills
  const requiredMeshKeys = [
    'schema_version',
    'id',
    'name',
    'description',
    'manual_version',
    'activation',
    'capabilities',
    'runtime',
    'risk_calibration',
    'quality',
    'classification',
    'observability',
    'ontology',
    'anti_patterns',
    'operational_memory',
    'fail_closed_strategy',
    'tier_policy'
  ];

  const activeSkills = [
    '.aurora/skills/agentic-web-architect/SKILL.md',
    '.aurora/skills/b2b-ai-outbound-architect/SKILL.md',
    '.aurora/skills/qa-review/SKILL.md',
    '.aurora/skills/ceo-web/SKILL.md',
    '.aurora/skills/ceo-copy/SKILL.md'
  ];

  for (const skillRel of activeSkills) {
    const skillPath = resolveRoot(skillRel);
    if (!fs.existsSync(skillPath)) {
      errors.push(`[ACTIVE_SKILL_MISSING] Missing ${skillRel}`);
      continue;
    }
    const content = fs.readFileSync(skillPath, 'utf8');
    const fm = extractFrontmatter(content);
    if (!fm) {
      errors.push(`[FRONTMATTER_MISSING] Missing YAML frontmatter in ${skillRel}`);
    } else {
      if (!/status:\s*active/i.test(fm)) {
        errors.push(`[ACTIVE_SKILL_STATUS_INVALID] ${skillRel} must have status: active`);
      }
      if (/deprecated:\s*true/i.test(fm)) {
        errors.push(`[ACTIVE_SKILL_DEPRECATED] ${skillRel} must not have deprecated: true`);
      }
    }

    try {
      const mesh = extractMeshContractJson(content);
      if (!mesh) {
        errors.push(`[MESH_CONTRACT_MISSING] Missing ## Mesh Contract JSON in ${skillRel}`);
      } else {
        for (const key of requiredMeshKeys) {
          if (!(key in mesh)) {
            errors.push(`[MESH_KEY_MISSING] ${skillRel} Mesh Contract missing key '${key}'`);
          }
        }
        if (mesh.manual_version !== 'V9.1') {
          errors.push(`[MESH_MANUAL_VERSION_INVALID] ${skillRel} must target manual_version V9.1`);
        }
      }
    } catch (err) {
      errors.push(`[MESH_JSON_INVALID] Invalid JSON in ${skillRel}: ${err.message}`);
    }
  }
  checks.push('active-skills-mesh');

  // Specific WebMCP & GEO checks on agentic-web-architect
  const webArchPath = resolveRoot('.aurora/skills/agentic-web-architect/SKILL.md');
  if (fs.existsSync(webArchPath)) {
    const webArchContent = fs.readFileSync(webArchPath, 'utf8');
    const requiredTokens = [
      'document.modelContext',
      'Accept: text/markdown',
      '/.well-known/agent-card.json',
      '/llms.txt',
      '@graph',
      'Spec-Sheet',
      'Citation-Magnet',
      'readOnlyHint',
      'consequentialHint'
    ];
    for (const token of requiredTokens) {
      if (!webArchContent.includes(token)) {
        errors.push(`[WEBMCP_TOKEN_MISSING] agentic-web-architect missing required contract token: ${token}`);
      }
    }
    // Check that navigator.modelContext is never used as a positive code registration call
    if (/navigator\.modelContext\.registerTool/.test(webArchContent)) {
      errors.push(`[DEPRECATED_WEBMCP_API] agentic-web-architect must not invoke navigator.modelContext.registerTool`);
    }
  }

  // Specific Outbound checks on b2b-ai-outbound-architect
  const outboundPath = resolveRoot('.aurora/skills/b2b-ai-outbound-architect/SKILL.md');
  if (fs.existsSync(outboundPath)) {
    const outboundContent = fs.readFileSync(outboundPath, 'utf8');
    for (const token of ['Plain-Text', 'Signal-Based Selling', 'Micro-Asset', 'EXCHANGELABS']) {
      if (!outboundContent.includes(token)) {
        errors.push(`[OUTBOUND_TOKEN_MISSING] b2b-ai-outbound-architect missing required token: ${token}`);
      }
    }
  }

  // 3. Deprecation of Legacy Aesthetic Skills & Brand Docs (Append-Only Enforcement)
  const deprecatedFiles = [
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

  for (const depRel of deprecatedFiles) {
    const depPath = resolveRoot(depRel);
    if (!fs.existsSync(depPath)) {
      errors.push(`[APPEND_ONLY_VIOLATION] Historical/deprecated file was deleted instead of marked deprecated: ${depRel}`);
      continue;
    }
    const content = fs.readFileSync(depPath, 'utf8');
    const fm = extractFrontmatter(content);
    if (!fm || !/deprecated:\s*true/i.test(fm) || !/status:\s*deprecated/i.test(fm)) {
      errors.push(`[DEPRECATION_MISSING] ${depRel} must contain 'deprecated: true' and 'status: deprecated' in YAML frontmatter`);
    }
  }
  checks.push('deprecated-skills-and-docs');

  // Check that .agents/rules/designmanualposthero.md and qa-review/SKILL.md do not enforce legacy Dark/Mad Lab Theme
  const postHeroPath = resolveRoot('.agents/rules/designmanualposthero.md');
  if (fs.existsSync(postHeroPath)) {
    const postHeroContent = fs.readFileSync(postHeroPath, 'utf8');
    if (
      postHeroContent.includes('# AURORA DESIGN MANUAL - POST-HERO v2.0') ||
      postHeroContent.includes('Hero termina CLARO -> Seção 1: CLARO')
    ) {
      errors.push(`[LEGACY_RULE_ACTIVE] .agents/rules/designmanualposthero.md still contains active Post-Hero v2.0 dark/light frequency rules`);
    }
    if (!postHeroContent.includes('criterio_formal_de_aceite_de_interface.md') || !postHeroContent.includes('document.modelContext')) {
      errors.push(`[RULE_MISSING_AGENTIC_CONTRACT] .agents/rules/designmanualposthero.md must reference criterio_formal_de_aceite_de_interface.md and document.modelContext`);
    }
  }

  const qaSkillPath = resolveRoot('.aurora/skills/qa-review/SKILL.md');
  if (fs.existsSync(qaSkillPath)) {
    const qaContent = fs.readFileSync(qaSkillPath, 'utf8');
    if (qaContent.includes('MAD_LAB_THEME_SURFACE_VIOLATION') || qaContent.includes('Exo Ape Clones Block')) {
      errors.push(`[LEGACY_QA_GATE_ACTIVE] .aurora/skills/qa-review/SKILL.md still enforces deprecated Mad Lab Theme / Exo Ape rules`);
    }
  }

  // 4. Configuration & Boundary Integrity
  const domainPolicyPath = resolveRoot('.aurora/domain-policy.json');
  if (fs.existsSync(domainPolicyPath)) {
    try {
      const dp = JSON.parse(fs.readFileSync(domainPolicyPath, 'utf8'));
      if (dp.constitution_ref !== 'docs/AGENTS/DOCTRINE.md') {
        errors.push(`[DOMAIN_POLICY_INVALID] constitution_ref must be 'docs/AGENTS/DOCTRINE.md'`);
      }
      if (!Array.isArray(dp.governance?.prohibited_actions) || !dp.governance.prohibited_actions.includes('replicate_alvaro_runtime')) {
        errors.push(`[DOMAIN_POLICY_BOUNDARY] prohibited_actions must include 'replicate_alvaro_runtime'`);
      }
    } catch (err) {
      errors.push(`[DOMAIN_POLICY_JSON_ERR] ${err.message}`);
    }
  }

  const toolbeltPath = resolveRoot('.aurora/toolbelt-consumer.json');
  if (fs.existsSync(toolbeltPath)) {
    try {
      const tb = JSON.parse(fs.readFileSync(toolbeltPath, 'utf8'));
      if (tb.on_unavailable !== 'FACTORY_TOOL_UNAVAILABLE') {
        errors.push(`[TOOLBELT_INVALID] on_unavailable must be FACTORY_TOOL_UNAVAILABLE`);
      }
    } catch (err) {
      errors.push(`[TOOLBELT_JSON_ERR] ${err.message}`);
    }
  }

  const manifestPath = resolveRoot('project-manifest.json');
  if (fs.existsSync(manifestPath)) {
    try {
      const pm = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
      if (pm.installed_skills?.['agentic-web-architect']?.status !== 'production') {
        errors.push(`[MANIFEST_MISSING_SKILL] project-manifest.json must list agentic-web-architect as production`);
      }
      if (pm.installed_skills?.['b2b-ai-outbound-architect']?.status !== 'production') {
        errors.push(`[MANIFEST_MISSING_SKILL] project-manifest.json must list b2b-ai-outbound-architect as production`);
      }
      const depNames = [
        'ceo-design',
        'ceo-effects',
        'ceo-3d',
        'ceo-art-direction',
        'cinematic-grammar',
        'design-md',
        'taste-design',
        'ceo-critique-theater'
      ];
      for (const name of depNames) {
        const entry = (pm.skills || []).find((s) => s.name === name);
        if (!entry || entry.status !== 'deprecated' || entry.deprecated !== true) {
          errors.push(`[MANIFEST_SKILL_NOT_DEPRECATED] project-manifest.json skill '${name}' must have status='deprecated' and deprecated=true`);
        }
      }
    } catch (err) {
      errors.push(`[MANIFEST_JSON_ERR] ${err.message}`);
    }
  }
  checks.push('configs-and-manifest');

  return { ok: errors.length === 0, errors, checks };
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  const { root } = parseArgs(process.argv);
  const result = runGovernanceCheck(root);
  if (!result.ok) {
    console.error(`[madlab-governance] FAILED (${result.errors.length} violation(s)) in ${root}:`);
    for (const err of result.errors) {
      console.error(`  - ${err}`);
    }
    process.exit(1);
  }
  console.log(`[madlab-governance] OK — checks=${result.checks.join(',')} violations=0 root=${root}`);
}
