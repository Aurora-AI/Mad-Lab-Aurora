#!/usr/bin/env python3
"""
server.py — Servidor FastMCP para o Google Antigravity IDE:
DevTools (CDP) Design System Extractor.
Conecta o agente de IA diretamente ao Chrome DevTools Protocol (CDP) via Playwright.
"""

import asyncio
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from playwright.async_api import CDPSession, Page, async_playwright

from launcher import create_secure_browser_context
from security import sanitize_css_value, sanitize_text, validate_url

mcp = FastMCP("antigravity-devtools-design-extractor")

TRACKED_INTERACTIVE_PROPS: List[str] = [
    "backgroundColor",
    "backgroundImage",
    "color",
    "borderColor",
    "boxShadow",
    "transform",
    "opacity",
    "filter",
    "backdropFilter",
]

WEBGL_INTERCEPTOR_INIT_SCRIPT: str = """
(() => {
    window.__AG_CAPTURED_SHADERS__ = [];
    window.__AG_CANVAS_CONTEXTS__ = [];

    const hookShaderSource = (Proto, contextVersion) => {
        if (!Proto || !Proto.shaderSource) return;
        const origShaderSource = Proto.shaderSource;
        const origGetUniformLocation = Proto.getUniformLocation;

        Proto.shaderSource = function(shader, source) {
            try {
                const typeEnum = this.getShaderParameter(shader, this.SHADER_TYPE);
                const shaderType = (typeEnum === this.VERTEX_SHADER) ? 'VERTEX_SHADER' :
                                   (typeEnum === this.FRAGMENT_SHADER ? 'FRAGMENT_SHADER' : 'UNKNOWN');
                window.__AG_CAPTURED_SHADERS__.push({
                    context: contextVersion,
                    type: shaderType,
                    source: String(source),
                    capturedAt: Date.now()
                });
            } catch (_) {}
            return origShaderSource.apply(this, arguments);
        };

        if (origGetUniformLocation) {
            Proto.getUniformLocation = function(program, name) {
                try {
                    window.__AG_CANVAS_CONTEXTS__.push({
                        context: contextVersion,
                        uniformName: String(name)
                    });
                } catch (_) {}
                return origGetUniformLocation.apply(this, arguments);
            };
        }
    };

    if (typeof WebGLRenderingContext !== 'undefined') {
        hookShaderSource(WebGLRenderingContext.prototype, 'webgl1');
    }
    if (typeof WebGL2RenderingContext !== 'undefined') {
        hookShaderSource(WebGL2RenderingContext.prototype, 'webgl2');
    }
})();
"""

