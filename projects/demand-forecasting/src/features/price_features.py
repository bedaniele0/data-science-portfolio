"""
Price Features Module
Crear features basadas en precios y cambios de precio

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


def create_price_features(
    df: pd.DataFrame,
    price_col: str = 'sell_price',
    group_cols: List[str] = ['store_id', 'item_id'],
    **kwargs
) -> pd.DataFrame:
    """
    Crear features basadas en precios.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con precios
    price_col : str
        Columna de precio
    group_cols : List[str]
        Columnas de agrupación

    Returns
    -------
    pd.DataFrame
        DataFrame con price features

    Features Creadas
    ----------------
    - price_change_pct: Cambio porcentual vs periodo anterior
    - price_momentum: Tendencia de precio (últimas 4 semanas)
    - days_since_price_change: Días desde último cambio de precio
    - price_is_discount: Si el precio actual es menor al promedio
    - price_volatility: Volatilidad del precio
    """
    logger.info("Creating price features")

    df_result = df.copy()

    # 1. Cambio porcentual de precio
    logger.info("  Creating price_change_pct")
    df_result = df_result.sort_values(group_cols + ['wm_yr_wk'] if 'wm_yr_wk' in df_result.columns else group_cols)

    df_result['price_lag_1'] = df_result.groupby(group_cols)[price_col].shift(1)
    df_result['price_change_pct'] = (
        (df_result[price_col] - df_result['price_lag_1']) / (df_result['price_lag_1'] + 1e-6) * 100
    )

    # 2. Price momentum (tendencia últimas 4 semanas)
    logger.info("  Creating price_momentum")
    df_result['price_lag_4'] = df_result.groupby(group_cols)[price_col].shift(4)
    df_result['price_momentum'] = (
        (df_result[price_col] - df_result['price_lag_4']) / (df_result['price_lag_4'] + 1e-6) * 100
    )

    # 3. Rolling statistics de precio
    logger.info("  Creating price rolling statistics")
    for window in [4, 8, 12]:  # 4, 8, 12 semanas
        df_result[f'price_rolling_mean_{window}'] = (
            df_result.groupby(group_cols)[price_col]
            .transform(lambda x: x.rolling(window=window, min_periods=1).mean())
        )

        df_result[f'price_rolling_std_{window}'] = (
            df_result.groupby(group_cols)[price_col]
            .transform(lambda x: x.rolling(window=window, min_periods=1).std())
        )

    # 4. Price vs promedio (¿está en descuento?)
    logger.info("  Creating price_vs_mean features")
    df_result['price_vs_mean_4w'] = (
        df_result[price_col] / (df_result['price_rolling_mean_4'] + 1e-6)
    )

    df_result['price_is_discount'] = (df_result['price_vs_mean_4w'] < 0.95).astype(int)
    df_result['price_is_premium'] = (df_result['price_vs_mean_4w'] > 1.05).astype(int)

    # 5. Volatilidad de precio
    logger.info("  Creating price_volatility")
    df_result['price_volatility'] = (
        df_result['price_rolling_std_4'] / (df_result['price_rolling_mean_4'] + 1e-6)
    )

    # Limpiar columnas temporales
    temp_cols = ['price_lag_1', 'price_lag_4']
    df_result = df_result.drop(columns=[c for c in temp_cols if c in df_result.columns])

    new_cols = [c for c in df_result.columns if c not in df.columns]
    logger.info(f"✓ Created {len(new_cols)} price features")

    return df_result


def create_price_category_features(
    df: pd.DataFrame,
    price_col: str = 'sell_price',
    category_col: str = 'cat_id',
    **kwargs
) -> pd.DataFrame:
    """
    Crear features de precio relativo a la categoría.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con precios y categorías
    price_col : str
        Columna de precio
    category_col : str
        Columna de categoría

    Returns
    -------
    pd.DataFrame
        DataFrame con features de precio por categoría
    """
    logger.info("Creating price vs category features")

    df_result = df.copy()

    # Precio promedio por categoría
    logger.info("  Calculating category average prices")
    cat_avg_price = df_result.groupby(category_col)[price_col].transform('mean')
    df_result['price_vs_category_avg'] = df_result[price_col] / (cat_avg_price + 1e-6)

    # Percentil del precio dentro de la categoría
    logger.info("  Calculating price percentile in category")
    df_result['price_percentile_in_cat'] = (
        df_result.groupby(category_col)[price_col]
        .transform(lambda x: x.rank(pct=True))
    )

    # Es precio alto/bajo en categoría
    df_result['is_expensive_in_cat'] = (df_result['price_percentile_in_cat'] > 0.75).astype(int)
    df_result['is_cheap_in_cat'] = (df_result['price_percentile_in_cat'] < 0.25).astype(int)

    new_cols = [c for c in df_result.columns if c not in df.columns]
    logger.info(f"✓ Created {len(new_cols)} category price features")

    return df_result


def get_price_feature_info() -> Dict[str, any]:
    """
    Información sobre price features.

    Returns
    -------
    Dict
        Información de features de precio
    """
    return {
        'basic_features': [
            'price_change_pct',  # % change from previous period
            'price_momentum',  # Trend over 4 weeks
            'price_volatility',  # Coefficient of variation
        ],
        'rolling_features': [
            'price_rolling_mean_4',  # 4-week average
            'price_rolling_mean_8',  # 8-week average
            'price_rolling_std_4',  # 4-week volatility
        ],
        'discount_features': [
            'price_is_discount',  # Below 4-week average
            'price_is_premium',  # Above 4-week average
            'price_vs_mean_4w',  # Ratio to 4-week mean
        ],
        'category_features': [
            'price_vs_category_avg',  # Relative to category
            'price_percentile_in_cat',  # Position in category
            'is_expensive_in_cat',  # Top 25% in category
            'is_cheap_in_cat',  # Bottom 25% in category
        ],
        'importance': {
            'price_change_pct': 'HIGH - Price changes drive demand',
            'price_is_discount': 'HIGH - Discounts boost sales',
            'price_momentum': 'MEDIUM - Longer-term trends',
            'price_volatility': 'LOW - May indicate promotional items'
        },
        'notes': {
            'granularity': 'M5 prices are weekly (wm_yr_wk)',
            'correlation': 'Expected negative correlation with sales',
            'elasticity': 'Varies by category (FOODS more elastic)'
        }
    }


if __name__ == "__main__":
    # Test
    logger.info("Testing price features module")

    # Datos de prueba
    np.random.seed(42)
    test_df = pd.DataFrame({
        'store_id': ['CA_1'] * 50 + ['CA_2'] * 50,
        'item_id': ['ITEM_1'] * 50 + ['ITEM_2'] * 50,
        'cat_id': ['FOODS'] * 50 + ['HOBBIES'] * 50,
        'wm_yr_wk': list(range(11101, 11151)) * 2,
        'sell_price': np.random.uniform(2, 10, 100)
    })

    # Añadir algunos cambios de precio
    test_df.loc[20:25, 'sell_price'] *= 0.8  # Discount
    test_df.loc[70:75, 'sell_price'] *= 1.2  # Premium

    # Crear features
    result = create_price_features(test_df)
    result = create_price_category_features(result)

    logger.info(f"\nOriginal shape: {test_df.shape}")
    logger.info(f"Result shape: {result.shape}")
    logger.info(f"\nPrice features created: {result.shape[1] - test_df.shape[1]}")

    # Sample
    sample_cols = ['sell_price', 'price_change_pct', 'price_is_discount', 'price_vs_category_avg']
    logger.info(f"\nSample:\n{result[sample_cols].head(30)}")

    # Info
    info = get_price_feature_info()
    logger.info(f"\n\nFeature categories: {list(info.keys())}")
