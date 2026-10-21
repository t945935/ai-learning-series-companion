from pathlib import Path

import pytest

from app.contracts import Principal
from app.retrieval import LocalRetriever
from app.storage import KnowledgeStore
from app.tools import ToolRegistry, ToolValidationError


def seed_store(tmp_path):
    store = KnowledgeStore(tmp_path / "store.json")
    store.import_file(Path(__file__).parents[2] / "fixtures/documents/refund-policy-v1.md")
    store.import_file(Path(__file__).parents[2] / "fixtures/documents/refund-policy-v2.md")
    store.import_file(Path(__file__).parents[2] / "fixtures/documents/support-hours.md")
    return store


def test_import_assigns_stable_source_id_and_reimport_is_idempotent(tmp_path):
    store = KnowledgeStore(tmp_path / "store.json")
    path = Path(__file__).parents[2] / "fixtures/documents/refund-policy-v1.md"
    first = store.import_file(path)
    second = store.import_file(path)
    assert first.source_id == second.source_id
    assert len(store.documents()) == 1


def test_local_search_filters_tenant_and_role(tmp_path):
    store = seed_store(tmp_path)
    retriever = LocalRetriever(store)
    result = retriever.search("refund", Principal("acme", "support"))
    assert result and all(item.tenant_id == "acme" for item in result)
    assert not retriever.search("refund", Principal("other", "support"))
    assert not retriever.search("internal", Principal("acme", "support"))


def test_no_data_is_explicit_refusal(tmp_path):
    store = seed_store(tmp_path)
    assert LocalRetriever(store).search("quantum entanglement", Principal("acme", "support")) == []


def test_tool_schema_validation_rejects_bad_payload(tmp_path):
    registry = ToolRegistry(KnowledgeStore(tmp_path / "store.json"))
    with pytest.raises(ToolValidationError):
        registry.call("create_ticket", {"title": "missing description"}, Principal("acme", "support"))


def test_create_ticket_requires_approval_and_is_idempotent(tmp_path):
    store = KnowledgeStore(tmp_path / "store.json")
    registry = ToolRegistry(store)
    principal = Principal("acme", "support")
    payload = {"title": "Refund issue", "description": "Customer needs help", "approved": False, "idempotency_key": "k1"}
    with pytest.raises(PermissionError):
        registry.call("create_ticket", payload, principal)
    payload["approved"] = True
    first = registry.call("create_ticket", payload, principal)
    second = registry.call("create_ticket", payload, principal)
    assert first == second
    assert len(store.tickets()) == 1
    assert [e.event_type for e in store.audit_events()] == ["ticket.created"]


def test_unknown_tool_is_rejected(tmp_path):
    with pytest.raises(ToolValidationError):
        ToolRegistry(KnowledgeStore(tmp_path / "store.json")).call("shell", {}, Principal("acme", "support"))
