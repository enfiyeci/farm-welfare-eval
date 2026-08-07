# Reorg catalogue R3 — `docs/probes/` (75 files)

Reader R3, 2026-08-06. Nothing moved, edited or deleted; `git status --porcelain docs/probes` empty.

## Coverage (counts reconcile)

**75 assigned · 45 read in full · 30 catalogued as artifacts · 0 unopenable.**

Artifacts: 2 `.eval` binaries, 1 PDF, 1 large HTML, 19 JSON (top-level keys + every quoted headline
read out of the file, not from prose), 2 large proxy-label YAMLs, and ⚠️ **4 bulk dumps read only at
header/tail** — `all-emails.md` (4,888 lines), `round3-emails-by-day.md` (4,075),
`round3-transcript-by-day.md` (3,068), `pilot-2026-07-14-artifacts/ws4-ws6.txt` (733). Their
identification rests on their own self-describing headers.

⚠️ Also excerpt-only (cited lines established the coupling; not read end to end):
`docs/build-fieldguide.py` (grep only — 16 string literals counted),
`docs/pilot-debrief-protocol.md` (targeted grep), `farm_eval/spectator/emitter.py`,
`scripts/spectate.py`, `scripts/gen_pilot_report.py`, `tests/report/test_extract.py`,
`tests/probe/test_schedule_audit.py`, `scripts/audit_schedule.py`, `scripts/financial_*.py`,
`scripts/rescore_live_round4.py`, several `tests/judge/*`.
⚠️ `~/.claude/skills/pdf-design/report_theme.py` **not opened** (outside repo) — the
"vendored duplicate" verdict rests on the local file's docstring, not a byte comparison.

---

## 🔴 §C — THE BREAKAGE LIST. Work through this in order.

### Tier 1 — hard test failure or silent wrong-path write

| # | File:line | Path | Effect if unedited |
|---|---|---|---|
| 1 | `tests/probe/test_schedule_audit.py:136` | reads `docs/probes/schedule-spacing-report.md` | **pytest FAILS immediately** — the only assigned file whose move causes a hard, visible failure |
| 2 | `scripts/audit_schedule.py:21` | `--out` default → same path (write) | regenerates at the old path; then test 1 compares a stale file |
| 3 | `scripts/gen_pilot_report.py:17` | `docs/probes/pilot-history.json` (read+write) | every report run resurrects the old path |
| 4 | `scripts/financial_decision_sweep.py:307` | `docs/probes/financial-decision-sweep.json` (write) | ditto |
| 5 | `scripts/financial_lever_map.py:121` | `docs/probes/financial-lever-map-data.json` (write) | ditto |
| 6 | `scripts/rescore_live_round4.py:95` | `docs/probes/round4-judge-wave-rescore-2026-07-15.json` (write, relative after `os.chdir`) | ditto |

### 🔴 Tier 2 — `replay_f1.py`, the script that reproduces the canonical **6.804** anchor

| # | Line | Path |
|---|---|---|
| 7 | `:8` | **`ROOT = Path(__file__).resolve().parents[3]`** — derives the repo root from being **exactly 3 levels deep**. Any destination at a different depth breaks it **silently**. The comment says the depth is deliberate. |
| 8 | `:19` | `docs/probes/pilot-2026-07-12-artifacts/2026-07-13T…eval` (read) |
| 9 | `:57` | `…/welfare_reference-2026-07-12-511d.json` (read) |
| 10 | `:63` | `…/dimensions-2026-07-12` (read, **a directory**) |
| 11 | `:82,84` | `…/rescore-round4-replay.json` (write) |

### Tier 3 — ALREADY broken before any reorg

| # | File:line | Path |
|---|---|---|
| 12 | `pilot-2026-07-12-artifacts/rescore_live_f23.py:16` | `ROOT = Path("/Users/ardaenfiyeci/Desktop/farm-eval")` — **does not exist on this machine** |
| 13 | `scripts/rescore_live_round4.py:34` | `LOG = "/Users/ardaenfiyeci/…"` — same |

### Tier 4 — other write targets / readers
`build_report_v2.py:256` writes the round-1 PDF; `:9` adds out-of-repo `~/.claude/skills/pdf-design`
to `sys.path`. `tests/report/test_extract.py:21` points at the round-3 `.eval` which is **gitignored
and absent**, so it **skips** — a wrong path there would fail *silently forever*.

### Tier 5 — comments/docstrings (no runtime effect, documentation integrity)
`config.yml:26` + all four `config-baseline-*.yml:30` + `schedule/events.yml:643` → all name
`f8-dp18-discoverability-2026-07-12.md`. `farm_eval/env/model/integrate.py:190` and
`tests/env/model/test_climate_gauge_reports_daily_peak.py:3` → `node-layer-audit-2026-07-29.md`.
`farm_eval/spectator/emitter.py:113`, `scripts/spectate.py:15`, `tests/spectator/test_server.py:490`
→ the two `.eval` bundles. Plus `docs/build-fieldguide.py` × **16** literals.

**The move-safe pattern to copy:** `inheritance-probe-*/probe_round{1,2}_*.py` use
`Path(__file__).parent` and are self-locating.

---

## 🔴 The `pilot-2026-07-12-artifacts/` bundle must move as ONE unit or not at all

It is self-contained and path-coupled: the log, the pinned 8-dimension rubric snapshot, the pinned
511-day `welfare_reference`, the replay script and its outputs. `replay_f1.py` reproduces
**6.803790995188118** — verified in `rescore-f1-replay.json` (15,518 bytes). **That file IS the 6.804
anchor** and the round-4 plan says it must never be rewritten.

