import argparse
from pathlib import Path

import pandas as pd
import yaml

from schema_validation import validate_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    parser.add_argument('--schema', required=True)
    parser.add_argument('--section', required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.path)
    schema = yaml.safe_load(Path(args.schema).read_text())

    errors = validate_df(df, schema, args.section)
    if errors:
        raise SystemExit(f"Schema validation failed: {', '.join(errors)}")

    print(f"Schema validation OK for {args.section}")


if __name__ == '__main__':
    main()
