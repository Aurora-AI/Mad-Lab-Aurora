import re
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, HttpUrl

class ColorSample(BaseModel):
    hex_value: str = Field(..., description="Cor estrita em formato HEX para evitar injeção de CSS sujo ou classes arbitrárias.")
    usage_frequency: float = Field(..., description="Percentagem de uso detetada na UI global.")
    semantic_guess: Optional[str] = Field(None, description="Tentativa de inferência semântica do Probe (ex: 'action-primary-bg').")

    @field_validator('hex_value')
    @classmethod
    def validate_hex(cls, v: str) -> str:
        if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', v):
            raise ValueError("Violação de Governança: O valor da cor deve ser um HEX válido. RGBA ou nomes de cores mascarados não são permitidos.")
        return v.upper()

class TypographyNode(BaseModel):
    font_family: str = Field(..., description="Declaração da família tipográfica extraída.")
    weight: int = Field(..., ge=100, le=900, description="Peso matemático da fonte (100 a 900).")
    size_px: float = Field(..., description="Tamanho absoluto computado em píxeis.")
    line_height: float = Field(..., description="Altura da linha computada.")

    @field_validator('font_family')
    @classmethod
    def require_fallback(cls, v: str) -> str:
        if ',' not in v:
            raise ValueError("Violação de Tipografia: A declaração de font-family deve conter uma fonte de fallback genérica (ex: 'Inter, sans-serif').")
        return v

class SpatialMetric(BaseModel):
    property_name: str = Field(..., description="Propriedade medida (ex: padding-left, gap, margin-bottom).")
    value_px: float = Field(..., description="Valor limpo computado em píxeis absolutos.")
    occurrence_count: int = Field(..., description="Frequência de repetição desta métrica para identificar escalas.")

class MotionSample(BaseModel):
    duration_ms: int = Field(..., description="Tempo da transição ou animação em milissegundos.")
    easing_function: str = Field(..., description="Curva de Bézier ou keyword computada (ex: 'cubic-bezier(0.4, 0, 0.2, 1)').")
    target_property: str = Field(..., description="O que está a ser animado (ex: 'transform', 'opacity').")

class A11yNodeSummary(BaseModel):
    role: str = Field(..., description="Papel semântico do nó (ex: 'button', 'navigation').")
    aria_label_present: bool = Field(..., description="Indica se o nó interativo possui rótulo acessível.")
    contrast_ratio: float = Field(..., description="Taxa de contraste calculada segundo a WCAG.")
    
    # NOVAS PROPRIEDADES DE INTEGRIDADE E CONTEXTO (OS-016)
    depth: int = Field(default=1, description="Profundidade do nó na árvore DOM original.")
    text_content: Optional[str] = Field(None, description="Conteúdo textual original do nó.")

class PageIntelligenceArtifact(BaseModel):
    """
    Contrato Central Read-Only. 
    Designação de Modo: pattern_synthesis
    O Artefacto definitivo que será passado ao Synthesizer (OS-002).
    """
    source_url: HttpUrl
    extracted_at: datetime
    colors: List[ColorSample]
    typography: List[TypographyNode]
    spatial_system: List[SpatialMetric]
    motion: List[MotionSample]
    a11y_tree: List[A11yNodeSummary]
    dom_hierarchy_snapshot: str = Field(..., description="Hash ou resumo topológico da árvore para deteção de layout e governança.")
    
    # Real Structural Probe Fields (OS-015)
    visible_texts: List[str] = Field(default_factory=list)
    headings: List[str] = Field(default_factory=list)
    buttons: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)
    nav_items: List[str] = Field(default_factory=list)
    sections: List[str] = Field(default_factory=list)
    landmarks: List[str] = Field(default_factory=list)
    bounding_boxes: Dict[str, Any] = Field(default_factory=dict)
    computed_styles: Dict[str, Any] = Field(default_factory=dict)
    dom_depth: int = Field(default=0)
    above_the_fold_elements: List[str] = Field(default_factory=list)
    viewport_metrics: Dict[str, Any] = Field(default_factory=dict)
    is_synthetic: bool = Field(default=False, description="Flag indicating if this is a synthetic artifact (mock/fixture)")
    crawler_tls_policy: Optional[Dict[str, Any]] = Field(default=None, description="Audit trail for TLS/SSL bypass policies used during crawl")

from enum import Enum

class ProvenanceWinner(str, Enum):
    KIT = "kit"
    PROBE = "probe"
    HUMAN = "human"

class ResolvedField(BaseModel):
    winner: ProvenanceWinner = Field(..., description="A fonte que venceu a resolução do conflito.")
    loser_value: Optional[Any] = Field(None, description="O valor que foi descartado.")
    reason: str = Field(..., description="Justificativa para a resolução.")
    confidence: float = Field(..., description="Score de confiança de 0.0 a 1.0.")

class AssetKitArtifact(BaseModel):
    """
    Contrato para o Asset Kit ingerido estaticamente.
    """
    source_path: str = Field(..., description="Caminho seguro e resolvido para o kit ingerido.")
    extracted_at: datetime
    css_variables: Dict[str, str] = Field(default_factory=dict, description="Variáveis CSS extraídas.")
    breakpoints: Dict[str, str] = Field(default_factory=dict, description="Media queries / breakpoints extraídos.")
    font_declarations: List[str] = Field(default_factory=list, description="Famílias de fontes extraídas.")
    asset_paths: Dict[str, str] = Field(default_factory=dict, description="Caminhos locais de assets validados.")
    html_hash: Optional[str] = Field(None, description="SHA256 do arquivo HTML principal.")
    css_hashes: Dict[str, str] = Field(default_factory=dict, description="SHA256 de cada arquivo CSS.")
    asset_hashes: Dict[str, str] = Field(default_factory=dict, description="SHA256 dos assets validados.")
    remote_resources: List[str] = Field(default_factory=list, description="URLs externos catalogados mas nunca baixados.")
    scripts_cataloged: List[str] = Field(default_factory=list, description="Tags <script> encontradas, catalogadas mas não executadas.")
    is_synthetic: bool = Field(default=False, description="Flag indicating if this is a synthetic artifact (mock/fixture)")

class HybridTruthArtifact(BaseModel):
    """
    Contrato para a verdade de design unificada (Hybrid Truth).
    """
    resolved_at: datetime
    resolved_fields: Dict[str, ResolvedField] = Field(description="Proveniência de cada campo resolvido.")
    
    # Dados combinados
    colors: List[ColorSample]
    typography: List[TypographyNode]
    spatial_system: List[SpatialMetric]
    motion: List[MotionSample]
    a11y_tree: List[A11yNodeSummary]
    
    # Dados priorizados do Kit
    css_variables: Dict[str, str]
    breakpoints: Dict[str, str]
    asset_paths: Dict[str, str]
    is_synthetic: bool = Field(default=False, description="Flag indicating if this is a synthetic artifact (mock/fixture)")

