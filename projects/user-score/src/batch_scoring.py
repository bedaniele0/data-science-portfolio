from pathlib import Path
import json

import pandas as pd
import yaml

from feature_pipeline import compute_features, ensure_id, row_hash
from schema_validation import validate_df
from storage import ensure_local_parent, joblib_load, load_config, resolve_path


def main():
    config = load_config('configs/config.yaml')
    model_path = resolve_path(config, 'model_artifact')
    input_path = resolve_path(config, 'prod_input')
    output_path = resolve_path(config, 'prod_predictions')

    payload = joblib_load(model_path)
    model = payload['model']
    vocab = payload['vocab']
    feature_cols = payload['feature_cols']

    df = pd.read_csv(input_path)
    df = ensure_id(df)
    schema = yaml.safe_load(Path('configs/schema.yaml').read_text())
    errors = validate_df(df, schema, 'input')
    if errors:
        raise ValueError(f"Input schema invalid: {errors}")

    df_feat = compute_features(df, vocab)
    X = df_feat[feature_cols]

    preds = model.predict(X)

    pred_df = pd.DataFrame({
        'id': df_feat['id'].astype(str),
        'prediction_date': pd.Timestamp.utcnow().strftime('%Y-%m-%d'),
        'predicted_user_score': preds,
        'model_version': config['project']['model_version'],
    })

    pred_df['features_hash'] = df_feat[feature_cols].apply(row_hash, axis=1)

    ensure_local_parent(output_path)
    pred_df.to_csv(output_path, index=False)

    print(json.dumps({'rows_scored': len(pred_df), 'output': str(output_path)}))


if __name__ == '__main__':
    main()
