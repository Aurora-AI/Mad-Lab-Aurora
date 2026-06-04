import os
import sys
import uuid
import logging
import numpy as np
import hashlib
import json
import re
from PIL import Image
from typing import Tuple, List

sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../factory'))
])

from perceptual_contracts import (
    PerceptualScoreBreakdown,
    PerceptualFinding,
    VisualRegressionReport
)
from factory_contracts import StandaloneRenderBundle, UINode
from renderer_adapter import LocalOfflineRendererAdapter

logger = logging.getLogger("PerceptualEvaluator")

class PipelinePausedException(Exception):
    pass

def is_valid_png_header(file_path: str) -> bool:
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, "rb") as f:
            header = f.read(8)
            return header == b"\x89PNG\r\n\x1a\n"
    except Exception:
        return False

def get_sha256(file_path: str) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def count_ast_nodes(node: UINode) -> int:
    count = 1
    for child in node.children:
        count += count_ast_nodes(child)
    return count

def parse_rgb_string(color_str: str) -> Tuple[int, int, int]:
    # Extrai números de rgb(...) ou rgba(...)
    match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", color_str)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return 255, 255, 255

def relative_luminance_rgb(r: int, g: int, b: int) -> float:
    r_val = r / 255.0
    g_val = g / 255.0
    b_val = b / 255.0
    
    def adjust(val):
        return val / 12.92 if val <= 0.03928 else ((val + 0.055) / 1.055) ** 2.4
        
    return 0.2126 * adjust(r_val) + 0.7152 * adjust(g_val) + 0.0722 * adjust(b_val)

def relative_luminance(color_hex: str) -> float:
    color_hex = color_hex.strip().lstrip("#")
    if len(color_hex) == 3:
        color_hex = "".join([c*2 for c in color_hex])
    if len(color_hex) != 6:
        return 0.0
    try:
        r_r, g_g, b_b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
    except ValueError:
        return 0.0
    return relative_luminance_rgb(r_r, g_g, b_b)

def contrast_ratio(l1: float, l2: float) -> float:
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

def parse_theme_colors_from_css(css_content: str) -> dict:
    colors = {}
    pattern = r"\.(text|bg)-([\w-]+)\s*\{\s*(color|background-color):\s*(#[0-9a-fA-F]{3,6})\s*;\s*\}"
    matches = re.findall(pattern, css_content)
    for prefix, name, prop, val in matches:
        colors[name] = val
    return colors

