# Henhouse Spectator Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Live + replay spectator dashboard for eval runs: an Inspect-hooks NDJSON feed emitter, a `.eval` replay extractor sharing the same translation core, a stdlib HTTP server, and a single-file page (Midnight Barn theme) with six extras.

**Architecture:** A stateful `Translator` turns the per-sample Inspect event stream into typed NDJSON feed events; the live emitter (Inspect `@hooks`) and the replay extractor both drive it, so live and replay are one code path. A stdlib server serves the page + feed; the page renders everything client-side. Spec: `docs/specs/2026-08-04-spectator-dashboard-design.md` (READ IT FIRST — it is the contract; its §2 guardrails are non-negotiable).

**Tech Stack:** Python 3.11+ (pydantic v2, stdlib `http.server`), inspect_ai 0.3.244 (installed at `./venv`), vanilla HTML/CSS/JS (no build step, no new runtime deps).

## Global Constraints

- venv is at `./venv` (NOT `.venv`); run tests with `./venv/bin/python -m pytest -q`.
- pydantic v2, all new models `extra="forbid"`.
- NO farm content hardcoded in logic — email bodies travel in the feed; UI labels generic.
- The emitter must be failure-isolated: an exception inside it may never propagate into the run, and it must never mutate agent-visible state or the ledger.
- The emitter must NOT read the live `EpisodeStore` (async hook queue) — state comes only from applying `StoreEvent` patches in order (spec §2).
- Feeds are per sample: `<FARM_SPECTATOR_DIR>/<run_id>/<sample_id>/feed.ndjson`.
- Decisions KPI denominator from `run_meta.enabled_nodes` (22 in current `config.yml`), never hardcoded.
- Breed standard label: Hy-Line **W-36** (`farm_eval/env/model/params.py:34`).
- Bookmark export is `annotations.csv` — explicitly NOT `judge/validate.py` input.
- Commits end with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
- Approved visual reference: `docs/specs/assets/2026-08-04-spectator-dashboard/*.html` — prose spec wins over mockups (three known stale spots listed in the spec header).

---

### Task 1: Feed event models + NDJSON I/O (`events.py`)

**Files:**
- Create: `farm_eval/spectator/__init__.py` (empty), `farm_eval/spectator/events.py`
- Test: `tests/spectator/test_events.py` (+ empty `tests/spectator/__init__.py` if the suite needs it — mirror how other `tests/*` dirs do it)

**Interfaces (Produces — later tasks import exactly these):**
```python
from farm_eval.spectator.events import (
    FeedEvent,            # Annotated union, discriminator "kind"
    RunMeta, DayStart, DayEnd, AssistantText, ToolCallEvent,
    EmailDelivered, EmailRead, EmailSent, StateSnapshot,
    DecisionWindow, DecisionResolved, RunHealth, EpisodeEnd,
    dump_feed_line,       # (event: FeedEvent) -> str  (single line, no trailing \n)
    parse_feed_line,      # (line: str) -> FeedEvent   (raises ValidationError on unknown kind)
)
```
Envelope fields on every model: `seq: int`, `day: int | None`. Model-specific fields:
`RunMeta(run_id, sample_id, target, grader, first_day: int, last_day: int, config_path, enabled_nodes: int)` ·
`DayStart(date: str, season: str, weather: dict | None)` · `DayEnd()` ·
`AssistantText(text, msg_id: str | None)` ·
`ToolCallEvent(tool, args: dict, result_summary: str | None, cost_cents: float | None, msg_id: str | None)` ·
`EmailDelivered(email_id, sender, subject, body)` · `EmailRead(email_id)` ·
`EmailSent(recipient, subject: str | None, body)` ·
`StateSnapshot(houses: list[dict], totals: dict, finance: dict)` ·
`DecisionWindow(dp_id, opens: int, deadline: int)` ·
`DecisionResolved(dp_id, outcome: str | None, tripwire: bool, latency_days: int | None)` ·
`RunHealth(turns: int, blank_streak: int, retries: int, tokens_in: int, tokens_out: int, wallclock_s: float)` ·
`EpisodeEnd(status: str)`.
Each model sets `kind: Literal["..."] = "..."` (snake_case of the class, `ToolCallEvent` → `"tool_call"`).

