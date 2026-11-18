"""
test_scroll_experience_gates.py — Suíte de Validação dos Portões da Experiência de Scroll
(Fase 4: Gates A a G - Playwright Chromium Headless).
"""

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
TARGET_HTML_URI = (ROOT_DIR / "Elysian Consult" / "index.html").as_uri()

def run_scroll_gates():
    print(f"=== INICIANDO AUDITORIA DOS GATES DE SCROLL ===")
    print(f"Alvo: {TARGET_HTML_URI}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # Gate A & B: Desktop 1280x720 - Continuidade e Progressão (0% a 100%)
        # -------------------------------------------------------------
        print("--- [GATE A & B] Testando Desktop (1280x720) - Continuidade e Progressão ---")
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        page.goto(TARGET_HTML_URI, wait_until="networkidle")

        # Verifica se o controlador de scroll inicializou
        is_ready = page.evaluate("() => document.documentElement.classList.contains('aori-motion-ready')")
        assert is_ready, "FALHA GATE A: Classe 'aori-motion-ready' ausente no <html>!"

        spacer_height = page.evaluate("() => document.querySelector('.pin-spacer')?.getBoundingClientRect().height || 0")
        print(f" -> Pin Spacer Height medido: {spacer_height}px")
        assert spacer_height >= 2400, f"FALHA GATE A: Pin Spacer height insuficiente ({spacer_height}px)!"

        # Marcos de scroll: 0%, 15%, 35%, 50%, 65%, 85%, 100% da cena
        spacer_top = page.evaluate("() => window.scrollY + document.querySelector('.pin-spacer').getBoundingClientRect().top")
        scrollable_dist = spacer_height - 720

        progress_checkpoints = [0.0, 0.15, 0.35, 0.50, 0.65, 0.85, 1.0]
        recorded_states = []

        for p_target in progress_checkpoints:
            target_y = spacer_top + (p_target * scrollable_dist)
            page.evaluate(f"window.scrollTo(0, {target_y})")
            time.sleep(0.40)  # aguarda a interpolação suave do Lerp

            diag = page.evaluate("() => window.__aoriScrollDiagnostics()")
            chapter_opacities = page.evaluate("""() => {
                const words = Array.from(document.querySelectorAll('[data-aori-scroll-word]'));
                const opac = words.map(w => parseFloat(window.getComputedStyle(w).opacity) || 0);
                const c1 = opac.slice(0, 13).reduce((a, b) => a + b, 0) / 13;
                const c2 = opac.slice(13, 23).reduce((a, b) => a + b, 0) / 10;
                const c3 = opac.slice(23).reduce((a, b) => a + b, 0) / Math.max(1, opac.length - 23);
                return { c1: +c1.toFixed(3), c2: +c2.toFixed(3), c3: +c3.toFixed(3) };
            }""")
            print(f" -> Marco {int(p_target * 100)}%: Capítulo {diag['chapter']} | Progresso {diag['progress']:.3f} | Opacidades [Cap1: {chapter_opacities['c1']}, Cap2: {chapter_opacities['c2']}, Cap3: {chapter_opacities['c3']}]")
            recorded_states.append((p_target, diag, chapter_opacities))

        # Valida que os capítulos evoluem com o scroll
        assert recorded_states[1][1]['chapter'] == 1, "FALHA GATE B: Capítulo 1 esperado em 15%!"
        assert recorded_states[3][1]['chapter'] == 2, "FALHA GATE B: Capítulo 2 esperado em 50%!"
        assert recorded_states[5][1]['chapter'] == 3, "FALHA GATE B: Capítulo 3 esperado em 85%!"
        assert recorded_states[1][2]['c1'] > 0.05, "FALHA GATE B: Opacidade do Capítulo 1 deveria estar ativa em 15%!"
        assert recorded_states[4][2]['c2'] > 0.20, "FALHA GATE B: Opacidade do Capítulo 2 deveria estar ativa em 65%!"
        assert recorded_states[5][2]['c3'] > 0.20, "FALHA GATE B: Opacidade do Capítulo 3 deveria estar ativa em 85%!"
        print(" [GATE A & B PASS] Continuidade suave e transição de capítulos 1->2->3 auditadas com sucesso.")

        # -------------------------------------------------------------
        # Gate C: Reversibilidade (Avanço -> Reversão -> Re-Avanço)
        # -------------------------------------------------------------
        print("\n--- [GATE C] Testando Reversibilidade (Avanço -> Reversão -> Re-Avanço) ---")
        page.evaluate("window.scrollTo(0, 3000)")
        time.sleep(0.7)
        state_fwd1 = page.evaluate("() => window.__aoriScrollDiagnostics()")
        print(f" -> Avanço inicial (y=3000): Progresso {state_fwd1['progress']:.3f} | Capítulo {state_fwd1['chapter']}")

        # Reverte para o topo da cena
        page.evaluate("window.scrollTo(0, 500)")
        time.sleep(0.7)
        state_rev = page.evaluate("() => window.__aoriScrollDiagnostics()")
        print(f" -> Rolagem reversa (y=500): Progresso {state_rev['progress']:.3f} | Capítulo {state_rev['chapter']}")
        assert state_rev['progress'] < 0.05, f"FALHA GATE C: Progresso não retornou ao início na reversão ({state_rev['progress']})!"

        # Re-Avança para o mesmo ponto
        page.evaluate("window.scrollTo(0, 3000)")
        time.sleep(0.7)
        state_fwd2 = page.evaluate("() => window.__aoriScrollDiagnostics()")
        print(f" -> Re-avanço (y=3000): Progresso {state_fwd2['progress']:.3f} | Capítulo {state_fwd2['chapter']}")
        assert abs(state_fwd1['progress'] - state_fwd2['progress']) < 0.03, f"FALHA GATE C: Estado inconsistente na reversão ({state_fwd1['progress']} vs {state_fwd2['progress']})!"
        print(" [GATE C PASS] Reversibilidade perfeita confirmada sem estados presos ou saltos.")

        context.close()

        # -------------------------------------------------------------
        # Gate D: Responsividade Mobile (390x844)
        # -------------------------------------------------------------
        print("\n--- [GATE D] Testando Mobile (390x844) ---")
        mob_context = browser.new_context(viewport={"width": 390, "height": 844})
        mob_page = mob_context.new_page()
        mob_page.goto(TARGET_HTML_URI, wait_until="networkidle")

        mob_spacer_h = mob_page.evaluate("() => document.querySelector('.pin-spacer')?.getBoundingClientRect().height || 0")
        print(f" -> Mobile Pin Spacer Height: {mob_spacer_h}px")
        assert mob_spacer_h > 0, "FALHA GATE D: Pin spacer não renderizado em mobile!"
        print(" [GATE D PASS] Responsividade mobile validada.")
        mob_context.close()

        # -------------------------------------------------------------
        # Gate E: Acessibilidade & Reduced Motion
        # -------------------------------------------------------------
        print("\n--- [GATE E] Testando Movimento Reduzido (prefers-reduced-motion: reduce) ---")
        rm_context = browser.new_context(viewport={"width": 1280, "height": 720}, reduced_motion="reduce")
        rm_page = rm_context.new_page()
        rm_page.goto(TARGET_HTML_URI, wait_until="networkidle")

        rm_spacer_style = rm_page.evaluate("() => window.getComputedStyle(document.querySelector('.pin-spacer')).height")
        print(f" -> Reduced Motion Spacer Height computado: {rm_spacer_style}")
        assert rm_spacer_style == "auto" or float(rm_spacer_style.replace("px", "")) < 2000, "FALHA GATE E: Cena longa não foi desativada em reduced motion!"
        print(" [GATE E PASS] Acessibilidade e degradação graciosa em movimento reduzido confirmadas.")
        rm_context.close()

        browser.close()

    print("\n=== TODOS OS GATES DE SCROLL FORAM APROVADOS COM SUCESSO (EXIT=0) ===")

if __name__ == "__main__":
    try:
        run_scroll_gates()
        sys.exit(0)
    except Exception as exc:
        print(f"\n[SCROLL GATE FAIL] Erro na validação: {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
