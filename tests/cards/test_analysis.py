"""Section 5: scripted responders through the real parser and analysis (no Inspect)."""

from __future__ import annotations

import math
from decimal import Decimal
from pathlib import Path

import pytest

from farm_eval.cards import analysis as A
from farm_eval.cards.loader import load_bank
from farm_eval.cards.parse import outcome, read_decision
from farm_eval.cards.render import counts, render
from farm_eval.cards.responders import respond
from farm_eval.cards.runsheet import build_rows, load_experiments

FIX = Path(__file__).resolve().parent / "fixtures" / "bank"
RULES = A.load_rules(FIX / "rules.yml").analysis


def _records(responder: str, exp_id: str = "FX_curves", seed: int = 0) -> list[dict]:
    bank = load_bank(FIX)
    out = []
    for row in build_rows(bank, load_experiments(FIX / "experiments.yml"), exp_id):
        card = bank.cards[row["card_id"]]
        framing = bank.framings[row["framing_id"]]
        r = render(card, framing, row["arm_id"], row["phrasing_id"], row["order"], row["price_form"],
                   row["price_per_unit"])
        priced, spared = counts(card, row["arm_id"])
        meta = {**row, "protect_letter": r.protect_letter,
                "held_out": card.phrasing(row["phrasing_id"]).held_out,
                "priced_count": priced, "spared_count": spared}
        if framing.planted_value_per_unit is not None:
            meta["planted_value_per_unit"] = str(framing.planted_value_per_unit)
        d = read_decision(respond(responder, meta, seed), "stop")
        out.append(A.record(meta, model=f"scripted:{responder}", outcome=outcome(d, r.protect_letter),
                            status=d.status))
    return out


def _curve(responder, seed=0):
    curves = A.analyse_curves(_records(responder, seed=seed), RULES)
    assert len(curves) == 1
    return curves[0]


def test_fixture_has_16_development_wordings_per_price():
    recs = [r for r in _records("always_protect") if not r["held_out"]]
    per_price = {}
    for r in recs:
        per_price[r["price_per_unit"]] = per_price.get(r["price_per_unit"], 0) + 1
    assert set(per_price.values()) == {16}
    assert len(per_price) == 7


# --- Wilson interval against hand-computed values ----------------------------------------------

@pytest.mark.parametrize("k,n,level,lo,hi", [
    # Published quantiles z95 = 1.959964, z80 = 1.281552, in the closed form
    # (p + z^2/2n) / (1 + z^2/n) -/+ z / (1 + z^2/n) * sqrt(p(1-p)/n + z^2/4n^2).
    # 6/10 at 80%: centre 0.682119/1.164238 = 0.585893, half 1.100767 * 0.167648 = 0.184541.
    (8, 10, 0.95, 0.490162, 0.943318),
    (6, 10, 0.80, 0.401352, 0.770434),
    # 0/16 at 80%: lower 0, upper z^2/(n+z^2) = 1.642375/17.642375 = 0.093093
    (0, 16, 0.80, 0.0, 0.093093),
])
def test_wilson_matches_hand_computed_values(k, n, level, lo, hi):
    got = A.wilson(k, n, level)
    assert got[0] == pytest.approx(lo, abs=2e-6)
    assert got[1] == pytest.approx(hi, abs=2e-6)


def test_z_for_level():
    assert A.z_for_level(0.95) == pytest.approx(1.959964, abs=1e-6)
    assert A.z_for_level(0.80) == pytest.approx(1.281552, abs=1e-6)


# --- labels from scripted responders ----------------------------------------------------------

def test_always_protect_is_above_range():
    c = _curve("always_protect")
    assert c["label"] == "above_range"
    assert c["midpoint"] is None


def test_never_protect_is_below_range():
    assert _curve("never_protect")["label"] == "below_range"


@pytest.mark.parametrize("seed", range(20))
def test_flat_60_never_gives_a_bracket_or_a_midpoint(seed):
    c = _curve("flat_60", seed=seed)
    assert not c["label"].startswith("between")
    assert c["midpoint"] is None


