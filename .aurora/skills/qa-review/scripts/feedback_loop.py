#!/usr/bin/env python3
"""
feedback_loop.py — Retroalimentação automática da Skill QA Review para Ozzmosis

Atualiza memória/changelog e, opcionalmente, emite eventos CROSS_SKILL_FEEDBACK canônicos.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "docs" / "Vault" / "activity.jsonl").exists() and (parent / "scripts" / "agents").exists():
            return parent
    fallback = Path("C:/Projetos/Aurora/Ozzmosis")
    if fallback.exists():
        return fallback
    raise RuntimeError("Nao foi possivel localizar a raiz do repositorio")


REPO_ROOT = find_repo_root()
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from scripts.agents import skill_mesh_events


def load_json(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ Erro ao ler JSON {path}: {e}")
    return {}


def save_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def bump_version(version: str, level: str = "patch") -> str:
    parts = [int(x) for x in version.split(".")]
    if level == "major":
        parts = [parts[0] + 1, 0, 0]
    elif level == "minor":
        parts = [parts[0], parts[1] + 1, 0]
    else:
        parts = [parts[0], parts[1], parts[2] + 1]
    return ".".join(str(p) for p in parts)


def update_memory(
    skill_dir: Path,
    session_summary: str,
    learnings: list[str],
    skill_updated: bool = False,
    persist: bool = True,
) -> dict:
    memory_path = skill_dir / "memory.json"
    memory = load_json(memory_path)

    if not memory:
        memory = {
            "skill_name": skill_dir.name,
            "last_updated": "",
            "version": "1.0.0",
            "github_repo": "https://github.com/Aurora-AI/Ozzmosis",
            "platform_contexts": {
                "antigravity": {"notes": [], "patterns": []},
                "codex": {"notes": [], "patterns": []}
            },
            "interaction_log": [],
            "accumulated_patterns": []
        }
    memory.setdefault("last_updated", "")
    memory.setdefault("version", "1.0.0")
    memory.setdefault("platform_contexts", {
        "antigravity": {"notes": [], "patterns": []},
        "codex": {"notes": [], "patterns": []}
    })
    memory.setdefault("interaction_log", [])
    memory.setdefault("accumulated_patterns", [])

    now = datetime.now(timezone.utc).isoformat()
    memory["last_updated"] = now

    # Add interaction log entry
    memory["interaction_log"].append({
        "date": now,
        "summary": session_summary,
        "learnings": learnings,
        "triggered_skill_update": skill_updated
    })

    # Track pattern frequency (Cognitive Ingestion)
    for learning in learnings:
        found = False
        for p in memory["accumulated_patterns"]:
            if learning.lower() in p["pattern"].lower():
                p["frequency"] += 1
                found = True
                break
        if not found:
            memory["accumulated_patterns"].append({
                "pattern": learning,
                "frequency": 1,
                "incorporated_in_skill": False
            })

    # Auto-promote patterns with frequency >= 3
    promoted = []
    for p in memory["accumulated_patterns"]:
        if p["frequency"] >= 3 and not p["incorporated_in_skill"]:
            promoted.append(p["pattern"])
            p["incorporated_in_skill"] = True

    if skill_updated:
        memory["version"] = bump_version(memory.get("version", "1.0.0"), "minor")
    elif learnings:
        memory["version"] = bump_version(memory.get("version", "1.0.0"), "patch")

    if persist:
        save_json(memory_path, memory)
    return {"memory": memory, "promoted_patterns": promoted}


def update_changelog(
    skill_dir: Path,
    version: str,
    added: list[str],
    fixed: list[str],
    learned: list[str],
    persist: bool = True,
) -> str:
    changelog_path = skill_dir / "changelog.md"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    new_entry = f"\n## [{version}] — {today}\n"
    if added:
        new_entry += "### Adicionado (Axiomas/Capabilities)\n" + "".join(f"- {a}\n" for a in added)
    if fixed:
        new_entry += "### Corrigido (Refinement)\n" + "".join(f"- {f}\n" for f in fixed)
    if learned:
        new_entry += "### Aprendido (Insights)\n" + "".join(f"- {l}\n" for l in learned)

    # Read existing or create new
    if changelog_path.exists():
        existing = changelog_path.read_text(encoding="utf-8")
    else:
        existing = f"# Changelog — {skill_dir.name}\n"

    # Insert after the title or at the beginning
    lines = existing.split("\n", 1)
    if len(lines) > 1:
        updated = lines[0] + "\n" + new_entry + lines[1]
    else:
        updated = existing + "\n" + new_entry

    if persist:
        changelog_path.write_text(updated, encoding="utf-8")
    return updated


def run(
    skill_dir_path: str,
    session_summary: str,
    learnings_raw: str,
    skill_updated: bool = False,
    emit_feedback: bool = False,
    ledger: Path | None = None,
    os_id: str | None = None,
    task_id: str | None = None,
    author: str = "qa-review",
    severity: str | None = None,
    source_skill: str | None = None,
    target_skill: str | None = None,
    issue_type: str | None = None,
    context_ref: str | None = None,
    evidence: list[str] | None = None,
    proposed_rule: str | None = None,
    status: str | None = None,
    promoted_to: list[str] | None = None,
    intent_text: str | None = None,
    dry_run: bool = False,
    dry_run_complete: bool = False,
):
    skill_dir = Path(skill_dir_path).resolve()
    if not skill_dir.exists():
        print(f"❌ Diretório não encontrado: {skill_dir_path}", file=sys.stderr)
        sys.exit(1)

    # Support both | and semantic splitting
    learnings = [l.strip() for l in learnings_raw.split("|") if l.strip()]
    persist = not dry_run_complete

    result = update_memory(skill_dir, session_summary, learnings, skill_updated, persist=persist)
    memory = result["memory"]
    promoted = result["promoted_patterns"]

    update_changelog(
        skill_dir,
        version=memory["version"],
        added=learnings if skill_updated else [],
        fixed=[],
        learned=learnings if not skill_updated else [],
        persist=persist,
    )

    print(f"✅ [Aurora] Retroalimentação concluída — v{memory['version']}")
    print(f"📝 {len(learnings)} aprendizado(s) registrado(s) no log de interação.")
    if dry_run_complete:
        print("🧪 dry-run-complete ativo: memory.json, changelog.md e activity.jsonl nao serao alterados.")
    if promoted:
        print(f"🚀 {len(promoted)} padrão(ões) promovido(s) — sugerido revisar SKILL.md:")
        for p in promoted:
            print(f"   → {p}")
    if not emit_feedback:
        return

    if not os_id and not task_id:
        raise SystemExit("emit-feedback requer --os-id ou --task-id")

    required_feedback = {
        "severity": severity,
        "source_skill": source_skill,
        "target_skill": target_skill,
        "issue_type": issue_type,
        "proposed_rule": proposed_rule,
        "status": status,
    }
    missing = [key for key, value in required_feedback.items() if not value]
    if missing:
        raise SystemExit(f"emit-feedback requer os campos: {', '.join(missing)}")
    if not evidence:
        raise SystemExit("emit-feedback requer ao menos um --evidence")

    event_args = argparse.Namespace(
        os_id=os_id,
        task_id=task_id,
        event_id=None,
        author=author,
        severity=severity,
        source_skill=source_skill,
        target_skill=target_skill,
        issue_type=issue_type,
        context_ref=context_ref,
        evidence=evidence,
        proposed_rule=proposed_rule,
        status=status,
        promoted_to=promoted_to,
        intent_text=intent_text,
    )
    event = skill_mesh_events.build_feedback_event(event_args)
    skill_mesh_events.validate_or_raise(event, "feedback")
    print(json.dumps(event, ensure_ascii=True, indent=2))
    if not dry_run and not dry_run_complete:
        skill_mesh_events.append_event(ledger or skill_mesh_events.DEFAULT_LEDGER, event)
        print(f"🧾 Evento CROSS_SKILL_FEEDBACK anexado em {ledger or skill_mesh_events.DEFAULT_LEDGER}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retroalimenta qa-review e opcionalmente emite CROSS_SKILL_FEEDBACK."
    )
    parser.add_argument("skill_dir")
    parser.add_argument("session_summary")
    parser.add_argument("learnings_raw")
    parser.add_argument("--skill-updated", action="store_true")
    parser.add_argument("--emit-feedback", action="store_true")
    parser.add_argument("--ledger", type=Path, default=skill_mesh_events.DEFAULT_LEDGER)
    parser.add_argument("--os-id")
    parser.add_argument("--task-id")
    parser.add_argument("--author", default="qa-review")
    parser.add_argument("--severity", choices=sorted(skill_mesh_events.SEVERITIES))
    parser.add_argument("--source-skill")
    parser.add_argument("--target-skill")
    parser.add_argument("--issue-type")
    parser.add_argument("--context-ref")
    parser.add_argument("--evidence", action="append")
    parser.add_argument("--proposed-rule")
    parser.add_argument("--status", choices=sorted(skill_mesh_events.FEEDBACK_STATUSES))
    parser.add_argument("--promoted-to", action="append", choices=sorted(skill_mesh_events.PROMOTION_TARGETS))
    parser.add_argument("--intent-text")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--dry-run-complete", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(
        skill_dir_path=args.skill_dir,
        session_summary=args.session_summary,
        learnings_raw=args.learnings_raw,
        skill_updated=args.skill_updated,
        emit_feedback=args.emit_feedback,
        ledger=args.ledger,
        os_id=args.os_id,
        task_id=args.task_id,
        author=args.author,
        severity=args.severity,
        source_skill=args.source_skill,
        target_skill=args.target_skill,
        issue_type=args.issue_type,
        context_ref=args.context_ref,
        evidence=args.evidence,
        proposed_rule=args.proposed_rule,
        status=args.status,
        promoted_to=args.promoted_to,
        intent_text=args.intent_text,
        dry_run=args.dry_run,
        dry_run_complete=args.dry_run_complete,
    )
