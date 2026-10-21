from src.error_analysis import detect_leakage, find_errors


def test_leakage_detects_normalized_text_across_splits():
    splits = {
        "train": [{"id": "1", "text": "Reset my Password", "label": "account"}],
        "test": [{"id": "2", "text": " reset  MY password ", "label": "account"}],
    }
    findings = detect_leakage(splits)
    assert findings and findings[0]["text"] == "reset my password"


def test_leakage_fixture_fails_then_corrected_split_passes():
    leaky = {
        "train": [{"id": "train-1", "text": "Reset my Password", "label": "account"}],
        "test": [{"id": "test-1", "text": " reset  MY password ", "label": "account"}],
    }
    assert detect_leakage(leaky)
    corrected = {
        "train": leaky["train"],
        "test": [{"id": "test-2", "text": "The export API returns an error", "label": "technical"}],
    }
    assert detect_leakage(corrected) == []


def test_error_analysis_returns_misclassified_rows():
    errors = find_errors([{"id": "x", "text": "refund", "label": "billing"}], ["technical"])
    assert errors[0]["id"] == "x"
