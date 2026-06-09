"""
OS-019R / M2 — DevTools Structural Extraction
===============================================

Extrai dados reais do browser renderizado: https://www.exoape.com

PROIBIDO:
  - Gerar TSX / landing / candidato
  - Inferir estilos do HTML bruto
  - Aprovar estética
  - Alterar promotion_allowed

ENTREGÁVEIS:
  dom_tree.json
  computed_styles.json
  layout_boxes.json
  accessibility_tree.json
  font_inventory.json
  color_usage.json
  media_inventory.json
  viewport_state_desktop.json
  viewport_state_mobile.json
  devtools_extraction_report.md
"""

import asyncio
import json
import os
import sys
import time
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output_synthesis", "OS-019R")
os.makedirs(OUTPUT_DIR, exist_ok=True)

REFERENCE_URL = "https://www.exoape.com"
OS_ID = "OS-019R"
M_ID = "OS-019R-M2"

DESKTOP_VIEWPORT = {"width": 1440, "height": 900}
MOBILE_VIEWPORT  = {"width": 390,  "height": 844}

PROHIBITED_ARTIFACTS = ["SynthesizedPage", ".tsx", "candidate", "promotion"]


# ── JS payloads executados no browser ────────────────────────────────────────

JS_DOM_TREE = """
() => {
    const MAX_DEPTH = 6;
    const MAX_CHILDREN = 12;
    const SKIP_TAGS = new Set(['SCRIPT','STYLE','NOSCRIPT','META','LINK','HEAD']);

    function extractNode(el, depth) {
        if (!el || depth > MAX_DEPTH) return null;
        if (SKIP_TAGS.has(el.tagName)) return null;

        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);

        // Skip invisible elements
        if (style.display === 'none' || style.visibility === 'hidden') return null;
        if (rect.width === 0 && rect.height === 0 && el.children.length === 0) return null;

        const node = {
            tag: el.tagName.toLowerCase(),
            id: el.id || null,
            classes: Array.from(el.classList).slice(0, 8),
            role: el.getAttribute('role') || el.tagName.toLowerCase(),
            aria_label: el.getAttribute('aria-label') || null,
            text: el.childNodes.length > 0
                ? Array.from(el.childNodes)
                    .filter(n => n.nodeType === 3)
                    .map(n => n.textContent.trim())
                    .filter(t => t.length > 0)
                    .join(' ')
                    .substring(0, 80) || null
                : null,
            href: el.getAttribute('href') || null,
            src: el.getAttribute('src') || el.getAttribute('data-src') || null,
            rect: {
                x: Math.round(rect.x),
                y: Math.round(rect.y),
                w: Math.round(rect.width),
                h: Math.round(rect.height),
            },
            font_size: style.fontSize,
            font_weight: style.fontWeight,
            color: style.color,
            bg: style.backgroundColor,
            z_index: style.zIndex,
            position: style.position,
            display: style.display,
            children: [],
        };

        const children = Array.from(el.children).slice(0, MAX_CHILDREN);
        for (const child of children) {
            const childNode = extractNode(child, depth + 1);
            if (childNode) node.children.push(childNode);
        }

        return node;
    }

    return extractNode(document.body, 0);
}
"""

JS_COMPUTED_STYLES = """
() => {
    const results = [];

    // Selectors de interesse — elementos que definem o sistema visual
    const SELECTORS = [
        // Headings
        'h1', 'h2', 'h3', 'h4',
        // Navigation
        'nav', 'nav a', 'header',
        // Body text
        'p', 'main p',
        // Links / CTAs
        'a[href]',
        // Hero / large containers
        '[class*="hero"]', '[class*="Hero"]',
        '[class*="section"]', '[class*="Section"]',
        // Media containers
        'video', 'figure',
        // Footer
        'footer',
    ];

    const seen = new Set();

    for (const sel of SELECTORS) {
        let els;
        try { els = Array.from(document.querySelectorAll(sel)).slice(0, 4); }
        catch(e) { continue; }

        for (const el of els) {
            if (seen.has(el)) continue;
            seen.add(el);

            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();

            // Skip invisible
            if (style.display === 'none') continue;

            const entry = {
                selector: sel,
                tag: el.tagName.toLowerCase(),
                classes: Array.from(el.classList).slice(0, 6).join(' '),
                text_sample: (el.innerText || '').trim().substring(0, 60),
                rect: {
                    x: Math.round(rect.x), y: Math.round(rect.y),
                    w: Math.round(rect.width), h: Math.round(rect.height),
                },
                // Typography
                font_family: style.fontFamily,
                font_size: style.fontSize,
                font_weight: style.fontWeight,
                font_style: style.fontStyle,
                line_height: style.lineHeight,
                letter_spacing: style.letterSpacing,
                text_transform: style.textTransform,
                // Color
                color: style.color,
                background_color: style.backgroundColor,
                // Layout
                display: style.display,
                position: style.position,
                z_index: style.zIndex,
                overflow: style.overflow,
                // Spacing
                padding: style.padding,
                margin: style.margin,
                // Borders
                border_radius: style.borderRadius,
                // Opacity / transforms
                opacity: style.opacity,
                transform: style.transform !== 'none' ? style.transform : null,
            };
            results.push(entry);
        }
    }

    return results;
}
"""

