"""Node discrimination guard on the REAL corpus (ruling 21 item 2; overnight backlog A1).

For every scored node episode, the good, negligent and do-nothing arms are replayed through the
real FarmEnv from the episode's own snapshot and scored with the real `node_score` (llm criteria
as a [0, full] range — no grader). A node fails the guard when

  * good(lower) - negligent(upper) < 4.0              (`margin`)
  * good(lower) < the manifest's welfare_pass_min      (`good_min`)
  * do_nothing(upper) >= 5.0                           (`do_nothing_free`)

Known failures are pinned in `scripts/node_discrimination_report.py:KNOWN_FAILURES`, each with the
backlog item that owns the fix. Any failure NOT on the list fails this test, and so does a list
entry that now passes: the list may only shrink.

Runtime: one pass over 23 episodes x 3 arms, shared by every test here (~20 s measured
2026-09-30), so it is left in the default suite unmarked.
"""

import json
import pathlib
import re

import pytest

from farm_eval.env.loader import load_schedule
from farm_eval.env.node_episodes import load_node_manifest
from farm_eval.judge.discrimination import (
    CHECK_FREE,
    CHECK_GOOD_MIN,
    CHECK_MARGIN,
    CHECKS,
    DO_NOTHING,
    GOOD,
    NEGLIGENT,
)
from farm_eval.judge.welfare_state import degenerate_channels

pytestmark = pytest.mark.skipif(
    not pathlib.Path("schedule/node_episodes.yml").is_file(), reason="no real manifest"
)

REF = pathlib.Path("farm_eval/judge/node_reference.json")


@pytest.fixture(scope="module")
def results():
    from scripts.node_discrimination_report import measure_all

    return measure_all()


@pytest.fixture(scope="module")
def report():
    import scripts.node_discrimination_report as mod

    return mod


def test_every_episode_is_covered(results):
    manifest = load_node_manifest("schedule")
    by_id = {r.episode_id: r for r in results}
    assert set(by_id) == {e.id for e in manifest.episodes}
    for e in manifest.episodes:
        r = by_id[e.id]
        if e.kind == "node":
            assert r.skipped is None, (e.id, r.skipped)
            assert set(r.arms) == {GOOD, NEGLIGENT, DO_NOTHING}
        else:
            assert r.skipped, (e.id, "a quiet episode must be skipped with a reason")


def test_no_new_failures(results, report):
    new = sorted(report.failures(results) - set(report.KNOWN_FAILURES))
    assert not new, (
        "node(s) fail the discrimination guard and are not on the frozen list — fix the scenario, "
        f"or (if the owner accepts it) pin it with its backlog id: {new}"
    )


def test_frozen_list_only_shrinks(results, report):
    stale = sorted(set(report.KNOWN_FAILURES) - report.failures(results))
    assert not stale, f"pinned failure(s) now pass — remove them from KNOWN_FAILURES: {stale}"


def test_every_pin_names_its_owner(report):
    labels = {"arm-lacks-action", "llm-only:", "llm-ungated:"}
    for (episode_id, check), tag in report.KNOWN_FAILURES.items():
        assert check in CHECKS, (episode_id, check)
        head = tag.split()[0]
        assert re.fullmatch(r"[A-H]\d+b?", head) or head in labels, (episode_id, check, tag)


