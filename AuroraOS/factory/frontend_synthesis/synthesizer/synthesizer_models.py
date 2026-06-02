import sys
import os
from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

# Adiciona o diretório de contratos para importação direta da Fonte da Verdade
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../contracts')))
from models import A11yNodeSummary

class SemanticToken(BaseModel):
    name: str = Field(..., description="Nome semântico Aurora (ex: 'color-surface-elevated').")
    value: str = Field(..., description="O valor transmutado (HEX, rem, ms).")
    rationale: str = Field(..., description="Justificação da síntese (ex: 'Mapeado a partir da cor de fundo predominante, ajustado para contraste Quiet Luxury').")

class AntiPlagiarismRule(BaseModel):
    blocked_original_value: str = Field(..., description="O valor exato (cor, fonte ou medida) detetado na concorrência.")
    violation_type: str = Field(..., description="Tipo de risco: 'Identity Theft', 'Exact Copy', etc.")
    aurora_transmutation: str = Field(..., description="O que usaremos em vez disso para manter a matemática, mas mudar a identidade.")

class DesignSystemDraft(BaseModel):
    """
    Contrato de Saída do Synthesizer (OS-002).
    Este é o artefacto que o Álvaro validará antes de enviar para a Frontend Factory.
    """
    synthesis_id: str
    synthesized_at: datetime
    governance_mode: str = Field(default="transmute", description="Modo de governança: 'transmute' ou 'clone'.")
    semantic_tokens: List[SemanticToken]
    typography_scale: Dict[str, str] = Field(..., description="Escala modular limpa mapeada para rem.")
    do_not_copy_rules: List[AntiPlagiarismRule] = Field(..., description="O relatório oficial de auditoria anti-plágio.")
    a11y_tree: List[A11yNodeSummary] = Field(..., description="Árvore de acessibilidade para inferência de componentes.")
    is_safe_for_production: bool = Field(..., description="Flag final que indica se o draft violou alguma regra estrita.")