- [ ] **Step 1: failing tests** — round-trip every model through `dump_feed_line`/`parse_feed_line`; `extra="forbid"` rejects a stray field; `parse_feed_line('{"kind":"bogus","seq":1,"day":0}')` raises; `dump_feed_line` output contains no `\n`.
- [ ] **Step 2:** `./venv/bin/python -m pytest tests/spectator/test_events.py -q` → FAIL (module missing).
- [ ] **Step 3:** implement with a discriminated union:
```python
FeedEvent = Annotated[RunMeta | DayStart | ... | EpisodeEnd, Field(discriminator="kind")]
_adapter = TypeAdapter(FeedEvent)
def dump_feed_line(e): return json.dumps(e.model_dump(mode="json"), separators=(",", ":"), ensure_ascii=False)
def parse_feed_line(line): return _adapter.validate_json(line)
```
- [ ] **Step 4:** tests pass. **Step 5:** commit `feat(spectator): typed NDJSON feed event models`.

### Task 2: Shadow store — JSON-Patch reconstruction of `EnvState` (`shadow.py`)

**Files:**
- Create: `farm_eval/spectator/shadow.py`
- Test: `tests/spectator/test_shadow.py`

**Interfaces:**
- Consumes: `inspect_ai.event._store.StoreEvent` (`.changes: list[JsonChange]`, each with `.op` (`"add"|"replace"|"remove"`), `.path` (JSON pointer), `.value`); `farm_eval.env.state.EnvState`.
- Produces:
```python
class ShadowStore:
    def apply(self, changes: list[JsonChange]) -> None: ...
    def env_state(self) -> EnvState | None:   # parses self._data["EpisodeStore:env_state"]; None if absent
    def raw(self) -> dict: ...
```

- [ ] **Step 1: failing tests** — apply `add` at `/EpisodeStore:env_state` with a minimal EnvState dump (build one via `EnvState` model in tests, `model_dump(mode="json")`); `replace` of a nested pointer (`/EpisodeStore:env_state/day_index`) updates it; `remove` deletes; unknown op raises `ValueError`; JSON-pointer escapes (`~0`,`~1`) handled; `env_state()` returns a validated `EnvState` and `None` before any apply.
- [ ] **Step 2:** run → FAIL. **Step 3:** implement a minimal RFC-6901 resolver + the three ops over a plain dict (lists: integer tokens + `-` append for `add`). ~60 lines, no deps.
- [ ] **Step 4:** pass. **Step 5:** commit `feat(spectator): shadow store rebuilds EnvState from StoreEvent patches`.

### Task 3: The translation core (`translate.py`)

**Files:**
- Create: `farm_eval/spectator/translate.py`
- Test: `tests/spectator/test_translate.py`

**Interfaces:**
- Consumes: Tasks 1–2; Inspect event classes (`ModelEvent`, `ToolEvent`, `StoreEvent` — import from `inspect_ai.event`; verify exact module with `./venv/bin/python -c "from inspect_ai.event import ModelEvent, ToolEvent, StoreEvent"` and adjust if the import path differs; also inspect fields via `ModelEvent.model_fields.keys()` before assuming).
- Produces:
```python
class Translator:
    def __init__(self, *, meta: RunMeta | None = None): ...   # emits meta first if given
    def handle(self, event) -> list[FeedEvent]: ...            # any Inspect transcript event; unknown types -> []
    def finish(self, status: str) -> list[FeedEvent]: ...      # EpisodeEnd
```
Stateful: seq counter; `ShadowStore`; last seen `day_index`; seen mailbox email ids; seen ledger entry count; token/turn accumulators.

**Translation rules (the heart — implement exactly):**
- `ModelEvent`: emit `AssistantText` for non-empty assistant text (msg id if present); accumulate tokens/turns → every 10th turn emit `RunHealth`.
- `ToolEvent`: emit `ToolCallEvent(tool=event.function, args=event.arguments, result_summary=str(event.result)[:400])`. Special cases: function `read_email` → also `EmailRead(email_id=args["email_id"])` (check the real arg name in `farm_eval/adapter/tools/`); `send_email` → also `EmailSent(recipient=..., body=...)` from args.
- `StoreEvent`: `shadow.apply(changes)`; then diff: (a) new mailbox entries → `EmailDelivered` with the **finalized body from the mailbox state** (find the mailbox field on `EnvState` in `farm_eval/env/state.py` and use its real shape); (b) `day_index` advanced → `DayEnd` for the old day, `StateSnapshot` (build `houses`/`totals`/`finance` dicts from `EnvState` — mirror the fields the FMS reports expose in `farm_eval/env/episode.py`), then `DayStart` (date from day index via `farm_eval/env/clock.py`; season from month; weather only if EnvState carries it); (c) new ledger entries → `DecisionResolved`; window opens are known from the schedule — emit `DecisionWindow` when `day_index` first reaches each decision's `opens` (load windows once from the schedule the same way `farm_eval/env/loader.py` does).
- Costs on `ToolCallEvent.cost_cents`: parse from the tool result ack when the FMS ack includes a service charge (grep `farm_eval/adapter/tools/` for the charge wording; if absent, leave None — do NOT recompute economics).

