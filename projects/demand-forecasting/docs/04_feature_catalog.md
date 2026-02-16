# Feature Catalog - Walmart Demand Forecasting

**Autor**: Ing. Daniel Varela Perez
**Email**: bedaniele0@gmail.com
**Tel**: +52 55 4189 3428
**Fecha**: 4 de Diciembre, 2024
**Versión**: 1.0

---

## 📋 FASE 4: FEATURE ENGINEERING (DVP-PRO, demo)

---

## 1. Resumen Ejecutivo

Este documento cataloga todas las features generadas para el modelo de forecasting de demanda. El pipeline de feature engineering crea **~80-100 features** agrupadas en 5 categorías principales (en el modelo demo actual se registran **93** features).

### Features Totales Estimadas (demo):
- **Calendar Features**: ~20-25 features
- **Lag Features**: ~6 features
- **Rolling Features**: ~16-24 features
- **Price Features**: ~15-20 features
- **Event & SNAP Features**: ~15-20 features

---

## 2. Calendar Features (20-25 features)

### 2.1 Componentes Básicos

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| `day_of_week` | int | 0-6 | 0=Monday, 6=Sunday |
| `day_of_month` | int | 1-31 | Día del mes |
| `day_of_year` | int | 1-366 | Día del año |
| `week_of_year` | int | 1-53 | Semana del año (ISO) |
| `month` | int | 1-12 | Mes del año |
| `quarter` | int | 1-4 | Trimestre |
| `year` | int | 2011-2016* | Año |

*Rango basado en el dataset M5 (demo); ajustar si se usan años diferentes.

### 2.2 Features Booleanas

| Feature | Type | Description | Importancia |
|---------|------|-------------|-------------|
| `is_weekend` | int (0/1) | Sábado o Domingo | **CRITICAL** |
| `is_month_start` | int (0/1) | Primer día del mes | MEDIUM |
| `is_month_end` | int (0/1) | Último día del mes | MEDIUM |
| `is_quarter_start` | int (0/1) | Inicio de trimestre | LOW |
| `is_quarter_end` | int (0/1) | Fin de trimestre | MEDIUM |
| `is_year_start` | int (0/1) | 1 de enero | LOW |
| `is_year_end` | int (0/1) | 31 de diciembre | LOW |

**Insight**: `is_weekend` es CRÍTICO - EDA mostró ~45% diferencia en ventas.

### 2.3 Encoding Cíclico

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| `dow_sin` | float | [-1, 1] | Sin(day_of_week) |
| `dow_cos` | float | [-1, 1] | Cos(day_of_week) |
| `month_sin` | float | [-1, 1] | Sin(month) |
| `month_cos` | float | [-1, 1] | Cos(month) |
| `dom_sin` | float | [-1, 1] | Sin(day_of_month) |
| `dom_cos` | float | [-1, 1] | Cos(day_of_month) |

**Rationale**: Encoding cíclico preserva la naturaleza circular (diciembre está cerca de enero).

### 2.4 Holiday Features

| Feature | Type | Description | Importancia |
|---------|------|-------------|-------------|
| `days_to_christmas` | int | Días hasta próxima navidad | HIGH |
| `days_to_thanksgiving` | int | Días hasta próximo Thanksgiving | MEDIUM |
| `near_christmas` | int (0/1) | ≤7 días de navidad | HIGH |
| `near_thanksgiving` | int (0/1) | ≤7 días de Thanksgiving | MEDIUM |
| `is_major_holiday` | int (0/1) | Navidad, Año Nuevo, etc. | MEDIUM |

---

## 3. Lag Features (6 features)

Features basadas en valores históricos de ventas (shifts por serie `id`).

| Feature | Lag (días) | Description | Importancia |
|---------|-----------|-------------|-------------|
| `sales_lag_1` | 1 | Venta de ayer | MEDIUM |
| `sales_lag_2` | 2 | Venta hace 2 días | LOW |
| `sales_lag_3` | 3 | Venta hace 3 días | LOW |
| `sales_lag_7` | 7 | Venta semana pasada | **HIGH** |
| `sales_lag_14` | 14 | Venta hace 2 semanas | MEDIUM |
| `sales_lag_28` | 28 | Venta hace 4 semanas | **HIGH** |

