"""
Rolling Statistics Features Module
Crear features basadas en estadísticas móviles (ventanas deslizantes)

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Callable
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_rolling_features(
    df: pd.DataFrame,
    target_col: str = 'sales',
    group_cols: List[str] = ['id'],
    windows: List[int] = [7, 14, 28, 90],
    functions: List[str] = ['mean', 'std', 'min', 'max'],
    **kwargs
) -> pd.DataFrame:
    """
    Crear rolling statistics features para series temporales.

    Las estadísticas móviles capturan tendencias y variabilidad
    en diferentes horizontes temporales.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos de ventas
    target_col : str
        Nombre de la columna objetivo (default: 'sales')
    group_cols : List[str]
        Columnas para agrupar (default: ['id'])
    windows : List[int]
        Tamaños de ventana en días (default: [7, 14, 28, 90])
    functions : List[str]
        Funciones estadísticas a aplicar (default: ['mean', 'std', 'min', 'max'])

    Returns
    -------
    pd.DataFrame
        DataFrame con rolling features añadidas

    Examples
    --------
    >>> df = create_rolling_features(df, windows=[7, 28])
    >>> # Crea: sales_rolling_mean_7, sales_rolling_std_7, etc.

    Notes
    -----
    - Rolling mean: promedio móvil (captura tendencia)
    - Rolling std: desviación estándar móvil (captura variabilidad)
    - Rolling min/max: rango de valores
    - Window 7: última semana
    - Window 28: último mes
    - Window 90: último trimestre
    """
    logger.info(f"Creating rolling features: windows={windows}, functions={functions}")

    df_result = df.copy()

    # Asegurar que está ordenado por fecha
    if 'date' in df_result.columns:
        df_result = df_result.sort_values(group_cols + ['date'])

    # Crear cada combinación de ventana y función
    for window in windows:
        for func in functions:
            feature_name = f'{target_col}_rolling_{func}_{window}'

            logger.info(f"  Creating {feature_name}")

            # Calcular rolling statistic por grupo
            df_result[feature_name] = (
                df_result.groupby(group_cols)[target_col]
                .transform(lambda x: x.rolling(window=window, min_periods=1).agg(func))
            )

            # Contar NaNs
            nan_count = df_result[feature_name].isna().sum()
            total = len(df_result)

            if nan_count > 0:
                logger.warning(f"    NaNs: {nan_count:,} ({nan_count/total*100:.2f}%)")

    total_features = len(windows) * len(functions)
    logger.info(f"✓ Created {total_features} rolling features")

    return df_result


def create_rolling_features_advanced(
    df: pd.DataFrame,
    target_col: str = 'sales',
    group_cols: List[str] = ['id'],
    windows: List[int] = [7, 28],
    **kwargs
) -> pd.DataFrame:
    """
    Crear rolling features avanzadas (percentiles, coef. variación, etc.).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos
    target_col : str
        Columna objetivo
    group_cols : List[str]
        Columnas de agrupación
    windows : List[int]
        Ventanas a usar

    Returns
    -------
    pd.DataFrame
        DataFrame con features avanzadas
    """
    logger.info("Creating advanced rolling features")

    df_result = df.copy()

    for window in windows:
        logger.info(f"  Window {window} days")

        # Percentiles (25, 50, 75)
        for q in [25, 50, 75]:
            feature_name = f'{target_col}_rolling_q{q}_{window}'
            df_result[feature_name] = (
                df_result.groupby(group_cols)[target_col]
                .transform(lambda x: x.rolling(window=window, min_periods=1).quantile(q/100))
            )
            logger.info(f"    Created {feature_name}")

        # Coeficiente de variación (std/mean)
        mean_col = f'{target_col}_rolling_mean_{window}'
        std_col = f'{target_col}_rolling_std_{window}'

        if mean_col in df_result.columns and std_col in df_result.columns:
            cv_col = f'{target_col}_rolling_cv_{window}'
            df_result[cv_col] = df_result[std_col] / (df_result[mean_col] + 1e-6)
            logger.info(f"    Created {cv_col}")

        # Trend (comparar última ventana vs ventana anterior)
        current_mean = f'{target_col}_rolling_mean_{window}'
        if current_mean in df_result.columns:
            trend_col = f'{target_col}_rolling_trend_{window}'
            df_result[trend_col] = (
                df_result.groupby(group_cols)[current_mean]
                .transform(lambda x: x.diff(window))
            )
            logger.info(f"    Created {trend_col}")

    logger.info("✓ Created advanced rolling features")

    return df_result


def create_expanding_features(
    df: pd.DataFrame,
    target_col: str = 'sales',
    group_cols: List[str] = ['id'],
    functions: List[str] = ['mean', 'std'],
    **kwargs
) -> pd.DataFrame:
    """
    Crear expanding window features (toda la historia hasta el momento).

    A diferencia de rolling (ventana fija), expanding usa toda la
    historia disponible hasta cada punto.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con los datos
    target_col : str
        Columna objetivo
    group_cols : List[str]
        Columnas de agrupación
    functions : List[str]
        Funciones a aplicar

    Returns
    -------
    pd.DataFrame
        DataFrame con expanding features

    Notes
    -----
    - Útil para capturar comportamiento histórico general
    - Mean expanding: promedio de todas las ventas históricas
    - Std expanding: variabilidad histórica total
    """
    logger.info("Creating expanding window features")

    df_result = df.copy()

    for func in functions:
        feature_name = f'{target_col}_expanding_{func}'

        logger.info(f"  Creating {feature_name}")

        df_result[feature_name] = (
            df_result.groupby(group_cols)[target_col]
            .transform(lambda x: x.expanding(min_periods=1).agg(func))
        )

    logger.info(f"✓ Created {len(functions)} expanding features")

    return df_result


def get_rolling_feature_info() -> Dict[str, any]:
    """
    Obtener información sobre rolling features recomendadas.

    Returns
    -------
    Dict
        Información de rolling windows
    """
    return {
        'recommended_windows': [7, 14, 28, 90],
        'window_interpretations': {
            7: 'Last week average/trend',
            14: 'Last 2 weeks (bi-weekly pattern)',
            28: 'Last month (monthly seasonality)',
            90: 'Last quarter (longer-term trend)'
        },
        'recommended_functions': {
            'mean': 'Average sales (trend indicator)',
            'std': 'Volatility/variability',
            'min': 'Minimum sales (demand floor)',
            'max': 'Maximum sales (demand ceiling)',
            'median': 'Robust central tendency'
        },
        'advanced_features': {
            'cv': 'Coefficient of variation (std/mean) - relative volatility',
            'trend': 'Difference between current and previous window',
            'percentiles': 'Q25, Q50, Q75 for distribution shape'
        },
        'importance': {
            'rolling_mean_7': 'HIGH - Weekly average crucial',
            'rolling_mean_28': 'HIGH - Monthly trend',
            'rolling_std_7': 'MEDIUM - Short-term volatility',
            'rolling_max_28': 'MEDIUM - Demand spikes'
        }
    }


if __name__ == "__main__":
    # Test con datos sintéticos
    logger.info("Testing rolling features module")

    # Crear datos de prueba
    np.random.seed(42)
    test_df = pd.DataFrame({
        'id': ['item_1'] * 100,
        'date': pd.date_range('2024-01-01', periods=100),
        'sales': np.random.poisson(10, 100) + np.sin(np.arange(100) * 0.1) * 3
    })

    # Crear rolling features
    result = create_rolling_features(
        test_df,
        windows=[7, 28],
        functions=['mean', 'std']
    )

    logger.info(f"\nOriginal shape: {test_df.shape}")
    logger.info(f"Result shape: {result.shape}")
    logger.info(f"\nNew columns: {[c for c in result.columns if c not in test_df.columns]}")

    # Sample
    sample_cols = ['sales', 'sales_rolling_mean_7', 'sales_rolling_std_7']
    logger.info(f"\nSample:\n{result[sample_cols].head(15)}")

    # Mostrar info
    info = get_rolling_feature_info()
    logger.info(f"\n\nRecommended windows: {info['recommended_windows']}")
