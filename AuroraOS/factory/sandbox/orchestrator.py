import os
import subprocess
import uuid
from pathlib import Path
from typing import List, Dict, Any, Union

class CommandBlockedException(Exception):
    pass

class SandboxOrchestrator:
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).resolve()
        self.run_id = f"SR-{uuid.uuid4().hex[:5].upper()}"
        self.sandbox_dir = self.workspace_root / f"sandbox_run_{self.run_id}"
        
        # Define allowed commands precisely
        self.allowed_commands = {
            "python_pytest": {
                "bin": "python",
                "args_prefix": ["-m", "pytest"],
                "network": False,
                "timeout_seconds": 300,
            },
            "npm_build": {
                "bin": "npm",
                "args_exact": ["run", "build"],
                "network": False,
                "timeout_seconds": 300,
            },
            "git_diff": {
                "bin": "git",
                "args_exact": ["diff", "--no-ext-diff"],
                "network": False,
                "timeout_seconds": 60,
            },
        }

    def setup_worktree(self):
        """Creates the git worktree for code isolation."""
        self.validate_path(self.sandbox_dir)
        
        # We need an empty temporary folder for hooksPath during worktree add.
        temp_hooks_dir = self.workspace_root / f".git-hooks-disabled-temp-{self.run_id}"
        os.makedirs(temp_hooks_dir, exist_ok=True)
        
        # Adiciona o worktree sem herdar hooks
        cmd = [
            "git", 
            "-c", f"core.hooksPath={temp_hooks_dir.resolve()}", 
            "worktree", "add", str(self.sandbox_dir), "HEAD", "--detach"
        ]
        env = self._get_isolated_env()
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        
        # Clean up temp_hooks_dir
        if temp_hooks_dir.exists():
            try:
                os.rmdir(temp_hooks_dir)
            except Exception:
                pass

        if res.returncode != 0:
            # Fallback seguro para criação de pasta física se não estiver sob Git
            os.makedirs(self.sandbox_dir, exist_ok=True)
            
        # Agora criamos o diretório permanente de hooks dentro do sandbox
        hooks_dir = self.sandbox_dir / ".git-hooks-disabled"
        os.makedirs(hooks_dir, exist_ok=True)
            
    def cleanup_worktree(self):
        """Cleans up the git worktree and dynamic files."""
        if self.sandbox_dir.exists():
            env = self._get_isolated_env()
            subprocess.run(["git", "worktree", "remove", "-f", str(self.sandbox_dir)], capture_output=True, env=env)
            subprocess.run(["git", "worktree", "prune"], capture_output=True, env=env)
            if self.sandbox_dir.exists():
                import shutil
                shutil.rmtree(self.sandbox_dir, ignore_errors=True)

    def validate_path(self, target_path: Union[str, Path]) -> Path:
        """Canonical path validation. Prevents symlink, junction, and boundary escapes."""
        p = Path(target_path).resolve()
        
        # Boundary escape check
        if not p.is_relative_to(self.workspace_root):
            raise CommandBlockedException(f"Security Block: Path '{target_path}' escapes workspace boundary.")
            
        # Symlinks and Junctions escape check
        curr = p
        while curr != curr.parent:
            if curr.is_symlink():
                raise CommandBlockedException(f"Security Block: Path '{target_path}' contains symlink or junction escapes.")
            curr = curr.parent
            
        return p

    def _get_isolated_env(self) -> Dict[str, str]:
        """Provides isolated environment variable mapping for the Network/Process Policy Layer.
        Network disabled by policy and scan. True network isolation deferred to container/firewall OS.
        """
        env = dict(os.environ)
        env["GIT_CONFIG_NOSYSTEM"] = "1"
        
        empty_gitconfig = self.workspace_root / ".gitconfig_empty"
        if not empty_gitconfig.exists():
            try:
                empty_gitconfig.write_text("", encoding="utf-8")
            except Exception:
                pass
                
        env["GIT_CONFIG_GLOBAL"] = str(empty_gitconfig.resolve())
        env["GIT_CONFIG_SYSTEM"] = str(empty_gitconfig.resolve())
        
        # Override network variables for proxy fallback
        env["HTTP_PROXY"] = "http://127.0.0.1:9999"
        env["HTTPS_PROXY"] = "http://127.0.0.1:9999"
        env["ALL_PROXY"] = "socks5://127.0.0.1:9999"
        env["NO_PROXY"] = ""
        return env

    def run_command(self, cmd_args: List[str], cwd: Union[str, Path], shell: bool = False) -> subprocess.CompletedProcess:
        """Executes a command enforcing allowlist rules, keyword restrictions, and git settings."""
        if shell:
            raise CommandBlockedException("Security Block: shell=True is strictly prohibited.")

        if not cmd_args:
            raise CommandBlockedException("Security Block: Empty command list.")

        cwd_path = self.validate_path(cwd)
        if not cwd_path.is_relative_to(self.sandbox_dir):
            raise CommandBlockedException(f"Security Block: Execution CWD '{cwd}' is outside sandbox '{self.sandbox_dir}'")

        bin_name = os.path.basename(cmd_args[0]).lower()
        bin_base = os.path.splitext(bin_name)[0]

        # 1. Interceptação de subcomandos e palavras-chave bloqueadas (Fail-closed principal)
        args_lower = [a.lower() for a in cmd_args[1:]]
        blocked_keywords = {"install", "exec", "npx", "clone", "fetch", "pull", "push", "submodule", "remote"}
        for kw in blocked_keywords:
            if kw in args_lower or kw == bin_base:
                raise CommandBlockedException(f"Security Block: Blocked command keyword '{kw}' detected.")

        # 2. Validar comando na allowlist
        matched_rule = None
        for rule in self.allowed_commands.values():
            if rule["bin"] == bin_base:
                args = cmd_args[1:]
                if "args_exact" in rule:
                    if args == rule["args_exact"]:
                        matched_rule = rule
                        break
                elif "args_prefix" in rule:
                    prefix = rule["args_prefix"]
                    if args[:len(prefix)] == prefix:
                        matched_rule = rule
                        break

        if not matched_rule:
            raise CommandBlockedException(f"Security Block: Command {cmd_args} is blocked by allowlist policy.")

        # Hardening Git commands
        run_args = list(cmd_args)
        if bin_base == "git":
            hooks_dir = self.sandbox_dir / ".git-hooks-disabled"
            run_args.insert(1, "-c")
            run_args.insert(2, f"core.hooksPath={hooks_dir.resolve()}")

        env = self._get_isolated_env()
        return subprocess.run(
            run_args,
            cwd=str(cwd_path),
            capture_output=True,
            text=True,
            timeout=matched_rule["timeout_seconds"],
            env=env
        )
