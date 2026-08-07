# Task D1 report — deterministic replay

## Status
DONE

## Commit
`c7c8aa2` — `feat(env): deterministic replay — rebuild EnvState from the action log`
(trailer `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>` included).

## Files changed
- `farm_eval/env/replay.py` (new) — `replay_env()`.
- `tests/env/test_replay.py` (new) — 6 tests.

Targeted `git add` only (`farm_eval/env/replay.py tests/env/test_replay.py`); untracked
`.superpowers/`, `scratchpad/`, `uv.lock` left alone.

## New tests (`tests/env/test_replay.py`)
1. `test_full_replay_is_bit_identical_when_no_rejections` — drives a realistic multi-beat
   episode (setpoint, feed order, staffing, send_email, set_egg_disposition, log_treatment,
   across days 0/5/10/20/30 plus the run-out to episode end), replays from `actions`, asserts
   `model_dump()` JSON-equal.
2. `test_replay_with_rejected_attempts_matches_on_scoring_relevant_fields` — same, with an
   absurd feed order (999M tons) and a negative staffing level interleaved as rejected attempts;
   asserts every scoring-relevant field (`ledger`, `actions`, `welfare`, `financial`, `market`,
   `world`, `mailbox`, `outbound`, `egg_dispositions`, `fired_event_ids`, `day_index`) bit-equal,
   and that filtering `fallback:*` entries out of the original `event_log` yields exactly the
   replayed `event_log`.
3. `test_truncated_replay_stops_at_last_beat_leq_to_day_and_resolves_only_due_windows` —
   `to_day=15` (between the day-10 and day-20 beats) stops at day 10, not day 20; asserts
   `DP_PLACEHOLDER_1` (deadline day 5) is resolved by day 10; asserts the truncated run's
   `nh3_ppm_hours_over` accumulator is `<=` the full run's (monotonic, no overshoot integration).
4. `test_replay_raises_loudly_on_a_doctored_action_day` — an action's `day` bumped to a
   non-beat day raises, message names the day (asserted via regex matching the record's day
   value).
5. `test_replay_raises_loudly_when_a_recorded_success_now_rejects` — a recorded
   `adjust_setpoint`'s `system` mutated to an unknown value (was successful originally) raises
   on replay because `apply_action` now rejects it.
6. `test_enabled_nodes_pass_through_seeds_only_selected_nodes` — `enabled_nodes={"DP_PLACEHOLDER_1"}`
   on both the original drive and the replay; asserts the ledger only ever contains that one
   node, and the replayed state is bit-identical to the original.

All 6 watched RED first (`ModuleNotFoundError: No module named 'farm_eval.env.replay'`) before
`replay.py` was written, per strict TDD.

## Suite counts
- Baseline (HEAD `1f1810a`, before this task): 654 passed, 1 skipped.
- After this task: **660 passed, 1 skipped** (654 + 6 new, zero regressions, zero
  failures/errors). Confirmed via dot-count (`pytest -q -p no:warnings`, since the trailing
  summary line was oddly swallowed in this shell/pytest combo — dot/`s` counting was used as a
  reliable cross-check) and via `pytest --co -q` collection tail.

## API-insufficiency encountered
None requiring an `episode.py`/`events.py` change. `replay.py` is a pure consumer of the existing
`FarmEnv` surface (`build_initial_state`, `FarmEnv.__init__`, `start`, `apply_action`, `end_day`,
`is_over`) plus the pure `clock.next_beat` helper (used to *peek* the next beat day before
committing it, so an overshoot past `to_day` can be caught before `end_day()`'s irreversible
commit — `end_day` itself has no "peek" mode, but `next_beat` is already a free function the
facade itself calls, so no facade change was needed).

