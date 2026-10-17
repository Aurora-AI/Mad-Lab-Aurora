#!/usr/bin/env node
/**
 * sync-doctrine.mjs — sincroniza docs/AGENTS/DOCTRINE.md para CLAUDE.md, GEMINI.md e AGENTS.md
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..");

const SOURCE = path.join(repoRoot, "docs", "AGENTS", "DOCTRINE.md");
const START = "<!-- DOCTRINE:START -->";
const END = "<!-- DOCTRINE:END -->";

const TARGETS = [
  { file: "CLAUDE.md", title: "CLAUDE.md — Doutrina e Governança Mad Lab Aurora para Claude Code" },
  { file: "GEMINI.md", title: "GEMINI.md — Doutrina e Governança Mad Lab Aurora para Gemini / Antigravity" },
  { file: "AGENTS.md", title: "AGENTS.md — Doutrina e Governança Mad Lab Aurora para qualquer agente" },
];

const HEADER_NOTE =
  "> Gerado a partir de `docs/AGENTS/DOCTRINE.md`. **Não edite este arquivo isoladamente** — edite a fonte\n" +
  "> e rode `node scripts/sync-doctrine.mjs`. O gate `scripts/check-madlab-governance.mjs` falha se divergir.\n" +
  "> Todo agente, em qualquer IDE, opera sob estas regras. Não há papel exclusivo por ferramenta.";

const sourceText = fs.readFileSync(SOURCE, "utf8");
const i = sourceText.indexOf(START);
const j = sourceText.indexOf(END);

if (i === -1 || j === -1 || j < i) {
  console.error(`[doctrine-sync] FAIL — marcadores ${START} / ${END} ausentes em ${SOURCE}`);
  process.exit(1);
}

const block = sourceText.slice(i + START.length, j).trim();

for (const { file, title } of TARGETS) {
  const outPath = path.join(repoRoot, file);
  const rendered = `# ${title}\n\n${HEADER_NOTE}\n\n${START}\n${block}\n${END}\n`;
  fs.writeFileSync(outPath, rendered, "utf8");
  console.log(`[doctrine-sync] escrito: ${file}`);
}

console.log("[doctrine-sync] OK — 3 arquivos sincronizados com docs/AGENTS/DOCTRINE.md");
