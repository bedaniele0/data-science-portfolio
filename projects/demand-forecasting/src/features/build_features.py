"""
Feature Engineering Pipeline - Main Script
Pipeline completo para generar todas las features

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
Fecha: 4 de Diciembre, 2024
"""

import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import logging
from typing import Dict, List, Optional
import time

# Import feature modules
from .lag_features import create_lag_features
from .rolling_features import create_rolling_features, create_rolling_features_advanced
from .calendar_features import create_calendar_features, create_holiday_features
from .price_features import create_price_features, create_price_category_features
from .event_features import create_event_features, create_snap_features, create_event_snap_interactions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FeatureEngineeringPipeline:
    """
    Pipeline completo de feature engineering para M5 Forecasting.

    Este pipeline orquesta la creación de todas las features necesarias
    para el modelo de forecasting, asegurando que no haya data leakage.

    Examples
    --------
    >>> pipeline = FeatureEngineeringPipeline(config_path='config/config.yaml')
    >>> df_features = pipeline.run(df_sales, df_calendar, df_prices)
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializar pipeline.

        Parameters
        ----------
        config_path : str, optional
            Ruta al archivo de configuración
        """
        self.config = self._load_config(config_path)
        self.feature_catalog = []

        logger.info("Feature Engineering Pipeline initialized")

    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Cargar configuración desde YAML."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            # Configuración por defecto
            return {
                'features': {
                    'lags': [1, 2, 3, 7, 14, 28],
                    'rolling_windows': [7, 14, 28, 90],
                    'rolling_functions': ['mean', 'std', 'min', 'max']
                }
            }

    def run(
        self,
        df_sales: pd.DataFrame,
        df_calendar: Optional[pd.DataFrame] = None,
        df_prices: Optional[pd.DataFrame] = None,
        include_advanced: bool = True
    ) -> pd.DataFrame:
        """
        Ejecutar pipeline completo de feature engineering.

        Parameters
        ----------
        df_sales : pd.DataFrame
            DataFrame de ventas
        df_calendar : pd.DataFrame, optional
            DataFrame de calendario
        df_prices : pd.DataFrame, optional
            DataFrame de precios
        include_advanced : bool
            Si incluir features avanzadas (más lentas)

        Returns
        -------
        pd.DataFrame
            DataFrame con todas las features

        Notes
        -----
        El orden de creación de features es importante para evitar data leakage:
        1. Calendar features (no dependen del futuro)
        2. Price features (basadas en histórico)
        3. Event/SNAP features (del calendario)
        4. Lag features (usan pasado)
        5. Rolling features (ventanas históricas)
        """
        logger.info("="*60)
        logger.info("STARTING FEATURE ENGINEERING PIPELINE")
        logger.info("="*60)

        start_time = time.time()
        df = df_sales.copy()
        initial_shape = df.shape

        logger.info(f"Initial shape: {initial_shape}")
        logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        # =====================================================================
        # STEP 1: CALENDAR FEATURES
        # =====================================================================
        logger.info("\n" + "="*60)
        logger.info("STEP 1: Creating Calendar Features")
        logger.info("="*60)

        step_start = time.time()
        df = create_calendar_features(df, include_cyclical=True)

        if df_calendar is not None:
            df = create_holiday_features(df, calendar_df=df_calendar)

        step_time = time.time() - step_start
        logger.info(f"✓ Calendar features completed in {step_time:.2f}s")
        logger.info(f"  Shape: {df.shape}")

        # =====================================================================
        # STEP 2: PRICE FEATURES
        # =====================================================================
        if df_prices is not None:
            logger.info("\n" + "="*60)
            logger.info("STEP 2: Creating Price Features")
            logger.info("="*60)

            step_start = time.time()

            # Merge prices
            logger.info("  Merging price data")
            if 'wm_yr_wk' in df.columns and 'wm_yr_wk' in df_prices.columns:
                merge_cols = ['store_id', 'item_id', 'wm_yr_wk']
                df = df.merge(df_prices, on=merge_cols, how='left')

            # Create price features
            if 'sell_price' in df.columns:
                df = create_price_features(df)

                if 'cat_id' in df.columns:
                    df = create_price_category_features(df)

            step_time = time.time() - step_start
            logger.info(f"✓ Price features completed in {step_time:.2f}s")
            logger.info(f"  Shape: {df.shape}")

        # =====================================================================
        # STEP 3: EVENT & SNAP FEATURES
        # =====================================================================
        if df_calendar is not None:
            logger.info("\n" + "="*60)
            logger.info("STEP 3: Creating Event & SNAP Features")
            logger.info("="*60)

            step_start = time.time()

            df = create_event_features(df, calendar_df=df_calendar)
            df = create_snap_features(df, calendar_df=df_calendar)
            df = create_event_snap_interactions(df)

            step_time = time.time() - step_start
            logger.info(f"✓ Event/SNAP features completed in {step_time:.2f}s")
            logger.info(f"  Shape: {df.shape}")

        # =====================================================================
        # STEP 4: LAG FEATURES
        # =====================================================================
        logger.info("\n" + "="*60)
        logger.info("STEP 4: Creating Lag Features")
        logger.info("="*60)

        step_start = time.time()

        lag_days = self.config.get('features', {}).get('lags', [1, 7, 28])
        df = create_lag_features(
            df,
            target_col='sales',
            group_cols=['id'],
            lag_days=lag_days
        )

        step_time = time.time() - step_start
        logger.info(f"✓ Lag features completed in {step_time:.2f}s")
        logger.info(f"  Shape: {df.shape}")

        # =====================================================================
        # STEP 5: ROLLING FEATURES
        # =====================================================================
        logger.info("\n" + "="*60)
        logger.info("STEP 5: Creating Rolling Features")
        logger.info("="*60)

        step_start = time.time()

        windows = self.config.get('features', {}).get('rolling_windows', [7, 28])
        functions = self.config.get('features', {}).get('rolling_functions', ['mean', 'std'])

        df = create_rolling_features(
            df,
            target_col='sales',
            group_cols=['id'],
            windows=windows,
            functions=functions
        )

        if include_advanced:
            logger.info("  Creating advanced rolling features")
            df = create_rolling_features_advanced(df, windows=[7, 28])

        step_time = time.time() - step_start
        logger.info(f"✓ Rolling features completed in {step_time:.2f}s")
        logger.info(f"  Shape: {df.shape}")

        # =====================================================================
        # SUMMARY
        # =====================================================================
        total_time = time.time() - start_time

        logger.info("\n" + "="*60)
        logger.info("FEATURE ENGINEERING PIPELINE COMPLETED")
        logger.info("="*60)
        logger.info(f"Initial shape: {initial_shape}")
        logger.info(f"Final shape: {df.shape}")
        logger.info(f"Features created: {df.shape[1] - initial_shape[1]}")
        logger.info(f"Total time: {total_time:.2f}s ({total_time/60:.2f} min)")
        logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

        # Catalog features
        self.feature_catalog = [col for col in df.columns if col not in df_sales.columns]
        logger.info(f"\nFeature catalog size: {len(self.feature_catalog)}")

        return df

    def get_feature_catalog(self) -> List[str]:
        """
        Obtener lista de features creadas.

        Returns
        -------
        List[str]
            Lista de nombres de features
        """
        return self.feature_catalog.copy()

    def get_feature_groups(self) -> Dict[str, List[str]]:
        """
        Agrupar features por tipo.

        Returns
        -------
        Dict
            Diccionario con features agrupadas
        """
        groups = {
            'calendar': [],
            'price': [],
            'event': [],
            'snap': [],
            'lag': [],
            'rolling': [],
            'other': []
        }

        for feat in self.feature_catalog:
            if any(x in feat for x in ['day_', 'month', 'week', 'quarter', 'year', 'weekend']):
                groups['calendar'].append(feat)
            elif 'price' in feat:
                groups['price'].append(feat)
            elif 'event' in feat:
                groups['event'].append(feat)
            elif 'snap' in feat:
                groups['snap'].append(feat)
            elif 'lag' in feat:
                groups['lag'].append(feat)
            elif 'rolling' in feat:
                groups['rolling'].append(feat)
            else:
                groups['other'].append(feat)

        return groups

    def validate_features(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Validar features para detectar problemas.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame con features

        Returns
        -------
        Dict
            Reporte de validación
        """
        logger.info("Validating features...")

        validation_report = {
            'missing_values': {},
            'infinite_values': {},
            'constant_features': [],
            'high_correlation': []
        }

        # Check missing values
        for col in self.feature_catalog:
            if col in df.columns:
                nan_pct = df[col].isna().sum() / len(df) * 100
                if nan_pct > 0:
                    validation_report['missing_values'][col] = f"{nan_pct:.2f}%"

        # Check infinite values
        numeric_cols = df[self.feature_catalog].select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if np.isinf(df[col]).any():
                validation_report['infinite_values'][col] = np.isinf(df[col]).sum()

        # Check constant features
        for col in self.feature_catalog:
            if col in df.columns:
                if df[col].nunique() == 1:
                    validation_report['constant_features'].append(col)

        logger.info("✓ Validation completed")

        return validation_report


def main():
    """Función principal para ejecutar pipeline desde línea de comandos."""
    import argparse

    parser = argparse.ArgumentParser(description='Feature Engineering Pipeline')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--sample', type=int, help='Sample N items for testing')

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = FeatureEngineeringPipeline(config_path=args.config)

    # Load data
    logger.info("Loading data...")
    # TODO: Implement data loading

    logger.info("Pipeline ready to run")


if __name__ == "__main__":
    main()
