from app.contracts import Principal
from app.storage import KnowledgeStore
from app.tools import ToolRegistry


def test_tenant_isolation_on_ticket_and_audit(tmp_path):
    store = KnowledgeStore(tmp_path / "store.json")
    registry = ToolRegistry(store)
    registry.call("create_ticket", {"title": "A", "description": "B", "approved": True, "idempotency_key": "same"}, Principal("tenant-a", "support"))
    assert store.tickets()[0]["tenant_id"] == "tenant-a"
    assert store.audit_events()[0].tenant_id == "tenant-a"
    assert not [t for t in store.tickets() if t["tenant_id"] == "tenant-b"]


def test_idempotency_key_is_scoped_to_tenant(tmp_path):
    store = KnowledgeStore(tmp_path / "store.json")
    registry = ToolRegistry(store)
    payload = {"title": "A", "description": "B", "approved": True, "idempotency_key": "same"}
    first = registry.call("create_ticket", payload, Principal("tenant-a", "support"))
    second = registry.call("create_ticket", payload, Principal("tenant-b", "support"))
    assert first["tenant_id"] == "tenant-a"
    assert second["tenant_id"] == "tenant-b"
    assert len(store.tickets()) == 2


def test_tool_does_not_execute_without_explicit_approval(tmp_path):
    store = KnowledgeStore(tmp_path / "store.json")
    registry = ToolRegistry(store)
    try:
        registry.call("create_ticket", {"title": "A", "description": "B", "approved": "yes", "idempotency_key": "x"}, Principal("a", "support"))
    except (PermissionError, ValueError):
        pass
    assert store.tickets() == []
