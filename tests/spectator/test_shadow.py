"""Tests for the spectator shadow store: JSON-Patch reconstruction of `EnvState`.

Generic placeholder content only -- no farm content in tests (house key `H_X`, ids `m1`/`out-1`).
"""

from __future__ import annotations

import pytest
from inspect_ai._util.json import JsonChange
from pydantic import ValidationError

from farm_eval.env.state import Email, EnvState, HouseWelfare, WelfareState, WorldState
from farm_eval.spectator.shadow import ENV_STATE_KEY, ShadowStore


def _email(email_id: str) -> Email:
    return Email.model_validate(
        {
            "id": email_id,
            "day": 0,
            "date": "2025-01-01",
            "from": "a@x.test",
            "to": "b@x.test",
            "subject": "PLACEHOLDER_SUBJECT",
            "body": "PLACEHOLDER_BODY",
        }
    )


def _seed_dump(**overrides) -> dict:
    """A minimal day-0 EnvState dumped the way the store serializes it (mode="json")."""
    state = EnvState(
        start_date="2025-01-01",
        welfare=WelfareState(
            houses={
                "H_X": HouseWelfare(
                    ammonia_ppm=8.0,
                    co2_ppm=2200.0,
                    litter_moisture=25.0,
                    lighting_lux=10.0,
                    lighting_hours=16.0,
                    heat_stress_index=0.0,
                    stocking_density=1.0,
                )
            }
        ),
        world=WorldState(
            setpoints={"H_X": {"ventilation": 1.0}},
            litter_age_days={"H_X": 0.0},
            bird_count={"H_X": 1000},
        ),
        mailbox=[_email("m1")],
        **overrides,
    )
    return state.model_dump(mode="json")


def _seeded() -> ShadowStore:
    shadow = ShadowStore()
    shadow.seed(_seed_dump())
    return shadow


# --- before seeding -------------------------------------------------------------------


def test_env_state_is_none_before_seeding():
    shadow = ShadowStore()
    assert shadow.env_state() is None
    assert shadow.raw() == {}


def test_apply_before_seed_raises_clear_error():
    shadow = ShadowStore()
    changes = [JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/day_index", value=1)]
    with pytest.raises(ValueError, match="seed"):
        shadow.apply(changes)


def test_apply_empty_change_list_before_seed_also_raises():
    # Fail on the unseeded store itself, not on the first change -- an emitter that forgot
    # to seed must not look healthy just because the first StoreEvent carried no changes.
    with pytest.raises(ValueError, match="seed"):
        ShadowStore().apply([])


# --- the real-stream shape: nested changes first ---------------------------------------


def test_nested_first_change_sequence_applies():
    shadow = _seeded()
    shadow.apply(
        [
            JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/day_index", value=1),
            JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/mailbox/0/unread", value=False),
        ]
    )
    state = shadow.env_state()
    assert state is not None
    assert state.day_index == 1
    assert state.mailbox[0].unread is False


def test_env_state_returns_validated_env_state():
    shadow = _seeded()
    state = shadow.env_state()
    assert isinstance(state, EnvState)
    assert state.day_index == 0
    assert state.welfare.houses["H_X"].ammonia_ppm == 8.0
    assert [e.id for e in state.mailbox] == ["m1"]


def test_env_state_is_none_when_the_key_is_removed():
    shadow = _seeded()
    shadow.apply([JsonChange(op="remove", path=f"/{ENV_STATE_KEY}")])
    assert shadow.env_state() is None


def test_env_state_is_none_when_the_key_holds_null():
    # EpisodeStore.env_state is `EnvState | None`; a null in the store is "not initialized yet".
    shadow = _seeded()
    shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}", value=None)])
    assert shadow.env_state() is None


def test_env_state_raises_on_corrupt_state():
    shadow = _seeded()
    shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/day_index", value="not-an-int")])
    with pytest.raises(ValidationError):
        shadow.env_state()


def test_seed_does_not_alias_the_callers_dump():
    dump = _seed_dump()
    shadow = ShadowStore()
    shadow.seed(dump)
    shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/day_index", value=7)])
    assert dump["day_index"] == 0


def test_seed_twice_replaces_the_state():
    shadow = _seeded()
    shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/day_index", value=5)])
    shadow.seed(_seed_dump())
    state = shadow.env_state()
    assert state is not None and state.day_index == 0


# --- the three ops --------------------------------------------------------------------


def test_add_replace_remove_on_dict_keys():
    shadow = _seeded()
    base = f"/{ENV_STATE_KEY}/weather"
    shadow.apply([JsonChange(op="add", path=f"{base}/k", value=1)])
    assert shadow.raw()[ENV_STATE_KEY]["weather"] == {"k": 1}
    shadow.apply([JsonChange(op="replace", path=f"{base}/k", value=2)])
    assert shadow.raw()[ENV_STATE_KEY]["weather"] == {"k": 2}
    shadow.apply([JsonChange(op="remove", path=f"{base}/k")])
    assert shadow.raw()[ENV_STATE_KEY]["weather"] == {}


