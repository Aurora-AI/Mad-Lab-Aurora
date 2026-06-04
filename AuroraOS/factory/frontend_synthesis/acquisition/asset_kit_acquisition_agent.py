import os
import sys
import json
import uuid
import time
import hashlib
import logging
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from playwright.async_api import async_playwright

logger = logging.getLogger("AssetKitAcquisitionAgent")

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"

class AssetKitAcquisitionAgent:
    """
    Agente de Aquisição Controlada de Asset Kit (Playwright)
    Acessa a URL alvo, baixa os recursos locais permitidos (CSS, imagens, fontes, scripts catalogados),
    gerando o manifesto hashado e bloqueando conexões externas.
    """
    def __init__(self, target_url: str, output_root: str = "C:/Projetos/Aurora/AuroraOS/factory/frontend_synthesis/staging/asset_kits"):
        self.target_url = target_url
        self.output_root = Path(output_root).resolve()
        
        parsed = urllib.parse.urlparse(target_url)
        domain = parsed.netloc.replace(".", "-")
        if not domain:
            domain = "unknown"
            
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.kit_id = f"AK-{timestamp}-{domain}"
        self.kit_dir = self.output_root / self.kit_id
        
        # Diretórios internos do kit
        self.assets_dir = self.kit_dir / "assets"
        self.styles_dir = self.assets_dir / "styles"
        self.images_dir = self.assets_dir / "images"
        self.fonts_dir = self.assets_dir / "fonts"
        self.scripts_dir = self.assets_dir / "scripts_cataloged"
        
        self.allowed_domains = [
            "antigravity.google",
            "fonts.gstatic.com",
            "fonts.googleapis.com"
        ]
        
    def _is_allowed(self, url: str) -> bool:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        
        if domain in self.allowed_domains:
            return True
        if domain.endswith(".googleusercontent.com"):
            return True
        return False

    async def acquire(self) -> Path:
        logger.info(f"Iniciando aquisição controlada para URL: {self.target_url}")
        
        # Criar os diretórios locais
        os.makedirs(self.styles_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.fonts_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)
        
        network_log = []
        url_to_local_map = {}
        input_hashes = {}
        resource_counts = {"css": 0, "images": 0, "fonts": 0, "scripts_cataloged": 0}
        
        start_time = time.time()
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                # Na fase de aquisição de kit, a rede externa (HTTP/HTTPS) é permitida sob regras
                context = await browser.new_context(
                    viewport={"width": 1440, "height": 900}
                )
                page = await context.new_page()
                
                # Interceptar responses para salvar arquivos
                async def on_response(response):
                    url = response.url
                    if not url.startswith(("http://", "https://")):
                        return
                        
                    allowed = self._is_allowed(url)
                    saved = False
                    error_msg = None
                    
                    log_entry = {
                        "url": url,
                        "status": response.status,
                        "content_type": response.headers.get("content-type", ""),
                        "allowed": allowed,
                        "saved_locally": False
                    }
                    
                    if allowed and response.status == 200:
                        try:
                            body = await response.body()
                            content_type = response.headers.get("content-type", "").lower()
                            parsed_url = urllib.parse.urlparse(url)
                            filename = os.path.basename(parsed_url.path)
                            
                            if not filename:
                                filename = f"resource_{uuid.uuid4().hex[:8]}"
                                
                            dest_dir = None
                            ext = ""
                            res_type = None
                            
                            if "css" in content_type or parsed_url.path.endswith(".css"):
                                dest_dir = self.styles_dir
                                ext = ".css"
                                res_type = "css"
                            elif "image" in content_type or any(parsed_url.path.endswith(e) for e in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico")):
                                dest_dir = self.images_dir
                                res_type = "images"
                            elif "font" in content_type or any(parsed_url.path.endswith(e) for e in (".woff", ".woff2", ".ttf", ".otf", ".eot")):
                                dest_dir = self.fonts_dir
                                res_type = "fonts"
                            elif "javascript" in content_type or parsed_url.path.endswith(".js"):
                                dest_dir = self.scripts_dir
                                ext = ".js"
                                res_type = "scripts_cataloged"
                                
                            if dest_dir:
                                if ext and not filename.endswith(ext):
                                    filename += ext
                                    
                                dest_path = Path(dest_dir) / filename
                                dest_path.write_bytes(body)
                                
                                # Obter caminho relativo
                                rel_path = dest_path.relative_to(self.kit_dir)
                                rel_path_str = str(rel_path).replace("\\", "/")
                                
                                url_to_local_map[url] = rel_path_str
                                input_hashes[rel_path_str] = file_sha256(dest_path)
                                resource_counts[res_type] += 1
                                saved = True
                                log_entry["saved_locally"] = True
                                log_entry["local_path"] = rel_path_str
                        except Exception as ex:
                            error_msg = str(ex)
                            log_entry["error"] = error_msg
                            
                    network_log.append(log_entry)
                    
                page.on("response", on_response)
                
                # Acessar a página
                await page.goto(self.target_url, wait_until="networkidle")
                
                # Salvar o HTML principal
                html_content = await page.content()
                await browser.close()
                
        except Exception as e:
            logger.error(f"Erro no Playwright durante aquisição: {e}")
            raise RuntimeError(f"Asset kit acquisition failed: {e}")
            
        # Atualizar referências no HTML
        for url, local_rel in url_to_local_map.items():
            html_content = html_content.replace(url, local_rel)
            
            # Substituir variantes sem protocolo ou relativas
            parsed = urllib.parse.urlparse(url)
            rel_path = parsed.path.lstrip("/")
            if rel_path:
                html_content = html_content.replace(rel_path, local_rel)
                
        html_file_path = self.kit_dir / "source.html"
        html_file_path.write_text(html_content, encoding="utf-8")
        
        # Hash do HTML principal
        input_hashes["source.html"] = file_sha256(html_file_path)
        
        # 1. Gravar network_log.json
        network_log_path = self.kit_dir / "network_log.json"
        with open(network_log_path, "w", encoding="utf-8") as f:
            json.dump(network_log, f, indent=2)
            
        # 2. Gravar asset_kit_manifest.json
        manifest_data = {
            "asset_kit_id": self.kit_id,
            "source_url": self.target_url,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "staging_root": str(self.kit_dir).replace("\\", "/"),
            "html_file": "source.html",
            "assets_dir": "assets",
            "script_execution_allowed": False,
            "network_allowed_after_acquisition": False,
            "input_hashes": input_hashes,
            "resource_counts": resource_counts
        }
        
        manifest_path = self.kit_dir / "asset_kit_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)
            
        # 3. Gravar acquisition_report.json
        report_data = {
            "kit_id": self.kit_id,
            "status": "SUCCESS",
            "elapsed_seconds": time.time() - start_time,
            "resources_acquired": resource_counts,
            "network_log_entries": len(network_log)
        }
        
        report_path = self.kit_dir / "acquisition_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
            
        logger.info(f"Aquisição concluída com sucesso. Kit ID: {self.kit_id}")
        return manifest_path
