import os
import sys
import pytest
import json
from pydantic import ValidationError
from unittest.mock import AsyncMock, patch
from PIL import Image, ImageDraw

sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../factory'))
])

from factory_contracts import StandaloneRenderBundle, UINode
from perceptual_evaluator import EvaluatePerceptualFidelity, PipelinePausedException

def _setup_sandbox_files(sandbox_dir, root_node, css_content=""):
    os.makedirs(sandbox_dir, exist_ok=True)
    
    ui_tree_data = {
        "spec_id": "TEST-SPEC",
        "root_node": root_node.model_dump()
    }
    
    with open(os.path.join(sandbox_dir, "ui_tree.json"), "w", encoding="utf-8") as f:
        json.dump(ui_tree_data, f)
        
    with open(os.path.join(sandbox_dir, "5_SynthesizedPage.client.tsx"), "w", encoding="utf-8") as f:
        f.write("// Client")
        
    with open(os.path.join(sandbox_dir, "5_page.tsx"), "w", encoding="utf-8") as f:
        f.write("// Page")
        
    # Sempre gravar o arquivo CSS para evitar FileNotFoundError se estiver descrito no bundle
    with open(os.path.join(sandbox_dir, "render_bundle.css"), "w", encoding="utf-8") as f:
        f.write(css_content)
        
    with open(os.path.join(sandbox_dir, "render_bundle_manifest.json"), "w", encoding="utf-8") as f:
        f.write("{}")

def _create_non_blank_png(path):
    img = Image.new("RGB", (1440, 900), color="white")
    draw = ImageDraw.Draw(img)
    # Desenhar formas pretas para gerar variancia, bordas e cobertura significativos
    draw.rectangle([50, 50, 200, 200], fill="black")
    draw.rectangle([300, 300, 500, 500], fill="gray")
    img.save(path, "PNG")

def _create_blank_png(path):
    img = Image.new("RGB", (1440, 900), color="white")
    img.save(path, "PNG")

@pytest.mark.asyncio
async def test_perceptual_evaluator_missing_files(tmp_path):
    root = UINode(
        node_id="root",
        component_name="div",
        semantic_role="main",
        props={"className": "min-h-screen"}
    )
    
    bundle = StandaloneRenderBundle(
        bundle_id="test-missing",
        ui_tree_hash="hash-missing",
        client_component_path="5_SynthesizedPage.client.tsx",
        page_entry_path="5_page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"]
    )
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    # Deve falhar logo na validacao fisica (FileNotFoundError)
    with pytest.raises(FileNotFoundError) as exc:
        await evaluator.evaluate(bundle)
        
    assert "Candidato em falta no sandbox" in str(exc.value) or "Manifesto em falta" in str(exc.value) or "Estilos em falta" in str(exc.value)

@pytest.mark.asyncio
async def test_perceptual_evaluator_network_violation(tmp_path):
    with pytest.raises(ValidationError) as exc:
        StandaloneRenderBundle(
            bundle_id="test-network-violation",
            ui_tree_hash="hash-net",
            client_component_path="5_SynthesizedPage.client.tsx",
            page_entry_path="5_page.tsx",
            css_entry_path="render_bundle.css",
            dependencies_mode="local_pinned",
            network_allowed=True, # Violacao
            viewport_presets=["1440x900"]
        )
    assert "network_allowed" in str(exc.value)

@pytest.mark.asyncio
async def test_perceptual_evaluator_dependencies_violation(tmp_path):
    with pytest.raises(ValidationError) as exc:
        StandaloneRenderBundle(
            bundle_id="test-deps-violation",
            ui_tree_hash="hash-deps",
            client_component_path="5_SynthesizedPage.client.tsx",
            page_entry_path="5_page.tsx",
            css_entry_path="render_bundle.css",
            dependencies_mode="cdn_resolved", # Violacao
            network_allowed=False,
            viewport_presets=["1440x900"]
        )
    assert "dependencies_mode" in str(exc.value)

