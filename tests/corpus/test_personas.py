"""The persona bible is the WS1 foundation: every schedule sender must have a voice
definition (personas.md prose) and lint rules (personas.yml)."""
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]


def _schedule_senders() -> set[str]:
    data = yaml.safe_load((REPO_ROOT / "schedule" / "events.yml").read_text())
    senders = set()
    for ev in data["events"]:
        frm = ev.get("payload", {}).get("from")
        if frm:
            senders.add(frm)
    return senders


def test_personas_yml_covers_every_schedule_sender():
    cfg = yaml.safe_load((REPO_ROOT / "corpus" / "personas.yml").read_text())
    covered = {p["email"] for p in cfg["personas"]}
    missing = _schedule_senders() - covered
    assert not missing, f"schedule senders without a persona definition: {sorted(missing)}"


def test_personas_yml_rules_are_well_formed():
    cfg = yaml.safe_load((REPO_ROOT / "corpus" / "personas.yml").read_text())
    g = cfg["global"]
    for key in ("em_dash_words_per", "em_dash_per_file_words_per", "question_file_fraction_max",
                "question_max_per_file", "length_cv_min", "short_words", "short_fraction_min",
                "long_words", "long_fraction_min", "banned_lexemes", "banned_patterns"):
        assert key in g, f"personas.yml global block missing {key!r}"
    for p in cfg["personas"]:
        assert set(p) >= {"email", "name", "max_words"}, f"persona {p} missing required keys"
        assert isinstance(p["max_words"], int) and p["max_words"] > 0


def test_personas_md_documents_every_persona():
    cfg = yaml.safe_load((REPO_ROOT / "corpus" / "personas.yml").read_text())
    md = (REPO_ROOT / "corpus" / "personas.md").read_text()
    undocumented = [p["name"] for p in cfg["personas"] if p["name"] not in md]
    assert not undocumented, f"personas.yml entries not documented in personas.md: {undocumented}"
