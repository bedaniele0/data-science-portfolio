from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from typing import Any

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SPANISH_STOP_WORDS = {
    "a", "al", "ante", "bajo", "con", "contra", "de", "del", "desde", "durante", "e", "el", "en",
    "entre", "es", "esa", "ese", "esta", "este", "la", "las", "lo", "los", "mas", "más", "no", "o",
    "para", "pero", "por", "que", "se", "sin", "sobre", "su", "sus", "un", "una", "unas", "unos", "y",
}


@dataclass(frozen=True)
class ClusteringConfig:
    similarity_threshold: float = 0.32
    review_confidence_threshold: float = 0.55
    max_days_between_articles: int = 3
    text_fields: tuple[str, ...] = ("title", "description")
    date_field: str = "published_at"
    article_id_field: str = "article_id"
    min_df: int = 1
    ngram_range: tuple[int, int] = (1, 2)


def normalize_cluster_text(text: object) -> str:
    value = "" if text is None else str(text)
    value = unicodedata.normalize("NFKC", value).lower()
    value = re.sub(r"[^\w\sáéíóúñü]", " ", value, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", value).strip()


def cluster_articles(articles: pd.DataFrame, config: ClusteringConfig) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if articles.empty:
        return _empty_events(), _empty_links(), _empty_review_queue()

    missing = [field for field in (*config.text_fields, config.date_field, config.article_id_field) if field not in articles.columns]
    if missing:
        raise ValueError(f"Missing columns for clustering: {missing}")

    work = articles.copy().reset_index(drop=True)
    work["_published_date"] = pd.to_datetime(work[config.date_field], errors="coerce").dt.date
    work["_text"] = work[list(config.text_fields)].fillna("").astype(str).agg(" ".join, axis=1).map(normalize_cluster_text)
    work = work.sort_values(["_published_date", "title", config.article_id_field], na_position="last").reset_index(drop=True)

    similarity = _text_similarity(work["_text"].tolist(), config)
    clusters: list[list[int]] = []

    for row_idx in range(len(work)):
        best_cluster_idx: int | None = None
        best_score = -1.0
        for cluster_idx, member_indices in enumerate(clusters):
            if not _within_date_window(work, row_idx, member_indices, config.max_days_between_articles):
                continue
            score = float(max(similarity[row_idx, member_idx] for member_idx in member_indices))
            if score > best_score:
                best_score = score
                best_cluster_idx = cluster_idx

        if best_cluster_idx is not None and best_score >= config.similarity_threshold:
            clusters[best_cluster_idx].append(row_idx)
        else:
            clusters.append([row_idx])

    events = _build_events(work, clusters, similarity, config)
    links = _build_links(work, clusters, similarity, events)
    review_queue = _build_review_queue(events, config)
    return events, links, review_queue


def _text_similarity(texts: list[str], config: ClusteringConfig) -> np.ndarray:
    if len(texts) == 1:
        return np.ones((1, 1))
    vectorizer = TfidfVectorizer(
        strip_accents="unicode",
        lowercase=True,
        stop_words=list(SPANISH_STOP_WORDS),
        min_df=config.min_df,
        ngram_range=config.ngram_range,
    )
    matrix = vectorizer.fit_transform(texts)
    return cosine_similarity(matrix)


def _within_date_window(work: pd.DataFrame, row_idx: int, member_indices: list[int], max_days: int) -> bool:
    current = work.loc[row_idx, "_published_date"]
    if not isinstance(current, date):
        return True
    for member_idx in member_indices:
        other = work.loc[member_idx, "_published_date"]
        if not isinstance(other, date):
            continue
        if abs((current - other).days) <= max_days:
            return True
    return False


def _event_id(member_article_ids: list[str]) -> str:
    basis = "|".join(sorted(member_article_ids))
    return "evt_" + hashlib.sha256(basis.encode("utf-8")).hexdigest()[:12]


def _cluster_confidence(member_indices: list[int], similarity: np.ndarray) -> float:
    if len(member_indices) == 1:
        return 0.0
    scores = []
    for pos, idx_a in enumerate(member_indices):
        for idx_b in member_indices[pos + 1 :]:
            scores.append(float(similarity[idx_a, idx_b]))
    return float(np.mean(scores)) if scores else 0.0


def _build_events(work: pd.DataFrame, clusters: list[list[int]], similarity: np.ndarray, config: ClusteringConfig) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for cluster_number, member_indices in enumerate(clusters, start=1):
        members = work.loc[member_indices].copy()
        article_ids = members[config.article_id_field].astype(str).tolist()
        first_date = members["_published_date"].dropna().min()
        last_date = members["_published_date"].dropna().max()
        confidence = _cluster_confidence(member_indices, similarity)
        example = members.iloc[0]
        rows.append(
            {
                "event_id": _event_id(article_ids),
                "event_number": cluster_number,
                "event_title": example.get("title", ""),
                "first_date": str(first_date) if pd.notna(first_date) else "",
                "last_date": str(last_date) if pd.notna(last_date) else "",
                "article_count": len(members),
                "media_count": int(members["media"].nunique()) if "media" in members.columns else 0,
                "query_count": int(members["query"].nunique()) if "query" in members.columns else 0,
                "confidence": confidence,
                "status": "needs_review" if len(members) == 1 or confidence < config.review_confidence_threshold else "auto",
                "example_article_id": str(example.get(config.article_id_field, "")),
                "example_url": str(example.get("url", "")),
            }
        )
    return pd.DataFrame(rows).sort_values(["first_date", "event_number"]).reset_index(drop=True)


def _build_links(work: pd.DataFrame, clusters: list[list[int]], similarity: np.ndarray, events: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for cluster_idx, member_indices in enumerate(clusters):
        event_id = str(events.iloc[cluster_idx]["event_id"])
        for member_idx in member_indices:
            member_scores = [float(similarity[member_idx, other]) for other in member_indices if other != member_idx]
            rows.append(
                {
                    "event_id": event_id,
                    "article_id": str(work.loc[member_idx, "article_id"]),
                    "link_confidence": float(max(member_scores)) if member_scores else 0.0,
                    "title": str(work.loc[member_idx, "title"]),
                    "media": str(work.loc[member_idx, "media"]),
                    "published_at": str(work.loc[member_idx, "published_at"]),
                    "url": str(work.loc[member_idx, "url"]),
                }
            )
    return pd.DataFrame(rows)


def _build_review_queue(events: pd.DataFrame, config: ClusteringConfig) -> pd.DataFrame:
    if events.empty:
        return _empty_review_queue()
    review = events.loc[events["status"] == "needs_review"].copy()
    if review.empty:
        return _empty_review_queue()
    review["review_reason"] = np.where(
        review["article_count"] == 1,
        "single_article_event",
        "low_cluster_confidence",
    )
    review["review_threshold"] = config.review_confidence_threshold
    return review[
        [
            "event_id",
            "event_title",
            "article_count",
            "media_count",
            "confidence",
            "review_reason",
            "review_threshold",
            "example_url",
        ]
    ].reset_index(drop=True)


def _empty_events() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "event_id", "event_number", "event_title", "first_date", "last_date", "article_count", "media_count",
            "query_count", "confidence", "status", "example_article_id", "example_url",
        ]
    )


def _empty_links() -> pd.DataFrame:
    return pd.DataFrame(columns=["event_id", "article_id", "link_confidence", "title", "media", "published_at", "url"])


def _empty_review_queue() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "event_id", "event_title", "article_count", "media_count", "confidence", "review_reason",
            "review_threshold", "example_url",
        ]
    )