# ---------------------------------------------------------------------------
# OS-20261020-CDP-STRUCTURAL-CLONE — ME-01 (tipografia por papel + font assets)
# e ME-02 (section blueprints com slots + filtros SVG vinculados ao CSS).
# Content-agnostic: nós de texto viram {{SLOT_*}}, <img>/<video> perdem a mídia
# proprietária, <script>/<iframe>/handlers são descartados na origem.
# ---------------------------------------------------------------------------
STRUCTURAL_CLONE_SCRIPT: str = r"""
() => {
    const HAND_RE = /(hand|script|caveat|brush|marker|cursive|scribble|kalam|pacifico|dancing|satisfy|sacramento|indie flower|shadows into light|permanent marker|homemade)/i;
    const MONO_RE = /(mono|code|courier|consolas|menlo|monaco)/i;
    const firstFamily = (stack) => (stack || '').split(',')[0].replace(/['"]/g, '').trim();
    const isHandStack = (stack) => {
        const fams = (stack || '').split(',').map((f) => f.replace(/['"]/g, '').trim().toLowerCase());
        return fams.includes('cursive') || fams.includes('fantasy') || HAND_RE.test(fams[0] || '');
    };
    const isMonoStack = (stack) => {
        const fams = (stack || '').split(',').map((f) => f.replace(/['"]/g, '').trim().toLowerCase());
        return fams.includes('monospace') || MONO_RE.test(fams[0] || '');
    };
    const isRotated = (cs) => {
        const t = cs.transform;
        if (!t || t === 'none') return false;
        const m = t.match(/matrix\(([^)]+)\)/);
        if (!m) return /rotate/.test(t);
        const p = m[1].split(',').map(Number);
        return Math.abs(p[1]) > 0.01 || Math.abs(p[2]) > 0.01;
    };
    const visible = (el, cs) => {
        const r = el.getBoundingClientRect();
        return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0;
    };
    const directText = (el) => Array.from(el.childNodes)
        .filter((n) => n.nodeType === Node.TEXT_NODE)
        .map((n) => n.textContent.trim()).join(' ').trim();

    // ---------------- ME-01: estatística tipográfica ----------------
    const fam = new Map();
    const famEntry = (stack) => {
        const key = firstFamily(stack);
        if (!fam.has(key)) {
            fam.set(key, { family: key, stack, totalChars: 0, bodyChars: 0, displayArea: 0, monoHits: 0,
                rotatedHits: 0, hand: isHandStack(stack), mono: isMonoStack(stack), displaySample: null });
        }
        return fam.get(key);
    };
    const BODY_TAGS = new Set(['P', 'LI', 'TD', 'DD', 'BLOCKQUOTE', 'ARTICLE', 'FIGCAPTION']);
    let bodyCharsTotal = 0;
    for (const el of Array.from(document.querySelectorAll('body *'))) {
        const txt = directText(el);
        if (!txt) continue;
        const cs = window.getComputedStyle(el);
        if (!visible(el, cs)) continue;
        const e = famEntry(cs.fontFamily);
        const chars = txt.length;
        e.totalChars += chars;
        const inBody = BODY_TAGS.has(el.tagName) || (el.closest('p, li, td, dd, blockquote, article') !== null);
        if (inBody) { e.bodyChars += chars; bodyCharsTotal += chars; }
        const fs = parseFloat(cs.fontSize);
        const isDisplayCandidate = el.matches('h1, h2, [class*="hero"], [class*="title"]') ||
            el.closest('h1, h2') !== null;
        if (isDisplayCandidate && fs >= 28) {
            const r = el.getBoundingClientRect();
            const area = r.width * r.height;
            e.displayArea += area;
            if (!e.displaySample || fs > parseFloat(e.displaySample.fontSize)) {
                const lhPx = parseFloat(cs.lineHeight);
                e.displaySample = {
                    fontSize: cs.fontSize, fontWeight: cs.fontWeight, letterSpacing: cs.letterSpacing,
                    lineHeight: cs.lineHeight, lineHeightRatio: isNaN(lhPx) ? null : +(lhPx / fs).toFixed(3),
                    textTransform: cs.textTransform, tag: el.tagName.toLowerCase()
                };
            }
        }
        if (el.matches('code, pre, kbd, samp, [class*="mono"], [class*="badge"], th') || el.closest('code, pre, kbd')) {
            e.monoHits += chars;
        }
        if (isRotated(cs) || (el.parentElement && isRotated(window.getComputedStyle(el.parentElement)))) {
            if (fs <= 40) e.rotatedHits += chars;
        }
    }
    const entries = Array.from(fam.values());
    const pick = (arr, score) => arr.filter((x) => score(x) > 0).sort((a, b) => score(b) - score(a))[0] || null;
    const totalChars = entries.reduce((s, e) => s + e.totalChars, 0) || 1;

    // body: proibido cursive/fantasy; exige >= 10% do texto corrido (ou do total se não houver texto corrido)
    const bodyBase = bodyCharsTotal > 0 ? bodyCharsTotal : totalChars;
    const bodyScore = (e) => {
        if (e.hand) return 0;
        const share = (bodyCharsTotal > 0 ? e.bodyChars : e.totalChars) / bodyBase;
        return share >= 0.10 ? share : 0;
    };
    const bodyPick = pick(entries, bodyScore);
    const displayPick = pick(entries.filter((e) => !e.hand || entries.every((x) => x.hand)), (e) => e.displayArea);
    const handPick = pick(entries, (e) => (e.hand ? e.totalChars + 1 : 0)) || pick(entries.filter((e) => e !== bodyPick && e !== displayPick), (e) => e.rotatedHits);
    const monoPick = pick(entries, (e) => (e.mono ? e.totalChars + 1 : 0)) || pick(entries.filter((e) => e !== bodyPick && !e.hand), (e) => e.monoHits);

    const role = (e, reason) => e ? {
        family: e.family, stack: e.stack, generic_hand: e.hand, total_chars: e.totalChars,
        body_share: +(e.bodyChars / (bodyCharsTotal || 1)).toFixed(3), sample: e.displaySample, reason
    } : null;
    const typography_roles = {
        display: role(displayPick, 'h1/h2/hero/title >= 28px ponderado por área'),
        body: role(bodyPick, 'maior parcela de texto corrido (p, li, td, article), cursive/fantasy bloqueados, >= 10%'),
        accent_hand: role(handPick, 'cursive/handwriting ou elementos pequenos rotacionados'),
        mono: role(monoPick, 'code, pre, kbd, [class*=mono], [class*=badge], th'),
        census: entries.sort((a, b) => b.totalChars - a.totalChars).slice(0, 12).map((e) => ({
            family: e.family, total_chars: e.totalChars, body_chars: e.bodyChars, hand: e.hand, mono: e.mono,
            display_area: Math.round(e.displayArea), rotated_chars: e.rotatedHits
        }))
    };

    // ---------------- ME-01: font assets ----------------
    const stylesheet_links = Array.from(document.querySelectorAll('link[rel~="stylesheet"][href], link[rel="preload"][as="font"][href]'))
        .map((l) => ({ href: l.href, rel: l.rel, as: l.getAttribute('as') || '' }))
        .filter((l) => /font/i.test(l.href) || l.as === 'font')
        .slice(0, 20);
    const font_faces = [];
    const absolutize = (css, base) => css.replace(/url\(\s*(['"]?)([^'")]+)\1\s*\)/g, (m, q, u) => {
        try { return `url("${new URL(u, base).href}")`; } catch (_) { return m; }
    });
    const walkRules = (rules, base) => {
        for (const rule of Array.from(rules || [])) {
            if (font_faces.length >= 40) return;
            if (rule.type === CSSRule.FONT_FACE_RULE) {
                font_faces.push({
                    family: (rule.style.getPropertyValue('font-family') || '').replace(/['"]/g, '').trim(),
                    weight: rule.style.getPropertyValue('font-weight') || '',
                    style: rule.style.getPropertyValue('font-style') || '',
                    src: absolutize(rule.style.getPropertyValue('src') || '', base),
                    display: rule.style.getPropertyValue('font-display') || ''
                });
            } else if (rule.cssRules) {
                walkRules(rule.cssRules, base);
            }
        }
    };
    for (const sheet of Array.from(document.styleSheets)) {
        try { walkRules(sheet.cssRules, sheet.href || location.href); } catch (_) { /* cross-origin sem CORS */ }
    }
    const font_assets = { stylesheet_links, font_faces };

    // ---------------- ME-02: filtros SVG ativos ----------------
    const filterRuleSelectors = new Map();
    const scanFilterRules = (rules) => {
        for (const rule of Array.from(rules || [])) {
            if (rule.type === CSSRule.STYLE_RULE && rule.style) {
                const f = rule.style.getPropertyValue('filter') + ' ' + rule.style.getPropertyValue('-webkit-filter');
                const m = f.match(/url\(\s*['"]?#([^'")]+)['"]?\s*\)/g);
                if (m) m.forEach((u) => {
                    const id = u.replace(/^url\(\s*['"]?#/, '').replace(/['"]?\s*\)$/, '');
                    if (!filterRuleSelectors.has(id)) filterRuleSelectors.set(id, []);
                    filterRuleSelectors.get(id).push({ selector: rule.selectorText, filter: f.trim() });
                });
            } else if (rule.cssRules) {
                scanFilterRules(rule.cssRules);
            }
        }
    };
    for (const sheet of Array.from(document.styleSheets)) {
        try { scanFilterRules(sheet.cssRules); } catch (_) {}
    }
    const allEls = Array.from(document.querySelectorAll('body *'));
    const active_svg_filters = Array.from(document.querySelectorAll('svg filter[id]')).slice(0, 20).map((f) => {
        const id = f.id;
        const applied = [];
        for (const el of allEls) {
            if (applied.length >= 8) break;
            const cs = window.getComputedStyle(el);
            const inline = el.getAttribute('filter') || '';
            if ((cs.filter && cs.filter.includes('#' + id)) || inline.includes('#' + id)) {
                const r = el.getBoundingClientRect();
                applied.push({
                    tag: el.tagName.toLowerCase(),
                    computed_filter: cs.filter,
                    via_attribute: inline.includes('#' + id),
                    width: Math.round(r.width), height: Math.round(r.height)
                });
            }
        }
        return {
            id,
            markup: f.outerHTML.slice(0, 6000),
            primitives: Array.from(f.children).map((c) => c.tagName),
            css_rules: filterRuleSelectors.get(id) || [],
            applied_elements: applied,
            is_active: applied.length > 0 || (filterRuleSelectors.get(id) || []).length > 0
        };
    });

    // ---------------- ME-02: section blueprints ----------------
    const vw = window.innerWidth;
    const effectiveBg = (el) => {
        let n = el;
        while (n && n !== document.documentElement) {
            const c = window.getComputedStyle(n).backgroundColor;
            if (c && c !== 'transparent' && c !== 'rgba(0, 0, 0, 0)') return c;
            n = n.parentElement;
        }
        const htmlBg = window.getComputedStyle(document.documentElement).backgroundColor;
        return htmlBg && htmlBg !== 'rgba(0, 0, 0, 0)' ? htmlBg : 'rgb(255, 255, 255)';
    };
    const isSectionLike = (el) => {
        const r = el.getBoundingClientRect();
        const cs = window.getComputedStyle(el);
        return r.width >= vw * 0.6 && r.height >= 120 && cs.display !== 'none' && cs.position !== 'fixed';
    };
    let candidates = Array.from(document.querySelectorAll('header, footer, section, main > *, body > div > *, body > div > div > *'))
        .filter(isSectionLike);
    // remove aninhados: mantém o ancestral mais externo que ainda é "section-like" porém não é wrapper de página inteira
    const pageH = document.documentElement.scrollHeight;
    candidates = candidates.filter((el) => el.getBoundingClientRect().height < pageH * 0.85 || el.tagName === 'SECTION');
    candidates = candidates.filter((el) => !candidates.some((o) => o !== el && o.contains(el) && o.getBoundingClientRect().height < pageH * 0.85));
    candidates = Array.from(new Set(candidates)).sort((a, b) =>
        (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1).slice(0, 14);

    const STYLE_WHITELIST = ['display', 'gridTemplateColumns', 'gridTemplateRows', 'gridColumn', 'flexDirection', 'flexWrap',
        'justifyContent', 'alignItems', 'gap', 'padding', 'margin', 'maxWidth', 'fontFamily', 'fontSize', 'fontWeight',
        'lineHeight', 'letterSpacing', 'textTransform', 'textAlign', 'color', 'backgroundColor', 'backgroundImage',
        'borderTop', 'borderRight', 'borderBottom', 'borderLeft', 'borderRadius', 'boxShadow', 'transform', 'filter',
        'mixBlendMode', 'backdropFilter', 'opacity', 'position', 'top', 'left', 'right', 'bottom', 'zIndex', 'width', 'aspectRatio'];
    const kebab = (s) => s.replace(/[A-Z]/g, (m) => '-' + m.toLowerCase());
    const DEFAULTS = { margin: '0px', padding: '0px', opacity: '1', transform: 'none', filter: 'none', mixBlendMode: 'normal',
        backdropFilter: 'none', boxShadow: 'none', backgroundImage: 'none', position: 'static', zIndex: 'auto', textTransform: 'none',
        letterSpacing: 'normal', gap: 'normal', borderRadius: '0px', top: 'auto', left: 'auto', right: 'auto', bottom: 'auto',
        gridTemplateColumns: 'none', gridTemplateRows: 'none', gridColumn: 'auto', aspectRatio: 'auto', maxWidth: 'none' };
    const inlineStyleFor = (el, isRoot) => {
        const cs = window.getComputedStyle(el);
        const out = [];
        for (const p of STYLE_WHITELIST) {
            let v = cs[p];
            if (!v || v === DEFAULTS[p]) continue;
            if (p.startsWith('border') && p !== 'borderRadius' && /^0px/.test(v)) continue;
            if (p === 'width') { if (isRoot) continue; const r = el.getBoundingClientRect(); v = Math.round(r.width) + 'px'; }
            if (p === 'backgroundImage' && /url\(/.test(v)) continue;  // mídia proprietária fora
            if (p === 'display' && v === 'inline') continue;
            out.push(`${kebab(p)}: ${v}`);
        }
        return out.join('; ');
    };
    const slotFor = (el, txt) => {
        const cs = window.getComputedStyle(el);
        if (isHandStack(cs.fontFamily) || isRotated(cs)) return 'SLOT_ANNOTATION';
        if (el.closest('a, button')) return 'SLOT_CTA';
        if (el.closest('h1')) return 'SLOT_HEADLINE';
        if (el.closest('h2, h3, h4')) return 'SLOT_TITLE';
        const fs = parseFloat(cs.fontSize);
        if ((cs.textTransform === 'uppercase' || txt.split(/\s+/).length <= 3) && fs <= 15) return 'SLOT_EYEBROW';
        if (/^[\d.,%+x$€R]+$/.test(txt.replace(/\s/g, ''))) return 'SLOT_METRIC';
        if (fs >= 18 && txt.length > 60) return 'SLOT_LEAD';
        return 'SLOT_BODY';
    };
    const DROP_TAGS = new Set(['SCRIPT', 'STYLE', 'IFRAME', 'OBJECT', 'EMBED', 'NOSCRIPT', 'LINK', 'META', 'TEMPLATE', 'CANVAS', 'VIDEO', 'AUDIO', 'SOURCE', 'FORM', 'INPUT', 'TEXTAREA', 'SELECT']);
    const cloneSkeleton = (root, maxNodes) => {
        let count = 0;
        const build = (orig, isRoot) => {
            if (count >= maxNodes) return null;
            if (DROP_TAGS.has(orig.tagName)) return null;
            const cs = window.getComputedStyle(orig);
            if (cs.display === 'none') return null;
            count++;
            const tag = orig.tagName.toLowerCase();
            const svgNs = orig.namespaceURI === 'http://www.w3.org/2000/svg';
            const node = svgNs ? document.createElementNS('http://www.w3.org/2000/svg', tag) : document.createElement(tag === 'img' ? 'div' : tag);
            if (svgNs) {
                for (const a of ['viewBox', 'd', 'fill', 'stroke', 'stroke-width', 'width', 'height', 'cx', 'cy', 'r', 'x', 'y', 'points', 'transform']) {
                    if (orig.hasAttribute(a)) node.setAttribute(a, orig.getAttribute(a));
                }
            } else {
                node.setAttribute('style', inlineStyleFor(orig, isRoot));
                const cls = typeof orig.className === 'string' ? orig.className.trim() : '';
                if (cls) node.setAttribute('data-ref-class', cls.slice(0, 120));
                if (tag === 'img') {
                    const r = orig.getBoundingClientRect();
                    node.setAttribute('data-slot', 'SLOT_MEDIA');
                    node.setAttribute('style', node.getAttribute('style') + `; aspect-ratio: ${Math.round(r.width)} / ${Math.max(1, Math.round(r.height))}`);
                    node.textContent = '{{SLOT_MEDIA}}';
                    return node;
                }
            }
            for (const child of Array.from(orig.childNodes)) {
                if (child.nodeType === Node.TEXT_NODE) {
                    const t = child.textContent.trim();
                    if (t) {
                        const slot = slotFor(orig, t);
                        node.appendChild(document.createTextNode(`{{${slot}}}`));
                        if (!svgNs && !node.hasAttribute('data-slot')) node.setAttribute('data-slot', slot);
                    }
                } else if (child.nodeType === Node.ELEMENT_NODE) {
                    const c = build(child, false);
                    if (c) node.appendChild(c);
                }
            }
            return node;
        };
        const out = build(root, true);
        return out ? out.outerHTML : '';
    };
    const findLayoutCore = (sec) => {
        const queue = [sec];
        while (queue.length) {
            const n = queue.shift();
            const cs = window.getComputedStyle(n);
            const kids = Array.from(n.children).filter((k) => { const r = k.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
            if ((cs.display.includes('grid') || cs.display.includes('flex')) && kids.length >= 2) return n;
            queue.push(...Array.from(n.children));
            if (queue.length > 400) break;
        }
        return sec;
    };
    const section_blueprints = candidates.map((sec, idx) => {
        const cs = window.getComputedStyle(sec);
        const core = findLayoutCore(sec);
        const ccs = window.getComputedStyle(core);
        const items = Array.from(core.children).filter((k) => { const r = k.getBoundingClientRect(); return r.width > 0 && r.height > 0; });
        const representative = items.slice().sort((a, b) => b.querySelectorAll('*').length - a.querySelectorAll('*').length)[0] || core;
        const r = sec.getBoundingClientRect();
        return {
            index: idx,
            tag: sec.tagName.toLowerCase(),
            ref_class: (typeof sec.className === 'string' ? sec.className : '').slice(0, 120),
            height_px: Math.round(r.height),
            background_token: effectiveBg(sec),
            background_image: /gradient/.test(cs.backgroundImage) ? cs.backgroundImage : 'none',
            text_token: cs.color,
            padding: cs.padding,
            border: `${cs.borderTopWidth} ${cs.borderTopStyle} ${cs.borderTopColor}`,
            layout_mode: ccs.display.includes('grid') ? 'grid' : (ccs.display.includes('flex') ? 'flex' : 'block'),
            grid_template_columns: ccs.gridTemplateColumns,
            flex_direction: ccs.flexDirection,
            gap: ccs.gap,
            item_count: items.length,
            item_widths_px: items.slice(0, 8).map((k) => Math.round(k.getBoundingClientRect().width)),
            structural_template_html: cloneSkeleton(representative, 60).slice(0, 12000),
            section_skeleton_html: cloneSkeleton(sec, 120).slice(0, 20000)
        };
    });

    return { typography_roles, font_assets, section_blueprints, active_svg_filters };
}
"""


