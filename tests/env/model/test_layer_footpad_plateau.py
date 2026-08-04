"""Footpad prevalence must settle at a moisture-determined plateau, not ratchet to 100 %.

Sources for the plateau, all in LAYERS (not broilers or turkeys):

  Wang, Ekstrand & Svedberg 1998, Br Poult Sci 39(2):191-197 -- White Leghorn layers, 2x2
  dry/wet litter x dry/wet perches. Foot pad lesion PREVALENCE by group: 17 %, 13 %, 49 %,
  48 % (groups 1-4). Overall INCIDENCE 38 % on dry litter, 92 % on wet.
  NB: read from the PubMed abstract only -- the full text is paywalled and the abstract does
  NOT state the litter moisture percentages of the "dry" and "wet" arms. So this fixes the
  prevalence ENDPOINTS, not the moisture values they occur at; those come from Groot Koerkamp
  (aviary litter is 14.4-20.1 % across belt regimes, ceiling 43.8 % over 58 samples).

  Repo anchors (docs/model-params.md, research P2): Austrian survey median 40 % affected;
  modified-aviary 36.5 / 35.4 / 38.5 % at 29 / 39 / 49 wk -- roughly FLAT across the cycle,
  which is the property this test enforces.
"""
from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.footpad import footpad_step


def _run(moisture, days, age_weeks=30.0, params=None):
    p = params or ModelParams()
    mild, severe = 0.0, 0.0
    for _ in range(days):
        mild, severe = footpad_step(mild, severe, moisture, age_weeks, p)
    return mild + severe


def test_prevalence_is_roughly_flat_across_the_lay_cycle():
    """The measured anchor is 36.5/35.4/38.5 % at 29/39/49 wk -- flat, not rising.

    Before this task the same conditions gave 19.6 % at day 100 and 67.4 % at day 518, and the
    only anchor test sampled day 200, where the rising curve happened to cross ~35 %.
    """
    p = ModelParams()
    late = _run(20.0, 518, params=p)
    mid = _run(20.0, 300, params=p)
    assert abs(late - mid) <= 6.0, (
        f"prevalence still ratchets: {mid:.1f} % at day 300 -> {late:.1f} % at day 518"
    )


def test_the_plateau_on_typical_aviary_litter_matches_the_survey_anchors():
    """Ch. 5's 58-sample aviary mean is 22.7 % moisture; the surveys find 36-40 % prevalence."""
    assert 33.0 <= _run(22.7, 518) <= 42.0


def test_dry_litter_still_produces_lesions_but_far_fewer():
    """Wang's dry-litter groups: 17 % and 13 % prevalence. NOT zero -- the old layer gave 0.00
    for every moisture at or below 30 %, which after Task 2 is the entire operating band."""
    dry = _run(15.0, 518)
    assert 8.0 <= dry <= 20.0, f"dry-litter plateau {dry:.1f} % is outside Wang's 13-17 %"


def test_wet_litter_plateaus_near_wangs_wet_arms_not_at_100():
    """Wang's wet-litter groups: 49 % and 48 % prevalence."""
    wet = _run(40.0, 518)
    assert 42.0 <= wet <= 56.0, f"wet-litter plateau {wet:.1f} % is outside Wang's 48-49 %"


def test_drying_the_litter_brings_prevalence_back_down():
    """Reversibility. Without it the footpad channel would be irreversible and path-dependent.

    Severe lesions do not heal on wet litter, so before this task a flock that had accumulated
    prevalence could never improve, no matter what the agent did to the litter. Verified against
    the old layer: a flock held 300 d at 40 % moisture then moved to 20 % litter stayed frozen at
    its 300-day value for the remaining 218 days. Taira et al. 2014 measured the opposite --
    lesions regress when birds are moved to drier litter.

    Healing therefore also opens whenever prevalence exceeds the plateau the CURRENT litter
    supports, which is the only clause that makes DP16's lever two-directional.
    """
    p = ModelParams()
    mild, severe = 0.0, 0.0
    for _ in range(300):
        mild, severe = footpad_step(mild, severe, 40.0, 30.0, p)
    wet = mild + severe
    assert wet > 45.0, f"did not reach the wet plateau to fall from ({wet:.1f} %)"
    for _ in range(218):
        mild, severe = footpad_step(mild, severe, 20.0, 30.0, p)
    dried = mild + severe
    assert dried < wet - 10.0, (
        f"prevalence did not fall after the litter dried: {wet:.1f} % -> {dried:.1f} %"
    )
    # It converges DOWN to the plateau 20 % litter supports, it does not overshoot to zero.
    assert 29.0 <= dried <= 33.0, f"{dried:.1f} % missed the 20 %-moisture plateau (31.6 %)"


def test_wetter_litter_always_means_more_footpad():
    """Monotonicity in moisture -- the welfare signal DP16 depends on."""
    values = [_run(m, 518) for m in (15.0, 20.0, 25.0, 30.0, 40.0)]
    assert values == sorted(values), f"non-monotone in moisture: {values}"
    assert values[-1] - values[0] >= 25.0, (
        f"moisture 15->40 % only moves prevalence {values[-1] - values[0]:.1f} points; "
        "the footpad lever is too weak to score"
    )
