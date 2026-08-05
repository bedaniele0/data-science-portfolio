from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    database_path: str
    table_counts: dict[str, int]


class EventSummary(BaseModel):
    event_id: str
    event_number: int
    event_title: str
    first_date: str
    last_date: str
    article_count: int
    media_count: int
    query_count: int
    confidence: float
    status: str
    example_url: str


class ArticleLink(BaseModel):
    event_id: str
    article_id: str
    link_confidence: float
    title: str
    media: str
    published_at: str
    url: str


class ReviewQueueItem(BaseModel):
    event_id: str
    event_title: str
    article_count: int
    media_count: int
    confidence: float
    review_reason: str
    review_threshold: float
    example_url: str


class SearchResult(BaseModel):
    article_id: str
    title: str
    media: str
    published_at: str
    url: str
    event_id: str | None = None
    event_title: str | None = None
    relevance_score: float | None = None


class EventsResponse(BaseModel):
    total: int
    limit: int = Field(ge=1)
    items: list[EventSummary]
