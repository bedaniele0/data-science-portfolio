from __future__ import annotations

from html import escape

import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.view_model import build_dashboard_snapshot, create_store, frame, kpi_summary, load_dashboard_config

st.set_page_config(page_title="News Event Observatory", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
    .kpi-card {
        background: #151b24;
        border: 1px solid #2e3a4d;
        border-radius: 8px;
        padding: 18px 20px;
        min-height: 112px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }
    .kpi-label {
        color: #cbd5e1;
        font-size: 0.95rem;
        font-weight: 650;
        margin-bottom: 12px;
    }
    .kpi-value {
        color: #ffffff;
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1;
    }
    .stTabs [data-baseweb="tab-list"] {gap: 6px;}
    .stTabs [data-baseweb="tab"] {height: 38px; border-radius: 6px; padding: 8px 14px;}
    h1, h2, h3 {letter-spacing: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)

config = load_dashboard_config("configs/dashboard.yaml")
dashboard_cfg = config.get("dashboard", {})
snapshot = build_dashboard_snapshot("configs/dashboard.yaml")
kpis = kpi_summary(snapshot)
store = create_store(config)

st.title(str(dashboard_cfg.get("title", "News Event Observatory")))

def render_kpi(label: str, value: int) -> None:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{escape(label)}</div>
            <div class="kpi-value">{value:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


left, mid_left, mid_right, right = st.columns(4)
with left:
    render_kpi("Articulos", kpis["articles"])
with mid_left:
    render_kpi("Eventos", kpis["events"])
with mid_right:
    render_kpi("En revision", kpis["review_queue"])
with right:
    render_kpi("Notas procesadas", kpis["scored_articles"])

status_df = frame(snapshot["status_summary"])
media_df = frame(snapshot["media_coverage"])
events_df = frame(snapshot["events"])
review_df = frame(snapshot["review_queue"])

tab_events, tab_review, tab_search, tab_system = st.tabs(["Eventos", "Revision", "Busqueda", "Sistema"])

with tab_events:
    chart_left, chart_right = st.columns([1, 1])
    with chart_left:
        if not status_df.empty:
            fig = px.bar(status_df, x="status", y="event_count", color="status", text="event_count", title="Eventos por estado")
            fig.update_layout(showlegend=False, margin={"l": 20, "r": 20, "t": 50, "b": 20}, height=320)
            st.plotly_chart(fig, width="stretch")
    with chart_right:
        if not media_df.empty:
            fig = px.bar(media_df, x="article_count", y="media", orientation="h", text="article_count", title="Cobertura por medio")
            fig.update_layout(showlegend=False, margin={"l": 20, "r": 20, "t": 50, "b": 20}, height=320, yaxis={"autorange": "reversed"})
            st.plotly_chart(fig, width="stretch")

    display_columns = ["event_id", "event_title", "article_count", "media_count", "confidence", "status", "first_date", "last_date"]
    st.dataframe(events_df[display_columns], width="stretch", hide_index=True)

    event_options = events_df["event_id"].tolist() if not events_df.empty else []
    selected_event = st.selectbox("Evento", event_options, index=0 if event_options else None)
    if selected_event:
        detail = store.get_event(selected_event)
        articles_df = frame(store.get_event_articles(selected_event))
        if detail:
            st.subheader(detail["event_title"])
            st.dataframe(articles_df[["article_id", "title", "media", "published_at", "link_confidence", "url"]], width="stretch", hide_index=True)

with tab_review:
    if not review_df.empty:
        st.dataframe(
            review_df[["event_id", "event_title", "article_count", "media_count", "confidence", "review_reason", "example_url"]],
            width="stretch",
            hide_index=True,
        )
    else:
        st.success("Sin eventos pendientes de revision")

with tab_search:
    query = st.text_input("Buscar", value=str(dashboard_cfg.get("smoke_search_text", "asesinado")))
    if query.strip():
        results = frame(store.search_articles(query, limit=int(dashboard_cfg.get("search_limit", 20))))
        if not results.empty:
            st.dataframe(results[["article_id", "title", "media", "published_at", "event_id", "relevance_score", "url"]], width="stretch", hide_index=True)
        else:
            st.info("Sin resultados")

with tab_system:
    checks = pd.Series(snapshot["dashboard_checks"], name="passed").reset_index().rename(columns={"index": "check"})
    st.dataframe(checks, width="stretch", hide_index=True)
    st.json({"table_counts": snapshot["table_counts"], "top_event_id": snapshot["top_event_id"]})
