from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal

class LayoutProfileSelection(BaseModel):
    profile: Literal[
        "editorial_field",
        "hero_centric",
        "split_screen",
        "bento_grid",
        "dashboard_grid",
        "dark_editorial",
    ]
    reason: str
    confidence: float
    source_signals: list[str] = Field(default_factory=list)

class UINode(BaseModel):
    node_id: str
    component_name: str  # Renomeado de component_type
    semantic_role: str
    props: dict[str, Any] = Field(default_factory=dict)
    children: list["UINode"] = Field(default_factory=list)
    layout_slot: str | None = None
    fallback_used: bool = False
    fallback_reason: Optional[str] = None
    blueprint_source: Optional[str] = None
    decision_owner: Optional[str] = None
    authority_level: Optional[str] = None
    text_content: Optional[str] = Field(None, description="Texto interno do nó (ex: label de um botão).")


    # Permite recursão estrita no Pydantic V2
    model_config = {"validate_assignment": True}

class ComponentMappingFinding(BaseModel):
    code: str
    severity: Literal["P0", "P1", "P2", "P3"]
    component_name: str
    reason: str
    action: Literal["rendered", "degraded", "blocked"]

class ComponentTree(BaseModel):
    """O artefacto pré-compilação supremo. Apenas AST Pura."""
    spec_id: str = Field(..., description="Rastreabilidade da origem (FrontendCodeSpec).")
    root_node: UINode
    layout_selection: LayoutProfileSelection
    component_findings: list[ComponentMappingFinding] = Field(default_factory=list)

# Resolve referências recursivas para Pydantic V2
UINode.model_rebuild()

class StandaloneRenderBundle(BaseModel):
    bundle_id: str
    ui_tree_hash: str
    client_component_path: str
    page_entry_path: str
    css_entry_path: str | None
    dependencies_mode: Literal["local_pinned"]
    network_allowed: Literal[False]
    viewport_presets: list[str]

