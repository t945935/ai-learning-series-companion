import csv
from pathlib import Path
import pytest
from src.data_contract import REQUIRED_COLUMNS, validate_rows, deduplicate_rows, load_csv


def test_required_columns_and_labels_are_validated():
    rows = [{"id": "1", "text": "help", "label": "billing"}]
    assert validate_rows(rows) == rows
    with pytest.raises(ValueError, match="label"):
        validate_rows([{ "id": "1", "text": "help", "label": "unknown"}])


def test_missing_column_is_rejected():
    with pytest.raises(ValueError, match="columns"):
        validate_rows([{ "id": "1", "label": "billing"}])


def test_duplicate_ids_and_text_are_removed_deterministically():
    rows = [
        {"id": "1", "text": "A", "label": "billing"},
        {"id": "1", "text": "A", "label": "billing"},
        {"id": "2", "text": "a", "label": "billing"},
    ]
    assert len(deduplicate_rows(rows)) == 1


def test_synthetic_csv_has_contract():
    rows = load_csv(Path("data/raw/synthetic-messages.csv"))
    assert set(rows[0]) == REQUIRED_COLUMNS
    assert len(rows) >= 20
