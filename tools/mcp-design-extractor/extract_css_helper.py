from playwright.sync_api import sync_playwright
from pathlib import Path

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://aoricreative.com/', wait_until='networkidle')
    
    # Extrai todo CSS de todas as stylesheets acessíveis
    css_text = page.evaluate('''() => {
        let allCss = '';
        for (const sheet of Array.from(document.styleSheets)) {
            try {
                for (const rule of Array.from(sheet.cssRules || [])) {
                    allCss += rule.cssText + '\\n';
                }
            } catch (_) {}
        }
        return allCss;
    }''')
    
    out_css = Path('../../Elysian Consult/aori_computed_styles.css')
    out_css.write_text(css_text, encoding='utf-8')
    print('Total CSS Rules extracted length:', len(css_text))
    browser.close()
