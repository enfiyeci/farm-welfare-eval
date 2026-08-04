# Henhouse — the spectator dashboard (live + replay) — design spec

**Date:** 2026-08-04 · **Status:** approved via visual brainstorm (mockups in `.superpowers/brainstorm/78363-1785875124/content/`, main tree)
**Owner decisions baked in:** composite layout · Midnight Barn theme · storybook barns + cutaway on click (overlay) · built-in mail reading pane with follow-the-agent · six extras (charts, toasts+reel, run health, bookmarks/notes, snapshot, ambience) · ghost-run overlay and spoiler shield explicitly REJECTED for now.

## 1. Purpose

Watch a running eval episode the way you'd watch a game: what mail the agent opens, what it writes, every tool call with its arguments and cost, the farm's welfare state evolving — live while `run_pilot.sh` is executing, and as a scrubbable replay of any finished `.eval` log. It is a **spectator** surface: strictly read-only over the run, invisible to the agent, and it never feeds anything back into the eval or the judge.

Non-goals: no live judging or provisional welfare headlines (the judge runs post-hoc); no run control (pause/kill stays in the terminal); not a public artifact.

## 2. Architecture — one renderer, two feed sources

```
LIVE:    inspect eval ── Inspect hooks emitter ──▶ spectator feed (NDJSON) ──▶ stdlib HTTP server ──▶ browser page (poll)
REPLAY:  finished .eval log ── extractor ────────▶ same NDJSON feed ─────────▶ same server ─────────▶ same page (scrubber)
```

- **Feed emitter (live):** an `inspect_ai.hooks.Hooks` subclass (installed v0.3.244 has `on_sample_event`, `on_sample_start/end`, `on_model_usage`) that observes transcript events and appends NDJSON to `spectator/<run_id>/feed.ndjson`. Enabled only when `FARM_SPECTATOR_DIR` is set (or a `config.yml` flag); **failure-isolated** — any exception inside the emitter is swallowed and logged, never propagated into the run; zero effect on determinism, agent-visible state, or the ledger.
- **Env-state snapshots:** the hook layer sees transcript/store events; per-day farm state (per-house metrics, welfare channels, finance) is emitted from the store's `EnvState` after each `end_day` commit (StoreModel changes surface as store events; the emitter reads the post-commit snapshot — exact tap point decided in the plan, with the hard rule: read-only, post-commit, never holding references across `end_day`).
- **Decision/ledger events:** derived from the silent ledger the same read-only way (window opened at `opens`, entry recorded, mechanical tripwires). Spectator-only; nothing about the ledger changes.
- **Extractor (replay):** `farm_eval/spectator/extract.py` reads a finished `.eval` via the Inspect log API and writes the **identical** feed format. Parity is tested (see §7).
- **Server:** stdlib `http.server` in the pattern of `scripts/play.py` (no new runtime deps): serves the single-file page, `GET /feed?offset=N` returns new NDJSON lines (the page polls ~1s in live mode; in replay the full feed loads once and the scrubber drives a cursor through it).
- **Launcher:** `scripts/spectate.py --live <spectator-dir> | --log <path.eval>` (also spawnable from `run_pilot.sh` via env var).

## 3. Feed event schema (NDJSON, one JSON object per line)

Common envelope: `{seq, day, ts_in_world, kind, ...}` — `seq` monotonically increasing; `ts_in_world` the in-world clock when known, else null.

| kind | payload |
|---|---|
| `run_meta` | run id, target model, grader, episode day span, config path |
| `day_start` / `day_end` | day index, calendar date, season, weather |
| `assistant_text` | visible reasoning/message text, msg id |
| `tool_call` | tool name, args (full), result summary, service cost if any, msg id |
| `email_delivered` | email id, sender, subject (body via `GET /email/<id>` from corpus) |
| `email_read` / `email_sent` | email id / full outgoing body + recipient |
| `state_snapshot` | per-house: birds, lay%, nh3, temp, litter moisture, vent; totals: eggs, mortality 7d, heat-stress hrs, footpad, keel, feathers; finance: cop¢/doz, energy¢, margin, service charges |
| `decision_window` | dp id, opened/closes day (spectator display only) |
| `decision_resolved` | dp id, outcome class, tripwire bool, latency days |
| `run_health` | turns, blank-turn streak, retries, tokens in/out, wall-clock day-rate |
| `episode_end` | final day, status |

The feed is derived data, gitignored, and never read back by the eval.

## 4. The page (single-file, no build step)

`farm_eval/spectator/static/index.html` — vanilla HTML/CSS/JS, self-contained; Google Fonts (Fraunces / Newsreader / IBM Plex Mono) with graceful system-serif/mono fallback offline.

