import re
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Literal

class DataDependency(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prop_name: str = Field(..., description="Nome da prop que será injetada no SynthesizedPage.client.tsx")
    contract_ref: str = Field(..., description="Referência lógica de domínio (ex: 'LeadManagement')")
    schema_ref: str = Field(..., description="Nome do Pydantic/Zod schema para validação de borda")
    adapter_ref: str = Field(..., description="Chave exata de mapeamento no api_manifest.json")
    access_scope: str = Field(..., description="Escopo de autorização OAuth/JWT necessário")
    required: bool = Field(default=True)
    cache_policy: Literal["no-store", "force-cache", "revalidate"] = Field(default="no-store")
    error_strategy: Literal["boundary", "null", "fallback"] = Field(default="boundary")

class APIManifestEntry(BaseModel):
    adapter_ref: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    path: str = Field(..., description="Caminho interno governado.")
    response_schema: str
    scope: str
    tenant_required: bool

    @field_validator('path')
    @classmethod
    def require_internal_routing(cls, v: str) -> str:
        if not re.match(r'^\/api\/', v):
            raise ValueError(f"Violação de Segurança: O path '{v}' não é uma rota interna controlada (/api/).")
        if ".." in v or "%2e" in v.lower():
            raise ValueError(f"Violação de Segurança (Path Traversal): Tentativa de escape de diretório detectada em '{v}'.")
        return v

class PagePropsContract(BaseModel):
    page_id: str
    dependencies: List[DataDependency]

class BFFAdapterSpec(BaseModel):
    spec_id: str
    target_runtime: Literal["nextjs_app_router_rsc"] = "nextjs_app_router_rsc"
    props_contract: PagePropsContract
