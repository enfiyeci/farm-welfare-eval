"""EnvState must reject non-finite floats at construction and deserialization.

Follow-up to the ModelParams finiteness guard (Codex adversarial review round 1, finding 2):
EnvState is a SEPARATE pydantic model with its own outside-data entry points, and a non-finite
float there does not crash — it is laundered by clamps into a plausible-looking, silently
wrong run. Measured before the guard: a NaN ventilation setpoint drove house NH3 to ~5e-26
and RAISED the welfare score and margin; a NaN litter_moisture pushed severe footpad
21.1% -> 26.6% with no error anywhere.

One model-level validator covers every EnvState entry point at once, because they all
construct or model_validate an EnvState:
  - play-session resume (farm_eval/play/session.py),
  - checkpoint / .eval-log deserialization (farm_eval/adapter/checkpoint.py),
  - corpus seeds via loader.build_initial_state — though for the YAML route the LOAD-time
    corpus sweep (tests/env/test_loader_finiteness.py) fires first; this validator is the
    backstop for states assembled without going through load_corpus.

Internal dynamics need no guard: a full clean 518-day episode was scanned after every single
day and produced zero non-finite floats, so non-finites only ever arrive from outside.
"""
import json
import math

import pytest
import yaml
from pydantic import BaseModel, ValidationError

from farm_eval.adapter.checkpoint import load_checkpoint
from farm_eval.env.finite import iter_model_floats
from farm_eval.env.loader import build_initial_state, load_corpus
from farm_eval.env.state import EnvState, HouseWelfare, WelfareState

FIXTURE_CORPUS = "tests/fixtures/corpus"


def _valid_state_dump() -> dict:
    corpus = load_corpus(FIXTURE_CORPUS)
    return build_initial_state(corpus).model_dump()


# --- the shared walker -----------------------------------------------------------------------

def test_walker_descends_pydantic_sub_models():
    # ModelParams has no sub-model fields today, but EnvState nests four levels deep
    # (EnvState -> WelfareState -> houses dict -> HouseWelfare). The walker must not stop at
    # a BaseModel boundary, and the reported path must read like an access expression.
    class Inner(BaseModel):
        x: float = 1.0

    class Outer(BaseModel):
        items: dict[str, Inner] = {}

    found = dict(iter_model_floats(Outer(items={"a": Inner(x=2.5)})))
    assert found == {"items['a'].x": 2.5}


# --- construction / model_validate ----------------------------------------------------------

def test_envstate_rejects_nan_nested_in_house_welfare():
    dump = _valid_state_dump()
    house = next(iter(dump["welfare"]["houses"]))
    dump["welfare"]["houses"][house]["ammonia_ppm"] = float("nan")
    with pytest.raises(ValidationError) as exc:
        EnvState.model_validate(dump)
    assert f"welfare.houses[{house!r}].ammonia_ppm" in str(exc.value)


def test_envstate_rejects_inf_in_setpoints_dict():
    dump = _valid_state_dump()
    house = next(iter(dump["world"]["setpoints"]))
    dump["world"]["setpoints"][house]["ventilation"] = float("inf")
    with pytest.raises(ValidationError) as exc:
        EnvState.model_validate(dump)
    assert f"world.setpoints[{house!r}]['ventilation']" in str(exc.value)


def test_direct_construction_is_guarded_too():
    # The validator must fire on plain construction, not only on model_validate: this is the
    # path build_initial_state takes after assembling the sub-models itself.
    welfare = WelfareState(
        houses={
            "H1": HouseWelfare.model_construct(  # bypass HouseWelfare's own validation
                ammonia_ppm=float("nan"), co2_ppm=1.0, litter_moisture=1.0, lighting_lux=1.0,
                lighting_hours=1.0, heat_stress_index=0.0, stocking_density=1.0,
            )
        }
    )
    with pytest.raises(ValidationError):
        EnvState(start_date="2025-06-09", welfare=welfare)


# --- the corpus entry point ------------------------------------------------------------------

def test_build_initial_state_rejects_nan_authored_in_company_yml(tmp_path):
    # This now trips the LOAD-time corpus sweep (loader._reject_non_finite), one layer
    # before the EnvState validator would see it — hence ValueError, not ValidationError.
    # The EnvState validator remains the guard for states that never pass through
    # load_corpus: play autosaves, checkpoints, .eval-log deserialization.
    import shutil

    base = tmp_path / "corpus"
    shutil.copytree(FIXTURE_CORPUS, base)
    company = yaml.safe_load((base / "company.yml").read_text(encoding="utf-8"))
    company["houses"][0]["welfare"]["litter_moisture"] = float("nan")
    (base / "company.yml").write_text(yaml.safe_dump(company), encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        build_initial_state(load_corpus(base))
    assert "litter_moisture" in str(exc.value)


def test_build_initial_state_accepts_the_fixture_corpus():
    # Positive control: the shipped fixture corpus must still build.
    state = build_initial_state(load_corpus(FIXTURE_CORPUS))
    assert all(math.isfinite(v) for _, v in iter_model_floats(state))


# --- the checkpoint entry point --------------------------------------------------------------

def test_load_checkpoint_rejects_nan_in_env_state(tmp_path):
    # Python's json module WRITES and READS bare NaN by default (it is not valid JSON, but
    # json.loads accepts it), so a checkpoint file is a live route for a non-finite value to
    # re-enter a process. load_checkpoint goes through EnvState.model_validate.
    dump = _valid_state_dump()
    house = next(iter(dump["welfare"]["houses"]))
    dump["welfare"]["houses"][house]["temp_c"] = float("nan")
    path = tmp_path / "day_7.json"
    path.write_text(
        json.dumps({"day": 7, "message_count": 3, "env_state": dump}), encoding="utf-8"
    )
    with pytest.raises(ValidationError):
        load_checkpoint(path)
