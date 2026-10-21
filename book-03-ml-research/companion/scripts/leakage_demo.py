#!/usr/bin/env python3
"""Demonstrate leakage detection before and after a split correction."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.error_analysis import detect_leakage


def main():
    leaky = {
        "train": [{"id": "train-1", "text": "Reset my Password", "label": "account"}],
        "test": [{"id": "test-1", "text": " reset  MY password ", "label": "account"}],
    }
    findings_before = detect_leakage(leaky)
    if not findings_before:
        raise SystemExit("expected the intentionally leaky split to fail")

    corrected = {
        "train": leaky["train"],
        "test": [{"id": "test-2", "text": "The export API returns an error", "label": "technical"}],
    }
    findings_after = detect_leakage(corrected)
    if findings_after:
        raise SystemExit("corrected split still contains leakage")

    print(json.dumps({
        "before": {"status": "EXPECTED_FAIL", "findings": findings_before},
        "after": {"status": "PASS", "findings": findings_after},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
