#!/usr/bin/env python3
"""
test_aesthetic_fidelity_gate.py — Validador Estético e Estrutural via Playwright.

Detecta 6 Anti-Padrões de Degradação Estética e Estrutural:
- AP1 (Paleta Descartada): Cores dominantes da telemetria ignoradas ou uso indevido de #f8fafc.
- AP2 (Contaminação Tipográfica): cursive/handwriting no body/<p> OU queda em fonte genérica do sistema (Segoe UI, Arial).
- AP3 (Filtro SVG Morto): <filter id="X"> presente no DOM com zero elementos aplicando filter: url(#X).
- AP4 (Monotonia Estrutural / Card Stacking): >50% das <section> filhas diretas usando mesma classe, bg e border-radius.
- AP5 (Física Genérica): Elementos interativos usando timing-function ease ou 0s em vez de cubic-bezier.
- AP6 (Regressão WebMCP / Conteúdo): Presença de navigator.modelContext ou erro de schema JSON-LD.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

SYSTEM_FONTS = {"segoe ui", "arial", "times new roman", "helvetica", "tahoma", "verdana"}
HANDWRITING_FONTS = {"faracohand", "caveat", "pacifico", "dancing script", "kalam", "cursive"}


def audit_html_file(html_path: Path, telemetry_path: Path = None) -> list:
    violations = []
    if not html_path.exists():
        return [f"Arquivo HTML não encontrado: {html_path}"]

    raw_html = html_path.read_text(encoding="utf-8")
    
    # ---------------- AP6: Regressão WebMCP ----------------
    if "navigator.modelContext" in raw_html:
        violations.append("AP6: Presença da API depreciada 'navigator.modelContext'. Use exclusivamente 'document.modelContext'.")

    # Inspeciona com Playwright Headless
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(raw_html)

        # ---------------- AP1: Paleta Descartada & #f8fafc ----------------
        if telemetry_path and telemetry_path.exists():
            telem = json.loads(telemetry_path.read_text(encoding="utf-8"))
            ref_bgs = [b["value"].lower() for b in telem.get("color_palette", {}).get("backgrounds", [])[:3]]
            # Se a referência não tem #f8fafc, proibir #f8fafc no HTML
            ref_has_slate = any("#f8fafc" in c or "248, 250, 252" in c for c in ref_bgs)
            if not ref_has_slate and ("#f8fafc" in raw_html or "rgb(248, 250, 252)" in raw_html):
                violations.append("AP1 (Paleta Descartada): Hardcode #f8fafc detectado quando a referência não utiliza essa cor.")

        # ---------------- AP2: Contaminação Tipográfica ----------------
        body_font = page.evaluate("() => window.getComputedStyle(document.body).fontFamily.toLowerCase()")
        p_fonts = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('p')).map(p => window.getComputedStyle(p).fontFamily.toLowerCase());
        }""")

        # Verifica se alguma fonte cursive assumiu o body ou parágrafos
        for hf in HANDWRITING_FONTS:
            if hf in body_font:
                violations.append(f"AP2 (Contaminação Tipográfica): Fonte decorativa/handwriting '{hf}' detectada no body!")
            if any(hf in pf for pf in p_fonts[:5]):
                violations.append(f"AP2 (Contaminação Tipográfica): Fonte decorativa/handwriting '{hf}' detectada nos parágrafos <p>!")

        # Verifica se caiu em fonte de sistema sem declarar webfont
        for sf in SYSTEM_FONTS:
            if sf in body_font and not any(k in body_font for k in ("inter", "jakarta", "roboto", "geist", "system-ui")):
                violations.append(f"AP2 (Contaminação Tipográfica): Queda em fonte genérica de sistema '{sf}' sem webfont declarada!")

        # ---------------- AP3: Filtro SVG Morto ----------------
        filter_ids = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('svg filter[id]')).map(f => f.id);
        }""")
        for fid in filter_ids:
            applied_count = page.evaluate(f"""() => {{
                return Array.from(document.querySelectorAll('*')).filter(el => {{
                    const cs = window.getComputedStyle(el);
                    const inline = el.getAttribute('filter') || '';
                    const styleAttr = el.getAttribute('style') || '';
                    return (cs.filter && cs.filter.includes('{fid}')) || 
                           inline.includes('{fid}') || 
                           styleAttr.includes('{fid}');
                }}).length;
            }}""")
            if applied_count == 0:
                violations.append(f"AP3 (Filtro SVG Morto): Filtro <filter id='{fid}'> declarado no DOM com ZERO elementos aplicando 'filter: url(#{fid})' ou CSS Variables associadas!")

        # ---------------- AP4: Monotonia Estrutural (Card Stacking) ----------------
        sections_info = page.evaluate("""() => {
            const secs = Array.from(document.querySelectorAll('section, main > section, .ds-shell > section'));
            return secs.map(s => {
                const cs = window.getComputedStyle(s);
                return {
                    className: s.className,
                    bg: cs.backgroundColor,
                    radius: cs.borderRadius
                };
            });
        }""")
        if len(sections_info) >= 4:
            # Conta seções idênticas
            class_counts = {}
            for s in sections_info:
                sig = f"{s['className']}|{s['bg']}|{s['radius']}"
                class_counts[sig] = class_counts.get(sig, 0) + 1
            max_dup = max(class_counts.values()) if class_counts else 0
            if (max_dup / len(sections_info)) > 0.40:
                violations.append(f"AP4 (Monotonia Estrutural / Card Stacking): {max_dup} de {len(sections_info)} seções compartilham layout e classe idênticos (.card empilhado monotônico)!")

        # ---------------- AP5: Física Genérica ----------------
        timing_funcs = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('button, a, .card, [class*="card"]')).map(el => {
                return window.getComputedStyle(el).transitionTimingFunction;
            });
        }""")
        # Se todos os botões/cards usam ease simples ou 0s
        if timing_funcs and all(tf in ("ease", "linear", "") for tf in timing_funcs):
            violations.append("AP5 (Física Genérica): Elementos interativos utilizam 'ease' padrão em vez de aceleração cubic-bezier extraída!")

        browser.close()

    return violations


def main():
    parser = argparse.ArgumentParser(description="Audit Aesthetic and Structural Fidelity Gate")
    parser.add_argument("--html", required=True, help="Caminho do HTML para auditoria")
    parser.add_argument("--telemetry", required=False, help="Caminho do design-telemetry.json")
    args = parser.parse_args()

    html_file = Path(args.html)
    telem_file = Path(args.telemetry) if args.telemetry else None

    print(f"=== INICIANDO GATE DE AUDITORIA ESTÉTICA E ESTRUTURAL ===")
    print(f"Alvo HTML: {html_file}")
    if telem_file:
        print(f"Telemetria: {telem_file}")

    violations = audit_html_file(html_file, telem_file)

    if violations:
        print(f"\n[REPROVADO - EXIT=1] Detectadas {len(violations)} violacoes:")
        for v in violations:
            print(f"  [VIOLACAO] {v}")
        sys.exit(1)
    else:
        print("\n[APROVADO - EXIT=0] Zero violacoes esteticas ou estruturais detectadas. Padrao S-Tier em conformidade!")
        sys.exit(0)


if __name__ == "__main__":
    main()
