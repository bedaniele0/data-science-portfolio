import ast
import hashlib
import json
from pathlib import Path

import pandas as pd

DEFAULT_GENRE_TOP_N = 20


def parse_genres(val):
    if pd.isna(val):
        return []
    if isinstance(val, list):
        return val
    s = str(val).strip()
    try:
        parsed = ast.literal_eval(s)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed]
    except Exception:
        pass
    s = s.strip('[]')
    parts = [p.strip().strip("'").strip('"') for p in s.split(',') if p.strip()]
    return parts


def add_date_features(df):
    parsed = pd.to_datetime(df['date'], errors='coerce')
    df['date_year'] = parsed.dt.year
    df['date_month'] = parsed.dt.month
    return df


def build_genre_vocab(df, top_n=DEFAULT_GENRE_TOP_N):
    all_genres = pd.Series([g for lst in df['genres_list'] for g in lst])
    counts = all_genres.value_counts()
    vocab = counts.head(top_n).index.tolist()
    return vocab, counts


def apply_genre_multihot(df, vocab):
    for g in vocab:
        df[f'genre_{g}'] = df['genres_list'].apply(lambda lst: 1 if g in lst else 0)
    return df


def compute_features(df, vocab):
    df = df.copy()
    df['genres_list'] = df['genres'].apply(parse_genres)
    df = add_date_features(df)
    df = apply_genre_multihot(df, vocab)
    return df


def row_hash(row):
    payload = '|'.join([str(x) for x in row.values])
    return hashlib.md5(payload.encode('utf-8')).hexdigest()


def ensure_id(df):
    df = df.copy()
    if 'id' not in df.columns:
        df['id'] = df.index.astype(str)
    else:
        df['id'] = df['id'].astype(str)
    return df


def save_vocab(vocab, path):
    Path(path).write_text(json.dumps(vocab, indent=2))


def load_vocab(path):
    return json.loads(Path(path).read_text())