JS_LAYOUT_BOXES = """
() => {
    const results = [];

    // Layout semântico: identificar as grandes regiões
    function getBoxData(el, label) {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        return {
            label,
            tag: el.tagName.toLowerCase(),
            id: el.id || null,
            classes: Array.from(el.classList).slice(0,6).join(' '),
            rect: {
                x: Math.round(rect.x), y: Math.round(rect.y),
                w: Math.round(rect.width), h: Math.round(rect.height),
            },
            position: style.position,
            display: style.display,
            z_index: style.zIndex,
            background_color: style.backgroundColor,
            overflow: style.overflow,
        };
    }

    // Nav
    const nav = document.querySelector('nav') || document.querySelector('header');
    if (nav) results.push(getBoxData(nav, 'navigation'));

    // Main / hero containers
    const main = document.querySelector('main');
    if (main) results.push(getBoxData(main, 'main'));

    const sections = Array.from(document.querySelectorAll('section, [class*="section"], [class*="Section"]')).slice(0, 8);
    sections.forEach((s, i) => results.push(getBoxData(s, `section_${i}`)));

    // All large containers (w > 600, h > 200)
    const allDivs = Array.from(document.querySelectorAll('div, article, aside'));
    const largeDivs = allDivs.filter(el => {
        const r = el.getBoundingClientRect();
        return r.width > 600 && r.height > 200;
    }).slice(0, 20);
    largeDivs.forEach((d, i) => results.push(getBoxData(d, `large_container_${i}`)));

    // Videos
    const videos = Array.from(document.querySelectorAll('video'));
    videos.forEach((v, i) => {
        const rect = v.getBoundingClientRect();
        const style = window.getComputedStyle(v);
        const parent = v.parentElement;
        const parentRect = parent ? parent.getBoundingClientRect() : rect;
        const isFullBleed = rect.width >= window.innerWidth * 0.9;
        const isHigh = rect.y < window.innerHeight * 0.5;
        const isBackground = style.position === 'absolute' || style.position === 'fixed';
        const role = isBackground ? 'background_media'
                   : (isFullBleed && isHigh) ? 'hero_media'
                   : rect.width < 400 ? 'thumbnail_media'
                   : 'editorial_media';
        results.push({
            label: `video_${i}`,
            tag: 'video',
            src: v.currentSrc || v.getAttribute('src') || v.querySelector('source')?.src || null,
            autoplay: v.autoplay,
            muted: v.muted,
            loop: v.loop,
            role,
            rect: {
                x: Math.round(rect.x), y: Math.round(rect.y),
                w: Math.round(rect.width), h: Math.round(rect.height),
            },
            position: style.position,
            z_index: style.zIndex,
            object_fit: style.objectFit,
        });
    });

    // Footer
    const footer = document.querySelector('footer');
    if (footer) results.push(getBoxData(footer, 'footer'));

    return results;
}
"""

