import pytest
from pathlib import Path
from validator import SandboxValidator
from sandbox_contracts import PipelinePausedException

def test_validator_shannon_entropy():
    validator = SandboxValidator("/tmp")
    # Low entropy
    assert validator.calculate_entropy("aaaaaaa") == 0.0
    # High entropy random string
    assert validator.calculate_entropy("A9x!kP89zLq@1s") > 3.0

def test_validator_scan_dangerous_code():
    validator = SandboxValidator("/tmp")
    
    # 1. P0 Hard Fails on dangerous invocations
    content_eval = "val = eval('2 + 2')"
    findings = validator.scan_content(content_eval, "test.py")
    assert any(f.code == "DANGEROUS_EVAL" and f.severity == "P0" for f in findings)
    
    content_exec = "exec(code)"
    findings = validator.scan_content(content_exec, "test.py")
    assert any(f.code == "DANGEROUS_EXEC" and f.severity == "P0" for f in findings)

    content_sys = "os.system('rm -rf')"
    findings = validator.scan_content(content_sys, "test.py")
    assert any(f.code == "DANGEROUS_SYSTEM" and f.severity == "P0" for f in findings)

def test_validator_scan_ips():
    validator = SandboxValidator("/tmp")
    
    # Metadata IP -> P0
    findings = validator.scan_content("metadata_url = '169.254.169.254'", "test.py")
    assert any(f.code == "IP_METADATA" and f.severity == "P0" for f in findings)
    
    # Private IP -> P0
    findings = validator.scan_content("local_ip = '192.168.1.10'", "test.py")
    assert any(f.code == "IP_PRIVATE" and f.severity == "P0" for f in findings)
    
    # Public IP -> P1 Warning
    findings = validator.scan_content("public_ip = '8.8.8.8'", "test.py")
    assert any(f.code == "IP_PUBLIC" and f.severity == "P1" for f in findings)

def test_validator_secrets_vs_hashes():
    validator = SandboxValidator("/tmp")
    
    # High entropy UUID/Hex Hash -> Excluded from P0
    hex_hash = "cbf5ad57dadd471c871321fbad51f25c" # md5/hex
    findings = validator.scan_content(f'hash_val = "{hex_hash}"', "test.py")
    # Pure hex shouldn't fail
    assert not any(f.severity == "P0" for f in findings)
    
    # High entropy password label -> P0
    findings = validator.scan_content('api_key = "dGhpcy1pcy1hLXNlY3JldC10b2tlbg=="', "test.py")
    assert any(f.code == "SECRET_KEY_LABEL" and f.severity == "P0" for f in findings)

def test_validator_public_domain_warning():
    validator = SandboxValidator("/tmp")
    findings = validator.scan_content("url = 'https://google.com'", "test.py")
    assert any(f.code == "PUBLIC_DOMAIN" and f.severity == "P3" for f in findings)

def test_validator_boundary_escapes(tmp_path):
    validator = SandboxValidator(str(tmp_path))
    
    # Valid relative import inside sandbox root
    file_in_root = tmp_path / "page.tsx"
    file_in_root.write_text("import { child } from './child';", encoding="utf-8")
    assert len(validator.check_boundary_escapes(file_in_root)) == 0
    
    # Escaping relative import outside sandbox root
    escaping_file = tmp_path / "escaping.tsx"
    escaping_file.write_text("import { config } from '../config';", encoding="utf-8")
    findings = validator.check_boundary_escapes(escaping_file)
    assert any(f.code == "BOUNDARY_ESCAPE_IMPORT" and f.severity == "P0" for f in findings)

def test_validator_symlink_escape(tmp_path):
    validator = SandboxValidator(str(tmp_path))
    
    file_sym = tmp_path / "symlinked_file.py"
    file_sym.write_text("print('symlink')", encoding="utf-8")
    
    from unittest.mock import patch
    # We patch Path.is_symlink on the level of the Path objects inside validate_workspace
    original_is_symlink = Path.is_symlink
    def mock_is_symlink(self):
        if self.name == "symlinked_file.py":
            return True
        return original_is_symlink(self)
        
    with patch.object(Path, "is_symlink", mock_is_symlink):
        with pytest.raises(PipelinePausedException) as exc:
            validator.validate_workspace()
        assert any(f.code == "BOUNDARY_ESCAPE_SYMLINK" and f.severity == "P0" for f in exc.value.findings)
