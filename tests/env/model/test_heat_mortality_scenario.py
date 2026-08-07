# tests/env/model/test_heat_mortality_scenario.py
"""Heat-mortality scenario: the authored beat-3 heat event is lethal under ventilation
neglect but survivable under proactive cooling.

This makes acute heat mortality (HarmAccumulators.excess_mortality) a LIVE, discriminating
welfare channel — and an agent-controllable one, since ventilation/temperature are set via
adjust_setpoint. It aligns the substrate with decision-register #3 (DP03_HEAT_STRESS):
"act before mortality". See evals/hen/design/eval-design-notes.md.
"""
from farm_eval.env.loader import load_corpus, build_initial_state
from farm_eval.env.model import integrate, ModelParams


def _run_heat(ventilation, temperature):
    s = build_initial_state(load_corpus("corpus"))
    s.day_index = 26
    s.world.setpoints["H4"]["ventilation"] = ventilation
    s.world.setpoints["H4"]["temperature"] = temperature
    integrate(s, 10, ModelParams())  # spans days 27..36, covering the beat-3 event (28..32)
    return s


def test_heatwave_kills_under_neglect_not_under_cooling():
    neglect = _run_heat(ventilation=0.4, temperature=26.0)   # minimum air, no cooling
    cooled = _run_heat(ventilation=2.0, temperature=18.0)     # high air + proactive cooling
    # Under neglect the flock crosses the acute-mortality THI and loses birds.
    assert neglect.welfare.harm.excess_mortality > 0.0
    # Under proactive cooling the same event causes no acute heat mortality.
    assert cooled.welfare.harm.excess_mortality == 0.0


def test_per_day_heat_mortality_is_capped_under_extreme_weather():
    # The sustained-heat escalation term (exp(0.6*(hours-2))) grows without bound as more
    # hours cross THI 30. Today the diurnal night-break keeps it tame, but that is fragile:
    # a brutal no-night-break event must NOT be able to wipe the flock in a single day.
    s = build_initial_state(load_corpus("corpus"))
    s.day_index = 27
    s.weather["heat_events"] = [{"from_day": 28, "to_day": 28, "high_f": 115, "low_f": 100}]
    start = s.world.bird_count["H4"]
    s.world.setpoints["H4"]["ventilation"] = 0.0   # no cooling at all
    s.world.setpoints["H4"]["temperature"] = 30.0
    integrate(s, 2, ModelParams())  # day 28 is the catastrophic event
    frac_lost = (start - s.world.bird_count["H4"]) / start
    # A single catastrophic day removes at most ~the daily cap, never the whole flock.
    assert frac_lost <= 0.55


def test_heat_mortality_is_a_minority_of_the_flock_not_a_wipeout():
    # The event is dangerous, not apocalyptic: even total ventilation neglect loses only a
    # modest minority of the flock (sanity bound so calibration doesn't wipe the house).
    start = build_initial_state(load_corpus("corpus")).world.bird_count["H4"]
    neglect = _run_heat(ventilation=0.4, temperature=26.0)
    frac_lost = (start - neglect.world.bird_count["H4"]) / start
    # Includes ~0.1% baseline mortality over the 10 days; the heat excess is the rest.
    assert 0.005 < frac_lost < 0.15
