from src.evaluate import classification_metrics


def test_metrics_are_computed_per_class_and_macro_averaged():
    result = classification_metrics(["a", "a", "b", "b"], ["a", "b", "b", "b"], labels=["a", "b"])
    assert result["accuracy"] == 0.75
    assert result["precision"] == (1.0 + 2 / 3) / 2
    assert result["recall"] == (0.5 + 1.0) / 2
    assert result["macro_f1"] == ((2 / 3) + 0.8) / 2


def test_metrics_handle_empty_predictions():
    result = classification_metrics([], [], labels=["a"])
    assert result["accuracy"] == 0.0
