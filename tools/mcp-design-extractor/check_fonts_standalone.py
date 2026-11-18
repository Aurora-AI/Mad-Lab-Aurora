from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('file:///C:/Projetos/MadLabAurora/Elysian%20Consult/aori_transplanted_landing.html')
    body_font = page.evaluate('window.getComputedStyle(document.body).fontFamily')
    print('Body font:', body_font)
    p_fonts = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('p')).slice(0, 5).map(p => ({
            tag: p.tagName,
            cls: p.className,
            font: window.getComputedStyle(p).fontFamily,
            text: p.textContent.slice(0, 30)
        }));
    }''')
    for pf in p_fonts:
        print(pf)
    browser.close()
