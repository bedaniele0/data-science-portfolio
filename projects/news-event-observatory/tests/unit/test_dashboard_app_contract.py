from __future__ import annotations

from pathlib import Path


def test_dashboard_kpi_cards_have_readable_dark_theme_contract() -> None:
    app_source = Path("src/dashboard/app.py").read_text()

    assert "st.metric" not in app_source
    assert ".kpi-card" in app_source
    assert "background: #151b24" in app_source
    assert ".kpi-label" in app_source
    assert "color: #cbd5e1" in app_source
    assert ".kpi-value" in app_source
    assert "color: #ffffff" in app_source
    assert 'render_kpi("Articulos", kpis["articles"])' in app_source
    assert 'render_kpi("Eventos", kpis["events"])' in app_source
    assert 'render_kpi("En revision", kpis["review_queue"])' in app_source
    assert 'render_kpi("Notas procesadas", kpis["scored_articles"])' in app_source


def test_dashboard_app_renders_expected_kpis() -> None:
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file("src/dashboard/app.py")
    app.run(timeout=30)

    assert not app.exception
    rendered_markdown = "\n".join(item.value for item in app.markdown)
    assert '<div class="kpi-label">Articulos</div>' in rendered_markdown
    assert '<div class="kpi-value">668</div>' in rendered_markdown
    assert '<div class="kpi-label">Eventos</div>' in rendered_markdown
    assert '<div class="kpi-value">8</div>' in rendered_markdown
    assert '<div class="kpi-label">En revision</div>' in rendered_markdown
    assert '<div class="kpi-label">Notas procesadas</div>' in rendered_markdown
    assert [tab.label for tab in app.tabs] == ["Eventos", "Revision", "Busqueda", "Sistema"]