**Layout (approved composite):** top bar (brand, LIVE/replay badge, day + date + season + target model, KPI strip: lay rate, eggs, NH₃ max, mortality 7d, COP¢, week margin, decisions n/21) → animated hero (storybook winter/season barns H1–H6, per-house chips: birds · lay% · NH₃; alert ring on trouble; empty-house greyed; hens pecking, weather + season + day/night from `day_start`) → **cutaway overlay** on barn click (aviary tiers, hopping hen dots, fans spinning at vent rate, litter wet-zone, NH₃ haze, sensor readout; overlay, not inline — the page must not reflow) → main grid: **Mail** (All/Inbox/Sent tabs, list + always-open reading pane, follow-the-agent auto-open on read AND send, 👁 read-timestamps, ✍ WRITTEN BY AGENT badge on outgoing) · **Agent feed** (assistant text as purple italics, tool calls with args, costs riding on action rows, day markers) · **Welfare + Finance rail** (gauges + NH₃ sparkline) → bottom: **Decisions panel** (spectator-only labels: ✓ score-pending, OPEN→deadline, UNNOTICED, TRIPWIRE) · **Timeline** (17-month bar, season labels, beat ticks green/gold/red, drag-to-scrub; live mode shows cursor at now; jumping into the past switches to replay-of-the-buffer, "▶ LIVE" snaps back).

**Theme — Midnight Barn tokens:** bg `#0f131c`, panel `#171c28`/`#131826`, line `#2a3145`, text `#c8cedb`, dim `#7d8899`, cream `#ece4d4`, gold `#d9a441`, barn `#b5382f`, blue `#7fb4e8`, green `#57bd7e`, red `#e56a5e`, purple `#b49ae8`; bordered-panel chrome per composite-v2 mockup; grain overlay optional.

## 5. The six extras (all approved)

1. **Charts tab** — tabs: Live | Charts | Mail | Decisions. Time-series from `state_snapshot`s: NH₃ worst-house (25 ppm ceiling band), lay rate vs Hy-Line W-80 standard, litter moisture, mortality, COP. One measure per chart, never dual-axis; decision beats as gold x-ticks; hover crosshair + tooltip. **Implementation rule from the mockup bug:** plot lines live in a `preserveAspectRatio="none"` SVG; all text labels are HTML overlays so they never stretch. Chart palette validated with the dataviz skill's `validate_palette.js` against the dark surface before merge.
2. **Moment toasts + reel** — toasts on `decision_resolved` (gold), tripwire (red), state alarms (mortality spike, NH₃ over ceiling); every toast appends to the reel (the run's table of contents); reel rows + toasts jump the dashboard to that day.
3. **Run health strip** — pinned bottom strip from `run_health` events: state (healthy/slow/stalling), day-rate + bar history, turns, blank-turn streak, retries, tokens, ETA to final day. Alarm styling when sick.
4. **Bookmarks & notes** — ⚑ on hover over any feed/mail/reel row; optional note; stored in `localStorage` keyed by run id; export buttons: `labels.csv` and judge-validate rows (run id, day, msg id, note, ts) shaped for the `judge/validate.py` hand-labeling workflow.
5. **Snapshot export** — capture the dashboard DOM to PNG named `henhouse_<model>_d<day>_<hhmm>.png`. No external libs: SVG `foreignObject` serialization to canvas; if fonts/canvas taint make this unreliable, degrade to a "print this frame" stylesheet and note it — do not add a CDN dependency.
6. **Ambience** — Web Audio synthesized (no audio files): low henhouse murmur whose density tracks welfare state, warm chime on decision resolved, low tone on tripwire. Off by default, volume + mute key.

## 6. Modules

```
farm_eval/spectator/
  __init__.py
  events.py      # pydantic v2 event models (the schema above), extra="forbid"
  emitter.py     # Inspect hooks subclass; env-gated, failure-isolated
  extract.py     # .eval log -> feed.ndjson (same models)
  server.py      # stdlib HTTP: static page, /feed?offset, /email/<id>
  static/index.html
scripts/spectate.py
```

Conventions honored: pydantic v2, `extra="forbid"`, no farm content hardcoded in logic (emails resolved from `corpus/` by id; UI labels generic), determinism untouched, venv at `./venv`.

## 7. Testing

- **Emitter goldens:** mockllm episode over the test fixtures → deterministic `feed.ndjson` golden (like existing goldens, regenerated from config horizon).
- **Live/replay parity:** run mockllm with emitter on; extract the same `.eval`; the two feeds must be identical modulo `run_health`/wall-clock fields (excluded by the comparator).
- **Isolation:** test that an emitter that raises on every event does not change episode results (state hash + ledger equality vs emitter-off run).
- **Schema:** event models round-trip; unknown kinds rejected.
- **UI:** manual + screenshot verification (no JS test harness for iteration 1); chart palette validator run recorded in the PR.

## 8. Risks / open points

- Exact hook tap for post-`end_day` state snapshots is decided in the plan (options: store-event diff reconstruction vs a tiny read-only accessor on `EpisodeStore`); the guardrails in §2 bind either way.
- `on_sample_event` payload shape must be verified against v0.3.244 during Task 1 (API confirmed present; field names not yet pinned).
- Snapshot PNG is the only genuinely uncertain extra (canvas tainting); it has an approved degrade path.
- Sent-email bodies exist only in tool-call args — the emitter must capture them at `send_email` time (they are not in `corpus/`).

## 9. Process note

Implementation is subagent-driven (owner directive 2026-08-04): plan tasks executed by **Opus** subagents in this worktree, orchestrator reviews each task (standard + Codex straight + Codex adversarial per the global review discipline), TDD per `superpowers:test-driven-development`.
