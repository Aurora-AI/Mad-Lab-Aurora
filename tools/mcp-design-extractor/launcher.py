"""
launcher.py — Gerenciador de Inicialização do Navegador e Contexto Seguro
para o CDP Design System Extractor.
"""

from typing import Tuple
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from security import security_route_guard


async def create_secure_browser_context(
    playwright_instance: Playwright,
    viewport_width: int = 1440,
    viewport_height: int = 900,
) -> Tuple[Browser, BrowserContext, Page]:
    """
    Inicializa o Chromium de forma headless, configurando bloqueio de Service Workers,
    resolução em alta densidade (2x DPI) e guarda de segurança anti-SSRF em sub-recursos.
    """
    browser: Browser = await playwright_instance.chromium.launch(
        headless=True,
        args=[
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-default-apps",
        ]
    )

    context: BrowserContext = await browser.new_context(
        viewport={"width": viewport_width, "height": viewport_height},
        device_scale_factor=2,
        service_workers="block",  # Bloqueia Service Workers para impedir desvios de roteador
    )

    page: Page = await context.new_page()

    # Aplica o filtro de segurança anti-SSRF em todas as rotas secundárias
    await page.route("**/*", security_route_guard)

    return browser, context, page
