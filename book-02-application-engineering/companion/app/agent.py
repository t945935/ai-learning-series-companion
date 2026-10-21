from .contracts import Principal
from .retrieval import LocalRetriever
from .storage import KnowledgeStore


class SafetyStop(RuntimeError):
    pass


class Agent:
    def __init__(self, store: KnowledgeStore):
        self.retriever = LocalRetriever(store)

    def answer(self, query: str, principal: Principal, max_steps: int = 3) -> str:
        if max_steps < 1:
            raise SafetyStop("maximum agent steps reached before retrieval")
        hits = self.retriever.search(query, principal)
        if not hits:
            return "I don't have enough information in the local knowledge base to answer that."
        lines = [f"{hit.document.text}\n(source_id: {hit.source_id})" for hit in hits]
        return "\n\n".join(lines)
