from pathlib import Path
import sys


def test_python_version():
    assert sys.version_info >= (3, 10), "Python 3.10+ requerido"


def test_required_files_exist():
    project_root = Path(__file__).resolve().parents[1]
    raw_csv = project_root / "data" / "raw" / "default of credit card clients.csv"
    model_file = project_root / "models" / "final_model.joblib"
    assert raw_csv.exists(), f"Dataset no encontrado: {raw_csv}"
    assert model_file.exists(), f"Modelo no encontrado: {model_file}"
