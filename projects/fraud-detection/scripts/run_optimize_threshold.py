# scripts/run_optimize_threshold.py

import pandas as pd
import joblib
import os
import json
from sklearn.metrics import classification_report, precision_recall_curve
import matplotlib.pyplot as plt

# === Paths ===
DATA_PATH = "data/processed/validation_clean.parquet"
MODEL_PATH = "models/simple_fraud_model.pkl"
SCALER_PATH = "data/scaler_clean.pkl"
OUTPUT_MODEL_PATH = "models/improved_recall_threshold_model.pkl"
THRESHOLD_CONFIG_PATH = "models/threshold_config.json"

# === 1. Cargar datos ===
def load_data():
    df_list = []
    for file in sorted(os.listdir(DATA_PATH)):
        if file.endswith(".parquet"):
            df = pd.read_parquet(os.path.join(DATA_PATH, file))
            df_list.append(df)
    return pd.concat(df_list)

# === 2. Cargar modelo y scaler ===
def load_model_and_scaler():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

# === 3. Ajustar umbral para mejorar recall ===
def optimize_threshold(model, scaler, df):
    X = df.drop(columns=["Class"])
    y = df["Class"]
    X_scaled = scaler.transform(X)
    
    y_scores = model.predict_proba(X_scaled)[:, 1]
    precisions, recalls, thresholds = precision_recall_curve(y, y_scores)

    best_idx = recalls.argmax()
    best_threshold = thresholds[best_idx]

    print(f"Mejor umbral para recall: {best_threshold:.3f} | Recall: {recalls[best_idx]:.3f}")
    
    y_pred = (y_scores >= best_threshold).astype(int)
    report = classification_report(y, y_pred, output_dict=True)
    
    return best_threshold, report, y_scores, y

# === 4. Guardar nuevo modelo y umbral ===
def save_outputs(threshold, report):
    joblib.dump(threshold, OUTPUT_MODEL_PATH)
    with open(THRESHOLD_CONFIG_PATH, "w") as f:
        json.dump({"threshold": float(threshold)}, f, indent=4)
    print(f"Modelo guardado en: {OUTPUT_MODEL_PATH}")
    print(f"Umbral guardado en: {THRESHOLD_CONFIG_PATH}")
    
    # Guardar clasificación
    with open("reports/ml_reports/threshold_report.json", "w") as f:
        json.dump(report, f, indent=4)

# === 5. Visualización (opcional)
def plot_precision_recall(y_true, y_scores):
    precisions, recalls, _ = precision_recall_curve(y_true, y_scores)
    plt.plot(recalls, precisions)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Curva Precision-Recall")
    plt.grid(True)
    plt.savefig("reports/figures/ml_reports/precision_recall_curve.png")
    print("Gráfico guardado en reports/figures/ml_reports/")

# === 6. Main ===
def main():
    df = load_data()
    model, scaler = load_model_and_scaler()
    threshold, report, y_scores, y_true = optimize_threshold(model, scaler, df)
    save_outputs(threshold, report)
    plot_precision_recall(y_true, y_scores)

if __name__ == "__main__":
    main()
