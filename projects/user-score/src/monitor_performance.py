from pathlib import Path

import pandas as pd
import yaml
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from storage import ensure_local_parent, load_config, resolve_path


def main():
    config = load_config('configs/config.yaml')
    pred_path = resolve_path(config, 'prod_predictions')
    actuals_path = resolve_path(config, 'prod_actuals')
    output_path = resolve_path(config, 'metrics_output')

    preds = pd.read_csv(pred_path)
    actuals = pd.read_csv(actuals_path)

    preds['join_date'] = preds['prediction_date'] if 'prediction_date' in preds.columns else None
    if 'date_window' in actuals.columns:
        actuals['join_date'] = actuals['date_window']
    elif 'event_date' in actuals.columns:
        actuals['join_date'] = actuals['event_date']
    else:
        actuals['join_date'] = None

    join_cols = ['id']
    if preds['join_date'].notna().any() and actuals['join_date'].notna().any():
        join_cols.append('join_date')

    total_preds = len(preds)
    merged = preds.merge(actuals, on=join_cols, how='inner')
    matched_on_date = len(merged)
    if merged.empty and join_cols != ['id']:
        # Fallback to id-only join for delayed labels.
        merged = preds.merge(actuals, on=['id'], how='inner')
    matched_on_id = len(merged) if join_cols != ['id'] else len(merged)
    if merged.empty:
        raise ValueError('No matching records between predictions and actuals')

    merged = merged[merged['real_user_score'].notna()].copy()
    if merged.empty:
        raise ValueError('No valid labels after filtering NaNs')

    y_true = merged['real_user_score']
    y_pred = merged['predicted_user_score']

    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    r2 = r2_score(y_true, y_pred)

    metrics = [
        {'metric': 'mae', 'value': mae, 'rows_evaluated': len(merged)},
        {'metric': 'rmse', 'value': rmse, 'rows_evaluated': len(merged)},
        {'metric': 'r2', 'value': r2, 'rows_evaluated': len(merged)},
        {'metric': 'match_rate_date', 'value': matched_on_date / max(total_preds, 1), 'rows_evaluated': total_preds},
        {'metric': 'match_rate_id', 'value': matched_on_id / max(total_preds, 1), 'rows_evaluated': total_preds},
        {'metric': 'match_rate_missing', 'value': 1 - (matched_on_id / max(total_preds, 1)), 'rows_evaluated': total_preds},
    ]
    ensure_local_parent(output_path)
    pd.DataFrame(metrics).to_csv(output_path, index=False)

    print(f'Wrote performance metrics to {output_path}')


if __name__ == '__main__':
    main()
