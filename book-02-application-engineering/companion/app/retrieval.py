import re
from dataclasses import dataclass

from .contracts import Document, Principal
from .storage import KnowledgeStore


@dataclass(frozen=True)
class SearchHit:
    document: Document
    score: int

    @property
    def source_id(self):
        return self.document.source_id

    @property
    def tenant_id(self):
        return self.document.tenant_id


class LocalRetriever:
    def __init__(self, store: KnowledgeStore):
        self.store = store

    def search(self, query: str, principal: Principal, limit: int = 5) -> list[SearchHit]:
        stopwords = {"a", "an", "and", "are", "is", "the", "to", "what", "when", "where", "how", "on", "of"}
        terms = set(re.findall(r"[\w-]+", query.lower())) - stopwords
        hits = []
        for doc in self.store.documents():
            if doc.tenant_id != principal.tenant_id or principal.role not in doc.roles:
                continue
            score = len(terms & set(re.findall(r"[\w-]+", (doc.title + " " + doc.text).lower())))
            if score:
                hits.append(SearchHit(doc, score))
        if not hits:
            return []
        best_score = max(hit.score for hit in hits)
        best_hits = [hit for hit in hits if hit.score == best_score]
        return sorted(best_hits, key=lambda h: h.source_id)[:limit]