### Interpretación:
- **Lag 7**: Captura seasonality semanal (patrón weekend)
- **Lag 28**: Captura seasonality mensual
- **Lag 1-3**: Capturan tendencia de corto plazo

### Data Loss:
- Lag 1: 0.05% (1 día de ~1900)
- Lag 7: 0.37% (7 días)
- Lag 28: 1.46% (28 días)

---

## 4. Rolling Statistics Features (16-24 features)

Features de ventanas deslizantes sobre ventas históricas.

### 4.1 Rolling Mean (Tendencia)

| Feature | Window | Description | Importancia |
|---------|--------|-------------|-------------|
| `sales_rolling_mean_7` | 7 días | Promedio última semana | **HIGH** |
| `sales_rolling_mean_14` | 14 días | Promedio últimas 2 semanas | MEDIUM |
| `sales_rolling_mean_28` | 28 días | Promedio último mes | **HIGH** |
| `sales_rolling_mean_90` | 90 días | Promedio último trimestre | MEDIUM |

### 4.2 Rolling Std (Volatilidad)

| Feature | Window | Description | Importancia |
|---------|--------|-------------|-------------|
| `sales_rolling_std_7` | 7 días | Volatilidad última semana | MEDIUM |
| `sales_rolling_std_14` | 14 días | Volatilidad 2 semanas | LOW |
| `sales_rolling_std_28` | 28 días | Volatilidad último mes | MEDIUM |
| `sales_rolling_std_90` | 90 días | Volatilidad trimestre | LOW |

### 4.3 Rolling Min/Max (Rango)

| Feature | Window | Description |
|---------|--------|-------------|
| `sales_rolling_min_7/14/28/90` | Variable | Mínimo en ventana |
| `sales_rolling_max_7/14/28/90` | Variable | Máximo en ventana |

### 4.4 Advanced Rolling Features (demo)

| Feature | Description | Importancia |
|---------|-------------|-------------|
| `sales_rolling_q25_7` | Percentil 25 (7 días) | LOW |
| `sales_rolling_q50_7` | Mediana (7 días) | MEDIUM |
| `sales_rolling_q75_7` | Percentil 75 (7 días) | LOW |
| `sales_rolling_cv_7` | Coef. variación (std/mean) | MEDIUM |
| `sales_rolling_trend_7` | Cambio de tendencia | MEDIUM |

---

## 5. Price Features (15-20 features)

Features basadas en precios y cambios de precio (si `sell_price` está disponible).

### 5.1 Price Changes

| Feature | Description | Importancia |
|---------|-------------|-------------|
| `sell_price` | Precio actual (semanal) | HIGH |
| `price_change_pct` | % cambio vs semana anterior | **HIGH** |
| `price_momentum` | Tendencia últimas 4 semanas | MEDIUM |

**Correlation**: Esperada negativa con ventas (elasticidad de demanda).

### 5.2 Price Rolling Statistics

| Feature | Window | Description |
|---------|--------|-------------|
| `price_rolling_mean_4` | 4 semanas | Precio promedio |
| `price_rolling_mean_8` | 8 semanas | Precio promedio |
| `price_rolling_mean_12` | 12 semanas | Precio promedio |
| `price_rolling_std_4/8/12` | Variable | Volatilidad precio |

### 5.3 Price vs Mean Features

| Feature | Description | Importancia |
|---------|-------------|-------------|
| `price_vs_mean_4w` | Precio / mean(4w) | HIGH |
| `price_is_discount` | price < 0.95 * mean | **HIGH** |
| `price_is_premium` | price > 1.05 * mean | MEDIUM |
| `price_volatility` | std / mean | LOW |

### 5.4 Category-Relative Price