@dataclass
class ComponentInteractionDelta:
    selector: str
    tag: str
    resting_state: Dict[str, str]
    hover_delta: Dict[str, Dict[str, str]]
    focus_delta: Dict[str, Dict[str, str]]
    transition_physics: str


@dataclass
class CDPDesignTelemetry:
    schema_version: str
    capture_id: str
    source_url: str
    extracted_at_utc: str
    dom_sha256: str
    css_custom_properties: Dict[str, str]
    color_palette: Dict[str, List[Dict[str, Any]]]
    typography_scale: List[Dict[str, Any]]
    surfaces_and_shadows: List[Dict[str, str]]
    easing_curves: List[str]
    keyframes: List[Dict[str, Any]]
    interactive_deltas: List[ComponentInteractionDelta]
    # OS-20261020-CDP-STRUCTURAL-CLONE (aditivo ao schema cdp.telemetry.v1)
    typography_roles: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    font_assets: Dict[str, List[Dict[str, str]]] = field(default_factory=dict)
    section_blueprints: List[Dict[str, Any]] = field(default_factory=list)
    active_svg_filters: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ComponentVisualPair:
    index: int
    selector: str
    tag: str
    bounding_box: Dict[str, float]
    resting_screenshot_path: str
    hover_screenshot_path: str