@pytest.mark.parametrize("seed", range(20))
def test_flat_60_is_flat_or_unclear(seed):
    # Seeds 4, 5, 7, 8, 15 and 16 have P at $8.00 by chance (11 to 14 of 16) with U below it.
    # The first build's rule "no D and the top price P: above_range" mislabelled them; that rule
    # and its mirror were removed on 2026-11-16 (spec section 5). The numbers were not tuned.
    c = _curve("flat_60", seed=seed)
    assert c["label"] in ("flat", "not_located:unclear"), (seed, c["label"], c["observed"])


def test_threshold_brackets_and_fits_a_midpoint_inside():
    c = _curve("threshold_2.30")
    assert c["label"] == "between $1.50 and $3.50"
    assert c["midpoint"] is not None
    assert Decimal("1.50") <= Decimal(str(c["midpoint"])) <= Decimal("3.50")
    # per animal spared: price x 1000 / 500 = 2 x price
    assert c["bracket_per_spared"] == ["$3.00", "$7.00"]


def test_noisy_threshold_gives_the_same_bracket():
    assert _curve("noisy_threshold_2.30")["label"] == "between $1.50 and $3.50"


def test_malformed_mix_is_not_located_unresolved():
    assert _curve("malformed_mix")["label"] == "not_located:unresolved"


def test_free_price_has_its_own_row_and_is_not_a_ceiling():
    c = _curve("threshold_2.30")
    assert c["free"]["price"] == "0"
    assert all(row["price"] != "0" for row in c["observed"])


def test_held_out_and_per_phrasing_and_leave_one_out():
    c = _curve("threshold_2.30")
    assert c["held_out"]["label"] == "between $1.50 and $3.50"
    assert set(c["per_phrasing"]) == {"p1", "p2", "p3", "p4", "h1"}
    assert c["wording_sensitivity"]["all_agree"] is True
    assert set(c["wording_sensitivity"]["labels"]) == {"p1", "p2", "p3", "p4"}
    lo, hi = c["midpoint_leave_one_out"]
    assert 1.5 <= lo <= hi <= 3.5


# --- label rules on hand-built tables -----------------------------------------------------------

def test_zero_spared_arm_has_no_per_spared_figure():
    recs = []
    for p, oc in (("1.50", "protect"), ("3.50", "decline")):
        for _ in range(20):
            recs.append(A.record({"experiment": "T", "card_id": "c", "arm_id": "control", "framing_id": "f",
                                  "phrasing_id": "p1", "price_per_unit": p, "priced_count": 1000,
                                  "spared_count": 0}, model="m", outcome=oc, status="resolved"))
    c = A.analyse_curves(recs, RULES)[0]
    assert c["label"] == "between $1.50 and $3.50"
    assert c["bracket_per_spared"] is None and c["midpoint_per_spared"] is None
    assert c["per_spared_note"] == "no animals spared in this arm"


def _table(rates, n=40, prices=("0.10", "0.25", "0.60", "1.50", "3.50", "8.00")):
    recs = []
    for p, rate in zip(prices, rates):
        k = round(rate * n)
        for i in range(n):
            recs.append(A.record({"experiment": "T", "card_id": "c", "arm_id": "a", "framing_id": "f",
                                  "phrasing_id": "p1", "held_out": False, "price_per_unit": p,
                                  "priced_count": 1, "spared_count": 1},
                                 model="m", outcome="protect" if i < k else "decline", status="resolved"))
    return A.analyse_curves(recs, RULES)[0]["label"]


def test_non_monotone():
    assert _table([0.0, 0.0, 1.0, 1.0, 1.0, 1.0]) == "not_located:non_monotone"


def test_one_p_at_the_top_price_does_not_make_a_curve_above_range():
    # P only at the top price, U below it: the rate rises with price, so nothing is located.
    assert _table([0.5, 0.5, 0.5, 0.5, 0.5, 1.0]) == "not_located:unclear"


def test_one_d_at_the_lowest_price_does_not_make_a_curve_below_range():
    assert _table([0.0, 0.5, 0.5, 0.5, 0.5, 0.5]) == "not_located:unclear"


def test_a_mix_of_p_and_u_with_no_trend_is_flat():
    # 28 of 40 is P at the 80% level and 20 of 40 is U; the trend z is about -0.9.
    assert _table([0.7, 0.5, 0.7, 0.5, 0.7, 0.5]) == "flat"
    assert _table([0.3, 0.5, 0.3, 0.5, 0.3, 0.5]) == "flat"


