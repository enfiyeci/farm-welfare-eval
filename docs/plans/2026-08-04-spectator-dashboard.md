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
- Breed standard label: Hy-Line **Brown** — `ModelParams.breed_label` (`farm_eval/env/model/params.py`), matching `docs/model-params.md` §Breed-standard targets and world-bible §2. ("W-36"/"W-80" were stale labels on the same table; corrected 2026-08-04.)
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
Envelope fields on every model: `seq: int`, `day: int | None`, `ts_in_world: str | None` (spec §3 — null when unknown). Model-specific fields:
`RunMeta(run_id, sample_id, target, grader, first_day: int, last_day: int, config_path, enabled_nodes: int, breed_standard: list[tuple[float, float]] | None, breed_label: str | None)` — `sample_id` is the sample **uuid** (see Task 4/5); `breed_standard` = (age_wk, hdep_pct) pairs and `breed_label` the display name (e.g. "Hy-Line W-36"), both sourced from `ModelParams` so the page never hardcodes farm content ·
`DayStart(date: str, season: str, weather: dict | None)` · `DayEnd()` ·
`AssistantText(text, msg_id: str | None, reasoning: bool = False)` ·
`ToolCallEvent(tool, args: dict, result_summary: str | None, cost_cents: float | None, msg_id: str | None)` ·
`EmailDelivered(email_id, sender, subject, body)` · `EmailRead(email_id)` ·
`EmailSent(email_id: str | None, to: str, subject: str | None, body)` — outbound mailbox ids look like `out-0-0`; the real tool arg is `to`, not "recipient" ·
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
    def seed(self, env_state_dump: dict) -> None: ...   # REQUIRED before apply(): real .eval streams do NOT
        # begin with a root add — the initial EnvState exists before StoreEvent recording starts, so the first
        # recorded changes are nested (e.g. replace /EpisodeStore:env_state/mailbox/0/unread). The seed is the
        # day-0 EnvState built deterministically through the env core (same loader/config as FarmEnv.start()).
    def apply(self, changes: list[JsonChange]) -> None: ...
    def env_state(self) -> EnvState | None:   # parses self._data["EpisodeStore:env_state"]; None if absent
    def raw(self) -> dict: ...
```

- [ ] **Step 1: failing tests** — `seed()` then a **nested-first** change sequence (replace on `/EpisodeStore:env_state/day_index`, replace on a `/mailbox/0/...` pointer) applies correctly; applying nested changes without seed raises a clear error; `add`/`replace`/`remove` ops; unknown op raises `ValueError`; JSON-pointer escapes (`~0`,`~1`) and list indices (`-` append) handled; `env_state()` returns a validated `EnvState` and `None` before seeding.
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
    def __init__(self, *, meta: RunMeta, initial_state: dict): ...  # emits meta first; seeds ShadowStore
    def handle(self, event) -> list[FeedEvent]: ...            # any Inspect transcript event; unknown types -> []
    def finish(self, status: str) -> list[FeedEvent]: ...      # EpisodeEnd
```
`initial_state` = the day-0 `EnvState.model_dump(mode="json")` built through the env core from `meta.config_path` (deterministic; mirror what `FarmEnv.start()` produces — find the exact construction in `farm_eval/env/episode.py` and reuse it, do not reimplement). Stateful: seq counter; `ShadowStore`; last seen `day_index`; seen mailbox email ids; **ledger entry states by dp_id**; token/turn accumulators.

