import re
import math
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys
import os

# Ajuste de path para importação
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from sandbox_contracts import DiagnosticFinding, PipelinePausedException

class SandboxValidator:
    def __init__(self, sandbox_root: str):
        self.sandbox_root = Path(sandbox_root).resolve()
        
    def calculate_entropy(self, s: str) -> float:
        if not s:
            return 0.0
        entropy = 0.0
        for x in set(s):
            p_x = float(s.count(x)) / len(s)
            entropy += - p_x * math.log(p_x, 2)
        return entropy
        
    def is_hex(self, s: str) -> bool:
        return bool(re.match(r'^[a-fA-F0-9]+$', s))
        
    def scan_content(self, content: str, file_path: str) -> List[DiagnosticFinding]:
        findings = []
        
        # 1. Chamadas perigosas
        if re.search(r'\beval\s*\(', content):
            findings.append(DiagnosticFinding(
                code="DANGEROUS_EVAL",
                severity="P0",
                file_path=file_path,
                redacted_message="Blocked eval() invocation pattern.",
                raw_value_hash=hashlib.sha256(b"eval").hexdigest(),
                recommended_action="Refactor to use dynamic lookup or safe parsers."
            ))
        if re.search(r'\bexec\s*\(', content):
            findings.append(DiagnosticFinding(
                code="DANGEROUS_EXEC",
                severity="P0",
                file_path=file_path,
                redacted_message="Blocked exec() invocation pattern.",
                raw_value_hash=hashlib.sha256(b"exec").hexdigest(),
                recommended_action="Remove dynamic execution patterns."
            ))
        if re.search(r'\bos\.system\s*\(', content) or "shell=True" in content:
            findings.append(DiagnosticFinding(
                code="DANGEROUS_SYSTEM",
                severity="P0",
                file_path=file_path,
                redacted_message="Blocked system/shell execution commands.",
                raw_value_hash=hashlib.sha256(b"system").hexdigest(),
                recommended_action="Use allowed commands allowlist instead."
            ))
        if re.search(r'\bsubprocess\s*\.', content):
            findings.append(DiagnosticFinding(
                code="DANGEROUS_SUBPROCESS",
                severity="P0",
                file_path=file_path,
                redacted_message="Blocked subprocess access.",
                raw_value_hash=hashlib.sha256(b"subprocess").hexdigest(),
                recommended_action="Delegate execution to orchestrator.run_command."
            ))
            
        # 2. Endereços IP
        ip_matches = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
        for ip in ip_matches:
            ip_hash = hashlib.sha256(ip.encode()).hexdigest()
            if ip == "169.254.169.254":
                findings.append(DiagnosticFinding(
                    code="IP_METADATA",
                    severity="P0",
                    file_path=file_path,
                    redacted_message="Metadata IP access blocked.",
                    raw_value_hash=ip_hash,
                    recommended_action="Remove cloud metadata IP references."
                ))
            elif ip.startswith("10.") or ip.startswith("192.168.") or ip.startswith("172.16.") or ip == "127.0.0.1":
                findings.append(DiagnosticFinding(
                    code="IP_PRIVATE",
                    severity="P0",
                    file_path=file_path,
                    redacted_message="Private or Loopback IP access blocked.",
                    raw_value_hash=ip_hash,
                    recommended_action="Do not reference local or private networks."
                ))
            else:
                findings.append(DiagnosticFinding(
                    code="IP_PUBLIC",
                    severity="P1",
                    file_path=file_path,
                    redacted_message="Public IP reference detected.",
                    raw_value_hash=ip_hash,
                    recommended_action="Ensure IP address references are authorized."
                ))
                
        # 3. Segredos por atribuição e alta entropia
        secret_patterns = re.findall(r'(?:key|secret|password|token|auth)\s*[:=]\s*["\']([A-Za-z0-9+/=_\-]{16,})["\']', content, re.IGNORECASE)
        for sec in secret_patterns:
            if not self.is_hex(sec) and self.calculate_entropy(sec) > 3.8:
                findings.append(DiagnosticFinding(
                    code="SECRET_KEY_LABEL",
                    severity="P0",
                    file_path=file_path,
                    redacted_message="Assigned secret token detected by label key.",
                    raw_value_hash=hashlib.sha256(sec.encode()).hexdigest(),
                    recommended_action="Inject secret credentials via environment context."
                ))
                
        # Strings literais de alta entropia (exclui hashes hex puro)
        all_strings = re.findall(r'["\']([A-Za-z0-9+/=_\-]{20,})["\']', content)
        for s in all_strings:
            if not self.is_hex(s) and self.calculate_entropy(s) > 4.5:
                findings.append(DiagnosticFinding(
                    code="SECRET_ENTROPY",
                    severity="P0",
                    file_path=file_path,
                    redacted_message="High entropy string literal detected.",
                    raw_value_hash=hashlib.sha256(s.encode()).hexdigest(),
                    recommended_action="Remove raw credential literals from source files."
                ))
                
        # 4. Domínios públicos (P3 Warning)
        domains = re.findall(r'https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}', content)
        for dom in domains:
            findings.append(DiagnosticFinding(
                code="PUBLIC_DOMAIN",
                severity="P3",
                file_path=file_path,
                redacted_message="Public URL schema referenced in file.",
                raw_value_hash=hashlib.sha256(dom.encode()).hexdigest(),
                recommended_action="Check if remote domain calls conform to network bounds."
            ))
            
        return findings
        
    def check_boundary_escapes(self, file_path: Path) -> List[DiagnosticFinding]:
        findings = []
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return []
            
        imports_found = re.findall(r'(?:import|from|require)\s*\(?\s*["\']([^"\'\n]+)["\']', content)
        for imp in imports_found:
            if imp.startswith(".") or os.path.isabs(imp):
                try:
                    resolved_imp = (file_path.parent / imp).resolve()
                    # Boundary escape check
                    if not resolved_imp.is_relative_to(self.sandbox_root):
                        findings.append(DiagnosticFinding(
                            code="BOUNDARY_ESCAPE_IMPORT",
                            severity="P0",
                            file_path=str(file_path),
                            redacted_message="Import statement escapes sandbox directory boundaries.",
                            raw_value_hash=hashlib.sha256(imp.encode()).hexdigest(),
                            recommended_action="Import relative workspace modules or declare dependencies in registry."
                        ))
                except Exception:
                    if ".." in imp:
                        findings.append(DiagnosticFinding(
                            code="BOUNDARY_ESCAPE_CHECK_FAILED",
                            severity="P0",
                            file_path=str(file_path),
                            redacted_message="Path traversal characters detected in import statement.",
                            raw_value_hash=hashlib.sha256(imp.encode()).hexdigest(),
                            recommended_action="Use internal imports relative to workspace root."
                        ))
        return findings

    def validate_workspace(self) -> List[DiagnosticFinding]:
        """Scans the sandbox workspace recursively for validation findings."""
        all_findings = []
        for root, _, files in os.walk(self.sandbox_root):
            for file in files:
                normalized_root = Path(root).as_posix()
                if ".git" in normalized_root or "__pycache__" in normalized_root or ".next" in normalized_root or "node_modules" in normalized_root or "factory/sandbox" in normalized_root:
                    continue
                    
                # Regra: Pular pastas de assets descarregados do kit original (_files)
                if "_files" in normalized_root:
                    continue
                # Regra: Pular scripts externos conhecidos do kit de terceiros
                if file.endswith(".js.download") or file.endswith(".min.js") or file == "js" or file.endswith(".css.download"):
                    continue
                    
                fp = Path(root) / file
                
                # Check for symlink/junction escapes
                curr = fp
                contains_symlink = False
                while curr != self.sandbox_root and curr != curr.parent:
                    if curr.is_symlink():
                        contains_symlink = True
                        break
                    curr = curr.parent
                
                if contains_symlink:
                    all_findings.append(DiagnosticFinding(
                        code="BOUNDARY_ESCAPE_SYMLINK",
                        severity="P0",
                        file_path=str(fp),
                        redacted_message="Symlink or junction path escape detected within sandbox.",
                        raw_value_hash=hashlib.sha256(str(fp).encode()).hexdigest(),
                        recommended_action="Remove all symbolic links and junction points inside sandbox root."
                    ))
                
                # Check boundary escapes
                escapes = self.check_boundary_escapes(fp)
                all_findings.extend(escapes)
                
                # Scan file content
                try:
                    content = fp.read_text(encoding="utf-8")
                    content_findings = self.scan_content(content, str(fp))
                    all_findings.extend(content_findings)
                except Exception:
                    pass
                    
        p0_findings = [f for f in all_findings if f.severity == "P0"]
        if p0_findings:
            raise PipelinePausedException("Sandbox Validation Failed: P0 critical findings detected.", p0_findings)
            
        return all_findings
