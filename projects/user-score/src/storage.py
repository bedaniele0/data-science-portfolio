import os
from pathlib import Path

import yaml


def load_config(path):
    return yaml.safe_load(Path(path).read_text())


def resolve_path(config, key):
    mode = os.getenv('STORAGE_MODE', 's3')
    if mode == 'local':
        return config['paths_local'][key]
    return config['paths'][key]


def is_s3(path):
    return str(path).startswith('s3://')


def ensure_local_parent(path):
    if is_s3(path):
        return
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def open_binary(path, mode):
    if is_s3(path):
        import fsspec
        return fsspec.open(path, mode)
    return open(path, mode)


def joblib_dump(payload, path):
    import joblib

    with open_binary(path, 'wb') as f:
        joblib.dump(payload, f)


def joblib_load(path):
    import joblib

    with open_binary(path, 'rb') as f:
        return joblib.load(f)
