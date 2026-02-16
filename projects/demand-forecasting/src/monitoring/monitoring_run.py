"""
============================================================================
monitoring_run.py - Script Principal de Monitoring
============================================================================
Monitoreo integrado de performance, drift detection y alertas

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Metodología: DVP-PRO
============================================================================
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import warnings

import pandas as pd
import numpy as np
import joblib
import yaml

# Configurar paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.monitoring.drift_detection import DriftDetector, DriftMonitor
from src.monitoring.alerts import get_alert_manager, AlertLevel

warnings.filterwarnings('ignore')


def setup_logging(log_level: str = "INFO") -> None:
    """Configura logging del sistema."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_dir / "monitoring.log")
        ]
    )


logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/alerts_config.yaml") -> Dict[str, Any]:
    """
    Carga configuración de monitoring.

    Args:
        config_path: Path al archivo de configuración

    Returns:
        Diccionario con configuración
    """
    try:
        config_file = PROJECT_ROOT / config_path
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)

        logger.info(f"✅ Configuración cargada desde: {config_path}")
        return config

    except Exception as e:
        logger.warning(f"⚠️ Error cargando config: {e}, usando defaults")
        return {
            'drift_thresholds': {
                'global_drift_score': {'warning': 0.1, 'critical': 0.25}
            },
            'performance_thresholds': {
                'mae': {'warning': 1.0, 'critical': 1.5},
                'wmape': {'warning': 30.0, 'critical': 50.0}
            }
        }


def load_reference_data() -> pd.DataFrame:
    """
    Carga datos de referencia para drift detection.

    Returns:
        DataFrame con datos de referencia
    """
    try:
        # Intentar cargar datos de training
        train_path = PROJECT_ROOT / "data" / "processed" / "train_data.parquet"

        if train_path.exists():
            logger.info(f"📊 Cargando datos de referencia: {train_path}")
            df = pd.read_parquet(train_path)

            # Tomar muestra si es muy grande
            if len(df) > 10000:
                df = df.sample(10000, random_state=42)
                logger.info(f"   Muestra reducida a {len(df):,} registros")

            return df
        else:
            logger.warning("⚠️ Datos de referencia no encontrados")
            return pd.DataFrame()

    except Exception as e:
        logger.error(f"❌ Error cargando datos de referencia: {e}")
        return pd.DataFrame()


def load_current_data() -> pd.DataFrame:
    """
    Carga datos actuales para comparación.

    Returns:
        DataFrame con datos actuales
    """
    try:
        # Intentar cargar últimas predicciones
        pred_dir = PROJECT_ROOT / "data" / "predictions"

        if pred_dir.exists():
            pred_files = sorted(pred_dir.glob("predictions_*.csv"), reverse=True)
            if pred_files:
                logger.info(f"📊 Cargando predicciones recientes: {pred_files[0]}")
                return pd.read_csv(pred_files[0])

        # Alternativamente, usar datos de validación
        valid_path = PROJECT_ROOT / "data" / "processed" / "valid_data.parquet"
        if valid_path.exists():
            logger.info(f"📊 Cargando datos de validación: {valid_path}")
            return pd.read_parquet(valid_path)

        logger.warning("⚠️ No se encontraron datos actuales")
        return pd.DataFrame()

    except Exception as e:
        logger.error(f"❌ Error cargando datos actuales: {e}")
        return pd.DataFrame()


