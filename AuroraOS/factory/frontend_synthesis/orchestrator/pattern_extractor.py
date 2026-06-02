import hashlib
import json
import datetime
from typing import List, Dict, Any
from transmutation_contracts import SourcePattern, SourceFingerprint

class SourcePatternExtractor:
    """
    Extrai padrões atômicos e abstrações estruturais do TruthResolutionResult.
    Produz a assinatura `SourceFingerprint` para a governança do Originality Gate.
    """
    def __init__(self, resolution_result):
        self.result = resolution_result
        self.resolved_data = getattr(resolution_result, "resolved_data", {})

    def _hash_list(self, items: List[Any]) -> str:
        s = json.dumps(items, sort_keys=True).encode("utf-8")
        return hashlib.sha256(s).hexdigest()
        
    def _hash_dict(self, d: Dict[str, Any]) -> str:
        s = json.dumps(d, sort_keys=True).encode("utf-8")
        return hashlib.sha256(s).hexdigest()

    def generate_fingerprint(self) -> SourceFingerprint:
        layout = self.resolved_data.get("layout_viewport", {})
        layout_items = [{"prop": k, "val": v} for k, v in layout.items()]
        layout_hash = self._hash_list(layout_items)
        
        computed = self.resolved_data.get("computed_styles", {})
        color_items = [{"hex": c} for c in computed.get("colors", [])]
        color_hash = self._hash_list(color_items)
        
        typo_items = []
        typo_hash = self._hash_list(typo_items)
        
        motion_items = []
        motion_hash = self._hash_list(motion_items)
        
        component_names = []
        
        asset_paths = self.resolved_data.get("asset_paths", {})
        asset_hashes = list(asset_paths.values()) if isinstance(asset_paths, dict) else []
        
        base_hash = self._hash_dict({"resolved_at": datetime.datetime.now().isoformat()})
        
        return SourceFingerprint(
            source_artifact_hash=base_hash,
            layout_hash=layout_hash,
            color_palette_hash=color_hash,
            typography_hash=typo_hash,
            motion_hash=motion_hash,
            asset_hashes=asset_hashes,
            text_hashes=[],
            component_names=component_names
        )

    def extract_patterns(self) -> List[SourcePattern]:
        patterns = []
        base_hash = self.generate_fingerprint().source_artifact_hash
        
        computed = self.resolved_data.get("computed_styles", {})
        for c in computed.get("colors", []):
            patterns.append(SourcePattern(
                pattern_id=f"color-{c[1:]}",
                source_artifact_hash=base_hash,
                pattern_type="color",
                extracted_principle=f"Cor extraída",
                raw_reference=c
            ))
            
        patterns.append(SourcePattern(
            pattern_id="layout-system",
            source_artifact_hash=base_hash,
            pattern_type="layout",
            extracted_principle="Sistema de espacamento baseado em métricas computadas.",
            raw_reference=json.dumps(self.resolved_data.get("layout_viewport", {}))
        ))

        return patterns
