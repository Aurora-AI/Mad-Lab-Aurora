from abc import ABC, abstractmethod
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

class ConflictReport(BaseModel):
    key: str = Field(..., description="Nome do campo ou propriedade em conflito")
    kit_value: Any = Field(..., description="Valor extraído do Asset Kit")
    probe_value: Any = Field(..., description="Valor extraído do Live Probe")
    resolved_value: Any = Field(..., description="Valor resolvido conforme a matriz de pesos")
    resolution_source: Literal["kit", "probe", "manual"] = Field(..., description="Origem da resolução vencedora")
    needs_escalation: bool = Field(default=False, description="Indica se o conflito exige intervenção manual e pausa do pipeline")

class TruthResolutionResult(BaseModel):
    resolved_data: Dict[str, Any] = Field(..., description="Dicionário com os dados finais de design/estilo consolidados")
    conflicts: Dict[str, ConflictReport] = Field(default_factory=dict, description="Todos os conflitos identificados e suas respectivas resoluções")
    has_critical_conflicts: bool = Field(default=False, description="Flag indicando se há algum conflito crítico pendente de escalação")

class TruthResolverPort(ABC):
    @abstractmethod
    def resolve(self, probe_data: Dict[str, Any], asset_kit_data: Dict[str, Any]) -> TruthResolutionResult:
        """
        Consolida os dados do Probe e do Asset Kit com base na política de conflitos:
        - Kit vence para verdade declarada
        - Probe vence para verdade renderizada
        - Outras discrepâncias disparam Manual Escalation
        """
        pass