def check_model_performance(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifica performance del modelo contra umbrales.

    Args:
        config: Configuración con umbrales

    Returns:
        Diccionario con resultados de performance check
    """
    try:
        logger.info("📊 Verificando performance del modelo...")

        # Cargar métricas del último entrenamiento
        metrics_path = PROJECT_ROOT / "reports" / "metrics" / "training_metrics.json"

        if not metrics_path.exists():
            logger.warning("⚠️ Métricas de entrenamiento no encontradas")
            return {'status': 'unknown', 'violations': []}

        import json
        with open(metrics_path, 'r') as f:
            metrics_data = json.load(f)

        # Obtener métricas de validación
        valid_metrics = metrics_data.get('valid_metrics', {})

        if not valid_metrics:
            logger.warning("⚠️ Métricas de validación no disponibles")
            return {'status': 'unknown', 'violations': []}

        # Verificar umbrales
        thresholds = config.get('performance_thresholds', {})
        violations = []
        critical_violations = []

        for metric, values in thresholds.items():
            if metric not in valid_metrics:
                continue

            metric_value = valid_metrics[metric]
            warning_threshold = values.get('warning', float('inf'))
            critical_threshold = values.get('critical', float('inf'))

            # Para forecast_accuracy, menor es peor
            if metric == 'forecast_accuracy':
                if metric_value < critical_threshold:
                    critical_violations.append(f"{metric}={metric_value:.4f} < {critical_threshold}")
                elif metric_value < warning_threshold:
                    violations.append(f"{metric}={metric_value:.4f} < {warning_threshold}")
            else:
                # Para otras métricas, mayor es peor
                if metric_value > critical_threshold:
                    critical_violations.append(f"{metric}={metric_value:.4f} > {critical_threshold}")
                elif metric_value > warning_threshold:
                    violations.append(f"{metric}={metric_value:.4f} > {warning_threshold}")

        # Determinar estado
        if critical_violations:
            status = 'critical'
        elif violations:
            status = 'warning'
        else:
            status = 'healthy'

        result = {
            'status': status,
            'violations': violations,
            'critical_violations': critical_violations,
            'metrics': valid_metrics,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        logger.info(f"✅ Performance check: {status}")
        if violations:
            logger.warning(f"   Violaciones: {violations}")
        if critical_violations:
            logger.error(f"   Violaciones críticas: {critical_violations}")

        return result

    except Exception as e:
        logger.error(f"❌ Error verificando performance: {e}")
        return {'status': 'error', 'violations': []}


def run_drift_detection(reference_data: pd.DataFrame,
                       current_data: pd.DataFrame,
                       config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ejecuta detección de drift.

    Args:
        reference_data: Datos de referencia
        current_data: Datos actuales
        config: Configuración

    Returns:
        Resultados de drift detection
    """
    try:
        logger.info("🔍 Ejecutando drift detection...")

        # Obtener features numéricas comunes
        common_features = list(set(reference_data.columns) & set(current_data.columns))
        numeric_features = reference_data[common_features].select_dtypes(include=[np.number]).columns.tolist()

        # Excluir columnas de identificación
        exclude_cols = ['id', 'sales', 'prediction', 'd']
        numeric_features = [f for f in numeric_features if f not in exclude_cols]

        if not numeric_features:
            logger.warning("⚠️ No hay features numéricas comunes para drift detection")
            return {'status': 'no_features'}

        logger.info(f"   Analizando {len(numeric_features)} features")

        # Inicializar detector
        drift_threshold = config.get('drift_thresholds', {}).get('global_drift_score', {}).get('warning', 0.1)

        detector = DriftDetector(
            reference_data=reference_data[numeric_features],
            feature_columns=numeric_features,
            drift_threshold=drift_threshold
        )

        # Detectar drift
        drift_results = detector.detect_drift(current_data[numeric_features])

        # Guardar reporte
        report_dir = PROJECT_ROOT / "reports" / "drift"
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = report_dir / f"drift_report_{timestamp}.json"

        detector.save_drift_report(drift_results, str(report_path))

        logger.info(f"✅ Drift detection completado")
        logger.info(f"   Overall drift score: {drift_results['overall_drift_score']:.4f}")
        logger.info(f"   Features con drift: {len(drift_results['features_with_drift'])}")

        return drift_results

    except Exception as e:
        logger.error(f"❌ Error en drift detection: {e}")
        return {'status': 'error'}


def send_alerts(performance_results: Dict[str, Any],
               drift_results: Dict[str, Any],
               config: Dict[str, Any]) -> None:
    """
    Envía alertas basadas en resultados de monitoring.

    Args:
        performance_results: Resultados de performance check
        drift_results: Resultados de drift detection
        config: Configuración
    """
    try:
        alert_manager = get_alert_manager()

        # Alerta de performance
        if performance_results['status'] in ['warning', 'critical']:
            level = AlertLevel.CRITICAL if performance_results['status'] == 'critical' else AlertLevel.WARNING

            all_violations = performance_results['violations'] + performance_results['critical_violations']

            alert_manager.send_model_performance_alert(
                metrics=performance_results['metrics'],
                threshold_violations=all_violations
            )

        # Alerta de drift
        if drift_results.get('summary', {}).get('has_significant_drift', False):
            drift_threshold_config = config.get('drift_thresholds', {}).get('global_drift_score', {})
            critical_threshold = drift_threshold_config.get('critical', 0.25)

            drift_score = drift_results['overall_drift_score']

            alert_manager.send_drift_alert(
                drift_score=drift_score,
                feature_drifts={
                    feat: metrics['psi_score']
                    for feat, metrics in drift_results.get('feature_drifts', {}).items()
                },
                threshold=drift_threshold_config.get('warning', 0.1)
            )

        logger.info("✅ Alertas enviadas")

    except Exception as e:
        logger.error(f"❌ Error enviando alertas: {e}")


def generate_monitoring_report(performance_results: Dict[str, Any],
                               drift_results: Dict[str, Any],
                               output_path: Optional[str] = None) -> str:
    """
    Genera reporte consolidado de monitoring.

    Args:
        performance_results: Resultados de performance
        drift_results: Resultados de drift
        output_path: Path del reporte

    Returns:
        Path del archivo generado
    """
    try:
        import json

        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'performance': performance_results,
            'drift': {
                'overall_drift_score': drift_results.get('overall_drift_score', 0.0),
                'features_with_drift': len(drift_results.get('features_with_drift', [])),
                'has_significant_drift': drift_results.get('summary', {}).get('has_significant_drift', False)
            },
            'status': 'healthy' if (
                performance_results['status'] == 'healthy' and
                not drift_results.get('summary', {}).get('has_significant_drift', False)
            ) else 'requires_attention'
        }

        # Guardar reporte
        if output_path is None:
            report_dir = PROJECT_ROOT / "reports" / "monitoring"
            report_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = report_dir / f"monitoring_report_{timestamp}.json"

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        logger.info(f"✅ Reporte de monitoring guardado: {output_path}")

        return str(output_path)

    except Exception as e:
        logger.error(f"❌ Error generando reporte: {e}")
        return ""


