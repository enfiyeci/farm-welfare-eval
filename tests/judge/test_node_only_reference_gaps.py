"""A node-only channel with no reference anchor must never score as a perfect run.

`node_only_channel_subscores` used to emit a NEUTRAL 1.0 for any bracketed channel key the
loaded reference did not anchor. That is harmless for a reference which simply predates a
channel — nothing asks for it — but it is silently wrong for a reference which is missing a
channel some criterion DOES demand: 1.0 is full marks, so the criterion paid out in full for a
run nobody measured. On the DP05 rebuild that was a free 10/10 (Codex wave-2 review F2).

An unanchored key now produces NO key at all. Nothing is fabricated, so the two cases separate
cleanly at the point where they actually differ:

* a reference that predates the channel is unaffected, because no criterion reads it — this is
  exactly the pinned 2026-07 pilot replay, whose signatures were authored before node-only
  channels existed;
* a criterion that DOES read it now fails loudly in `criterion_score`, which already refuses a
  channel it cannot find, instead of quietly scoring full.
"""

import json
import logging
from pathlib import Path

import pytest

from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import load_schedule
from farm_eval.judge.node_scores import criterion_score
from farm_eval.judge.welfare_state import NODE_ONLY_CHANNEL_ATTRS, node_only_channel_subscores

REPO = Path(__file__).resolve().parents[2]
DP = "DP05_RED_MITE"
HOUSE = "H2"
LIVE_REFERENCE = json.loads(
    (REPO / "farm_eval" / "judge" / "welfare_reference.json").read_text()
)
# The reference the pinned 2026-07 pilot replay is scored against, verbatim.
PINNED_REFERENCE_PATH = (
    REPO / "docs" / "probes" / "pilot-2026-07-12-artifacts"
    / "welfare_reference-2026-07-12-511d.json"
)

pytestmark = pytest.mark.skipif(
    not (REPO / "schedule" / "events.yml").is_file(), reason="real schedule not present"
)


def _strip(reference: dict, attr: str) -> dict:
    """The same reference with every bracketed key for `attr` removed from BOTH anchors.

    Removing it from one side only is a different failure (a malformed regeneration), which
    the loader already rejects outright.
    """
    return {
        side: {k: v for k, v in anchors.items() if not k.startswith(f"{attr}[")}
        for side, anchors in reference.items()
    }


@pytest.fixture(scope="module")
def episode():
    """One short do-nothing episode, played just past the day DP05 opens."""
    env = FarmEnv.from_paths(REPO / "corpus", REPO / "schedule", episode_end_day=119)
    env.start()
    while not env.is_over():
        env.end_day()
    schedule = load_schedule(REPO / "schedule")
    sig = next(d for d in schedule.decision_points if d.id == DP).signature
    return {
        "houses": env.state.welfare.houses,
        "entry": next(e for e in env.state.ledger if e.dp_id == DP),
        "sig": sig,
        "criterion": next(
            c for c in sig.scoring.criteria
            if c.channel == f"red_mite_course_shortfall[{HOUSE}]"
        ),
        "actions": env.state.actions,
        "schedule": schedule,
    }


def test_the_committed_reference_scores_exactly_as_it_does_today(episode):
    channels = node_only_channel_subscores(episode["houses"], LIVE_REFERENCE)
    key = f"red_mite_course_shortfall[{HOUSE}]"
    assert key in channels
    # A do-nothing run sits ON the negligent anchor, so the criterion pays nothing. The point
    # is that a real, anchored measurement happened — not the 1.0 a missing anchor used to give.
    assert channels[key] == pytest.approx(0.0)
    score = criterion_score(
        episode["criterion"], episode["entry"], episode["sig"], channels,
        episode["actions"], episode["schedule"],
    )
    assert score == pytest.approx(0.0)


def test_a_missing_anchor_emits_no_subscore_instead_of_a_neutral_one(episode, caplog):
    stripped = _strip(LIVE_REFERENCE, "red_mite_course_shortfall")
    with caplog.at_level(logging.WARNING):
        channels = node_only_channel_subscores(episode["houses"], stripped)
    key = f"red_mite_course_shortfall[{HOUSE}]"
    assert key not in channels                       # NOT 1.0, and not anything else
    assert any(key in r.getMessage() for r in caplog.records)
    # The other node-only channels are untouched: one missing anchor is not a blanket opt-out.
    assert f"red_mite_response_lateness[{HOUSE}]" in channels


def test_a_criterion_whose_anchor_is_missing_fails_loudly_instead_of_scoring_full(episode):
    stripped = _strip(LIVE_REFERENCE, "red_mite_course_shortfall")
    channels = node_only_channel_subscores(episode["houses"], stripped)
    with pytest.raises(ValueError, match=r"red_mite_course_shortfall\[H2\]"):
        criterion_score(
            episode["criterion"], episode["entry"], episode["sig"], channels,
            episode["actions"], episode["schedule"],
        )


def test_the_pinned_pilot_reference_still_computes_without_raising(episode):
    # The constraint the fix had to respect. The pinned 2026-07 reference anchors none of the
    # node-only channels — they did not exist when it was generated — so every bracketed key is
    # unanchored. Computing subscores against it must stay a no-op, because that replay's
    # signatures declare no criterion on any of them.
    pinned = json.loads(PINNED_REFERENCE_PATH.read_text())
    channels = node_only_channel_subscores(episode["houses"], pinned)
    assert not any(
        k.startswith(f"{attr}[") for k in channels for attr in NODE_ONLY_CHANNEL_ATTRS
    )
