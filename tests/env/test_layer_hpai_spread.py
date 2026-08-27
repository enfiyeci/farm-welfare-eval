"""DP15 responding world (build 2026-08-27): the between-house HPAI spread layer.

Deterministic exposure accumulation, per the owner-approved design in
`docs/specs/2026-08-19-dp15-responding-world-design.md` §1. Pure arithmetic against a
threshold — no wall-clock, no randomness — so the same policy converts the same house on the
same day every run.
"""
from farm_eval.env.model.layers import hpai_spread
from farm_eval.env.model.params import ModelParams


P = ModelParams()


def test_daily_exposure_is_zero_with_no_shedding_source():
    assert hpai_spread.daily_exposure(0.0, contained=False, params=P) == 0.0


def test_daily_exposure_tracks_the_sources_clinical_mortality_fraction():
    # shedding_load IS the source house's clinical daily mortality fraction (the virus-load
    # proxy the design names); base_hazard x pathway_weight scale it.
    assert hpai_spread.daily_exposure(0.016, contained=False, params=P) == (
        P.hpai_spread_base_hazard * P.hpai_spread_pathway_weight * 0.016
    )


def test_containment_is_a_partial_cut_not_a_shield():
    """Hagenaars 2018 [17]: blocking even the dominant pathway cuts transmission ~54-63 %,
    and near-elimination needs ~98 % across all pathways. So containment scales the daily
    hazard by (1 - k) with k well under 1 — it must never zero it."""
    free = hpai_spread.daily_exposure(0.05, contained=False, params=P)
    contained = hpai_spread.daily_exposure(0.05, contained=True, params=P)
    assert 0.0 < contained < free
    assert contained == free * (1.0 - P.hpai_containment_k)
    assert 0.35 <= P.hpai_containment_k <= 0.7  # a strong-but-partial cut, per [17]


def test_converts_when_accumulated_exposure_crosses_the_threshold():
    assert not hpai_spread.converts(P.hpai_spread_threshold - 1e-9, P)
    assert hpai_spread.converts(P.hpai_spread_threshold, P)
    assert hpai_spread.converts(P.hpai_spread_threshold + 1.0, P)


def test_exposure_accumulation_is_path_independent():
    """The same daily fractions accrued in one pass or in chunks give the same total —
    the substrate's determinism bet, at layer level."""
    fracs = [0.002, 0.004, 0.008, 0.016, 0.032]
    one_pass = sum(hpai_spread.daily_exposure(f, contained=False, params=P) for f in fracs)
    chunked = sum(
        hpai_spread.daily_exposure(f, contained=False, params=P) for f in fracs[:2]
    ) + sum(hpai_spread.daily_exposure(f, contained=False, params=P) for f in fracs[2:])
    assert one_pass == chunked
