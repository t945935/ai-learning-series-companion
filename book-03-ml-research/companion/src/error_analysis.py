from collections import defaultdict
from .data_contract import normalize_text


def detect_leakage(splits):
    seen = defaultdict(list)
    for split, rows in splits.items():
        for row in rows: seen[normalize_text(row["text"])].append((split, row["id"]))
    return [{"text": text, "occurrences": occurrences} for text, occurrences in seen.items() if len({s for s,_ in occurrences}) > 1]


def find_errors(rows, predictions):
    return [{**row, "prediction": pred} for row, pred in zip(rows, predictions) if row["label"] != pred]