@dataclass
class VisualAndShaderTelemetry:
    schema_version: str
    capture_id: str
    source_url: str
    captured_at_utc: str
    webgl_supported: bool
    webgl_shaders: List[Dict[str, Any]]
    detected_uniforms: List[str]
    canvas_metadata: List[Dict[str, Any]]
    svg_filters_and_masks: List[Dict[str, str]]
    component_visual_pairs: List[ComponentVisualPair]


class CDPExtractorEngine:
    def __init__(self, url: str, viewport_width: int = 1440, viewport_height: int = 900) -> None:
        self.url = validate_url(url)
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

    async def execute_telemetry_extraction(self) -> CDPDesignTelemetry:
        async with async_playwright() as p:
            browser, context, page = await create_secure_browser_context(
                p, self.viewport_width, self.viewport_height
            )
            cdp: CDPSession = await context.new_cdp_session(page)
            await cdp.send("DOM.enable")
            await cdp.send("CSS.enable")
            await cdp.send("Animation.enable")

            cdp_easings: List[str] = []

            def on_animation_created(event: Dict[str, Any]) -> None:
                source = event.get("animation", {}).get("source", {})
                easing = source.get("easing")
                if easing and easing not in ("linear", "ease"):
                    cdp_easings.append(easing)

            cdp.on("Animation.animationCreated", on_animation_created)

            await page.goto(self.url, wait_until="networkidle", timeout=30000)
            await page.evaluate("() => document.fonts.ready")
            await self._trigger_scroll_lifecycle(page)

            dom_content = await page.content()
            dom_hash = hashlib.sha256(dom_content.encode("utf-8")).hexdigest()
            now_iso = datetime.now(timezone.utc).isoformat()
            capture_id = f"cap_{dom_hash[:12]}_{int(datetime.now(timezone.utc).timestamp())}"

            cssom_payload = await self._extract_cssom_and_computed(page)
            # Estrutural ANTES do probe de pseudo-estados para não capturar estados forçados
            structural_payload = await self._extract_structural_clone(page)
            interactive_deltas = await self._probe_pseudo_states(page, cdp)

            await browser.close()

            merged_easings = sorted(list(set(cssom_payload["easing_curves"] + cdp_easings)))

            return CDPDesignTelemetry(
                schema_version="cdp.telemetry.v1",
                capture_id=capture_id,
                source_url=self.url,
                extracted_at_utc=now_iso,
                dom_sha256=dom_hash,
                css_custom_properties=cssom_payload["css_variables"],
                color_palette=cssom_payload["color_palette"],
                typography_scale=cssom_payload["typography_scale"],
                surfaces_and_shadows=cssom_payload["surfaces_and_shadows"],
                easing_curves=merged_easings,
                keyframes=cssom_payload["keyframes"],
                interactive_deltas=interactive_deltas,
                typography_roles=structural_payload["typography_roles"],
                font_assets=structural_payload["font_assets"],
                section_blueprints=structural_payload["section_blueprints"],
                active_svg_filters=structural_payload["active_svg_filters"],
            )

    async def execute_visual_and_shader_capture(
        self, assets_dir: Path, max_components: int = 8
    ) -> VisualAndShaderTelemetry:
        assets_dir.mkdir(parents=True, exist_ok=True)
        async with async_playwright() as p:
            browser, context, page = await create_secure_browser_context(
                p, self.viewport_width, self.viewport_height
            )
            # Injeta interceptor de WebGL1 e WebGL2 antes de qualquer script da página
            await context.add_init_script(WEBGL_INTERCEPTOR_INIT_SCRIPT)

            cdp: CDPSession = await context.new_cdp_session(page)
            await cdp.send("DOM.enable")
            await cdp.send("CSS.enable")
            await cdp.send("Page.enable")

            await page.goto(self.url, wait_until="networkidle", timeout=30000)
            await page.evaluate("() => document.fonts.ready")
            await self._trigger_scroll_lifecycle(page)

            dom_content = await page.content()
            dom_hash = hashlib.sha256(dom_content.encode("utf-8")).hexdigest()
            capture_id = f"cap_{dom_hash[:12]}_{int(datetime.now(timezone.utc).timestamp())}"

            shader_and_canvas_data = await page.evaluate(
                """() => {
                    const uniqueShaders = [];
                    const seenSources = new Set();
                    for (const item of (window.__AG_CAPTURED_SHADERS__ || [])) {
                        const key = `${item.context}|${item.type}|${item.source.trim()}`;
                        if (!seenSources.has(key)) {
                            seenSources.add(key);
                            uniqueShaders.push(item);
                        }
                    }
                    const uniforms = Array.from(
                        new Set((window.__AG_CANVAS_CONTEXTS__ || []).map((u) => u.uniformName))
                    );
                    const canvases = Array.from(document.querySelectorAll('canvas')).map((c, idx) => {
                        const r = c.getBoundingClientRect();
                        const cs = window.getComputedStyle(c);
                        return {
                            index: idx,
                            id: c.id || null,
                            width: c.width,
                            height: c.height,
                            cssWidth: r.width,
                            cssHeight: r.height,
                            position: cs.position,
                            zIndex: cs.zIndex,
                            opacity: cs.opacity
                        };
                    });
                    const svgFilters = Array.from(
                        document.querySelectorAll('svg filter, svg mask, svg linearGradient, svg radialGradient')
                    ).slice(0, 15).map((el) => ({
                        tag: el.tagName,
                        id: el.id || 'anonymous',
                        outerHTML: el.outerHTML.slice(0, 1500)
                    }));
                    return {
                        shaders: uniqueShaders,
                        uniforms,
                        canvases,
                        svgFilters
                    };
                }"""
            )

            visual_pairs = await self._capture_component_pairs(page, cdp, assets_dir, max_components)
            await browser.close()

            has_shaders = len(shader_and_canvas_data["shaders"]) > 0 or len(shader_and_canvas_data["canvases"]) > 0

            return VisualAndShaderTelemetry(
                schema_version="cdp.shaders.v1",
                capture_id=capture_id,
                source_url=self.url,
                captured_at_utc=datetime.now(timezone.utc).isoformat(),
                webgl_supported=has_shaders,
                webgl_shaders=shader_and_canvas_data["shaders"],
                detected_uniforms=shader_and_canvas_data["uniforms"],
                canvas_metadata=shader_and_canvas_data["canvases"],
                svg_filters_and_masks=shader_and_canvas_data["svgFilters"],
                component_visual_pairs=visual_pairs,
            )

    async def _trigger_scroll_lifecycle(self, page: Page) -> None:
        await page.evaluate(
            """async () => {
                const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
                const step = Math.max(400, Math.floor(window.innerHeight * 0.75));
                const maxScroll = Math.min(document.body.scrollHeight, window.innerHeight * 4);
                for (let y = 0; y <= maxScroll; y += step) {
                    window.scrollTo({ top: y, behavior: 'instant' });
                    await sleep(80);
                }
                window.scrollTo({ top: 0, behavior: 'instant' });
                await sleep(100);
            }"""
        )

    async def _extract_cssom_and_computed(self, page: Page) -> Dict[str, Any]:
        return await page.evaluate(
            """() => {
                const cssVariables = {};
                const keyframes = [];
                const easingSet = new Set();

                for (const sheet of Array.from(document.styleSheets)) {
                    let rules;
                    try {
                        rules = sheet.cssRules || sheet.rules;
                    } catch (_) {
                        continue;
                    }
                    if (!rules) continue;
                    for (const rule of Array.from(rules)) {
                        if (rule.type === CSSRule.STYLE_RULE && rule.style) {
                            for (let i = 0; i < rule.style.length; i++) {
                                const prop = rule.style[i];
                                if (prop.startsWith('--')) {
                                    cssVariables[prop] = rule.style.getPropertyValue(prop).trim();
                                }
                            }
                        } else if (rule.type === CSSRule.KEYFRAMES_RULE) {
                            const steps = [];
                            for (const frame of Array.from(rule.cssRules)) {
                                steps.push({ offset: frame.keyText, declarations: frame.style.cssText });
                            }
                            keyframes.push({ name: rule.name, steps });
                        }
                    }
                }

                const bgMap = new Map();
                const textMap = new Map();
                const borderMap = new Map();
                const typographyMap = new Map();
                const surfacesAndShadows = [];
                const seenSurfaceSigs = new Set();

                const isVisibleColor = (val) => val && val !== 'transparent' && val !== 'rgba(0, 0, 0, 0)';
                const countColor = (map, val) => {
                    if (isVisibleColor(val)) {
                        map.set(val, (map.get(val) || 0) + 1);
                    }
                };

                for (const el of Array.from(document.querySelectorAll('body *'))) {
                    const rect = el.getBoundingClientRect();
                    if (rect.width < 4 || rect.height < 4) continue;
                    const cs = window.getComputedStyle(el);
                    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;

                    countColor(bgMap, cs.backgroundColor);
                    countColor(textMap, cs.color);
                    if (parseFloat(cs.borderTopWidth) > 0) {
                        countColor(borderMap, cs.borderTopColor);
                    }

                    if (cs.transitionTimingFunction && cs.transitionTimingFunction !== 'ease') {
                        cs.transitionTimingFunction.split(/,(?![^(]*\\))/).forEach((fn) => {
                            const cleaned = fn.trim();
                            if (cleaned && cleaned !== 'ease' && cleaned !== 'linear') {
                                easingSet.add(cleaned);
                            }
                        });
                    }

                    const hasDirectText = Array.from(el.childNodes).some(
                        (n) => n.nodeType === Node.TEXT_NODE && n.textContent.trim().length > 0
                    );
                    if (hasDirectText) {
                        const primaryFont = cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim();
                        const sig = `${primaryFont}|${cs.fontSize}|${cs.fontWeight}|${cs.letterSpacing}`;
                        if (!typographyMap.has(sig)) {
                            typographyMap.set(sig, {
                                sampleTag: el.tagName.toLowerCase(),
                                fontFamily: cs.fontFamily,
                                fontSize: cs.fontSize,
                                fontWeight: cs.fontWeight,
                                lineHeight: cs.lineHeight,
                                letterSpacing: cs.letterSpacing
                            });
                        }
                    }

                    const hasShadow = cs.boxShadow && cs.boxShadow !== 'none';
                    const backdrop = cs.backdropFilter !== 'none' ? cs.backdropFilter : (cs.webkitBackdropFilter || 'none');
                    const hasBlur = backdrop && backdrop !== 'none';
                    const hasGradient = cs.backgroundImage && cs.backgroundImage.includes('gradient');

                    if ((hasShadow || hasBlur || hasGradient) && surfacesAndShadows.length < 25) {
                        const sig = `${cs.boxShadow}|${backdrop}|${cs.backgroundImage}|${cs.borderRadius}`;
                        if (!seenSurfaceSigs.has(sig)) {
                            seenSurfaceSigs.add(sig);
                            surfacesAndShadows.push({
                                tag: el.tagName.toLowerCase(),
                                backgroundColor: cs.backgroundColor,
                                backgroundImage: hasGradient ? cs.backgroundImage : 'none',
                                boxShadow: cs.boxShadow,
                                backdropFilter: backdrop,
                                borderRadius: cs.borderRadius,
                                border: `${cs.borderTopWidth} ${cs.borderTopStyle} ${cs.borderTopColor}`
                            });
                        }
                    }
                }

                const topColors = (map, limit = 12) =>
                    Array.from(map.entries())
                        .sort((a, b) => b[1] - a[1])
                        .slice(0, limit)
                        .map(([value, occurrences]) => ({ value, occurrences }));

                return {
                    css_variables: cssVariables,
                    color_palette: {
                        backgrounds: topColors(bgMap),
                        texts: topColors(textMap),
                        borders: topColors(borderMap)
                    },
                    typography_scale: Array.from(typographyMap.values()).slice(0, 16),
                    surfaces_and_shadows: surfacesAndShadows,
                    easing_curves: Array.from(easingSet),
                    keyframes: keyframes.slice(0, 20)
                };
            }"""
        )

    async def _extract_structural_clone(self, page: Page) -> Dict[str, Any]:
        """
        ME-01 + ME-02 (OS-20261020-CDP-STRUCTURAL-CLONE):
        classificação tipográfica por papel, font assets, section blueprints com slots
        e filtros SVG vinculados às regras CSS que os aplicam.
        """
        payload = await page.evaluate(STRUCTURAL_CLONE_SCRIPT)
        if not isinstance(payload, dict):
            raise ValueError("Extração estrutural retornou payload inválido (não-objeto).")
        for key in ("typography_roles", "font_assets", "section_blueprints", "active_svg_filters"):
            if key not in payload:
                raise ValueError(f"Extração estrutural sem a chave obrigatória '{key}'.")
        return payload

    async def _probe_pseudo_states(
        self, page: Page, cdp: CDPSession
    ) -> List[ComponentInteractionDelta]:
        deltas: List[ComponentInteractionDelta] = []
        total_probed: int = await page.evaluate(
            """() => {
                const interactive = Array.from(
                    document.querySelectorAll('button, a, [role="button"], input, [class*="card"], [class*="btn"]')
                ).filter((el) => {
                    const r = el.getBoundingClientRect();
                    return r.width >= 32 && r.height >= 20 && r.top >= 0 && r.top <= window.innerHeight * 2.5;
                }).slice(0, 14);
                interactive.forEach((el, i) => el.setAttribute('data-ag-cdp-id', String(i)));
                return interactive.length;
            }"""
        )

        doc_node = await cdp.send("DOM.getDocument", {"depth": 1})
        root_id = doc_node["root"]["nodeId"]

        for idx in range(total_probed):
            selector = f'[data-ag-cdp-id="{idx}"]'
            q = await cdp.send("DOM.querySelector", {"nodeId": root_id, "selector": selector})
            node_id = q.get("nodeId", 0)
            if not node_id:
                continue

            resting = await self._snapshot_element_props(page, selector)

            # 1. Ativa :hover via CDP usando o nodeId numérico
            await cdp.send("CSS.forcePseudoState", {"nodeId": node_id, "forcedPseudoClasses": ["hover"]})
            # 2. Também aciona hover via Playwright para ativar listeners JS se existirem
            try:
                locator = page.locator(selector).first
                if await locator.is_visible():
                    await locator.hover(timeout=500)
            except Exception:
                pass

            hovered = await self._snapshot_element_props(page, selector)

            # 3. Força :focus-visible via CDP
            await cdp.send(
                "CSS.forcePseudoState",
                {"nodeId": node_id, "forcedPseudoClasses": ["focus", "focus-visible"]}
            )
            focused = await self._snapshot_element_props(page, selector)

            # Restaura o estado normal
            await cdp.send("CSS.forcePseudoState", {"nodeId": node_id, "forcedPseudoClasses": []})

            hover_diff: Dict[str, Dict[str, str]] = {}
            focus_diff: Dict[str, Dict[str, str]] = {}

            for prop in TRACKED_INTERACTIVE_PROPS:
                base_val = resting["props"].get(prop, "")
                hov_val = hovered["props"].get(prop, "")
                foc_val = focused["props"].get(prop, "")
                if base_val != hov_val:
                    hover_diff[prop] = {"from": base_val, "to": hov_val}
                if base_val != foc_val:
                    focus_diff[prop] = {"from": base_val, "to": foc_val}

            if hover_diff or focus_diff:
                deltas.append(
                    ComponentInteractionDelta(
                        selector=resting["label"],
                        tag=resting["tag"],
                        resting_state=resting["props"],
                        hover_delta=hover_diff,
                        focus_delta=focus_diff,
                        transition_physics=resting["transition"],
                    )
                )

        await page.evaluate(
            """() => {
                document.querySelectorAll('[data-ag-cdp-id]').forEach((el) => el.removeAttribute('data-ag-cdp-id'));
            }"""
        )
        return deltas

    async def _snapshot_element_props(self, page: Page, selector: str) -> Dict[str, Any]:
        return await page.evaluate(
            """({ selector, trackedProps }) => {
                const el = document.querySelector(selector);
                if (!el) return { tag: '', label: '', transition: '', props: {} };
                const prevTransition = el.style.transition;
                el.style.transition = 'none';
                const cs = window.getComputedStyle(el);
                const props = {};
                for (const p of trackedProps) {
                    props[p] = cs[p];
                }
                const transition = `${cs.transitionProperty} | ${cs.transitionDuration} | ${cs.transitionTimingFunction}`;
                el.style.transition = prevTransition;
                const classTokens = typeof el.className === 'string' && el.className.trim()
                    ? '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.')
                    : '';
                return {
                    tag: el.tagName.toLowerCase(),
                    label: `${el.tagName.toLowerCase()}${classTokens}`,
                    transition,
                    props
                };
            }""",
            {"selector": selector, "trackedProps": TRACKED_INTERACTIVE_PROPS},
        )

    async def _capture_component_pairs(
        self, page: Page, cdp: CDPSession, assets_dir: Path, max_components: int
    ) -> List[ComponentVisualPair]:
        pairs: List[ComponentVisualPair] = []
        candidates_meta = await page.evaluate(
            """(limit) => {
                const nodes = Array.from(
                    document.querySelectorAll('button, a, [role="button"], [class*="card"], [class*="btn"]')
                ).filter((el) => {
                    const r = el.getBoundingClientRect();
                    const cs = window.getComputedStyle(el);
                    return (
                        r.width >= 40 && r.height >= 24 && r.top >= 0 &&
                        r.bottom <= window.innerHeight * 2.5 &&
                        cs.visibility !== 'hidden' && cs.display !== 'none'
                    );
                }).slice(0, limit);
                return nodes.map((el, idx) => {
                    el.setAttribute('data-ag-shot-id', String(idx));
                    const cls = typeof el.className === 'string' && el.className.trim()
                        ? '.' + el.className.trim().split(/\\s+/).slice(0, 2).join('.')
                        : '';
                    return { idx, tag: el.tagName.toLowerCase(), label: `${el.tagName.toLowerCase()}${cls}` };
                });
            }""",
            max_components,
        )

        doc_node = await cdp.send("DOM.getDocument", {"depth": 1})
        root_id = doc_node["root"]["nodeId"]

        for item in candidates_meta:
            idx = item["idx"]
            selector = f'[data-ag-shot-id="{idx}"]'
            q = await cdp.send("DOM.querySelector", {"nodeId": root_id, "selector": selector})
            node_id = q.get("nodeId", 0)
            if not node_id:
                continue

            locator = page.locator(selector).first
            await locator.scroll_into_view_if_needed()

            # Congela transição para evitar motion blur
            await page.evaluate(
                """(sel) => {
                    const el = document.querySelector(sel);
                    if (el) {
                        el.setAttribute('data-prev-trans', el.style.transition || '');
                        el.style.transition = 'none';
                    }
                }""",
                selector,
            )

            resting_file = assets_dir / f"comp_{idx:02d}_resting.png"
            hover_file = assets_dir / f"comp_{idx:02d}_hover.png"

            await locator.screenshot(path=str(resting_file))

            # Força :hover via CDP
            await cdp.send("CSS.forcePseudoState", {"nodeId": node_id, "forcedPseudoClasses": ["hover"]})
            await page.wait_for_timeout(40)
            await locator.screenshot(path=str(hover_file))

            # Restaura
            await cdp.send("CSS.forcePseudoState", {"nodeId": node_id, "forcedPseudoClasses": []})
            box = await locator.bounding_box() or {"x": 0.0, "y": 0.0, "width": 0.0, "height": 0.0}

            await page.evaluate(
                """(sel) => {
                    const el = document.querySelector(sel);
                    if (el) {
                        el.style.transition = el.getAttribute('data-prev-trans') || '';
                        el.removeAttribute('data-prev-trans');
                        el.removeAttribute('data-ag-shot-id');
                    }
                }""",
                selector,
            )

            pairs.append(
                ComponentVisualPair(
                    index=idx,
                    selector=item["label"],
                    tag=item["tag"],
                    bounding_box=box,
                    resting_screenshot_path=str(resting_file),
                    hover_screenshot_path=str(hover_file),
                )
            )

        return pairs


