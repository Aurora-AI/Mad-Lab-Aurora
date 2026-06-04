import os
import sys
import logging
import json
from playwright.async_api import async_playwright

sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts'))
])

from factory_contracts import StandaloneRenderBundle, UINode

logger = logging.getLogger("RendererAdapter")

class LocalOfflineRendererAdapter:
    def __init__(self, sandbox_dir: str):
        self.sandbox_dir = sandbox_dir

    async def render_and_screenshot(self, bundle: StandaloneRenderBundle) -> dict:
        # 1. Validar que os caminhos físicos existem e que as restrições contratuais são respeitadas
        if bundle.dependencies_mode != "local_pinned":
            raise ValueError("Violação de Contrato: StandaloneRenderBundle deve usar dependencies_mode = 'local_pinned'.")
        if bundle.network_allowed is not False:
            raise ValueError("Violação de Contrato: StandaloneRenderBundle deve ter network_allowed = False.")

        client_path = os.path.join(self.sandbox_dir, bundle.client_component_path)
        page_path = os.path.join(self.sandbox_dir, bundle.page_entry_path)
        ui_tree_path = os.path.join(self.sandbox_dir, "ui_tree.json")

        if not os.path.exists(client_path):
            raise FileNotFoundError(f"Candidato em falta no sandbox: {client_path}")
        if not os.path.exists(page_path):
            raise FileNotFoundError(f"Candidato em falta no sandbox: {page_path}")
        if not os.path.exists(ui_tree_path):
            raise FileNotFoundError(f"Candidato em falta no sandbox: {ui_tree_path}")

        # Ler CSS físico
        css_code = ""
        if bundle.css_entry_path:
            css_path = os.path.join(self.sandbox_dir, bundle.css_entry_path)
            if not os.path.exists(css_path):
                raise FileNotFoundError(f"Estilos em falta no sandbox: {css_path}")
            with open(css_path, "r", encoding="utf-8") as f:
                css_code = f.read()

        # Reconstruir UINode tree a partir de ui_tree.json para compilação HTML
        with open(ui_tree_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
            root_node = UINode(**tree_data["root_node"])

        # Extrair cores do CSS para compilação HTML precisa
        import re
        theme_colors = {}
        if css_code:
            matches = re.findall(r"\.(text|bg)-([\w-]+)\s*\{\s*(color|background-color):\s*(#[0-9a-fA-F]{3,6})\s*;\s*\}", css_code)
            for prefix, name, prop, val in matches:
                theme_colors[name] = val

        from tsx_compiler import _compile_html_node
        html_fallback = _compile_html_node(root_node, theme_colors=theme_colors)

        # 2. Cria o wrapper HTML isolado
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Renderer {bundle.bundle_id}</title>
            <style>
                body {{ margin: 0; padding: 0; }}
                {css_code}
            </style>
        </head>
        <body>
            <div id="root">
                {html_fallback}
            </div>
        </body>
        </html>
        """
        
        # 3. Grava offline no sandbox
        html_path = os.path.join(self.sandbox_dir, f"render_{bundle.bundle_id}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        screenshot_path = os.path.join(self.sandbox_dir, "6_rendered_screenshot.png")

        console_errors = []
        network_requests_blocked = []
        page_errors = []

        # 4. Executa Playwright (Fail-Closed block)
        try:
            viewport_str = bundle.viewport_presets[0] if bundle.viewport_presets else "1440x900"
            w, h = map(int, viewport_str.split("x"))
            viewport = {"width": w, "height": h}
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    offline=True, # STRICT OFFLINE MODE
                    viewport=viewport
                )
                page = await context.new_page()
                
                # Listen to console messages and extract errors
                def on_console(msg):
                    if msg.type == "error":
                        console_errors.append(msg.text)
                page.on("console", on_console)

                # Listen to page unhandled exceptions
                def on_page_error(error):
                    logger.error(f"Render Page Error: {error}")
                    page_errors.append(str(error))
                page.on("pageerror", on_page_error)

                # Listen to requests to detect network leaks
                def on_request(request):
                    url = request.url
                    if url.startswith("http://") or url.startswith("https://"):
                        logger.error(f"Fuga de rede detectada e bloqueada: {url}")
                        network_requests_blocked.append(url)
                page.on("request", on_request)

                file_url = f"file:///{os.path.abspath(html_path).replace(chr(92), '/')}"
                await page.goto(file_url, wait_until="load")
                
                # Extrair estilos computados reais dos elementos com texto direto
                text_elements_style = await page.evaluate("""() => {
                    const elements = Array.from(document.querySelectorAll('*'));
                    const list = [];
                    elements.forEach(el => {
                        const hasDirectText = Array.from(el.childNodes).some(node => node.nodeType === 3 && node.textContent.trim().length > 0);
                        if (hasDirectText) {
                            const style = window.getComputedStyle(el);
                            let bgEl = el;
                            let bgColor = 'rgba(0, 0, 0, 0)';
                            while (bgEl) {
                                const resolvedBg = window.getComputedStyle(bgEl).backgroundColor;
                                if (resolvedBg !== 'rgba(0, 0, 0, 0)' && resolvedBg !== 'transparent' && !resolvedBg.endsWith(', 0)')) {
                                    bgColor = resolvedBg;
                                    break;
                                }
                                bgEl = bgEl.parentElement;
                            }
                            list.push({
                                tagName: el.tagName,
                                id: el.id,
                                className: el.className,
                                color: style.color,
                                backgroundColor: bgColor,
                                fontSize: style.fontSize,
                                fontWeight: style.fontWeight,
                                textContent: el.textContent.trim().substring(0, 30)
                            });
                        }
                    });
                    return list;
                }""")

                # Extract all inner text for AntiStubGate
                rendered_text = await page.evaluate("() => document.body.innerText")

                await page.screenshot(path=screenshot_path, full_page=True)
                await browser.close()
                
        except Exception as e:
            logger.error(f"Playwright falhou ou falha de render: {e}")
            raise RuntimeError(f"RendererAdapter failure: {e}")

        return {
            "screenshot_path": screenshot_path,
            "console_errors": console_errors,
            "network_requests_blocked": network_requests_blocked,
            "page_errors": page_errors,
            "text_elements_style": text_elements_style,
            "rendered_text": rendered_text
        }


