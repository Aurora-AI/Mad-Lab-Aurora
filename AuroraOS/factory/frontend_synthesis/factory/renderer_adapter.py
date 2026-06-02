import os
import sys
import logging
from playwright.async_api import async_playwright

sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts'))
])

from factory_contracts import StandaloneRenderBundle

logger = logging.getLogger("RendererAdapter")

class LocalOfflineRendererAdapter:
    def __init__(self, sandbox_dir: str):
        self.sandbox_dir = sandbox_dir

    async def render_and_screenshot(self, bundle: StandaloneRenderBundle) -> str:
        # 1. Cria o wrapper HTML isolado
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Renderer {bundle.bundle_id}</title>
            <style>
                body {{ margin: 0; padding: 0; }}
                {bundle.css_code}
            </style>
        </head>
        <body>
            <div id="root">
                {bundle.html_fallback}
            </div>
        </body>
        </html>
        """
        
        # 2. Grava offline no sandbox
        html_path = os.path.join(self.sandbox_dir, f"render_{bundle.bundle_id}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        screenshot_path = os.path.join(self.sandbox_dir, "6_rendered_screenshot.png")

        # 3. Executa Playwright (Fail-Closed block)
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                # Bloqueia network externa
                context = await browser.new_context(
                    offline=True, # STRICT OFFLINE MODE
                    viewport=bundle.viewport
                )
                page = await context.new_page()
                
                # Fail se console error crítico
                def on_page_error(error):
                    logger.error(f"Render Error: {error}")
                    raise RuntimeError(f"Console Render Error: {error}")
                    
                page.on("pageerror", on_page_error)

                # Carrega o ficheiro local
                file_url = f"file:///{os.path.abspath(html_path).replace(chr(92), '/')}"
                await page.goto(file_url, wait_until="load")
                
                await page.screenshot(path=screenshot_path, full_page=True)
                await browser.close()
                
        except Exception as e:
            logger.error(f"Playwright falhou ou falha de render: {e}")
            raise RuntimeError(f"RendererAdapter failure: {e}")

        return screenshot_path
