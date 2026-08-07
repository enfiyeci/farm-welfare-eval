# Task D1 — Deterministic replay: rebuild EnvState from the action log (TDD)

Deterministic egg-farm operations simulator; no live models. Work only in the worktree
`/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/c6-env-levers`. Tests:
`./venv/bin/python -m pytest -q`. Strict TDD. Baseline suite count comes in your dispatch message.

## Why
Pilot-hardening (a grader crash nearly cost a full paid episode). The env core is deterministic and
`EnvState.actions` already serializes every successful tool call with its day — so a dead run's
state can be rebuilt to any day without model calls, enabling partial scoring and forensic what-ifs.

## Interface
New `farm_eval/env/replay.py`:

```
def replay_env(corpus, schedule, actions: list[ActionRecord], to_day: int, params,
               *, episode_end_day: int, enabled_nodes: frozenset[str] | None = None) -> EnvState
```

Mirror `FarmEnv.__init__`'s construction inputs exactly (read `farm_eval/env/episode.py` — pass
through whatever it needs, e.g. seed, in the same way; if its signature carries other required
pieces, mirror them and keep the mirroring obvious). Algorithm:

1. Build a fresh `FarmEnv` exactly as a live episode would; `env.start()`.
2. Loop: apply every `ActionRecord` whose `day == state.day_index` (in list order) via
   `env.apply_action(rec.tool, rec.params)`; then `env.end_day()`. Stop when
   `state.day_index >= to_day` (do not overshoot: if the next beat jumps past `to_day`, stop
   BEFORE advancing — the returned state's `day_index` is the last beat ≤ `to_day`) or the episode
   is over.
3. Return `env.state` (the plain-pydantic EnvState).

Notes that are binding:
- `end_day` advances beat-to-beat (`next_beat`), and agents only act on beat days, so
  `ActionRecord.day` values always land on beat days — assert-or-raise loudly if an action's day
  can never be reached (a mismatched schedule/actions pairing is a caller error, not a skip).
- Actions are replayed in their recorded order within a day.
- A replayed action that comes back `ok=False` when the original recorded it as successful means
  the replay diverged (wrong schedule/params/corpus) — raise loudly with the record, never continue
  silently.

## The rejected-attempts caveat (design decision, already ruled — implement as stated)
`EnvState.actions` holds only SUCCESSFUL calls; rejected attempts exist only as non-state-bearing
`fallback:*` entries in `event_log` ({day, type, tool, params}). Replay does NOT re-execute
rejected attempts. Consequences you must encode in tests + the module docstring:
- For a run with no rejected attempts, replay is **bit-identical**: `model_dump()` of original vs
  replayed state compares equal, including `event_log`.
- For a run WITH rejected attempts, everything scoring-relevant is bit-identical — `ledger`,
  `actions`, `welfare` (incl. harm accumulators), `financial`, `market`, `world`, `mailbox`,
  `outbound`, `egg_dispositions`, `fired_event_ids`, `day_index` — and `event_log` differs ONLY by
  the absent `fallback:*` entries (assert exactly that: filtering fallback entries out of the
  original event_log yields the replayed event_log). Rejected attempts remain recoverable from the
  original log; document this limitation in the docstring.

## TDD — tests FIRST (`tests/env/test_replay.py`; build envs from `tests/fixtures/` like existing
env tests)
1. Bit-identical full replay: drive a fixture episode imperatively (start, several beats, a realistic
   mix of successful actions across days — setpoints, feed order, staffing, disposition, send_email,
   treatment), capture the final state; `replay_env` from its `actions` to the final day; compare
   `model_dump()` equal. (Serialize both to JSON strings if that makes the diff readable.)
2. Rejection caveat: same but include 1–2 REJECTED attempts mid-run (e.g. absurd feed order); assert
   the scoring-relevant fields bit-identical and the event_log fallback-filter property above.
3. Truncated replay: `to_day` mid-episode → returned `day_index` is the last beat ≤ `to_day`;
   ledger contains resolutions ONLY for windows whose deadline ≤ that day (later nodes still open or
   absent — "resolves only due windows"); no overshoot integration (welfare accumulators strictly
   less than the full run's).
4. Divergence fail-loud: replay with a doctored record (e.g. an action whose day is not a beat day,
   or params the env now rejects) raises with a message naming the record.
5. `enabled_nodes` pass-through: a replay with a restricted node set seeds only those nodes (mirror
   the B1 behavior).

Then RUN THE FULL SUITE. Zero existing-test changes expected (pure addition).

## Constraints
- Pure env-core module: no Inspect imports, no adapter imports, no wall-clock/random.
- Do NOT modify `episode.py`/`events.py` behavior — replay is a CONSUMER of the existing API. If
  you find the existing API genuinely insufficient for the contract above, STOP and report rather
  than patching the core.
- Partial-scoring/"unresolved nodes" REPORTING is the scoring layer's job — out of scope here;
  D1 only rebuilds state.
- Commit: `feat(env): deterministic replay — rebuild EnvState from the action log` with the exact
  trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Targeted `git add` only.

## Done when
Replay reproduces a full run bit-identically (modulo the documented rejected-attempt caveat),
truncated replays resolve only due windows, divergence fails loudly; full suite green. Report:
files changed, new test names, suite counts, and any API-insufficiency you hit.
