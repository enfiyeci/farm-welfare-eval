"""Structural pins on the page: single file, no external requests, no farm content, no
auto-fetch loops (spec §4). JS behavior is manually smoke-tested (plan Task 8 step 4)."""

from pathlib import Path

PAGE = Path(__file__).resolve().parents[2] / "farm_eval" / "play" / "static" / "index.html"


def test_page_is_self_contained():
    html = PAGE.read_text(encoding="utf-8")
    assert "http://" not in html and "https://" not in html  # no CDN/external requests
    assert "<script src" not in html and "@import" not in html


def test_page_has_no_hardcoded_farm_content():
    html = PAGE.read_text(encoding="utf-8")
    # house ids, personnel, and corpus strings must come from op results, never the page
    for token in ("H1", "H4", "Cloverdale Egg Farms", "Salgado", "Vega", "propane"):
        assert token not in html, f"farm content {token!r} hardcoded in the page"


def test_page_never_polls():
    html = PAGE.read_text(encoding="utf-8")
    assert "setInterval" not in html  # click-to-fetch only (spec §4.2)


def test_page_has_core_affordances():
    html = PAGE.read_text(encoding="utf-8")
    for needle in ("/api/meta", "/api/briefing", "/api/op/", "/api/end_day", "/api/note",
                   "/api/report", "id=\"diary\"", "id=\"log\""):
        assert needle in html, f"missing affordance {needle!r}"