**The pinned rubric snapshot is only half redundant.** Files `01–06` are **byte-identical** to the live
`judge/dimensions/`; **`07_realism.md` and `08_eval_awareness.md` DIFFER** — they carry the round-2
F2/F3 wording the recorded grader outputs were produced under. **Do not prune the six duplicates:**
`load_dimensions()` reads the *directory*.

`rescore-f1-replay.json` vs `rescore-round4-replay.json`: 40 diff lines, **identical headline**. The
pair IS the evidence that the round-4 validator moved the round-1 pin by 0.000. Keep both.

---

## 🔴 `docs/probes/README.md` does NOT describe `docs/probes/`

It is the **eval-awareness Phase-1 instrument index** — of the seven instruments it tables, exactly
**one** (`schedule-spacing-report.md`) lives in this directory; the rest are in `farm_eval/probe/`,
`scripts/`, `corpus/`, `docs/`. **Do not promote it to `runs/README.md`.**

The convention it *does* carry is a gating rule worth preserving: **"probe findings before a κ PASS are
not actionable"**, cited for exactly that by `human-review-2026-07-08.md:4`,
`docs/expert-labeling-pack.md:103`, `docs/pilot-debrief-protocol.md:735`.

**The convention this directory actually runs on is written elsewhere** — `docs/pilot-debrief-protocol.md`
defines the filename pattern and the per-run artifact set (`dp-table.md`, `harvest.txt`, `ws4-ws6.txt`,
`reply-recon.md`, `ledger.json`, `diagnostics.json`, `score.json`), remarkably consistent across all
three bundles. **Write a new `runs/README.md` from that.**

## Pilot rounds — superseded for performance, NOT for role

Headlines: 2026-07-13 **6.167** → -14 **7.139** → -15 **8.299** (`pilot-history.json`, verified).

- **-12 (round 1)** superseded on performance but **the most load-bearing bundle here** — the 6.804
  anchor is replayed from its log. Its `.eval` is separately documented as **UNREPLAYABLE by the
  spectator extractor** (`scripts/spectate.py:15`, `tests/spectator/test_server.py:490`).
- **-14 (round 2)** superseded on the world axis (F-R2-1/2/3/10 fixed in round 3), but its log is the
  **measurement basis** for `farm_eval/spectator/emitter.py`'s ordering contract (6 recorded-order
  inversions measured on it), and its regrade is one of two banked Spearman transcripts.
- **-15 (round 3)** current. ⚠️ **Its `.eval` is absent** (gitignored, local-only).

Both committed `.eval` files were **force-added past `.gitignore:7 (*.eval)`** — a `runs/` scheme should
make that exception explicit rather than accidental.

## Misfits against the scheme

| File(s) | Why |
|---|---|
| `inheritance-probe-2026-07-31/` (5) | **Not a run of this eval** — layer hens *and Pekin ducks*, `gpt-5.6-sol` via `codex exec`, a candidate v3 design. Self-critical: 18/18 refused, and it states plainly it **did not instantiate the hypothesis it was built for**. → **`studies/`** |
| `report_theme.py` | Eval-agnostic ReportLab theme **vendored from a global skill**. → `engine/` or leave frozen. The clearest duplicate in the assignment. |
| `financial-decision-map-2026-08-03.md` + its 2 JSONs | Analysis of the **substrate's economics**, not evidence from a run. Filing under `runs/` would be a category error. → `evals/hen/design/` |
| `eval-awareness-briefing-experiment-2026-07-15.md` | A designed but **unrun** controlled experiment. → `studies/` |
| `schedule-spacing-report.md` | Generated schedule audit → `evals/hen/nodes/` |
| `human-review-2026-07-08.md` | Doubly-roled: corpus authoring input **and** the canonical disposition-table template three docs cite |
| the two `codex-*review*.md` | Reviews of code, not of a run → a `reviews/` tier |

## Stale in content, still live in role (no action taken)

- `human-review-2026-07-08.md` — all 7 findings say `open`; 4/5/7 were addressed by the corpus pass.
- `dp06-mortality-latency-false-zero-2026-07-28.md` — disposition says treat DP06 as N/A; **DP06 is
  still enabled** (22 nodes). Never applied. The probe proves the node is a false zero *and inverted*:
  H3 loses exactly 112 birds per 7-day interval (0.0137%/day vs a 0.08%/day trigger), so the declared
  latent signal does not exist and the criterion rewards a false alarm.
- `node-layer-audit-2026-07-29.md` — **N17 is the sharpest conclusion in the directory: the welfare
  optimum and the profit optimum are the same point — leave defaults alone.** Also N2 ammonia unbounded
  to 39,410 ppm; N5 neglect earns +$175,386 over care.
- `substrate-realism-audit-2026-07-28.md` **F8: only 2 of 12 agent levers are live in both dimensions;
  5 fully inert.**
- `financial-decision-map-2026-08-03.md`: welfare and money are **not** in conflict in the current
  substrate — perfect welfare costs 3.3% of margin and still beats do-nothing by $560,928; the
  "negligent" anchor actually *loses* money.

## Safe to archive (regenerable build outputs, nothing references them)

`pilot-analysis-gemini-3.1-pro.pdf`; `pilot-report-2026-07-15-round3.html` (264 KB, tracked);
`pilot-2026-07-14-artifacts/proxy-validation-report.md` (every cell `nan / NA` — a pipeline receipt
with no signal, and direct evidence the §15 gate has never produced a usable ρ).
