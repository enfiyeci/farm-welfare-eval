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
    # House ids, personnel, corpus strings, brand, and the egg-disposition channel enum must
    # all come from op results / the briefing at runtime — never baked into the page. Tokens are
    # case-sensitive: uppercase house ids (H1..H6) can't collide with lowercase HTML heading
    # tags (<h2>), and "Cloverdale" (bare) also catches "Cloverdale Egg Farms".
    forbidden = (
        "H1", "H2", "H3", "H4", "H5", "H6",              # house ids
        "Cloverdale", "Salgado", "Vega", "propane",       # brand / personnel / corpus prose
        "shell", "breaker", "pasteurization", "discard",  # egg-disposition channel enum
    )
    for token in forbidden:
        assert token not in html, f"farm content {token!r} hardcoded in the page"


def test_page_never_polls():
    html = PAGE.read_text(encoding="utf-8")
    assert "setInterval" not in html  # click-to-fetch only (spec §4.2)


def test_page_has_core_affordances():
    html = PAGE.read_text(encoding="utf-8")
    for needle in ("/api/meta", "/api/briefing", "/api/op/", "/api/end_day", "/api/note",
                   "/api/report", "id=\"diary\"", "id=\"log\""):
        assert needle in html, f"missing affordance {needle!r}"


def test_page_has_quick_actions_affordances():
    """Quick-reads toolbar, per-house tile actions, and the clickable inbox (quick-actions
    increment) — generic hooks only, no farm content (see test_page_has_no_hardcoded_farm_content)."""
    html = PAGE.read_text(encoding="utf-8")
    for needle in (
        "quickbar", "buildQuickReads",              # 1. quick-reads toolbar
        "tile-actions", "stopPropagation",           # 2. per-house tile action buttons
        "id=\"inbox\"", "renderInbox", "read_email",  # 3. clickable inbox
    ):
        assert needle in html, f"missing quick-actions affordance {needle!r}"
    # the tile is now a div (nested-button fix), not a button
    assert 'el("div", { class: "tile" })' in html
    assert 'el("button", { type: "button", class: "tile"' not in html
