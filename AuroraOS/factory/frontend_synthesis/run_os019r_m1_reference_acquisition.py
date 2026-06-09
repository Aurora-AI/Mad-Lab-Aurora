"""
OS-019R / M1 — Reference Acquisition
=====================================

Captura read-only da referência real: https://www.exoape.com

Proibido nesta etapa:
  - Gerar TSX
  - Gerar candidato visual
  - Fazer redesign
  - Aprovar estética
  - Alterar promotion_allowed

Entregáveis:
  capture_metadata.json
  raw_html.html
  screenshot_desktop.png
  screenshot_mobile.png
  network_manifest.json
  asset_inventory.json
"""

import asyncio
import hashlib
import json
import os
import sys
import time
from urllib.parse import urlparse, urljoin

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", "OS-019R")
os.makedirs(OUTPUT_DIR, exist_ok=True)

REFERENCE_URL = "https://www.exoape.com"
OS_ID = "OS-019R"
M_ID = "OS-019R-M1"

DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
MOBILE_VIEWPORT  = {"width": 390, "height": 844}   # iPhone 14

# Gate: artefatos PROIBIDOS nesta etapa
PROHIBITED_ARTIFACTS = ["SynthesizedPage", ".tsx", "candidate", "perceptual", "promotion"]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def classify_asset(url: str, content_type: str) -> str:
    ct = (content_type or "").lower()
    u  = url.lower()
    if "font" in ct or any(u.endswith(e) for e in (".woff", ".woff2", ".ttf", ".otf")):
        return "font"
    if "css" in ct or u.endswith(".css"):
        return "css"
    if "javascript" in ct or u.endswith(".js") or u.endswith(".mjs"):
        return "script"
    if "image" in ct or any(u.endswith(e) for e in (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".avif")):
        return "image"
    if "video" in ct or any(u.endswith(e) for e in (".mp4", ".webm", ".mov")):
        return "video"
    if "html" in ct:
        return "html"
    if "json" in ct:
        return "json"
    return "other"


