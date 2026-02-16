#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import time
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, f1_score

# ============================
# CONFIGURACIÓN PRINCIPAL
# ============================
st.set_page_config(page_title="Sistema de Detección de Fraude", layout="wide")
st.title("💳 Sistema de Detección de Fraude")
st.caption("Desarrollado por: Ing. Daniel Varela Perez | 📧 bedaniele0@gmail.com | 📱 +52 55 4189 3428")

DEBUG = False  # ponlo en True si quieres ver mensajes informativos extra

# ============================
# UTILIDADES DE PREPROCESAMIENTO
# ============================

SPANISH_TO_EN = {
    "tiempo": "Time",
    "importe": "Amount",
    "monto": "Amount",
    "clase": "Class",
    "class_real": "Class_Real",
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Estandariza nombres: quita espacios, corrige español→inglés y 'Vxx' mal escritos."""
    cols = []
    for c in df.columns:
        c2 = str(c).strip()
        # "14" -> "V14"
        if c2.isdigit() and 1 <= int(c2) <= 28:
            c2 = f"V{int(c2)}"
        # variantes tipo 'V 10', 'v10 ', etc.
        if c2.upper().startswith("V") and c2[1:].strip().isdigit():
            c2 = f"V{int(c2[1:].strip())}"
        # español → inglés
        key = c2.lower()
        if key in SPANISH_TO_EN:
            c2 = SPANISH_TO_EN[key]
        cols.append(c2)
    df = df.copy()
    df.columns = cols
    return df

def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """Genera variables derivadas que el modelo espera."""
    df = df.copy()
    if "Time" in df.columns:
        df["hour_from_start"] = (df["Time"] // 3600).astype(int)
        df["day_from_start"] = (df["Time"] // 86400).astype(int)
    if "Amount" in df.columns:
        df["amount_log"] = np.log1p(df["Amount"].astype(float))
        df["is_zero_amount"] = (df["Amount"] == 0).astype(int)
        df["is_high_amount"] = (df["Amount"] > 1000).astype(int)
        std_ = df["Amount"].std()
        df["amount_zscore"] = 0.0 if pd.isna(std_) or std_ == 0 else (df["Amount"] - df["Amount"].mean()) / std_

    # Interacciones/aggregates
    if {"V1", "V2"}.issubset(df.columns):
        df["V1_x_V2"] = df["V1"] * df["V2"]
    else:
        df["V1_x_V2"] = 0.0
    if {"V3", "V4"}.issubset(df.columns):
        df["V3_x_V4"] = df["V3"] * df["V4"]
    else:
        df["V3_x_V4"] = 0.0

    v1_5 = [f"V{i}" for i in range(1, 6) if f"V{i}" in df.columns]
    df["V_sum_main"] = df[v1_5].sum(axis=1) if v1_5 else 0.0

    v6_10 = [f"V{i}" for i in range(6, 11) if f"V{i}" in df.columns]
    df["V_mean_main"] = df[v6_10].mean(axis=1) if v6_10 else 0.0
    return df

def get_model_features(model) -> list:
    """Obtiene el set exacto de features que espera el modelo."""
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    # Fallback del proyecto si el modelo no trae feature_names_in_
    return [
        "V1","V2","V3","V4","V5","V6","V7","V8","V9","V10",
        "V11","V12","V13","V14","V15","V16","V17","V18","V19","V20",
        "V21","V22","V23","V24","V25","V26","V27","V28",
        "Time","Amount","hour_from_start","day_from_start",
        "amount_log","is_zero_amount","is_high_amount","amount_zscore",
        "V1_x_V2","V3_x_V4","V_sum_main","V_mean_main"
    ]

def prepare_X_for_model(df: pd.DataFrame, model) -> pd.DataFrame:
    """Normaliza, genera derivadas y ordena columnas exactamente como el modelo las espera."""
    df = normalize_columns(df)

    # Garantizar columnas base
    for i in range(1, 29):
        col = f"V{i}"
        if col not in df.columns:
            df[col] = 0.0
    for base in ["Time", "Amount"]:
        if base not in df.columns:
            df[base] = 0.0

    # Derivar
    df = add_derived_features(df)

    # Orden exacto según el modelo
    model_features = get_model_features(model)
    missing = [c for c in model_features if c not in df.columns]
    extra = [c for c in df.columns if c not in model_features and c not in ["Class","Class_Real","Predicción","Probabilidad","Pred_Label"]]

    if missing:
        st.error(f"❌ Columnas faltantes respecto al modelo: {missing}")
        st.stop()

    if DEBUG and extra:
        st.info(f"ℹ️ Columnas no usadas por el modelo (se ignoran): {extra}")

    X = df[model_features].copy()
    return X

# ============================
# CARGA DEL MODELO (robusta)
# ============================
@st.cache_resource
def load_model():
    candidates = [
        "improved_recall_threshold_model.pkl",
        "./improved_recall_threshold_model.pkl",
        "models/improved_recall_threshold_model.pkl",
        "../models/improved_recall_threshold_model.pkl",
    ]
    for p in candidates:
        if Path(p).exists():
            return joblib.load(p)
    st.error("❌ No se encontró el archivo del modelo 'improved_recall_threshold_model.pkl' en rutas conocidas.")
    st.stop()

model = load_model()
MODEL_FEATURES = get_model_features(model)
st.success("✅ Modelo cargado y listo para predicciones.")

# ============================
# PESTAÑAS
# ============================
tabs = st.tabs([
    "🔍 Predicción individual",
    "📂 Análisis por lote",
    "📈 Métricas en tiempo real",
    "📊 Métricas acumuladas"
])

# ============================
# 1️⃣ PREDICCIÓN INDIVIDUAL
# ============================
with tabs[0]:
    st.header("🔍 Predicción individual")
    st.markdown("Ingresa **Time**, **Amount** y **V1–V28** (puedes dejar valores en 0 si no los conoces).")

    c1, c2 = st.columns(2)
    with c1:
        time_val = st.number_input("Time (segundos)", min_value=0, value=3600, step=60)
    with c2:
        amount_val = st.number_input("Amount ($)", min_value=0.0, value=100.0, step=10.0)

    with st.expander("V1 – V14"):
        cols = st.columns(7)
        v_inputs_1 = {f"V{i}": cols[(i-1) % 7].number_input(f"V{i}", value=0.0, step=0.01, key=f"v{i}_ind") for i in range(1, 15)}

    with st.expander("V15 – V28"):
        cols2 = st.columns(7)
        v_inputs_2 = {f"V{i}": cols2[(i-15) % 7].number_input(f"V{i}", value=0.0, step=0.01, key=f"v{i}_ind") for i in range(15, 29)}

    if st.button("🔎 Analizar Transacción"):
        row = {"Time": time_val, "Amount": amount_val}
        row.update(v_inputs_1)
        row.update(v_inputs_2)
        df_one = pd.DataFrame([row])

        X_one = prepare_X_for_model(df_one, model)
        prob = float(model.predict_proba(X_one)[:, 1][0])
        pred = int(prob > 0.5)

        st.metric("Probabilidad de Fraude", f"{prob*100:.2f}%")
        st.write("**Predicción:**", "⚠️ FRAUDE" if pred == 1 else "✅ NORMAL")
        st.write("**Nivel de riesgo:**", "ALTO" if prob > 0.7 else ("MEDIO" if prob > 0.3 else "BAJO"))

# ==============================
# 2️⃣ 📂 ANÁLISIS POR LOTE
# ==============================
with tabs[1]:
    st.subheader("📂 Análisis de múltiples transacciones")
    uploaded_file = st.file_uploader("Sube un archivo CSV con transacciones", type=["csv"])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df = normalize_columns(df)            # nombra Time/Amount y Vxx correctamente
            X = prepare_X_for_model(df, model)    # genera derivadas y ordena columnas

            # Predicciones
            probs = model.predict_proba(X)[:, 1]
            preds = (probs >= 0.5).astype(int)
            df["Probabilidad"] = probs
            df["Pred"] = preds
            df["Pred_Label"] = np.where(preds == 1, "FRAUDE", "NORMAL")

            st.success("✅ Predicciones completadas con éxito.")
            st.dataframe(df.head())

            # Guardar en sesión para pestaña de métricas acumuladas
            st.session_state["last_batch_df"] = df.copy()

            # 📊 Métricas si existe columna real
            if "Class_Real" in df.columns:
                y_true = df["Class_Real"].astype(int).values
                y_pred = preds
                precision = precision_score(y_true, y_pred, zero_division=0)
                recall = recall_score(y_true, y_pred, zero_division=0)
                f1 = f1_score(y_true, y_pred, zero_division=0)

                st.markdown("### 📈 Métricas del modelo en este lote:")
                c1, c2, c3 = st.columns(3)
                c1.metric("Precisión", f"{precision:.3f}")
                c2.metric("Recall", f"{recall:.3f}")
                c3.metric("F1-Score", f"{f1:.3f}")

            # 💾 Descargar resultados
            st.download_button(
                label="📥 Descargar resultados en CSV",
                data=df.to_csv(index=False).encode("utf-8-sig"),
                file_name="resultados_fraude.csv",
                mime="application/octet-stream"
            )

        except Exception as e:
            st.error(f"❌ Error al procesar el archivo: {e}")

# ============================
# 3️⃣ MÉTRICAS EN TIEMPO REAL
# ============================
with tabs[2]:
    st.header("📈 Métricas en tiempo real")
    st.markdown("Simula flujo con CSV o datos aleatorios (se generan V1–V28 y features derivadas).")

    uploaded_file_rt = st.file_uploader("CSV opcional para streaming", type=["csv"], key="rt")
    if st.button("▶️ Iniciar simulación"):
        if uploaded_file_rt:
            df_rt = pd.read_csv(uploaded_file_rt)
            df_rt = normalize_columns(df_rt)
        else:
            n = 200
            df_rt = pd.DataFrame({
                "Time": np.random.randint(0, 20000, n),
                "Amount": np.random.uniform(1, 5000, n),
                **{f"V{i}": np.random.randn(n) for i in range(1, 29)}
            })

        chart = st.line_chart()
        for i in range(len(df_rt)):
            X_i = prepare_X_for_model(df_rt.iloc[[i]].copy(), model)
            prob_i = float(model.predict_proba(X_i)[:, 1][0])
            chart.add_rows(pd.DataFrame({"Probabilidad": [prob_i]}))
            time.sleep(0.02)

# ============================
# 4️⃣ MÉTRICAS ACUMULADAS
# ============================
with tabs[3]:
    st.header("📊 Métricas acumuladas")
    st.markdown("Requiere haber corrido **Análisis por lote**. Si existe `Class_Real`, se mostrarán métricas acumuladas.")

    if "last_batch_df" not in st.session_state:
        st.warning("⚠️ Aún no hay datos cargados. Sube y analiza un CSV en 'Análisis por lote'.")
    else:
        df_last = st.session_state["last_batch_df"].copy()
        if "Pred" not in df_last.columns:
            st.info("Primero genera predicciones en la pestaña 'Análisis por lote'.")
        elif "Class_Real" not in df_last.columns:
            st.warning("El CSV no contiene `Class_Real`; no se pueden calcular métricas acumuladas.")
        else:
            y_true = df_last["Class_Real"].astype(int).values
            y_pred = df_last["Pred"].astype(int).values

            metrics_df = pd.DataFrame({
                "Transacciones": np.arange(1, len(y_true) + 1),
                "Precisión": [precision_score(y_true[:i], y_pred[:i], zero_division=0) if i > 1 else np.nan for i in range(1, len(y_true)+1)],
                "Recall": [recall_score(y_true[:i], y_pred[:i], zero_division=0) if i > 1 else np.nan for i in range(1, len(y_true)+1)],
                "F1": [f1_score(y_true[:i], y_pred[:i], zero_division=0) if i > 1 else np.nan for i in range(1, len(y_true)+1)],
            })

            fig = px.line(metrics_df, x="Transacciones", y=["Precisión", "Recall", "F1"],
                          title="📈 Evolución de métricas acumuladas")
            st.plotly_chart(fig, use_container_width=True)
