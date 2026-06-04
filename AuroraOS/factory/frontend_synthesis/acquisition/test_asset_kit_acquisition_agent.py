import pytest
import os
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from asset_kit_acquisition_agent import AssetKitAcquisitionAgent

def test_is_allowed_filtering():
    agent = AssetKitAcquisitionAgent("https://antigravity.google/")
    # Allowed domains and subdomains
    assert agent._is_allowed("https://antigravity.google/styles.css")
    assert agent._is_allowed("https://fonts.gstatic.com/font.woff")
    assert agent._is_allowed("https://fonts.googleapis.com/css")
    assert agent._is_allowed("https://something.googleusercontent.com/img.png")
    
    # Not allowed
    assert not agent._is_allowed("https://evil.com/script.js")
    assert not agent._is_allowed("https://analytics.google.com/tracking.js")

@pytest.mark.asyncio
async def test_acquire_mocked(tmp_path):
    agent = AssetKitAcquisitionAgent("https://antigravity.google/", output_root=str(tmp_path))
    
    # Mock Playwright objects
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    
    mock_browser.new_context.return_value = mock_context
    mock_context.new_page.return_value = mock_page
    mock_page.content.return_value = "<html><body>Test Page <link href='https://antigravity.google/styles.css' rel='stylesheet'></body></html>"
    mock_page.goto = AsyncMock()
    mock_page.on = MagicMock()
    mock_browser.close = AsyncMock()
    
    with patch("asset_kit_acquisition_agent.async_playwright") as mock_ap:
        mock_playwright_instance = MagicMock()
        mock_playwright_instance.chromium.launch = AsyncMock(return_value=mock_browser)
        
        # Make the async context manager return our mocked instance
        mock_ap.return_value.__aenter__.return_value = mock_playwright_instance
        
        # Execute the acquisition method
        manifest_path = await agent.acquire()
        
        # Validate that folders and manifest files were created
        assert manifest_path.exists()
        assert (agent.kit_dir / "asset_kit_manifest.json").exists()
        assert (agent.kit_dir / "network_log.json").exists()
        assert (agent.kit_dir / "acquisition_report.json").exists()
        assert (agent.kit_dir / "source.html").exists()
        
        with open(agent.kit_dir / "asset_kit_manifest.json", "r") as f:
            manifest_data = json.load(f)
            assert manifest_data["source_url"] == "https://antigravity.google/"
            assert manifest_data["html_file"] == "source.html"
            assert manifest_data["script_execution_allowed"] is False