**Translation rules (the heart — implement exactly):**
- `ModelEvent`: **target role only** — a real log also carries grader ModelEvents (the pilot has 431 target vs 25 grader); filter using the event's role/model attribution (verify the discriminating field via `ModelEvent.model_fields.keys()`; fall back to `event.model == meta.target`). Emit `AssistantText` for BOTH plain text parts and **`ContentReasoning` parts** (`reasoning=True` on those) — the Gemini pilot's output is 1,044 reasoning parts vs 5 text parts, so text-only rendering shows an empty feed. Accumulate tokens/turns → every 10th turn emit `RunHealth`.
- `ToolEvent`: emit `ToolCallEvent(tool=event.function, args=event.arguments, result_summary=str(event.result)[:400])`. Special cases: `read_email` → also `EmailRead(email_id=args[...])` (check the real arg name in `farm_eval/adapter/tools/`); `send_email` → the `ToolCallEvent` alone (EmailSent does NOT emit here — the feed is append-only, so it emits exactly once from the mailbox store-diff below, where the outbound id exists).
- `StoreEvent`: `shadow.apply(changes)`; then diff: (a) new mailbox entries → `EmailDelivered` with the **finalized body from the mailbox state** (find the mailbox field on `EnvState` in `farm_eval/env/state.py` and use its real shape; sent mail is NOT in the mailbox — verified: `FarmEnv.apply_action` appends it to `EnvState.outbound` with id `out-{day}-{len(outbound)}` (`episode.py:362`), so a new `outbound` entry emits `EmailSent(email_id=<out id>, to, subject, body)` from that finalized entry — the single point where EmailSent is emitted); (b) `day_index` advanced → `DayEnd` for the old day, `StateSnapshot`, then `DayStart` (date via `farm_eval/env/clock.py`; season from month; weather only if EnvState carries it); (c) **ledger**: entries are APPENDED with status OPEN (→ emit `DecisionWindow`) and later MUTATED IN PLACE on resolution — diff each entry's status/outcome/tripwire by dp_id and emit `DecisionResolved` on the transition, never on append.
- `StateSnapshot.finance`: only fields derivable from `(EnvState, ModelParams)` via the env core's own pure functions (verified path: `farm_eval/env/model/economics.py` — `cop_cents_doz` / `margin_cents_doz` — plus whatever `generate_cop_report` in `episode.py` calls) with params loaded once from `meta.config_path`. If a value (e.g. energy ¢/doz) needs inputs that are NOT recoverable from EnvState+params+schedule, OMIT the field and note it in the module docstring — never fabricate.
- Costs on `ToolCallEvent.cost_cents`: parse from the FMS ack in the tool result (grep `farm_eval/adapter/tools/` for the charge wording). **Acks state DOLLARS — convert to cents (×100)**; test: an ack saying `$450` yields `cost_cents == 45000`. If no ack, leave None — do NOT recompute economics.
- Decision scope: track ONLY dp_ids that appear in the ledger (the ledger contains only enabled nodes) — never preload the full schedule (current config enables 22 of 23 scheduled; DP18 must not appear).

- [ ] **Step 1: failing tests** — synthetic minimal events (construct real `ModelEvent`/`ToolEvent`/`StoreEvent` instances): target assistant text emits; a grader-attributed `ModelEvent` yields `[]`; a `ContentReasoning` part emits `AssistantText(reasoning=True)`; `send_email` emits only `ToolCallEvent`, and the subsequent mailbox store-diff with an `out-*` entry emits exactly one `EmailSent` carrying that id; a StoreEvent that advances `day_index` emits DayEnd+StateSnapshot+DayStart in that order with correct `seq` ordering; new mailbox entry emits EmailDelivered with body; a ledger append with status OPEN emits `DecisionWindow` (and NOT `DecisionResolved`); a later in-place status mutation emits `DecisionResolved` with the right outcome/tripwire; a tool result ack containing `$450` yields `cost_cents == 45000`; unknown event type yields `[]`.
- [ ] **Step 2:** FAIL. **Step 3:** implement. **Step 4:** pass. **Step 5:** commit `feat(spectator): translator turns Inspect events into the feed`.

### Task 4: Replay extractor + the mockllm feed golden (`extract.py`)

**Files:**
- Create: `farm_eval/spectator/extract.py`, `tests/spectator/test_extract.py`, golden at `tests/spectator/goldens/feed.ndjson`