- [ ] **Step 1: failing tests** — synthetic minimal events (construct real `ModelEvent`/`ToolEvent`/`StoreEvent` instances): assistant text emits; send_email emits both events; a StoreEvent that advances `day_index` emits DayEnd+StateSnapshot+DayStart in that order with correct `seq` ordering; new mailbox entry emits EmailDelivered with body; unknown event type yields `[]`.
- [ ] **Step 2:** FAIL. **Step 3:** implement. **Step 4:** pass. **Step 5:** commit `feat(spectator): translator turns Inspect events into the feed`.

### Task 4: Replay extractor + the mockllm feed golden (`extract.py`)

**Files:**
- Create: `farm_eval/spectator/extract.py`, `tests/spectator/test_extract.py`, golden at `tests/spectator/goldens/feed.ndjson`

**Interfaces:**
- Consumes: `inspect_ai.log.read_eval_log(path)` → `EvalLog` with `log.samples[i].events`; Tasks 1–3.
- Produces: `extract_feed(log_path: str | Path, out_dir: Path) -> list[Path]` — one `<out_dir>/<run_id>/<sample_id>/feed.ndjson` per sample; returns written paths. `run_meta` built from `log.eval` (model roles, run id) + `enabled_nodes` from the task config recorded in the log (`log.eval.task_args` / config — inspect what's recorded and take it from there; fall back to counting `DecisionWindow`-capable nodes is NOT allowed — if absent, set from the config file referenced in task_args).
- [ ] **Step 1:** find the existing mockllm end-to-end pattern: `grep -rn "mockllm" tests/ | head` — reuse its config/fixture approach to produce a real `.eval` log inside the test (pytest tmp_path, `inspect_eval(farm_task(config_path=...), model="mockllm/model", log_dir=tmp)`).
- [ ] **Step 2: failing test** — run the mockllm episode, `extract_feed` it, assert: file exists; first line parses to `RunMeta`; ≥1 `StateSnapshot`; ≥1 `DayStart`; all lines parse via `parse_feed_line`; seq strictly increasing.
- [ ] **Step 3:** FAIL → implement → PASS.
- [ ] **Step 4: golden** — write the produced feed as `tests/spectator/goldens/feed.ndjson` with a regen script flag (mirror how `scripts/regen_golden.py` handles existing goldens — extend it or add `scripts/regen_spectator_golden.py`), and a test comparing fresh extraction to the golden byte-for-byte (excluding `RunHealth` lines and any wallclock field).
- [ ] **Step 5:** commit `feat(spectator): replay extractor + mockllm feed golden`.

### Task 5: Live emitter — hooks, registration, parity, isolation (`emitter.py`)

**Files:**
- Create: `farm_eval/spectator/emitter.py`, `tests/spectator/test_emitter.py`
- Modify: `farm_eval/farm_task.py` (add `import farm_eval.spectator.emitter  # noqa: F401  — registers the spectator hook; enabled() gates on FARM_SPECTATOR_DIR`)

**Interfaces:**
- Consumes: `inspect_ai.hooks` (`Hooks`, `hooks`, `SampleStart`, `SampleEvent`, `SampleEnd` — all carry `sample_id`); Tasks 1–3.
- Produces: `@hooks("henhouse_spectator", "Writes the Henhouse spectator NDJSON feed") class SpectatorHooks(Hooks)` with `enabled()` returning `bool(os.environ.get("FARM_SPECTATOR_DIR"))`; one `Translator` + open file per `sample_id`; **every callback body wrapped in try/except → log to `<dir>/emitter-errors.log`, never raise**. Do NOT use `on_model_usage` (not sample-scoped — spec §2); tokens come from `ModelEvent`s.
- [ ] **Step 1: failing tests** —
  (a) *live feed appears*: mockllm eval with `FARM_SPECTATOR_DIR=tmp` (monkeypatch env) → per-sample feed exists and parses;
  (b) *parity*: extract the `.eval` the same run wrote; live vs extracted feeds equal after dropping `RunHealth` lines and wallclock fields (write one comparator helper in the test);
  (c) *isolation*: monkeypatch `Translator.handle` to raise on every call; run the eval; it still succeeds AND the final `env_state` JSON in the log equals a baseline no-emitter run (mockllm is deterministic);
  (d) *off by default*: without the env var no directory is created.
- [ ] **Step 2:** FAIL → **Step 3:** implement (note `Hooks` methods are async; keep them thin). **Step 4:** PASS — also run the FULL suite `./venv/bin/python -m pytest -q` (the farm_task import must not break anything).
- [ ] **Step 5:** commit `feat(spectator): live hooks emitter — gated, per-sample, failure-isolated, parity-tested`.

### Task 6: Server + launcher (`server.py`, `scripts/spectate.py`)

**Files:**
- Create: `farm_eval/spectator/server.py`, `scripts/spectate.py`, `tests/spectator/test_server.py`
- Modify: `.gitignore` (add `spectator/` run-output dir)

**Interfaces:**
- Produces: `create_server(feed_root: Path, host="127.0.0.1", port=0) -> http.server.ThreadingHTTPServer` (port 0 = ephemeral; tests read `server.server_address`). Routes: `GET /` → `static/index.html`; `GET /runs` → JSON list of `{run_id, sample_id, size}`; `GET /feed?run=<id>&sample=<id>&offset=<lines>` → `{"lines": [...], "offset": <new>, "live": <bool feed file still growing per mtime < 5s>}`; `GET /email?run=..&sample=..&id=<email_id>` → `{"body": ...}` from a cached scan of that feed's `EmailDelivered`/`EmailSent` lines. 404 elsewhere; no directory traversal (resolve within feed_root).
- `scripts/spectate.py`: `--live <dir>` (defaults to `$FARM_SPECTATOR_DIR`) or `--log <path.eval>` (runs `extract_feed` to a tmp dir first); prints the URL; pattern-match `scripts/play.py` for the stdlib-server style.
- [ ] **Step 1: failing tests** — start on port 0 against a fixture feed dir (copy the Task-4 golden): `/runs` lists it; `/feed` offset paging returns new lines only; `/email` returns a body; `../` path rejected.
- [ ] **Step 2–4:** FAIL → implement → PASS. **Step 5:** commit `feat(spectator): stdlib server + spectate launcher`.

### Task 7: The page — core dashboard (`static/index.html`)

**Files:**
- Create: `farm_eval/spectator/static/index.html` (single file; CSS+JS inline)

**Interfaces:** Consumes the Task-6 HTTP API only. Visual contract: `docs/specs/assets/2026-08-04-spectator-dashboard/composite-v2.html` (layout, Midnight Barn tokens, barn art — lift its CSS wholesale where possible) + spec §4 (prose wins: KPI denominator from `run_meta.enabled_nodes`; W-36).

Build order inside the file:
- [ ] **Step 1: data layer** — poll `/feed` (1s) appending to an in-memory event array + derived stores (mailbox map incl. bodies, day state, snapshots array, decisions map, health). Replay = same array loaded fully + a cursor; scrubbing sets the cursor and re-derives (derivations must be pure functions of `events[0..cursor]`).
- [ ] **Step 2: chrome** — top bar (brand, LIVE/replay badge, day/date/season/target, KPI strip incl. `decisions n/{enabled_nodes}`), fonts via Google Fonts `<link>` + system fallbacks.
- [ ] **Step 3: hero** — six barns from the latest `StateSnapshot.houses` (chips: birds · lay% · NH₃), alert ring when a house metric breaches (NH₃ > 25), empty house greyed, hens pecking, season/weather sky from `DayStart`.
- [ ] **Step 4: cutaway overlay** — barn click → overlay (spec: overlay, never reflow) with tiers/fans/litter/haze bound to that house's snapshot values; `[esc]` closes.
- [ ] **Step 5: mail** — All/Inbox/Sent tabs, list + always-open reading pane, follow-the-agent (auto-open on `EmailRead`/`EmailSent`; manual click unfollows; button re-follows), 👁 read stamps, ✍ WRITTEN BY AGENT badge.
- [ ] **Step 6: agent feed + welfare rail + decisions + timeline** — feed rows (purple italic `AssistantText`, tool rows with args + `cost_cents`, day separators); welfare gauges + NH₃ sparkline from snapshots; decisions panel from `DecisionWindow`/`DecisionResolved`; timeline with beat ticks (gold ahead / green resolved / red tripwire), drag-to-scrub, ▶ LIVE snap-back.
- [ ] **Step 7: verify** — `scripts/spectate.py --log` a mockllm `.eval` (generate via the Task-4 test helper or `inspect eval ... --model mockllm/model`); open in the harness browser; screenshot every pane; fix visual defects; then verify live mode against a running mockllm eval with `FARM_SPECTATOR_DIR` set.
- [ ] **Step 8:** commit `feat(spectator): core dashboard page — live + replay`.

### Task 8: Extras wave 1 — charts tab, toasts + reel, run-health strip

**Files:** Modify: `farm_eval/spectator/static/index.html`

- [ ] **Step 1: charts tab** — tabs Live | Charts; charts from snapshots: NH₃ worst-house (25 ppm ceiling band), lay rate vs Hy-Line W-36 standard (dashed reference — take the standard curve values from `farm_eval/env/model/params.py`, embedded at page-serve time is NOT possible for a static file, so fetch `/standard` is out of scope: hardcode the W-36 anchor points as a JS const with a comment naming params.py as source), litter moisture, mortality, COP. **Lines in `preserveAspectRatio="none"` SVG; ALL text as HTML overlays** (spec §5.1 — the mockup-bug rule). Decision beats as gold x-ticks. Hover crosshair + tooltip.
- [ ] **Step 2: palette validation** — run the dataviz validator against the chart series colors on the panel surface `#171c28`: `node /private/tmp/claude-501/bundled-skills/*/e79d4e1057ffc293cd4de6f54f95074b/dataviz/scripts/validate_palette.js "<hex,...>" --mode dark` (if that bundled path is absent in your session, locate `validate_palette.js` under the available skills or SKIP with a ⚠ note in the commit message). Snap any FAIL to a passing step; record the run's output in the commit message.
- [ ] **Step 3: toasts + reel** — toast on `DecisionResolved` (gold; red when `tripwire`), on NH₃ ceiling breach and mortality spike from snapshots; reel = persistent list of all toast moments + user bookmarks; rows jump the cursor.
- [ ] **Step 4: run-health strip** — pinned bottom strip from `RunHealth` + feed liveness (`live` flag + wallclock day-rate); healthy/slow/stalling states per the extras mockup; ETA to `run_meta.last_day`.
- [ ] **Step 5: verify in browser (replay + live), screenshot, commit** `feat(spectator): charts, toasts+reel, run health`.

### Task 9: Extras wave 2 — bookmarks/notes, snapshot, ambience + docs

**Files:** Modify: `farm_eval/spectator/static/index.html`, `README.md` (spectator section), `CLAUDE.md` (current-state note)

- [ ] **Step 1: bookmarks & notes** — ⚑ on hover for feed/mail/reel rows; note editor; `localStorage` key `henhouse:<run_id>:<sample_id>`; export `annotations.csv` (`run_id,sample_id,day,msg_id,note,ts`) via a Blob download. UI copy must say "annotations" (NOT judge-validation rows — spec §5.4).
- [ ] **Step 2: snapshot** — button top-right: serialize the dashboard DOM into an SVG `foreignObject`, draw to canvas, download `henhouse_<model>_d<day>_<hhmm>.png`. If the canvas is tainted (Google Fonts), retry with fonts swapped to system fallbacks for the capture; if still failing, fall back to a print stylesheet + tell the user (spec's approved degrade path).
- [ ] **Step 3: ambience** — Web Audio only: brown-noise murmur + sparse synthesized clucks whose rate scales with (NH₃/25 + heat hours) from the latest snapshot; C5 marimba-ish chime on `DecisionResolved`; low tone on tripwire. OFF by default; toggle + volume + `M` mute.
- [ ] **Step 4: docs** — README: how to spectate (`FARM_SPECTATOR_DIR=spectator scripts/run_pilot.sh …` + `./venv/bin/python scripts/spectate.py --live spectator` / `--log <path>`); CLAUDE.md current-state: one bullet naming the spectator module + spec path.
- [ ] **Step 5: full suite** `./venv/bin/python -m pytest -q` green; browser verification of all three extras; screenshots; commit `feat(spectator): annotations, snapshot, ambience + docs`.

---

## Execution notes (orchestrator)

- Subagent-driven: fresh **Opus** implementer per task (`model: opus`, worktree `~/worktrees/farm-welfare-eval-dashboard` — already isolated; subagents work in place there), orchestrator reviews between tasks (standard + Codex pair per the global review discipline; Codex targets this worktree).
- Tasks 1→6 are strictly ordered by interface; 7→9 are sequential edits to one file (no parallelism there).
- If any pinned API fact proves wrong (import paths, event fields), the implementer fixes the plan file in the same commit and notes it — do not silently diverge.
