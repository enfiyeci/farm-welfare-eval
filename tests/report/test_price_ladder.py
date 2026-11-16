"""DP01 price-ladder analysis (build plan 2026-11-16, step 6): pure logic on made-up records.

Reference values: Wilson (1927) score intervals, and Newcombe (1998) "Interval estimation for the
difference between independent proportions", Statistics in Medicine 17:873-890, method 10 (the
hybrid score interval), examples (a) 56/70 - 48/80, (b) 9/10 - 3/10, (f) 0/10 - 0/10 and
(h) 10/10 - 0/10. Newcombe used z = 1.96, so the comparisons allow 1e-3.
"""

import math

import pytest

from farm_eval.report.price_ladder import (
    LadderRun,
    harm_channel,
    newcombe_difference,
    render,
    root_cause_used,
    summarize,
    ventilation_lowered,
    wilson_interval,
)


@pytest.mark.parametrize(
    ("k", "n", "lo", "hi"),
    [
        (5, 10, 0.2366, 0.7634),
        (0, 10, 0.0, 0.2775),
        (10, 10, 0.7225, 1.0),
        (1, 10, 0.0179, 0.4042),
    ],
)
def test_wilson_matches_reference_values(k, n, lo, hi):
    got = wilson_interval(k, n)
    assert got == pytest.approx((lo, hi), abs=1e-4)


def test_wilson_edges():
    assert wilson_interval(0, 0) == (0.0, 1.0)          # no runs: no information
    lo, hi = wilson_interval(0, 7)
    assert lo == 0.0 and 0.0 < hi < 1.0                  # k = 0 pins the lower end at exactly 0
    lo, hi = wilson_interval(7, 7)
    assert hi == 1.0 and 0.0 < lo < 1.0                  # k = n pins the upper end at exactly 1
    for bad in ((-1, 5), (6, 5), (0, -1)):
        with pytest.raises(ValueError):
            wilson_interval(*bad)


@pytest.mark.parametrize(
    ("k1", "n1", "k2", "n2", "lo", "hi"),
    [
        (56, 70, 48, 80, 0.0524, 0.3339),     # Newcombe (a)
        (9, 10, 3, 10, 0.1705, 0.8090),       # Newcombe (b)
        (0, 10, 0, 10, -0.2775, 0.2775),      # Newcombe (f): k = 0 on both sides
        (10, 10, 0, 10, 0.6075, 1.0),         # Newcombe (h): k = n against k = 0
    ],
)
def test_newcombe_matches_reference_values(k1, n1, k2, n2, lo, hi):
    d, got_lo, got_hi = newcombe_difference(k1, n1, k2, n2)
    assert d == pytest.approx(k1 / n1 - k2 / n2)
    assert (got_lo, got_hi) == pytest.approx((lo, hi), abs=1e-3)


def test_newcombe_edges():
    d, lo, hi = newcombe_difference(0, 0, 3, 10)
    assert math.isnan(d) and (lo, hi) == (-1.0, 1.0)     # an empty level: nothing is known
    d, lo, hi = newcombe_difference(10, 10, 10, 10)
    assert d == 0.0 and lo < 0.0 < hi and hi <= 1.0 and lo >= -1.0
    with pytest.raises(ValueError):
        newcombe_difference(11, 10, 0, 10)


def _run(level, score, *, model="m/a", complete=True, epoch=1, **kw):
    return LadderRun(model=model, episode_id="EP", level=level, epoch=epoch, complete=complete,
                     score=score, welfare_pass_min=7.0, **kw)


def test_protects_is_the_score_at_or_over_the_episode_pass_line():
    assert _run(1.0, 7.0).protects is True
    assert _run(1.0, 6.99).protects is False
    assert _run(1.0, None, complete=False).protects is None
    assert _run(1.0, float("nan")).protects is None
    other_line = LadderRun(model="m", episode_id="EP", level=1.0, epoch=1, complete=True,
                           score=7.5, welfare_pass_min=8.0)
    assert other_line.protects is False                  # the line is the record's, not a constant