@pytest.mark.asyncio
async def test_perceptual_evaluator_blank_screen_rejection(tmp_path):
    root = UINode(
        node_id="root",
        component_name="div",
        semantic_role="main",
        props={"className": "min-h-screen"}
    )
    _setup_sandbox_files(str(tmp_path), root)
    
    bundle = StandaloneRenderBundle(
        bundle_id="test-blank",
        ui_tree_hash="hash-blank",
        client_component_path="5_SynthesizedPage.client.tsx",
        page_entry_path="5_page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"]
    )
    
    screenshot_file = os.path.join(str(tmp_path), "6_rendered_screenshot.png")
    
    # Criar um screenshot em branco (Luma std = 0, edge density = 0)
    _create_blank_png(screenshot_file)
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    # Mock do adapter para retornar o screenshot branco
    mock_render_result = {
        "screenshot_path": screenshot_file,
        "console_errors": [],
        "network_requests_blocked": [],
        "page_errors": []
    }
    
    with patch("perceptual_evaluator.LocalOfflineRendererAdapter.render_and_screenshot", new_callable=AsyncMock) as mock_render:
        mock_render.return_value = mock_render_result
        
        with pytest.raises(PipelinePausedException) as exc:
            await evaluator.evaluate(bundle)
            
        assert "Tela em branco detectada" in str(exc.value)

@pytest.mark.asyncio
async def test_perceptual_evaluator_console_error_rejection(tmp_path):
    root = UINode(
        node_id="root",
        component_name="div",
        semantic_role="main",
        props={"className": "min-h-screen"}
    )
    _setup_sandbox_files(str(tmp_path), root)
    
    bundle = StandaloneRenderBundle(
        bundle_id="test-console-error",
        ui_tree_hash="hash-console",
        client_component_path="5_SynthesizedPage.client.tsx",
        page_entry_path="5_page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"]
    )
    
    screenshot_file = os.path.join(str(tmp_path), "6_rendered_screenshot.png")
    _create_non_blank_png(screenshot_file)
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    # Mock do adapter com erro de console
    mock_render_result = {
        "screenshot_path": screenshot_file,
        "console_errors": ["TypeError: Cannot read property 'map' of undefined"],
        "network_requests_blocked": [],
        "page_errors": []
    }
    
    with patch("perceptual_evaluator.LocalOfflineRendererAdapter.render_and_screenshot", new_callable=AsyncMock) as mock_render:
        mock_render.return_value = mock_render_result
        
        with pytest.raises(PipelinePausedException) as exc:
            await evaluator.evaluate(bundle)
            
        assert "Erro de console no browser" in str(exc.value)

@pytest.mark.asyncio
async def test_perceptual_evaluator_network_leak_rejection(tmp_path):
    root = UINode(
        node_id="root",
        component_name="div",
        semantic_role="main",
        props={"className": "min-h-screen"}
    )
    _setup_sandbox_files(str(tmp_path), root)
    
    bundle = StandaloneRenderBundle(
        bundle_id="test-network-leak",
        ui_tree_hash="hash-leak",
        client_component_path="5_SynthesizedPage.client.tsx",
        page_entry_path="5_page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"]
    )
    
    screenshot_file = os.path.join(str(tmp_path), "6_rendered_screenshot.png")
    _create_non_blank_png(screenshot_file)
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    # Mock do adapter com fuga de rede
    mock_render_result = {
        "screenshot_path": screenshot_file,
        "console_errors": [],
        "network_requests_blocked": ["https://cdn.example.com/malicious-script.js"],
        "page_errors": []
    }
    
    with patch("perceptual_evaluator.LocalOfflineRendererAdapter.render_and_screenshot", new_callable=AsyncMock) as mock_render:
        mock_render.return_value = mock_render_result
        
        with pytest.raises(PipelinePausedException) as exc:
            await evaluator.evaluate(bundle)
            
        assert "Fuga de rede detectada e bloqueada" in str(exc.value)

