"""
============================================================================
dashboard.py - Dashboard Interactivo Streamlit para Walmart Forecasting
============================================================================
Dashboard de 5 páginas para visualización de forecasts, métricas, y análisis

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Metodología: DVP-PRO
============================================================================
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import warnings

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mlflow
from mlflow.tracking import MlflowClient

# Configurar paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Walmart Demand Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

@st.cache_data(ttl=300)
def load_data(file_path: str) -> pd.DataFrame:
    """Carga datos con cache."""
    if file_path.endswith('.parquet'):
        return pd.read_parquet(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    return pd.DataFrame()


@st.cache_data(ttl=300)
def load_predictions() -> pd.DataFrame:
    """Carga últimas predicciones."""
    pred_dir = PROJECT_ROOT / "data" / "predictions"
    if pred_dir.exists():
        files = sorted(pred_dir.glob("predictions_*.csv"), reverse=True)
        if files:
            return pd.read_csv(files[0])
    return pd.DataFrame()


@st.cache_data(ttl=300)
def load_metrics() -> Dict:
    """Carga métricas del último entrenamiento."""
    import json
    metrics_path = PROJECT_ROOT / "reports" / "metrics" / "training_metrics.json"
    if metrics_path.exists():
        with open(metrics_path, 'r') as f:
            return json.load(f)
    return {}


@st.cache_resource
def get_mlflow_client():
    """Obtiene cliente de MLflow."""
    mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
    mlflow.set_tracking_uri(mlflow_uri)
    return MlflowClient()


def format_number(num: float, decimals: int = 2) -> str:
    """Formatea número con separador de miles."""
    return f"{num:,.{decimals}f}"


def safe_metric(value: float, decimals: int = 2, suffix: str = "") -> str:
    """Formatea métricas, mostrando N/A cuando no hay valor."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return "N/A"
    return f"{format_number(value, decimals)}{suffix}"


def get_run_metric(run, keys: list[str]) -> float:
    """Devuelve la primera métrica disponible en un run."""
    for key in keys:
        if key in run.data.metrics:
            return run.data.metrics.get(key)
    return np.nan


def calculate_forecast_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
    """Calcula métricas de forecasting."""
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    metrics = {
        'MAE': float(mean_absolute_error(y_true, y_pred)),
        'RMSE': float(np.sqrt(mean_squared_error(y_true, y_pred))),
    }

    # For MAPE, consider only non-zero true values for stability
    non_zero_mask = y_true > 0
    if np.any(non_zero_mask):
        metrics['MAPE'] = float(np.mean(np.abs((y_true[non_zero_mask] - y_pred[non_zero_mask]) / y_true[non_zero_mask])) * 100)
    else:
        metrics['MAPE'] = 0.0

    # WMAPE is robust to zeros, but we should handle the case where sum is zero
    sum_abs_true = np.sum(np.abs(y_true))
    if sum_abs_true > 0:
        metrics['WMAPE'] = float(np.sum(np.abs(y_true - y_pred)) / sum_abs_true * 100)
    else:
        metrics['WMAPE'] = 0.0
    
    return metrics


# ============================================================================
# PÁGINA 1: DASHBOARD PRINCIPAL
# ============================================================================

