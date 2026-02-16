"""
Calendar Features Module
Crear features basadas en calendario (día, mes, eventos, etc.)

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


def create_calendar_features(
    df: pd.DataFrame,
    date_col: str = 'date',
    include_cyclical: bool = True,
    **kwargs
) -> pd.DataFrame:
    """
    Crear features basadas en información de calendario.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con columna de fecha
    date_col : str
        Nombre de la columna de fecha
    include_cyclical : bool
        Si incluir encoding cíclico (sin, cos) para variables circulares

    Returns
    -------
    pd.DataFrame
        DataFrame con calendar features añadidas

    Features Creadas
    ----------------
    - day_of_week: 0=Monday, 6=Sunday
    - day_of_month: 1-31
    - day_of_year: 1-365/366
    - week_of_year: 1-52/53
    - month: 1-12
    - quarter: 1-4
    - year: 2011-2016
    - is_weekend: Boolean
    - is_month_start/end: Boolean
    - is_quarter_start/end: Boolean
    - is_year_start/end: Boolean
    - Cyclical encodings (si include_cyclical=True)
    """
    logger.info("Creating calendar features")

    df_result = df.copy()

    # Asegurar que date_col es datetime
    if not pd.api.types.is_datetime64_any_dtype(df_result[date_col]):
        df_result[date_col] = pd.to_datetime(df_result[date_col])

    # Extraer componentes básicos
    logger.info("  Extracting basic calendar components")
    df_result['day_of_week'] = df_result[date_col].dt.dayofweek  # 0=Monday
    df_result['day_of_month'] = df_result[date_col].dt.day
    df_result['day_of_year'] = df_result[date_col].dt.dayofyear
    df_result['week_of_year'] = df_result[date_col].dt.isocalendar().week
    df_result['month'] = df_result[date_col].dt.month
    df_result['quarter'] = df_result[date_col].dt.quarter
    df_result['year'] = df_result[date_col].dt.year

    # Features booleanas
    logger.info("  Creating boolean features")
    df_result['is_weekend'] = (df_result['day_of_week'] >= 5).astype(int)
    df_result['is_month_start'] = df_result[date_col].dt.is_month_start.astype(int)
    df_result['is_month_end'] = df_result[date_col].dt.is_month_end.astype(int)
    df_result['is_quarter_start'] = df_result[date_col].dt.is_quarter_start.astype(int)
    df_result['is_quarter_end'] = df_result[date_col].dt.is_quarter_end.astype(int)
    df_result['is_year_start'] = df_result[date_col].dt.is_year_start.astype(int)
    df_result['is_year_end'] = df_result[date_col].dt.is_year_end.astype(int)

    # Encoding cíclico para variables circulares
    if include_cyclical:
        logger.info("  Creating cyclical encodings")

        # Day of week (0-6)
        df_result['dow_sin'] = np.sin(2 * np.pi * df_result['day_of_week'] / 7)
        df_result['dow_cos'] = np.cos(2 * np.pi * df_result['day_of_week'] / 7)

        # Month (1-12)
        df_result['month_sin'] = np.sin(2 * np.pi * df_result['month'] / 12)
        df_result['month_cos'] = np.cos(2 * np.pi * df_result['month'] / 12)

        # Day of month (1-31)
        df_result['dom_sin'] = np.sin(2 * np.pi * df_result['day_of_month'] / 31)
        df_result['dom_cos'] = np.cos(2 * np.pi * df_result['day_of_month'] / 31)

    # Contar features creadas
    new_cols = [c for c in df_result.columns if c not in df.columns]
    logger.info(f"✓ Created {len(new_cols)} calendar features")

    return df_result


def create_holiday_features(
    df: pd.DataFrame,
    calendar_df: pd.DataFrame = None,
    date_col: str = 'date',
    **kwargs
) -> pd.DataFrame:
    """
    Crear features basadas en días festivos y eventos especiales.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame principal
    calendar_df : pd.DataFrame
        DataFrame de calendario con eventos (M5 calendar.csv)
    date_col : str
        Columna de fecha

    Returns
    -------
    pd.DataFrame
        DataFrame con holiday features

    Features Creadas
    ----------------
    - days_to_christmas: Días hasta navidad
    - days_to_thanksgiving: Días hasta thanksgiving
    - days_to_superbowl: Días hasta superbowl
    - is_major_holiday: Boolean para fechas importantes
    """
    logger.info("Creating holiday features")

    df_result = df.copy()

    # Asegurar datetime
    if not pd.api.types.is_datetime64_any_dtype(df_result[date_col]):
        df_result[date_col] = pd.to_datetime(df_result[date_col])

    # Definir holidays importantes
    def days_to_christmas(date):
        """Calcular días hasta próxima navidad"""
        year = date.year
        christmas = pd.Timestamp(f'{year}-12-25')

        # Si ya pasó navidad este año, usar próximo año
        if date > christmas:
            christmas = pd.Timestamp(f'{year + 1}-12-25')

        return (christmas - date).days

    def days_to_thanksgiving(date):
        """Días hasta próximo Thanksgiving (4to jueves de noviembre)"""
        year = date.year

        # Encontrar 4to jueves de noviembre
        nov_first = pd.Timestamp(f'{year}-11-01')
        # Primer jueves
        days_to_thursday = (3 - nov_first.dayofweek) % 7
        first_thursday = nov_first + pd.Timedelta(days=days_to_thursday)
        # Cuarto jueves
        thanksgiving = first_thursday + pd.Timedelta(weeks=3)

        # Si ya pasó, usar próximo año
        if date > thanksgiving:
            year += 1
            nov_first = pd.Timestamp(f'{year}-11-01')
            days_to_thursday = (3 - nov_first.dayofweek) % 7
            first_thursday = nov_first + pd.Timedelta(days=days_to_thursday)
            thanksgiving = first_thursday + pd.Timedelta(weeks=3)

        return (thanksgiving - date).days

    # Aplicar funciones
    logger.info("  Calculating days to major holidays")
    df_result['days_to_christmas'] = df_result[date_col].apply(days_to_christmas)
    df_result['days_to_thanksgiving'] = df_result[date_col].apply(days_to_thanksgiving)

    # Proximity features (cercano a holiday = 1, lejos = 0)
    df_result['near_christmas'] = (df_result['days_to_christmas'] <= 7).astype(int)
    df_result['near_thanksgiving'] = (df_result['days_to_thanksgiving'] <= 7).astype(int)

    # Major holidays (lista de fechas específicas)
    major_holidays = [
        '-01-01',  # New Year
        '-07-04',  # Independence Day
        '-12-25',  # Christmas
    ]

    df_result['is_major_holiday'] = 0
    for holiday_suffix in major_holidays:
        for year in df_result['year'].unique():
            holiday_date = pd.Timestamp(f'{year}{holiday_suffix}')
            df_result.loc[df_result[date_col] == holiday_date, 'is_major_holiday'] = 1

    new_cols = [c for c in df_result.columns if c not in df.columns]
    logger.info(f"✓ Created {len(new_cols)} holiday features")

    return df_result


def get_calendar_feature_info() -> Dict[str, any]:
    """
    Obtener información sobre calendar features.

    Returns
    -------
    Dict
        Información de features de calendario
    """
    return {
        'basic_features': [
            'day_of_week', 'day_of_month', 'day_of_year',
            'week_of_year', 'month', 'quarter', 'year'
        ],
        'boolean_features': [
            'is_weekend', 'is_month_start', 'is_month_end',
            'is_quarter_start', 'is_quarter_end',
            'is_year_start', 'is_year_end'
        ],
        'cyclical_features': [
            'dow_sin', 'dow_cos',  # Day of week
            'month_sin', 'month_cos',  # Month
            'dom_sin', 'dom_cos'  # Day of month
        ],
        'holiday_features': [
            'days_to_christmas', 'days_to_thanksgiving',
            'near_christmas', 'near_thanksgiving',
            'is_major_holiday'
        ],
        'importance': {
            'is_weekend': 'CRITICAL - EDA showed 45% difference',
            'day_of_week': 'HIGH - Strong weekly seasonality',
            'month': 'HIGH - Annual seasonality',
            'cyclical_encodings': 'MEDIUM - Better than one-hot for trees'
        },
        'encoding_notes': {
            'cyclical': 'Use sin/cos to preserve circular nature (Dec is close to Jan)',
            'one_hot': 'Alternative for tree-based models, but creates more features'
        }
    }


if __name__ == "__main__":
    # Test
    logger.info("Testing calendar features module")

    # Datos de prueba
    test_df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', '2024-12-31', freq='D')
    })

    # Crear features
    result = create_calendar_features(test_df, include_cyclical=True)
    result = create_holiday_features(result)

    logger.info(f"\nOriginal shape: {test_df.shape}")
    logger.info(f"Result shape: {result.shape}")
    logger.info(f"\nCalendar features created: {result.shape[1] - test_df.shape[1]}")

    # Sample
    sample_cols = ['date', 'day_of_week', 'is_weekend', 'month', 'days_to_christmas']
    logger.info(f"\nSample:\n{result[sample_cols].head(10)}")

    # Weekend distribution
    logger.info(f"\nWeekend distribution:")
    logger.info(result['is_weekend'].value_counts())

    # Info
    info = get_calendar_feature_info()
    logger.info(f"\n\nTotal feature types: {len(info.keys())}")
