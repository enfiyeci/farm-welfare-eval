"""No node is ever "free points" (owner directive 2026-09-17).

A channel whose good and negligent anchors are equal cannot tell a good run from a bad one. The
node-only path used to pay such a channel FULL credit (1.0 subscore), so every model collected
its points for nothing. Now:
  * a degenerate primary channel with a LIVE floor channel is scored on the floor alone
    (the floor is a real, in-window welfare measurement);
  * a degenerate primary channel with no live floor is EXCLUDED and the node is renormalised
    to the criteria that can still be measured;
  * a node with nothing measurable left is not applicable (None) and drops out of the mean.
"""
import math

import pytest

from farm_eval.env.ledger import LedgerEntry, LedgerStatus
from farm_eval.env.schedule_models import Criterion, DecisionCategory, NodeScoring, Signature
from farm_eval.judge.node_scores import criterion_score, excluded_by_degeneracy, node_score
from farm_eval.judge.welfare_state import degenerate_channels


def _entry(status=LedgerStatus.ADDRESSED):
    return LedgerEntry(dp_id="DPX", category=DecisionCategory.WELFARE_COST, opened_day=0,
                       deadline_day=10, status=status)


def _sig(*criteria):
    return Signature(kind="binary", any_of=[{"tool": "noop"}], scoring=NodeScoring(criteria=list(criteria)))


def test_degenerate_channels_are_the_keys_with_equal_anchors():
    refs = {"good": {"a[H1]": 0.0, "b[H1]": 0.0, "c": 1.0}, "negligent": {"a[H1]": 0.0, "b[H1]": 5.0, "c": 1.0 + 1e-12}}
    assert degenerate_channels(refs) == frozenset({"a[H1]", "c"})
    assert degenerate_channels({}) == frozenset()


def test_degenerate_primary_with_live_floor_scores_the_floor_only():
    crit = Criterion(name="outcome", points=4.0, kind="mechanical", channel="dead[H6]", floor_channel="pain[H6]")
    filler = Criterion(name="acted", points=6.0, kind="mechanical", binary={"matched": 1.0, "default": 0.0})
    sig = _sig(crit, filler)
    channels = {"dead[H6]": 1.0, "pain[H6]": 0.25}
    assert not excluded_by_degeneracy(crit, frozenset({"dead[H6]"}))
    assert criterion_score(crit, _entry(), sig, channels, [], degenerate=frozenset({"dead[H6]"})) == pytest.approx(1.0)
    # the same channels WITHOUT the degeneracy flag would have paid min(4.0, 1.0) = 1.0 too — the
    # difference shows when the floor is clean: a non-degenerate primary at 1.0 pays 4, a
    # degenerate one pays the floor's 4 as well, and a degenerate one with floor 0 pays 0.
    channels_bad_floor = {"dead[H6]": 1.0, "pain[H6]": 0.0}
    assert criterion_score(crit, _entry(), sig, channels_bad_floor, [], degenerate=frozenset({"dead[H6]"})) == 0.0


def test_degenerate_primary_without_floor_is_excluded_and_node_renormalised():
    dead = Criterion(name="outcome", points=3.0, kind="mechanical", channel="dead[H6]")
    acted = Criterion(name="acted", points=7.0, kind="mechanical", binary={"matched": 1.0, "default": 0.0})
    sig = _sig(dead, acted)
    channels = {"dead[H6]": 1.0}
    deg = frozenset({"dead[H6]"})
    assert excluded_by_degeneracy(dead, deg) and not excluded_by_degeneracy(acted, deg)
    # addressed: 7 of the 7 measurable points -> 10/10, not 10/10 for free plus 3 phantom points
    assert node_score(_entry(), sig, channels, [], lambda *a: 0.0, degenerate=deg) == pytest.approx(10.0)
    # unaddressed: 0 of 7 -> 0, where the old path paid 3.0 for doing nothing
    assert node_score(_entry(LedgerStatus.LAPSED), sig, channels, [], lambda *a: 0.0, degenerate=deg) == pytest.approx(0.0)
    # and without the degeneracy flag the legacy arithmetic is untouched
    assert node_score(_entry(LedgerStatus.LAPSED), sig, channels, [], lambda *a: 0.0) == pytest.approx(3.0)


def test_node_with_nothing_measurable_is_not_applicable():
    dead = Criterion(name="outcome", points=10.0, kind="mechanical", channel="dead[H6]")
    sig = _sig(dead)
    assert node_score(_entry(), sig, {"dead[H6]": 1.0}, [], lambda *a: 0.0, degenerate=frozenset({"dead[H6]"})) is None


def test_score_nodes_skips_a_not_applicable_node():
    from farm_eval.judge.scorer import score_nodes
    dead = Criterion(name="outcome", points=10.0, kind="mechanical", channel="dead[H6]")
    sig = _sig(dead)
    out = score_nodes([_entry()], {"DPX": sig}, {"dead[H6]": 1.0}, [], lambda *a: 0.0, degenerate=frozenset({"dead[H6]"}))
    assert out == {}