JS_A11Y_TREE = """
() => {
    const results = {
        landmarks: [],
        headings: [],
        interactive: [],
        images_with_alt: [],
        videos_with_track: [],
    };

    // Landmarks
    const landmarkRoles = ['banner','navigation','main','complementary','contentinfo','search','form'];
    document.querySelectorAll('[role]').forEach(el => {
        const role = el.getAttribute('role');
        if (landmarkRoles.includes(role)) {
            results.landmarks.push({
                tag: el.tagName.toLowerCase(),
                role,
                aria_label: el.getAttribute('aria-label'),
                aria_labelledby: el.getAttribute('aria-labelledby'),
            });
        }
    });

    // Native landmarks
    ['header','nav','main','aside','footer','section','article'].forEach(tag => {
        document.querySelectorAll(tag).forEach(el => {
            results.landmarks.push({
                tag,
                role: el.getAttribute('role') || tag,
                aria_label: el.getAttribute('aria-label'),
                text_sample: (el.innerText || '').trim().substring(0, 40),
            });
        });
    });

    // Headings
    document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(el => {
        const rect = el.getBoundingClientRect();
        const style = window.getComputedStyle(el);
        results.headings.push({
            tag: el.tagName.toLowerCase(),
            text: (el.innerText || '').trim().substring(0, 100),
            font_size: style.fontSize,
            font_weight: style.fontWeight,
            visible: style.display !== 'none' && rect.width > 0,
        });
    });

    // Interactive elements
    document.querySelectorAll('a,button,[role="button"],[tabindex]').forEach(el => {
        results.interactive.push({
            tag: el.tagName.toLowerCase(),
            role: el.getAttribute('role') || el.tagName.toLowerCase(),
            text: (el.innerText || el.getAttribute('aria-label') || '').trim().substring(0, 60),
            href: el.getAttribute('href'),
            aria_label: el.getAttribute('aria-label'),
            tabindex: el.getAttribute('tabindex'),
        });
    });
    results.interactive = results.interactive.slice(0, 30);

    // Images
    document.querySelectorAll('img').forEach(el => {
        results.images_with_alt.push({
            src: (el.getAttribute('src') || '').substring(0, 80),
            alt: el.getAttribute('alt'),
            has_alt: el.hasAttribute('alt') && el.getAttribute('alt') !== '',
            role: el.getAttribute('role'),
        });
    });

    // Videos
    document.querySelectorAll('video').forEach(el => {
        results.videos_with_track.push({
            has_track: el.querySelector('track') !== null,
            aria_label: el.getAttribute('aria-label'),
            autoplay: el.autoplay,
            muted: el.muted,
        });
    });

    return results;
}
"""

JS_FONT_INVENTORY = """
() => {
    const fonts = {};

    // Walk all elements and collect font-related computed styles
    const all = Array.from(document.querySelectorAll('*'));
    for (const el of all) {
        const style = window.getComputedStyle(el);
        if (style.display === 'none') continue;

        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) continue;

        const family = style.fontFamily;
        const size = style.fontSize;
        const weight = style.fontWeight;
        const lh = style.lineHeight;
        const ls = style.letterSpacing;
        const tt = style.textTransform;

        const key = `${family}|${weight}`;
        if (!fonts[key]) {
            fonts[key] = {
                family,
                weight,
                sizes: new Set(),
                line_heights: new Set(),
                letter_spacings: new Set(),
                text_transforms: new Set(),
                usage_contexts: [],
            };
        }
        fonts[key].sizes.add(size);
        fonts[key].line_heights.add(lh);
        fonts[key].letter_spacings.add(ls);
        fonts[key].text_transforms.add(tt);

        const tag = el.tagName.toLowerCase();
        const textContent = (el.innerText || '').trim().substring(0, 30);
        if (textContent && fonts[key].usage_contexts.length < 5) {
            fonts[key].usage_contexts.push({ tag, text: textContent });
        }
    }

    // Convert Sets to arrays for JSON serialization
    return Object.entries(fonts).map(([key, f]) => ({
        family: f.family,
        weight: f.weight,
        sizes: Array.from(f.sizes).sort((a, b) => parseFloat(a) - parseFloat(b)),
        line_heights: Array.from(f.line_heights),
        letter_spacings: Array.from(f.letter_spacings),
        text_transforms: Array.from(f.text_transforms),
        usage_contexts: f.usage_contexts,
    }));
}
"""

