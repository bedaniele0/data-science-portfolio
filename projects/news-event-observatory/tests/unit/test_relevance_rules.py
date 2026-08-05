import pandas as pd

from src.models.relevance_rules import RelevanceRules, apply_relevance_rules, score_text

RULES = RelevanceRules(
    event_terms=[{"name": "homicidio", "patterns": [r"\basesin\w*"]}],
    actor_terms=[{"name": "negocio", "patterns": [r"\bcomerciant\w*"]}],
    scoring={"score_if_relevant": 1.0, "score_if_event_only": 0.45, "score_if_actor_only": 0.35},
)


def test_score_text_marks_relevant_only_when_event_and_actor_match():
    scored = score_text("Asesinan a comerciante en mercado", RULES)

    assert scored["is_relevant"] is True
    assert scored["relevance_score"] == 1.0
    assert scored["matched_event_terms"] == "homicidio"
    assert scored["matched_actor_terms"] == "negocio"


def test_score_text_keeps_event_only_as_not_relevant():
    scored = score_text("Asesinan a una persona en carretera", RULES)

    assert scored["is_relevant"] is False
    assert scored["relevance_score"] == 0.45


def test_apply_relevance_rules_adds_expected_columns():
    articles = pd.DataFrame(
        [{"title": "Asesinan a comerciante", "description": "", "article_id": "a1"}]
    )

    scored = apply_relevance_rules(articles, RULES)

    assert scored.loc[0, "is_relevant"]
    assert "matched_event_terms" in scored.columns
