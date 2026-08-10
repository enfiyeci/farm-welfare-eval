import pytest
from pydantic import ValidationError

from farm_eval.env.model.layers.access import (
    access_hours,
    floor_manure_share,
    open_lit_hours,
    opportunity_available,
)
from farm_eval.env.model.params import ModelParams


P = ModelParams()
LIGHTS_ON = 5.0


def test_full_access_at_16_hours_is_fully_available():
    assert floor_manure_share(5.0, 21.0, LIGHTS_ON, 16.0, P) == 1.0
    assert opportunity_available(5.0, 21.0, LIGHTS_ON, 16.0, P) == 1.0


def test_inherited_schedule_matches_16_hour_anchors():
    assert floor_manure_share(11.0, 21.0, LIGHTS_ON, 16.0, P) == pytest.approx(0.505, abs=0.01)
    assert opportunity_available(11.0, 21.0, LIGHTS_ON, 16.0, P) >= 0.90


def test_afternoon_closure_is_opportunity_expensive_at_16_hours():
    assert opportunity_available(5.0, 12.0, LIGHTS_ON, 16.0, P) <= 0.35


def test_full_access_renormalizes_for_12_hour_photoperiod():
    assert floor_manure_share(5.0, 21.0, LIGHTS_ON, 12.0, P) == 1.0
    assert opportunity_available(5.0, 21.0, LIGHTS_ON, 12.0, P) == 1.0


def test_closed_all_day_when_open_is_not_before_close():
    for open_h, close_h in ((21.0, 21.0), (22.0, 21.0)):
        assert open_lit_hours(open_h, close_h, LIGHTS_ON, 16.0) == []
        assert access_hours(open_h, close_h, LIGHTS_ON, 16.0) == 0.0
        assert floor_manure_share(open_h, close_h, LIGHTS_ON, 16.0, P) == 0.0
        assert opportunity_available(open_h, close_h, LIGHTS_ON, 16.0, P) == 0.0


def test_diurnal_weights_must_sum_to_one():
    with pytest.raises(ValidationError, match="w_dep_hourly must sum to 1.0"):
        ModelParams(w_dep_hourly=[0.0] * 16)
    with pytest.raises(ValidationError, match="w_opp_hourly must sum to 1.0"):
        ModelParams(w_opp_hourly=[0.0] * 16)


def test_open_hours_past_the_table_still_count():
    # Review finding: the weight tables hold 16 entries but lighting_hours is a (0, 24)
    # setpoint. Hours past the table used to be dropped, so a door open ONLY in those hours
    # reported zero share and zero opportunity while access_hours still counted it open.
    # The tail entry is held instead, so an open hour is never silently worth nothing.
    assert open_lit_hours(21.0, 23.0, LIGHTS_ON, 18.0) == [21, 22]
    assert access_hours(21.0, 23.0, LIGHTS_ON, 18.0) == 2.0
    assert floor_manure_share(21.0, 23.0, LIGHTS_ON, 18.0, P) > 0.0
    assert opportunity_available(21.0, 23.0, LIGHTS_ON, 18.0, P) > 0.0


@pytest.mark.parametrize("lighting_hours", [8.0, 12.0, 12.5, 14.0, 16.0, 18.0, 20.0])
def test_full_access_is_exactly_one_at_every_photoperiod(lighting_hours):
    # The round-2 F2 contract: both shares are denominated against the CURRENT lit window, so
    # a fully-open door is 1.0 at ANY photoperiod. H4 runs 12.0 h; nothing may charge the
    # litter node for a correct pullet lighting program.
    assert floor_manure_share(0.0, 24.0, LIGHTS_ON, lighting_hours, P) == 1.0
    assert opportunity_available(0.0, 24.0, LIGHTS_ON, lighting_hours, P) == 1.0


def test_fractional_door_hours_resolve_to_whole_hours():
    # Documented contract (module docstring): an hour counts as open only if it starts at or
    # after open_h, so a door opening at 11.5 first counts hour 12 — same as opening at 12.0.
    assert open_lit_hours(11.5, 21.0, LIGHTS_ON, 16.0) == open_lit_hours(12.0, 21.0, LIGHTS_ON, 16.0)
