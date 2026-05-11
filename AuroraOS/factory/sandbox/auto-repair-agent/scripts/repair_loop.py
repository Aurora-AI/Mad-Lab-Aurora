"""Cérebro do ciclo de reparo autônomo."""
from __future__ import annotations

import json
import time
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Adicionar o diretório atual e o pai ao sys.path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(current_dir))
sys.path.append(str(parent_dir))

from contracts import (
    RepairRequest, RepairResult, RepairState,
    AttemptResult, ActivityEvent, SandboxMode,
    AntiPatternCandidate, QAHeadlessRequest, QAHeadlessVerdict
)
from sandbox_executor import (
    execute_in_sandbox, emit_activity_event,
    save_checkpoint, load_checkpoint, atomic_write_json
)
from classify_mode import classify_mode

def log_activity(activity_path: Path, entry: dict) -> None:
    """Registra atividade com retry (exponential backoff) para suportar concorrência."""
    import time
    import random
    
    max_retries = 5
    for i in range(max_retries):
        try:
            fd = os.open(str(activity_path), os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_EXCL)
            with os.fdopen(fd, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, default=str) + "\n")
            return
        except FileExistsError:
            wait = (2 ** i) * 0.1 + random.uniform(0, 0.1)
            time.sleep(wait)
        except Exception:
            break
    
    # Fallback determinístico
    with open(activity_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")

def repair_loop(
    request: RepairRequest, 
    hypothesis_patches: list[str],
    os_id: str,
    activity_path: Path,
    state_path: Path,
    work_dir: Path | None = None,
    artifacts_dir: Path | None = None
) -> RepairResult:
    """Executa o loop completo de reparo."""
    
    # 1. Carregar checkpoint existente
    state_data = load_checkpoint(state_path)
    if state_data:
        state = RepairState(**state_data)
        if state.is_terminal and state.final_result:
            return state.final_result
    else:
        # 2. Classificar SandboxMode
        mode = classify_mode(request.test_cmd)
        state = RepairState(
            task_id=request.task_id,
            sandbox_mode=mode,
            current_attempt=0
        )

    # Emitir evento de início se for a primeira tentativa
    if state.current_attempt == 0:
        emit_activity_event(
            activity_path, "REPAIR_STARTED", os_id, request.task_id, 
            {"sandbox_mode": state.sandbox_mode}
        )

    # 3. Iterar sobre hipóteses
    for i in range(state.current_attempt, len(hypothesis_patches)):
        if i >= request.max_attempts:
            break
            
        patch = hypothesis_patches[i]
        state.current_attempt = i + 1
        
        emit_activity_event(
            activity_path, "REPAIR_ATTEMPT", os_id, request.task_id,
            {"attempt": state.current_attempt, "hypothesis": f"Hipótese {state.current_attempt}"}
        )

        # Em uma implementação real, aplicaríamos o patch aqui.
        # OS-004 e OS-005 lidarão com a aplicação física no worktree.
        
        try:
            returncode, stdout, stderr, duration, metrics = execute_in_sandbox(
                request.test_cmd,
                state.sandbox_mode,
                request.timeout_seconds,
                work_dir=work_dir
            )
        except Exception as e:
            # Falha de infraestrutura
            returncode, stdout, stderr, duration, metrics = 1, "", f"Erro fatal no executor: {str(e)}", 0.0, {}
            
        status = "success" if returncode == 0 else "failure"
        if returncode == 124 or duration >= request.timeout_seconds:
            status = "timeout"
            
        attempt = AttemptResult(
            attempt_number=state.current_attempt,
            status=status,
            duration_seconds=duration,
            stdout=stdout,
            stderr=stderr,
            patch_diff=patch,
            hypothesis=f"Hipótese {state.current_attempt}",
            metrics=metrics
        )
        
        state.completed_attempts.append(attempt)
        save_checkpoint(state_path, state.model_dump())
        
        if status == "success":
            # Reparo técnico bem-sucedido. Iniciar QA Headless
            target_artifacts_dir = artifacts_dir or state_path.parent / "artifacts"
            target_artifacts_dir.mkdir(parents=True, exist_ok=True)
            
            qa_req_path = target_artifacts_dir / f"qa_request_{request.task_id}_{state.current_attempt}.json"
            qa_verdict_path = target_artifacts_dir / f"qa_verdict_{request.task_id}_{state.current_attempt}.json"
            
            test_cmd_str = request.test_cmd if isinstance(request.test_cmd, str) else " ".join(request.test_cmd)
            
            # Fallback para original_requirement se vazio
            orig_req = request.original_requirement or f"Reparar falha na tarefa {request.task_id} reportada pelo executor."
            
            qa_req = QAHeadlessRequest(
                task_id=request.task_id,
                os_id=os_id,
                repair_result=RepairResult(
                    task_id=request.task_id,
                    status="fixed",
                    sandbox_mode=state.sandbox_mode,
                    total_attempts=state.current_attempt,
                    attempts=state.completed_attempts,
                    patch_diff=patch
                ),
                original_requirement=orig_req,
                test_cmd=test_cmd_str,
                test_output=f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}",
                patch_diff=patch
            )
            
            atomic_write_json(qa_req_path, qa_req.model_dump())
            emit_activity_event(
                activity_path, "QA_REQUEST_GENERATED", os_id, request.task_id, 
                {"qa_req_path": str(qa_req_path), "original_requirement_len": len(orig_req)}
            )
            
            # Polling síncrono para o Veredito de QA
            verdict_data = None
            wait_timeout = request.qa_timeout_seconds
            start_wait = time.time()
            
            while time.time() - start_wait < wait_timeout:
                if qa_verdict_path.exists():
                    # Check para evitar leitura de arquivo em escrita (Race Condition)
                    if qa_verdict_path.stat().st_size == 0:
                        time.sleep(0.5)
                        continue
                        
                    try:
                        with open(qa_verdict_path, "r", encoding="utf-8") as f:
                            v_dict = json.load(f)
                            verdict_data = QAHeadlessVerdict(**v_dict)
                        break
                    except (json.JSONDecodeError, Exception) as e:
                        # Se falhar após o polling, registramos como erro de integridade
                        emit_activity_event(
                            activity_path, "QA_VERDICT_PARSE_FAILURE", os_id, request.task_id, 
                            {
                                "error": str(e), 
                                "attempt": state.current_attempt, 
                                "file_size": qa_verdict_path.stat().st_size,
                                "is_corrupt": isinstance(e, json.JSONDecodeError)
                            }
                        )
                        # Dá uma pequena chance para o OS terminar o flush (race condition persistente)
                        time.sleep(1)
                else:
                    time.sleep(2)
            
            if not verdict_data:
                # QA Timeout -> Tratar como falha para continuar para a próxima hipótese
                attempt.status = "failure"
                attempt.stderr += f"\n\n[QA HEADLESS TIMEOUT] Veredito não recebido após {wait_timeout}s."
                state.completed_attempts[-1] = attempt
                save_checkpoint(state_path, state.model_dump())
                continue
                
            if verdict_data.verdict == "REJECTED":
                attempt.status = "failure"
                attempt.stderr += f"\n\n[QA REJECTED]\nFindings: {verdict_data.findings}\nCorrections: {verdict_data.suggested_corrections}"
                state.completed_attempts[-1] = attempt
                save_checkpoint(state_path, state.model_dump())
                emit_activity_event(
                    activity_path, "QA_REJECTED", os_id, request.task_id, 
                    {"findings": verdict_data.findings}
                )
                continue # Vai para a próxima hipótese
                
            if verdict_data.verdict == "NEEDS_REVIEW":
                attempt.status = "failure"
                attempt.stderr += f"\n\n[QA NEEDS REVIEW]\nFindings: {verdict_data.findings}"
                state.completed_attempts[-1] = attempt
                save_checkpoint(state_path, state.model_dump())
                break # Sai do loop para escalar diretamente
            
            # verdict == "APPROVED"
            
            # Enriquecimento de Anti-pattern
            anti_pattern = AntiPatternCandidate(
                pattern_id=f"KI-{datetime.now().strftime('%Y%m%d')}-{request.task_id}",
                category="CC", 
                product="Ozzmosis",
                symptom=attempt.stderr[:200] if attempt.stderr else "Falha genérica",
                fix_applied=attempt.patch_diff if attempt.patch_diff else "Patch manual",
                domains=["Repair", "Autocure"]
            )
            
            ap_path = target_artifacts_dir / f"{anti_pattern.pattern_id}.json"
            atomic_write_json(ap_path, anti_pattern.model_dump())
            
            # --- Inserção da OS-07: Sincronização Semântica ---
            try:
                import subprocess
                subprocess.run([
                    "C:/Projetos/Aurora/AuroraOS/factory/sandbox/qdrant-memory/.venv/Scripts/python.exe", 
                    "C:/Projetos/Aurora/AuroraOS/factory/sandbox/qdrant-memory/scripts/embed_antipattern.py",
                    "--single", str(ap_path)
                ], check=False)
                emit_activity_event(
                    activity_path, "MEMORY_SYNC_SUCCESS", os_id, request.task_id, 
                    {"pattern_id": anti_pattern.pattern_id}
                )
            except Exception as e:
                emit_activity_event(
                    activity_path, "MEMORY_SYNC_FAILURE", os_id, request.task_id, 
                    {"error": str(e)}
                )
            # --------------------------------------------------
            
            result = RepairResult(
                task_id=request.task_id,
                status="fixed",
                sandbox_mode=state.sandbox_mode,
                total_attempts=state.current_attempt,
                attempts=state.completed_attempts,
                patch_diff=patch,
                anti_pattern_id=anti_pattern.pattern_id
            )
            
            state.is_terminal = True
            state.final_result = result
            save_checkpoint(state_path, state.model_dump())
            
            emit_activity_event(
                activity_path, "REPAIR_COMPLETED", os_id, request.task_id, 
                {"attempts": state.current_attempt, "anti_pattern_id": anti_pattern.pattern_id, "qa_verdict": "APPROVED"}
            )
            
            return result

    # 4. Escalação (se nenhuma hipótese funcionou)
    escalation_reason = "Esgotou todas as hipóteses disponíveis."
    
    result = RepairResult(
        task_id=request.task_id,
        status="escalated",
        sandbox_mode=state.sandbox_mode,
        total_attempts=state.current_attempt,
        attempts=state.completed_attempts,
        escalation_reason=escalation_reason
    )

    # Sanitização de patch_diff para Markdown
    patch_display = result.patch_diff if result.patch_diff else "Nenhum patch gerado"
    if "```" in patch_display:
        # Escapar blocos de código internos
        patch_display = patch_display.replace("```", "'''")
    
    # Gerar ESCALATION.md com patch sanitizado
    result.patch_diff = patch_display
    generate_escalation_report(request, result, os_id)
    
    state.is_terminal = True
    state.final_result = result
    save_checkpoint(state_path, state.model_dump())
    
    emit_activity_event(
        activity_path, "REPAIR_ESCALATED", os_id, request.task_id, 
        {"reason": escalation_reason}
    )
    
    return result

