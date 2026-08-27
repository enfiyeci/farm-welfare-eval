"""Daily-wake-up during active harm (companion to the DP13 egg-test subsystem).

`active_harm_day(state, params)` answers a single question the solver asks before each
day-advance: is a day-scoped tripwire-grace counter still charging in an OCCUPIED house,
AND within its bounded wake window? While the answer is yes, `FarmEnv.end_day` caps the
beat-skip to a single day, so the agent gets a turn on every day a grace counter charges
(the DP13/DP21 tripwires otherwise give a grace that is meaningless if the agent has
no turn on those days).

Two harms are covered — both day-accruing tripwire-grace counters:
  * drug residue (`residue_food_channel_days`) — the DP21 retrofit;
  * SE table-egg latency (`se_positive_shell_days`) — the DP13 companion.
Each mirrors its accrual guard in `integrate()` (farm_eval/env/model/integrate.py). Keep the
two in step: a condition that accrues a counter there but is absent here would re-open the
unfair-skip bug; a condition here that does not accrue there would wake the agent for no
reason. `tests/env/test_harm_window.py` pins each guard.

BOUNDED window (owner ruling 2026-08-13): the wake fires only while the counter has charged
FEWER than `params.harm_wake_days` days. Once it reaches that many, normal beat-skipping
resumes — so a flock that never diverts is woken for the bounded grace window, NOT daily
across the whole ~238-day SE window. The counters are their own
day-clocks (each increments once per accruing day), so `counter < harm_wake_days` is exactly
"still inside the wake window".

Colibacillosis is deliberately EXCLUDED. It has no grace tripwire — its harm is excess
mortality scored by treatment latency — and its fairness needs a LEARNING-anchored window:
the seeded onset (e.g. day 217) precedes the workup email that tells the agent (day 224) by
about a week, so an onset-anchored daily window would close before the agent even learns.
Anchoring coli's daily turns on the discovery beat is a DP06/DPN content-design question,
not this SE/residue grace mechanic; the agent still gets its turn at the workup-email beat.

Why the current state suffices (no look-ahead into the skip window): each covered harm
becomes agent-relevant AT a beat with its counter at 0 — the SE environmental positive is a
state_seed on the DP13 opening day, and drug residue starts from an agent `log_treatment` on
a wake day — so the predicate, read on the post-seed state at that beat, is already True
(counter 0 < harm_wake_days) before the first skippable day.
"""

from __future__ import annotations

from farm_eval.env.model.layers import salmonella
from farm_eval.env.model.params import ModelParams
from farm_eval.env.state import EnvState, current_disposition


def active_harm_day(state: EnvState, params: ModelParams) -> bool:
    """True iff a day-scoped tripwire-grace counter (drug residue or SE table-egg latency) is
    still charging in an occupied house AND has charged fewer than `params.harm_wake_days`
    days. The bounded daily-wake-up condition (companion to D7)."""
    window = params.harm_wake_days
    # The channel that will apply on the next integrated day (integrate() reads
    # current_disposition at as_of_day == the integrated day == day_index + 1).
    next_day = state.day_index + 1
    for hid, hw in state.welfare.houses.items():
        if state.world.bird_count.get(hid, 0) <= 0:
            continue  # empty house accrues nothing (integrate skips it) — no wake owed
        channel = current_disposition(state, hid, as_of_day=next_day)
        # Drug residue: eggs laid through a live withdrawal that leave on any FOOD channel
        # (anything but discard — processing does not remove residue) accrue
        # residue_food_channel_days. Woken while the counter is inside the bounded window.
        if (
            hw.egg_residue_days_left > 0.0
            and channel != "discard"
            and hw.residue_food_channel_days < window
        ):
            return True
        # SE table-egg latency: a known-positive, not-yet-cleared flock still shipping table
        # eggs (shell/conventional) accrues se_positive_shell_days. Same bounded window.
        if (
            hw.se_status
            and hw.se_env_positive_day >= 0
            and channel in salmonella.TABLE_EGG_CHANNELS
            and not salmonella.protocol_cleared(state, hid)
            and hw.se_positive_shell_days < window
        ):
            return True
    return False


def active_mortality_latency_wake(
    state: EnvState, params: ModelParams, decision_points, enabled_nodes
) -> bool:
    """True iff a latent daily-mortality node's window is open for an occupied house whose
    USDA surveillance trigger fired IN-WINDOW within the last ``params.harm_wake_days`` days.

    DP06's observation-anchored companion to ``active_harm_day``. Colibacillosis has no
    tripwire-grace day-clock (its harm is excess mortality scored by treatment latency), so
    this wake tracks the in-window elevated-mortality period instead: the trigger latch
    (``usda_trigger_last_day``) re-advances every elevated day, so ``next_day - last_day <
    harm_wake_days`` holds throughout the die-off and releases a few days after it subsides —
    upper-bounded by the node's ``deadline_day``. The result is a turn on each day the H5
    slope is observably rising within the scoring window, so a vigilant model can catch it and
    an inattentive one is fairly scored.

    The ``last_day >= opens_day`` guard is load-bearing: H5 also trips the trigger during the
    earlier DPN colibacillosis course (~day 224, verified in a passive run), so a persistent
    first-fire anchor would be consumed months before this window opens. The in-window
    ``last_day`` is the robust anchor, and it matches DP06's own scoring gate
    (``requires_state: usda_trigger_last_day`` inside the window).

    Keyed off the node's declared ``latent_signal`` (``metric`` daily_deaths / ``pattern``
    rising_slope), so it is generic to any such node, not hardcoded to DP06/H5.
    """
    window = params.harm_wake_days
    next_day = state.day_index + 1
    for dp in decision_points:
        # enabled_nodes is None => all nodes enabled (the project convention); otherwise a
        # disabled/ablated node must not alter the run's turn cadence.
        if enabled_nodes is not None and dp.id not in enabled_nodes:
            continue
        ls = dp.latent_signal
        if not ls or ls.get("metric") != "daily_deaths" or ls.get("pattern") != "rising_slope":
            continue
        if not (dp.opens_day <= next_day <= dp.deadline_day):
            continue  # only while the node's own window is open
        hid = ls.get("house_id")
        if not isinstance(hid, str) or state.world.bird_count.get(hid, 0) <= 0:
            continue  # missing/malformed house_id, or empty house — no mortality signal
        hw = state.welfare.houses.get(hid)
        if hw is None:
            continue
        last_day = hw.usda_trigger_last_day
        if last_day >= dp.opens_day and (next_day - last_day) < window:
            return True
    return False
