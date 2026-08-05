import pandas as pd

from src.models.event_clustering import ClusteringConfig, cluster_articles


def test_cluster_articles_groups_similar_articles_within_date_window():
    articles = pd.DataFrame(
        [
            {
                "article_id": "a1",
                "title": "Asesinan a arquitecto en Puebla",
                "description": "Sala de Despecho Angelopolis",
                "published_at": "2026-02-17",
                "media": "Medio A",
                "query": "asesinado",
                "url": "https://example.com/a1",
            },
            {
                "article_id": "a2",
                "title": "Madre de arquitecto asesinado rompe silencio",
                "description": "Sala de Despecho en Angelopolis Puebla",
                "published_at": "2026-02-17",
                "media": "Medio B",
                "query": "asesinado",
                "url": "https://example.com/a2",
            },
            {
                "article_id": "a3",
                "title": "Detienen a operador por muerte de motociclista",
                "description": "Cuautitlan Izcalli",
                "published_at": "2026-02-17",
                "media": "Medio C",
                "query": "muerte",
                "url": "https://example.com/a3",
            },
        ]
    )

    events, links, review_queue = cluster_articles(
        articles,
        ClusteringConfig(similarity_threshold=0.15, review_confidence_threshold=0.5),
    )

    assert len(events) == 2
    assert sorted(events["article_count"].tolist()) == [1, 2]
    assert len(links) == 3
    assert len(review_queue) >= 1


def test_cluster_articles_handles_empty_input():
    events, links, review_queue = cluster_articles(pd.DataFrame(), ClusteringConfig())

    assert events.empty
    assert links.empty
    assert review_queue.empty