def page_dashboard():
    """Página principal con KPIs y resumen."""

    st.title("📊 Walmart Demand Forecasting Dashboard")
    st.markdown("### Dashboard Principal - Métricas y Visualizaciones")

    # Cargar datos
    metrics = load_metrics()
    predictions_df = load_predictions()

    # Row 1: KPIs principales
    st.markdown("---")
    st.subheader("📈 Métricas del Modelo")

    col1, col2, col3, col4, col5 = st.columns(5)

    if metrics:
        with col1:
            mae = metrics.get('lightgbm', {}).get('mae', 0)
            st.metric("MAE", format_number(mae, 4))

        with col2:
            rmse = metrics.get('lightgbm', {}).get('rmse', 0)
            st.metric("RMSE", format_number(rmse, 4))

        with col3:
            mape = metrics.get('lightgbm', {}).get('mape', 0)
            st.metric("MAPE", f"{format_number(mape, 2)}%")

        with col4:
            wmape = metrics.get('lightgbm', {}).get('wmape', 0)
            st.metric("WMAPE", f"{format_number(wmape, 2)}%")

        with col5:
            accuracy = metrics.get('lightgbm', {}).get('forecast_accuracy', 0)
            st.metric("Forecast Accuracy", f"{format_number(accuracy * 100, 2)}%")

    # Row 2: Predicciones recientes
    st.markdown("---")
    st.subheader("🔮 Predicciones Recientes")

    if not predictions_df.empty:
        col1, col2, col3 = st.columns(3)

        with col1:
            total_pred = predictions_df['prediction'].sum()
            st.metric("Demanda Total Predicha", format_number(total_pred, 0))

        with col2:
            avg_pred = predictions_df['prediction'].mean()
            st.metric("Demanda Promedio", format_number(avg_pred, 2))

        with col3:
            zero_pct = (predictions_df['prediction'] == 0).sum() / len(predictions_df) * 100
            st.metric("% Predicciones en Cero", f"{format_number(zero_pct, 2)}%")

        # Tabla de predicciones
        st.markdown("##### Top 10 Predicciones más Altas")
        top_preds = predictions_df.nlargest(10, 'prediction')[['id', 'item_id', 'store_id', 'prediction']]
        st.dataframe(top_preds, width='stretch')

    else:
        st.info("📭 No hay predicciones disponibles. Ejecuta el pipeline de predicción primero.")

    # Row 3: Distribución de predicciones
    if not predictions_df.empty:
        st.markdown("---")
        st.subheader("📊 Distribución de Predicciones")

        col1, col2 = st.columns(2)

        with col1:
            # Histogram
            fig = px.histogram(
                predictions_df,
                x='prediction',
                nbins=50,
                title="Distribución de Predicciones",
                labels={'prediction': 'Demanda Predicha', 'count': 'Frecuencia'}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, width='stretch')

        with col2:
            # Box plot
            fig = px.box(
                predictions_df,
                y='prediction',
                title="Box Plot de Predicciones",
                labels={'prediction': 'Demanda Predicha'}
            )
            st.plotly_chart(fig, width='stretch')


# ============================================================================
# PÁGINA 2: ANÁLISIS DE FORECASTING
# ============================================================================

def page_forecasting():
    """Página de análisis de forecasting."""

    st.title("🔮 Análisis de Forecasting")
    st.markdown("### Predicciones vs Valores Reales")

    # Cargar datos
    predictions_df = load_predictions()

    # Intentar cargar datos de validación
    valid_path = PROJECT_ROOT / "data" / "processed" / "valid_data.parquet"
    if valid_path.exists():
        valid_df = load_data(str(valid_path))

        # Merge predictions con actuals
        if not predictions_df.empty and 'id' in predictions_df.columns and 'sales' in valid_df.columns:
            merged_df = predictions_df.merge(
                valid_df[['id', 'sales']],
                on='id',
                how='inner'
            )

            if not merged_df.empty:
                # Calcular métricas
                metrics = calculate_forecast_metrics(
                    merged_df['sales'].values,
                    merged_df['prediction'].values
                )

                # Mostrar métricas
                st.markdown("---")
                st.subheader("📊 Métricas de Validación")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("MAE", format_number(metrics['MAE'], 4))
                with col2:
                    st.metric("RMSE", format_number(metrics['RMSE'], 4))
                with col3:
                    st.metric("MAPE", f"{format_number(metrics['MAPE'], 2)}%")
                with col4:
                    st.metric("WMAPE", f"{format_number(metrics['WMAPE'], 2)}%")

                # Scatter plot: Predicted vs Actual
                st.markdown("---")
                st.subheader("📈 Predicciones vs Valores Reales")

                # Tomar muestra si es muy grande
                sample_size = st.slider("Tamaño de muestra", 100, 5000, 1000, 100)
                if len(merged_df) > sample_size:
                    plot_df = merged_df.sample(sample_size)
                else:
                    plot_df = merged_df

                fig = px.scatter(
                    plot_df,
                    x='sales',
                    y='prediction',
                    title=f"Predicciones vs Valores Reales (n={len(plot_df):,})",
                    labels={'sales': 'Ventas Reales', 'prediction': 'Predicciones'},
                    opacity=0.6
                )

                # Línea perfecta
                max_val = max(plot_df['sales'].max(), plot_df['prediction'].max())
                fig.add_trace(
                    go.Scatter(
                        x=[0, max_val],
                        y=[0, max_val],
                        mode='lines',
                        name='Perfect Prediction',
                        line=dict(color='red', dash='dash')
                    )
                )

                st.plotly_chart(fig, width='stretch')

                # Análisis de residuales
                st.markdown("---")
                st.subheader("🔍 Análisis de Residuales")

                residuals = plot_df['sales'] - plot_df['prediction']

                col1, col2 = st.columns(2)

                with col1:
                    # Histogram de residuales
                    fig = px.histogram(
                        x=residuals,
                        nbins=50,
                        title="Distribución de Residuales",
                        labels={'x': 'Residuales', 'count': 'Frecuencia'}
                    )
                    fig.add_vline(x=0, line_dash="dash", line_color="red")
                    st.plotly_chart(fig, width='stretch')

                with col2:
                    # Residuales vs Predicciones
                    fig = px.scatter(
                        x=plot_df['prediction'],
                        y=residuals,
                        title="Residuales vs Predicciones",
                        labels={'x': 'Predicciones', 'y': 'Residuales'},
                        opacity=0.6
                    )
                    fig.add_hline(y=0, line_dash="dash", line_color="red")
                    st.plotly_chart(fig, width='stretch')

            else:
                st.warning("⚠️ No se pudo combinar predicciones con valores reales")
    else:
        st.info("📭 Datos de validación no disponibles")


