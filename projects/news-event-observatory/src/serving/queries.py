from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

TABLES = [
    "articles",
    "scored_articles",
    "events",
    "article_event_links",
    "review_queue",
    "pipeline_runs",
]


class EventStore:
    def __init__(self, database_path: Path | str, *, max_limit: int = 100) -> None:
        self.database_path = Path(database_path)
        self.max_limit = max_limit

    def health(self) -> dict[str, Any]:
        self._ensure_database_exists()
        return {
            "database_path": str(self.database_path),
            "table_counts": self.table_counts(),
        }

    def table_counts(self) -> dict[str, int]:
        with self._connect() as connection:
            return {
                table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
                for table in TABLES
            }

    def list_events(self, *, limit: int = 10, status: str | None = None, min_articles: int | None = None) -> list[dict[str, Any]]:
        safe_limit = self._normalize_limit(limit)
        clauses: list[str] = []
        params: list[Any] = []
        if status:
            clauses.append("status = ?")
            params.append(status)
        if min_articles is not None:
            clauses.append("article_count >= ?")
            params.append(min_articles)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = (
            "SELECT event_id, event_number, event_title, first_date, last_date, "
            "article_count, media_count, query_count, confidence, status, example_url "
            "FROM events "
            f"{where} "
            "ORDER BY article_count DESC, confidence DESC, event_number ASC "
            "LIMIT ?"
        )
        params.append(safe_limit)
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, params).fetchall()]

    def get_event(self, event_id: str) -> dict[str, Any] | None:
        query = (
            "SELECT event_id, event_number, event_title, first_date, last_date, "
            "article_count, media_count, query_count, confidence, status, example_url "
            "FROM events WHERE event_id = ?"
        )
        with self._connect() as connection:
            row = connection.execute(query, [event_id]).fetchone()
            return dict(row) if row else None

    def get_event_articles(self, event_id: str) -> list[dict[str, Any]]:
        query = (
            "SELECT event_id, article_id, link_confidence, title, media, published_at, url "
            "FROM article_event_links WHERE event_id = ? "
            "ORDER BY link_confidence DESC, published_at ASC, article_id ASC"
        )
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, [event_id]).fetchall()]

    def review_queue(self, *, limit: int = 25) -> list[dict[str, Any]]:
        safe_limit = self._normalize_limit(limit)
        query = (
            "SELECT event_id, event_title, article_count, media_count, confidence, "
            "review_reason, review_threshold, example_url "
            "FROM review_queue "
            "ORDER BY article_count ASC, confidence ASC, event_id ASC "
            "LIMIT ?"
        )
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, [safe_limit]).fetchall()]

    def search_articles(self, text: str, *, limit: int = 10) -> list[dict[str, Any]]:
        safe_limit = self._normalize_limit(limit)
        term = f"%{text.strip()}%"
        if term == "%%":
            return []
        query = (
            "SELECT s.article_id, s.title, s.media, s.published_at, s.url, "
            "l.event_id, e.event_title, s.relevance_score "
            "FROM scored_articles AS s "
            "LEFT JOIN article_event_links AS l ON s.article_id = l.article_id "
            "LEFT JOIN events AS e ON l.event_id = e.event_id "
            "WHERE s.title LIKE ? OR s.description LIKE ? OR s.raw_text LIKE ? "
            "ORDER BY COALESCE(s.relevance_score, 0) DESC, s.published_at DESC, s.article_id ASC "
            "LIMIT ?"
        )
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, [term, term, term, safe_limit]).fetchall()]

    def event_status_summary(self) -> list[dict[str, Any]]:
        query = (
            "SELECT status, COUNT(*) AS event_count, SUM(article_count) AS article_count, "
            "AVG(confidence) AS avg_confidence "
            "FROM events GROUP BY status ORDER BY event_count DESC, status ASC"
        )
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query).fetchall()]

    def media_coverage(self, *, limit: int = 10) -> list[dict[str, Any]]:
        safe_limit = self._normalize_limit(limit)
        query = (
            "SELECT media, COUNT(DISTINCT article_id) AS article_count, COUNT(DISTINCT event_id) AS event_count "
            "FROM article_event_links "
            "GROUP BY media "
            "ORDER BY article_count DESC, event_count DESC, media ASC "
            "LIMIT ?"
        )
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(query, [safe_limit]).fetchall()]

    def _connect(self) -> sqlite3.Connection:
        self._ensure_database_exists()
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_database_exists(self) -> None:
        if not self.database_path.exists():
            raise FileNotFoundError(f"Database does not exist: {self.database_path}")

    def _normalize_limit(self, limit: int) -> int:
        if limit < 1:
            raise ValueError("limit must be greater than zero")
        return min(limit, self.max_limit)
