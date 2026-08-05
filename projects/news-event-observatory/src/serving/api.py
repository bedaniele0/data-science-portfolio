from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from fastapi import Depends, FastAPI, HTTPException, Query

from src.serving.queries import EventStore
from src.serving.schemas import ArticleLink, EventsResponse, EventSummary, HealthResponse, ReviewQueueItem, SearchResult

ROOT = Path(__file__).resolve().parents[2]


def _resolve(path: str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else ROOT / candidate


def load_store(config_path: Path | str = "configs/serving.yaml") -> EventStore:
    config_file = _resolve(str(config_path))
    config = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    defaults = config.get("query_defaults", {})
    return EventStore(_resolve(config["input"]["database_path"]), max_limit=int(defaults.get("max_limit", 100)))


def create_app(config_path: Path | str = "configs/serving.yaml") -> FastAPI:
    app = FastAPI(title="News Event Observatory API", version="0.1.0")
    store = load_store(config_path)

    def get_store() -> EventStore:
        return store

    @app.get("/health", response_model=HealthResponse)
    def health(event_store: EventStore = Depends(get_store)) -> dict[str, Any]:
        payload = event_store.health()
        return {"status": "ok", **payload}

    @app.get("/events", response_model=EventsResponse)
    def list_events(
        limit: int = Query(default=10, ge=1),
        status: str | None = None,
        min_articles: int | None = Query(default=None, ge=1),
        event_store: EventStore = Depends(get_store),
    ) -> dict[str, Any]:
        items = event_store.list_events(limit=limit, status=status, min_articles=min_articles)
        return {"total": len(items), "limit": limit, "items": items}

    @app.get("/events/{event_id}", response_model=EventSummary)
    def get_event(event_id: str, event_store: EventStore = Depends(get_store)) -> dict[str, Any]:
        event = event_store.get_event(event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="event not found")
        return event

    @app.get("/events/{event_id}/articles", response_model=list[ArticleLink])
    def get_event_articles(event_id: str, event_store: EventStore = Depends(get_store)) -> list[dict[str, Any]]:
        if event_store.get_event(event_id) is None:
            raise HTTPException(status_code=404, detail="event not found")
        return event_store.get_event_articles(event_id)

    @app.get("/review-queue", response_model=list[ReviewQueueItem])
    def review_queue(limit: int = Query(default=25, ge=1), event_store: EventStore = Depends(get_store)) -> list[dict[str, Any]]:
        return event_store.review_queue(limit=limit)

    @app.get("/search", response_model=list[SearchResult])
    def search(q: str = Query(min_length=1), limit: int = Query(default=10, ge=1), event_store: EventStore = Depends(get_store)) -> list[dict[str, Any]]:
        return event_store.search_articles(q, limit=limit)

    return app


app = create_app()