@mcp.tool()
async def extract_cdp_design_telemetry(
    url: str,
    output_path: str = "design-telemetry.json",
) -> str:
    """
    Inspeciona uma URL de referência via Chrome DevTools Protocol (CDP), extraindo
    tokens brutos em :root, regras computadas, escala tipográfica, sombras e deltas de hover.
    Emite o artefato imutável `design-telemetry.json` (schema cdp.telemetry.v1).
    """
    engine = CDPExtractorEngine(url=url)
    telemetry = await engine.execute_telemetry_extraction()
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(asdict(telemetry), indent=2, ensure_ascii=False), encoding="utf-8")

    return json.dumps(
        {
            "status": "success",
            "schema_version": telemetry.schema_version,
            "capture_id": telemetry.capture_id,
            "source_url": url,
            "saved_telemetry_path": str(out),
            "css_variables_count": len(telemetry.css_custom_properties),
            "hover_deltas_count": len(telemetry.interactive_deltas),
        },
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
async def capture_webgl_and_component_states(
    url: str,
    output_dir: str = ".antigravity/visual-captures",
    max_components: int = 8,
) -> str:
    """
    Intercepta código-fonte GLSL de Shaders WebGL1/WebGL2, uniforms e captura pares
    de screenshots 2x DPI (repouso vs. hover congelado).
    Emite o artefato instrumental `visual-shader-manifest.json` (schema cdp.shaders.v1).
    """
    engine = CDPExtractorEngine(url=url)
    assets_path = Path(output_dir).resolve()
    visual_telemetry = await engine.execute_visual_and_shader_capture(
        assets_dir=assets_path, max_components=max_components
    )
    manifest_path = assets_path / "visual-shader-manifest.json"
    manifest_path.write_text(
        json.dumps(asdict(visual_telemetry), indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return json.dumps(
        {
            "status": "success",
            "schema_version": visual_telemetry.schema_version,
            "capture_id": visual_telemetry.capture_id,
            "source_url": url,
            "manifest_path": str(manifest_path),
            "webgl_supported": visual_telemetry.webgl_supported,
            "webgl_shaders_captured": len(visual_telemetry.webgl_shaders),
            "component_screenshot_pairs": len(visual_telemetry.component_visual_pairs),
        },
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
async def compile_living_design_system_html(
    telemetry_path: str = "design-telemetry.json",
    visual_manifest_path: str = ".antigravity/visual-captures/visual-shader-manifest.json",
    output_html_path: str = "design-system.html",
    output_tokens_path: str = "design-tokens.json",
    export_raw_fidelity: bool = False,
) -> str:
    """
    Compila os dados extraídos pelo CDP em:
    1. `design-tokens.json` (contrato semântico w3c.design-tokens.v1);
    2. `design-system.html` (Living Style Guide executável calibrado para Paz Cognitiva e WebMCP);
    3. `design-system-raw.html` (opcional, quando export_raw_fidelity=True).
    """
    src = Path(telemetry_path).resolve()
    if not src.exists():
        raise FileNotFoundError(f"Arquivo de telemetria não encontrado em {src}.")

    data = json.loads(src.read_text(encoding="utf-8"))
    capture_id = sanitize_text(data.get("capture_id", "anonymous_cap"))
    source_url = sanitize_text(data.get("source_url", "unknown"))

    bgs = data.get("color_palette", {}).get("backgrounds", [])
    texts = data.get("color_palette", {}).get("texts", [])
    borders = data.get("color_palette", {}).get("borders", [])
    easings = data.get("easing_curves", [])
    surfaces = data.get("surfaces_and_shadows", [])
    fonts = data.get("typography_scale", [])

    raw_easing = easings[0] if easings else "cubic-bezier(0.16, 1, 0.3, 1)"
    raw_font = fonts[0]["fontFamily"] if fonts else "'Inter', -apple-system, sans-serif"
    raw_shadow = surfaces[0]["boxShadow"] if surfaces else "0 10px 30px -10px rgba(0,0,0,0.12)"
    raw_backdrop = surfaces[0]["backdropFilter"] if surfaces else "blur(12px)"

    primary_easing = sanitize_css_value(raw_easing, "cubic-bezier(0.16, 1, 0.3, 1)")
    primary_font = sanitize_css_value(raw_font, "'Inter', -apple-system, sans-serif")
    primary_shadow = sanitize_css_value(raw_shadow, "0 10px 30px -10px rgba(0,0,0,0.12)")
    primary_backdrop = sanitize_css_value(raw_backdrop, "blur(12px)")

    # 2. Tipografia por papéis semânticos (ME-01)
    roles = data.get("typography_roles", {})
    body_role = roles.get("body") or {}
    display_role = roles.get("display") or {}
    hand_role = roles.get("accent_hand") or {}
    mono_role = roles.get("mono") or {}

    # Se body_role for nulo ou classificado como hand, DEVE usar fallback semântico limpo
    if body_role and body_role.get("family") and not body_role.get("generic_hand", False):
        font_sans = sanitize_css_value(body_role.get("stack", body_role.get("family")), "'Inter', system-ui, sans-serif")
    else:
        # Fallback estrito: NUNCA permitir cursive, hand ou fantasy no sans/body
        cand = [
            f["fontFamily"] for f in fonts
            if not any(c in f["fontFamily"].lower() for c in ("cursive", "fantasy", "hand", "caveat", "script", "duducalligraphy", "chicle", "faracohand"))
        ]
        font_sans = sanitize_css_value(cand[0] if cand else "'Inter', system-ui, -apple-system, sans-serif")

    if display_role and display_role.get("family"):
        font_display = sanitize_css_value(display_role.get("stack", display_role.get("family")), font_sans)
    else:
        font_display = font_sans

    if hand_role and hand_role.get("family"):
        font_hand = sanitize_css_value(hand_role.get("stack", hand_role.get("family")), "'Caveat', cursive")
    else:
        font_hand = "'Caveat', cursive"

    if mono_role and mono_role.get("family"):
        font_mono = sanitize_css_value(mono_role.get("stack", mono_role.get("family")), "'JetBrains Mono', monospace")
    else:
        font_mono = "'JetBrains Mono', monospace"

    # Cores Reais da Referência (ME-03)
    raw_bgs = [b["value"] for b in bgs]
    raw_texts = [t["value"] for t in texts]
    raw_borders = [br["value"] for br in borders]

    ref_bg_primary = sanitize_css_value(raw_bgs[0] if raw_bgs else "#0b0b0b")
    ref_bg_surface = sanitize_css_value(raw_bgs[1] if len(raw_bgs) > 1 else ref_bg_primary)
    ref_text_primary = sanitize_css_value(raw_texts[0] if raw_texts else "#f3f1ec")
    ref_text_secondary = sanitize_css_value(raw_texts[1] if len(raw_texts) > 1 else ref_text_primary)
    ref_border = sanitize_css_value(raw_borders[0] if raw_borders else "rgba(255, 255, 255, 0.1)")

    # Font assets: gerar tags de link e @font-face capturados
    font_assets = data.get("font_assets", {})
    font_links_html = "\n".join([f'    <link rel="stylesheet" href="{sanitize_text(l.get("href"))}">' for l in font_assets.get("stylesheet_links", []) if l.get("href")])
    font_faces_css = "\n".join([
        f"@font-face {{ font-family: '{sanitize_text(ff.get('family'))}'; src: {ff.get('src')}; font-weight: {ff.get('weight', 'normal')}; font-style: {ff.get('style', 'normal')}; font-display: swap; }}"
        for ff in font_assets.get("font_faces", []) if ff.get("family") and ff.get("src")
    ])

    # Seção Blueprints e Filtros SVG
    blueprints = data.get("section_blueprints", [])
    active_filters = data.get("active_svg_filters", [])
    svg_defs_html = "\n".join([f.get("markup", "") for f in active_filters if f.get("markup")])

    # 1. Gera o contrato semântico design-tokens.json
    semantic_tokens = {
        "$schema": "https://design-tokens.github.io/community-group/format/",
        "schema_version": "w3c.design-tokens.v1",
        "capture_id": capture_id,
        "source_url": source_url,
        "color": {
            "background": {
                "canvas": {"$value": ref_bg_primary, "$type": "color"},
                "surface": {"$value": ref_bg_surface, "$type": "color"},
                "elevated": {"$value": ref_bg_surface, "$type": "color"},
            },
            "text": {
                "primary": {"$value": ref_text_primary, "$type": "color"},
                "secondary": {"$value": ref_text_secondary, "$type": "color"},
            },
            "border": {
                "subtle": {"$value": ref_border, "$type": "color"},
            },
        },
        "typography": {
            "fontFamily": {
                "sans": {"$value": font_sans, "$type": "fontFamily"},
                "display": {"$value": font_display, "$type": "fontFamily"},
                "hand": {"$value": font_hand, "$type": "fontFamily"},
                "mono": {"$value": font_mono, "$type": "fontFamily"},
            },
            "fontSize": {
                "hero": {"$value": "clamp(2rem, 4vw, 3rem)", "$type": "dimension"},
                "title": {"$value": "clamp(1.25rem, 2vw, 1.5rem)", "$type": "dimension"},
                "base": {"$value": "1rem", "$type": "dimension"},
            },
        },
        "elevation": {
            "card": {"$value": primary_shadow, "$type": "shadow"},
            "backdrop": {"$value": primary_backdrop, "$type": "filter"},
        },
        "motion": {
            "easing": {"$value": primary_easing, "$type": "cubicBezier"},
            "duration": {"$value": "350ms", "$type": "duration"},
        },
    }

    tokens_path = Path(output_tokens_path).resolve()
    tokens_path.write_text(json.dumps(semantic_tokens, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. Compila o Living Design System em HTML (Paz Cognitiva + Clone Estrutural + WebMCP)
    # Filtros SVG com classes CSS ativas correspondentes
    svg_filter_classes_css = []
    svg_filter_demo_html = []
    for flt in active_filters:
        fid = flt.get("id")
        if fid:
            cls_name = f"ds-effect-{fid}"
            svg_filter_classes_css.append(f".{cls_name} {{ filter: url(#{fid}) !important; }}")
            svg_filter_demo_html.append(f"""
            <div class="{cls_name}" style="padding: 1.5rem; min-height: 80px; display: flex; align-items: center; justify-content: center; background: var(--ds-bg-surface); border: 1px solid var(--ds-border-subtle); border-radius: 8px;">
                <span style="font-family: var(--ds-font-mono); font-size: 0.9rem;">Filtro Ativo: <code>url(#{fid})</code></span>
            </div>
            """)

    svg_filters_css_block = "\n        ".join(svg_filter_classes_css)
    svg_filters_demo_block = "\n".join(svg_filter_demo_html) if svg_filter_demo_html else "<p style='color: var(--ds-text-secondary);'>Nenhum filtro SVG com id registrado.</p>"

    # Seção Blueprints HTML (Variedade Estrutural Anti-Card-Stacking)
    blueprints_demo_html = []
    section_classes = ["ds-section-hero-blueprint", "ds-section-grid-blueprint", "ds-section-console-blueprint", "ds-section-summary-blueprint"]
    for idx, bp in enumerate(blueprints[:4]):
        b_idx = bp.get("index", idx)
        b_mode = bp.get("layout_mode", "block")
        b_cols = bp.get("grid_template_columns", "none")
        b_skel = bp.get("structural_template_html", "")
        sec_cls = section_classes[idx % len(section_classes)]
        blueprints_demo_html.append(f"""
        <section class="{sec_cls}" style="margin-top: 1.5rem; padding: 2rem; background: {'rgba(255,255,255,0.02)' if idx % 2 == 0 else 'rgba(0,0,0,0.2)'}; border-radius: {12 + idx * 4}px; border: 1px solid var(--ds-border-subtle);">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.75rem;">
                <span class="ds-badge">ARQUÉTIPO #{b_idx} // LAYOUT: {b_mode.upper()}</span>
                <span style="font-size: 0.8rem; font-family: var(--ds-font-mono); color: var(--ds-text-secondary);">{b_cols}</span>
            </div>
            <div class="blueprint-preview" style="background: rgba(0,0,0,0.05); padding: 1rem; border-radius: 8px;">
                {b_skel}
            </div>
        </section>
        """)
    blueprints_block = "\n".join(blueprints_demo_html) if blueprints_demo_html else "<p>Nenhum archetype de seção capturado.</p>"

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Living Design System — {source_url}</title>
{font_links_html}
    <style>
{font_faces_css}

        :root {{
            --ds-bg-canvas: {ref_bg_primary};
            --ds-bg-surface: {ref_bg_surface};
            --ds-text-primary: {ref_text_primary};
            --ds-text-secondary: {ref_text_secondary};
            --ds-border-subtle: {ref_border};
            --ds-border-highlight: rgba(255, 255, 255, 0.25);
            --ds-accent-agentic: #4f46e5;
            --ds-font-primary: {font_sans};
            --ds-font-sans: {font_sans};
            --ds-font-display: {font_display};
            --ds-font-hand: {font_hand};
            --ds-font-mono: {font_mono};
            --ds-ease-primary: {primary_easing};
            --ds-shadow-card: {primary_shadow};
            --ds-backdrop-filter: {primary_backdrop};
            --ds-radius-card: 16px;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: var(--ds-bg-canvas);
            color: var(--ds-text-primary);
            font-family: var(--ds-font-sans);
            line-height: 1.6;
            min-height: 100vh;
            padding: 3rem 1.5rem;
            -webkit-font-smoothing: antialiased;
        }}

        h1, h2, .ds-display {{
            font-family: var(--ds-font-display);
        }}

        .ds-hand {{
            font-family: var(--ds-font-hand);
        }}

        .ds-mono {{
            font-family: var(--ds-font-mono);
        }}

        .ds-shell {{
            max-width: 1140px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 2.5rem;
        }}

        .ds-card {{
            position: relative;
            background: var(--ds-bg-surface);
            border: 1px solid var(--ds-border-subtle);
            border-radius: var(--ds-radius-card);
            padding: 2rem;
            box-shadow: var(--ds-shadow-card);
            transition: transform 350ms var(--ds-ease-primary), border-color 350ms var(--ds-ease-primary);
            overflow: hidden;
        }}

        .ds-card:hover {{
            transform: translateY(-2px);
            border-color: var(--ds-border-highlight);
        }}

        {svg_filters_css_block}

        /* WebMCP: Estilização do estado ativo da ferramenta de agente */
        form[toolname]:tool-form-active {{
            outline: 2px solid var(--ds-accent-agentic);
            box-shadow: 0 0 24px rgba(79, 70, 229, 0.25);
            transition: box-shadow 300ms var(--ds-ease-primary);
        }}

        .ds-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
        }}

        .ds-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            background: #e0e7ff;
            color: #3730a3;
            margin-bottom: 0.75rem;
        }}

        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }}
        }}
    </style>
