import pytest
from pydantic import ValidationError
from bff_contracts import DataDependency, APIManifestEntry

def test_data_dependency_blocks_free_endpoint():
    with pytest.raises(ValidationError) as exc:
        DataDependency(
            prop_name="leadsData",
            contract_ref="Leads",
            schema_ref="LeadSchema",
            adapter_ref="twenty.rest.leads.list",
            access_scope="crm:read",
            source_endpoint="https://api.banco.com/v1"
        )
    assert "Extra inputs are not permitted" in str(exc.value)

def test_api_manifest_enforces_internal_routing():
    with pytest.raises(ValidationError) as exc:
        APIManifestEntry(
            adapter_ref="malicious.fetch",
            method="GET",
            path="https://hacker.com/payload",
            response_schema="Any",
            scope="none",
            tenant_required=False
        )
    assert "Violação de Segurança" in str(exc.value)

def test_api_manifest_blocks_path_traversal():
    with pytest.raises(ValidationError) as exc:
        APIManifestEntry(
            adapter_ref="traversal.fetch",
            method="GET",
            path="/api/../internal/database/drop",
            response_schema="Any",
            scope="none",
            tenant_required=False
        )
    assert "Path Traversal" in str(exc.value)

def test_valid_data_dependency():
    dep = DataDependency(
        prop_name="dashboardMetrics",
        contract_ref="Analytics",
        schema_ref="MetricsSchema",
        adapter_ref="chronos.metrics.dashboard",
        access_scope="analytics:read"
    )
    assert dep.cache_policy == "no-store"
