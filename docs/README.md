# docs/ — the cross-eval slot

Eval: cross

**The rule (ruling 13b): if a document belongs to one eval it lives under `evals/<eval>/`;
everything else stays in `docs/`.** Mixed documents live where their majority is; the minority side
gets a pointer line — never a copy, never a split.

File conventions for everything written in this repo: [save-protocol.md](save-protocol.md).

## What lives here

| Where | What |
|---|---|
| [STATUS.md](STATUS.md) | What is built, in what state (ruling 12's status doc) |
| [LANES.md](LANES.md) | Who is working where, right now |
| [save-protocol.md](save-protocol.md) | The six file-conventions rules |
| `specs/` | Cross-eval (engine) design specs and their assets |
| `research/` | Cross-eval research: the judge-methodology sweeps, the citation-integrity audit, briefing prior art, CLAUDE.md governance, the aquatic reading list |
| `design/v2-game-dynamics/` | Cross-eval elicitation methodology and its raw-claims provenance (never edit or prune the `raw-claims-*` files) |
| `handoffs/` | Session process records (cross-eval by function, whatever their subject) |
| `plans/` | Live cross-eval plans (the programme plan) |
| `probes/` | Path-pinned run-artifact bundles that stay this pass (move plan §4c) + the eval-awareness instrument index |
| `reorg/` | The 2026-08 reorganization record: the six catalogues, the move plan, the prior-art analyses |
| Process docs at root | `pilot-debrief-protocol.md`, `judge-validation.md`, `divergence-protocol.md`, `expert-labeling-pack.md`, `cleanup-backlog.md`, `future-work.md`, `lane-prompts.md` |
| Build tooling + generated output | `build-*.{js,py,mjs}`, `decisions-*.mjs`, `welfare-decisions.html`, `field-guide.pdf`, `inside-the-farm.pptx` — code does not move this pass |

## Where the eval-specific material went

- **Hen**: `evals/hen/` — design (incl. `design/decisions/00-RULINGS.md`, the owner's authoritative
  ruling record), research, nodes, world, judge, surface, runs, archive.
- **Dairy**: `evals/dairy/` — design, research.

The full move record: [reorg/](reorg/) (per-file destination table in the move plan).
