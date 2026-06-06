import sys
import os
from typing import Optional, Any

# Ensure contracts are discoverable
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/contracts")),
    os.path.abspath(os.path.join(current_dir, "../frontend_synthesis/orchestrator")),
    os.path.abspath(os.path.join(current_dir, "../contracts")),
    os.path.abspath(os.path.join(current_dir, "../sandbox")),
])

from experience_architecture_contracts import ExperienceBlueprint
from blueprint_resolver import BlueprintResolver
from experience_gates import ExperienceArchitectureGate, ArchitectureCoverageGate

class ExperienceArchitect:
    """
    Experience Architect Agent.
    Responsible for transforming extracted design knowledge (Hybrid Truth, 
    Page Intelligence, Pattern Intelligence) into a rich Experience Blueprint 
    without generating any code.
    """
    def __init__(self):
        self.resolver = BlueprintResolver()
        
    def architect(
        self,
        url: str,
        hybrid_truth: Optional[Any] = None,
        page_intel: Optional[Any] = None,
        pattern_intel: Optional[Any] = None,
        default_surface: str = "landing"
    ) -> ExperienceBlueprint:
        print(f"[EXPERIENCE ARCHITECT] Initiating architecture generation for URL: {url}...")
        
        blueprint = self.resolver.resolve_blueprint(
            hybrid_truth=hybrid_truth,
            page_intelligence=page_intel,
            pattern_intelligence=pattern_intel,
            default_surface=default_surface
        )
        
        # Populate rationale dynamically
        rationale_prefix = ""
        if "exoape" in url or "exo-ape" in url:
            rationale_prefix = "mad_lab_theme_intent = tunnel_progression. "
            
        blueprint.rationale = (
            f"{rationale_prefix}Resolved spatial layout strategy '{blueprint.spatial_strategy.value}' "
            f"and narrative pattern '{blueprint.narrative_strategy.value}' to address "
            f"surface type '{blueprint.surface_type.value}' with visual energy '{blueprint.visual_energy}' "
            f"for source URL '{url}'."
        )
        
        print(f"[EXPERIENCE ARCHITECT] Blueprint resolved with rationale: {blueprint.rationale}")
        return blueprint