def generate_escalation_report(request: RepairRequest, result: RepairResult, os_id: str):
    """Gera relatório de escalação para revisão humana."""
    # Buscar templates em relação ao script
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / "templates" / "ESCALATION.md"
    report_path = script_dir.parent / "ESCALATION.md"
    
    if not template_path.exists():
        return
        
    content = template_path.read_text()
    
    # Substituições básicas
    replacements = {
        "{{task_id}}": request.task_id,
        "{{os_id}}": os_id,
        "{{total_attempts}}": str(result.total_attempts),
        "{{max_attempts}}": str(request.max_attempts),
        "{{sandbox_mode}}": result.sandbox_mode.value if hasattr(result.sandbox_mode, 'value') else str(result.sandbox_mode),
        "{{timestamp}}": datetime.now(timezone.utc).isoformat(),
        "{{last_stderr}}": result.attempts[-1].stderr if result.attempts else "N/A",
        "{{patch_diff}}": result.patch_diff or "N/A"
    }
    
    for k, v in replacements.items():
        content = content.replace(k, v)
        
    # Tratamento de loop {{#each attempts}} - mais robusto
    if "{{#each attempts}}" in content and "{{/each}}" in content:
        try:
            start_tag = "{{#each attempts}}"
            end_tag = "{{/each}}"
            
            start_idx = content.find(start_tag)
            end_idx = content.find(end_tag) + len(end_tag)
            
            loop_block = content[start_idx:end_idx]
            loop_template = content[start_idx + len(start_tag) : content.find(end_tag)]
            
            rendered_attempts = []
            for att in result.attempts:
                att_render = loop_template
                att_render = att_render.replace("{{attempt_number}}", str(att.attempt_number))
                att_render = att_render.replace("{{status}}", att.status)
                att_render = att_render.replace("{{hypothesis}}", att.hypothesis)
                att_render = att_render.replace("{{duration_seconds}}", f"{att.duration_seconds:.2f}")
                # Sanitização básica de stdout para evitar quebra de markdown
                safe_stdout = att.stdout.replace("```", "'''")
                att_render = att_render.replace("{{stdout}}", safe_stdout[:500] + ("..." if len(safe_stdout) > 500 else ""))
                rendered_attempts.append(att_render)
                
            content = content.replace(loop_block, "".join(rendered_attempts))
        except Exception as e:
            content += f"\n\n<!-- Erro ao renderizar loop de tentativas: {str(e)} -->"
        
    report_path.write_text(content, encoding="utf-8")
