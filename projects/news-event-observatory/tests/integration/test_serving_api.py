from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from src.pipelines.build_master_pipeline import run as run_master
from src.pipelines.clustering_pipeline import run as run_clustering
from src.pipelines.ingest_pipeline import run as run_ingest
from src.pipelines.relevance_pipeline import run as run_relevance
from src.serving.api import create_app


@pytest.mark.anyio
async def test_serving_api_contract() -> None:
    run_ingest("configs/ingestion.yaml")
    run_relevance("configs/relevance.yaml")
    run_clustering("configs/clustering.yaml")
    run_master("configs/storage.yaml")

    transport = ASGITransport(app=create_app("configs/serving.yaml"))
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        health = await client.get("/health")
        assert health.status_code == 200
        assert health.json()["table_counts"]["articles"] == 668

        events = await client.get("/events", params={"limit": 3})
        assert events.status_code == 200
        items = events.json()["items"]
        assert len(items) == 3

        event_id = items[0]["event_id"]
        detail = await client.get(f"/events/{event_id}")
        assert detail.status_code == 200
        assert detail.json()["event_id"] == event_id

        articles = await client.get(f"/events/{event_id}/articles")
        assert articles.status_code == 200
        assert len(articles.json()) > 0

        search = await client.get("/search", params={"q": "asesinado", "limit": 5})
        assert search.status_code == 200
        assert len(search.json()) > 0
