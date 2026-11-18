from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://aoricreative.com/', wait_until='networkidle')
    page.wait_for_timeout(4000)
    html_cls = page.evaluate('document.documentElement.className')
    print('HTML classes after 4s:', html_cls)
    has_intro = page.evaluate('Boolean(document.querySelector(".intro-stage"))')
    print('Has .intro-stage:', has_intro)
    if has_intro:
        disp = page.evaluate('window.getComputedStyle(document.querySelector(".intro-stage")).display')
        opac = page.evaluate('window.getComputedStyle(document.querySelector(".intro-stage")).opacity')
        print('intro-stage display:', disp, 'opacity:', opac)
    browser.close()
