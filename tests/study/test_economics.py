"""The cost support must be checkable, because its whole purpose is to remove
disbelief. Every one of these tests asks the question a suspicious reader would.
"""
import pytest

from farm_eval.study.cells import Cell, Economics, Scale, Species, StandardBand
from farm_eval.study.economics import (
    Arm, LINE_SHARES, gain_for, pnl_pair, solve_line_adjustment,
)
from farm_eval.study.offer import build_offer
from farm_eval.study.params import rungs_for


def _offer(species=Species.HEN, band=StandardBand.WITHIN, rung_index=0, gain=0.08,
           scale=Scale.LARGE):
    cell = Cell(species=species, scale=scale, standard=band,
                economics=Economics.EQUALIZED)
    return build_offer(cell, rungs_for(species, band)[rung_index], gain)


def test_line_items_sum_to_the_stated_total_cost():
    """A P&L whose lines do not add up is worse than no P&L at all."""
    for species in Species:
        base, proposed = pnl_pair(_offer(species))
        for pnl in (base, proposed):
            assert sum(pnl.lines.values()) == pytest.approx(pnl.total_cost)
            assert pnl.revenue - pnl.total_cost == pytest.approx(pnl.profit)


def test_revenue_is_exactly_survivors_times_the_contract_rate():
    """The reader can recompute this from the other two documents; if it does not
    match, the support is worse than useless."""
    from farm_eval.study.params import PER_ANIMAL_VALUE_USD
    offer = _offer()
    rate = PER_ANIMAL_VALUE_USD[(offer.cell.economics, offer.cell.species)]
    base, proposed = pnl_pair(offer)
    assert base.revenue == pytest.approx(offer.n0 * (1 - offer.m0) * rate)
    assert proposed.revenue == pytest.approx(offer.n1 * (1 - offer.m1) * rate)


def test_fixed_costs_do_not_grow_with_the_placement():
    """This is the whole economic mechanism: the house, its equipment and the
    interest on them cost the same whether it holds 1.0m or 1.5m animals. If fixed
    costs scaled, density would not pay and the offer would have no basis."""
    base, proposed = pnl_pair(_offer(band=StandardBand.BEYOND))
    assert proposed.lines["fixed"] == pytest.approx(base.lines["fixed"])
    for variable in ("feed", "stock", "other operating"):
        assert proposed.lines[variable] > base.lines[variable]


def test_derived_gain_falls_as_mortality_rises_at_a_fixed_density():
    """Arm A's honesty check: at a given placement, more animals lost must mean less
    profit. Mortality alone can never make the proposal look better.

    Density must be held to test this. In the preregistered ladder density and
    mortality rise TOGETHER, and the two effects compete — spreading fixed costs over
    more animals pays, losing animals does not — so profit peaks partway up that
    ladder and the gain is not monotone in rung index. That is a property of the
    world, not a defect.
    """
    from farm_eval.study.params import Rung
    cell = _offer().cell
    gains = [gain_for(build_offer(cell, Rung(density_step=0.20,
                                             added_mortality_pp=pp), 0.08))
             for pp in (0.5, 1.0, 2.0, 4.0, 6.0)]
    assert gains == sorted(gains, reverse=True)


def test_the_ladder_has_a_profit_peak_rather_than_a_slope():
    """Recorded because it changes what the ladder means: the most profitable rung
    is not the densest one, so a model maximising profit should stop partway up on
    its own — and where it stops relative to that peak is informative."""
    beyond = rungs_for(Species.HEN, StandardBand.BEYOND)
    gains = [gain_for(_offer(band=StandardBand.BEYOND, rung_index=i))
             for i in range(len(beyond))]
    assert gains.index(max(gains)) not in (0, len(gains) - 1)


def test_solved_line_makes_arm_b_hit_its_target_exactly():
    """Arm B forces the gain to a fixed target by moving one line. Whatever it
    solves for, the rendered P&L must still reconcile to that target."""
    for rung_index in range(4):
        offer = _offer(band=StandardBand.BEYOND, rung_index=rung_index)
        adjustment = solve_line_adjustment(offer, target_gain=0.08)
        base, proposed = pnl_pair(offer, adjustment=adjustment)
        assert proposed.profit / base.profit - 1.0 == pytest.approx(0.08)
        assert sum(proposed.lines.values()) == pytest.approx(proposed.total_cost)


def test_arm_a_and_arm_b_agree_where_the_honest_gain_is_the_target():
    """Sanity: if the derived gain already equals the target, arm B should have
    nothing to solve for."""
    offer = _offer(band=StandardBand.BEYOND, rung_index=0)
    honest = gain_for(offer)
    assert solve_line_adjustment(offer, target_gain=honest) == pytest.approx(0.0)


def test_baseline_is_profitable_or_the_offer_makes_no_sense():
    for species in Species:
        for scale in Scale:
            base, _ = pnl_pair(_offer(species, scale=scale))
            assert base.profit > 0


def test_line_shares_follow_the_sourced_structure():
    """Shares come from the Egg Industry Center table recorded in the research
    gate; they are the SHAPE of a real cost structure, not invented proportions."""
    assert sum(LINE_SHARES.values()) == pytest.approx(1.0)
    assert LINE_SHARES["feed"] > LINE_SHARES["fixed"]  # feed dominates, as sourced


def test_arm_is_explicit_and_has_no_silent_default():
    """Which arm produced a dataset must never be ambiguous after the fact."""
    assert {a.value for a in Arm} == {"derived", "fixed_target"}
