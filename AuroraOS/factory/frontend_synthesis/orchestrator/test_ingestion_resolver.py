import sys
import os
import pytest
from pathlib import Path

# Adjust paths
sys.path.extend([
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sandbox')),
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ingestion'))
])

from kit_ingestor import KitIngestor, KitParserException
from truth_resolver import HybridTruthResolver
from sandbox_contracts import PipelinePausedException

@pytest.fixture
def mock_staging_dir(tmp_path):
    staging = tmp_path / "staging"
    staging.mkdir()
    
    # Create HTML
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="Google Antigravity_files/styles.css" rel="stylesheet">
        <script src="http://evil.com/script.js"></script>
    </head>
    <body>
        <img src="Google Antigravity_files/logo.png">
    </body>
    </html>
    """
    html_file = staging / "Google Antigravity.html"
    html_file.write_text(html_content, encoding='utf-8')
    
    # Create Manifest
    manifest_file = staging / "asset_kit_manifest.json"
    manifest_file.write_text('{"version": "1.0"}', encoding='utf-8')
    
    # Create files directory
    files_dir = staging / "Google Antigravity_files"
    files_dir.mkdir()
    
    css_content = """
    :root {
        --palette-primary: #000000;
        --theme-bg: #FFFFFF;
    }
    body {
        font-family: "Inter", sans-serif;
    }
    @media (max-width: 768px) {
        .container { padding: 10px; }
    }
    /* Comment with malicious script <script> */
    """
    css_file = files_dir / "styles.css"
    css_file.write_text(css_content, encoding='utf-8')
    
    # Logo
    logo_file = files_dir / "logo.png"
    logo_file.write_text("fake binary", encoding='utf-8')
    
    return staging

def test_kit_ingestion_parsing(mock_staging_dir):
    ingestor = KitIngestor(staging_dir=mock_staging_dir, kit_name="Google Antigravity")
    artifact = ingestor.ingest()
    
    # Assert variables
    assert artifact.css_variables.get("--palette-primary") == "#000000"
    assert artifact.css_variables.get("--theme-bg") == "#FFFFFF"
    
    # Assert fonts
    assert '"Inter", sans-serif' in artifact.font_declarations
    
    # Assert breakpoints
    assert len(artifact.breakpoints) == 1
    assert artifact.breakpoints["breakpoint_0"] == "(max-width: 768px)"
    
    # Assert assets
    assert "Google Antigravity_files/styles.css" in artifact.asset_paths
    assert "Google Antigravity_files/logo.png" in artifact.asset_paths

def test_kit_ingestion_path_traversal(mock_staging_dir):
    # Try to include a file outside staging
    html_file = mock_staging_dir / "Google Antigravity.html"
    html_file.write_text('<link href="../../../../../Windows/System32/cmd.exe">', encoding='utf-8')
    
    ingestor = KitIngestor(staging_dir=mock_staging_dir, kit_name="Google Antigravity")
    artifact = ingestor.ingest()
    
    # Path traversal should be ignored/caught safely and not added to assets
    assert "../../../../../Windows/System32/cmd.exe" not in artifact.asset_paths

def test_hybrid_truth_resolver_weights():
    resolver = HybridTruthResolver()
    
    probe_data = {
        "css_variables": {"--palette-primary": "#FFFFFF"}, # Probe trying to override Kit
        "layout_viewport": {"height": "100vh"}             # Probe domain
    }
    
    kit_data = {
        "css_variables": {"--palette-primary": "#000000"}, # Kit domain
        "layout_viewport": {"height": "50vh"}              # Kit trying to override Probe
    }
    
    resolution = resolver.resolve(probe_data, kit_data)
    
    # Kit wins css_variables
    assert resolution.resolved_data["css_variables"] == {"--palette-primary": "#000000"}
    assert resolution.conflicts["css_variables"].resolution_source == "kit"
    
    # Probe wins layout_viewport
    assert resolution.resolved_data["layout_viewport"] == {"height": "100vh"}
    assert resolution.conflicts["layout_viewport"].resolution_source == "probe"
    
    assert not resolution.has_critical_conflicts

def test_hybrid_truth_resolver_critical_conflict():
    resolver = HybridTruthResolver()
    
    probe_data = {
        "unknown_structural_key": "PROBE_VALUE"
    }
    
    kit_data = {
        "unknown_structural_key": "KIT_VALUE"
    }
    
    with pytest.raises(PipelinePausedException) as exc_info:
        resolver.resolve(probe_data, kit_data)
        
    assert "Conflito Crítico" in str(exc_info.value)
    assert len(exc_info.value.findings) == 1
    assert exc_info.value.findings[0].severity == "P1"
