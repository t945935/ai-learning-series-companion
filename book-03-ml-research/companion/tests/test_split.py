from src.data_contract import validate_rows
from src.split import split_rows


def rows(n=30):
    return [{"id": str(i), "text": f"message {i}", "label": "a" if i % 2 else "b"} for i in range(n)]


def test_split_is_fixed_and_disjoint():
    first = split_rows(rows(), seed=17)
    second = split_rows(rows(), seed=17)
    assert first == second
    assert set(first) == {"train", "validation", "test"}
    assert not ({r["id"] for r in first["train"]} & {r["id"] for r in first["validation"]})
    assert not ({r["id"] for r in first["train"]} & {r["id"] for r in first["test"]})


def test_split_preserves_labels():
    result = split_rows(rows(60), seed=7)
    for part in result.values():
        assert {r["label"] for r in part} == {"a", "b"}
