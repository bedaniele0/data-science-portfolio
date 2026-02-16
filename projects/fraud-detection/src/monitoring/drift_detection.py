"""
============================================================================
drift_detection.py - Data & Model Drift Detection para Fraud Detection
============================================================================
Sistema de detección de drift usando PSI y KS tests

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Metodología: DVP-PRO
============================================================================
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class FraudDriftDetector:
    """Detector de drift para fraud detection."""

    def __init__(self, threshold_psi: float = 0.2, threshold_ks: float = 0.05):
        """
        Inicializa el detector de drift.

        Args:
            threshold_psi: Threshold para PSI (0.2 es común)
            threshold_ks: Threshold para KS test p-value
        """
        self.threshold_psi = threshold_psi
        self.threshold_ks = threshold_ks

    def calculate_psi(
        self,
        reference: np.ndarray,
        current: np.ndarray,
        bins: int = 10
    ) -> float:
        """
        Calcula Population Stability Index (PSI).

        PSI < 0.1: No drift
        0.1 <= PSI < 0.2: Drift moderado
        PSI >= 0.2: Drift significativo

        Args:
            reference: Datos de referencia (baseline)
            current: Datos actuales
            bins: Número de bins para binning

        Returns:
            PSI score
        """
        # Binning
        breakpoints = np.percentile(reference, np.linspace(0, 100, bins + 1))
        breakpoints[0] = -np.inf
        breakpoints[-1] = np.inf

        # Calcular distribuciones
        ref_counts = np.histogram(reference, bins=breakpoints)[0]
        cur_counts = np.histogram(current, bins=breakpoints)[0]

        # Normalizar
        ref_percents = ref_counts / len(reference)
        cur_percents = cur_counts / len(current)

        # Evitar división por cero
        ref_percents = np.where(ref_percents == 0, 0.0001, ref_percents)
        cur_percents = np.where(cur_percents == 0, 0.0001, cur_percents)

        # Calcular PSI
        psi = np.sum((cur_percents - ref_percents) * np.log(cur_percents / ref_percents))

        return float(psi)

    def calculate_ks_test(
        self,
        reference: np.ndarray,
        current: np.ndarray
    ) -> Tuple[float, float]:
        """
        Calcula Kolmogorov-Smirnov test.

        Args:
            reference: Datos de referencia
            current: Datos actuales

        Returns:
            Tuple de (ks_statistic, p_value)
        """
        ks_stat, p_value = stats.ks_2samp(reference, current)
        return float(ks_stat), float(p_value)

    def detect_feature_drift(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        features: List[str]
    ) -> Dict[str, Dict]:
        """
        Detecta drift en múltiples features.

        Args:
            reference_data: DataFrame de referencia
            current_data: DataFrame actual
            features: Lista de features a monitorear

        Returns:
            Diccionario con métricas de drift por feature
        """
        drift_report = {}

        for feature in features:
            if feature not in reference_data.columns or feature not in current_data.columns:
                logger.warning(f"Feature {feature} not found in data")
                continue

            ref_values = reference_data[feature].dropna().values
            cur_values = current_data[feature].dropna().values

            # Calcular PSI
            psi = self.calculate_psi(ref_values, cur_values)

            # Calcular KS test
            ks_stat, p_value = self.calculate_ks_test(ref_values, cur_values)

            # Determinar si hay drift
            drift_detected = psi > self.threshold_psi or p_value < self.threshold_ks

            drift_report[feature] = {
                'psi': psi,
                'ks_statistic': ks_stat,
                'ks_p_value': p_value,
                'drift_detected': drift_detected,
                'drift_severity': self._classify_drift_severity(psi)
            }

        return drift_report

    def _classify_drift_severity(self, psi: float) -> str:
        """Clasifica la severidad del drift basado en PSI."""
        if psi < 0.1:
            return "none"
        elif psi < 0.2:
            return "moderate"
        else:
            return "significant"

    def detect_target_drift(
        self,
        reference_predictions: np.ndarray,
        current_predictions: np.ndarray
    ) -> Dict:
        """
        Detecta drift en las predicciones (concept drift).

        Args:
            reference_predictions: Probabilidades de referencia
            current_predictions: Probabilidades actuales

        Returns:
            Métricas de drift en predicciones
        """
        # Calcular tasas de fraude
        ref_fraud_rate = (reference_predictions > 0.5).mean()
        cur_fraud_rate = (current_predictions > 0.5).mean()

        # Cambio relativo
        rate_change = abs(cur_fraud_rate - ref_fraud_rate) / ref_fraud_rate if ref_fraud_rate > 0 else 0

        # PSI en las probabilidades
        psi = self.calculate_psi(reference_predictions, current_predictions)

        # Chi-square test
        chi2, p_value = stats.chisquare([cur_fraud_rate, 1-cur_fraud_rate],
                                       [ref_fraud_rate, 1-ref_fraud_rate])

        return {
            'reference_fraud_rate': float(ref_fraud_rate),
            'current_fraud_rate': float(cur_fraud_rate),
            'fraud_rate_change': float(rate_change),
            'psi': float(psi),
            'chi2_statistic': float(chi2),
            'chi2_p_value': float(p_value),
            'drift_detected': psi > self.threshold_psi or rate_change > 0.3
        }

    def generate_drift_summary(self, drift_report: Dict) -> str:
        """
        Genera resumen del reporte de drift.

        Args:
            drift_report: Reporte de drift

        Returns:
            Resumen en texto
        """
        total_features = len(drift_report)
        drift_features = [f for f, metrics in drift_report.items() if metrics['drift_detected']]

        summary = f"Drift Detection Summary:\n"
        summary += f"  Total features monitored: {total_features}\n"
        summary += f"  Features with drift: {len(drift_features)}\n"

        if drift_features:
            summary += f"\n  Critical features:\n"
            for feature in drift_features[:5]:  # Top 5
                psi = drift_report[feature]['psi']
                summary += f"    - {feature}: PSI = {psi:.4f}\n"

        return summary
