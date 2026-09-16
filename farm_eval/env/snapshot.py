"""Derive a node episode's starting snapshot: the routine-only world at `start_day` (D1-D4).

Drives the SAME FarmEnv facade a live episode uses (start/apply_action/end_day) with no agent
actions except the manifest's prelude branch, stops on the last routine beat before start_day,
then advances once more to start_day and captures that hop as the opening digest in the exact
`DayAdvanceResult.summary` format the model sees after every `end_day`. Deterministic, no RNG,
no model tokens - so every model starts every episode from a byte-identical state.
"""

from __future__ import annotations

from farm_eval.env.clock import date_for_day, next_beat
from farm_eval.env.digest import build_digest
from farm_eval.env.episode import FarmEnv
from farm_eval.env.loader import Corpus, Schedule, build_initial_state
from farm_eval.env.model import ModelParams
from farm_eval.env.node_episodes import ResolvedEpisode
from farm_eval.env.state import EnvState


def derive_snapshot(
    corpus: Corpus,
    schedule: Schedule,
    params: ModelParams,
    ep: ResolvedEpisode,
    *,
    seed: int = 0,
) -> tuple[EnvState, str]:
    """Return (state at ep.start_day, opening digest text).

    Prelude actions are applied on their own day, through `apply_action`, and a rejection is a
    manifest error (fail loud - a silently-skipped branch would change the world every model
    sees).
    """
    enabled = frozenset(ep.enabled_nodes)
    state = build_initial_state(corpus, seed=seed, params=params)
    env = FarmEnv(
        corpus, schedule, state, ep.end_day, params, enabled,
        allow_empty_nodes=not ep.scored,
    )
    env.start()
    pending = sorted(ep.prelude_actions, key=lambda a: a.day)

    def _apply_due(day: int) -> None:
        while pending and pending[0].day <= day:
            action = pending.pop(0)
            if action.day != day:
                raise ValueError(
                    f"prelude action for day {action.day} was never reached as a beat "
                    f"(clock is at {day}); prelude days must be schedule beat days"
                )
            result = env.apply_action(action.tool, dict(action.params))
            if not result.ok:
                raise ValueError(
                    f"prelude action rejected on day {day}: {action.tool} {action.params!r} -> {result.detail!r}"
                )

    _apply_due(env.current_day())
    # Routine beats up to (not including) start_day: the schedule's own calendar, as a live
    # continuous run would walk it.
    while True:
        nxt, _ = next_beat(env.current_day(), schedule.event_days(), ep.end_day)
        if nxt >= ep.start_day:
            break
        env.end_day()
        _apply_due(env.current_day())
    if pending:
        raise ValueError(f"prelude action(s) on day(s) {[a.day for a in pending]} never applied")

    before = env.state.model_copy(deep=True)
    # Land on start_day. The daily-wake caps may take more than one hop; the digest below spans
    # the WHOLE gap from the last routine beat, which is what "since your last session" means.
    while env.current_day() < ep.start_day:
        env.end_day()
    if env.current_day() != ep.start_day:
        raise RuntimeError(f"snapshot overshot start_day {ep.start_day}: clock at {env.current_day()}")

    # D3: the predecessor sessions handled everything before today.
    for mail in env.state.mailbox:
        if mail.day < ep.start_day:
            mail.unread = False

    elapsed = ep.start_day - before.day_index
    summary = (
        f"{elapsed} day(s) pass. It is now {date_for_day(env.state.start_date, ep.start_day)}.\n"
        f"{build_digest(before, env.state, corpus.digest_flavor)}"
    )
    if ep.digest_note:
        summary += f"\n- {ep.digest_note}"
    return env.state, summary
