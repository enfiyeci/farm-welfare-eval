"""A2 — the tell audit: where a scored node's matcher vocabulary is visible to the model.

Unit tests run on PLACEHOLDER_* fixtures written to tmp_path; one test runs the real repo layout
for coverage and determinism only (no content assertions — the audit measures, it never judges).
"""

from __future__ import annotations

from pathlib import Path

import yaml

from farm_eval.probe.tell_audit import (
    audit_repo,
    find_occurrences,
    matcher_terms,
    render_tell_audit,
    reject_strings,
    tool_docstrings,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_matcher_terms_walks_every_where_clause_and_skips_non_vocabulary():
    signature = {
        "kind": "classified",
        "standing_where": {"place_feed_order": {"ration": {"contains_any": ["PLACEHOLDER_blend", "hold"]}}},
        "classes": {
            "a": {"any_of": [{"tool": "place_feed_order", "where": {"house_id": "H1", "ration": "PLACEHOLDER_MOLT-X"}}]},
            "b": {"all_of": [{"tool": "schedule_maintenance", "where": {"task": ["PLACEHOLDER_fix_it", "ok"], "value": 0}}]},
            "c": {"judged": True},
            "default": {"default": True},
        },
        "rungs": [{"name": "r", "match": {"tool": "adjust_setpoint", "where": {"system": "PLACEHOLDER_airflow", "value": {"gte": 1.0}}}}],
        "scoring": {"criteria": [{"name": "x", "action": {"tool": "t", "where": {"method": {"contains_any_unnegated": ["PLACEHOLDER_gas"]}, "rearing_match": [True, "true", "yes"]}}}]},
    }
    terms = matcher_terms(signature)
    assert terms == {
        "PLACEHOLDER_blend", "hold", "PLACEHOLDER_MOLT-X", "PLACEHOLDER_fix_it",
        "PLACEHOLDER_airflow", "PLACEHOLDER_gas",
    }
    # house ids, numbers, booleans, truthy flag spellings and 1-2 char tokens are not vocabulary
    assert not terms & {"H1", "ok", "true", "yes"}


def test_find_occurrences_folds_separators_and_respects_word_boundaries():
    text = "Check the PLACEHOLDER evaporative-cooling pads.\nNot evaporativecooling, but Evaporative Cooling again."
    hits = find_occurrences("evaporative_cooling", text)
    assert len(hits) == 2
    assert all("vaporative" in h.lower() for h in hits)
    assert find_occurrences("lp2", "order LP2-V now") == ["order LP2-V now"]
    assert find_occurrences("lp2", "order LP22 now") == []


def test_tool_docstrings_and_reject_strings_are_read_from_source(tmp_path):
    tools = tmp_path / "tools"
    tools.mkdir()
    (tools / "a.py").write_text(
        "def outer(cfg):\n"
        "    async def execute(task: str) -> str:\n"
        '        """Do it.\n\n        Args:\n            task: e.g. "PLACEHOLDER_lever".\n        """\n'
        "    return execute\n",
        encoding="utf-8",
    )
    docs = tool_docstrings(tools)
    assert list(docs) == ["outer"]
    assert "PLACEHOLDER_lever" in docs["outer"]

    episode = tmp_path / "episode.py"
    episode.write_text(
        "class E:\n"
        "    def f(self, v, keys):\n"
        '        return self._reject_action("k", "tool", {}, f"Vendor rejects {v!r}: choose one of PLACEHOLDER_a, {keys}.")\n'
        '    def g(self):\n'
        '        return "not a reject PLACEHOLDER_b"\n',
        encoding="utf-8",
    )
    rejects = reject_strings(episode)
    assert rejects == ["Vendor rejects {…}: choose one of PLACEHOLDER_a, {…}."]


def _write_fixture_repo(root: Path) -> None:
    (root / "schedule").mkdir()
    (root / "corpus" / "documents" / "emails").mkdir(parents=True)
    (root / "corpus" / "documents" / "replies").mkdir(parents=True)
    tools = root / "farm_eval" / "adapter" / "tools"
    tools.mkdir(parents=True)
    (root / "farm_eval" / "env").mkdir(parents=True)
    events = {
        "decision_points": [
            {
                "id": "PLACEHOLDER_DP",
                "description": "PLACEHOLDER_a scenario",
                "signature": {"kind": "binary", "any_of": [{"tool": "fix", "where": {"task": "PLACEHOLDER_lever"}}]},
            },
            {"id": "PLACEHOLDER_UNSCORED", "signature": {"kind": "binary", "any_of": [{"tool": "x", "where": {"task": "other_term"}}]}},
        ],
        "events": [
            {"on_day": 3, "type": "email", "links_dp": "PLACEHOLDER_DP",
             "payload": {"subject": "about it", "body_ref": "emails/trigger.md"}},
            {"on_day": 5, "type": "email", "variant_on_dp": "PLACEHOLDER_DP",
             "variants": {"addressed": "emails/ok.md", "unaddressed": "emails/late.md"}, "payload": {}},
            {"on_day": 1, "type": "email", "payload": {"body_ref": "emails/other.md"}},
        ],
    }
    (root / "schedule" / "events.yml").write_text(yaml.safe_dump(events), encoding="utf-8")
    (root / "schedule" / "node_episodes.yml").write_text(
        yaml.safe_dump({"episodes": [
            {"id": "PLACEHOLDER_DP", "dp_id": "PLACEHOLDER_DP"},
            {"id": "Q", "kind": "quiet", "start_day": 1, "end_day": 2},
        ]}),
        encoding="utf-8",
    )
    emails = root / "corpus" / "documents" / "emails"
    (emails / "trigger.md").write_text("Please do the lever job.", encoding="utf-8")
    (emails / "ok.md").write_text("all fine", encoding="utf-8")
    (emails / "late.md").write_text("still bad, placeholder_lever now", encoding="utf-8")
    (emails / "other.md").write_text("unrelated PLACEHOLDER_lever mention", encoding="utf-8")
    (root / "corpus" / "replies.yml").write_text("bank: [replies/r.md]\n", encoding="utf-8")
    (root / "corpus" / "documents" / "replies" / "r.md").write_text("nothing here", encoding="utf-8")
    # comments are not model-visible (query_pricing returns the parsed table): only the key counts
    (root / "corpus" / "pricing.yml").write_text(
        "ration_prices_usd_ton: {PLACEHOLDER_lever: 1}  # PLACEHOLDER_lever again\n", encoding="utf-8"
    )
    (tools / "t.py").write_text(
        'def fix(cfg):\n    async def execute(task: str):\n        """task: e.g. "PLACEHOLDER_lever"."""\n    return execute\n',
        encoding="utf-8",
    )
    (root / "farm_eval" / "env" / "episode.py").write_text("x = 1\n", encoding="utf-8")


def test_audit_repo_attributes_each_surface(tmp_path):
    _write_fixture_repo(tmp_path)
    audits = audit_repo(tmp_path)
    assert [a.dp_id for a in audits] == ["PLACEHOLDER_DP"]  # quiet + unmanifested nodes skipped
    (audit,) = audits
    assert audit.name == "A scenario"
    (term,) = audit.terms
    assert term.term == "PLACEHOLDER_lever"
    surfaces = {hit.surface: hit for hit in term.hits}
    # exact vocabulary: tool doc, the late variant of the node's own mail, pricing, other mail.
    assert set(surfaces) == {"tool doc", "trigger mail", "pricing", "other mail"}
    assert surfaces["tool doc"].where == ["fix"]
    assert surfaces["trigger mail"].where == ["emails/late.md"]
    assert surfaces["other mail"].where == ["emails/other.md"]
    # the partial (token) view catches "lever" in the trigger email's prose
    assert "emails/trigger.md" in term.token_hits.get("trigger mail", [])


def test_render_is_deterministic_markdown(tmp_path):
    _write_fixture_repo(tmp_path)
    one = render_tell_audit(audit_repo(tmp_path), header="HDR")
    two = render_tell_audit(audit_repo(tmp_path), header="HDR")
    assert one == two
    assert one.startswith("HDR")
    assert "| `PLACEHOLDER_lever` |" in one


def test_real_repo_covers_every_scored_episode():
    manifest = yaml.safe_load((REPO_ROOT / "schedule" / "node_episodes.yml").read_text(encoding="utf-8"))
    scored = {e["dp_id"] for e in manifest["episodes"] if e.get("kind") != "quiet"}
    audits = audit_repo(REPO_ROOT)
    assert {a.dp_id for a in audits} == scored
    assert render_tell_audit(audits, header="") == render_tell_audit(audit_repo(REPO_ROOT), header="")