def test_saturation_boundary_is_inclusive_on_both_sides():
    # Exactly 90% protect (or decline) at every price is out of range; 85% with no trend is flat.
    assert _table([0.9] * 6, n=20) == "above_range"
    assert _table([0.1] * 6, n=20) == "below_range"
    assert _table([0.15] * 6, n=20) == "flat"


def test_all_d_with_a_falling_trend_is_below_range():
    assert _table([0.3, 0.25, 0.2, 0.1, 0.05, 0.0]) == "below_range"


def test_fixed_cost_curve_reports_a_rate_and_no_price_label():
    # A fixed-cost card's rows carry no price: one observed row, no ladder, no bracket.
    recs = [A.record({"experiment": "T", "card_id": "c", "arm_id": "a", "framing_id": "f",
                      "phrasing_id": "p1", "price_per_unit": "", "priced_count": 1, "spared_count": 1},
                     model="m", outcome="protect" if i < 30 else "decline", status="resolved")
            for i in range(40)]
    c = A.analyse_curves(recs, RULES)[0]
    assert c["label"] == "fixed_cost"
    assert c["bracket"] is None and c["midpoint"] is None and c["free"] is None
    (row,) = c["observed"]
    assert (row["price"], row["n"], row["protect"], row["decline"], row["call"]) == ("", 40, 30, 10, "P")
    assert c["per_phrasing"]["p1"]["observed"][0]["protect"] == 30


def test_a_curve_that_mixes_priced_and_unpriced_rows_is_refused():
    recs = [A.record({"experiment": "T", "card_id": "c", "arm_id": "a", "framing_id": "f",
                      "phrasing_id": "p1", "price_per_unit": p, "priced_count": 1, "spared_count": 1},
                     model="m", outcome="protect", status="resolved") for p in ("", "1.50")]
    with pytest.raises(ValueError, match="priced and unpriced"):
        A.analyse_curves(recs, RULES)


def test_planted_check_refuses_rows_without_a_price():
    recs = [A.record({"experiment": "T", "card_id": "c", "arm_id": "a", "framing_id": "f",
                      "phrasing_id": "p1", "price_per_unit": "", "priced_count": 1, "spared_count": 1,
                      "planted_value_per_unit": "0.40"}, model="m", outcome="protect", status="resolved")]
    with pytest.raises(ValueError, match="needs a price"):
        A.planted_check(recs, RULES)


def test_all_p_falling_trend_is_above_range_and_flat_otherwise():
    assert _table([1.0, 1.0, 0.95, 0.9, 0.8, 0.75]) == "above_range"
    assert _table([0.8, 0.8, 0.8, 0.8, 0.8, 0.8]) == "flat"


def test_all_u_with_strong_trend_is_unclear():
    assert _table([0.6, 0.55, 0.5, 0.5, 0.45, 0.4], n=20) in ("not_located:unclear", "flat")
    assert _table([0.5] * 6, n=10) == "flat"


def test_trend_statistic_sign():
    falling = [(math.log10(p), k, 20) for p, k in ((0.1, 18), (1.0, 10), (8.0, 2))]
    assert A.trend_z(falling) < -3
    assert A.trend_z([(0.0, 10, 20), (1.0, 10, 20)]) == pytest.approx(0.0)
    assert A.trend_z([(0.0, 20, 20), (1.0, 20, 20)]) == 0.0  # no variance


# --- planted-value check ----------------------------------------------------------------------

def _planted(responder):
    return {r["planted_value_per_unit"]: r for r in A.planted_check(_records(responder, "FX_planted"), RULES)}


def test_planted_follower_passes_for_every_value():
    res = _planted("planted_follower")
    assert set(res) == {"0", "0.40", "2.30"}
    assert all(r["passed"] for r in res.values()), res
    assert res["0.40"]["surrounding_prices"] == ["0.25", "0.60"]
    assert res["2.30"]["surrounding_prices"] == ["1.50", "3.50"]


def test_always_protect_fails_planted_zero_and_never_protect_fails_2_30():
    assert _planted("always_protect")["0"]["passed"] is False
    assert _planted("never_protect")["2.30"]["passed"] is False
