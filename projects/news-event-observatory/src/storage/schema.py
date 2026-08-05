from __future__ import annotations

from sqlalchemy import Boolean, Column, Float, Integer, MetaData, String, Table, Text

metadata = MetaData()

articles = Table(
    "articles",
    metadata,
    Column("article_id", String),
    Column("source", String),
    Column("query", String),
    Column("title", Text),
    Column("description", Text),
    Column("published_at", String),
    Column("media", String),
    Column("url", Text),
    Column("raw_text", Text),
    Column("content_hash", String),
    Column("ingested_at", String),
)

scored_articles = Table(
    "scored_articles",
    metadata,
    Column("article_id", String),
    Column("source", String),
    Column("query", String),
    Column("title", Text),
    Column("description", Text),
    Column("published_at", String),
    Column("media", String),
    Column("url", Text),
    Column("raw_text", Text),
    Column("content_hash", String),
    Column("ingested_at", String),
    Column("is_relevant", Boolean),
    Column("relevance_score", Float),
    Column("matched_event_terms", String),
    Column("matched_actor_terms", String),
    Column("has_event_terms", Boolean),
    Column("has_actor_terms", Boolean),
)

events = Table(
    "events",
    metadata,
    Column("event_id", String),
    Column("event_number", Integer),
    Column("event_title", Text),
    Column("first_date", String),
    Column("last_date", String),
    Column("article_count", Integer),
    Column("media_count", Integer),
    Column("query_count", Integer),
    Column("confidence", Float),
    Column("status", String),
    Column("example_article_id", String),
    Column("example_url", Text),
)

article_event_links = Table(
    "article_event_links",
    metadata,
    Column("event_id", String),
    Column("article_id", String),
    Column("link_confidence", Float),
    Column("title", Text),
    Column("media", String),
    Column("published_at", String),
    Column("url", Text),
)

review_queue = Table(
    "review_queue",
    metadata,
    Column("event_id", String),
    Column("event_title", Text),
    Column("article_count", Integer),
    Column("media_count", Integer),
    Column("confidence", Float),
    Column("review_reason", String),
    Column("review_threshold", Float),
    Column("example_url", Text),
)

pipeline_runs = Table(
    "pipeline_runs",
    metadata,
    Column("run_id", String),
    Column("run_started_at", String),
    Column("source", String),
    Column("articles_rows", Integer),
    Column("scored_articles_rows", Integer),
    Column("events_rows", Integer),
    Column("article_event_links_rows", Integer),
    Column("review_queue_rows", Integer),
)
