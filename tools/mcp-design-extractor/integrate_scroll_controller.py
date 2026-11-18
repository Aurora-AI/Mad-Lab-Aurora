import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
target_html_path = ROOT_DIR / "Elysian Consult" / "index.html"
soup = BeautifulSoup(target_html_path.read_text(encoding="utf-8"), "html.parser")

runtime_css_path = ROOT_DIR / "Elysian Consult" / "temp_aori_scroll" / "aori_scroll_runtime.css"
runtime_js_path = ROOT_DIR / "Elysian Consult" / "temp_aori_scroll" / "aori_scroll_runtime.js"

runtime_css = runtime_css_path.read_text(encoding="utf-8")
runtime_js = runtime_js_path.read_text(encoding="utf-8")

# 1. Injeta runtime_css inline no head
style_tag = soup.new_tag("style")
style_tag["data-aori-scroll-style"] = "true"
style_tag.string = runtime_css
soup.head.append(style_tag)

# 2. Injeta runtime_js no fim do body
script_tag = soup.new_tag("script")
script_tag["data-aori-scroll-script"] = "true"
script_tag.string = runtime_js
soup.body.append(script_tag)

# 3. Garante que html não tenha intro-on travando o scroll e tenha aori-motion-ready
html_tag = soup.find("html")
if html_tag:
    classes = html_tag.get("class", [])
    if isinstance(classes, str):
        classes = classes.split()
    classes = [c for c in classes if c not in ("intro-on", "intro")]
    if "aori-motion-ready" not in classes:
        classes.append("aori-motion-ready")
    html_tag["class"] = classes

# Salva arquivo atualizado
target_html_path.write_text(str(soup), encoding="utf-8")
print(f"Scroll controller integrado com sucesso em: {target_html_path}")