| Feature | Description | Importancia |
|---------|-------------|-------------|
| `price_vs_category_avg` | Precio relativo a categoría | MEDIUM |
| `price_percentile_in_cat` | Percentil en categoría | LOW |
| `is_expensive_in_cat` | Top 25% en categoría | LOW |
| `is_cheap_in_cat` | Bottom 25% en categoría | LOW |

---

## 6. Event & SNAP Features (15-20 features)

### 6.1 Event Features

| Feature | Type | Description | Importancia |
|---------|------|-------------|-------------|
| `is_event` | int (0/1) | Hay evento hoy | MEDIUM |
| `event_type_cultural` | int (0/1) | Evento cultural | LOW |
| `event_type_national` | int (0/1) | Evento nacional | MEDIUM |
| `event_type_religious` | int (0/1) | Evento religioso | LOW |
| `event_type_sporting` | int (0/1) | Evento deportivo | LOW |
| `num_events` | int (0-2) | Número de eventos | LOW |

**Note**: EDA mostró efecto mixto de eventos - requiere análisis por categoría.

### 6.2 SNAP Features

| Feature | Type | Description | Importancia |
|---------|------|-------------|-------------|
| `snap_CA` | int (0/1) | SNAP activo en California | LOW |
| `snap_TX` | int (0/1) | SNAP activo en Texas | LOW |
| `snap_WI` | int (0/1) | SNAP activo en Wisconsin | LOW |
| `snap_any` | int (0/1) | SNAP activo en algún estado | MEDIUM |
| `snap_count` | int (0-3) | Estados con SNAP activo | LOW |

### 6.3 SNAP × State Interactions

| Feature | Description | Importancia |
|---------|-------------|-------------|
| `snap_active_ca` | SNAP AND state=CA | LOW |
| `snap_active_tx` | SNAP AND state=TX | LOW |
| `snap_active_wi` | SNAP AND state=WI | LOW |

### 6.4 Event × Category Interactions

| Feature | Description | Importancia |
|---------|-------------|-------------|
| `event_x_foods` | Event AND category=FOODS | MEDIUM |
| `event_x_hobbies` | Event AND category=HOBBIES | LOW |
| `event_x_household` | Event AND category=HOUSEHOLD | LOW |
| `snap_x_foods` | SNAP AND category=FOODS | **MEDIUM** |

**Insight**: SNAP afecta principalmente a FOODS.

---

## 7. Feature Importancia Summary (demo)

### Critical Features (Must Have)
1. `is_weekend` - 45% impacto en ventas
2. `sales_lag_7` - Weekly seasonality
3. `sales_rolling_mean_7` - Tendencia semanal
4. `price_change_pct` - Elasticidad de demanda
5. `price_is_discount` - Promociones

### High Importance Features
- `sales_lag_28` - Monthly seasonality
- `sales_rolling_mean_28` - Tendencia mensual
- `day_of_week` - Patrón semanal
- `month` - Seasonality anual
- `sell_price` - Nivel de precio

### Medium Importance Features
- Calendar features (quarter, holidays)
- Rolling std features (volatilidad)
- Event type features
- SNAP × FOODS interaction

### Low Importance Features
- Lag 2, 3 (redundantes con lag 1)
- Event features individuales
- SNAP por estado (similares)
- Price percentiles

---

## 8. Data Leakage Prevention

### Reglas Implementadas:

1. **Lag Features**: Siempre shift() por grupo
2. **Rolling Features**: `min_periods=1`, no lookahead
3. **Price Features**: Solo histórico, no futuro
4. **Calendar Features**: OK (no dependen de target)
5. **Event Features**: Del calendario (conocidas de antemano)

### Validaciones:
- ✅ No usar información del futuro
- ✅ Rolling windows solo hacia atrás
- ✅ Lags shifteados correctamente
- ✅ Split temporal train/val

---

## 9. Missing Values Strategy