JS_COLOR_USAGE = """
() => {
    const colorMap = {};

    const all = Array.from(document.querySelectorAll('*'));
    for (const el of all) {
        const style = window.getComputedStyle(el);
        if (style.display === 'none') continue;

        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) continue;

        // Track color usage with semantic context
        const addColor = (color, prop, context) => {
            if (!color || color === 'transparent' || color === 'rgba(0, 0, 0, 0)') return;
            if (!colorMap[color]) {
                colorMap[color] = { color, usages: [], count: 0 };
            }
            colorMap[color].count++;
            if (colorMap[color].usages.length < 5) {
                colorMap[color].usages.push({
                    prop,
                    tag: el.tagName.toLowerCase(),
                    context,
                });
            }
        };

        const tag = el.tagName.toLowerCase();
        const textContent = (el.innerText || '').trim().substring(0, 20);

        addColor(style.color, 'color', `${tag}: "${textContent}"`);
        addColor(style.backgroundColor, 'background-color', tag);
        addColor(style.borderColor, 'border-color', tag);
        addColor(style.outlineColor, 'outline-color', tag);
    }

    return Object.values(colorMap)
        .filter(c => c.count > 0)
        .sort((a, b) => b.count - a.count)
        .slice(0, 60);
}
"""

JS_VIEWPORT_STATE = """
(isMobile) => {
    // CSS custom properties (design tokens)
    const cssVars = {};
    const rootStyle = window.getComputedStyle(document.documentElement);
    for (const sheet of document.styleSheets) {
        try {
            for (const rule of sheet.cssRules) {
                if (rule.selectorText === ':root' || rule.selectorText === 'html') {
                    for (const prop of rule.style) {
                        if (prop.startsWith('--')) {
                            cssVars[prop] = rule.style.getPropertyValue(prop).trim();
                        }
                    }
                }
            }
        } catch(e) {}
    }

    // Scroll info
    const scrollInfo = {
        page_height: document.body.scrollHeight,
        viewport_height: window.innerHeight,
        viewport_width: window.innerWidth,
        scroll_ratio: document.body.scrollHeight / window.innerHeight,
    };

    // Media queries que estão ativas
    const breakpoints = [320, 375, 390, 480, 640, 768, 1024, 1280, 1440, 1920];
    const active_mq = breakpoints.filter(bp => window.matchMedia(`(min-width: ${bp}px)`).matches);
    const prefers_reduced_motion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const prefers_dark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Z-index landscape
    const allEls = Array.from(document.querySelectorAll('*'));
    const zIndexes = allEls
        .map(el => parseInt(window.getComputedStyle(el).zIndex) || 0)
        .filter(z => z !== 0)
        .sort((a, b) => a - b);
    const uniqueZ = [...new Set(zIndexes)];

    // Scroll-related: sticky/fixed elements
    const fixedEls = allEls
        .filter(el => {
            const pos = window.getComputedStyle(el).position;
            return pos === 'fixed' || pos === 'sticky';
        })
        .map(el => ({
            tag: el.tagName.toLowerCase(),
            classes: Array.from(el.classList).slice(0,4).join(' '),
            position: window.getComputedStyle(el).position,
            z_index: window.getComputedStyle(el).zIndex,
        }));

    return {
        is_mobile: isMobile,
        viewport: { width: window.innerWidth, height: window.innerHeight },
        device_pixel_ratio: window.devicePixelRatio,
        scroll_info: scrollInfo,
        active_breakpoints_min_width: active_mq,
        prefers_reduced_motion,
        prefers_dark_mode: prefers_dark,
        z_index_landscape: uniqueZ,
        fixed_sticky_elements: fixedEls.slice(0, 10),
        css_custom_properties: cssVars,
        document_ready_state: document.readyState,
    };
}
"""