def main():
    """Pipeline principal de monitoring."""

    # Argumentos
    parser = argparse.ArgumentParser(description="Sistema de monitoring Walmart Forecasting")
    parser.add_argument('--config', type=str, default='config/alerts_config.yaml',
                       help='Path a configuración')
    parser.add_argument('--skip-drift', action='store_true',
                       help='Omitir drift detection')
    parser.add_argument('--skip-alerts', action='store_true',
                       help='Omitir envío de alertas')
    parser.add_argument('--log-level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Nivel de logging')

    args = parser.parse_args()

    # Setup
    setup_logging(args.log_level)
    logger.info("🚀 Iniciando pipeline de monitoring")

    try:
        # 1. Cargar configuración
        config = load_config(args.config)

        # 2. Check de performance del modelo
        performance_results = check_model_performance(config)

        # 3. Drift detection (si no se omite)
        drift_results = {}
        if not args.skip_drift:
            reference_data = load_reference_data()
            current_data = load_current_data()

            if not reference_data.empty and not current_data.empty:
                drift_results = run_drift_detection(reference_data, current_data, config)
            else:
                logger.warning("⚠️ Datos insuficientes para drift detection")
                drift_results = {'status': 'no_data'}

        # 4. Enviar alertas (si no se omite)
        if not args.skip_alerts and drift_results:
            send_alerts(performance_results, drift_results, config)

        # 5. Generar reporte consolidado
        report_path = generate_monitoring_report(performance_results, drift_results)

        # 6. Resumen en consola
        print("\n" + "="*80)
        print("📊 RESUMEN DE MONITORING")
        print("="*80)
        print(f"Performance Status: {performance_results['status'].upper()}")
        if performance_results['violations']:
            print(f"Violaciones: {len(performance_results['violations'])}")
        if drift_results and 'overall_drift_score' in drift_results:
            print(f"Drift Score: {drift_results['overall_drift_score']:.4f}")
            print(f"Features con drift: {len(drift_results.get('features_with_drift', []))}")
        print(f"\nReporte: {report_path}")
        print("="*80 + "\n")

        logger.info("✅ Pipeline de monitoring completado")

    except Exception as e:
        logger.error(f"❌ Error en pipeline de monitoring: {e}")
        raise


if __name__ == "__main__":
    main()
