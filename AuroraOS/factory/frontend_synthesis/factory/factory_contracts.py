from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal

class UINode(BaseModel):
    node_id: str
    component_type: str = Field(..., description="Mapeamento com ComponentRegistry ou tag HTML (ex: 'div', 'AuroraButton').")
    props: Dict[str, Any] = Field(default_factory=dict, description="Propriedades injetadas no React Component.")
    tailwind_classes: List[str] = Field(default_factory=list, description="Vetor puro de classes governadas.")
    text_content: Optional[str] = Field(None, description="Texto interno do nó (ex: label de um botão).")
    children: Optional[List['UINode']] = Field(None, description="Alofocação recursiva de nós filhos.")

    # Permite recursão estrita no Pydantic V2
    model_config = {"validate_assignment": True}

class ComponentTree(BaseModel):
    """O artefacto pré-compilação supremo. Apenas AST Pura."""
    spec_id: str = Field(..., description="Rastreabilidade da origem (FrontendCodeSpec).")
    root_node: UINode

# Resolve referências recursivas para Pydantic V2
UINode.model_rebuild()

class StandaloneRenderBundle(BaseModel):
    bundle_id: str
    component_code: str
    html_fallback: str
    css_code: str
    tailwind_safelist: list[str]
    viewport: dict[str, int]
    dependencies_mode: Literal["local_pinned"]
    network_allowed: Literal[False]
