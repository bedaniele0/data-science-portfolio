from __future__ import annotations

from pathlib import Path

from sqlalchemy import Engine, create_engine, text

from src.storage.schema import metadata


def sqlite_url(path: Path | str) -> str:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{db_path}"


def get_engine(path: Path | str) -> Engine:
    return create_engine(sqlite_url(path), future=True)


def initialize_database(engine: Engine) -> None:
    metadata.create_all(engine)


def table_counts(engine: Engine, table_names: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    with engine.connect() as connection:
        for table_name in table_names:
            counts[table_name] = int(connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())
    return counts
