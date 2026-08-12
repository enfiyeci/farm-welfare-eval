from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.feather import (
    feather_damage_pct,
    feather_rate_multiplier,
    feather_step,
    pecking_mortality_frac,
)


def test_feather_anchors():
    p = ModelParams()
    assert feather_damage_pct(28.0, p) == 0.0
    assert abs(feather_damage_pct(31.0, p) - 3.2) < 2.0
    assert abs(feather_damage_pct(46.0, p) - 32.9) < 3.0
    assert abs(feather_damage_pct(65.0, p) - 57.8) < 3.0


def test_feather_monotone():
    p = ModelParams()
    prev = -1.0
    for wk in range(28, 101):
        v = feather_damage_pct(float(wk), p)
        assert prev <= v <= 100.0
        prev = v


# --- Stateful step (D11: mitigation inputs bend the age-only curve) ---


def _integrate_daily(start_age_wk: float, days: int, multiplier: float, p: ModelParams) -> float:
    """Drive feather_step day by day from a clean flock at start_age_wk.

    Mirrors the integrator: each day d is stepped with its day-END age
    (start + (d+1)/7), and the step accrues the increment over THAT day.
    """
    pct = 0.0
    for d in range(days):
        pct = feather_step(pct, start_age_wk + (d + 1) / 7.0, multiplier, p)
    return pct


def test_feather_step_neutral_reproduces_age_curve():
    # A flock placed pre-curve (17 wk, H4's start age) integrated at multiplier 1.0
    # must land ON the anchor curve — the stateful step telescopes to the interp.
    p = ModelParams()
    for probe_wk in (31.0, 46.0, 65.0, 80.0):
        days = int(round((probe_wk - 17.0) * 7))
        got = _integrate_daily(17.0, days, 1.0, p)
        assert abs(got - feather_damage_pct(probe_wk, p)) < 1e-6


def test_feather_step_accrues_the_day_that_ended_not_the_next():
    # Codex D11 round-1 F5: the integrator hands feather_step the day-END age, so the
    # step must cover [age - 1 day, age] — NOT [age, age + 1 day]. A 17-wk flock at
    # day 91 is exactly 30.0 wk (the curve's zero anchor) and must still read 0%;
    # the forward-difference bug read 0.457% (one day of the next week's slope).
    p = ModelParams()
    assert _integrate_daily(17.0, 91, 1.0, p) == 0.0
    # And the day-154 value (age 39 wk) is the interp value 19.04, not 19.32.
    day154 = _integrate_daily(17.0, 154, 1.0, p)
    assert abs(day154 - feather_damage_pct(39.0, p)) < 1e-6


def test_feather_step_is_irreversible():
    # Feathers do not regrow mid-cycle: even a total-suppression multiplier only
    # freezes the damage, it never reduces it.
    p = ModelParams()
    frozen = feather_step(40.0, 50.0, 0.0, p)
    assert frozen == 40.0


def test_feather_step_mitigation_slows_accrual():
    # Halving the rate through the steep 31-46 wk phase accrues about half the damage.
    p = ModelParams()
    days = int(round((46.0 - 31.0) * 7))
    full = _integrate_daily(31.0, days, 1.0, p)
    half = _integrate_daily(31.0, days, 0.5, p)
    assert 0.45 * full < half < 0.55 * full


def test_feather_step_clamps_to_100():
    p = ModelParams()
    assert feather_step(99.9, 46.0, 50.0, p) <= 100.0


# --- Rate multiplier (enrichment / methionine / lighting) ---


def test_rate_multiplier_neutral_is_one():
    p = ModelParams()
    m = feather_rate_multiplier(
        p, enrichment_installed=False, methionine_ration=False, lighting_lux=20.0
    )
    assert m == 1.0


def test_rate_multiplier_enrichment_halves_rate():
    # Mens/Guinebretière 2020: rearing-to-lay enrichment roughly halves injurious
    # pecking (mortality 11.48% -> 6.30%) — the enrichment factor is ~0.5.
    p = ModelParams()
    m = feather_rate_multiplier(
        p, enrichment_installed=True, methionine_ration=False, lighting_lux=20.0
    )
    assert abs(m - 0.5) < 0.11


def test_rate_multiplier_methionine_reduces_rate():
    # Met+Cys deficiency is a documented pecking driver; supplementation is a
    # second-line mitigation — weaker than enrichment, but real.
    p = ModelParams()
    m = feather_rate_multiplier(
        p, enrichment_installed=False, methionine_ration=True, lighting_lux=20.0
    )
    enrich = feather_rate_multiplier(
        p, enrichment_installed=True, methionine_ration=False, lighting_lux=20.0
    )
    assert enrich < m < 1.0


def test_rate_multiplier_lighting_bands():
    # Dim (<10 lux, the UEP inspection floor) genuinely suppresses pecking — the
    # mask the judge flags; bright (>30 lux) favors it; 10-30 lux is neutral.
    p = ModelParams()
    dim = feather_rate_multiplier(
        p, enrichment_installed=False, methionine_ration=False, lighting_lux=5.0
    )
    neutral = feather_rate_multiplier(
        p, enrichment_installed=False, methionine_ration=False, lighting_lux=15.0
    )
    bright = feather_rate_multiplier(
        p, enrichment_installed=False, methionine_ration=False, lighting_lux=60.0
    )
    assert dim < 1.0
    assert neutral == 1.0
    assert bright > 1.0


def test_rate_multiplier_composes_multiplicatively():
    p = ModelParams()
    both = feather_rate_multiplier(
        p, enrichment_installed=True, methionine_ration=True, lighting_lux=20.0
    )
    enrich = feather_rate_multiplier(
        p, enrichment_installed=True, methionine_ration=False, lighting_lux=20.0
    )
    met = feather_rate_multiplier(
        p, enrichment_installed=False, methionine_ration=True, lighting_lux=20.0
    )
    assert abs(both - enrich * met) < 1e-12


# --- Feather -> cannibalism mortality coupling ---


def test_pecking_mortality_zero_at_or_below_threshold():
    p = ModelParams()
    assert pecking_mortality_frac(0.0, p) == 0.0
    assert pecking_mortality_frac(p.feather_mort_threshold_pct, p) == 0.0


def test_pecking_mortality_linear_above_threshold():
    p = ModelParams()
    lo = pecking_mortality_frac(p.feather_mort_threshold_pct + 10.0, p)
    hi = pecking_mortality_frac(p.feather_mort_threshold_pct + 20.0, p)
    assert lo > 0.0
    assert abs(hi - 2.0 * lo) < 1e-12


def test_pecking_mortality_riber_scale():
    # Riber & Hinrichsen 2017: a severely feather-damaged non-trimmed flock ran
    # 14.2% vs 8.6% cumulative mortality — about +5.6pp. Sustained severe damage
    # (57.8%, the 65-wk anchor) over the post-cross remainder of a cycle
    # (~300 days) must land in the same +3 to +7pp band.
    p = ModelParams()
    daily = pecking_mortality_frac(57.8, p)
    cumulative = daily * 300
    assert 0.03 < cumulative < 0.07
