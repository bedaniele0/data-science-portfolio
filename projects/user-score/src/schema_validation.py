import pandas as pd


def _dtype_ok(series, expected):
    if expected == 'string':
        return pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)
    if expected == 'float':
        return pd.api.types.is_float_dtype(series) or pd.api.types.is_numeric_dtype(series)
    if expected == 'int':
        return pd.api.types.is_integer_dtype(series)
    return True


def validate_df(df, schema, section):
    errors = []
    spec = schema.get(section, {})
    required = spec.get('required', [])
    dtypes = spec.get('dtypes', {})

    for col in required:
        if col not in df.columns:
            errors.append(f"missing_column:{col}")

    for col, expected in dtypes.items():
        if col in df.columns and not _dtype_ok(df[col], expected):
            errors.append(f"dtype_mismatch:{col}:{expected}")

    return errors
