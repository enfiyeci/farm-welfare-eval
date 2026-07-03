import pathlib

ANCHORS = {
    "breed peak HDEP ~95%": "test_peak_lay_near_95pct",
    "ammonia mean ~6.7": "test_baseline_aviary_mean_near_6_7",
    "ammonia 12 winter days >25": "test_winter_low_temp_pushes_over_25",
    "panting onset THI 28.5": "test_panting_onset_at_thi_28_5",
    "keel 60/76/86.5": "test_keel_anchors",
    "feather 3.2/32.9/57.8": "test_feather_anchors",
    "footpad mid-30s prevalence": "test_prevalence_reaches_mid_30s_on_wet_litter",
    "downgrade 3.2%@30wk / 23.8%@80wk": "test_downgrade_rises_with_age",
    "feed tons conversion": "test_feed_tons_conversion",
    "margin identity": "test_integrate_populates_pnl",
    "procurement timing lever": "test_buying_ahead_of_price_rise_is_cheaper",
    "COP cents/doz": "test_cop_and_margin_per_dozen",
    "worker NH3 over-threshold accrual": "test_worker_exposure_accrues_only_over_threshold",
    "red-mite logistic growth": "test_red_mite_grows_logistically_toward_carrying",
    "drug-residue withdrawal map (erythromycin 11d)": "test_withdrawal_map_has_research_anchored_values",
    "SE env-test sensitivity-limited": "test_positive_flock_detection_is_sensitivity_limited_but_deterministic",
    "HPAI subclinical-then-exponential": "test_subclinical_then_exponential_rise",
    "staffing 4.1pp mortality gap at u=1": "test_full_cycle_understaffed_mortality_reproduces_the_4_1pp_gap_at_u_1",
    "staffing floor-egg 10-15% band": "test_floor_egg_ceiling_matches_the_10_to_15_pct_band",
    "staffing 40k hens/FTE full adequacy": "test_full_adequacy_sits_at_the_40k_hens_per_fte_anchor",
}


def test_every_model_params_anchor_has_a_test():
    body = "\n".join(p.read_text() for p in pathlib.Path("tests/env/model").glob("test_*.py"))
    missing = [label for label, name in ANCHORS.items() if name not in body]
    assert not missing, f"uncovered model-params anchors: {missing}"
