import csv
import re
from pathlib import Path

REQUIRED_COLUMNS = {"id", "text", "label"}
LABELS = {"account", "billing", "technical"}


def validate_rows(rows):
    rows = list(rows)
    if not rows:
        raise ValueError("dataset must not be empty")
    if set(rows[0]) != REQUIRED_COLUMNS:
        raise ValueError(f"columns must be exactly {sorted(REQUIRED_COLUMNS)}")
    seen = set()
    for row in rows:
        if set(row) != REQUIRED_COLUMNS or not all(str(row[k]).strip() for k in REQUIRED_COLUMNS):
            raise ValueError("rows must contain non-empty id, text, and label columns")
        if row["label"] not in LABELS:
            raise ValueError(f"label must be one of {sorted(LABELS)}")
        if row["id"] in seen:
            continue
        seen.add(row["id"])
    return rows


def normalize_text(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def deduplicate_rows(rows):
    result, ids, texts = [], set(), set()
    for row in rows:
        text = normalize_text(row["text"])
        if row["id"] not in ids and text not in texts:
            ids.add(row["id"]); texts.add(text)
            result.append(dict(row))
    return result


def load_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    validate_rows(rows)
    return deduplicate_rows(rows)


def write_csv(path, rows):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted(REQUIRED_COLUMNS))
        writer.writeheader(); writer.writerows(rows)
