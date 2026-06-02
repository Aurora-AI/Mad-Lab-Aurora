from datetime import datetime

SYNTHETIC_PROBE_OUTPUT = {
    "source_url": "https://competitor-quiet-luxury.example.com",
    "extracted_at": datetime.now().isoformat(),
    "colors": [
        {"hex_value": "#0F0F13", "usage_frequency": 60.5, "semantic_guess": "surface-background"},
        {"hex_value": "#FAFAFA", "usage_frequency": 30.0, "semantic_guess": "text-primary"},
        {"hex_value": "#4A3FF4", "usage_frequency": 9.5, "semantic_guess": "action-primary"}
    ],
    "typography": [
        {"font_family": "Geist, system-ui, sans-serif", "weight": 400, "size_px": 16.0, "line_height": 24.0},
        {"font_family": "Geist, system-ui, sans-serif", "weight": 600, "size_px": 24.0, "line_height": 32.0}
    ],
    "spatial_system": [
        {"property_name": "padding", "value_px": 16.0, "occurrence_count": 84},
        {"property_name": "gap", "value_px": 8.0, "occurrence_count": 45}
    ],
    "motion": [
        {"duration_ms": 250, "easing_function": "cubic-bezier(0.16, 1, 0.3, 1)", "target_property": "all"}
    ],
    "a11y_tree": [
        {"role": "button", "aria_label_present": True, "contrast_ratio": 8.1},
        {"role": "navigation", "aria_label_present": True, "contrast_ratio": 12.0}
    ],
    "dom_hierarchy_snapshot": "SHA256:8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4"
}