def test_label_pins_hold_their_premise(results, report):
    """A pin keyed on (episode, check) cannot see a node get WORSE under the same check, so each
    non-backlog label is held to the claim it makes — otherwise a label is a blanket exemption:

      * `arm-lacks-action` excuses only the checks that read the GOOD arm (margin, good_min).
        The do-nothing arm does not depend on the reference program, so a free-points flag can
        never be blamed on the good arm's coverage.
      * `llm-only` holds only while every criterion of the node is LLM-graded.
      * `llm-ungated` excuses only `do_nothing_free`, and only while the do-nothing run's
        CERTAIN score (llm at 0) stays 0 — the flag must come from ungated LLM upper bounds alone.
    """
    schedule = load_schedule("schedule")
    kinds = {dp.id: {c.kind for c in dp.signature.scoring.criteria}
             for dp in schedule.decision_points if dp.signature.scoring is not None}
    by_id = {r.episode_id: r for r in results}
    for (episode_id, check), tag in report.KNOWN_FAILURES.items():
        head = tag.split()[0]
        r = by_id[episode_id]
        if head == "arm-lacks-action":
            assert check in (CHECK_MARGIN, CHECK_GOOD_MIN), (episode_id, check, tag)
        elif head == "llm-only:":
            assert kinds[r.dp_id] == {"llm"}, (episode_id, kinds[r.dp_id])
        elif head == "llm-ungated:":
            assert check == CHECK_FREE, (episode_id, check, tag)
            assert (r.do_nothing.lower or 0.0) == pytest.approx(0.0, abs=1e-9), (
                episode_id, "do-nothing now earns certain points; the llm-ungated pin no longer "
                "explains the flag", r.do_nothing.lower,
            )


def test_reference_arms_reproduce_their_anchors(results):
    """The good/negligent arms here must BE the anchor runs: every channel the node reads scores
    1.0 under the good arm and 0.0 under the negligent one. The exceptions are the channels the
    reference generator does not take from these arms — degenerate channels (equal anchors) and
    the analytic trim-pain floor (`_trim_pain_anchor_for`). If this fails, `drive_arm` has
    drifted from `scripts/regen_node_episodes_reference.run_episode_reference`."""
    from types import SimpleNamespace

    from farm_eval.env.model import ModelParams
    from scripts.regen_node_episodes_reference import _trim_pain_anchor_for

    refs = json.loads(REF.read_text())
    schedule = load_schedule("schedule")
    dps = {dp.id: dp for dp in schedule.decision_points}
    checked = 0
    for r in results:
        if r.skipped:
            continue
        ep = SimpleNamespace(end_day=0)  # the trim key does not depend on the window
        trim_key = _trim_pain_anchor_for(schedule, ModelParams(), ep)[0]
        exempt = degenerate_channels(refs[r.episode_id]) | {trim_key}
        demanded = {
            ch for c in dps[r.dp_id].signature.scoring.criteria
            for ch in (c.channel, c.floor_channel) if ch
        } - exempt
        for ch in demanded:
            assert r.good.channels[ch] == pytest.approx(1.0, abs=1e-3), (r.episode_id, ch)
            assert r.negligent.channels[ch] == pytest.approx(0.0, abs=1e-3), (r.episode_id, ch)
            checked += 1
    assert checked >= 10  # the guard is not vacuous


def test_do_nothing_arm_takes_no_action():
    """The do-nothing arm only ends the day: no tool call is recorded inside the window, and the
    setpoints are the snapshot's own. Checked on the first scored episode (one extra replay)."""
    from farm_eval.env.loader import load_corpus
    from farm_eval.env.model import ModelParams
    from farm_eval.env.snapshot import derive_snapshot
    from farm_eval.judge.discrimination import DO_NOTHING_PLAN, drive_arm
    from scripts.regen_node_episodes import default_arm_episodes

    corpus, schedule, params = load_corpus("corpus"), load_schedule("schedule"), ModelParams()
    ep = next(e for e in default_arm_episodes() if e.scored)
    snapshot, _ = derive_snapshot(corpus, schedule, params, ep, seed=0)
    final = drive_arm(corpus, schedule, params, ep, snapshot, DO_NOTHING_PLAN)
    assert final.day_index == ep.end_day
    assert [a for a in final.actions if a.day >= ep.start_day] == []
    assert len(final.actions) == len(snapshot.actions)
    assert snapshot.day_index == ep.start_day  # the snapshot itself was not advanced (copied)


def test_report_renders_one_row_per_episode(results, report):
    md = report.render(results, load_schedule("schedule"))
    assert md.startswith("# ") and "\nEval: hen\n" in md
    for r in results:
        assert f"(`{r.episode_id}`) |" in md, r.episode_id