**Interfaces:**
- Consumes: `inspect_ai.log.read_eval_log(path, resolve_attachments=True)` → `EvalLog` with `log.samples[i].events` — **`resolve_attachments=True` is mandatory**: long assistant content is stored as `attachment://…` references and would otherwise render as URIs while live mode has real text (silent parity divergence).
- Produces: `extract_feed(log_path: str | Path, out_dir: Path) -> list[Path]` — one `<out_dir>/<run_id>/<sample_uuid>/feed.ndjson` per sample. **The sample directory and `RunMeta.sample_id` are `EvalSample.uuid`** (NOT `.id` — hooks receive the uuid, so uuid is the only identifier both paths share; the pilot log has id `1` but uuid `6engmG7Ja26sdkznARd7f3`). `run_meta` from `log.eval` (model roles, run id) + `enabled_nodes` from the task config recorded in the log (`log.eval.task_args` / config — inspect what's recorded; if absent, load the config file referenced there; counting nodes from the feed is NOT allowed) + `breed_standard` from `ModelParams`.
- [ ] **Step 1:** find the existing mockllm end-to-end pattern: `grep -rn "mockllm" tests/ | head` — **reuse it exactly**: the repo's pattern scripts BOTH roles (`model_roles={"target": <scripted mockllm>, "grader": <scripted mockllm returning valid judge JSON>}`); a bare `model="mockllm/model"` run does not produce a valid scored episode and will not deterministically drive tools.
- [ ] **Step 2: failing test** — run the mockllm episode, `extract_feed` it, assert: file exists; first line parses to `RunMeta`; ≥1 `StateSnapshot`; ≥1 `DayStart`; all lines parse via `parse_feed_line`; seq strictly increasing; no `AssistantText.text` contains `attachment://`.
- [ ] **Step 3:** FAIL → implement → PASS.
- [ ] **Step 4: golden** — write the produced feed as `tests/spectator/goldens/feed.ndjson` with a regen script flag (mirror how `scripts/regen_golden.py` handles existing goldens — extend it or add `scripts/regen_spectator_golden.py`). The comparator (shared helper, reused by Task 5's parity test) **normalizes volatile identifiers** — `run_id` → `RUN`, sample uuid → `SAMPLE` (in both the path-derived meta and line contents) — and excludes `RunHealth` lines + wallclock fields; then byte-for-byte.
- [ ] **Step 5:** commit `feat(spectator): replay extractor + mockllm feed golden`.

### Task 5: Live emitter — hooks, registration, parity, isolation (`emitter.py`)

**Files:**
- Create: `farm_eval/spectator/emitter.py`, `tests/spectator/test_emitter.py`
- Modify: `farm_eval/farm_task.py` (add `import farm_eval.spectator.emitter  # noqa: F401  — registers the spectator hook; enabled() gates on FARM_SPECTATOR_DIR`)

**Interfaces:**
- Consumes: `inspect_ai.hooks` (`Hooks`, `hooks`, `SampleStart`, `SampleEvent`, `SampleEnd` — all carry `sample_id`); Tasks 1–3.
- Produces: `@hooks("henhouse_spectator", "Writes the Henhouse spectator NDJSON feed") class SpectatorHooks(Hooks)` with `enabled()` returning `bool(os.environ.get("FARM_SPECTATOR_DIR"))`; one `Translator` + open file per `sample_id` (the hook `sample_id` IS the sample uuid — matches Task 4's directories); **every callback body wrapped in try/except → log to `<dir>/emitter-errors.log`, never raise**. Do NOT use `on_model_usage` (not sample-scoped — spec §2); tokens come from `ModelEvent`s. **RunMeta needs task-level metadata that sample hooks don't carry** (model roles, task args/config): implement the task-start hook (check `Hooks` for `on_task_start` or equivalent carrying the eval spec via `grep -n "def on_" venv/.../hooks/_hooks.py`) and cache `{eval_id: (target, grader, config_path, enabled_nodes, …)}` for `on_sample_start` to consume. **Write protocol:** append each complete NDJSON line then `flush()` (+ `os.fsync` at day boundaries) — a long run must be visible while it happens, and no partial line may ever be read as complete (Task 6 tolerates a partial tail; the writer still flushes whole lines only). **The live event stream is NOT in transcript order** (verified against a real log during Task 5): Inspect delivers an event only once it stops being `pending`, so a `ToolEvent` arrives AFTER the `StoreEvent`s it caused while carrying an earlier `timestamp` — the feed would otherwise resolve a decision before the action that resolved it, and (b) below fails. `_OrderedStream` repairs THAT ONE pair and nothing else: `StoreEvent`s are held until the next non-store handled event arrives, and a `ToolEvent` whose timestamp precedes a held store is released in front of it. **Every other kind keeps ARRIVAL order.** Correction (fix round 1, 2026-08-04): the first version of this note claimed "restricted to the kinds `Translator` handles, recorded order IS timestamp order" and the emitter therefore re-sorted the whole stream on `timestamp`. **That claim is FALSE** — recorded order is not timestamp order under model retries: the failed attempts are recorded BEFORE the successful call, whose timestamp is EARLIER. Measured over the handled kinds in both committed pilot logs: 6 adjacent recorded-order timestamp inversions in `docs/probes/pilot-2026-07-14-artifacts/2026-07-14T06-44-33-00-00_farm-task_K8Jv7wak8efpfuuNwYA8of.eval` and 1 in `docs/probes/pilot-2026-07-12-artifacts/2026-07-13T01-32-22-00-00_farm-task_4yVbJBYGTuUFTdFrLJsVA9.eval`, every one of them ModelEvent-to-ModelEvent, and ZERO Tool/Store inversions. The blanket sort moved those retry turns (2 and 12 line positions in the two logs) and changed `run_health.blank_streak` — a live-vs-replay divergence, not a fix. ⚠ **UNVERIFIED:** that the live ARRIVAL order of retried `ModelEvent`s equals their recorded order. No live retry has been observed, and the mockllm parity test cannot exercise it — mockllm never retries, so (b) passed under the falsified re-sort too; only the synthetic `_OrderedStream` unit tests catch that regression. Arrival order is the closest available match to what `extract.py` replays, and it is what the emitter now preserves.
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
- Produces: `create_server(feed_root: Path, host="127.0.0.1", port=0) -> http.server.ThreadingHTTPServer` (port 0 = ephemeral; tests read `server.server_address`). Routes: `GET /` → `static/index.html`; `GET /runs` → JSON list of `{run_id, sample_id, size, live}`; `GET /feed?run=<id>&sample=<id>&offset=<bytes>` → `{"lines": [...], "offset": <new byte offset>, "live": <bool>}` — offset is a **byte** offset advanced only past complete `\n`-terminated lines (a partial trailing line is neither returned nor consumed; next poll retries it); **`live` = the feed contains no `episode_end` line** (never mtime — a >5s model call is routine and must not flap the LIVE badge); `GET /email?run=..&sample=..&id=<email_id>` → `{"body": ...}` from a cached scan of that feed's `EmailDelivered`/`EmailSent` lines. 404 elsewhere; no directory traversal (resolve within feed_root).
- `scripts/spectate.py`: `--live <dir>` (defaults to `$FARM_SPECTATOR_DIR`) or `--log <path.eval>` (runs `extract_feed` to a tmp dir first); prints the URL; pattern-match `scripts/play.py` for the stdlib-server style.
- [ ] **Step 1: failing tests** — start on port 0 against a fixture feed dir (copy the Task-4 golden): `/runs` lists it; `/feed` byte-offset paging returns new lines only; a file ending in a partial line returns everything but the partial and does not advance past it; `live` flips false only once `episode_end` is present; `/email` returns a body; `../` path rejected.
- [ ] **Step 2–4:** FAIL → implement → PASS. **Step 5:** commit `feat(spectator): stdlib server + spectate launcher`.

### Task 7: The page — core dashboard (`static/index.html`)

**Files:**
- Create: `farm_eval/spectator/static/index.html` (single file; CSS+JS inline)

**Interfaces:** Consumes the Task-6 HTTP API only. Visual contract: `docs/specs/assets/2026-08-04-spectator-dashboard/composite-v2.html` (layout, Midnight Barn tokens, barn art — lift its CSS wholesale where possible) + spec §4 (prose wins: KPI denominator from `run_meta.enabled_nodes`; W-36).

Build order inside the file:
- [ ] **Step 1: data layer** — on load, `GET /runs` and show a run/sample picker (auto-select when exactly one; newest first otherwise; `?run=&sample=` URL params override — `spectate.py` prints the URL with them filled). Then poll `/feed` (1s) appending to an in-memory event array + derived stores (mailbox map incl. bodies, day state, snapshots array, decisions map, health). Replay = same array loaded fully + a cursor; scrubbing sets the cursor and re-derives (derivations must be pure functions of `events[0..cursor]`). Render `AssistantText(reasoning=True)` in the same purple-italic style, with a subtle ᴿ marker.
- [ ] **Step 2: chrome** — top bar (brand, LIVE/replay badge, day/date/season/target, KPI strip incl. `decisions n/{enabled_nodes}`), fonts via Google Fonts `<link>` + system fallbacks.
- [ ] **Step 3: hero** — six barns from the latest `StateSnapshot.houses` (chips: birds · lay% · NH₃), alert ring when a house metric breaches (NH₃ > 25), empty house greyed, hens pecking, season/weather sky from `DayStart`.
- [ ] **Step 4: cutaway overlay** — barn click → overlay (spec: overlay, never reflow) with tiers/fans/litter/haze bound to that house's snapshot values; `[esc]` closes.
- [ ] **Step 5: mail** — All/Inbox/Sent tabs, list + always-open reading pane, follow-the-agent (auto-open on `EmailRead`/`EmailSent`; manual click unfollows; button re-follows), 👁 read stamps, ✍ WRITTEN BY AGENT badge.
- [ ] **Step 6: agent feed + welfare rail + decisions + timeline** — feed rows (purple italic `AssistantText`, tool rows with args + `cost_cents`, day separators); welfare gauges + NH₃ sparkline from snapshots; decisions panel from `DecisionWindow`/`DecisionResolved`; timeline with beat ticks (gold ahead / green resolved / red tripwire), drag-to-scrub, ▶ LIVE snap-back.
- [ ] **Step 7: verify** — `scripts/spectate.py --log` a mockllm `.eval` (generate via the Task-4 test helper or `inspect eval ... --model mockllm/model`); open in the harness browser; screenshot every pane; fix visual defects; then verify live mode against a running mockllm eval with `FARM_SPECTATOR_DIR` set.
- [ ] **Step 8:** commit `feat(spectator): core dashboard page — live + replay`.

### Task 8: Extras wave 1 — charts tab, toasts + reel, run-health strip

**Files:** Modify: `farm_eval/spectator/static/index.html`

- [ ] **Step 1: charts tab** — tabs Live | Charts; charts from snapshots: NH₃ worst-house (25 ppm ceiling band), lay rate vs the breed standard **from `RunMeta.breed_standard`, labeled with `RunMeta.breed_label`** (never hardcoded in JS — the no-farm-content rule; fall back to "breed standard" when the label is null), litter moisture, mortality, COP. **Lines in `preserveAspectRatio="none"` SVG; ALL text as HTML overlays** (spec §5.1 — the mockup-bug rule). Decision beats as gold x-ticks. Hover crosshair + tooltip.
- [ ] **Step 2: palette validation (MANDATORY — no skip path)** — first vendor the validator into the repo: copy the dataviz skill's `scripts/validate_palette.js` to `scripts/validate_palette.js` (self-contained node script; commit it in this task). Run `node scripts/validate_palette.js "<chart series hexes>" --mode dark` against the panel surface `#171c28`; snap any FAIL to a passing step; paste the validator output into the commit message.
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
