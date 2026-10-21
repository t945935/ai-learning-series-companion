import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .contracts import AuditEvent, Document


class KnowledgeStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._documents: dict[str, Document] = {}
        self._tickets: dict[str, dict[str, Any]] = {}
        self._audit: list[AuditEvent] = []

    def import_file(self, path: str | Path) -> Document:
        path = Path(path)
        raw = path.read_text(encoding="utf-8")
        source_id = "sha256:" + hashlib.sha256(raw.encode()).hexdigest()[:16]
        metadata, body = self._parse_frontmatter(raw)
        doc = Document(source_id, metadata.get("title", path.stem), body.strip(), metadata.get("tenant_id", "acme"), tuple(metadata.get("roles", "support").split(",")), str(path))
        self._documents[source_id] = doc
        return doc

    def documents(self) -> list[Document]:
        return list(self._documents.values())

    def add_ticket(self, ticket: dict[str, Any], event: AuditEvent) -> dict[str, Any]:
        key = f"{ticket['tenant_id']}:{ticket['idempotency_key']}"
        if key in self._tickets:
            return self._tickets[key]
        self._tickets[key] = ticket
        self._audit.append(event)
        return ticket

    def tickets(self) -> list[dict[str, Any]]:
        return list(self._tickets.values())

    def audit_events(self) -> list[AuditEvent]:
        return list(self._audit)

    @staticmethod
    def _parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
        if not raw.startswith("---"):
            return {}, raw
        _, header, body = raw.split("---", 2)
        metadata = {}
        for line in header.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
        return metadata, body
