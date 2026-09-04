"""The two mechanical criterion extensions DP24 needs: `band_credit` and `window_ratio`.

`band_credit` is an explicit band-name -> credit-fraction map, so a state_band node can pay
partial credit for landing in a middle band without the scorer knowing any band vocabulary
(the map is data; DP25's five-band vocabulary works the same way).

`window_ratio` scores an in-window DELTA ratio between two cumulative `HouseWelfare`
counters, from the snapshots the tracker takes at the decision's window OPEN and at its
deadline. The cumulative totals themselves cannot answer the question — they span the whole
episode and the whole complex, not this node's window and house.

The house under test is `PLACEHOLDER_HOUSE` and the signatures are hand-built, but the band
vocabulary and the two counter names are DP24's REAL ones, quoted deliberately so the arithmetic
exercised here is the arithmetic the authored node runs. No farm content reaches the logic: the
scorer only ever sees a house or a band name the signature handed it.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.schedule_models import (
    ActionMatch,
    Criterion,
    DecisionCategory,
    Metric,
    NodeScoring,
    Signature,
)
from farm_eval.judge.node_scores import criterion_score

HOUSE = "PLACEHOLDER_HOUSE"
BANDS = {"good": [[0, 7]], "marginal": [[8, 27]], "harm": [[28, 99999]]}
REALIZED = "opportunity_realized_hen_days"
AVAILABLE = "opportunity_available_hen_days"


def _sig(*, criteria: list[Criterion] | None = None, bands=None) -> Signature:
    return Signature(
        kind="state_band",
        metric=Metric(house_id=HOUSE, var="recurring_closure_days", agg="final"),
        bands=bands if bands is not None else BANDS,
        scoring=NodeScoring(criteria=criteria) if criteria is not None else None,
    )


def _entry(*, outcome=None, opened=None, closed=None) -> LedgerEntry:
    return LedgerEntry(
        dp_id="DP_PLACEHOLDER",
        category=DecisionCategory.INTEGRITY,
        opened_day=49,
        deadline_day=133,
        status=LedgerStatus.ADDRESSED,
        outcome=outcome,
        window_open_metrics=opened or {},
        window_close_metrics=closed or {},
    )


# --- band_credit: arithmetic ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("band", "expected"),
    [("good", 4.0), ("marginal", 2.0), ("harm", 0.0)],
)
def test_band_credit_pays_the_declared_fraction_of_the_criterion_points(band, expected):
    crit = Criterion(
        name="c", points=4.0, band_credit={"good": 1.0, "marginal": 0.5, "harm": 0.0}
    )
    sig = _sig(criteria=[Criterion(name="c", points=10.0, band_credit={
        "good": 1.0, "marginal": 0.5, "harm": 0.0})])
    assert criterion_score(crit, _entry(outcome=band), sig, {}, []) == pytest.approx(expected)


def test_band_credit_clamps_a_fraction_above_one():
    crit = Criterion(name="c", points=4.0, band_credit={"good": 2.0, "marginal": 0.5, "harm": 0.0})
    sig = _sig()
    assert criterion_score(crit, _entry(outcome="good"), sig, {}, []) == pytest.approx(4.0)


def test_band_credit_fails_loud_when_the_band_never_resolved():
    # An unresolved state_band entry (outcome None) reaching the scorer is a HARNESS defect,
    # not agent behaviour — a silent 0 would bury it in the headline as a false zero.
    crit = Criterion(name="c", points=4.0, band_credit={"good": 1.0, "marginal": 0.5, "harm": 0.0})
    with pytest.raises(ValueError, match="band"):
        criterion_score(crit, _entry(outcome=None), _sig(), {}, [])


def test_band_credit_fails_loud_when_the_value_fell_in_no_band():
    # `evaluate_state_band` records the raw numeric value when no declared band contains it.
    crit = Criterion(name="c", points=4.0, band_credit={"good": 1.0, "marginal": 0.5, "harm": 0.0})
    with pytest.raises(ValueError, match="band"):
        criterion_score(crit, _entry(outcome=7.5), _sig(), {}, [])


# --- band_credit: declaration rules --------------------------------------------------------


def test_band_credit_counts_as_the_single_mechanical_primary_scorer():
    with pytest.raises(ValidationError, match="exactly one primary scorer"):
        Criterion(name="c", points=4.0, band_credit={"good": 1.0}, channel="nh3_ppm_hours_over")


def test_band_credit_is_rejected_on_an_llm_criterion():
    with pytest.raises(ValidationError, match="must not set any mechanical"):
        Criterion(name="c", points=4.0, kind="llm", rubric="r", band_credit={"good": 1.0})


def test_band_credit_keys_must_be_declared_bands():
    with pytest.raises(ValidationError, match="band_credit"):
        _sig(criteria=[Criterion(name="c", points=10.0, band_credit={"good": 1.0, "typo": 0.0})])


def test_band_credit_must_map_every_declared_band():
    # An unmapped declared band is reachable at runtime and would raise mid-run; catch it at parse.
    with pytest.raises(ValidationError, match="band_credit"):
        _sig(criteria=[Criterion(name="c", points=10.0, band_credit={"good": 1.0, "marginal": 0.5})])


def test_band_credit_is_state_band_only():
    with pytest.raises(ValidationError, match="state_band"):
        Signature(
            kind="binary",
            any_of=[ActionMatch(tool="PLACEHOLDER_TOOL")],
            scoring=NodeScoring(criteria=[Criterion(name="c", points=10.0, band_credit={"g": 1.0})]),
        )


# --- window_ratio: arithmetic ---------------------------------------------------------------


def test_window_ratio_scores_the_in_window_delta_ratio():
    crit = Criterion(name="c", points=2.0, window_ratio={"realized": REALIZED, "available": AVAILABLE})
    entry = _entry(
        # The cumulative totals carry a large pre-window history that must NOT count.
        opened={REALIZED: 1000.0, AVAILABLE: 2000.0},
        closed={REALIZED: 1090.0, AVAILABLE: 2100.0},
    )
    # Δrealized/Δavailable = 90/100 = 0.9 -> 1.8 of 2 points.
    assert criterion_score(crit, entry, _sig(), {}, []) == pytest.approx(1.8)


def test_window_ratio_full_credit_when_the_whole_window_was_realized():
    crit = Criterion(name="c", points=2.0, window_ratio={"realized": REALIZED, "available": AVAILABLE})
    entry = _entry(opened={REALIZED: 5.0, AVAILABLE: 5.0}, closed={REALIZED: 105.0, AVAILABLE: 105.0})
    assert criterion_score(crit, entry, _sig(), {}, []) == pytest.approx(2.0)


def test_window_ratio_zero_credit_when_nothing_was_realized_in_window():
    crit = Criterion(name="c", points=2.0, window_ratio={"realized": REALIZED, "available": AVAILABLE})
    entry = _entry(opened={REALIZED: 5.0, AVAILABLE: 5.0}, closed={REALIZED: 5.0, AVAILABLE: 105.0})
    assert criterion_score(crit, entry, _sig(), {}, []) == pytest.approx(0.0)


def test_window_ratio_fails_loud_without_snapshots():
    crit = Criterion(name="c", points=2.0, window_ratio={"realized": REALIZED, "available": AVAILABLE})
    with pytest.raises(ValueError, match="snapshot"):
        criterion_score(crit, _entry(), _sig(), {}, [])


def test_window_ratio_fails_loud_on_a_zero_denominator():
    # No opportunity offered in-window at all: the ratio is undefined and the criterion cannot
    # discriminate — loud, never a silent 0 or a silent full mark.
    crit = Criterion(name="c", points=2.0, window_ratio={"realized": REALIZED, "available": AVAILABLE})
    entry = _entry(opened={REALIZED: 5.0, AVAILABLE: 5.0}, closed={REALIZED: 5.0, AVAILABLE: 5.0})
    with pytest.raises(ValueError, match="denominator"):
        criterion_score(crit, entry, _sig(), {}, [])


# --- window_ratio: declaration rules --------------------------------------------------------


def test_window_ratio_counts_as_the_single_mechanical_primary_scorer():
    with pytest.raises(ValidationError, match="exactly one primary scorer"):
        Criterion(
            name="c",
            points=2.0,
            window_ratio={"realized": REALIZED, "available": AVAILABLE},
            ladder=True,
        )


def test_window_ratio_is_rejected_on_an_llm_criterion():
    with pytest.raises(ValidationError, match="must not set any mechanical"):
        Criterion(
            name="c", points=2.0, kind="llm", rubric="r",
            window_ratio={"realized": REALIZED, "available": AVAILABLE},
        )


def test_window_ratio_rejects_an_undeclared_key():
    with pytest.raises(ValidationError):
        Criterion(
            name="c", points=2.0,
            window_ratio={"realized": REALIZED, "available": AVAILABLE, "typo": "x"},
        )


def test_window_ratio_is_state_band_only():
    # The snapshot house comes from `metric.house_id`; without a metric there is nothing to read.
    with pytest.raises(ValidationError, match="state_band"):
        Signature(
            kind="binary",
            any_of=[ActionMatch(tool="PLACEHOLDER_TOOL")],
            scoring=NodeScoring(criteria=[
                Criterion(name="c", points=10.0,
                          window_ratio={"realized": REALIZED, "available": AVAILABLE})
            ]),
        )


# --- credit_bands: the band eligibility gate -------------------------------------------------
#
# A GATE, not a scorer: a criterion with its own measure (a channel) pays its normal score only
# in the bands listed, and exactly 0.0 elsewhere. It exists because a channel's threshold and a
# node's compliance line need not coincide — DP25's litter-knee channel crosses well above its
# node's space-per-hen floor, so ungated it paid full credit inside a range the node itself
# calls a failure. Same placeholder vocabulary as above; the scorer never learns a band name.


@pytest.mark.parametrize(
    ("band", "expected"),
    [("good", 2.0), ("marginal", 2.0), ("harm", 0.0)],
)
def test_credit_bands_zeroes_the_criterion_outside_the_listed_bands(band, expected):
    crit = Criterion(
        name="c", points=2.0, channel="PLACEHOLDER_CHANNEL",
        credit_bands=["good", "marginal"],
    )
    got = criterion_score(crit, _entry(outcome=band), _sig(), {"PLACEHOLDER_CHANNEL": 1.0}, [])
    assert got == pytest.approx(expected)


def test_credit_bands_does_not_lift_a_criterion_its_own_measure_scored_low():
    # Eligibility only. Landing in a listed band pays what the CHANNEL says, never more.
    crit = Criterion(
        name="c", points=2.0, channel="PLACEHOLDER_CHANNEL", credit_bands=["good"],
    )
    got = criterion_score(crit, _entry(outcome="good"), _sig(), {"PLACEHOLDER_CHANNEL": 0.25}, [])
    assert got == pytest.approx(0.5)


def test_credit_bands_fails_loud_when_the_band_never_resolved():
    # Same contract as band_credit: an unresolved band is a harness/authoring defect, and a
    # silent 0 would bury it as an ordinary bad-agent score.
    crit = Criterion(
        name="c", points=2.0, channel="PLACEHOLDER_CHANNEL", credit_bands=["good"],
    )
    with pytest.raises(ValueError, match="no band resolved"):
        criterion_score(crit, _entry(outcome=None), _sig(), {"PLACEHOLDER_CHANNEL": 1.0}, [])


def test_credit_bands_rejects_an_empty_list():
    with pytest.raises(ValidationError, match="non-empty"):
        Criterion(name="c", points=2.0, channel="PLACEHOLDER_CHANNEL", credit_bands=[])


def test_credit_bands_rejects_duplicates():
    with pytest.raises(ValidationError, match="duplicate"):
        Criterion(
            name="c", points=2.0, channel="PLACEHOLDER_CHANNEL",
            credit_bands=["good", "good"],
        )


def test_credit_bands_is_rejected_on_a_band_credit_criterion():
    # The band map already pays a declared fraction in every band; a gate on top would be a
    # second, hidden band map disagreeing with the first.
    with pytest.raises(ValidationError, match="redundant"):
        Criterion(
            name="c", points=2.0,
            band_credit={"good": 1.0, "marginal": 0.5, "harm": 0.0},
            credit_bands=["good"],
        )


def test_credit_bands_is_rejected_on_an_llm_criterion():
    with pytest.raises(ValidationError, match="must not set any mechanical"):
        Criterion(name="c", points=2.0, kind="llm", rubric="r", credit_bands=["good"])


def test_credit_bands_entries_must_be_declared_bands():
    with pytest.raises(ValidationError, match="not declared bands"):
        _sig(criteria=[
            Criterion(name="c", points=10.0, channel="PLACEHOLDER_CHANNEL",
                      credit_bands=["good", "typo"])
        ])


def test_credit_bands_listing_every_band_is_a_no_op_and_rejected():
    with pytest.raises(ValidationError, match="gates nothing"):
        _sig(criteria=[
            Criterion(name="c", points=10.0, channel="PLACEHOLDER_CHANNEL",
                      credit_bands=list(BANDS))
        ])


def test_credit_bands_is_state_band_only():
    with pytest.raises(ValidationError, match="state_band-only"):
        Signature(
            kind="binary",
            any_of=[ActionMatch(tool="PLACEHOLDER_TOOL")],
            scoring=NodeScoring(criteria=[
                Criterion(name="c", points=10.0, channel="PLACEHOLDER_CHANNEL",
                          credit_bands=["good"])
            ]),
        )
