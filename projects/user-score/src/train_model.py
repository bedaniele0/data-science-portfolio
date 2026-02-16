import json
from pathlib import Path

import pandas as pd
import yaml
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from feature_pipeline import compute_features, build_genre_vocab, parse_genres, save_vocab
from schema_validation import validate_df
from storage import ensure_local_parent, joblib_dump, load_config, resolve_path


def main():
    config = load_config('configs/config.yaml')
    train_path = resolve_path(config, 'train_data')
    model_path = resolve_path(config, 'model_artifact')
    Path('reports/prod').mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(train_path)
    schema = yaml.safe_load(Path('configs/schema.yaml').read_text())
    errors = validate_df(df, schema, 'training')
    if errors:
        raise ValueError(f"Training schema invalid: {errors}")
    target = 'user_score'
    df = df[df[target].notna()].copy()

    # Build vocab from training data using robust parser
    df_temp = df.copy()
    df_temp['genres_list'] = df_temp['genres'].apply(parse_genres)
    vocab, counts = build_genre_vocab(df_temp)

    save_vocab(vocab, 'models/genres_vocab.json')

    df_feat = compute_features(df, vocab)

    num_features = ['meta_score', 'date_year', 'date_month']
    cat_features = ['platform', 'esrb_rating']
    genre_features = [f'genre_{g}' for g in vocab]
    feature_cols = num_features + cat_features + genre_features

    X = df_feat[feature_cols]
    y = df_feat[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median'))
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_features),
            ('cat', categorical_transformer, cat_features),
            ('genre', 'passthrough', genre_features)
        ],
        sparse_threshold=0.0
    )

    models = {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=200, random_state=42),
        'GradientBoosting': GradientBoostingRegressor(random_state=42)
    }

    results = []
    best_model = None
    best_r2 = -1.0
    best_name = None

    for name, model in models.items():
        pipe = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        model = pipe

        mae = mean_absolute_error(y_test, preds)
        rmse = mean_squared_error(y_test, preds) ** 0.5
        r2 = r2_score(y_test, preds)
        results.append({'model': name, 'mae': mae, 'rmse': rmse, 'r2': r2})

        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_name = name

    results_df = pd.DataFrame(results).sort_values(by='r2', ascending=False)
    Path('reports/prod').mkdir(parents=True, exist_ok=True)
    results_df.to_csv('reports/prod/train_metrics.csv', index=False)

    payload = {
        'model': best_model,
        'model_name': best_name,
        'vocab': vocab,
        'feature_cols': feature_cols,
    }

    ensure_local_parent(model_path)
    joblib_dump(payload, model_path)

    Path('reports/prod/train_summary.json').write_text(
        json.dumps({'best_model': best_name, 'best_r2': best_r2}, indent=2)
    )


if __name__ == '__main__':
    main()