</head>
<body>
    <div style="display:none;">
        {svg_defs_html}
    </div>

    <main class="ds-shell">
        <header class="ds-card">
            <span class="ds-badge">AURORA LIVING DESIGN SYSTEM // CDP SPEC v2.0 CLONE</span>
            <h1 style="font-size: clamp(1.8rem, 3.5vw, 2.75rem); margin-bottom: 0.5rem;">
                Referência: {source_url}
            </h1>
            <p style="color: var(--ds-text-secondary);">
                Capture ID: <code>{capture_id}</code> | Curva de Física: <code>{primary_easing}</code>
            </p>
            <div class="ds-hand" style="font-size: 1.25rem; margin-top: 0.5rem; color: #7fa8f0;">
                Anotação estilizada com fonte accent hand: {{SLOT_ANNOTATION}}
            </div>
        </header>

        <!-- Bloco C: Demonstração Ativa de Filtros SVG Extraídos -->
        <section class="ds-card">
            <h2>Efeitos Ativos (Filtros SVG da Referência com Regras CSS Vinculadas)</h2>
            <div style="margin-top: 1rem; display: flex; flex-direction: column; gap: 1rem;">
                {svg_filters_demo_block}
            </div>
        </section>

        <!-- Bloco A & B: Blueprints de Seção Clonados -->
        <section>
            <h2>Blueprints de Seções Clonadas da Referência (DOM Skeletons com Slots)</h2>
            {blueprints_block}
        </section>

        <!-- Bloco D: Ferramenta WebMCP -->
        <section class="ds-card">
            <h2 style="margin-bottom: 1rem;">Console WebMCP (document.modelContext)</h2>
            <form toolname="simulate_roi" tooldescription="Calcula o retorno de investimento da arquitetura agêntica">
                <p style="color: var(--ds-text-secondary); margin-bottom: 1rem;">
                    Formulário instrumentado para agentes navegadores (Chrome 150+ WebMCP com suporte a degradação graciosa).
                </p>
                <div id="webmcp-status" style="font-size: 0.85rem; color: var(--ds-text-secondary);">
                    Verificando suporte à API <code>document.modelContext</code>...
                </div>
            </form>
        </section>
    </main>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const statusEl = document.getElementById('webmcp-status');
            const hasWebMCP = typeof document !== 'undefined' && 'modelContext' in document;
            if (hasWebMCP) {{
                statusEl.textContent = 'API WebMCP (document.modelContext) ativa e disponível.';
                statusEl.style.color = '#15803d';
            }} else {{
                statusEl.textContent = 'Modo padrão: document.modelContext ausente. Degradação funcional HTML5 ativa.';
            }}
        }});
    </script>
</body>
</html>"""

    html_path = Path(output_html_path).resolve()
    html_path.write_text(html_content, encoding="utf-8")

    result = {
        "status": "compiled",
        "capture_id": capture_id,
        "design_tokens_path": str(tokens_path),
        "design_system_html_path": str(html_path),
    }

    if export_raw_fidelity:
        raw_html_path = html_path.parent / "design-system-raw.html"
        raw_html_path.write_text(html_content, encoding="utf-8")
        result["design_system_raw_html_path"] = str(raw_html_path)

    return json.dumps(result, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(transport="stdio")