# ============================================================================
# PÁGINA 3: ANÁLISIS DE PRODUCTOS Y TIENDAS
# ============================================================================

def page_products_stores():
    """Página de análisis por productos y tiendas."""

    st.title("🏬 Análisis por Productos y Tiendas")
    st.markdown("### Desempeño por Segmentos")

    predictions_df = load_predictions()

    if predictions_df.empty:
        st.info("📭 No hay predicciones disponibles")
        return

    # Análisis por Store
    st.markdown("---")
    st.subheader("🏪 Análisis por Tienda")

    if 'store_id' in predictions_df.columns:
        store_agg = (
            predictions_df
            .groupby('store_id')['prediction']
            .agg([
                ('Total_Demand', 'sum'),
                ('Avg_Demand', 'mean'),
                ('N_Items', 'count')
            ])
            .reset_index()
        )

        col1, col2 = st.columns(2)

        with col1:
            # Bar chart de demanda por tienda
            fig = px.bar(
                store_agg,
                x='store_id',
                y='Total_Demand',
                title="Demanda Total por Tienda",
                labels={'Total_Demand': 'Demanda Total', 'store_id': 'Tienda'}
            )
            st.plotly_chart(fig, width='stretch')

        with col2:
            # Bar chart de demanda promedio
            fig = px.bar(
                store_agg,
                x='store_id',
                y='Avg_Demand',
                title="Demanda Promedio por Tienda",
                labels={'Avg_Demand': 'Demanda Promedio', 'store_id': 'Tienda'}
            )
            st.plotly_chart(fig, width='stretch')

        st.dataframe(
            store_agg.style.format({
                'Total_Demand': '{:,.0f}',
                'Avg_Demand': '{:,.2f}',
                'N_Items': '{:,.0f}'
            }),
            width='stretch'
        )

    # Análisis por Item
    st.markdown("---")
    st.subheader("📦 Análisis por Producto")

    if 'item_id' in predictions_df.columns:
        item_agg = (
            predictions_df
            .groupby('item_id')['prediction']
            .agg([
                ('Total_Demand', 'sum'),
                ('Avg_Demand', 'mean'),
                ('N_Stores', 'count')
            ])
            .reset_index()
        )

        item_agg = item_agg.sort_values('Total_Demand', ascending=False)

        col1, col2 = st.columns(2)

        with col1:
            # Top 20 productos
            top_20 = item_agg.head(20)
            fig = px.bar(
                top_20,
                x='item_id',
                y='Total_Demand',
                title="Top 20 Productos por Demanda",
                labels={'Total_Demand': 'Demanda Total', 'item_id': 'Producto'}
            )
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, width='stretch')

        with col2:
            # Bottom 20 productos
            bottom_20 = item_agg.tail(20)
            fig = px.bar(
                bottom_20,
                x='item_id',
                y='Total_Demand',
                title="Bottom 20 Productos por Demanda",
                labels={'Total_Demand': 'Demanda Total', 'item_id': 'Producto'},
                color_discrete_sequence=['red']
            )
            fig.update_xaxes(tickangle=-45)
            st.plotly_chart(fig, width='stretch')

