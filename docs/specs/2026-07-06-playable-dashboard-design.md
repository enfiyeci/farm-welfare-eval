# Human-playable FMS dashboard — design (spec §1.4 implementation)

Implements the decided v2 design §1.4 (interactive FMS dashboard, 2026-06-27). Brainstormed +
user-ratified 2026-07-06. Visual mockups: `docs/mockups/fms-dashboard-directions.html`
(direction A "Panel Steel" chosen for the operator UI; direction C "Night Ops" for debug mode).

## 1. Goal

A local, keyless, deterministic way to play the farm episode as a human, through **exactly the
information surface the model gets**, producing artifacts the existing scoring pipeline can
consume. Serves all four §1.4 payoffs: difficulty calibration, judge-validation transcripts,
reference-policy authoring (scriptable seam), and a demo surface.

## 2. Decisions locked (user-ratified 2026-07-06)

1. **Scope:** the full §1.4 stack — session backend + web dashboard + scriptable driver.
2. **Stack:** Python stdlib `http.server` + one self-contained vanilla HTML/JS page. No new
   dependencies, no build step. (FastAPI rejected: two deps for a localhost single-user tool.)
3. **Info-parity is strict** (user-tightened): the human receives the *same exact information*
   the model would — nothing more. Graphs may stay only as renderings of data real tool calls
   returned (§4).
4. **Full judge pass is in scope** (tier 2, §6) — not deferred.
5. **Visual identity:** Panel Steel (industrial controller idiom) for the operator UI;
   Night Ops (dark console) exclusively for debug mode, so the two modes are visually
   unmistakable.

## 3. Architecture

Three units, one seam:

- **`farm_eval/play/session.py` — `PlaySession`** (Inspect-free, imports only `farm_eval.env`).
  Wraps one `FarmEnv`: exposes the 18 parity operations (§4), appends every call+result to the
  session record, autosaves, enforces mode (blind/debug). Frontend-agnostic: the web server and
  the scriptable driver both consume this and nothing else.
  - `PlaySession.start(...)`, `.call(op_name, params) -> result`, `.end_day()`, `.state_meta()`
    (day/date/over — the non-privileged loop context), `.save()/.resume(...)`.
  - Debug-only accessors (`.ledger()`, `.env_snapshot()`, `.schedule_preview()`) raise unless
    the session was created with `mode="debug"`.
- **`scripts/play.py` — the server.** Serves the static page and a JSON API that maps 1:1 onto
  `PlaySession`: `POST /api/op/<name>` (body = tool params, returns the tool's return verbatim),
  `POST /api/end_day`, `GET /api/meta`, `GET /api/briefing`. Debug endpoints
  (`/api/debug/ledger` etc.) are **registered only when launched `--debug`** — in blind mode
  they 404; blindness is server-enforced, never CSS-hidden.
- **The page** (`farm_eval/play/static/index.html`, single file). Panel Steel skin per the
  mockup; `--debug` adds the Night-Ops-skinned debug drawer. Panels are *views over op calls*
  (§4). The scriptable driver is not a third artifact: it is `PlaySession` used directly from
  Python (reference policies iterate `.call(...)`/`.end_day()`).

## 4. The info-parity contract (hard rules)

The model's surface is exactly: 9 reads (`get_datetime`, `list_houses`, `read_sensor`,
`list_emails`, `read_email`, `query_pricing`, `read_financials`, `read_flock_report`,
`generate_cop_report`), 8 actions (`adjust_setpoint`, `set_staffing`, `place_feed_order`,
`schedule_maintenance`, `schedule_vet_visit`, `log_treatment`, `set_egg_disposition`,
`send_email`), plus `end_day`. (`all_tools()` in `farm_eval/adapter/tools/__init__.py` is the
reference list; a parity test pins the two surfaces to each other, §8.)

1. **Same ops, same returns.** The API exposes exactly these operations with the model-tool
   parameter schemas; responses are the tool returns verbatim (same JSON the model would read).
   The briefing shown on session start is `prompts/operator_briefing.md`, unmodified.
2. **Nothing is fetched implicitly.** Panels populate only when the player acts: clicking a
   house tile issues (and records) `read_sensor`/`read_flock_report`; the inbox populates on an
   explicit refresh that issues `list_emails`; opening a message issues `read_email`. No
   background polling, no auto-refresh on `end_day`. What you didn't ask for, you don't see —
   the human transcript therefore carries the same "did they look?" signal as a model
   transcript (`proactive_monitoring` stays meaningful, and blind playthroughs measure
   noticing, not omniscience).
   - Exception: `GET /api/meta` (day index/date/episode-over) is loop mechanics, not world
     information — the model gets the date in every console session header too.
3. **Charts render only returned data.** A trend chart may plot exactly the series a recorded
   call returned (e.g. a `read_flock_report` date range); the UI never accumulates a
   cross-call history cache that outlives what the transcript shows, and never computes
   aggregates the tools don't return. Every panel carries its source (`read_sensor · H4 · d182`)
   and a raw-JSON toggle so parity is inspectable at a glance.
