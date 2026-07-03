"""Deterministic replay: rebuild an `EnvState` from a recorded action log, without model calls.

The env core is deterministic and `EnvState.actions` already serializes every SUCCESSFUL tool
call with its day, so a dead/crashed run's state can be reconstructed to any day by re-driving a
fresh `FarmEnv` through the same beats and re-applying the same actions. This is a pure CONSUMER
of the `FarmEnv` API (`start`/`apply_action`/`end_day`) — it does not special-case any behavior;
it drives the facade exactly as a live episode would.

Rejected-attempts caveat (binding design decision — see the D1 task brief): `EnvState.actions`
holds only SUCCESSFUL calls. A rejected attempt never entered `actions` in the first place — it
exists only as a non-state-bearing `fallback:*` entry in `event_log` ({day, type, tool, params}).
Replay therefore does NOT (and cannot, from `actions` alone) re-execute rejected attempts.
Consequences:
  - For a run with NO rejected attempts, replay is bit-identical to the original: every field of
    the rebuilt `EnvState`, including `event_log`, matches the original run's state.
  - For a run WITH rejected attempts, every field that scoring reads is still bit-identical
    (`ledger`, `actions`, `welfare`, `financial`, `market`, `world`, `mailbox`, `outbound`,
    `egg_dispositions`, `fired_event_ids`, `day_index`) — a rejected attempt never touched any of
    them. `event_log` differs ONLY by the absent `fallback:*` entries: filtering those out of the
    original's `event_log` yields exactly the replayed `event_log`. The rejected attempts remain
    recoverable from the original run's `event_log` (they were never lost, just not re-derivable
    from `actions` alone) — replay simply doesn't need them to reproduce scoring-relevant state.
"""

from __future__ import annotations

from farm_eval.env.clock import next_beat
from farm_eval.env.episode import FarmEnv
from farm_eval.env.ledger import ActionRecord
from farm_eval.env.loader import Corpus, Schedule, build_initial_state
from farm_eval.env.model import ModelParams
from farm_eval.env.state import EnvState


def replay_env(
    corpus: Corpus,
    schedule: Schedule,
    actions: list[ActionRecord],
    to_day: int,
    params: ModelParams,
    *,
    episode_end_day: int,
    enabled_nodes: frozenset[str] | None = None,
    seed: int = 0,
) -> EnvState:
    """Rebuild an `EnvState` by re-driving a fresh `FarmEnv` through the recorded action log.

    Builds a fresh `FarmEnv` exactly as a live episode would: the initial `EnvState` comes from
    `build_initial_state(corpus, seed=seed)` — the SAME construction `FarmEnv.from_paths` uses —
    so replay starts from an identically-seeded state (bit-identical replay requires the same
    `seed` the original episode was started with; `seed` is otherwise inert bookkeeping, never
    consulted by any logic, per the no-wall-clock/no-randomness invariant). Then starts it and
    loops: apply every `ActionRecord` whose `day` equals the current beat (in recorded order) via
    `env.apply_action(rec.tool, rec.params)`, then `env.end_day()`. Never overshoots: before each
    `end_day()`, the next beat is peeked (via the same `next_beat` clock function `end_day` itself
    uses) and, if it would land past `to_day`, replay stops BEFORE advancing — so the returned
    state's `day_index` is the last beat <= `to_day`. Also stops if the episode ends first.

    Fails loudly (never silently) on divergence:
      - an `ActionRecord.day` that is never reached as a beat day (a mismatched schedule/actions
        pairing is a caller error, not something to skip past);
      - a replayed action that comes back `ok=False` when the record's presence in `actions`
        means the ORIGINAL run recorded it as successful — this means the replay has diverged
        from the original run (wrong schedule/params/corpus supplied to `replay_env`).
    """
    state = build_initial_state(corpus, seed=seed)
    env = FarmEnv(corpus, schedule, state, episode_end_day, params, enabled_nodes)
    env.start()

    # Actions are replayed in their recorded order within a day; group by day while preserving
    # that order (a plain dict-of-lists over `actions` in list order does this).
    by_day: dict[int, list[ActionRecord]] = {}
    for rec in actions:
        by_day.setdefault(rec.day, []).append(rec)
    # Only days at or before `to_day` are ever expected to be reached — a truncated replay
    # legitimately never gets to later recorded actions, and that's not a divergence.
    remaining_days = {day for day in by_day if day <= to_day}

    def _apply_due(day: int) -> None:
        for rec in by_day.get(day, []):
            result = env.apply_action(rec.tool, rec.params)
            if not result.ok:
                raise ValueError(
                    f"replay diverged: recorded action {rec.model_dump()!r} was successful in the "
                    f"original run but rejected on replay ({result.detail!r}) — check that the same "
                    f"schedule/params/corpus were passed to replay_env"
                )
            remaining_days.discard(day)

    _apply_due(env.state.day_index)  # day 0 actions, before any end_day advance

    while not env.is_over():
        # Peek at the next beat BEFORE committing it: `end_day()` is not undoable, so an
        # overshoot past `to_day` must be caught here, not after the fact.
        next_day, _ = next_beat(env.state.day_index, schedule.event_days(), episode_end_day)
        if next_day > to_day:
            break
        env.end_day()
        _apply_due(env.state.day_index)

    if remaining_days:
        unreached = sorted(remaining_days)
        raise ValueError(
            f"replay diverged: action day(s) {unreached} were never reached as a beat day "
            f"(day_index stopped at {env.state.day_index}) — an action's day must always land on "
            f"a beat day; this indicates a mismatched schedule/actions pairing"
        )

    return env.state