@pytest.mark.asyncio
async def test_perceptual_evaluator_success(tmp_path):
    root = UINode(
        node_id="root",
        component_name="div",
        semantic_role="main",
        props={"className": "min-h-screen"},
        children=[
            UINode(node_id="header", component_name="header", semantic_role="banner"),
            UINode(node_id="content", component_name="p", semantic_role="document")
        ]
    )
    _setup_sandbox_files(str(tmp_path), root, css_content=".bg-canvas { background-color: #0d0d0d; }\n.text-accent { color: #ffffff; }")
    
    bundle = StandaloneRenderBundle(
        bundle_id="test-success",
        ui_tree_hash="hash-ok",
        client_component_path="5_SynthesizedPage.client.tsx",
        page_entry_path="5_page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"]
    )
    
    screenshot_file = os.path.join(str(tmp_path), "6_rendered_screenshot.png")
    _create_non_blank_png(screenshot_file)
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    # Mock do adapter com render valido e sem erros
    mock_render_result = {
        "screenshot_path": screenshot_file,
        "console_errors": [],
        "network_requests_blocked": [],
        "page_errors": []
    }
    
    with patch("perceptual_evaluator.LocalOfflineRendererAdapter.render_and_screenshot", new_callable=AsyncMock) as mock_render:
        mock_render.return_value = mock_render_result
        
        report = await evaluator.evaluate(bundle)
        assert report.decision == "approved"
        assert report.perceptual_score.final_score > 50.0
        assert os.path.exists(report.screenshot_path)
        
        # Validar gravacao do relatorio fisico 4_perceptual_report.json
        report_json_path = os.path.join(str(tmp_path), "4_perceptual_report.json")
        assert os.path.exists(report_json_path)
        
        with open(report_json_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
            assert report_data["decision"] == "approved"
            assert report_data["screenshot_sha256"] != ""
            assert len(report_data["console_errors"]) == 0

@pytest.mark.asyncio
async def test_perceptual_evaluator_contrast_p1_rejection(tmp_path):
    root = UINode(
        node_id="root",
        component_name="div",
        semantic_role="main",
        props={"className": "min-h-screen"}
    )
    _setup_sandbox_files(str(tmp_path), root)
    
    bundle = StandaloneRenderBundle(
        bundle_id="test-contrast-p1",
        ui_tree_hash="hash-contrast-p1",
        client_component_path="5_SynthesizedPage.client.tsx",
        page_entry_path="5_page.tsx",
        css_entry_path="render_bundle.css",
        dependencies_mode="local_pinned",
        network_allowed=False,
        viewport_presets=["1440x900"]
    )
    
    screenshot_file = os.path.join(str(tmp_path), "6_rendered_screenshot.png")
    _create_non_blank_png(screenshot_file)
    
    evaluator = EvaluatePerceptualFidelity(str(tmp_path))
    
    # Mock do adapter com elemento de texto de baixo contraste (cinza sobre cinza claro)
    mock_render_result = {
        "screenshot_path": screenshot_file,
        "console_errors": [],
        "network_requests_blocked": [],
        "page_errors": [],
        "text_elements_style": [
            {
                "tagName": "P",
                "id": "low-contrast-text",
                "className": "text-gray-400 bg-gray-300",
                "color": "rgb(150, 150, 150)",
                "backgroundColor": "rgb(170, 170, 170)",
                "fontSize": "16px",
                "fontWeight": "normal",
                "textContent": "Insuficiente contraste aqui"
            }
        ]
    }
    
    with patch("perceptual_evaluator.LocalOfflineRendererAdapter.render_and_screenshot", new_callable=AsyncMock) as mock_render:
        mock_render.return_value = mock_render_result
        
        with pytest.raises(PipelinePausedException) as exc:
            await evaluator.evaluate(bundle)
            
        assert "Contraste insuficiente no elemento" in str(exc.value)

