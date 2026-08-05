from __future__ import annotations

from dataclasses import dataclass

RAW_COLUMN_ALIASES = {
    "uuid": "UUID",
    "search_url": "search_URL",
    "title": "title",
    "description": "description",
    "date": "date",
    "media": "media",
    "url": "link",
}

NORMALIZED_COLUMNS = [
    "article_id",
    "source",
    "query",
    "title",
    "description",
    "published_at",
    "media",
    "url",
    "raw_text",
    "content_hash",
    "ingested_at",
]

REQUIRED_RAW_COLUMNS = ["title", "date", "media", "link"]


@dataclass(frozen=True)
class IngestionConfig:
    input_path: str
    source_name: str
    output_path: str
    report_path: str
    drop_placeholder_rows: bool = True
    drop_empty_title: bool = True
    deduplicate_by: tuple[str, ...] = ("url", "title", "media")
