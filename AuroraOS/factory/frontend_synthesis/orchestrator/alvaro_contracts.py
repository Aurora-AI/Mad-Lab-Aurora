import re
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict

class TailwindThemeSpec(BaseModel):
    """Mapeamento determinístico para o ficheiro tailwind.config.js da fábrica."""
    colors: Dict[str, str] = Field(..., description="Chaves semânticas (ex: 'base-surface') mapeadas para HEX.")
    fontFamily: Dict[str, List[str]] = Field(..., description="Stack tipográfica governada e segura.")
    fontSize: Dict[str, str] = Field(..., description="Escala modular em rem.")

    @field_validator('colors')
    @classmethod
    def validate_hex_colors(cls, v: Dict[str, str]) -> Dict[str, str]:
        for key, value in v.items():
            if not re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value):
                raise ValueError(f"Violação de Code Spec: A cor {key} não é um HEX válido ({value}).")
        return v

    @field_validator('fontSize')
    @classmethod
    def validate_rem_units(cls, v: Dict[str, str]) -> Dict[str, str]:
        for key, value in v.items():
            if not (value.endswith('rem') or (value.startswith('clamp(') and 'rem' in value)):
                raise ValueError(f"Violação Espacial: O tamanho de fonte {key} deve usar 'rem'. Valor recebido: {value}")
        return v

    @field_validator('fontFamily')
    @classmethod
    def validate_fallback_stack(cls, v: Dict[str, List[str]]) -> Dict[str, List[str]]:
        for key, stack in v.items():
            if len(stack) < 2:
                raise ValueError(f"Violação de Tipografia: A stack {key} deve conter no mínimo uma fonte primária e um fallback. Recebido: {stack}")
        return v

class ComponentRequirement(BaseModel):
    """Registo de componentes da biblioteca Aurora necessários para montar o ecrã."""
    component_name: str = Field(..., description="Nome exato do componente (ex: 'AuroraButton', 'AuroraCard').")
    required_variants: List[str] = Field(..., description="Variantes identificadas (ex: ['primary', 'outline', 'ghost']).")
    is_core_library: bool = Field(default=True, description="Garante que não estamos a criar componentes do zero desnecessariamente.")
    
    # NOVAS PROPRIEDADES SEMÂNTICAS (OS-016)
    label: str = Field(default="Ação", description="Rótulo original ou semântico.")
    semantic_role: str = Field(default="generic", description="Papel semântico correspondente.")
    content_function: str = Field(default="content_placeholder", description="Função textual do componente.")
    source_reference_id: str = Field(default="ref_none", description="ID de referência na página original.")
    transformed_text: str = Field(default="Transmuted Text", description="Texto transmutado para o ecossistema Aurora.")
    section_group: str = Field(default="default_section", description="Seção à qual pertence na composição.")

class ComponentMissingAlert(BaseModel):
    """Selo de Governança: Disparado quando um role não existe na biblioteca Aurora."""
    original_role: str = Field(..., description="Papel semântico original da a11y_tree.")
    degraded_to: str = Field(..., description="Elemento primitivo de fallback (ex: 'div', 'span').")
    reason: str = Field(..., description="Motivo detalhado da degradação.")

class ScaffoldingResolution(BaseModel):
    """Gestor de Dívida Técnica (Regra P1). Mantém o rasto dos mocks da OS-001."""
    target_os: str = Field(default="OS-003", description="A OS responsável pela gestão do rasto.")
    pending_injectors: List[str] = Field(..., description="Módulos que ainda operam em modo mock (ex: ['motion']).")
    resolution_status: str = Field(..., description="Estado atual da dívida (ex: 'PARTIALLY_RESOLVED').")

class FrontendCodeSpec(BaseModel):
    """
    Contrato Central do Orquestrador (Álvaro).
    Este é o artefacto definitivo que será injetado na Frontend Factory.
    """
    spec_id: str
    derived_from_draft_id: str = Field(..., description="ID do DesignSystemDraft (Garante a Rastreabilidade).")
    theme_config: TailwindThemeSpec
    component_registry: List[ComponentRequirement]
    component_alerts: List[ComponentMissingAlert] = Field(default_factory=list, description="Log de degradação de componentes não mapeados.")
    debt_tracking: ScaffoldingResolution
    ready_for_factory: bool = Field(
        default=True, 
        description="Selo final do Álvaro. Se False, o pipeline de CI/CD deve abortar."
    )
