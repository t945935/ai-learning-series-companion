import pytest

from app.agent import Agent, SafetyStop
from app.contracts import Principal
from app.storage import KnowledgeStore


def test_agent_answers_from_local_evidence_and_refuses_unknown(tmp_path):
    store = KnowledgeStore(tmp_path / "store.json")
    store.import_file(__import__("pathlib").Path(__file__).parents[2] / "fixtures/documents/support-hours.md")
    agent = Agent(store)
    answer = agent.answer("When is support open?", Principal("acme", "support"))
    assert "support" in answer.lower() and "source_id" in answer
    refusal = agent.answer("What is the weather on Mars?", Principal("acme", "support"))
    assert "don't have enough information" in refusal.lower()


def test_agent_max_steps_is_safe_stop(tmp_path):
    agent = Agent(KnowledgeStore(tmp_path / "store.json"))
    with pytest.raises(SafetyStop):
        agent.answer("anything", Principal("acme", "support"), max_steps=0)
