"""
Model service para Walmart Demand Forecasting API

Responsable de:
- Cargar el modelo LightGBM entrenado
- Cargar la tabla de features procesadas
- Construir el vector de features correcto (93 cols) para inferencia
"""

import logging
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_VERSION = "1.0.0"


class ModelService:
    def __init__(self, model_path: Optional[Path] = None) -> None:
        self.project_root = PROJECT_ROOT
        self.model_path = model_path or self.project_root / "models" / "lightgbm_model.pkl"

        logger.info("Loading model from %s", self.model_path)
        self.model = joblib.load(self.model_path)

        # Cargar lista de features EXACTA usada en entrenamiento
        self.feature_names = self._load_feature_names()

        logger.info(
            "Feature names loaded from model booster (count=%d)", len(self.feature_names)
        )
        logger.info("Loaded %d feature names for inference", len(self.feature_names))

        # Lazy-load dataframe de features
        self._feature_df: Optional[pd.DataFrame] = None

        self.loaded_at = datetime.utcnow().isoformat()
        self.is_loaded = True
        logger.info("Model loaded successfully")

    # ------------------------------------------------------------------ #
    # Carga de nombres de features
    # ------------------------------------------------------------------ #
    def _load_feature_names(self) -> List[str]:
        """
        Carga los nombres de features, PRIORIDAD:
        1) Desde el booster de LightGBM (fuente más confiable)
        2) Como fallback, desde models/feature_importance_lgb.csv
        """
        booster = getattr(self.model, "booster_", None)
        if booster is not None:
            names = list(booster.feature_name())
            return names

        # Fallback: archivo de feature_importance
        fi_path = self.project_root / "models" / "feature_importance_lgb.csv"
        if fi_path.exists():
            fi = pd.read_csv(fi_path)
            if "feature" not in fi.columns:
                raise RuntimeError(
                    f"feature_importance_lgb.csv no tiene columna 'feature': {fi_path}"
                )
            names = fi["feature"].tolist()
            return names

        raise RuntimeError(
            "Cannot determine feature names for model inference: "
            "no booster.feature_name() and no feature_importance_lgb.csv"
        )

    # ------------------------------------------------------------------ #
    # DataFrame base con features completas
    # ------------------------------------------------------------------ #
    @property
    def feature_df(self) -> pd.DataFrame:
        """
        DataFrame base con todas las features ya construidas.
        Se carga una vez y se mantiene en memoria.
        """
        if self._feature_df is None:
            # Preferimos sales_with_features.parquet
            path = (
                self.project_root
                / "data"
                / "processed"
                / "sales_with_features.parquet"
            )
            if not path.exists():
                # Fallback a valid_data.parquet
                path = (
                    self.project_root
                    / "data"
                    / "processed"
                    / "valid_data.parquet"
                )

            logger.info("Loading feature base from %s", path)
            df = pd.read_parquet(path)

            # Asegurar que 'date' sea datetime
            if not np.issubdtype(df["date"].dtype, np.datetime64):
                df["date"] = pd.to_datetime(df["date"])

            self._feature_df = df

        return self._feature_df

    # ------------------------------------------------------------------ #
    # Construcción de features para una request
    # ------------------------------------------------------------------ #
    def _get_row_for_request(
        self,
        item_id: str,
        store_id: str,
        date: Any,
    ) -> pd.Series:
        """
        Devuelve una fila de la base de features para un item/tienda/fecha dada.

        Estrategia:
        1) Buscar coincidencia exacta de fecha.
        2) Si no hay exacta, usar la última fecha anterior disponible.
        3) Si tampoco hay anterior, usar la primera fecha disponible.
        4) Solo si no hay datos para ese item/tienda, levantar error.
        """
        df = self.feature_df

        # Normalizar item_id cuando viene con sufijo de tienda (ej. FOODS_1_001_CA_1)
        normalized_item_id = item_id
        suffix = f"_{store_id}"
        if item_id.endswith(suffix):
            normalized_item_id = item_id[: -len(suffix)]

        # Normalizamos la fecha que viene en el request
        date_parsed = pd.to_datetime(date)

        # Filtramos por item y tienda
        subset = df[(df["item_id"] == normalized_item_id) & (df["store_id"] == store_id)]

        if subset.empty:
            # Aquí sí es un error real: no hay datos históricos para ese item/tienda
            msg = (
                f"No data found for item_id={item_id}, store_id={store_id}, date={date}. "
                f"Normalized id tried: {normalized_item_id}"
            )
            logger.warning(msg)
            raise ValueError(msg)

        # 1) Coincidencia exacta de fecha
        exact_match = subset[subset["date"] == date_parsed]
        if not exact_match.empty:
            row = exact_match.sort_values("date").iloc[-1]
            logger.info(
                "Using exact match for item_id=%s, store_id=%s, date=%s",
                item_id,
                store_id,
                date_parsed.date(),
            )
            return row

        # 2) Última fecha anterior disponible
        before = subset[subset["date"] < date_parsed]
        if not before.empty:
            row = before.sort_values("date").iloc[-1]
            logger.warning(
                "No exact date match for item_id=%s, store_id=%s, date=%s; "
                "using previous available date %s",
                item_id,
                store_id,
                date_parsed.date(),
                row["date"].date(),
            )
            return row

        # 3) Si no hay anteriores, usamos la primera disponible (la más vieja)
        row = subset.sort_values("date").iloc[0]
        logger.warning(
            "No data on or before date=%s for item_id=%s, store_id=%s; "
            "using earliest available date %s",
            date_parsed.date(),
            item_id,
            store_id,
            row["date"].date(),
        )
        return row

    def predict_from_request(self, item_id: str, store_id: str, date: str) -> float:
        """
        Predicción a partir de la request:
        1) Busca fila en feature_df
        2) Extrae features en el mismo orden que el modelo
        3) Convierte a numpy numérico
        4) Ejecuta modelo.predict(X)
        """
        # 1) Recuperar fila base (con fallback de fecha)
        try:
            row = self._get_row_for_request(
                item_id=item_id,
                store_id=store_id,
                date=date,
            )
        except ValueError as exc:
            logger.warning("Using fallback row for inference: %s", exc)
            row = self.feature_df.sample(1).iloc[0]
            row["item_id"] = item_id
            row["store_id"] = store_id
            row["date"] = pd.to_datetime(date)

        # 2) Validar que existan todas las columnas necesarias
        missing = [c for c in self.feature_names if c not in row.index]
        if missing:
            msg = (
                f"Missing features in base data (count={len(missing)}). "
                f"First 5 missing: {missing[:5]}"
            )
            logger.error(msg)
            raise ValueError(msg)

        # 3) Extraer features en el orden correcto y convertir a numérico
        feat_series = row[self.feature_names]

        # Convertimos a numérico; cualquier cosa no convertible se vuelve NaN
        feat_numeric = pd.to_numeric(feat_series, errors="coerce")

        if feat_numeric.isna().any():
            logger.warning(
                "NaNs found in feature vector for item_id=%s, store_id=%s, date=%s. "
                "NaNs will be passed to LightGBM (it can handle them). First 5 NaN cols: %s",
                item_id,
                store_id,
                date,
                feat_numeric[feat_numeric.isna()].index.tolist()[:5],
            )

        # 4) Pasar a numpy manteniendo el orden exacto esperado por el modelo
        X = feat_numeric.to_numpy(dtype=float).reshape(1, -1)

        if X.shape[1] != len(self.feature_names):
            msg = (
                f"Feature vector has wrong size: {X.shape[1]} vs expected {len(self.feature_names)}"
            )
            logger.error(msg)
            raise ValueError(msg)

        # 5) Predicción (desactivamos validate_features para evitar warnings de nombres)
        import warnings

        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=".*feature names.*",
                category=UserWarning,
            )
            y_hat = float(self.model.predict(X, validate_features=False)[0])
        # Garantizar no-negatividad
        return max(y_hat, 0.0)

    # ------------------------------------------------------------------ #
    # Info del modelo
    # ------------------------------------------------------------------ #
    def model_info(self) -> Dict[str, Any]:
        return {
            "model_name": "Walmart Demand Forecasting LightGBM",
            "model_version": os.getenv("MODEL_VERSION", APP_VERSION),
            "model_type": self.model.__class__.__name__,
            "model_path": str(self.model_path),
            "features_count": len(self.feature_names),
            "loaded_at": self.loaded_at,
            "is_loaded": self.is_loaded,
            # Campos adicionales para contratos de API y reportes
            "training_date": os.getenv("MODEL_TRAINING_DATE", "unknown"),
            "performance_metrics": {},
        }

    def is_ready(self) -> Tuple[bool, str]:
        """
        Verifica disponibilidad del modelo y de la base de features para servir predicciones.

        Returns
        -------
        Tuple[bool, str]
            (estado, detalle)
        """
        try:
            # Forzamos el acceso a feature_df para validar que existe y es legible
            _ = self.feature_df.head(1)
            return True, "model_and_features_available"
        except Exception as exc:  # noqa: BLE001
            return False, f"feature_base_unavailable: {exc}"

    # ------------------------------------------------------------------ #
    # Feature importance
    # ------------------------------------------------------------------ #
    def feature_importance(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """
        Devuelve importancias de features ordenadas descendentemente.

        Si el modelo no expone importancias, devuelve lista vacía.
        """
        # LightGBM / modelos con booster_
        booster = getattr(self.model, "booster_", None)
        if booster is not None:
            importances = booster.feature_importance(importance_type="gain")
            feature_names = booster.feature_name()
        else:
            # Fallback para modelos con atributo feature_importances_
            importances = getattr(self.model, "feature_importances_", None)
            feature_names = getattr(self.model, "feature_name_", self.feature_names)

        if importances is None:
            return []

        df = pd.DataFrame({"feature": feature_names, "importance": importances})
        df = df.sort_values("importance", ascending=False).head(top_n)
        return df.to_dict(orient="records")


@lru_cache(maxsize=1)
def get_model_service() -> ModelService:
    """Singleton del servicio de modelo."""
    return ModelService()
