import json
from pathlib import Path
from .data_contract import load_csv
from .split import split_rows


def prepare(input_path, output_dir, seed=20261021):
    rows = load_csv(input_path)
    splits = split_rows(rows, seed=seed)
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    for name, part in splits.items():
        (out / f"{name}.json").write_text(json.dumps(part, indent=2), encoding="utf-8")
    return splits


if __name__ == "__main__":
    prepare("data/raw/synthetic-messages.csv", "data/processed")