| Feature Type | NaN% | Strategy |
|--------------|------|----------|
| Lag 1 | 0.05% | Primeros días - Drop o Fill 0 |
| Lag 7 | 0.37% | Primera semana - Drop o Fill 0 |
| Lag 28 | 1.46% | Primer mes - Drop o Fill 0 |
| Rolling | <5% | min_periods=1 (completa con disponible) |
| Price | 0% | No NaNs (merge completo) |
| Calendar | 0% | No NaNs (generadas) |
| Event | 0% | No NaNs (binarias) |

**Recomendación**: En demo se puede imputar o recortar los primeros 28 días por serie (loss: ~1.5%).

---

## 10. Feature Selection Recommendations

### Estrategia de Selección:

1. **Correlación Alta** (>0.95): Remover redundantes
   - Ejemplo: Lag 2 y Lag 3 probablemente redundantes con Lag 1

2. **Importancia Baja** (<0.01 en tree-based models)
   - Remover después de feature importance analysis

3. **Varianza Cero**
   - Remover features constantes

4. **Multicolinealidad**
   - VIF analysis para features numéricas

### Expected Final Feature Count:
- **Inicio**: ~80-100 features (demo actual: 93)
- **Después de selección**: ~40-60 features
- **Core features**: ~20-30 features más importantes

---

## 11. Computational Considerations

### Memory Usage:
- **Original data**: ~455 MB (sales, M5 completo)
- **Con features**: ~800-1000 MB estimado
- **Optimization**: Usar dtypes eficientes

### Processing Time (30,490 series):
- Calendar features: ~5-10s
- Lag features: ~30-60s
- Rolling features: ~2-5 min
- Price features: ~10-20s
- Event features: ~5-10s
- **Total**: ~5-10 minutos

### Optimization Tips:
1. Procesar por batches si memory issues
2. Usar `transform()` en lugar de loops
3. Parallelizar por grupo (multiprocessing)
4. Cachear resultados intermedios

---

## 12. Usage Example

```python
from src.features import FeatureEngineeringPipeline

# Initialize pipeline
pipeline = FeatureEngineeringPipeline(config_path='config/config.yaml')

# Run full pipeline
df_features = pipeline.run(
    df_sales=sales,        # requiere columnas id/date/sales + ids de tienda/item
    df_calendar=calendar,  # opcional (eventos/SNAP)
    df_prices=prices,      # opcional (sell_price)
    include_advanced=True
)

# Get feature catalog
features = pipeline.get_feature_catalog()
print(f"Total features: {len(features)}")

# Get feature groups
groups = pipeline.get_feature_groups()
print(f"Lag features: {len(groups['lag'])}")
print(f"Rolling features: {len(groups['rolling'])}")

# Validate features
validation = pipeline.validate_features(df_features)
print(f"Features with NaNs: {len(validation['missing_values'])}")
```

---

## 13. Next Steps (Fase 5, demo)

**Después de Feature Engineering**:

1. ✅ **Baseline Modeling** (demo disponible)
   - Naive forecast
   - Moving average
   - Exponential smoothing

2. ✅ **ML Modeling** (demo LightGBM)
   - LightGBM (primary)
   - XGBoost (secondary)
   - Feature importance analysis

3. ✅ **Feature Selection** (pendiente de ajuste fino)
   - Remove low importance features
   - Correlation analysis
   - Final feature set

4. ✅ **Model Evaluation** (métricas de demo)
   - WRMSSE metric
   - Time-series CV
   - Walk-forward validation

---

## 14. Referencias

### Código:
- `src/features/build_features.py`
- `src/features/calendar_features.py`
- `src/features/lag_features.py`
- `src/features/rolling_features.py`
- `src/features/price_features.py`
- `src/features/event_features.py`

### Configuración:
- `config/config.yaml` - Feature parameters

---

**Elaborado por**:
Ing. Daniel Varela Perez
Senior Data Scientist & ML Engineer
📧 bedaniele0@gmail.com
📱 +52 55 4189 3428

**Versión**: 1.0 - Feature Catalog
**Fecha**: 4 de Diciembre, 2024
**Status**: ✅ Feature Engineering (demo) listo

---

**Next Phase**: Baseline Modeling (Fase 5)
