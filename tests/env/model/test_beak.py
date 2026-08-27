from farm_eval.env.model.layers.beak import (
    beak_cannibalism_multiplier,
    beak_feather_multiplier,
    trim_pain_pulse,
)
from farm_eval.env.model.params import ModelParams


P = ModelParams()


def test_the_default_treatment_is_the_neutral_element_of_both_multipliers():
    """Every authored flock is a routinely trimmed commercial flock, and the pre-DPD feather
    and cannibalism calibrations describe exactly that flock — so the DEFAULT beak treatment
    must multiply both rates by exactly 1.0. Batch-10 review fix (2026-08-27): the first
    build shipped the IR cannibalism factor at 0.5, which silently halved pecking mortality
    in every house and moved the DP15 gold-path cull count and the financial reference."""
    default = P.beak_default_treatment
    assert P.beak_cannibalism_factor[default] == 1.0
    assert beak_cannibalism_multiplier(
        P, beak_treatment=default, strain_low_pecking=False
    ) == 1.0
    assert beak_feather_multiplier(
        P, beak_treatment=default, strain_low_pecking=False, rearing_match=False
    ) == 1.0


def test_trimmed_is_baseline():
    assert (
        beak_feather_multiplier(
            P,
            beak_treatment="infrared_dayold",
            strain_low_pecking=False,
            rearing_match=False,
        )
        == 1.0
    )


def test_intact_unprepared_is_worse():
    multiplier = beak_feather_multiplier(
        P,
        beak_treatment="intact",
        strain_low_pecking=False,
        rearing_match=False,
    )
    assert multiplier > 1.5


def test_intact_fully_prepared_approaches_trimmed():
    multiplier = beak_feather_multiplier(
        P,
        beak_treatment="intact",
        strain_low_pecking=True,
        rearing_match=True,
    )
    assert multiplier < 1.05


def test_intact_no_trim_pain():
    assert trim_pain_pulse(P, beak_treatment="intact") == (0.0, 0.0)


def test_dayold_ir_acute_only_no_chronic():
    acute, chronic = trim_pain_pulse(P, beak_treatment="infrared_dayold")
    assert acute > 0.0 and chronic == 0.0


def test_deep_has_chronic():
    acute_deep, chronic_deep = trim_pain_pulse(P, beak_treatment="deep")
    acute_ir, _ = trim_pain_pulse(P, beak_treatment="infrared_dayold")
    assert acute_deep > acute_ir and chronic_deep > 0.0
