from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


@dataclass(frozen=True)
class RelevanceRules:
    event_terms: list[dict[str, Any]]
    actor_terms: list[dict[str, Any]]
    scoring: dict[str, Any]

    @classmethod
    def from_yaml(cls, path: Path | str) -> RelevanceRules:
        raw = yaml.safe_load(Path(path).read_text()) or {}
        return cls(
            event_terms=list(raw.get("event_terms", [])),
            actor_terms=list(raw.get("actor_terms", [])),
            scoring=dict(raw.get("scoring", {})),
        )


def normalize_for_matching(text: object) -> str:
    value = "" if text is None else str(text)
    value = unicodedata.normalize("NFKC", value).lower()
    value = value.replace(" ", " ")
    return re.sub(r"\s+", " ", value).strip()


def _matches(text: str, groups: list[dict[str, Any]]) -> list[str]:
    matched: list[str] = []
    for group in groups:
        group_name = str(group.get("name", "unnamed"))
        for pattern in group.get("patterns", []):
            if re.search(str(pattern), text, flags=re.IGNORECASE):
                matched.append(group_name)
                break
    return matched


def score_text(text: object, rules: RelevanceRules) -> dict[str, Any]:
    normalized = normalize_for_matching(text)
    event_matches = _matches(normalized, rules.event_terms)
    actor_matches = _matches(normalized, rules.actor_terms)
    has_event = bool(event_matches)
    has_actor = bool(actor_matches)
    is_relevant = has_event and has_actor

    scoring = rules.scoring
    if is_relevant:
        score = float(scoring.get("score_if_relevant", 1.0))
    elif has_event:
        score = float(scoring.get("score_if_event_only", 0.45))
    elif has_actor:
        score = float(scoring.get("score_if_actor_only", 0.35))
    else:
        score = float(scoring.get("score_if_no_match", 0.0))

    return {
        "is_relevant": is_relevant,
        "relevance_score": score,
        "matched_event_terms": ";".join(event_matches),
        "matched_actor_terms": ";".join(actor_matches),
        "has_event_terms": has_event,
        "has_actor_terms": has_actor,
    }


def apply_relevance_rules(
    articles: pd.DataFrame,
    rules: RelevanceRules,
    *,
    text_fields: tuple[str, ...] = ("title", "description"),
) -> pd.DataFrame:
    missing = [field for field in text_fields if field not in articles.columns]
    if missing:
        raise ValueError(f"Missing text fields: {missing}")

    scored = articles.copy()
    text = scored[list(text_fields)].fillna("").astype(str).agg(" ".join, axis=1)
    scores = pd.DataFrame([score_text(value, rules) for value in text])
    return pd.concat([scored.reset_index(drop=True), scores], axis=1)
