from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Principal:
    tenant_id: str
    role: str


@dataclass(frozen=True)
class Document:
    source_id: str
    title: str
    text: str
    tenant_id: str
    roles: tuple[str, ...]
    path: str


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    tenant_id: str
    actor_role: str
    target_id: str
    details: dict[str, Any]
