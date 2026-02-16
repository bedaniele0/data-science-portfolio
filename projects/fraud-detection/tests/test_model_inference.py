import pytest
import joblib
import os
import numpy as np
import pandas as pd

MODEL_PATH = "models/improved_recall_threshold_model.pkl"

def test_model_file_exists():
    assert os.path.exists(MODEL_PATH), f"Modelo no encontrado en {MODEL_PATH}"

def test_model_can_predict():
    model = joblib.load(MODEL_PATH)
    n_features = model.n_features_in_
    feature_names = getattr(model, "feature_names_in_", None)
    sample_input = np.random.rand(1, n_features)
    if feature_names is not None:
        sample_input = pd.DataFrame(sample_input, columns=feature_names)
    pred = model.predict(sample_input)
    assert pred.shape == (1,), f"La predicción debe tener una forma de (1,), obtuvo {pred.shape}"
