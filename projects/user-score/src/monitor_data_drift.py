from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from feature_pipeline import compute_features, load_vocab
from storage import ensure_local_parent, load_config, resolve_path


def psi_numeric(expected, actual, bins=10):
    expected = pd.Series(expected).dropna()
    actual = pd.Series(actual).dropna()
    if expected.empty or actual.empty:
        return np.nan
    quantiles = np.linspace(0, 1, bins + 1)
    breakpoints = expected.quantile(quantiles).values
    breakpoints = np.unique(breakpoints)
    if len(breakpoints) < 3:
        return np.nan
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]
    expected_perc = expected_counts / expected_counts.sum()
    actual_perc = actual_counts / actual_counts.sum()
    psi = np.sum((expected_perc - actual_perc) * np.log((expected_perc + 1e-6) / (actual_perc + 1e-6)))
    return float(psi)


def psi_categorical(expected, actual):
    expected = pd.Series(expected).fillna('MISSING')
    actual = pd.Series(actual).fillna('MISSING')
    categories = sorted(set(expected.unique()) | set(actual.unique()))
    exp_counts = expected.value_counts().reindex(categories, fill_value=0).values
    act_counts = actual.value_counts().reindex(categories, fill_value=0).values
    exp_perc = exp_counts / exp_counts.sum() if exp_counts.sum() else np.zeros_like(exp_counts)
    act_perc = act_counts / act_counts.sum() if act_counts.sum() else np.zeros_like(act_counts)
    psi = np.sum((exp_perc - act_perc) * np.log((exp_perc + 1e-6) / (act_perc + 1e-6)))
    return float(psi)


def main():
    config = load_config('configs/config.yaml')
    train_path = resolve_path(config, 'train_data')
    prod_path = resolve_path(config, 'prod_input')
    output_path = resolve_path(config, 'drift_output')

    train_df = pd.read_csv(train_path)
    prod_df = pd.read_csv(prod_path)

    vocab = load_vocab('models/genres_vocab.json')

    train_feat = compute_features(train_df, vocab)
    prod_feat = compute_features(prod_df, vocab)

    numeric_features = ['meta_score', 'date_year', 'date_month']
    genre_features = [f'genre_{g}' for g in vocab]
    cat_features = ['platform', 'esrb_rating']

    rows = []

    for col in numeric_features + genre_features:
        val = psi_numeric(train_feat[col], prod_feat[col])
        rows.append({'feature': col, 'psi': val, 'type': 'numeric'})

    for col in cat_features:
        val = psi_categorical(train_feat[col], prod_feat[col])
        rows.append({'feature': col, 'psi': val, 'type': 'categorical'})

    ensure_local_parent(output_path)
    pd.DataFrame(rows).to_csv(output_path, index=False)

    print(f'Wrote drift report to {output_path}')


if __name__ == '__main__':
    main()