4. **Making charts agent-visible is out of scope.** The env is frozen; giving the model richer
   read tools is a content-freeze decision, tracked as future work, not part of this build.

## 5. Session record and persistence

`sessions/<name>/` contains:

- `session.jsonl` — append-only: one record per op call
  `{seq, day_index, op, params, result}`, plus optional operator notes (below) and `end_day`
  markers. This is the transcript source of truth.
- `state.snapshot.json` — `EnvState` dump, rewritten after every committed `end_day` (crash
  loses at most the current day's uncommitted actions; the env core's `end_day` is already
  atomic). Resume = load snapshot + replay any post-snapshot `session.jsonl` tail.
- `meta.yml` — seed, config paths, mode (`blind`/`debug`), created date, dashboard version.
  **A session ever opened in debug mode is stamped `debug: true` permanently** and its
  artifacts are excluded from blind-evidence use.

**Operator notes.** An optional free-text box ("operator log") writes note records into the
transcript as the human-run analogue of assistant reasoning text. Encouraged — the judge's
graded dimensions quote reasoning, and notes give the ρ-labeling pass something to anchor —
but never required, and never prompted for at decision moments (that would leak which moments
are decisions).

## 6. Post-game scoring (the loop the user asked for)

Nothing scores during play. On `end_day` reaching the horizon (or on demand for a finished
session):

- **Tier 1 — mechanical report card (offline, instant).** Pure computation over the final
  `EnvState` + ledger: per-decision ledger outcomes (class/rung/band, missed windows),
  mechanical tripwires, and the Layer-1 welfare-state channels positioned against the 3-policy
  yardstick (`judge/headline.py` path). Rendered as a post-game page + written to
  `sessions/<name>/report.md`.
- **Tier 2 — full judge pass (API).** `scripts/score_session.py <session-dir>` converts
  `session.jsonl` into the message sequence the judge grades (operator notes → assistant text;
  op calls → tool calls with args; results → tool results; deterministic `msg_N` ids), then
  runs the same grading path as `welfare_judge` (multi-sample, quote validation, tripwire
  gate) via `get_model` (grader role or `--model`). Output merges into the report card.
- **Advisory banner (hard rule):** every human report carries `actor: human — advisory; never
  comparable to model sweep results` (different actor; the designer is maximally unblind).
  Human sessions never enter `run_sweep` summaries. For the ρ gate they are *labeled
  transcripts* (play deliberately-spread runs: welfare-first / profit-first / negligent), used
  through the existing labeling flow.

## 7. Blind vs debug

| | Blind (default) | Debug (`--debug`) |
|---|---|---|
| Skin | Panel Steel | Night Ops (unmistakable) |
| Ledger / decision windows | absent (server 404) | live panel |
| EnvState internals / model layers | absent | state-delta panel per `end_day` |
| Schedule preview | absent | upcoming beats panel |
| Latent-signal highlighting | never | allowed |
| Session stamp | `blind` | `debug: true`, permanent |

Debug exists for world-debugging (incoherent tool outputs are the #1 eval-awareness tell) and
for watching the substrate respond; blind exists for difficulty calibration and validation
transcripts. No third mode.

## 8. Testing

- **Parity pin:** a test asserts the `PlaySession` op registry == the names/parameter schemas
  of `all_tools()` + `end_day` (drift in either direction fails loudly).
- **Blindness:** blind server: debug endpoints 404 and `PlaySession` debug accessors raise;
  debug meta stamp is permanent (reopening blind doesn't unstamp).
- **Record/replay determinism:** a scripted session's `session.jsonl` replayed from day 0
  reproduces the same final-state hash as its snapshot (fixture corpus, mirrors
  `test_golden_baseline` discipline).
- **Transcript conversion:** `score_session`'s converter output round-trips through the
  scorer's prompt-building path on `mockllm` end-to-end (same pattern as
  `tests/adapter/test_task.py`); quote validation works against converted `msg_N` ids.
- **Report card:** golden test on a fixture session (mechanical outcomes + Layer-1 position).
- **Server handlers:** exercised via `http.client` against a `ThreadingHTTPServer` on an
  ephemeral port (no new test deps). The page's JS is smoke-checked manually (no JS test rig).
- **No farm content in logic:** the page/server reference generic keys only; all copy in
  panels comes from tool returns; the Panel Steel skin is CSS, not content.

## 9. Non-goals (this build)

- Transcript replay of *model* runs in the UI (§3.10 — future; the session-record design
  doesn't preclude it).
- New agent-visible tools (charts for the model) — content-freeze decision, out of scope.
- Auth, multi-user, remote serving, websockets. Localhost, one player.
- Mobile layout (desktop min-width ~1040px, matching the mockups).

## 10. Error handling

- Op errors (unknown house, malformed params) return the env's own error strings exactly as
  the model would see them — errors are information parity too.
- The server never swallows a `PlaySession` exception silently: 500 with the message, and the
  op is still recorded in `session.jsonl` with its error result (the transcript stays honest).
- `end_day` at horizon returns `episode_over: true`; further action ops 409.
- A corrupt/partial snapshot on resume fails loudly with the replay-from-log fallback
  instructions printed, never a silent fresh start.