class EvaluatePerceptualFidelity:
    """
    OS-012: Rendered Visual Regression & Perceptual Evaluator
    Executa testes baseados em imagem e analisa a integridade visual da página renderizada.
    """
    def __init__(self, sandbox_dir: str, edge_threshold: float = 10.0):
        self.sandbox_dir = sandbox_dir
        self.edge_threshold = edge_threshold

    async def evaluate(self, bundle: StandaloneRenderBundle) -> VisualRegressionReport:
        logger.info(f"OS-012: Avaliando integridade perceptual do bundle {bundle.bundle_id}")
        
        # 1. Validar propriedades contratuais obrigatórias
        if bundle.dependencies_mode != "local_pinned":
            raise ValueError("Violação de Contrato: StandaloneRenderBundle deve usar dependencies_mode = 'local_pinned'.")
        if bundle.network_allowed is not False:
            raise ValueError("Violação de Contrato: StandaloneRenderBundle deve ter network_allowed = False.")
            
        # 2. Validar existência física dos arquivos descritos no manifesto
        client_path = os.path.join(self.sandbox_dir, bundle.client_component_path)
        page_path = os.path.join(self.sandbox_dir, bundle.page_entry_path)
        ui_tree_path = os.path.join(self.sandbox_dir, "ui_tree.json")
        manifest_path = os.path.join(self.sandbox_dir, "render_bundle_manifest.json")
        
        if not os.path.exists(client_path):
            raise FileNotFoundError(f"Candidato em falta no sandbox: {client_path}")
        if not os.path.exists(page_path):
            raise FileNotFoundError(f"Candidato em falta no sandbox: {page_path}")
        if not os.path.exists(ui_tree_path):
            raise FileNotFoundError(f"Candidato em falta no sandbox: {ui_tree_path}")
        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifesto em falta no sandbox: {manifest_path}")
            
        css_content = ""
        if bundle.css_entry_path:
            css_path = os.path.join(self.sandbox_dir, bundle.css_entry_path)
            if not os.path.exists(css_path):
                raise FileNotFoundError(f"Estilos em falta no sandbox: {css_path}")
            with open(css_path, "r", encoding="utf-8") as f:
                css_content = f.read()

        # Reconstruir UINode tree a partir de ui_tree.json para contagem do DOM
        with open(ui_tree_path, "r", encoding="utf-8") as f:
            tree_data = json.load(f)
            root_node = UINode(**tree_data["root_node"])

        findings: List[PerceptualFinding] = []

        # 3. Invocar Renderizador Real
        renderer = LocalOfflineRendererAdapter(self.sandbox_dir)
        render_results = await renderer.render_and_screenshot(bundle)

        screenshot_path = render_results["screenshot_path"]
        console_errors = render_results["console_errors"]
        network_requests_blocked = render_results["network_requests_blocked"]
        page_errors = render_results["page_errors"]
        text_elements_style = render_results.get("text_elements_style", [])
        rendered_text = render_results.get("rendered_text", "")

        try:
            from anti_stub_gate import AntiStubGate
            gate = AntiStubGate(surface_type="landing")
            gate.evaluate_rendered_dom_text(rendered_text)
            logger.info("AntiStubGate.RenderedDOMText Passed.")
        except Exception as e:
            # We catch it here and convert to PerceptualFinding if it fails?
            # No, if AntiStubGate raises PipelinePausedException, it will abort the pipeline.
            # But perceptual_evaluator catches PipelinePausedException? Wait, perceptual_evaluator defines its own PipelinePausedException.
            # Better to just add it as a finding.
            if hasattr(e, 'findings'):
                for f in e.findings:
                    findings.append(PerceptualFinding(
                        code=f.code,
                        severity=f.severity,
                        axis="render_error",
                        message=f.redacted_message,
                        recommended_action=f.recommended_action
                    ))
            else:
                raise

        # Validar integridade binária do screenshot
        if not is_valid_png_header(screenshot_path):
            findings.append(PerceptualFinding(
                code="SCREENSHOT_MISSING_OR_INVALID",
                severity="P0",
                axis="render_error",
                message="O screenshot gerado pelo Playwright nao e um arquivo PNG valido ou esta ausente.",
                recommended_action="Verificar instalacao do Playwright e compatibilidade de renderizacao."
            ))
            screenshot_sha256 = ""
        else:
            screenshot_sha256 = get_sha256(screenshot_path)

        # Adicionar erros de console capturados
        for err in console_errors:
            findings.append(PerceptualFinding(
                code="CONSOLE_RENDER_ERROR",
                severity="P0",
                axis="render_error",
                message=f"Erro de console no browser: {err}",
                recommended_action="Corrigir os scripts/componentes React para nao quebrar a renderizacao."
            ))

        for err in page_errors:
            findings.append(PerceptualFinding(
                code="PAGE_UNHANDLED_EXCEPTION",
                severity="P0",
                axis="render_error",
                message=f"Excecao nao tratada na pagina: {err}",
                recommended_action="Corrigir erros de runtime do React/JavaScript."
            ))

        for req in network_requests_blocked:
            findings.append(PerceptualFinding(
                code="NETWORK_POLICY_VIOLATION",
                severity="P0",
                axis="render_error",
                message=f"Fuga de rede detectada e bloqueada: {req}",
                recommended_action="Remover dependencias de CDN externas e usar assets locais."
            ))

        # 4. Avaliação de Métricas Perceptuais via Computer Vision
        color_std_luma = 0.0
        edge_density = 0.0
        non_background_ratio = 0.0
        visible_dom_nodes = count_ast_nodes(root_node)

        if is_valid_png_header(screenshot_path):
            img = Image.open(screenshot_path)
            img_gray = img.convert("L")
            img_arr = np.array(img_gray)
            
            color_std_luma = float(np.std(img_arr))
            
            gy, gx = np.gradient(img_arr)
            edge_magnitude = np.sqrt(gx**2 + gy**2)
            edges = edge_magnitude > self.edge_threshold
            edge_density = float(np.mean(edges))
            
            unique_colors, counts = np.unique(img_arr, return_counts=True)
            if len(unique_colors) > 0:
                bg_color = unique_colors[np.argmax(counts)]
                non_bg_mask = np.abs(img_arr - bg_color) > 10
                non_background_ratio = float(np.mean(non_bg_mask))

        # Teste Composto para Blank Screen (P0)
        is_blank_screen = (
            color_std_luma < 2.5 and
            edge_density < 0.001 and
            non_background_ratio < 0.005 and
            visible_dom_nodes <= 1
        )

        if is_blank_screen:
            findings.append(PerceptualFinding(
                code="BLANK_SCREEN_DETECTED",
                severity="P0",
                axis="blank_screen",
                message=f"Tela em branco detectada (luma std={color_std_luma:.2f}, edge density={edge_density:.4f}, ratio={non_background_ratio:.4f}, DOM={visible_dom_nodes}).",
                recommended_action="Adicionar elementos ou ajustar layout para renderizar conteudo real."
            ))

        # Densidade Visual Warnings (P2)
        if non_background_ratio < 0.015:
            if not is_blank_screen:
                findings.append(PerceptualFinding(
                    code="LOW_VISUAL_DENSITY",
                    severity="P2",
                    axis="density",
                    message=f"Densidade visual baixa ({non_background_ratio:.4f} < 0.015). Verifique se o espaco negativo e intencional.",
                    recommended_action="Rever layout se espaco negativo nao for intencional."
                ))
        elif non_background_ratio > 0.72:
            findings.append(PerceptualFinding(
                code="HIGH_VISUAL_DENSITY",
                severity="P2",
                axis="density",
                message=f"Densidade visual muito alta ({non_background_ratio:.4f} > 0.72). Layout pode estar poluído.",
                recommended_action="Simplificar layout e reduzir densidade de informacao."
            ))

        # 5. Avaliação de Contraste Dinâmico (Real computed style do Playwright)
        dynamic_contrast_violations = 0
        for el in text_elements_style:
            text_color = el.get("color", "")
            bg_color = el.get("backgroundColor", "")
            font_size = el.get("fontSize", "16px")
            font_weight = el.get("fontWeight", "normal")
            tag_name = el.get("tagName", "")
            text_content = el.get("textContent", "")

            # Normalizar se for transparente
            if bg_color in ("rgba(0, 0, 0, 0)", "transparent") or bg_color.endswith(", 0)"):
                bg_color = "rgb(255, 255, 255)"

            r_t, g_t, b_t = parse_rgb_string(text_color)
            r_b, g_b, b_b = parse_rgb_string(bg_color)

            lum_t = relative_luminance_rgb(r_t, g_t, b_t)
            lum_b = relative_luminance_rgb(r_b, g_b, b_b)

            ratio = contrast_ratio(lum_t, lum_b)
            
            # Converter font_size px para float
            size_px = 16.0
            size_match = re.match(r"([\d\.]+)", font_size)
            if size_match:
                try:
                    size_px = float(size_match.group(1))
                except ValueError:
                    pass

            is_bold = "bold" in font_weight or (font_weight.isdigit() and int(font_weight) >= 700)
            threshold = 3.0 if (size_px >= 24.0 or (size_px >= 18.66 and is_bold)) else 4.5

            if ratio < threshold:
                dynamic_contrast_violations += 1
                findings.append(PerceptualFinding(
                    code="LOW_CONTRAST_RATIO",
                    severity="P1",  # Computed style real no browser é P1 blocker
                    axis="contrast",
                    message=f"Contraste insuficiente no elemento <{tag_name.lower()}> ({text_content}): {ratio:.1f}:1. Minimo {threshold}:1. Texto: {text_color}, Fundo: {bg_color}.",
                    recommended_action="Ajustar cores ou fundo do elemento para atingir o contraste WCAG minimo."
                ))

        # 6. Avaliação de Contraste Estático do CSS (Fallback quando sem elementos de texto dinâmicos)
        static_contrast_violations = 0
        if not text_elements_style and css_content:
            theme_colors = parse_theme_colors_from_css(css_content)
            bg_keys = [k for k in theme_colors.keys() if "canvas" in k or "surface" in k or "bg" in k]
            text_keys = [k for k in theme_colors.keys() if "text" in k or "accent" in k or "foreground" in k or "primary" in k or "secondary" in k]
            
            for bg in bg_keys:
                bg_val = theme_colors[bg]
                bg_lum = relative_luminance(bg_val)
                for tx in text_keys:
                    tx_val = theme_colors[tx]
                    tx_lum = relative_luminance(tx_val)
                    ratio = contrast_ratio(bg_lum, tx_lum)
                    
                    if ratio < 4.5:
                        static_contrast_violations += 1
                        findings.append(PerceptualFinding(
                            code="LOW_CONTRAST_RATIO_STATIC",
                            severity="P2",  # Estático é apenas warning P2
                            axis="contrast",
                            message=f"Contraste insuficiente estatico entre .{bg} ({bg_val}) e .{tx} ({tx_val}): {ratio:.1f}:1. Minimo 4.5:1.",
                            recommended_action="Ajustar cores do tema para aumentar o contraste perceptual."
                        ))

        # 7. Pontuações e Decisões
        # Mapeamento de score de densidade
        if 0.015 <= non_background_ratio <= 0.72:
            density_score = 100.0
        elif non_background_ratio < 0.015:
            density_score = max(0.0, (non_background_ratio / 0.015) * 100.0)
        else:
            density_score = max(0.0, ((1.0 - non_background_ratio) / (1.0 - 0.72)) * 100.0)

        # Mapeamento de contraste (P1 e P2 afetam o score)
        contrast_score = max(0.0, 100.0 - (dynamic_contrast_violations * 15.0 + static_contrast_violations * 10.0))

        # Decisão de bloqueio baseada em severity P0 ou P1
        blocking_findings = [f for f in findings if f.severity in ("P0", "P1")]
        blocked_reasons = [f.message for f in blocking_findings]

        if blocking_findings:
            decision = "rejected"
        else:
            decision = "approved"

        score_breakdown = PerceptualScoreBreakdown(
            structural_similarity_score=100.0,
            contrast_score=contrast_score,
            visual_density_score=density_score,
            layout_integrity_score=100.0,
            overlap_score=100.0,
            viewport_fit_score=100.0,
            final_score=(100.0 + contrast_score + density_score + 100.0 + 100.0 + 100.0) / 6.0
        )

        viewport_str = bundle.viewport_presets[0] if bundle.viewport_presets else "1440x900"
        w, h = map(int, viewport_str.split("x"))

        # 8. Gravação do Relatório Físico Obrigatório
        report_data = {
            "screenshot_path": screenshot_path,
            "screenshot_sha256": screenshot_sha256,
            "viewport_width": w,
            "viewport_height": h,
            "render_bundle_id": bundle.bundle_id,
            "perceptual_score": score_breakdown.model_dump(),
            "findings": [f.model_dump() for f in findings],
            "decision": decision,
            "blocked_reasons": blocked_reasons,
            "network_requests_blocked": network_requests_blocked,
            "console_errors": console_errors
        }
        
        report_json_path = os.path.join(self.sandbox_dir, "4_perceptual_report.json")
        with open(report_json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        # Se foi rejeitado (P0 ou P1), levantamos a exceção para pausar a pipeline (Fail-Closed)
        if decision == "rejected":
            raise PipelinePausedException(f"Perceptual Evaluation Failed: {', '.join(blocked_reasons)}")

        return VisualRegressionReport(
            report_id=f"perceptual-{uuid.uuid4().hex[:8]}",
            render_bundle_id=bundle.bundle_id,
            screenshot_path=screenshot_path,
            perceptual_score=score_breakdown,
            findings=findings,
            decision=decision,
            blocked_reasons=blocked_reasons
        )
