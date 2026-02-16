import json
from pathlib import Path


def test_model_artifacts_exist():
    project_root = Path(__file__).resolve().parents[1]
    assert (project_root / "models" / "final_model.joblib").exists()
    assert (project_root / "models" / "final_metrics.json").exists()
    assert (project_root / "models" / "model_metadata.json").exists()


def test_final_metrics_has_required_keys():
    project_root = Path(__file__).resolve().parents[1]
    metrics_path = project_root / "models" / "final_metrics.json"
    with metrics_path.open() as f:
        data = json.load(f)
    key_map = {
        "auc_roc": "auc_roc",
        "ks": "ks_statistic",
        "recall": "recall_class_1",
        "precision": "precision_class_1",
        "brier": "brier_score",
    }
    for logical, actual in key_map.items():
        assert actual in data, f"{logical} missing ({actual})"