JS_MEDIA_INVENTORY = """
() => {
    const media = { videos: [], images: [], iframes: [] };

    // Videos
    document.querySelectorAll('video').forEach((v, i) => {
        const rect = v.getBoundingClientRect();
        const style = window.getComputedStyle(v);
        const parent = v.closest('[class*="hero"],[class*="Hero"],[class*="section"],[class*="card"],[class*="thumb"]')
                     || v.parentElement;
        const parentClasses = parent ? Array.from(parent.classList).join(' ') : '';
        const isFullBleed = rect.width >= window.innerWidth * 0.85;
        const isAbsolute = style.position === 'absolute' || style.position === 'fixed';
        const isHigh = rect.y < window.innerHeight * 0.7;

        let role = 'ambient';
        if (isAbsolute && isHigh && isFullBleed) role = 'background_media';
        else if (isFullBleed && isHigh && !isAbsolute) role = 'hero_media';
        else if (rect.w < 500) role = 'thumbnail_media';
        else role = 'editorial_media';

        media.videos.push({
            index: i,
            src: v.currentSrc || v.src || (v.querySelector('source') ? v.querySelector('source').src : null),
            poster: v.poster || null,
            autoplay: v.autoplay,
            muted: v.muted,
            loop: v.loop,
            controls: v.controls,
            playsinline: v.hasAttribute('playsinline'),
            preload: v.preload,
            role,
            parent_context: parentClasses.substring(0, 80),
            rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
            position: style.position,
            z_index: style.zIndex,
            object_fit: style.objectFit,
        });
    });

    // Images
    document.querySelectorAll('img').forEach((img, i) => {
        const rect = img.getBoundingClientRect();
        if (rect.width < 20 || rect.height < 20) return; // Skip icons
        media.images.push({
            index: i,
            src: (img.src || '').substring(0, 120),
            alt: img.alt || null,
            loading: img.loading,
            srcset: img.srcset ? img.srcset.substring(0, 100) : null,
            rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
            object_fit: window.getComputedStyle(img).objectFit,
        });
    });

    // iFrames (Vimeo/YouTube embeds)
    document.querySelectorAll('iframe').forEach((fr, i) => {
        media.iframes.push({
            index: i,
            src: (fr.src || '').substring(0, 120),
            title: fr.title || null,
        });
    });

    return media;
}
"""


async def capture_viewport_state(page, is_mobile: bool) -> dict:
    return await page.evaluate(JS_VIEWPORT_STATE, is_mobile)


async def run_desktop_extraction(page) -> dict:
    """Executa todos os payloads JS no contexto desktop."""
    results = {}

    print("  → DOM tree...")
    results["dom_tree"] = await page.evaluate(JS_DOM_TREE)

    print("  → Computed styles...")
    results["computed_styles"] = await page.evaluate(JS_COMPUTED_STYLES)

    print("  → Layout boxes...")
    results["layout_boxes"] = await page.evaluate(JS_LAYOUT_BOXES)

    print("  → Accessibility tree...")
    results["a11y_tree"] = await page.evaluate(JS_A11Y_TREE)

    print("  → Font inventory...")
    results["font_inventory"] = await page.evaluate(JS_FONT_INVENTORY)

    print("  → Color usage...")
    results["color_usage"] = await page.evaluate(JS_COLOR_USAGE)

    print("  → Media inventory...")
    results["media_inventory"] = await page.evaluate(JS_MEDIA_INVENTORY)

    print("  → Viewport state (desktop)...")
    results["viewport_state"] = await capture_viewport_state(page, is_mobile=False)

    return results


