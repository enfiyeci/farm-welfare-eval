from farm_eval.env.model.params import ModelParams
from farm_eval.env.model.layers.footpad import footpad_step


# ---------------------------------------------------------------------------
# Original anchor tests (do not weaken)
# ---------------------------------------------------------------------------

def test_prevalence_reaches_mid_30s_on_wet_litter():
    p = ModelParams()
    mild, severe = 0.0, 0.0
    for _ in range(200):                      # ~ to mid-lay on persistently wet litter
        mild, severe = footpad_step(mild, severe, litter_moisture=35.0, age_weeks=30.0, params=p)
    assert 30.0 <= mild + severe <= 45.0      # ~35% prevalence with saturating incidence


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


# ---------------------------------------------------------------------------
# New tests covering the redesign fixes
# ---------------------------------------------------------------------------

def test_total_prevalence_never_exceeds_100():
    """Saturating incidence + hard clamp guarantee sum <= 100 for any inputs."""
    p = ModelParams()

    # Stress state: sum already over 100 at init — single step must not exceed 100
    m, s = footpad_step(60.0, 60.0, litter_moisture=40.0, age_weeks=80.0, params=p)
    assert m + s <= 100.0 + 1e-9
    assert m >= 0.0 and s >= 0.0

    # Long run at very wet, very old flock — still bounded
    mild, severe = 0.0, 0.0
    for _ in range(2000):
        mild, severe = footpad_step(mild, severe, litter_moisture=40.0, age_weeks=80.0, params=p)
        assert mild + severe <= 100.0 + 1e-9, f"sum exceeded 100 at step: mild={mild}, severe={severe}"
        assert mild >= 0.0 and severe >= 0.0


def test_severe_nondecreasing_on_wet_litter_from_low_mild():
    """With mild=0, severe should not fall on wet litter (healing gated to dry)."""
    p = ModelParams()
    _, severe2 = footpad_step(0.0, 80.0, litter_moisture=40.0, age_weeks=40.0, params=p)
    assert severe2 >= 80.0


def test_old_flock_prevalence_bounded():
    """At age 73 wk, 300 wet-litter steps must stay within [0, 100]."""
    p = ModelParams()
    mild, severe = 0.0, 0.0
    for step in range(300):
        mild, severe = footpad_step(mild, severe, litter_moisture=35.0, age_weeks=73.0, params=p)
        assert 0.0 <= mild + severe <= 100.0, (
            f"prevalence out of bounds at step {step}: mild={mild}, severe={severe}"
        )


def test_dry_litter_severe_can_heal():
    """On dry litter, severe eventually decreases (healing gated to dry, not globally zero)."""
    p = ModelParams()
    mild, severe = 0.0, 20.0   # start with elevated severe, no mild
    for _ in range(500):
        mild, severe = footpad_step(mild, severe, litter_moisture=22.0, age_weeks=30.0, params=p)
    # After 500 dry-litter steps, severe should have decreased from 20
    assert severe < 20.0, f"severe did not decrease on dry litter (still {severe:.2f}%)"
