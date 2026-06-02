import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from truth_resolver_mock import MockTruthResolver

def test_hybrid_weighted_policy():
    resolver = MockTruthResolver()
    
    # 1. Test Kit wins for declared truths
    probe_data = {
        "css_variables": {"color": "#000"},
        "font_declarations": {"family": "Comic Sans"}
    }
    asset_kit_data = {
        "css_variables": {"color": "#fff"},
        "font_declarations": {"family": "Inter"}
    }
    
    res = resolver.resolve(probe_data, asset_kit_data)
    assert res.resolved_data["css_variables"] == {"color": "#fff"}
    assert res.resolved_data["font_declarations"] == {"family": "Inter"}
    assert res.conflicts["css_variables"].resolution_source == "kit"
    assert not res.has_critical_conflicts

    # 2. Test Probe wins for rendered truths
    probe_data_2 = {
        "computed_styles": {"color": "rgb(0, 0, 0)"},
        "layout_viewport": {"height": "100vh"}
    }
    asset_kit_data_2 = {
        "computed_styles": {"color": "rgb(255, 255, 255)"},
        "layout_viewport": {"height": "80vh"}
    }
    res_2 = resolver.resolve(probe_data_2, asset_kit_data_2)
    assert res_2.resolved_data["computed_styles"] == {"color": "rgb(0, 0, 0)"}
    assert res_2.resolved_data["layout_viewport"] == {"height": "100vh"}
    assert res_2.conflicts["computed_styles"].resolution_source == "probe"
    assert not res_2.has_critical_conflicts

def test_critical_conflict_escalation():
    resolver = MockTruthResolver()
    
    # 3. Test Critical Conflict escalates
    probe_data = {"unknown_random_style_property": "red"}
    asset_kit_data = {"unknown_random_style_property": "blue"}
    
    res = resolver.resolve(probe_data, asset_kit_data)
    assert res.has_critical_conflicts
    assert res.conflicts["unknown_random_style_property"].needs_escalation == True
    assert res.conflicts["unknown_random_style_property"].resolution_source == "manual"
