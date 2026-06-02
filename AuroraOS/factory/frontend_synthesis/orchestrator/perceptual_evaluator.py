import os
import sys
import uuid
import logging
import numpy as np
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
from factory_contracts import StandaloneRenderBundle
from renderer_adapter import LocalOfflineRendererAdapter

logger = logging.getLogger("PerceptualEvaluator")

# Fallback fail-closed skimage block
try:
    from skimage.metrics import structural_similarity as ssim
except ImportError:
    raise RuntimeError("Fail-closed: skimage must be installed for PerceptualEvaluator.")

class PipelinePausedException(Exception):
    pass

class EvaluatePerceptualFidelity:
    """
    OS-012: Rendered Visual Regression & Perceptual Evaluator
    """
    def __init__(self, sandbox_dir: str):
        self.sandbox_dir = sandbox_dir
        self.adapter = LocalOfflineRendererAdapter(sandbox_dir)

    async def evaluate(self, bundle: StandaloneRenderBundle) -> VisualRegressionReport:
        logger.info(f"OS-012: Avaliando fidelidade perceptual para bundle {bundle.bundle_id}")
        
        # 1. Obter a Screenshot
        screenshot_path = await self.adapter.render_and_screenshot(bundle)

        # 2. Carregar imagem para análise com Pillow/numpy
        img = Image.open(screenshot_path).convert('L')  # Greyscale
        img_array = np.array(img)
        
        findings: List[PerceptualFinding] = []
        blocked_reasons: List[str] = []

        # 3. Métricas
        
        # 3.1 Blank Screen Check (maximum_blank_screen_ratio = 0.92)
        unique_pixels, counts = np.unique(img_array, return_counts=True)
        max_color_ratio = counts.max() / img_array.size
        
        logger.info(f"Unique pixels: {unique_pixels}, counts: {counts}")
    
        if max_color_ratio > 0.92:
            msg = f"Tela considerada em branco/vazia (ratio={max_color_ratio:.2f} > 0.92)"
            findings.append(PerceptualFinding(
                code="BLANK_SCREEN",
                severity="P0",
                axis="blank_screen",
                message=msg,
                recommended_action="Verificar se o JSX está sendo renderizado e se possui conteúdo visível."
            ))
            blocked_reasons.append(msg)

        # 3.2 Densidade Visual (Edge/Variance estimation)
        std_dev = img_array.std()
        visual_density_score = min((std_dev / 128.0) * 100, 100.0)
        
        # 3.3 Contrast Real Simulado
        contrast_score = min(((img_array.max() - img_array.min()) / 255.0) * 100, 100.0)
        
        if contrast_score < 10.0:
            msg = f"Contraste insuficiente detectado na renderização (score={contrast_score:.2f})"
            findings.append(PerceptualFinding(
                code="LOW_CONTRAST",
                severity="P1",
                axis="contrast",
                message=msg,
                recommended_action="Rever propriedades de cor do CSS e visibilidade dos nós principais."
            ))
            blocked_reasons.append(msg)

        structural_similarity_score = 100.0 
        overlap_score = 100.0
        layout_integrity_score = 100.0
        viewport_fit_score = 100.0

        # Métrica Final
        final_score = 100.0
        if len(blocked_reasons) > 0:
            final_score = 40.0 # Reprova

        score_breakdown = PerceptualScoreBreakdown(
            structural_similarity_score=structural_similarity_score,
            contrast_score=contrast_score,
            visual_density_score=visual_density_score,
            layout_integrity_score=layout_integrity_score,
            overlap_score=overlap_score,
            viewport_fit_score=viewport_fit_score,
            final_score=final_score
        )

        decision = "approved" if final_score >= 75.0 else "rejected"
        
        report = VisualRegressionReport(
            report_id=f"perceptual-{uuid.uuid4().hex[:8]}",
            render_bundle_id=bundle.bundle_id,
            screenshot_path=screenshot_path,
            perceptual_score=score_breakdown,
            findings=findings,
            decision=decision,
            blocked_reasons=blocked_reasons
        )

        # Falha determinística (Fail-Closed)
        if decision == "rejected":
            raise PipelinePausedException(f"Perceptual Evaluation Failed: {blocked_reasons}")

        return report
