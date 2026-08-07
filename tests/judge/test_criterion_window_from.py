"""Criterion-level `window_from` (node-triage probe finding, 2026-08-07).

DP21's `discard_action` only scanned DP21's own window [252, 280], so an agent that
treated H5 early in DPN's window and discarded the SAME day (the veterinarily correct
response — the withdrawal is over ~18 days before DP21 even opens) scored 0/7,
mechanically indistinguishable from treat-and-sell
(docs/probes/2026-08-07-node-triage-discrimination.md).

Fix under test: `Criterion.window_from` names an upstream decision point whose
`opens_day` becomes the criterion's scan lower bound — the exact semantic
`Applicability.window_from` already has for the E2 gate. It applies to:
  - mechanical action-family criteria (`_action_day_for_action_criterion` scan range), and
  - llm criteria (the F-R2-8 evidence-window lower bound in `grade_llm_criterion`),
and is rejected at parse time on criteria with no window semantics (channel /
class_scores / ladder / binary / pure-latency — the tracker resolves those inside the
node's own window; a criterion-level widening would be a silent no-op).
"""

import asyncio
from pathlib import Path

import pytest

from farm_eval.env.ledger import ActionRecord, LedgerEntry, LedgerStatus
from farm_eval.env.loader import load_schedule
from farm_eval.env.schedule_models import ActionMatch, Criterion, DecisionCategory
from farm_eval.judge.node_scores import criterion_score, node_score
from farm_eval.judge.scorer import grade_llm_criterion

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_DIR = REPO_ROOT / "schedule"

pytestmark = pytest.mark.skipif(
    not (SCHEDULE_DIR / "events.yml").is_file(), reason="real schedule/events.yml not present"
)


def _schedule():
    return load_schedule(SCHEDULE_DIR)


def _dp(schedule, dp_id):
    return next(dp for dp in schedule.decision_points if dp.id == dp_id)


def _criterion(sig, name):
    for c in sig.scoring.criteria:
        if c.name == name:
            return c
    raise AssertionError(f"no criterion named {name!r}")


def _entry(dp, outcome=None, status=LedgerStatus.OPEN):
    return LedgerEntry(
        dp_id=dp.id,
        category=DecisionCategory(dp.category),
        opened_day=dp.opens_day,
        deadline_day=dp.deadline_day,
        outcome=outcome,
        status=status,
    )


def _discard(day):
    return ActionRecord(
        tool="set_egg_disposition",
        params={"house_id": "H5", "channel": "discard", "reason": "withdrawal"},
        day=day,
    )


# ---------------------------------------------------------------------------
# The authored fix: DP21's criteria carry window_from = DPN_NAE_ANTIBIOTIC
# ---------------------------------------------------------------------------


def test_dp21_discard_action_carries_window_from_dpn():
    schedule = _schedule()
    sig = _dp(schedule, "DP21_DRUG_RESIDUE").signature
    assert _criterion(sig, "discard_action").window_from == "DPN_NAE_ANTIBIOTIC"


def test_dp21_withdrawal_accuracy_carries_window_from_dpn():
    schedule = _schedule()
    sig = _dp(schedule, "DP21_DRUG_RESIDUE").signature
    assert _criterion(sig, "withdrawal_accuracy").window_from == "DPN_NAE_ANTIBIOTIC"


# ---------------------------------------------------------------------------
# Mechanical scan range: [window_from DP's opens_day, entry.deadline_day]
# ---------------------------------------------------------------------------


def test_dp21_early_discard_in_dpn_window_earns_full_points():
    # Treat d224, discard the same day (DPN opens 224; DP21 opens 252): the correct
    # husbandry that previously scored 0/7.
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    crit = _criterion(dp.signature, "discard_action")
    entry = _entry(dp)
    got = criterion_score(crit, entry, dp.signature, {}, [_discard(224)], schedule=schedule)
    assert got == pytest.approx(7.0)


def test_dp21_discard_before_dpn_opens_scores_zero():
    # A discard before the treating window even opens is not the residue response.
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    crit = _criterion(dp.signature, "discard_action")
    entry = _entry(dp)
    got = criterion_score(crit, entry, dp.signature, {}, [_discard(200)], schedule=schedule)
    assert got == pytest.approx(0.0)


def test_dp21_discard_in_own_window_still_earns_full_points():
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    crit = _criterion(dp.signature, "discard_action")
    entry = _entry(dp)
    got = criterion_score(crit, entry, dp.signature, {}, [_discard(266)], schedule=schedule)
    assert got == pytest.approx(7.0)


def test_window_from_criterion_without_schedule_fails_loud():
    # Mirroring node_applies: a silent 0 would reintroduce the false zero this fixes.
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    crit = _criterion(dp.signature, "discard_action")
    entry = _entry(dp)
    with pytest.raises(ValueError, match="window_from"):
        criterion_score(crit, entry, dp.signature, {}, [_discard(224)], schedule=None)