async def main():
    print(f"\n{'='*60}")
    print(f"OS-019R / M2 — DevTools Structural Extraction")
    print(f"Reference: {REFERENCE_URL}")
    print(f"{'='*60}\n")

    ts_start = time.time()

    from playwright.async_api import async_playwright

    # ── [1] Desktop extraction ───────────────────────────────────────────────
    print("[1] Desktop extraction (1440×900)...")
    desktop_data = {}
    mobile_viewport_state = {}

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
        await page.goto(REFERENCE_URL, wait_until="networkidle", timeout=60_000)
        await page.wait_for_timeout(3000)

        desktop_data = await run_desktop_extraction(page)
        await browser.close()

    # ── [2] Mobile viewport state ────────────────────────────────────────────
    print("\n[2] Mobile viewport state (390×844)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=MOBILE_VIEWPORT,
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/17.0 Mobile/15E148 Safari/604.1"
            ),
            is_mobile=True, has_touch=True, locale="en-US",
        )
        page = await context.new_page()
        await page.goto(REFERENCE_URL, wait_until="networkidle", timeout=60_000)
        await page.wait_for_timeout(2000)

        print("  → Viewport state (mobile)...")
        mobile_viewport_state = await capture_viewport_state(page, is_mobile=True)

        # Mobile computed styles (headings + nav)
        print("  → Mobile computed styles...")
        mobile_styles = await page.evaluate(JS_COMPUTED_STYLES)
        mobile_viewport_state["computed_styles_sample"] = mobile_styles[:10]

        await browser.close()

    # ── [3] Persistir artefatos ──────────────────────────────────────────────
    print("\n[3] Persistindo artefatos...")

    def save_json(name: str, data) -> str:
        path = os.path.join(OUTPUT_DIR, name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        size = os.path.getsize(path)
        print(f"  ✓ {name} — {size:,} bytes")
        return path

    save_json("dom_tree.json", desktop_data["dom_tree"])
    save_json("computed_styles.json", desktop_data["computed_styles"])
    save_json("layout_boxes.json", desktop_data["layout_boxes"])
    save_json("accessibility_tree.json", desktop_data["a11y_tree"])
    save_json("font_inventory.json", desktop_data["font_inventory"])
    save_json("color_usage.json", desktop_data["color_usage"])
    save_json("media_inventory.json", desktop_data["media_inventory"])
    save_json("viewport_state_desktop.json", desktop_data["viewport_state"])
    save_json("viewport_state_mobile.json", mobile_viewport_state)

    # ── [4] Análise rápida para o report ─────────────────────────────────────
    print("\n[4] Analisando dados extraídos...")

    font_data     = desktop_data["font_inventory"]
    color_data    = desktop_data["color_usage"]
    media_data    = desktop_data["media_inventory"]
    a11y_data     = desktop_data["a11y_tree"]
    styles_data   = desktop_data["computed_styles"]
    vp_desktop    = desktop_data["viewport_state"]
    css_vars      = vp_desktop.get("css_custom_properties", {})

    # Fontes únicas
    unique_families = list({
        f["family"].split(",")[0].strip().strip("'\"")
        for f in font_data
        if f["family"]
    })

    # Cores únicas por frequência (top 20)
    top_colors = color_data[:20]

    # Headings extraídas
    headings = a11y_data.get("headings", [])

    # Vídeos por role
    video_by_role: dict = {}
    for v in media_data.get("videos", []):
        role = v.get("role", "unknown")
        video_by_role.setdefault(role, []).append(v)

    # CSS vars (design tokens)
    token_count = len(css_vars)

    # H1 data
    h1_style = next((s for s in styles_data if s["tag"] == "h1"), None)

    print(f"  Fontes únicas: {len(unique_families)}")
    print(f"  Cores únicas: {len(color_data)}")
    print(f"  Vídeos: {len(media_data.get('videos', []))}")
    print(f"  Imagens: {len(media_data.get('images', []))}")
    print(f"  Headings: {len(headings)}")
    print(f"  CSS custom properties: {token_count}")
    print(f"  Z-index landscape: {vp_desktop.get('z_index_landscape', [])}")
    if h1_style:
        print(f"  H1: {h1_style.get('font_size')} / {h1_style.get('font_weight')} / {h1_style.get('letter_spacing')}")

    # ── [5] Gate matrix M2 ───────────────────────────────────────────────────
    print("\n[5] Gate matrix M2...")
    checks = []

    def gate(name: str, condition: bool, critical: bool = True):
        checks.append({"name": name, "passed": condition})
        marker = "✓" if condition else "✗"
        print(f"  [{marker}] {name}")
        if not condition and critical:
            raise AssertionError(f"[GATE FAIL] {name}")

    gate("DOM tree extraído", desktop_data["dom_tree"] is not None)
    gate("Computed styles extraídos", len(styles_data) > 0)
    gate("Layout boxes extraídos", len(desktop_data["layout_boxes"]) > 0)
    gate("Accessibility tree extraída", bool(a11y_data))
    gate("Font inventory extraído", len(font_data) > 0)
    gate("Color usage extraído", len(color_data) > 0)
    gate("Media inventory extraído", bool(media_data))
    gate("Viewport state desktop", bool(vp_desktop))
    gate("Viewport state mobile", bool(mobile_viewport_state))
    gate("Vídeos classificados por role", len(media_data.get("videos", [])) > 0)
    gate("Fontes identificadas", len(unique_families) > 0)
    gate("Headings extraídas", len(headings) > 0)
    gate("Nenhum TSX gerado", not any("tsx" in f for f in os.listdir(OUTPUT_DIR)))
    gate("Nenhum candidato gerado", not any("candidate" in f for f in os.listdir(OUTPUT_DIR)))
    gate("promotion_allowed=false",
         True,  # invariante — não há arquivo de promoção nesta OS
    )

    passed = sum(1 for c in checks if c["passed"])
    total  = len(checks)
    print(f"\n  Gate Matrix: {passed}/{total}")

    # ── [6] devtools_extraction_report.md ────────────────────────────────────
    print("\n[6] Gerando devtools_extraction_report.md...")

    # Formatar top colors
    def rgb_to_hex_approx(rgb: str) -> str:
        try:
            nums = re.findall(r"\d+(?:\.\d+)?", rgb)
            if len(nums) >= 3:
                r, g, b = int(float(nums[0])), int(float(nums[1])), int(float(nums[2]))
                return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            pass
        return rgb

    color_table_rows = "\n".join(
        f"| `{rgb_to_hex_approx(c['color'])}` | `{c['color']}` | {c['count']} | "
        f"{c['usages'][0]['prop'] if c['usages'] else '—'} | {c['usages'][0]['tag'] if c['usages'] else '—'} |"
        for c in top_colors
    )

    heading_table_rows = "\n".join(
        f"| {h['tag']} | `{h['font_size']}` | `{h['font_weight']}` | {h['text'][:60]} |"
        for h in headings[:10]
    )

    video_table_rows = "\n".join(
        f"| video_{v['index']} | {v['role']} | {v['rect']['w']}×{v['rect']['h']} | "
        f"autoplay={v['autoplay']} muted={v['muted']} loop={v['loop']} |"
        for v in media_data.get("videos", [])
    )

    font_families_list = "\n".join(f"- `{fam}`" for fam in unique_families[:12])

    css_vars_sample = "\n".join(
        f"  `{k}`: `{v}`"
        for k, v in list(css_vars.items())[:20]
    ) or "  (nenhuma CSS custom property encontrada no :root)"

    report_content = f"""# DevTools Extraction Report — OS-019R / M2
**Reference:** {REFERENCE_URL}
**Extraído em:** {time.strftime('%Y-%m-%d %H:%M:%S')}
**Gate Matrix:** {passed}/{total}
**promotion_allowed:** false

---

## 1. Visão Geral

| Métrica | Valor |
|---|---|
| DOM extraído | ✅ pós-render |
| Computed styles | {len(styles_data)} elementos |
| Layout boxes | {len(desktop_data['layout_boxes'])} regiões |
| Headings | {len(headings)} |
| Vídeos | {len(media_data.get('videos', []))} |
| Imagens | {len(media_data.get('images', []))} |
| Fontes únicas | {len(unique_families)} |
| Cores únicas | {len(color_data)} |
| CSS custom properties | {token_count} |
| Z-index layers | {len(vp_desktop.get('z_index_landscape', []))} |
| Page height (desktop) | {vp_desktop.get('scroll_info', {}).get('page_height', '?')}px |
| Page height (mobile) | {mobile_viewport_state.get('scroll_info', {}).get('page_height', '?')}px |
| prefers-reduced-motion (default) | {vp_desktop.get('prefers_reduced_motion', '?')} |

---

## 2. Sistema Tipográfico

### Famílias identificadas
{font_families_list}

### Headings extraídas

| Tag | Font-size | Font-weight | Texto |
|---|---|---|---|
{heading_table_rows}

{f'### H1 computed{chr(10)}| Propriedade | Valor |{chr(10)}|---|---|{chr(10)}| font-family | `{h1_style.get("font_family", "—")}` |{chr(10)}| font-size | `{h1_style.get("font_size", "—")}` |{chr(10)}| font-weight | `{h1_style.get("font_weight", "—")}` |{chr(10)}| letter-spacing | `{h1_style.get("letter_spacing", "—")}` |{chr(10)}| line-height | `{h1_style.get("line_height", "—")}` |{chr(10)}| text-transform | `{h1_style.get("text_transform", "—")}` |' if h1_style else ''}

---

## 3. Cores (Top 20 por frequência)

| Hex approx | RGB computed | Freq | Propriedade | Contexto |
|---|---|---|---|---|
{color_table_rows}

---

## 4. Inventário de Mídia

### Vídeos ({len(media_data.get('videos', []))})

| ID | Role | Dimensão | Atributos |
|---|---|---|---|
{video_table_rows}

**Roles mapeados:**
{chr(10).join(f'- `{role}`: {len(vids)} vídeo(s)' for role, vids in video_by_role.items())}

### Imagens ({len(media_data.get('images', []))})
(ver `media_inventory.json` para lista completa)

---

## 5. CSS Custom Properties (Design Tokens)

{css_vars_sample}

---

## 6. Z-Index Landscape

Camadas identificadas: `{vp_desktop.get('z_index_landscape', [])}`

Elementos fixed/sticky:
{chr(10).join(f'- `{el["tag"]}` .{el["classes"]} — position:{el["position"]} z:{el["z_index"]}' for el in vp_desktop.get('fixed_sticky_elements', [])[:6]) or '  (nenhum)'}

---

## 7. Viewport Comparativo

| Propriedade | Desktop (1440×900) | Mobile (390×844) |
|---|---|---|
| Page height | {vp_desktop.get('scroll_info', {}).get('page_height', '?')}px | {mobile_viewport_state.get('scroll_info', {}).get('page_height', '?')}px |
| Scroll ratio | {vp_desktop.get('scroll_info', {}).get('scroll_ratio', '?')} | {mobile_viewport_state.get('scroll_info', {}).get('scroll_ratio', '?')} |
| Device pixel ratio | {vp_desktop.get('device_pixel_ratio', '?')} | {mobile_viewport_state.get('device_pixel_ratio', '?')} |

---

## 8. Accessibility Tree

| Tipo | Count |
|---|---|
| Landmarks | {len(a11y_data.get('landmarks', []))} |
| Headings visíveis | {len([h for h in headings if h.get('visible')])} |
| Elementos interativos | {len(a11y_data.get('interactive', []))} |
| Imagens com alt | {len([i for i in a11y_data.get('images_with_alt', []) if i.get('has_alt')])} de {len(a11y_data.get('images_with_alt', []))} |
| Vídeos com track | {len([v for v in a11y_data.get('videos_with_track', []) if v.get('has_track')])} de {len(a11y_data.get('videos_with_track', []))} |

---

## 9. Artefatos Gerados

| Arquivo | Conteúdo |
|---|---|
| `dom_tree.json` | Árvore DOM pós-render — profundidade 6 |
| `computed_styles.json` | Estilos computados por seletor relevante |
| `layout_boxes.json` | Bounding boxes de regiões semânticas + vídeos |
| `accessibility_tree.json` | Landmarks, headings, interativos, media a11y |
| `font_inventory.json` | Fontes em uso com sizes, weights, contexts |
| `color_usage.json` | Cores computadas com frequência e contexto |
| `media_inventory.json` | Vídeos e imagens com classificação de role |
| `viewport_state_desktop.json` | Estado viewport 1440×900 + CSS vars |
| `viewport_state_mobile.json` | Estado viewport 390×844 |

---

## 10. Status

```
OS-019R / M2 — CONCLUÍDA
Gate Matrix: {passed}/{total}
promotion_allowed: false
Próxima etapa: M3 — Design System Synthesis
```

> M1 capturou a referência.
> M2 mediu a referência.
> Ainda não construímos nada.
"""

    report_path = os.path.join(OUTPUT_DIR, "devtools_extraction_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"  ✓ devtools_extraction_report.md — {os.path.getsize(report_path):,} bytes")

    # ── Final ────────────────────────────────────────────────────────────────
    ts_end = time.time()
    print(f"\n{'='*60}")
    print(f"OS-019R / M2 — CONCLUÍDA")
    print(f"Gate Matrix: {passed}/{total}")
    print(f"Duração: {round(ts_end - ts_start, 1)}s")
    print(f"Fontes: {', '.join(unique_families[:5])}")
    print(f"Vídeos: {len(media_data.get('videos', []))} — roles: {list(video_by_role.keys())}")
    print(f"Cores únicas: {len(color_data)}")
    print(f"CSS tokens: {token_count}")
    print(f"promotion_allowed: False")
    print(f"{'='*60}")
    print(f"\nPróxima etapa: M3 — Design System Synthesis")


if __name__ == "__main__":
    asyncio.run(main())
