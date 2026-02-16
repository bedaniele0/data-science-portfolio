# Data Contract (F2)

**Proyecto**: Walmart Demand Forecasting & Inventory Optimization  
**Fecha**: 2026-02-06  

## Alcance

Contrato de datos para el dataset M5 (Walmart). Define archivos, llaves y campos esperados para el pipeline de forecasting y features.

## Datasets y llaves

### 1) `data/raw/sales_train_validation.csv`
**Grano**: producto-tienda-dia  
**Llave primaria**: `item_id`, `store_id`, `d_1..d_1913`  
**Campos mínimos esperados**:
- `item_id` (string)
- `dept_id` (string)
- `cat_id` (string)
- `store_id` (string)
- `state_id` (string)
- `d_1..d_1913` (int, ventas diarias)

### 2) `data/raw/calendar.csv`
**Grano**: dia  
**Llave primaria**: `d`  
**Campos mínimos esperados**:
- `d` (string, ej. d_1)
- `date` (YYYY-MM-DD)
- `wm_yr_wk` (int)
- `weekday`, `wday`, `month`, `year`
- `event_name_1`, `event_type_1`, `event_name_2`, `event_type_2`
- `snap_CA`, `snap_TX`, `snap_WI`

### 3) `data/raw/sell_prices.csv`
**Grano**: producto-tienda-semana  
**Llave primaria**: `store_id`, `item_id`, `wm_yr_wk`  
**Campos mínimos esperados**:
- `store_id` (string)
- `item_id` (string)
- `wm_yr_wk` (int)
- `sell_price` (float)

## Reglas de calidad (mínimas)

- Sin nulls en llaves.
- Fechas validas en `calendar.csv`.
- `sell_price` > 0 cuando exista registro.
- Ventas diarias no negativas.

## Salidas procesadas (referencia)

- `data/processed/train_data.csv` (train features)
- `data/processed/valid_data.csv` (validation features)
- `data/processed/test_data.parquet` (test features)