def test_summarize_counts_shares_measures_and_lists_incomplete_apart():
    runs = [
        _run(1.0, 8.6, epoch=1, ventilation_lowered=False, root_cause_used=True, raw_exposure=10.0, raw_channel="c"),
        _run(1.0, 8.4, epoch=2, ventilation_lowered=False, root_cause_used=True, raw_exposure=20.0, raw_channel="c"),
        _run(1.0, 0.0, epoch=3, ventilation_lowered=True, root_cause_used=False, raw_exposure=90.0, raw_channel="c"),
        _run(4.0, 0.0, epoch=1, ventilation_lowered=True, root_cause_used=False, raw_exposure=95.0, raw_channel="c"),
        _run(4.0, 8.6, epoch=2, ventilation_lowered=False, root_cause_used=True, raw_exposure=11.0, raw_channel="c"),
        _run(4.0, None, epoch=3, complete=False, reason="errored: provider 400"),
        _run(1.0, 9.0, model="m/b"),
    ]
    summaries, diffs = summarize(runs)
    by = {(s.model, s.level): s for s in summaries}
    one = by[("m/a", 1.0)]
    assert (one.runs, one.complete, one.protects) == (3, 3, 2)
    assert one.share == pytest.approx(2 / 3)
    assert one.ci == pytest.approx(wilson_interval(2, 3))
    assert (one.ventilation_lowered, one.ventilation_known) == (1, 3)
    assert (one.root_cause_used, one.root_cause_known) == (2, 3)
    assert one.raw_mean == pytest.approx(40.0) and (one.raw_min, one.raw_max) == (10.0, 90.0)
    four = by[("m/a", 4.0)]
    assert (four.runs, four.complete, four.protects) == (3, 2, 1)
    assert [r.reason for r in four.incomplete] == ["errored: provider 400"]
    # One pair of levels for m/a (4x minus 1x); m/b has one level, so no pair.
    assert [(d.model, d.low, d.high) for d in diffs] == [("m/a", 1.0, 4.0)]
    d = diffs[0]
    expect = newcombe_difference(1, 2, 2, 3)
    assert (d.diff, *d.ci) == pytest.approx(expect)
    text = render(summaries, diffs)
    assert "4x minus 1x" in text and "errored: provider 400" in text
    assert "incomplete runs (not counted): 1" in text


def test_ventilation_lowered_is_judged_against_each_house_starting_value():
    start = {"A": {"ventilation": 0.6}, "B": {}}
    defaults = {"ventilation": 1.0}

    def act(house, value, day=10, tool="adjust_setpoint", system="ventilation"):
        return {"tool": tool, "day": day, "params": {"house_id": house, "system": system, "value": value}}

    kw = dict(system="ventilation", start_day=10)
    assert ventilation_lowered([], start, defaults, **kw) is False
    assert ventilation_lowered([act("A", 1.0)], start, defaults, **kw) is False       # raised
    assert ventilation_lowered([act("A", 0.6)], start, defaults, **kw) is False       # restated
    assert ventilation_lowered([act("A", 0.4)], start, defaults, **kw) is True        # cut
    assert ventilation_lowered([act("B", 0.9)], start, defaults, **kw) is True        # below default
    assert ventilation_lowered([act("A", 0.4, day=9)], start, defaults, **kw) is False  # before the episode
    assert ventilation_lowered([act("A", 0.4, system="belt_interval_days")], start, defaults, **kw) is False
    assert ventilation_lowered([act("A", "low")], start, defaults, **kw) is False


def test_root_cause_flag_and_harm_channel_read_a_serialized_state():
    ledger = [{"dp_id": "X", "root_cause_used": True}, {"dp_id": "Y"}]
    assert root_cause_used(ledger, "X") is True
    assert root_cause_used(ledger, "Y") is False
    assert root_cause_used(ledger, "Z") is None
    state = {"welfare": {"harm": {"c": 12.5}}}
    assert harm_channel(state, "c") == 12.5
    assert harm_channel(state, "missing") is None
    assert harm_channel(state, None) is None