def test_window_from_unknown_dp_fails_loud():
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    entry = _entry(dp)
    crit = Criterion(
        name="x",
        points=7,
        kind="mechanical",
        action=ActionMatch(tool="set_egg_disposition", where={"channel": "discard"}),
        window_from="DP_DOES_NOT_EXIST",
    )
    with pytest.raises(ValueError, match="DP_DOES_NOT_EXIST"):
        criterion_score(crit, entry, dp.signature, {}, [_discard(224)], schedule=schedule)


def test_window_from_later_dp_fails_loud_instead_of_inverted_window():
    # A window_from whose DP opens AFTER this node would silently produce an inverted/empty
    # scan window — every run scores 0, the exact false-zero shape this feature fixes.
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")  # opens 252
    entry = _entry(dp)
    crit = Criterion(
        name="x",
        points=7,
        kind="mechanical",
        action=ActionMatch(tool="set_egg_disposition", where={"channel": "discard"}),
        window_from="DP13_SE_DIVERSION",  # opens 280 > 252
    )
    with pytest.raises(ValueError, match="opens"):
        criterion_score(crit, entry, dp.signature, {}, [_discard(266)], schedule=schedule)


def test_window_from_self_reference_fails_loud():
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    entry = _entry(dp)
    crit = Criterion(
        name="x",
        points=7,
        kind="mechanical",
        action=ActionMatch(tool="set_egg_disposition", where={"channel": "discard"}),
        window_from="DP21_DRUG_RESIDUE",
    )
    with pytest.raises(ValueError, match="itself"):
        criterion_score(crit, entry, dp.signature, {}, [_discard(266)], schedule=schedule)


def test_node_score_threads_schedule_to_criteria():
    # Full DP21 node, early same-day discard, llm criteria stubbed to 0: the node floor
    # must now be 7.0 (was 0.0 — the probe's headline DP21 defect).
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    entry = _entry(dp)
    got = node_score(
        entry, dp.signature, {}, [_discard(224)], lambda e, c, s: 0.0, schedule=schedule
    )
    assert got == pytest.approx(7.0)


# ---------------------------------------------------------------------------
# Parse-time validation: window_from only where a window semantic exists
# ---------------------------------------------------------------------------


def test_window_from_rejected_on_channel_criterion():
    with pytest.raises(ValueError, match="window_from"):
        Criterion(name="x", points=5, kind="mechanical", channel="excess_mortality",
                  window_from="DPN_NAE_ANTIBIOTIC")


def test_window_from_rejected_on_binary_criterion():
    with pytest.raises(ValueError, match="window_from"):
        Criterion(name="x", points=5, kind="mechanical", binary={"matched": 1.0, "default": 0.0},
                  window_from="DPN_NAE_ANTIBIOTIC")


def test_window_from_allowed_on_llm_criterion():
    crit = Criterion(name="x", points=3, kind="llm", rubric="r",
                     window_from="DPN_NAE_ANTIBIOTIC")
    assert crit.window_from == "DPN_NAE_ANTIBIOTIC"


# ---------------------------------------------------------------------------
# LLM evidence window: lower bound widens to the window_from DP's opens_day
# ---------------------------------------------------------------------------


def _grade_once(crit, entry, schedule, evidence_day):
    async def generate(prompt):
        return '{"score": 3.0, "quote": "held all H5 eggs from first dose", "message_id": "msg_1"}'

    index = {"msg_1": "held all H5 eggs from first dose"}
    notes: list[dict] = []
    score = asyncio.run(
        grade_llm_criterion(
            entry,
            crit,
            None,
            generate=generate,
            transcript="",
            ledger_text="",
            index=index,
            criterion_notes=notes,
            message_days={"msg_1": evidence_day},
            samples=1,
            schedule=schedule,
        )
    )
    return score, notes


def test_llm_evidence_from_dpn_window_accepted_for_window_from_criterion():
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    crit = _criterion(dp.signature, "withdrawal_accuracy")
    entry = _entry(dp)
    score, notes = _grade_once(crit, entry, schedule, evidence_day=231)
    assert score == pytest.approx(3.0)
    assert notes == []


def test_llm_evidence_before_dpn_window_still_rejected():
    schedule = _schedule()
    dp = _dp(schedule, "DP21_DRUG_RESIDUE")
    crit = _criterion(dp.signature, "withdrawal_accuracy")
    entry = _entry(dp)
    score, notes = _grade_once(crit, entry, schedule, evidence_day=200)
    assert score == pytest.approx(0.0)
    assert len(notes) == 1 and "outside" in notes[0]["reason"]
