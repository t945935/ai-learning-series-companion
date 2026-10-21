from .contracts import AuditEvent, Principal
from .storage import KnowledgeStore


class ToolValidationError(ValueError):
    pass


class ToolRegistry:
    SCHEMAS = {"create_ticket": {"title": str, "description": str, "approved": bool, "idempotency_key": str}}

    def __init__(self, store: KnowledgeStore):
        self.store = store

    def call(self, name: str, payload: dict, principal: Principal):
        if name not in self.SCHEMAS or not isinstance(payload, dict):
            raise ToolValidationError("unknown tool or payload")
        schema = self.SCHEMAS[name]
        if set(payload) != set(schema):
            raise ToolValidationError("payload fields do not match schema")
        if any(type(payload[key]) is not expected for key, expected in schema.items()):
            raise ToolValidationError("payload types do not match schema")
        if not payload["approved"]:
            raise PermissionError("create_ticket requires explicit approval")
        ticket = {"id": f"ticket:{principal.tenant_id}:{payload['idempotency_key']}", "tenant_id": principal.tenant_id, "created_by_role": principal.role, **payload}
        event = AuditEvent("ticket.created", principal.tenant_id, principal.role, ticket["id"], {"idempotency_key": payload["idempotency_key"]})
        return self.store.add_ticket(ticket, event)
