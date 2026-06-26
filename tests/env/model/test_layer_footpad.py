from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.footpad import footpad_step


def test_prevalence_reaches_mid_30s_on_wet_litter():
    p = ModelParams()
    mild, severe = 0.0, 0.0
    for _ in range(200):                      # ~ to mid-lay on persistently wet litter
        mild, severe = footpad_step(mild, severe, litter_moisture=35.0, age_weeks=30.0, params=p)
    assert 30.0 <= mild + severe <= 45.0      # ~36-40% prevalence


def test_severe_accumulates_and_barely_heals():
    p = ModelParams()
    mild, severe = 20.0, 10.0
    _, severe2 = footpad_step(mild, severe, litter_moisture=40.0, age_weeks=40.0, params=p)
    assert severe2 >= severe                  # wet litter -> severe does not fall


def test_dry_litter_does_not_worsen():
    p = ModelParams()
    mild0, severe0 = 10.0, 5.0
    mild1, _ = footpad_step(mild0, severe0, litter_moisture=22.0, age_weeks=30.0, params=p)
    assert mild1 <= mild0 + 0.5