async def main():
    print(f"\n{'='*60}")
    print(f"OS-019R / M1 — Reference Acquisition")
    print(f"Reference: {REFERENCE_URL}")
    print(f"{'='*60}\n")

    ts_start = time.time()

    from playwright.async_api import async_playwright

    network_entries: list[dict] = []
    console_messages: list[dict] = []

    # ── [1] Desktop capture ─────────────────────────────────────────────────
    print("[1] Capturando referência — desktop (1440×900)...")

    raw_html_desktop = ""
    screenshot_desktop_bytes = b""
    page_title = ""
    meta_description = ""
    page_performance = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=DESKTOP_VIEWPORT,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="en-US",
        )
        page = await context.new_page()

        # Registrar todos os requests de rede
        def on_request(req):
            network_entries.append({
                "url": req.url,
                "method": req.method,
                "resource_type": req.resource_type,
                "content_type": None,
                "size_bytes": None,
                "category": classify_asset(req.url, req.resource_type),
            })

        async def on_response(resp):
            ct = resp.headers.get("content-type", "")
            size = None
            try:
                body = await resp.body()
                size = len(body)
            except Exception:
                pass
            # Atualizar entry correspondente
            for entry in reversed(network_entries):
                if entry["url"] == resp.url:
                    entry["content_type"] = ct
                    entry["size_bytes"] = size
                    entry["category"] = classify_asset(resp.url, ct)
                    entry["status"] = resp.status
                    break

        page.on("request", on_request)
        page.on("response", lambda r: asyncio.ensure_future(on_response(r)))

        def on_console(msg):
            if msg.type in ("error", "warning"):
                console_messages.append({"type": msg.type, "text": msg.text})
        page.on("console", on_console)

        # Navegar
        print(f"  → Navigating to {REFERENCE_URL}...")
        await page.goto(REFERENCE_URL, wait_until="networkidle", timeout=60_000)
        await page.wait_for_timeout(3000)  # Aguardar animações iniciais

        # Capturar HTML bruto
        raw_html_desktop = await page.content()

        # Metadados da página
        page_title = await page.title()
        meta_description = await page.evaluate(
            "() => document.querySelector('meta[name=\"description\"]')?.content || ''"
        )

        # Performance timing
        page_performance = await page.evaluate("""() => {
            const nav = performance.getEntriesByType('navigation')[0] || {};
            return {
                dom_content_loaded: Math.round(nav.domContentLoadedEventEnd || 0),
                load_complete: Math.round(nav.loadEventEnd || 0),
                first_paint: Math.round(
                    (performance.getEntriesByName('first-paint')[0] || {}).startTime || 0
                ),
                first_contentful_paint: Math.round(
                    (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || 0
                ),
            };
        }""")

        # Screenshot desktop
        screenshot_desktop_bytes = await page.screenshot(full_page=True)
        print(f"  ✓ Desktop screenshot: {len(screenshot_desktop_bytes):,} bytes")

        await browser.close()

    # ── [2] Mobile capture ──────────────────────────────────────────────────
    print("\n[2] Capturando referência — mobile (390×844)...")
    screenshot_mobile_bytes = b""

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=MOBILE_VIEWPORT,
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            is_mobile=True,
            has_touch=True,
            locale="en-US",
        )
        page = await context.new_page()
        await page.goto(REFERENCE_URL, wait_until="networkidle", timeout=60_000)
        await page.wait_for_timeout(3000)
        screenshot_mobile_bytes = await page.screenshot(full_page=True)
        print(f"  ✓ Mobile screenshot: {len(screenshot_mobile_bytes):,} bytes")
        await browser.close()

    # ── [3] Persistir artefatos ─────────────────────────────────────────────
    print("\n[3] Persistindo artefatos...")

    # raw_html.html
    html_path = os.path.join(OUTPUT_DIR, "raw_html.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(raw_html_desktop)
    html_sha = sha256_text(raw_html_desktop)
    print(f"  ✓ raw_html.html — {len(raw_html_desktop):,} chars — SHA256: {html_sha[:16]}...")

    # screenshot_desktop.png
    desktop_path = os.path.join(OUTPUT_DIR, "screenshot_desktop.png")
    with open(desktop_path, "wb") as f:
        f.write(screenshot_desktop_bytes)
    desktop_sha = sha256_bytes(screenshot_desktop_bytes)
    print(f"  ✓ screenshot_desktop.png — {len(screenshot_desktop_bytes):,} bytes — SHA256: {desktop_sha[:16]}...")

    # screenshot_mobile.png
    mobile_path = os.path.join(OUTPUT_DIR, "screenshot_mobile.png")
    with open(mobile_path, "wb") as f:
        f.write(screenshot_mobile_bytes)
    mobile_sha = sha256_bytes(screenshot_mobile_bytes)
    print(f"  ✓ screenshot_mobile.png — {len(screenshot_mobile_bytes):,} bytes — SHA256: {mobile_sha[:16]}...")

    # ── [4] Network manifest ─────────────────────────────────────────────────
    print("\n[4] Construindo network manifest...")

    # Deduplicar por URL
    seen_urls: set[str] = set()
    unique_entries = []
    for e in network_entries:
        if e["url"] not in seen_urls:
            seen_urls.add(e["url"])
            unique_entries.append(e)

    # Classificar
    by_category: dict[str, list] = {}
    for e in unique_entries:
        cat = e.get("category", "other")
        by_category.setdefault(cat, []).append(e)

    network_manifest = {
        "reference_url": REFERENCE_URL,
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_requests": len(unique_entries),
        "by_category": {k: len(v) for k, v in by_category.items()},
        "fonts": [
            {"url": e["url"], "content_type": e.get("content_type"), "size_bytes": e.get("size_bytes")}
            for e in by_category.get("font", [])
        ],
        "css_files": [
            {"url": e["url"], "size_bytes": e.get("size_bytes")}
            for e in by_category.get("css", [])
        ],
        "scripts": [
            {"url": e["url"], "size_bytes": e.get("size_bytes")}
            for e in by_category.get("script", [])
        ],
        "images": [
            {"url": e["url"], "content_type": e.get("content_type"), "size_bytes": e.get("size_bytes")}
            for e in by_category.get("image", [])
        ],
        "videos": [
            {"url": e["url"], "content_type": e.get("content_type")}
            for e in by_category.get("video", [])
        ],
        "all_requests": unique_entries,
    }

    net_path = os.path.join(OUTPUT_DIR, "network_manifest.json")
    with open(net_path, "w", encoding="utf-8") as f:
        json.dump(network_manifest, f, indent=2, ensure_ascii=False)
    print(f"  ✓ network_manifest.json — {len(unique_entries)} requests únicos")
    print(f"    fonts: {len(network_manifest['fonts'])}")
    print(f"    css:   {len(network_manifest['css_files'])}")
    print(f"    js:    {len(network_manifest['scripts'])}")
    print(f"    imgs:  {len(network_manifest['images'])}")
    print(f"    video: {len(network_manifest['videos'])}")

    # ── [5] Asset inventory ──────────────────────────────────────────────────
    print("\n[5] Construindo asset inventory...")

    # Extrair font-face declarations do HTML
    import re
    font_face_urls = re.findall(r"url\(['\"]?(https?://[^'\")\s]+\.(?:woff2?|ttf|otf))['\"]?\)", raw_html_desktop)
    font_face_families = re.findall(r"font-family:\s*['\"]?([^'\";\n]+)['\"]?", raw_html_desktop)

    # Extrair links de fontes do Google/CDN
    cdn_font_links = re.findall(
        r'href=["\']([^"\']*(?:fonts\.googleapis|fonts\.gstatic|use\.typekit)[^"\']*)["\']',
        raw_html_desktop
    )

    # Inventário de imagens
    img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', raw_html_desktop)
    bg_images = re.findall(r'url\(["\']([^"\']+\.(png|jpg|jpeg|svg|webp|gif|avif))["\']?\)', raw_html_desktop)

    asset_inventory = {
        "reference_url": REFERENCE_URL,
        "page_title": page_title,
        "meta_description": meta_description,
        "fonts": {
            "cdn_links": cdn_font_links,
            "woff_urls": list(set(font_face_urls)),
            "family_declarations": list(set(f.strip() for f in font_face_families if len(f.strip()) > 1))[:20],
            "network_fonts": [
                {"url": e["url"], "size_bytes": e.get("size_bytes")}
                for e in by_category.get("font", [])
            ],
        },
        "images": {
            "img_tags": list(set(img_srcs))[:50],
            "background_images": [bg[0] for bg in bg_images][:30],
            "network_images": [
                {"url": e["url"], "content_type": e.get("content_type"), "size_bytes": e.get("size_bytes")}
                for e in by_category.get("image", [])
            ],
        },
        "videos": [
            {"url": e["url"], "content_type": e.get("content_type")}
            for e in by_category.get("video", [])
        ],
        "scripts_count": len(by_category.get("script", [])),
        "css_count": len(by_category.get("css", [])),
        "total_assets": len(unique_entries),
    }

    inv_path = os.path.join(OUTPUT_DIR, "asset_inventory.json")
    with open(inv_path, "w", encoding="utf-8") as f:
        json.dump(asset_inventory, f, indent=2, ensure_ascii=False)
    print(f"  ✓ asset_inventory.json")
    print(f"    font CDN links: {len(cdn_font_links)}")
    print(f"    font families declared: {len(asset_inventory['fonts']['family_declarations'])}")
    print(f"    images: {len(asset_inventory['images']['network_images'])}")
    print(f"    videos: {len(asset_inventory['videos'])}")

    # ── [6] Anti-stub gate ───────────────────────────────────────────────────
    print("\n[6] Anti-stub gate...")
    for prohibited in PROHIBITED_ARTIFACTS:
        for fname in os.listdir(OUTPUT_DIR):
            assert prohibited not in fname, (
                f"[GATE FAIL] Artefato proibido detectado: {fname} contém '{prohibited}'"
            )
    print(f"  ✓ Nenhum artefato proibido gerado")

    # ── [7] Gate matrix M1 ───────────────────────────────────────────────────
    print("\n[7] Gate matrix M1...")
    checks = []

    def gate(name: str, condition: bool):
        checks.append({"name": name, "passed": condition})
        marker = "✓" if condition else "✗"
        print(f"  [{marker}] {name}")
        if not condition:
            raise AssertionError(f"[GATE FAIL] {name}")

    gate("Reference URL declarada", bool(REFERENCE_URL))
    gate("HTML bruto capturado", len(raw_html_desktop) > 1000)
    gate("Screenshot desktop gerado", len(screenshot_desktop_bytes) > 10_000)
    gate("Screenshot mobile gerado", len(screenshot_mobile_bytes) > 10_000)
    gate("Network manifest gerado", os.path.exists(net_path))
    gate("Asset inventory gerado", os.path.exists(inv_path))
    gate("Font data capturado", len(network_manifest["fonts"]) > 0 or len(cdn_font_links) > 0)
    gate("Nenhum TSX gerado", not any("tsx" in f for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum candidato gerado", not any("candidate" in f for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum artefato de promoção", not any("promotion" in f for f in os.listdir(OUTPUT_DIR)))
    gate("Page title capturado", bool(page_title))
    gate("HTML > 10KB", len(raw_html_desktop.encode("utf-8")) > 10_000)

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    print(f"\n  Gate Matrix: {passed}/{total}")

    # ── [8] capture_metadata.json ────────────────────────────────────────────
    print("\n[8] Escrevendo capture_metadata.json...")
    ts_end = time.time()

    capture_metadata = {
        "os_id": OS_ID,
        "m_id": M_ID,
        "reference_url": REFERENCE_URL,
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "capture_duration_s": round(ts_end - ts_start, 2),
        "page_title": page_title,
        "meta_description": meta_description,
        "performance": page_performance,
        "desktop_viewport": DESKTOP_VIEWPORT,
        "mobile_viewport": MOBILE_VIEWPORT,
        "artifacts": {
            "raw_html.html":            {"sha256": html_sha,    "size_chars": len(raw_html_desktop)},
            "screenshot_desktop.png":   {"sha256": desktop_sha, "size_bytes": len(screenshot_desktop_bytes)},
            "screenshot_mobile.png":    {"sha256": mobile_sha,  "size_bytes": len(screenshot_mobile_bytes)},
            "network_manifest.json":    {"requests": len(unique_entries)},
            "asset_inventory.json":     {"assets": len(unique_entries)},
        },
        "summary": {
            "total_requests": len(unique_entries),
            "fonts_detected": len(network_manifest["fonts"]) + len(cdn_font_links),
            "images_detected": len(by_category.get("image", [])),
            "videos_detected": len(by_category.get("video", [])),
            "css_files": len(by_category.get("css", [])),
            "scripts": len(by_category.get("script", [])),
            "console_errors": len([m for m in console_messages if m["type"] == "error"]),
        },
        "gate_matrix": {"passed": passed, "total": total},
        "mode": "read-only capture",
        "promotion_allowed": False,
        "next_step": "M2 — DevTools Structural Extraction",
    }

    meta_path = os.path.join(OUTPUT_DIR, "capture_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(capture_metadata, f, indent=2, ensure_ascii=False)

    print(f"  ✓ capture_metadata.json")
    print(f"\n{'='*60}")
    print(f"OS-019R / M1 — CONCLUÍDA")
    print(f"Gate Matrix: {passed}/{total}")
    print(f"Duração: {round(ts_end - ts_start, 1)}s")
    print(f"Referência: {REFERENCE_URL}")
    print(f"Título: {page_title}")
    print(f"HTML: {len(raw_html_desktop):,} chars")
    print(f"Requests capturados: {len(unique_entries)}")
    print(f"promotion_allowed: False")
    print(f"{'='*60}\n")
    print(f"Próxima etapa: M2 — DevTools Structural Extraction")


if __name__ == "__main__":
    asyncio.run(main())
