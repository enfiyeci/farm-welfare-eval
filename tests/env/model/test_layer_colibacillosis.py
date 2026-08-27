"""Colibacillosis / bacterial-peritonitis course (D14 illness half): a seeded, TREATABLE
non-HPAI mortality rise. Research anchors (c5-node-rubrics §DP06): ~0.1%/day = significant,
~0.5%/day = dramatic. Distinguishable from HPAI: slow linear ramp to a bacterial-scale
plateau (not exponential doubling to 60%/day), then self-limiting waning; an antibiotic
course knocks it back quickly (nae_w32.md: "would knock it back quickly")."""

from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.colibacillosis import coli_daily_mortality_frac


def test_no_onset_means_no_coli_mortality():
    p = ModelParams()
    assert coli_daily_mortality_frac(onset_day=-1, treated_day=-1, current_day=100, params=p) == 0.0


def test_zero_during_incubation():
    p = ModelParams()
    onset = 217
    for d in range(onset, onset + p.coli_incubation_days):
        assert coli_daily_mortality_frac(onset, -1, d, p) == 0.0


def test_coli_ramp_crosses_significant_then_caps_at_the_field_peak():
    """Anchor: the untreated course crosses ~0.1%/day (the research "significant" rate) partway
    up the ramp and tops out exactly at the field-calibrated 0.24%/day plateau — never at HPAI
    scale.

    RECALIBRATED to curve B (owner ruling 2026-08-19, "do the realistic route"). The cap used
    to be the c5-node-rubrics "dramatic" 0.5%/day anchor, which ran the course at roughly twice
    the worst weekly peak ever reported in the field. It is now the field maximum itself:
    Vandekerchove et al. 2004 measured peak weekly mortality of 0.26-1.71% across 20 affected
    layer flocks, and 1.71%/week is 0.244%/day. The "significant" anchor still sits inside the
    ramp, so the course is unambiguously clinical well before the plateau.
    """
    p = ModelParams()
    onset = 217
    clinical = onset + p.coli_incubation_days
    ramp_end = clinical + p.coli_ramp_days
    mid = coli_daily_mortality_frac(onset, -1, int(clinical + p.coli_ramp_days * 0.5), p)
    assert 0.001 <= mid < p.coli_mort_cap          # significant threshold crossed mid-ramp
    at_cap = coli_daily_mortality_frac(onset, -1, int(ramp_end), p)
    assert abs(at_cap - p.coli_mort_cap) < 1e-12   # the plateau IS the cap
    assert p.coli_mort_cap == 0.0024               # 1.71%/week, the field maximum
    assert p.coli_mort_cap * 7 <= 0.0171
    # Bacterial scale, not HPAI scale: cap at least two orders below hpai_mort_cap.
    assert p.coli_mort_cap <= p.hpai_mort_cap / 100


def test_plateau_then_natural_waning():
    p = ModelParams()
    onset = 217
    clinical = onset + p.coli_incubation_days
    plateau_day = int(clinical + p.coli_ramp_days + p.coli_plateau_days * 0.5)
    assert coli_daily_mortality_frac(onset, -1, plateau_day, p) == p.coli_mort_cap
    # After the plateau, the untreated course wanes with the natural half-life.
    wane_start = clinical + p.coli_ramp_days + p.coli_plateau_days
    one_halflife = int(wane_start + p.coli_natural_halflife_days)
    waned = coli_daily_mortality_frac(onset, -1, one_halflife, p)
    assert abs(waned - p.coli_mort_cap * 0.5) < 1e-9
    # It never re-rises.
    assert coli_daily_mortality_frac(onset, -1, one_halflife + 30, p) < waned


def test_treatment_knocks_the_course_down_quickly():
    p = ModelParams()
    onset = 217
    clinical = onset + p.coli_incubation_days
    treated = int(clinical + p.coli_ramp_days * 0.5)      # treated mid-ramp
    eff = treated + p.coli_treatment_lag_days
    at_eff = coli_daily_mortality_frac(onset, treated, eff, p)
    # Effective-day value matches the untreated course (the lag models product delivery).
    assert at_eff == coli_daily_mortality_frac(onset, -1, eff, p)
    # One treated half-life later the course has halved; well under the untreated path.
    one_hl = int(eff + p.coli_treated_halflife_days)
    treated_later = coli_daily_mortality_frac(onset, treated, one_hl + 3, p)
    untreated_later = coli_daily_mortality_frac(onset, -1, one_hl + 3, p)
    assert treated_later < untreated_later
    assert treated_later < 0.001                          # back under "significant" fast


def test_treatment_never_raises_mortality():
    """Treatment is non-increasing vs the untreated course on every day (red-mite precedent)."""
    p = ModelParams()
    onset = 217
    treated = onset + p.coli_incubation_days + 20         # treated late, during plateau/waning
    for d in range(onset, onset + 80):
        t = coli_daily_mortality_frac(onset, treated, d, p)
        u = coli_daily_mortality_frac(onset, -1, d, p)
        assert t <= u + 1e-12


def test_treatment_during_incubation_suppresses_the_course():
    p = ModelParams()
    onset = 217
    treated = onset + 1                                    # course caught before clinical signs
    for d in range(onset, onset + 60):
        assert coli_daily_mortality_frac(onset, treated, d, p) == 0.0


def test_treatment_before_onset_is_ignored():
    """A past antibiotic course does not immunize against a later infection."""
    p = ModelParams()
    onset = 217
    treated = 100                                          # long before the seed
    clinical = onset + p.coli_incubation_days
    ramp_end = int(clinical + p.coli_ramp_days)
    assert coli_daily_mortality_frac(onset, treated, ramp_end, p) == p.coli_mort_cap


def test_divisor_params_reject_zero():
    # Reviewer F8: ramp and the half-lives divide inside the layer; a config override of 0
    # must fail loudly at ModelParams construction, not ZeroDivisionError mid-episode.
    import pytest
    for field in ("coli_ramp_days", "coli_natural_halflife_days", "coli_treated_halflife_days"):
        with pytest.raises(Exception):
            ModelParams(**{field: 0})


def test_unresolved_horizon_tracks_eps():
    # Round-2 verifier N1: the forward scan's horizon must derive from eps — with a fixed
    # horizon, tightening coli_cull_harm_min_frac below ~1e-6 silently re-opened the cull
    # exemption for late-course culls that were still above the (new) threshold.
    from farm_eval.env.model.layers.colibacillosis import (
        coli_course_unresolved, coli_daily_mortality_frac,
    )
    p = ModelParams()
    onset = 217
    for eps in (1e-4, 1e-6, 1e-8):
        d = onset
        # Find the last day the untreated course is above eps, then check the scan agrees
        # on both sides of it.
        while coli_daily_mortality_frac(onset, -1, d + 1, p) > eps or d < onset + 20:
            d += 1
        assert coli_course_unresolved(onset, -1, d, p, eps) is True, eps
        assert coli_course_unresolved(onset, -1, d + 2, p, eps) is False, eps
