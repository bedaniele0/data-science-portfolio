from datetime import UTC, datetime

import pandas as pd

from src.ingestion.normalize import normalize_articles


def test_normalize_articles_drops_placeholder_and_extracts_query():
    raw = pd.DataFrame(
        [
            {
                "UUID": "1",
                "search_URL": "https://www.google.com/search?q=asesinan&tbm=nws",
                "title": "text_title",
                "description": "text_description",
                "date": "text_date",
                "media": "text_media",
                "link": "text_link",
            },
            {
                "UUID": "2",
                "search_URL": "https://www.google.com/search?q=asesinan&tbm=nws",
                "title": " Asesinan a comerciante en mercado ",
                "description": " Nota de prueba ",
                "date": "2026-02-16",
                "media": "Medio Local",
                "link": "https://example.com/nota",
            },
        ]
    )

    normalized = normalize_articles(
        raw,
        source_name="test",
        ingested_at=datetime(2026, 8, 4, tzinfo=UTC),
    )

    assert len(normalized) == 1
    row = normalized.iloc[0]
    assert row["query"] == "asesinan"
    assert row["title"] == "Asesinan a comerciante en mercado"
    assert row["published_at"] == "2026-02-16"
    assert row["url"] == "https://example.com/nota"
    assert row["article_id"]


def test_normalize_articles_deduplicates_by_url_title_media():
    raw = pd.DataFrame(
        [
            {
                "search_URL": "https://www.google.com/search?q=test",
                "title": "Titulo",
                "description": "Uno",
                "date": "2026-02-16",
                "media": "Medio",
                "link": "https://example.com/a",
            },
            {
                "search_URL": "https://www.google.com/search?q=test",
                "title": "Titulo",
                "description": "Dos",
                "date": "2026-02-16",
                "media": "Medio",
                "link": "https://example.com/a",
            },
        ]
    )

    normalized = normalize_articles(raw, source_name="test")

    assert len(normalized) == 1