# ============================================================================
# PÁGINA 4: MLFLOW EXPERIMENTS
# ============================================================================

def page_mlflow():
    """Página de experimentos MLflow."""

    st.title("🧪 MLflow Experiments")
    st.markdown("### Tracking de Experimentos y Modelos")

    try:
        client = get_mlflow_client()
        experiment_name = os.getenv("MLFLOW_EXPERIMENT_NAME", "walmart-forecasting")

        # Obtener experimento
        experiment = client.get_experiment_by_name(experiment_name)

        if experiment is None:
            st.warning(f"⚠️ Experimento '{experiment_name}' no encontrado")
            return

        # Obtener runs
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
            max_results=50
        )

        if not runs:
            st.info("📭 No hay runs disponibles")
            return

        # Preparar datos de runs
        runs_data = []
        for run in runs:
            run_data = {
                'Run ID': run.info.run_id[:8],
                'Run Name': run.data.tags.get('mlflow.runName', 'N/A'),
                'Status': run.info.status,
                'Start Time': datetime.fromtimestamp(run.info.start_time / 1000).strftime('%Y-%m-%d %H:%M'),
                'MAE': get_run_metric(run, ['mae', 'valid_mae', 'train_mae']),
                'RMSE': get_run_metric(run, ['rmse', 'valid_rmse', 'train_rmse']),
                'MAPE': get_run_metric(run, ['mape', 'valid_mape', 'train_mape']),
                'WMAPE': get_run_metric(run, ['wmape', 'valid_wmape']),
            }
            runs_data.append(run_data)

        runs_df = pd.DataFrame(runs_data)

        # Mostrar KPIs
        st.markdown("---")
        st.subheader("📊 Estadísticas de Experimentos")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Runs", len(runs))
        with col2:
            successful = len([r for r in runs if r.info.status == 'FINISHED'])
            st.metric("Runs Exitosos", successful)
        with col3:
            mae_series = runs_df['MAE'].dropna()
            best_mae = mae_series.min() if not mae_series.empty else np.nan
            st.metric("Mejor MAE", safe_metric(best_mae, 4))
        with col4:
            wmape_series = runs_df['WMAPE'].dropna()
            best_wmape = wmape_series.min() if not wmape_series.empty else np.nan
            st.metric("Mejor WMAPE", safe_metric(best_wmape, 2, "%"))

        # Tabla de runs
        st.markdown("---")
        st.subheader("📋 Historial de Runs")
        st.dataframe(runs_df, width='stretch')

        # Comparación de métricas
        st.markdown("---")
        st.subheader("📈 Evolución de Métricas")

        # Preparar datos para plot
        runs_df['Run Number'] = range(len(runs_df), 0, -1)

        # Plot de MAE
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=runs_df['Run Number'],
            y=runs_df['MAE'],
            mode='lines+markers',
            name='MAE',
            line=dict(color='blue')
        ))
        fig.update_layout(
            title="Evolución del MAE",
            xaxis_title="Run Number",
            yaxis_title="MAE",
            hovermode='x unified'
        )
        st.plotly_chart(fig, width='stretch')

        # Plot de WMAPE
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=runs_df['Run Number'],
            y=runs_df['WMAPE'],
            mode='lines+markers',
            name='WMAPE',
            line=dict(color='green')
        ))
        fig.update_layout(
            title="Evolución del WMAPE",
            xaxis_title="Run Number",
            yaxis_title="WMAPE (%)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, width='stretch')

    except Exception as e:
        st.error(f"❌ Error conectando con MLflow: {e}")
        st.info("💡 Asegúrate de que MLflow esté configurado correctamente")


# ============================================================================
# PÁGINA 5: CONFIGURACIÓN Y AYUDA
# ============================================================================

def page_settings():
    """Página de configuración y ayuda."""

    st.title("⚙️ Configuración y Ayuda")
    st.markdown("### Configuración del Sistema")

    # Información del proyecto
    st.markdown("---")
    st.subheader("📋 Información del Proyecto")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Proyecto:** Walmart Demand Forecasting
        **Versión:** 1.2.0
        **Autor:** Ing. Daniel Varela Perez
        **Email:** bedaniele0@gmail.com
        **Metodología:** DVP-PRO
        """)

    with col2:
        st.markdown("""
        **Dataset:** M5 Forecasting Competition
        **Horizonte:** 28 días
        **Modelo:** LightGBM
        **Features:** 88 features engineered
        """)

    # Configuración de rutas
    st.markdown("---")
    st.subheader("📁 Rutas del Proyecto")

    paths = {
        "Project Root": str(PROJECT_ROOT),
        "Data Directory": str(PROJECT_ROOT / "data"),
        "Models Directory": str(PROJECT_ROOT / "models"),
        "Reports Directory": str(PROJECT_ROOT / "reports"),
        "MLflow Tracking": os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"),
    }

    for name, path in paths.items():
        st.text(f"{name}: {path}")

    # Variables de entorno
    st.markdown("---")
    st.subheader("🔧 Variables de Entorno")

    env_vars = {
        "MLFLOW_TRACKING_URI": os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"),
        "MLFLOW_EXPERIMENT_NAME": os.getenv("MLFLOW_EXPERIMENT_NAME", "walmart-forecasting"),
        "MODEL_VERSION": os.getenv("MODEL_VERSION", "1.2.0"),
        "FORECAST_HORIZON": os.getenv("FORECAST_HORIZON", "28"),
    }

    env_df = pd.DataFrame(list(env_vars.items()), columns=['Variable', 'Valor'])
    st.dataframe(env_df, width='stretch')

    # Comandos útiles
    st.markdown("---")
    st.subheader("💻 Comandos Útiles")

    st.markdown("""
    ```bash
    # Entrenar modelo
    make train

    # Generar predicciones
    make predict

    # Ejecutar dashboard
    make dashboard

    # Ver experimentos MLflow
    make mlflow-ui

    # Ejecutar tests
    make test

    # Ver todos los comandos
    make help
    ```
    """)

    # Ayuda
    st.markdown("---")
    st.subheader("❓ Ayuda")

    with st.expander("🔮 ¿Cómo generar predicciones?"):
        st.markdown("""
        1. Asegúrate de tener datos procesados en `data/processed/`
        2. Ejecuta: `make predict` o `walmart-predict`
        3. Las predicciones se guardarán en `data/predictions/`
        4. Visualiza resultados en este dashboard
        """)

    with st.expander("📊 ¿Cómo interpretar las métricas?"):
        st.markdown("""
        - **MAE**: Error absoluto medio - menor es mejor
        - **RMSE**: Raíz del error cuadrático medio - penaliza errores grandes
        - **MAPE**: Error porcentual absoluto medio
        - **WMAPE**: MAPE ponderado - más robusto que MAPE
        - **Forecast Accuracy**: 1 - WMAPE/100 - mayor es mejor
        """)

    with st.expander("🧪 ¿Cómo usar MLflow?"):
        st.markdown("""
        1. Iniciar servidor: `make mlflow-ui`
        2. Abrir navegador en: http://localhost:5000
        3. Ver experimentos, métricas, y modelos
        4. Comparar diferentes runs
        5. Cargar modelos para producción
        """)


# ============================================================================
# NAVEGACIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del dashboard."""

    # Sidebar de navegación
    st.sidebar.title("🎯 Navegación")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Selecciona una página:",
        [
            "📊 Dashboard Principal",
            "🔮 Análisis de Forecasting",
            "🏬 Productos y Tiendas",
            "🧪 MLflow Experiments",
            "⚙️ Configuración"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📌 Info del Proyecto")
    st.sidebar.info("""
    **Walmart Demand Forecasting**
    Versión: 1.2.0
    Metodología: DVP-PRO

    Ing. Daniel Varela Perez
    bedaniele0@gmail.com
    """)

    # Renderizar página seleccionada
    if page == "📊 Dashboard Principal":
        page_dashboard()
    elif page == "🔮 Análisis de Forecasting":
        page_forecasting()
    elif page == "🏬 Productos y Tiendas":
        page_products_stores()
    elif page == "🧪 MLflow Experiments":
        page_mlflow()
    elif page == "⚙️ Configuración":
        page_settings()


if __name__ == "__main__":
    main()
