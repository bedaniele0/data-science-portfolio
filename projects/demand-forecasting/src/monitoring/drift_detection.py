"""
============================================================================
drift_detection.py - Detección de Data Drift
============================================================================
Sistema de detección de drift en features y distribuciones para forecasting

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Metodología: DVP-PRO
============================================================================
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from pathlib import Path
import warnings

import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import jensenshannon
import json

warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)


class DriftDetector:
    """
    Detector de data drift para modelos de forecasting.

    Implementa múltiples métodos de detección:
    - Kolmogorov-Smirnov test
    - Population Stability Index (PSI)
    - Jensen-Shannon divergence
    - Statistical tests (mean, std, quantiles)
    """

    def __init__(self,
                 reference_data: pd.DataFrame,
                 feature_columns: Optional[List[str]] = None,
                 drift_threshold: float = 0.1):
        """
        Inicializa el detector de drift.

        Args:
            reference_data: Datos de referencia (train/baseline)
            feature_columns: Columnas de features a monitorear
            drift_threshold: Umbral de drift (PSI)
        """
        self.reference_data = reference_data
        self.feature_columns = feature_columns or list(reference_data.columns)
        self.drift_threshold = drift_threshold

        # Calcular estadísticas de referencia
        self.reference_stats = self._calculate_statistics(reference_data)

        logger.info(f"✅ DriftDetector inicializado con {len(self.feature_columns)} features")

    def _calculate_statistics(self, df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """
        Calcula estadísticas de referencia.

        Args:
            df: DataFrame con features

        Returns:
            Diccionario con estadísticas por feature
        """
        stats_dict = {}

        for col in self.feature_columns:
            if col not in df.columns:
                continue

            data = df[col].dropna()

            if len(data) == 0:
                continue

            stats_dict[col] = {
                'mean': float(data.mean()),
                'std': float(data.std()),
                'min': float(data.min()),
                'max': float(data.max()),
                'median': float(data.median()),
                'q25': float(data.quantile(0.25)),
                'q75': float(data.quantile(0.75)),
                'q95': float(data.quantile(0.95)),
            }

        return stats_dict

    def detect_drift(self, current_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Detecta drift entre datos de referencia y actuales.

        Args:
            current_data: Datos actuales para comparar

        Returns:
            Diccionario con resultados de drift
        """
        logger.info(f"🔍 Detectando drift en {len(current_data)} registros...")

        drift_results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'n_features': len(self.feature_columns),
            'n_samples_reference': len(self.reference_data),
            'n_samples_current': len(current_data),
            'feature_drifts': {},
            'overall_drift_score': 0.0,
            'features_with_drift': [],
            'summary': {}
        }

        feature_drift_scores = []

        # Analizar cada feature
        for feature in self.feature_columns:
            if feature not in current_data.columns:
                logger.warning(f"⚠️ Feature {feature} no encontrada en datos actuales")
                continue

            # Calcular drift para la feature
            feature_drift = self._calculate_feature_drift(
                feature,
                self.reference_data[feature].dropna(),
                current_data[feature].dropna()
            )

            drift_results['feature_drifts'][feature] = feature_drift
            feature_drift_scores.append(feature_drift['psi_score'])

            # Verificar si hay drift
            if feature_drift['has_drift']:
                drift_results['features_with_drift'].append(feature)

        # Calcular score global de drift
        if feature_drift_scores:
            drift_results['overall_drift_score'] = float(np.mean(feature_drift_scores))

        # Summary
        drift_results['summary'] = {
            'total_features_analyzed': len(drift_results['feature_drifts']),
            'features_with_drift': len(drift_results['features_with_drift']),
            'drift_percentage': len(drift_results['features_with_drift']) / len(drift_results['feature_drifts']) * 100 if drift_results['feature_drifts'] else 0,
            'has_significant_drift': drift_results['overall_drift_score'] > self.drift_threshold,
            'max_drift_score': max(feature_drift_scores) if feature_drift_scores else 0.0,
            'min_drift_score': min(feature_drift_scores) if feature_drift_scores else 0.0,
        }

        logger.info(f"✅ Drift detection completado")
        logger.info(f"   Overall drift score: {drift_results['overall_drift_score']:.4f}")
        logger.info(f"   Features con drift: {len(drift_results['features_with_drift'])} / {len(drift_results['feature_drifts'])}")

        return drift_results

    def _calculate_feature_drift(self,
                                  feature_name: str,
                                  reference: pd.Series,
                                  current: pd.Series) -> Dict[str, Any]:
        """
        Calcula drift para una feature específica.

        Args:
            feature_name: Nombre de la feature
            reference: Serie de datos de referencia
            current: Serie de datos actuales

        Returns:
            Diccionario con métricas de drift
        """
        drift_metrics = {
            'feature': feature_name,
            'psi_score': 0.0,
            'ks_statistic': 0.0,
            'ks_pvalue': 1.0,
            'js_divergence': 0.0,
            'mean_shift': 0.0,
            'std_shift': 0.0,
            'has_drift': False,
            'drift_type': None
        }

        try:
            # 1. Population Stability Index (PSI)
            psi_score = self._calculate_psi(reference, current)
            drift_metrics['psi_score'] = float(psi_score)

            # 2. Kolmogorov-Smirnov test
            ks_stat, ks_pval = stats.ks_2samp(reference, current)
            drift_metrics['ks_statistic'] = float(ks_stat)
            drift_metrics['ks_pvalue'] = float(ks_pval)

            # 3. Jensen-Shannon divergence
            js_div = self._calculate_js_divergence(reference, current)
            drift_metrics['js_divergence'] = float(js_div)

            # 4. Cambios en estadísticas
            mean_shift = abs(current.mean() - reference.mean()) / (reference.std() + 1e-10)
            std_shift = abs(current.std() - reference.std()) / (reference.std() + 1e-10)

            drift_metrics['mean_shift'] = float(mean_shift)
            drift_metrics['std_shift'] = float(std_shift)

            # Determinar si hay drift
            drift_metrics['has_drift'] = (
                psi_score > self.drift_threshold or
                ks_pval < 0.05 or
                js_div > self.drift_threshold
            )

            # Clasificar tipo de drift
            if drift_metrics['has_drift']:
                if mean_shift > 1.0:
                    drift_metrics['drift_type'] = 'mean_shift'
                elif std_shift > 0.5:
                    drift_metrics['drift_type'] = 'variance_change'
                elif psi_score > self.drift_threshold * 2:
                    drift_metrics['drift_type'] = 'distribution_change'
                else:
                    drift_metrics['drift_type'] = 'moderate_drift'

        except Exception as e:
            logger.warning(f"⚠️ Error calculando drift para {feature_name}: {e}")

        return drift_metrics

    def _calculate_psi(self, reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
        """
        Calcula Population Stability Index (PSI).

        Args:
            reference: Serie de referencia
            current: Serie actual
            bins: Número de bins para histograma

        Returns:
            PSI score
        """
        try:
            # Crear bins basados en datos de referencia
            _, bin_edges = np.histogram(reference, bins=bins)

            # Calcular distribuciones
            ref_hist, _ = np.histogram(reference, bins=bin_edges)
            curr_hist, _ = np.histogram(current, bins=bin_edges)

            # Normalizar
            ref_dist = ref_hist / (len(reference) + 1e-10)
            curr_dist = curr_hist / (len(current) + 1e-10)

            # Evitar divisiones por cero
            ref_dist = np.where(ref_dist == 0, 0.0001, ref_dist)
            curr_dist = np.where(curr_dist == 0, 0.0001, curr_dist)

            # Calcular PSI
            psi = np.sum((curr_dist - ref_dist) * np.log(curr_dist / ref_dist))

            return float(psi)

        except Exception as e:
            logger.warning(f"⚠️ Error calculando PSI: {e}")
            return 0.0

    def _calculate_js_divergence(self, reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
        """
        Calcula Jensen-Shannon divergence.

        Args:
            reference: Serie de referencia
            current: Serie actual
            bins: Número de bins

        Returns:
            JS divergence
        """
        try:
            # Crear bins
            _, bin_edges = np.histogram(
                np.concatenate([reference, current]),
                bins=bins
            )

            # Calcular distribuciones
            ref_hist, _ = np.histogram(reference, bins=bin_edges)
            curr_hist, _ = np.histogram(current, bins=bin_edges)

            # Normalizar
            ref_dist = ref_hist / (ref_hist.sum() + 1e-10)
            curr_dist = curr_hist / (curr_hist.sum() + 1e-10)

            # Calcular JS divergence
            js_div = jensenshannon(ref_dist, curr_dist)

            return float(js_div)

        except Exception as e:
            logger.warning(f"⚠️ Error calculando JS divergence: {e}")
            return 0.0

    def get_top_drifted_features(self, n: int = 10) -> List[Tuple[str, float]]:
        """
        Obtiene las top N features con más drift.

        Args:
            n: Número de features a retornar

        Returns:
            Lista de tuplas (feature, drift_score)
        """
        # Requiere haber ejecutado detect_drift primero
        if not hasattr(self, 'last_drift_results'):
            logger.warning("⚠️ Ejecuta detect_drift() primero")
            return []

        feature_scores = [
            (feat, metrics['psi_score'])
            for feat, metrics in self.last_drift_results['feature_drifts'].items()
        ]

        return sorted(feature_scores, key=lambda x: x[1], reverse=True)[:n]

    def save_drift_report(self, drift_results: Dict[str, Any], output_path: str) -> None:
        """
        Guarda reporte de drift en archivo JSON.

        Args:
            drift_results: Resultados de detect_drift()
            output_path: Path del archivo de salida
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(drift_results, f, indent=2)

            logger.info(f"✅ Reporte de drift guardado: {output_path}")

        except Exception as e:
            logger.error(f"❌ Error guardando reporte: {e}")


class DriftMonitor:
    """
    Monitor de drift que almacena historial y permite tracking temporal.
    """

    def __init__(self, drift_detector: DriftDetector, history_path: Optional[str] = None):
        """
        Inicializa monitor de drift.

        Args:
            drift_detector: Instancia de DriftDetector
            history_path: Path para almacenar historial
        """
        self.detector = drift_detector
        self.history_path = history_path or "reports/drift/drift_history.json"
        self.history = self._load_history()

    def _load_history(self) -> List[Dict[str, Any]]:
        """Carga historial de drift."""
        history_file = Path(self.history_path)
        if history_file.exists():
            with open(history_file, 'r') as f:
                return json.load(f)
        return []

    def _save_history(self) -> None:
        """Guarda historial de drift."""
        history_file = Path(self.history_path)
        history_file.parent.mkdir(parents=True, exist_ok=True)

        with open(history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def monitor(self, current_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Monitorea drift y actualiza historial.

        Args:
            current_data: Datos actuales

        Returns:
            Resultados de drift
        """
        # Detectar drift
        drift_results = self.detector.detect_drift(current_data)

        # Agregar a historial
        self.history.append({
            'timestamp': drift_results['timestamp'],
            'overall_drift_score': drift_results['overall_drift_score'],
            'features_with_drift': len(drift_results['features_with_drift']),
            'has_significant_drift': drift_results['summary']['has_significant_drift']
        })

        # Guardar historial
        self._save_history()

        # Guardar reporte completo
        report_path = Path("reports/drift") / f"drift_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.detector.save_drift_report(drift_results, str(report_path))

        return drift_results

    def get_drift_trend(self, last_n: int = 10) -> pd.DataFrame:
        """
        Obtiene tendencia de drift en últimos N checkpoints.

        Args:
            last_n: Número de checkpoints a analizar

        Returns:
            DataFrame con tendencia
        """
        recent_history = self.history[-last_n:] if len(self.history) > last_n else self.history

        if not recent_history:
            return pd.DataFrame()

        df = pd.DataFrame(recent_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        return df


if __name__ == "__main__":
    # Demo
    logging.basicConfig(level=logging.INFO)

    # Simular datos
    np.random.seed(42)
    n_samples = 1000

    # Datos de referencia
    ref_data = pd.DataFrame({
        'feature_1': np.random.normal(10, 2, n_samples),
        'feature_2': np.random.exponential(5, n_samples),
        'feature_3': np.random.uniform(0, 100, n_samples),
    })

    # Datos actuales con drift
    curr_data = pd.DataFrame({
        'feature_1': np.random.normal(12, 2.5, n_samples),  # Mean shift
        'feature_2': np.random.exponential(5, n_samples),  # Sin drift
        'feature_3': np.random.uniform(0, 150, n_samples),  # Variance shift
    })

    # Detectar drift
    detector = DriftDetector(ref_data, drift_threshold=0.1)
    results = detector.detect_drift(curr_data)

    print("\n" + "="*80)
    print("RESULTADOS DE DRIFT DETECTION")
    print("="*80)
    print(f"Overall drift score: {results['overall_drift_score']:.4f}")
    print(f"Features con drift: {len(results['features_with_drift'])}")
    print(f"Features: {results['features_with_drift']}")
    print("="*80 + "\n")
