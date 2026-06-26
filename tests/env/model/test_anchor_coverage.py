import pathlib

ANCHORS = {
    "breed peak HDEP ~95%": "test_peak_lay_near_95pct",
    "ammonia mean ~6.7": "test_baseline_aviary_mean_near_6_7",
    "ammonia 12 winter days >25": "test_winter_low_temp_pushes_over_25",
    "panting onset THI 28.5": "test_panting_onset_at_thi_28_5",
    "keel 60/76/86.5": "test_keel_anchors",
    "feather 3.2/32.9/57.8": "test_feather_anchors",
    "footpad mid-30s prevalence": "test_prevalence_reaches_mid_30s_on_wet_litter",
}


def test_every_model_params_anchor_has_a_test():
    body = "\n".join(p.read_text() for p in pathlib.Path("tests/env/model").glob("test_*.py"))
    missing = [label for label, name in ANCHORS.items() if name not in body]
    assert not missing, f"uncovered model-params anchors: {missing}"
