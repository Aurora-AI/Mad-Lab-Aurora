import pytest
from bff_agent import generate_types_file, generate_client_component, generate_server_component, load_api_manifest
from bff_contracts import BFFAdapterSpec, PagePropsContract, DataDependency, APIManifestEntry

@pytest.fixture
def sample_spec():
    return BFFAdapterSpec(
        spec_id="BFF-TEST-002",
        props_contract=PagePropsContract(
            page_id="TEST-002",
            dependencies=[
                DataDependency(
                    prop_name="usersList",
                    contract_ref="UserManagement",
                    schema_ref="UserListResponse",
                    adapter_ref="chronos.metrics.dashboard",
                    access_scope="analytics:read",
                    required=True,
                    cache_policy="force-cache",
                    error_strategy="null"
                )
            ]
        )
    )

@pytest.fixture
def mock_manifest():
    return {
        "chronos.metrics.dashboard": APIManifestEntry(
            adapter_ref="chronos.metrics.dashboard",
            method="GET",
            path="/api/chronos/v1/metrics",
            response_schema="DashboardMetricsSchema",
            scope="analytics:read",
            tenant_required=True
        )
    }

def test_generate_types_file_conforms_to_schema(sample_spec):
    types_code = generate_types_file(sample_spec)
    assert "import type { UserListResponse } from '@/schemas';" in types_code
    assert "usersList: UserListResponse;" in types_code
    assert "export interface SynthesizedPageProps" in types_code

def test_generate_client_component_conforms(sample_spec):
    jsx_body = "    <div />"
    imports = {"import { Something } from 'somewhere';"}
    client_code = generate_client_component(sample_spec, jsx_body, imports)
    assert "'use client';" in client_code
    assert "import type { SynthesizedPageProps } from './SynthesizedPage.types';" in client_code
    assert "export default function SynthesizedPageClient" in client_code
    assert "import { Something } from 'somewhere';" in client_code
    assert "<div />" in client_code

def test_generate_server_component_mappings(sample_spec, mock_manifest):
    server_code = generate_server_component(sample_spec, mock_manifest)
    assert "process.env.INTERNAL_API_GATEWAY + '/api/chronos/v1/metrics'" in server_code
    assert "method: 'GET'" in server_code
    assert "cache: 'force-cache'" in server_code
    assert "'X-Aurora-Scope': 'analytics:read'" in server_code
    assert "usersList = null;" in server_code # Da estratégia de erro "null"
    assert "<SynthesizedPageClient usersList={usersList} />" in server_code

def test_generate_server_component_raises_on_missing_adapter(sample_spec):
    empty_manifest = {}
    with pytest.raises(ValueError) as exc:
        generate_server_component(sample_spec, empty_manifest)
    assert "FALHA DE LIGAÇÃO: Adapter 'chronos.metrics.dashboard' não existe" in str(exc.value)

def test_load_manifest_reads_and_validates():
    manifest = load_api_manifest()
    assert "twenty.rest.leads.list" in manifest
    assert manifest["twenty.rest.leads.list"].method == "GET"
    assert manifest["twenty.rest.leads.list"].path == "/api/twenty/leads"