def test_add_to_a_dict_overwrites_an_existing_key():
    shadow = _seeded()
    shadow.apply(
        [
            JsonChange(op="add", path=f"/{ENV_STATE_KEY}/weather/k", value=1),
            JsonChange(op="add", path=f"/{ENV_STATE_KEY}/weather/k", value=2),
        ]
    )
    assert shadow.raw()[ENV_STATE_KEY]["weather"] == {"k": 2}


def test_add_appends_to_a_list_with_dash():
    shadow = _seeded()
    shadow.apply(
        [JsonChange(op="add", path=f"/{ENV_STATE_KEY}/mailbox/-", value=_email("m2").model_dump(mode="json"))]
    )
    state = shadow.env_state()
    assert state is not None
    assert [e.id for e in state.mailbox] == ["m1", "m2"]


def test_add_inserts_at_a_list_index():
    shadow = _seeded()
    shadow.apply(
        [JsonChange(op="add", path=f"/{ENV_STATE_KEY}/mailbox/0", value=_email("m0").model_dump(mode="json"))]
    )
    state = shadow.env_state()
    assert state is not None
    assert [e.id for e in state.mailbox] == ["m0", "m1"]


def test_add_at_the_list_length_appends():
    shadow = _seeded()
    shadow.apply(
        [JsonChange(op="add", path=f"/{ENV_STATE_KEY}/mailbox/1", value=_email("m2").model_dump(mode="json"))]
    )
    state = shadow.env_state()
    assert state is not None
    assert [e.id for e in state.mailbox] == ["m1", "m2"]


def test_replace_and_remove_at_a_list_index():
    shadow = _seeded()
    shadow.apply(
        [
            JsonChange(op="add", path=f"/{ENV_STATE_KEY}/mailbox/-", value=_email("m2").model_dump(mode="json")),
            JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/mailbox/1/subject", value="PLACEHOLDER_OTHER"),
        ]
    )
    state = shadow.env_state()
    assert state is not None and state.mailbox[1].subject == "PLACEHOLDER_OTHER"

    shadow.apply([JsonChange(op="remove", path=f"/{ENV_STATE_KEY}/mailbox/0")])
    state = shadow.env_state()
    assert state is not None
    assert [e.id for e in state.mailbox] == ["m2"]


def test_add_a_new_top_level_store_key():
    shadow = _seeded()
    shadow.apply([JsonChange(op="add", path="/EpisodeStore:forced_advances", value=3)])
    assert shadow.raw()["EpisodeStore:forced_advances"] == 3


# --- errors ---------------------------------------------------------------------------


@pytest.mark.parametrize("op", ["move", "copy", "test"])
def test_unsupported_op_raises_value_error(op):
    shadow = _seeded()
    change = JsonChange.model_validate(
        {"op": op, "path": f"/{ENV_STATE_KEY}/day_index", "from": f"/{ENV_STATE_KEY}/seed", "value": 1}
    )
    with pytest.raises(ValueError, match=op):
        shadow.apply([change])


def test_whole_document_pointer_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path="", value={})])


def test_pointer_without_leading_slash_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path=f"{ENV_STATE_KEY}/day_index", value=1)])


def test_replace_on_a_missing_dict_key_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/weather/nope", value=1)])


def test_remove_on_a_missing_dict_key_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="remove", path=f"/{ENV_STATE_KEY}/weather/nope")])


def test_traversal_through_a_missing_key_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/nope/deeper", value=1)])


def test_out_of_range_list_index_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/mailbox/9/unread", value=False)])


def test_non_integer_list_token_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/mailbox/first/unread", value=False)])


def test_dash_token_is_rejected_for_replace_and_remove():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/mailbox/-", value={})])
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="remove", path=f"/{ENV_STATE_KEY}/mailbox/-")])


def test_traversal_into_a_scalar_raises():
    shadow = _seeded()
    with pytest.raises(ValueError):
        shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/day_index/deeper", value=1)])


# --- RFC 6901 escaping ----------------------------------------------------------------


def test_pointer_escapes_are_decoded():
    shadow = ShadowStore()
    shadow.seed(_seed_dump(weather={"a/b": 1, "c~d": 2, "": 3}))
    shadow.apply(
        [
            JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/weather/a~1b", value=10),
            JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/weather/c~0d", value=20),
            JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/weather/", value=30),
        ]
    )
    state = shadow.env_state()
    assert state is not None
    assert state.weather == {"a/b": 10, "c~d": 20, "": 30}


def test_escape_order_tilde_one_is_not_double_decoded():
    # "~01" must decode to the literal "~1", never to "/".
    shadow = ShadowStore()
    shadow.seed(_seed_dump(weather={"~1": 1}))
    shadow.apply([JsonChange(op="replace", path=f"/{ENV_STATE_KEY}/weather/~01", value=9)])
    state = shadow.env_state()
    assert state is not None and state.weather == {"~1": 9}
