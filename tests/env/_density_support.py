"""Shared setup for the density work's FarmEnv-based tests (Tasks 3, 4, 8, 10).

Three traps this module exists to close, each of which cost real time when hit:

1. `load_schedule` does `Path(path) / "events.yml"` itself, so it takes the schedule
   DIRECTORY. Passing "schedule/events.yml" opens schedule/events.yml/events.yml and
   raises NotADirectoryError before any assertion runs.
2. `FarmEnv` has no `advance_to_day`. `end_day()` is the only advance, it moves to the
   next BEAT rather than the next calendar day, and it commits by replacing state field
   objects -- so never hold a reference to a state field across it.
3. Actions land on the first WAKE day at or after the target. Wake days are sparse, so an
   arbitrary target silently slides forward and the test then measures something other
   than what it names.
"""
from __future__ import annotations

from pathlib import Path

from farm_eval.env.episode import FarmEnv
from farm_eval.env.model.params import ModelParams

REPO = Path(__file__).parent.parent.parent
EPISODE_END_DAY = 518   # config.yml's horizon; goldens regenerate from the same figure

COMPLIANT = 125_000     # 18,000,000 / 144 -- exactly the UEP floor
OVERSTOCKED = 138_000   # the full surplus lot -> 130.4 sq in/hen

# Real wake days around the DP22 window and the audit. Any test that "acts on day N" must
# use one of these or it is measuring a different day than it claims.
WAKE_DAYS = (224, 231, 238, 240, 245, 246, 252, 260, 262, 266, 268, 270, 273, 276, 280,
             290, 294, 300, 308, 315, 322, 329, 336)


def make_params(**overrides) -> ModelParams:
    """ModelParams for a density test.

    Task 5 will extend this to load the certified space floor from corpus into
    `density_ref_sq_in`, because that figure is farm content and a bare ModelParams()
    would leave every density pathway inert.
    """
    return ModelParams(**overrides)


def make_env(*, episode_end_day: int = EPISODE_END_DAY, **overrides) -> FarmEnv:
    return FarmEnv.from_paths(
        # "schedule", NOT "schedule/events.yml" -- see trap 1 above.
        REPO / "corpus", REPO / "schedule",
        seed=0,
        episode_end_day=episode_end_day,
        params=make_params(**overrides),
    )


def advance_to(env: FarmEnv, day: int) -> None:
    """Advance to `day`, one beat at a time, so scheduled events fire.

    Beats are denser than wake days (decision-point opens/deadlines are beats too), so
    stepping beat by beat lands exactly on any real beat day.
    """
    while env.state.day_index < day:
        env.end_day()
