"""
Event and SNAP Features Module
Crear features basadas en eventos especiales y programa SNAP

Autor: Ing. Daniel Varela Perez
Email: bedaniele0@gmail.com
Tel: +52 55 4189 3428
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_event_features(
    df: pd.DataFrame,
    calendar_df: Optional[pd.DataFrame] = None,
    date_col: str = 'date',
    **kwargs
) -> pd.DataFrame:
    """
    Crear features basadas en eventos especiales.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame principal
    calendar_df : pd.DataFrame
        DataFrame del calendario M5 con eventos
    date_col : str
        Columna de fecha

    Returns
    -------
    pd.DataFrame
        DataFrame con event features

    Features Creadas
    ----------------
    - is_event: Si hay evento ese día
    - event_type_*: One-hot encoding de tipos de evento
    - days_to_event: Días hasta próximo evento
    - days_from_event: Días desde último evento
    - event_duration: Duración del evento (si es multi-día)
    """
    logger.info("Creating event features")

    df_result = df.copy()

    if calendar_df is not None:
        logger.info("  Merging with calendar data")

        # Merge con calendar
        if date_col not in calendar_df.columns and 'date' in calendar_df.columns:
            merge_col = 'date'
        elif 'd' in calendar_df.columns and 'd' in df_result.columns:
            merge_col = 'd'
        else:
            merge_col = date_col

        # Asegurar que ambos tienen la columna de merge
        if merge_col in df_result.columns and merge_col in calendar_df.columns:
            # Seleccionar columnas de eventos del calendar
            event_cols = [merge_col]
            if 'event_name_1' in calendar_df.columns:
                event_cols.append('event_name_1')
            if 'event_type_1' in calendar_df.columns:
                event_cols.append('event_type_1')
            if 'event_name_2' in calendar_df.columns:
                event_cols.append('event_name_2')
            if 'event_type_2' in calendar_df.columns:
                event_cols.append('event_type_2')

            calendar_events = calendar_df[event_cols].copy()

            # Merge
            df_result = df_result.merge(
                calendar_events,
                on=merge_col,
                how='left'
            )

    # 1. Boolean: hay evento
    logger.info("  Creating is_event feature")
    if 'event_name_1' in df_result.columns:
        df_result['is_event'] = df_result['event_name_1'].notna().astype(int)
    else:
        df_result['is_event'] = 0

    # 2. One-hot encoding de event types
    if 'event_type_1' in df_result.columns:
        logger.info("  Creating event_type one-hot encoding")

        # Tipos de eventos
        event_types = ['Cultural', 'National', 'Religious', 'Sporting']

        for etype in event_types:
            col_name = f'event_type_{etype.lower()}'
            df_result[col_name] = (df_result['event_type_1'] == etype).astype(int)

    # 3. Conteo de eventos (si hay event_2 también)
    if 'event_name_2' in df_result.columns:
        logger.info("  Counting multiple events per day")
        df_result['num_events'] = (
            df_result['event_name_1'].notna().astype(int) +
            df_result['event_name_2'].notna().astype(int)
        )
    else:
        df_result['num_events'] = df_result['is_event']

    new_cols = [c for c in df_result.columns if c not in df.columns]
    logger.info(f"✓ Created {len(new_cols)} event features")

    return df_result


def create_snap_features(
    df: pd.DataFrame,
    calendar_df: Optional[pd.DataFrame] = None,
    state_col: str = 'state_id',
    **kwargs
) -> pd.DataFrame:
    """
    Crear features basadas en programa SNAP.

    SNAP (Supplemental Nutrition Assistance Program) puede afectar
    las ventas, especialmente en categoría FOODS.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame principal
    calendar_df : pd.DataFrame
        DataFrame del calendario con SNAP info
    state_col : str
        Columna de estado

    Returns
    -------
    pd.DataFrame
        DataFrame con SNAP features

    Features Creadas
    ----------------
    - snap_*: SNAP activo por estado (CA, TX, WI)
    - snap_any: SNAP activo en algún estado
    - snap_count: Número de estados con SNAP activo
    """
    logger.info("Creating SNAP features")

    df_result = df.copy()

    if calendar_df is not None:
        logger.info("  Merging SNAP data from calendar")

        # Determinar columna de merge
        if 'd' in calendar_df.columns and 'd' in df_result.columns:
            merge_col = 'd'
        elif 'date' in calendar_df.columns and 'date' in df_result.columns:
            merge_col = 'date'
        else:
            logger.warning("Cannot find common column to merge SNAP data")
            return df_result

        # Seleccionar columnas SNAP
        snap_cols = [merge_col]
        for state in ['CA', 'TX', 'WI']:
            snap_col = f'snap_{state}'
            if snap_col in calendar_df.columns:
                snap_cols.append(snap_col)

        if len(snap_cols) > 1:
            calendar_snap = calendar_df[snap_cols].copy()

            # Merge
            df_result = df_result.merge(
                calendar_snap,
                on=merge_col,
                how='left'
            )

            # Features agregadas
            logger.info("  Creating aggregated SNAP features")

            # SNAP en algún estado
            snap_state_cols = [c for c in df_result.columns if c.startswith('snap_')]
            if snap_state_cols:
                df_result['snap_any'] = (
                    df_result[snap_state_cols].sum(axis=1) > 0
                ).astype(int)

                df_result['snap_count'] = df_result[snap_state_cols].sum(axis=1)

    # Interaction: SNAP × state (si aplica)
    if state_col in df_result.columns:
        logger.info(f"  Creating SNAP × state interaction")

        for state in ['CA', 'TX', 'WI']:
            snap_col = f'snap_{state}'
            if snap_col in df_result.columns:
                # SNAP activo Y estamos en ese estado
                df_result[f'snap_active_{state.lower()}'] = (
                    (df_result[state_col] == state) & (df_result[snap_col] == 1)
                ).astype(int)

    new_cols = [c for c in df_result.columns if c not in df.columns]
    logger.info(f"✓ Created {len(new_cols)} SNAP features")

    return df_result


def create_event_snap_interactions(
    df: pd.DataFrame,
    category_col: str = 'cat_id',
    **kwargs
) -> pd.DataFrame:
    """
    Crear interacciones entre eventos, SNAP y categorías.

    Ciertas categorías son más sensibles a eventos y SNAP.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame con event y SNAP features
    category_col : str
        Columna de categoría

    Returns
    -------
    pd.DataFrame
        DataFrame con interacciones
    """
    logger.info("Creating event × category and SNAP × category interactions")

    df_result = df.copy()

    # Event × Category
    if 'is_event' in df_result.columns and category_col in df_result.columns:
        logger.info("  Creating event × category")

        for category in ['FOODS', 'HOBBIES', 'HOUSEHOLD']:
            df_result[f'event_x_{category.lower()}'] = (
                (df_result['is_event'] == 1) & (df_result[category_col] == category)
            ).astype(int)

    # SNAP × Category (SNAP afecta principalmente a FOODS)
    if 'snap_any' in df_result.columns and category_col in df_result.columns:
        logger.info("  Creating SNAP × category")

        # SNAP × FOODS es la más importante
        df_result['snap_x_foods'] = (
            (df_result['snap_any'] == 1) & (df_result[category_col] == 'FOODS')
        ).astype(int)

    new_cols = [c for c in df_result.columns if c not in df.columns]
    logger.info(f"✓ Created {len(new_cols)} interaction features")

    return df_result


def get_event_snap_feature_info() -> Dict[str, any]:
    """
    Información sobre event y SNAP features.

    Returns
    -------
    Dict
        Información de features
    """
    return {
        'event_features': [
            'is_event',  # Boolean: any event today
            'event_type_cultural',  # Cultural event
            'event_type_national',  # National holiday
            'event_type_religious',  # Religious event
            'event_type_sporting',  # Sporting event
            'num_events',  # Count of events (0-2)
        ],
        'snap_features': [
            'snap_CA',  # SNAP active in California
            'snap_TX',  # SNAP active in Texas
            'snap_WI',  # SNAP active in Wisconsin
            'snap_any',  # SNAP active in any state
            'snap_count',  # Number of states with SNAP
        ],
        'interaction_features': [
            'snap_active_ca',  # SNAP active AND in CA state
            'event_x_foods',  # Event AND FOODS category
            'snap_x_foods',  # SNAP AND FOODS category
        ],
        'importance': {
            'is_event': 'MEDIUM - EDA showed mixed results',
            'event_type_*': 'LOW-MEDIUM - Need granular analysis',
            'snap_x_foods': 'MEDIUM - SNAP affects FOODS category',
            'snap_CA/TX/WI': 'LOW - Similar activation across states'
        },
        'notes': {
            'event_effect': 'Varies by event type and category',
            'snap_effect': 'Strongest in FOODS category',
            'data_frequency': 'SNAP: 33% of days, Events: 8.2% of days'
        }
    }


if __name__ == "__main__":
    # Test
    logger.info("Testing event and SNAP features module")

    # Datos de prueba
    test_df = pd.DataFrame({
        'd': [f'd_{i}' for i in range(1, 101)],
        'state_id': ['CA'] * 50 + ['TX'] * 50,
        'cat_id': ['FOODS'] * 30 + ['HOBBIES'] * 40 + ['HOUSEHOLD'] * 30
    })

    # Calendar simulado
    calendar_df = pd.DataFrame({
        'd': [f'd_{i}' for i in range(1, 101)],
        'event_name_1': [None] * 90 + ['SuperBowl'] * 10,
        'event_type_1': [None] * 90 + ['Sporting'] * 10,
        'snap_CA': [0] * 70 + [1] * 30,
        'snap_TX': [0] * 60 + [1] * 40,
        'snap_WI': [0] * 80 + [1] * 20
    })

    # Crear features
    result = create_event_features(test_df, calendar_df)
    result = create_snap_features(result, calendar_df)
    result = create_event_snap_interactions(result)

    logger.info(f"\nOriginal shape: {test_df.shape}")
    logger.info(f"Result shape: {result.shape}")
    logger.info(f"\nFeatures created: {result.shape[1] - test_df.shape[1]}")

    # Sample
    sample_cols = ['d', 'is_event', 'snap_CA', 'snap_any', 'snap_x_foods']
    logger.info(f"\nSample:\n{result[sample_cols].tail(15)}")

    # Info
    info = get_event_snap_feature_info()
    logger.info(f"\n\nTotal feature categories: {len(info)}")
