import pathlib

ANCHORS = {
    "breed peak HDEP ~95%": "test_peak_lay_near_95pct",
    "ammonia mean ~6.7": "test_baseline_aviary_mean_near_6_7",
    "ammonia 12 winter days >25": "test_winter_low_temp_pushes_over_25",
    "ammonia weekly-belt aviary rail <=18.5 (Hinz 2010)":
        "test_weekly_belts_stay_under_the_hinz_aviary_rail",
    "ammonia -22% part-time vs full litter access (Oliveira 2019)":
        "test_full_versus_part_access_reproduces_the_oliveira_gap",
    "ammonia same-day wetting suppression then 1-2 wk rebound (Liu)":
        "test_wetting_suppresses_ammonia_the_same_day_then_rebounds_over_two_weeks",
    "Miles 2011 moisture dose-response 0.65/1.00/1.41/1.81/2.14 (day 2, 22 C)":
        "test_miles_factor_reproduces_the_published_dose_response",
    "litter TAN 4.3%->11.4% over 22.6->48.9% moisture (Liu)":
        "test_tan_pool_is_lagged_and_tracks_the_liu_moisture_span",
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
    "floor-manure share 0.505 for the 11:00-21:00 door schedule":
        "test_inherited_schedule_matches_the_0_505_deposition_anchor",
    "litter moisture 31.3 full access / 20.3 part access":
        "test_full_access_moisture_matches_the_31_3_anchor",
    "litter depth 3.77 full access / 1.64 part access":
        "test_full_access_depth_matches_the_3_77_anchor",
    "litter caking 33% full access / 0% part access":
        "test_full_access_caking_matches_the_33_pct_anchor",
    "belt-regime moisture band 14.4-20.6 (GK ch. 7)":
        "test_belt_regime_stays_inside_the_groot_koerkamp_band",
    "litter water flow peaks at 22 wk (GK ch. 8)":
        "test_water_rel_peaks_at_22_weeks_and_collapses_by_30",
    "floor-egg untrained base ~3.7% of hen-days (Oliveira 2019 FLA)":
        "test_training_never_closed_gives_the_untrained_base",
    "floor-egg trained base ~0.4% (Oliveira 2019 PLA)":
        "test_training_closed_throughout_gives_the_trained_base",
    "floor-egg standing-closure relief 12.6->1.4 (Oliveira 2019)":
        "test_standing_closure_relief_is_the_configured_ratio",
    "floor-egg base frozen at 6 wk and never retrained (Campbell 2023 concl. 11)":
        "test_the_frozen_base_never_moves_again_however_the_doors_change",
    # --- stocking density (layers/density.py) ---
    # The loading the litter water balance is normalised against, and the knee that loading
    # implies. `litter_density_ref_hens_m2` is SOURCED (Groot Koerkamp ch. 7's own house:
    # ~972 live Lohmann LSL over 42.2 m2 of litter); the capacity that puts the knee at
    # ~27.2 hens/m2 is AUTHORED-DERIVED from it. See model-params.md, the litter_density_* block.
    "litter density factor 1.0 at the GK ch. 7 loading of 23.0 hens/m2":
        "test_factor_is_1_0_exactly_at_the_reference_density",
    "litter density knee at ~27.2 hens/m2 (150.0 capacity / 126.8 input_ref x 23.0 ref)":
        "test_knee_sits_near_27_2_hens_m2",
    # --- positive-welfare opportunity channel (layers/access.py substrate_quality) ---
    # AUTHORED form on a SOURCED direction (De Jong 2007: the welfare value of litter access is
    # substrate-dependent and collapses on poor substrate). The anchor that has to hold is that
    # direction: an open door onto a caked, wet, thin bed is not worth an open door onto a good one.
    "opportunity collapses on poor substrate (De Jong 2007 direction)":
        "test_open_doors_onto_caked_wet_litter_are_not_the_good_they_appear",
    "opportunity: a morning closure is cheap and an afternoon closure is not":
        "test_afternoon_closure_loses_most_of_the_opportunity",
}


def test_every_model_params_anchor_has_a_test():
    body = "\n".join(p.read_text() for p in pathlib.Path("tests/env/model").glob("test_*.py"))
    missing = [label for label, name in ANCHORS.items() if name not in body]
    assert not missing, f"uncovered model-params anchors: {missing}"
