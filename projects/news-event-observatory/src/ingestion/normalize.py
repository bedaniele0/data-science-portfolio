from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from urllib.parse import parse_qs, unquote, urlparse

import pandas as pd

from src.ingestion.schema import NORMALIZED_COLUMNS

_PLACEHOLDER_VALUES = {"text_title", "text_description", "text_date", "text_media", "text_link"}


def _clean_text(value: object) -> str:
    text = "" if value is None else str(value)
    text = text.replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def _normalize_url(value: object) -> str:
    text = _clean_text(value)
    return text if text.startswith(("http://", "https://")) else ""


def _extract_query(search_url: object) -> str:
    text = _clean_text(search_url)
    if not text.startswith(("http://", "https://")):
        return ""
    parsed = urlparse(text)
    query_values = parse_qs(parsed.query).get("q", [])
    return unquote(query_values[0]).strip() if query_values else ""


def _content_hash(title: str, media: str, published_at: str, url: str) -> str:
    basis = f"{title.lower()}|{media.lower()}|{published_at}|{url.lower()}"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def normalize_articles(
    df: pd.DataFrame,
    *,
    source_name: str,
    drop_placeholder_rows: bool = True,
    drop_empty_title: bool = True,
    deduplicate_by: tuple[str, ...] = ("url", "title", "media"),
    ingested_at: datetime | None = None,
) -> pd.DataFrame:
    ingested = (ingested_at or datetime.now(UTC)).replace(microsecond=0).isoformat()
    work = df.copy()

    for col in ["search_URL", "title", "description", "date", "media", "link"]:
        if col not in work.columns:
            work[col] = ""
        work[col] = work[col].map(_clean_text)

    if drop_placeholder_rows:
        mask_placeholder = work[["title", "description", "date", "media", "link"]].isin(_PLACEHOLDER_VALUES).any(axis=1)
        work = work.loc[~mask_placeholder].copy()

    work["title"] = work["title"].map(_clean_text)
    work["description"] = work["description"].map(_clean_text)
    work["media"] = work["media"].map(_clean_text)
    work["url"] = work["link"].map(_normalize_url)
    work["published_at"] = pd.to_datetime(work["date"], errors="coerce").dt.date.astype("string").fillna("")
    work["query"] = work["search_URL"].map(_extract_query)
    work["source"] = source_name
    work["raw_text"] = (work["title"] + " " + work["description"]).str.strip()

    if drop_empty_title:
        work = work.loc[work["title"].str.len() > 0].copy()

    work["content_hash"] = [
        _content_hash(title, media, published_at, url)
        for title, media, published_at, url in zip(work["title"], work["media"], work["published_at"], work["url"], strict=False)
    ]
    work["article_id"] = [
        hashlib.sha256((url or content_hash).encode("utf-8")).hexdigest()[:16]
        for url, content_hash in zip(work["url"], work["content_hash"], strict=False)
    ]
    work["ingested_at"] = ingested

    dedupe_cols = [col for col in deduplicate_by if col in work.columns]
    if dedupe_cols:
        work = work.drop_duplicates(subset=dedupe_cols, keep="first")

    return work[NORMALIZED_COLUMNS].reset_index(drop=True)
