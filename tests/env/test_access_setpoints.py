from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model.params import ModelParams

CORPUS = "corpus"; SCHEDULE = "schedule"

def _state():
    return build_initial_state(load_corpus(CORPUS))

def test_access_setpoint_bounds_registered():
    b = ModelParams().setpoint_bounds
    assert b["litter_access_open_hour"] == (0.0, 24.0)
    assert b["litter_access_close_hour"] == (0.0, 24.0)

def test_day0_schedule_is_the_inherited_practice():
    # GATE-2 default: standing morning closure, doors open 11:00 (CSES/Oliveira PLA practice).
    st = _state()
    for hid in ("H1", "H2", "H3", "H4", "H5"):
        assert st.world.setpoints[hid]["litter_access_open_hour"] == 11.0
        assert st.world.setpoints[hid]["litter_access_close_hour"] == 21.0

def test_litter_area_loaded():
    st = _state()
    assert st.world.litter_area_m2["H4"] > 0
