"""ModelParams must reject non-finite calibration values at construction.

Pydantic accepts ``inf``/``-inf``/``nan`` for a ``float`` field by default, and YAML can
express all three (``.inf``, ``-.inf``, ``.nan``). ModelParams has TWO construction surfaces
and both were unguarded:

  1. ``loader.params_for`` injects three corpus-owned farm-content values with a bare
     ``float()`` coercion (``density_ref_sq_in``, ``litter_area_frac``,
     ``belt_service_days_credit``).
  2. ``config.yml``'s ``model_params:`` block reaches ``ModelParams(**...)`` directly in
     ``farm_task.py``, bypassing ``params_for`` — so it can set ANY field, including ones with
     no corpus key at all (``belt_service_decay_days``).

The failures were silent rather than loud: ``belt_service_days_credit: .inf`` floors the
effective belt interval at 1.0 for every serviced house (maximal drying credit), and
``belt_service_decay_days: .inf`` makes that credit permanent instead of decaying.
"""
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from farm_eval.env.loader import load_corpus, params_for
from farm_eval.env.model.params import ModelParams


# --- Surface 2: any field, straight through ModelParams(**...) ------------------------------

@pytest.mark.parametrize("bad", [float("inf"), float("-inf"), float("nan")])
def test_rejects_non_finite_scalar_naming_field_and_value(bad):
    with pytest.raises(ValidationError) as exc:
        ModelParams(belt_service_days_credit=bad)
    msg = str(exc.value)
    assert "belt_service_days_credit" in msg
    assert repr(bad) in msg or f"{bad}" in msg


def test_rejects_non_finite_decay_days_the_config_only_field():
    # No corpus key exists for this one, so params_for cannot guard it -- a `model_params:`
    # block in config.yml is its only route in. `.inf` here makes a belt-service credit
    # permanent (days_since / inf == 0 -> remaining stays 1.0).
    with pytest.raises(ValidationError) as exc:
        ModelParams(belt_service_decay_days=float("inf"))
    assert "belt_service_decay_days" in str(exc.value)


def test_rejects_non_finite_inside_a_list_field():
    with pytest.raises(ValidationError) as exc:
        ModelParams(breed_hdep=[4.4, float("nan"), 92.3, 95.2, 95.7, 94.0, 89.0, 84.2,
                                79.3, 74.4, 70.8])
    assert "breed_hdep[1]" in str(exc.value)


def test_rejects_non_finite_inside_a_dict_field():
    with pytest.raises(ValidationError) as exc:
        ModelParams(egg_withdrawal_days={"tiamulin": float("inf")})
    assert "egg_withdrawal_days['tiamulin']" in str(exc.value)


def test_rejects_non_finite_inside_a_nested_tuple_field():
    # setpoint_bounds values are (min, max) pairs; an infinite bound silently disables the
    # action-tool sanity rail it exists to enforce.
    with pytest.raises(ValidationError) as exc:
        ModelParams(setpoint_bounds={"ventilation": (0.0, float("inf"))})
    assert "setpoint_bounds['ventilation'][1]" in str(exc.value)


def test_accepts_the_calibrated_defaults():
    # The sweep must not reject the shipped calibration.
    assert ModelParams().belt_service_decay_days == 7.0


def test_rejects_non_finite_assigned_after_construction():
    # An after-validator only fires at construction unless validate_assignment is on, which
    # would leave `p = ModelParams(); p.belt_service_decay_days = inf` as a live route to the
    # exact litter-layer failure this guard exists to prevent. (Codex adversarial review.)
    # The contract pinned here is that the assignment RAISES. Pydantic installs the value
    # before running model-level `after` validators, so it is not rolled back -- see the
    # model_config comment in params.py for why that residue is left alone.
    p = ModelParams()
    with pytest.raises(ValidationError):
        p.belt_service_decay_days = float("inf")


def test_rejects_out_of_range_assigned_after_construction():
    p = ModelParams()
    with pytest.raises(ValidationError):
        p.litter_area_frac = 1.5


# --- Sign / range on the four fields the two surfaces actually write ------------------------

def test_rejects_negative_belt_service_credit():
    # A negative credit would STRETCH the effective belt interval -- inverting the lever a
    # manure-belt service is supposed to pull.
    with pytest.raises(ValidationError) as exc:
        ModelParams(belt_service_days_credit=-1.0)
    assert "belt_service_days_credit" in str(exc.value)


def test_rejects_negative_decay_days():
    with pytest.raises(ValidationError):
        ModelParams(belt_service_decay_days=-1.0)


def test_rejects_negative_density_reference():
    with pytest.raises(ValidationError):
        ModelParams(density_ref_sq_in=-144.0)


@pytest.mark.parametrize("bad", [-0.1, 1.5])
def test_rejects_litter_area_frac_outside_unit_interval(bad):
    # It is a SHARE of usable floor area.
    with pytest.raises(ValidationError) as exc:
        ModelParams(litter_area_frac=bad)
    assert "litter_area_frac" in str(exc.value)


def test_accepts_the_inert_zero_defaults():
    # 0.0 means "switched off" for all three corpus-owned fields and must stay valid.
    p = ModelParams()
    assert (p.density_ref_sq_in, p.litter_area_frac, p.belt_service_days_credit) == (0.0, 0.0, 0.0)


# --- Surface 1: corpus YAML through loader.params_for ---------------------------------------

def _write_corpus(base: Path, company: dict) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    (base / "company.yml").write_text(yaml.safe_dump(company), encoding="utf-8")
    (base / "pricing.yml").write_text("{}\n", encoding="utf-8")
    return base


@pytest.mark.parametrize(
    "yaml_body, expected_field",
    [
        ("audit_thresholds:\n  space_sq_in_per_hen_min: .inf\n", "density_ref_sq_in"),
        ("litter_area_frac: .nan\n", "litter_area_frac"),
        ("belt_service_days_credit: .inf\n", "belt_service_days_credit"),
    ],
)
def test_params_for_rejects_non_finite_corpus_values(tmp_path, yaml_body, expected_field):
    # `.inf` / `.nan` are valid YAML floats, and params_for coerces with a bare float(), so
    # the guard has to live in ModelParams itself.
    base = tmp_path / "corpus"
    base.mkdir()
    (base / "company.yml").write_text(yaml_body, encoding="utf-8")
    (base / "pricing.yml").write_text("{}\n", encoding="utf-8")
    corpus = load_corpus(base)
    with pytest.raises(ValidationError) as exc:
        params_for(corpus)
    assert expected_field in str(exc.value)


def test_params_for_still_builds_from_a_valid_corpus(tmp_path):
    base = _write_corpus(
        tmp_path / "corpus",
        {
            "audit_thresholds": {"space_sq_in_per_hen_min": 144.0},
            "litter_area_frac": 0.41,
            "belt_service_days_credit": 1.0,
        },
    )
    p = params_for(load_corpus(base))
    assert (p.density_ref_sq_in, p.litter_area_frac, p.belt_service_days_credit) == (144.0, 0.41, 1.0)
