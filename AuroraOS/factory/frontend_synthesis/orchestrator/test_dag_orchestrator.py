import pytest
import os
import sys
import tempfile
import shutil
from unittest.mock import MagicMock

sys.path.extend([
    os.path.abspath(os.path.dirname(__file__)),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../synthesizer')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../factory')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../bff'))
])

from dag_orchestrator import SynthesisDAG, PipelineAbortedException, PipelinePausedException
from models import PageIntelligenceArtifact, ColorSample, A11yNodeSummary

@pytest.fixture
def temp_dir():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)

@pytest.fixture
def mock_artifact():
    artifact = MagicMock(spec=PageIntelligenceArtifact)
    artifact.source_url = "https://example.com"
    artifact.colors = [
        ColorSample(hex_value="#112233", usage_frequency=0.8),
        ColorSample(hex_value="#998877", usage_frequency=0.2)
    ]
    artifact.typography = []
    artifact.a11y_tree = [
        A11yNodeSummary(role="navigation", aria_label_present=True, contrast_ratio=12.0, text_content="Pricing", depth=3),
        A11yNodeSummary(role="button", aria_label_present=True, contrast_ratio=8.1, text_content="Explore", depth=5),
        A11yNodeSummary(role="heading", aria_label_present=True, contrast_ratio=10.0, text_content="Welcome to Antigravity", depth=4)
    ]
    artifact.headings = ["Welcome to Antigravity"]
    artifact.buttons = ["Explore"]
    artifact.links = ["Learn More"]
    artifact.nav_items = ["Pricing"]
    artifact.sections = ["main", "section"]
    artifact.dom_depth = 10
    artifact.visible_texts = ["Welcome to Antigravity", "Explore", "Learn More", "Pricing"]
    artifact.model_dump_json.return_value = "{}"
    return artifact

def _setup_mock_asset_kit(kit_dir):
    os.makedirs(kit_dir, exist_ok=True)
    with open(os.path.join(kit_dir, "Google Antigravity.html"), "w") as f:
        f.write("<html><body>Antigravity</body></html>")
    with open(os.path.join(kit_dir, "asset_kit_manifest.json"), "w") as f:
        f.write('{"kit_name": "Google Antigravity", "html_file": "Google Antigravity.html", "files": []}')

import asyncio

def test_dag_manifest_check_fail(temp_dir):
    dag = SynthesisDAG("https://example.com", os.path.join(temp_dir, "missing.json"), temp_dir)
    with pytest.raises(PipelineAbortedException) as exc:
        dag.validate_pre_conditions()
    assert "API Manifest not found" in str(exc.value)

def test_dag_execution_success(temp_dir, mock_artifact):
    # Setup mock git folder inside temp_dir to force repo_root resolution there
    os.makedirs(os.path.join(temp_dir, ".git"), exist_ok=True)
    
    manifest_path = os.path.join(temp_dir, "api_manifest.json")
    with open(manifest_path, "w") as f:
        f.write('{"antigravity.workspace.status": {"adapter_ref": "antigravity.workspace.status", "method": "GET", "path": "/api/antigravity/v1/workspace", "response_schema": "WorkspaceStatusSchema", "scope": "workspace:read", "tenant_required": true}}')
    
    # Setup mock asset kit directory
    kit_dir = os.path.join(temp_dir, "mock_asset_kit")
    _setup_mock_asset_kit(kit_dir)
    
    output_dir = os.path.join(temp_dir, "output")
    dag = SynthesisDAG("https://example.com", manifest_path, output_dir)
    
    from unittest.mock import patch, MagicMock
    mock_uuid = MagicMock()
    mock_uuid.hex = "c8879f8310"
    
    with patch("uuid.uuid4", return_value=mock_uuid):
        # 1. Negative Case: Expect HumanPromotionHalt without approvals file
        from dag_orchestrator import HumanPromotionHalt
        with pytest.raises(HumanPromotionHalt) as exc_info:
            asyncio.run(dag.execute(
                probe_artifact_mock=mock_artifact,
                asset_kit_mock=kit_dir,
                governance_mode="transmute" # Use transmute to pass OriginalityGate
            ))
        
        assert "Approval record required" in str(exc_info.value)
        
        # Extract run ID and hashes from exception message
        import re
        run_id = re.search(r"sandbox_run_id:\s*(\S+)", str(exc_info.value)).group(1)
        patch_sha = re.search(r"patch_candidate_sha256:\s*(\S+)", str(exc_info.value)).group(1)
        qa_sha = re.search(r"qa_report_sha256:\s*(\S+)", str(exc_info.value)).group(1)
        
        # 2. Positive Case: Write the approvals record to approvals directory
        approval_dir = os.path.join(temp_dir, ".aurora", "approvals")
        os.makedirs(approval_dir, exist_ok=True)
        
        from datetime import datetime
        import json
        approval_data = {
            "promotion_candidate_id": "PC-TEST",
            "sandbox_run_id": run_id,
            "patch_candidate_sha256": patch_sha,
            "qa_report_sha256": qa_sha,
            "approved_by": "Operator",
            "approved_at": datetime.now().isoformat(),
            "approval_nonce": "nonce-123",
            "approval_source": "manual_cli"
        }
        
        with open(os.path.join(approval_dir, "promotion_approval.json"), "w") as f:
            json.dump(approval_data, f)
            
        # Execute again: should pass HumanPromotionGate and authorize promotion
        results = asyncio.run(dag.execute(
            probe_artifact_mock=mock_artifact,
            asset_kit_mock=kit_dir,
            governance_mode="transmute"
        ))
        
        assert results.get("promotion_authorized") is True
        assert "resolved_truth" in results
        assert "draft" in results
        assert "code_spec" in results
        assert "ui_tree" in results
        assert "client_code" in results

def test_dag_pause_on_critical_conflict(temp_dir, mock_artifact):
    manifest_path = os.path.join(temp_dir, "api_manifest.json")
    with open(manifest_path, "w") as f:
        f.write('{"antigravity.workspace.status": {"adapter_ref": "antigravity.workspace.status", "method": "GET", "path": "/api/antigravity/v1/workspace", "response_schema": "WorkspaceStatusSchema", "scope": "workspace:read", "tenant_required": true}}')
    
    kit_dir = os.path.join(temp_dir, "mock_asset_kit")
    _setup_mock_asset_kit(kit_dir)
    
    dag = SynthesisDAG("https://example.com", manifest_path, os.path.join(temp_dir, "output"))
    
    probe_mock = mock_artifact
    # We trigger conflict on html_hash since it's in the kit output and not in priority keys
    probe_truth_mock = {"html_hash": "different_conflict_hash"}
    
    with pytest.raises(PipelinePausedException) as exc:
        asyncio.run(dag.execute(
            probe_artifact_mock=probe_mock,
            asset_kit_mock=kit_dir,
            governance_mode="transmute",
            probe_truth_mock=probe_truth_mock
        ))
    assert "ResolveTruth pausado" in str(exc.value) or "ResolveTruth paused" in str(exc.value)
