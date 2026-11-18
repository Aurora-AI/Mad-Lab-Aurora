from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 720})
    page.goto('file:///C:/Projetos/MadLabAurora/Elysian%20Consult/index.html')
    time.sleep(0.3)
    meta = page.evaluate('''() => {
        const el = document.querySelector('.pin-spacer');
        const r = el.getBoundingClientRect();
        return {
            top: window.scrollY + r.top,
            height: r.height,
            scrollable: r.height - window.innerHeight
        };
    }''')
    print('Meta:', meta)
    for pct in [0.0, 0.15, 0.35, 0.50, 0.65, 0.85, 1.0]:
        y = meta['top'] + (pct * meta['scrollable'])
        page.evaluate(f'window.scrollTo(0, {y})')
        time.sleep(0.4)
        diag = page.evaluate('window.__aoriScrollDiagnostics()')
        print(f"pct={pct:.2f} -> target={diag['target']:.3f}, progress={diag['progress']:.3f}, chapter={diag['chapter']}")
    browser.close()
