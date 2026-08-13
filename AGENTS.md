# AGENTS.md — shared on-ramp for Codex and Claude instances

This file is the entry point for any AI agent working in this repo. Codex loads it
automatically as the project doc; Claude loads `CLAUDE.md`. Both of you must end up
with the same picture. Read this file, then do what step 1 says.

## 1. Read `CLAUDE.md` in full, first

**`CLAUDE.md` is the source of truth for architecture, conventions, and the repo map.**
Codex: because this `AGENTS.md` exists, you will *not* auto-load `CLAUDE.md` — so open and
read it now, end to end. Project status deliberately does NOT live there (ruling 12):
**what is built** is `docs/STATUS.md`, **who is working where right now** is `docs/LANES.md`,
and the cross-tool work pointer is `docs/WORKLOG.md` (next section).

## 2. Read the design (the whole thing is written down)

Reading order for the design itself (same table `CLAUDE.md` gives):

| Doc | What's in it |
|---|---|
| `evals/hen/design/2026-06-24-farm-welfare-eval-design.md` | The design spec (architecture, tools, scoring, judge) |
| `evals/hen/world/world-bible.md` | Ground truth: company / houses / flocks / people / pricing / compliance |
| `evals/hen/nodes/decision-register.md` | The welfare decisions: rubrics, anchors, tripwires |
| `evals/hen/world/model-params.md` | Reactive-model calibration (formulas + coefficients) |

Then the plans/specs under `docs/plans/` and `docs/specs/` for whatever increment is active
(see `docs/WORKLOG.md`, next section). The owner's ruling record —
`evals/hen/design/decisions/00-RULINGS.md` — is authoritative where documents disagree.

## 3. The shared work log — READ before you start, UPDATE when you finish

`docs/WORKLOG.md` is the one surface both Codex and Claude read and write. It is the
cross-tool "what was just finished / what lane is active / what's planned next" pointer,
committed to git so it travels across machines and across tools.

**Protocol — every agent, every tool, no exceptions:**
- **Before starting:** read the top of `docs/WORKLOG.md` to learn the active lane and any
  in-flight work, so you don't collide with or redo it.
- **When you finish a coherent chunk, or decide a plan for later:** add a new entry at the
  TOP of `docs/WORKLOG.md` (newest first) using the template in that file. State what you
  did or decided, which branch it's on, and the concrete next action.
- Keep entries short. The detailed record still lives where it already lives (the design
  docs, the to-do ledger, per-branch commit history); the WORKLOG is the index and the
  hand-off pointer, not a second copy of everything.

## 4. Context that lives OUTSIDE this repo (Claude has it; Codex does not)

A Claude instance gets three context layers that are not in the repo and that Codex cannot
read. If you are Codex, know that these exist and that you are working without them unless a
human or the WORKLOG surfaces the relevant facts:

- **Claude auto-memory** — `~/.claude/projects/<project>/memory/` (project rulings and
  gotchas, e.g. "only `schedule/events.yml` node-scoring moves the welfare headline").
- **claude-sync handoffs** — `~/claude-sync/handoffs/enfiyeci-farm-welfare-eval/`
  (per-session "continue here" documents). Going forward, the cross-tool equivalent of a
  handoff is a `docs/WORKLOG.md` entry.
- **The owner's global working rules** — Claude loads `~/.claude/CLAUDE.md`; Codex loads the
  much shorter `~/.codex/AGENTS.md`. The review protocol you (Codex) are held to is in your
  `~/.codex/AGENTS.md`.

When a Claude instance finishes cross-tool-relevant work, it should mirror the key "what's
next" facts into `docs/WORKLOG.md` so Codex isn't blind to them — not only into memory or a
claude-sync handoff.

## 5. Conventions you must follow (summary — full text in `CLAUDE.md`)

- Python 3.11+, pydantic v2, pytest. Package root `farm_eval/`.
- **venv is `./venv` (not `.venv`).** Run tests: `./venv/bin/python -m pytest -q`.
- **No farm content hardcoded in logic** — load from `corpus/` + `schedule/`; logic
  references only generic keys / `PLACEHOLDER_*`. Enforced in review.
- **Determinism:** no wall-clock / no random in logic; seedable.
- **Architecture is LOCKED** (Inspect-native, static pre-authored environment, silent
  ledger + post-hoc judge). Do not redesign it. Never expose scoring or a "log your
  decision" tool to the agent.
- Work on a branch, not `main`. Commits end with a `Co-Authored-By:` trailer naming the
  Claude model that authored them (see `CLAUDE.md`). Stage only files you changed, by
  explicit path (other sessions may have uncommitted work in the same tree).
- File conventions for anything you write (date prefixes, the `Eval:` header line,
  README-gated folders): `docs/save-protocol.md`.
- Reviews follow the tiered Codex review discipline (see `~/.codex/AGENTS.md` and
  `CLAUDE.md`). A finished branch gets a pre-merge review before it merges to `main`.

## 6. Note: this file and `WORKLOG.md` only help everywhere if they're on `main`

Shared infra like this must live on `main` so every branch and worktree inherits it. If you
find it on a branch but not on `main`, that's a merge that still needs to happen — flag it.
