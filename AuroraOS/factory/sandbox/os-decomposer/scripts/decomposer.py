import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import sys
import os
import re
import shlex

# Ajusta path para importar contratos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from contracts import MicroTask, DecomposedOS
from scripts.os_parser import parse_os_file

class Decomposer:
    """Transforma passos de OS em uma DAG de MicroTasks."""
    
    def __init__(self, os_id: str, os_path: Path):
        self.os_id = os_id
        self.os_path = os_path
        
    def decompose(self) -> DecomposedOS:
        steps = parse_os_file(self.os_path)
        tasks = []
        graph = {}
        
        last_task_id = None
        
        # Verifica se existe diretório de testes para fallback inteligente
        has_tests = (self.os_path.parent / "tests").exists() or (self.os_path.parent.parent / "tests").exists()
        
        for i, step in enumerate(steps, 1):
            task_id = f"MT-{str(i).zfill(3)}"
            
            # Tenta extrair comandos de teste do conteúdo
            test_cmds = self._extract_test_cmds(step["content"])
            if not test_cmds:
                # Fallback inteligente: se houver diretório de testes e o passo sugerir teste
                if has_tests and any(k in step["title"].lower() for k in ["test", "valida", "check"]):
                    test_cmds = ["pytest", "-v"]
                else:
                    test_cmds = ["python", "--version"] 
            
            task = MicroTask(
                task_id=task_id,
                description=f"{step['title']}\n{step['content'][:200]}...",
                input_expected="Estado anterior conforme plano",
                output_expected="Estado posterior conforme plano",
                test_cmd=test_cmds,
                depends_on=[last_task_id] if last_task_id else []
            )
            
            tasks.append(task)
            graph[task_id] = task.depends_on
            last_task_id = task_id
            
        return DecomposedOS(
            os_id=self.os_id,
            original_os_path=self.os_path,
            tasks=tasks,
            dependency_graph=graph,
            estimated_total_duration_seconds=len(tasks) * 120,
            decomposed_at=datetime.now()
        )

    def _extract_test_cmds(self, content: str) -> List[str]:
        """Busca blocos de código powershell/bash para usar como teste."""
        code_blocks = re.findall(r"```(?:powershell|bash|sh|cmd)?\n(.*?)\n```", content, re.S)
        if code_blocks:
            last_block = code_blocks[-1]
            lines = [l.strip() for l in last_block.split("\n") if l.strip() and not l.startswith("#")]
            if lines:
                # Usa shlex para parsing robusto
                try:
                    cmd_list = shlex.split(lines[0])
                    # Validação de Segurança Industrial
                    if self._is_safe_command(cmd_list):
                        return cmd_list
                except Exception:
                    pass
        return []

    def _is_safe_command(self, cmd_list: List[str]) -> bool:
        """Valida se o comando é seguro para execução automática."""
        if not cmd_list:
            return False
            
        # Lista de operadores proibidos em comandos atômicos
        banned_operators = {";", "&", "|", ">", "<", "`", "$(", "${"}
        
        # Banned binaries (prevenção básica)
        banned_binaries = {"rm", "format", "del", "rd", "curl", "wget", "ssh"}
        
        binary = cmd_list[0].lower()
        violation = None
        
        if binary in banned_binaries:
            violation = f"Banned binary detected: {binary}"
        else:
            for part in cmd_list:
                for op in banned_operators:
                    if op in part:
                        violation = f"Banned operator '{op}' detected in command part: {part}"
                        break
                if violation: break
        
        if violation:
            self._log_security_violation(cmd_list, violation)
            return False
                
        return True

    def _log_security_violation(self, cmd_list: List[str], reason: str):
        """Registra violações de segurança para auditoria do Comandante."""
        log_path = self.os_path.parent / "SECURITY_AUDIT.jsonl"
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "os_id": self.os_id,
            "blocked_command": " ".join(cmd_list),
            "reason": reason,
            "severity": "HIGH"
        }
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"⚠️ [SECURITY_ALERT] Comando bloqueado por segurança: {reason}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("os_path", type=str)
    parser.add_argument("--os_id", type=str, default="OS-UNKNOWN")
    args = parser.parse_args()
    
    decomposer = Decomposer(args.os_id, Path(args.os_path))
    decomposed = decomposer.decompose()
    
    output_path = Path(args.os_path).with_suffix(".decomposed.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decomposed.model_dump_json(indent=2))
        
    print(f"Decomposição concluída: {output_path}")
