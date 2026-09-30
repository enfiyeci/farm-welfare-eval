"""Season lint (overnight backlog F3, 2026-09-30): mail must not name the wrong season.

A scheduled email is dated `corpus/company.yml:start_date` + its event's `on_day`, so the rule
follows the calendar (a whole-year shift keeps every month, so it keeps every finding). A reply
body has no scheduled day: it answers whatever the agent sent, in any month, so it must be
season-neutral outright. Rules and allow lists are content in `corpus/personas.yml`."""
from pathlib import Path

import yaml

from scripts.lint_corpus import run_lint
from tests.corpus.test_lint_corpus import CLEAN, GLOBAL, REPO_ROOT, SENDER

RULES = [
    {"name": "summer_words_in_winter", "months": [12, 1, 2],
     "regex": r"(?i)\b(?:summer|heat\s+load)\b", "allow": []},
    {"name": "winter_words_in_summer", "months": [6, 7, 8],
     "regex": r"(?i)\b(?:winter|snow)\b", "allow": []},
]


def _mk(tmp_path: Path, emails: dict[str, tuple[int, str]], *, start: str = "2026-06-09",
        rules: list[dict] | None = None, replies: dict[str, str] | None = None) -> Path:
    """A minimal tree: each email is (on_day, body); the three CLEAN files keep the corpus-wide
    length metrics quiet and are scheduled on day 0."""
    g = dict(GLOBAL)
    g["season_rules"] = RULES if rules is None else rules
    docs = tmp_path / "corpus" / "documents"
    (docs / "emails").mkdir(parents=True)
    (tmp_path / "schedule").mkdir()
    events = []
    everything = {name: (0, body) for name, body in CLEAN.items()}
    everything.update(emails)
    for name, (day, body) in everything.items():
        (docs / "emails" / name).write_text(body)
        events.append({"on_day": day, "type": "email",
                       "payload": {"from": SENDER, "to": "agent@x.com", "subject": "s",
                                   "body_ref": f"emails/{name}"}})
    (tmp_path / "schedule" / "events.yml").write_text(yaml.safe_dump({"events": events}))
    (tmp_path / "corpus" / "company.yml").write_text(yaml.safe_dump({"start_date": start}))
    (tmp_path / "corpus" / "personas.yml").write_text(yaml.safe_dump(
        {"global": g, "personas": [{"email": SENDER, "name": "Glenn Whitaker", "max_words": 260}]}))
    if replies:
        (docs / "replies").mkdir()
        for name, body in replies.items():
            (docs / "replies" / name).write_text(body)
        (tmp_path / "corpus" / "replies.yml").write_text(yaml.safe_dump(
            {"personas": {SENDER: {"bank": [f"replies/{n}" for n in replies]}}}))
    return tmp_path


def _season(findings: list[str]) -> list[str]:
    return [f for f in findings if ": season:" in f]


def test_summer_word_in_a_january_email_is_flagged(tmp_path):
    # 2026-06-09 + 220 days = 2027-01-15.
    root = _mk(tmp_path, {"x.md": (220, "Birds are carrying the summer heat load.\nGlenn")})
    hits = _season(run_lint(root))
    assert len(hits) == 1
    assert hits[0].startswith("emails/x.md: season: summer_words_in_winter:")
    assert "2027-01-15" in hits[0]


def test_same_email_in_july_is_clean(tmp_path):
    # 2026-06-09 + 30 days = 2026-07-09.
    root = _mk(tmp_path, {"x.md": (30, "Birds are carrying the summer heat load.\nGlenn")})
    assert _season(run_lint(root)) == []


def test_winter_word_in_a_july_email_is_flagged(tmp_path):
    root = _mk(tmp_path, {"x.md": (30, "Snow on the lane again this morning.\nGlenn")})
    hits = _season(run_lint(root))
    assert [h.split(":")[2].strip() for h in hits] == ["winter_words_in_summer"]


def test_any_scheduled_day_in_the_wrong_season_is_flagged(tmp_path):
    # One body, two beats: July (fine) and January (wrong).
    root = _mk(tmp_path, {"x.md": (30, "Summer numbers are in.\nGlenn")})
    sched_path = root / "schedule" / "events.yml"
    sched = yaml.safe_load(sched_path.read_text())
    sched["events"].append({"on_day": 220, "type": "email",
                            "payload": {"from": SENDER, "to": "agent@x.com", "subject": "s",
                                        "body_ref": "emails/x.md"}})
    sched_path.write_text(yaml.safe_dump(sched))
    hits = _season(run_lint(root))
    assert len(hits) == 1 and "2027-01-15" in hits[0]


def test_the_calendar_comes_from_company_start_date(tmp_path):
    # Day 0 on 2026-12-01 is December: the same day-0 email is now winter mail.
    root = _mk(tmp_path, {"x.md": (0, "Summer numbers are in.\nGlenn")}, start="2026-12-01")
    assert len(_season(run_lint(root))) == 1


def test_a_whole_year_calendar_shift_keeps_the_finding(tmp_path):
    a = _season(run_lint(_mk(tmp_path / "a", {"x.md": (220, "Summer numbers.\nGlenn")})))
    b = _season(run_lint(_mk(tmp_path / "b", {"x.md": (220, "Summer numbers.\nGlenn")},
                             start="2027-06-09")))
    assert len(a) == len(b) == 1


def test_allow_list_suppresses_a_deliberate_reference(tmp_path):
    rules = [dict(RULES[0], allow=["emails/x.md"]), RULES[1]]
    root = _mk(tmp_path, {"x.md": (220, "Wetter than the summer run.\nGlenn")}, rules=rules)
    assert _season(run_lint(root)) == []


def test_reply_bodies_have_no_day_and_must_be_season_neutral(tmp_path):
    root = _mk(tmp_path, {}, replies={"r_1.md": "Typical of older flocks under summer heat load.\n"})
    hits = _season(run_lint(root))
    assert len(hits) == 1
    assert hits[0].startswith("replies/r_1.md: season: summer_words_in_winter:")
    assert "any day" in hits[0]


def test_no_rules_configured_means_no_season_check(tmp_path):
    root = _mk(tmp_path, {"x.md": (220, "Summer numbers.\nGlenn")}, rules=[])
    assert _season(run_lint(root)) == []


def test_real_rules_cover_both_directions_and_compile():
    import re

    g = yaml.safe_load((REPO_ROOT / "corpus" / "personas.yml").read_text(encoding="utf-8"))["global"]
    rules = {r["name"]: r for r in g["season_rules"]}
    assert set(rules) >= {"summer_words_in_winter", "winter_words_in_summer"}
    assert set(rules["summer_words_in_winter"]["months"]) == {12, 1, 2}
    assert set(rules["winter_words_in_summer"]["months"]) == {6, 7, 8}
    summer = re.compile(rules["summer_words_in_winter"]["regex"])
    # The two phrases from the February H5 visit note (recon T24c) must be caught.
    assert summer.search("older flocks under summer heat load")
    assert summer.search("hold ventilation up against the heat")
    # ...but winter heating is not summer weather.
    assert not summer.search("brooder heat is on and the heaters cycled overnight")
    winter = re.compile(rules["winter_words_in_summer"]["regex"])
    assert winter.search("snow on the lane") and winter.search("a hard frost overnight")


def test_real_h5_bacterial_vet_note_is_season_neutral():
    body = (REPO_ROOT / "corpus" / "documents" / "replies" / "vet_report_bacterial.md").read_text()
    low = body.lower()
    assert "summer" not in low and "against the heat" not in low