One thing worth flagging for awareness (not a blocker, handled within `replay.py`/tests, not by
touching the core): the illustrative interface signature in the brief omits `seed`, but
`FarmEnv.from_paths`/`build_initial_state` need a `seed` to construct the initial `EnvState`
identically to the original episode (it's inert bookkeeping stored on `EnvState.seed`, never
consulted by any logic, but still participates in `model_dump()` equality). Per the brief's own
guidance ("pass through whatever it needs, e.g. seed... if its signature carries other required
pieces, mirror them and keep the mirroring obvious"), I added `seed: int = 0` as a keyword-only
parameter, defaulted to match `FarmEnv.from_paths`'s default.

## Self-review notes
- Initial implementation had a real bug caught during TDD: I first wrote the overshoot check to
  inspect `end_day()`'s return value AFTER calling it — too late, since `end_day()` commits
  irreversibly. Fixed by peeking via `next_beat(...)` (the same clock function `end_day` uses
  internally) BEFORE calling `end_day()`, only advancing if the next beat is `<= to_day`.
- Second bug caught by the truncated-replay test: the "unreached action day" divergence check
  originally scanned the FULL action list for days never reached, which incorrectly fired for a
  legitimately truncated replay (actions recorded on days after `to_day` are *expected* to be
  unreached, not a divergence). Fixed by scoping the "must be reached" set to
  `{day for day in by_day if day <= to_day}`.
- Third bug caught by my own test driver: I initially called `env.set_egg_disposition(...)`
  directly in the realistic-episode driver, which bypasses `apply_action`/`record_tool_call` and
  so never lands in `EnvState.actions` — meaning a replay driven from `actions` would silently
  never reproduce it. Fixed the test driver to go through `apply_action("set_egg_disposition",
  ...)`, the only path that's actually replayable; this incidentally reinforces the module
  docstring's point that replay is scoped to what `actions` records.
- Verified both divergence paths manually (outside pytest) to confirm the raised messages
  actually name the offending record/day, not just "an exception happened to be raised for some
  unrelated reason":
  - doctored day: `"replay diverged: action day(s) [3] were never reached as a beat day ..."`
  - doctored params: `"replay diverged: recorded action {...} was successful in the original run
    but rejected on replay (\"Controller rejects unknown system 'not_a_real_system'...\") ..."`
- Confirmed `to_day=0` and `to_day` far beyond `episode_end_day` both behave correctly (stop at
  day 0 with day-0 actions applied once; cap at `episode_end_day` via `is_over()`).
- Not covered (explicitly out of scope per the brief): negative `to_day` values, and any
  "unresolved nodes" reporting layer (the brief reserves that for the scoring layer, D1 only
  rebuilds state).
- No changes to `episode.py`/`events.py`/`tracker.py` — confirmed via `git status`/`git diff`
  before commit; only the two new files were staged.

---

# Review-fix addendum (commit `6976d04`)

Coordinator relayed two codex review findings against `c7c8aa2`; both fixed via TDD.

## F1 (Critical) — reads are state-bearing
`replay_env` ignored `EnvState.reads`, but the adapter read tools (`get_sensor`/
`read_flock_report`) append to `state.reads` via `tracker.record_read` (tracker.py:261 — the
exact seam mirrored), and `end_day()` runs `tracker.resolve_inspected`, which sets ledger
entries' `inspected` recognition flags from that log. A rejection-free run that used any read
tool therefore replayed to `reads=[]` / `inspected=False`, violating bit-identity and changing
scoring metadata (diagnostic only — never gates the headline — but feeds recognition analysis).

Fix: `replay_env` gains `reads: list[ActionRecord] | None = None`. Reads are grouped by day
(original list order preserved) and re-appended as fresh `ActionRecord` copies (mirroring
`record_read`; never aliasing the caller's list) on arrival at each beat day, BEFORE that day's
`end_day()` — matching the live lifecycle (reads happen during the day, resolved at that day's
end_day). Same fail-loud rule as actions: a read whose day (<= to_day) is never reached as a
beat raises a ValueError naming the day(s) ("read day(s) [...] were never reached..."). Module +
function docstrings updated: salvage callers pass BOTH `state.actions` and `state.reads`.

## F2 (Important) — negative to_day
`to_day < 0` previously still built/started the env (firing day-0 events) and returned a day-0
state already PAST the requested target. Now guarded as the very first statement:
`ValueError("to_day=... is before day 0: no beat <= to_day exists...")`, before any construction
or day-0 event firing. Day 0 remains the first valid target.

## Deferred (recorded, per coordinator — NOT implemented)
Seed-API polish (deriving seed from the original `EnvState` instead of a parameter). Task
reviewer verified a wrong seed only differs in the cosmetic `seed` field.

## New tests (3, `tests/env/test_replay.py`)
1. `test_replay_with_reads_is_bit_identical_including_inspected_flags` — drives an episode with
   day-0 reads on DP_PLACEHOLDER_1's surface house (original: `inspected=True`, non-empty
   `reads`); asserts the no-reads replay FAILS bit-identity (`reads=[]`, `inspected=False`,
   dumps differ — kept as a permanent assertion documenting why `reads` is in the contract);
   asserts the with-reads replay is fully `model_dump()`-identical including the reads list and
   inspected flags. Also includes a later-day read for reads-list ordering fidelity.
2. `test_replay_raises_loudly_on_a_doctored_read_day` — a read doctored to non-beat day 3 raises
   with a message naming the day (strict regex `read day\(s\) \[3\]` — deliberately tightened
   after the initial loose `"read"` regex passed spuriously on the red-phase TypeError).
3. `test_replay_rejects_negative_to_day` — `to_day=-1` raises ValueError mentioning `to_day`.

All 3 watched RED for the right reasons first (TypeError: unexpected keyword `reads` ×2 after
the regex tightening; DID NOT RAISE for F2), then GREEN after the fix.

## Suite counts after fix
**663 passed, 1 skipped** (post-D1 baseline 660 + 3 new; zero regressions). Verified by
dot-count under `pytest -q -p no:warnings` (same summary-line quirk as before).

## Self-review notes (addendum)
- Injection order within a day (reads before actions) is arbitrary and documented as such:
  they land in separate state lists and nothing consults either until end_day.
- Reads on the final reached day are injected on arrival even though no further end_day
  resolves them — matching a live run where post-last-advance reads sit unresolved in the log.
- Reads with day > to_day are silently not required (truncated-replay symmetry with actions).
- `env.state.reads` is re-read on every injection (never held across `end_day`, which replaces
  state field objects on commit).
