# tests/env/model/test_new_channels_integration.py
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model.integrate import integrate
from farm_eval.env.model.params import ModelParams


def _fresh():
    return build_initial_state(load_corpus("corpus"))


def test_new_channels_populate_and_are_path_independent():
    one = _fresh()
    integrate(one, 210, ModelParams())
    chunk = _fresh()
    for _ in range(7):
        integrate(chunk, 30, ModelParams())
        chunk.day_index += 30
    # path-independence across the new channels
    assert one.model_dump() == {**chunk.model_dump(), "day_index": one.day_index}
    # channels advanced
    h4 = one.welfare.houses["H4"]
    assert h4.red_mite_index > 0.05                 # mites grew
    assert one.welfare.harm.worker_nh3_ppm_hours_over >= 0.0


def test_hpai_onset_drives_excess_mortality():
    s = _fresh()
    h = "H4"
    s.welfare.houses[h].hpai_onset_day = s.day_index + 2
    before = s.world.bird_count[h]
    integrate(s, 14, ModelParams())
    assert s.world.bird_count[h] < before * 0.95     # mass mortality after onset


def test_mortality_conserves_birds_under_extreme_excess():
    # When per-day excess mortality (heat + HPAI) would exceed the live flock, deaths must be
    # capped at `birds` — no phantom deaths beyond the flock inflating mortality_cumulative /
    # the sunk-cost line. Conservation: cumulative deaths == birds actually removed.
    s = _fresh()
    initial = dict(s.world.bird_count)
    s.welfare.houses["H4"].hpai_onset_day = s.day_index + 1
    # Extreme params: HPAI fraction alone exceeds 1.0/day (cap 2.0) once clinical.
    p = ModelParams(hpai_incubation_days=0, hpai_mort_base=0.8,
                    hpai_mort_doubling_days=1.0, hpai_mort_cap=2.0)
    integrate(s, 10, p)
    removed = sum(initial[hid] - s.world.bird_count[hid] for hid in initial)
    assert all(c >= 0 for c in s.world.bird_count.values())     # never negative
    assert s.welfare.mortality_cumulative == removed            # no phantom deaths
