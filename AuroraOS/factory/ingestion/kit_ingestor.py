import os
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser
from typing import Dict, List, Optional

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend_synthesis/contracts')))
from models import AssetKitArtifact

class KitParserException(Exception):
    pass

class SafeHTMLParser(HTMLParser):
    def __init__(self, base_dir: Path):
        super().__init__()
        self.base_dir = base_dir
        self.assets_found: List[str] = []
        self.remote_resources: List[str] = []
        self.scripts_cataloged: List[str] = []

    def handle_starttag(self, tag, attrs):
        # Capturamos apenas as referências estáticas. NÃO EXECUTAMOS.
        attr_dict = dict(attrs)
        
        if tag == 'script':
            src = attr_dict.get('src', '<inline script>')
            self.scripts_cataloged.append(src)
            return
            
        target_attr = 'href' if tag in ('link', 'a') else 'src'
        if target_attr in attr_dict:
            val = attr_dict[target_attr]
            # Ignorar URLs externos ou data URIs
            if val.startswith(('http://', 'https://', '//')):
                self.remote_resources.append(val)
            elif val.startswith('data:'):
                pass
            else:
                self.assets_found.append(val)

class KitIngestor:
    """
    Ingestor Estático do Asset Kit (OS-009).
    - Parsing via regex/html.parser, sem execução de código
    - Validação de manifest `asset_kit_manifest.json`
    - Prevenção de Path Traversal
    """
    
    def __init__(self, staging_dir: Path, kit_name: str = "Google Antigravity"):
        self.staging_dir = staging_dir.resolve()
        self.kit_name = kit_name
        self.manifest_file = self.staging_dir / "asset_kit_manifest.json"
        
        # Tenta ler do manifesto dinamicamente
        html_name = f"{kit_name}.html"
        assets_dir_name = f"{kit_name}_files"
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, 'r', encoding='utf-8') as f:
                    manifest_data = json.load(f)
                html_name = manifest_data.get("html_file", html_name)
                assets_dir_name = manifest_data.get("assets_dir", assets_dir_name)
            except Exception:
                pass
                
        self.html_file = self.staging_dir / html_name
        self.files_dir = self.staging_dir / assets_dir_name

    def _validate_path_security(self, file_path: Path) -> Path:
        resolved = file_path.resolve()
        try:
            if not resolved.is_relative_to(self.staging_dir):
                raise KitParserException(f"Violação de Segurança: Tentativa de path traversal bloqueada: {file_path}")
        except AttributeError:
            pass
        return resolved

    def _verify_manifest(self) -> dict:
        manifest_path = self.manifest_file
        try:
            safe_path = self._validate_path_security(manifest_path)
            if not safe_path.exists():
                raise KitParserException(f"Mandatory asset_kit_manifest.json missing in {self.staging_dir}")
            
            with open(safe_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise KitParserException(f"asset_kit_manifest.json inválido: {e}")
        except FileNotFoundError:
            raise KitParserException(f"Mandatory asset_kit_manifest.json missing in {self.staging_dir}")

    def ingest(self) -> AssetKitArtifact:
        manifest = self._verify_manifest()
        
        html_path = self.html_file
        try:
            safe_html_path = self._validate_path_security(html_path)
            if not safe_html_path.exists():
                raise KitParserException(f"Main HTML file {html_path.name} missing.")
        except FileNotFoundError:
            raise KitParserException(f"Main HTML file {html_path.name} missing.")
            
        import hashlib
        
        def compute_hash(p: Path) -> str:
            return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else ""
            
        html_hash = compute_hash(safe_html_path)
        css_hashes = {}
        asset_hashes = {}
        css_vars = {}
        breakpoints = {}
        font_declarations = []
        asset_paths = {}

        # 1. Parsing estático do HTML
        html_parser = SafeHTMLParser(self.staging_dir)
        with open(safe_html_path, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
        html_parser.feed(html_content)

        # 2. Cataloga Assets seguros
        for relative_path in html_parser.assets_found:
            asset_full_path = self.staging_dir / relative_path
            try:
                safe_path = self._validate_path_security(asset_full_path)
                if safe_path.exists():
                    asset_paths[relative_path] = str(safe_path)
                    asset_hashes[relative_path] = compute_hash(safe_path)
                else:
                    # Se faltar, registramos o missing path (poderá virar P2 no truth_resolver)
                    pass
            except KitParserException:
                pass # Ignora violações de traversal e não cataloga

        # 3. Parsing estático dos arquivos CSS
        if self.files_dir.exists():
            safe_files_dir = self._validate_path_security(self.files_dir)
            for css_file in safe_files_dir.rglob("*.css"):
                safe_css_path = self._validate_path_security(css_file)
                css_hashes[css_file.name] = compute_hash(safe_css_path)
                self._extract_css_tokens(safe_css_path, css_vars, breakpoints, font_declarations)
                
        return AssetKitArtifact(
            source_path=str(self.staging_dir),
            extracted_at=datetime.now(timezone.utc),
            css_variables=css_vars,
            breakpoints=breakpoints,
            font_declarations=font_declarations,
            asset_paths=asset_paths,
            html_hash=html_hash,
            css_hashes=css_hashes,
            asset_hashes=asset_hashes,
            remote_resources=html_parser.remote_resources,
            scripts_cataloged=html_parser.scripts_cataloged
        )
        
    def _extract_css_tokens(self, css_path: Path, css_vars: dict, breakpoints: dict, font_decls: list):
        with open(css_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Remover comentários CSS
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Extrair Variáveis CSS (--palette-* e --theme-*)
        var_pattern = re.compile(r'(--(?:palette|theme)-[\w-]+)\s*:\s*([^;]+);')
        for match in var_pattern.finditer(content):
            css_vars[match.group(1)] = match.group(2).strip()
            
        # Extrair Breakpoints (@media)
        mq_pattern = re.compile(r'@media\s+([^{]+)\{')
        for i, match in enumerate(mq_pattern.finditer(content)):
            mq_rule = match.group(1).strip()
            breakpoints[f"breakpoint_{len(breakpoints)}"] = mq_rule
            
        # Extrair Famílias de Fontes
        font_pattern = re.compile(r'font-family\s*:\s*([^;\}]+)')
        for match in font_pattern.finditer(content):
            font_val = match.group(1).strip().replace("'", '"')
            if font_val not in font_decls:
                font_decls.append(font_val)
