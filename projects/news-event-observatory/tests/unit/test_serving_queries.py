from __future__ import annotations

import pytest

from src.serving.queries import EventStore


def test_store_rejects_zero_limit() -> None:
    store = EventStore("data/processed/events.db")
    with pytest.raises(ValueError, match="limit"):
        store.list_events(limit=0)


def test_store_caps_large_limits() -> None:
    store = EventStore("data/processed/events.db", max_limit=2)
    events = store.list_events(limit=999)
    assert len(events) <= 2
