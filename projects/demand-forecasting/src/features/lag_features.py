"""
Lag Features Module
Crear features basadas en valores históricos (lags)

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_lag_features(
    df: pd.DataFrame,
    target_col: str = 'sales',
    group_cols: List[str] = ['id'],
    lag_days: List[int] = [1, 2, 3, 7, 14, 28],
    **kwargs
) -> pd.DataFrame:
    """
    Crear lag features para series temporales.

    Los lags permiten al modelo capturar dependencias temporales
    y patrones de autocorrelación en las ventas.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos de ventas
    target_col : str
        Nombre de la columna objetivo (default: 'sales')
    group_cols : List[str]
        Columnas para agrupar (default: ['id'])
    lag_days : List[int]
        Días de lag a crear (default: [1, 2, 3, 7, 14, 28])

    Returns
    -------
    pd.DataFrame
        DataFrame con lag features añadidas

    Examples
    --------
    >>> df = create_lag_features(df, lag_days=[1, 7, 28])
    >>> # Crea: sales_lag_1, sales_lag_7, sales_lag_28

    Notes
    -----
    - Los lags crean NaN para los primeros días (no tienen historia)
    - Lag 1: venta del día anterior
    - Lag 7: venta de hace una semana (captura seasonality semanal)
    - Lag 28: venta de hace 4 semanas (captura seasonality mensual)
    """
    logger.info(f"Creating lag features: {lag_days}")

    df_result = df.copy()

    # Crear cada lag feature
    for lag in lag_days:
        feature_name = f'{target_col}_lag_{lag}'

        logger.info(f"  Creating {feature_name}")

        # Calcular lag por grupo (cada serie temporal)
        df_result[feature_name] = df_result.groupby(group_cols)[target_col].shift(lag)

        # Contar NaNs generados
        nan_count = df_result[feature_name].isna().sum()
        total = len(df_result)
        logger.info(f"    NaNs: {nan_count:,} ({nan_count/total*100:.2f}%)")

    logger.info(f"✓ Created {len(lag_days)} lag features")

    return df_result


def create_lag_features_multi_target(
    df: pd.DataFrame,
    target_cols: List[str],
    group_cols: List[str] = ['id'],
    lag_days: List[int] = [1, 7, 28],
    **kwargs
) -> pd.DataFrame:
    """
    Crear lag features para múltiples variables objetivo.

    Útil cuando se quieren lags de ventas y precios simultáneamente.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos
    target_cols : List[str]
        Lista de columnas objetivo
    group_cols : List[str]
        Columnas para agrupar
    lag_days : List[int]
        Días de lag a crear

    Returns
    -------
    pd.DataFrame
        DataFrame con lag features de todas las variables
    """
    logger.info(f"Creating lag features for {len(target_cols)} targets")

    df_result = df.copy()

    for target_col in target_cols:
        logger.info(f"Processing target: {target_col}")
        df_result = create_lag_features(
            df_result,
            target_col=target_col,
            group_cols=group_cols,
            lag_days=lag_days
        )

    logger.info(f"✓ Created lag features for all targets")

    return df_result


def get_lag_feature_info() -> Dict[str, any]:
    """
    Obtener información sobre las lag features recomendadas.

    Returns
    -------
    Dict
        Diccionario con información de lags recomendados
    """
    return {
        'recommended_lags': [1, 2, 3, 7, 14, 28],
        'lag_interpretations': {
            1: 'Yesterday sales (short-term trend)',
            2: 'Day before yesterday',
            3: '3 days ago',
            7: 'Same day last week (weekly seasonality)',
            14: '2 weeks ago (bi-weekly pattern)',
            28: '4 weeks ago (monthly seasonality)'
        },
        'data_loss': {
            'lag_1': '0.05%',  # 1 día de ~1900
            'lag_7': '0.37%',  # 7 días
            'lag_28': '1.46%'  # 28 días
        },
        'importance': {
            'lag_7': 'HIGH - Weekly seasonality is strong',
            'lag_28': 'HIGH - Monthly patterns',
            'lag_1': 'MEDIUM - Short-term trend',
            'lag_2_3': 'LOW - Redundant with lag_1'
        }
    }


if __name__ == "__main__":
    # Test con datos sintéticos
    logger.info("Testing lag features module")

    # Crear datos de prueba
    np.random.seed(42)
    test_df = pd.DataFrame({
        'id': ['item_1'] * 100 + ['item_2'] * 100,
        'date': pd.date_range('2024-01-01', periods=100).tolist() * 2,
        'sales': np.random.poisson(5, 200)
    })

    # Crear lag features
    result = create_lag_features(test_df, lag_days=[1, 7, 14])

    logger.info(f"\nOriginal shape: {test_df.shape}")
    logger.info(f"Result shape: {result.shape}")
    logger.info(f"\nNew columns: {[c for c in result.columns if c not in test_df.columns]}")
    logger.info(f"\nSample:\n{result[['id', 'sales', 'sales_lag_1', 'sales_lag_7']].head(10)}")

    # Mostrar info de lags
    info = get_lag_feature_info()
    logger.info(f"\n\nRecommended lags: {info['recommended_lags']}")
    logger.info("\nInterpretations:")
    for lag, interp in info['lag_interpretations'].items():
        logger.info(f"  Lag {lag}: {interp}")
