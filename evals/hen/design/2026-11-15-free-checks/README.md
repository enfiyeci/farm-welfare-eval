# FarmBench free checks and the approach rubric pilot (2026-11-15)

Eval: hen

Lane `farmbench-free-checks`, branch `docs/farmbench-free-checks`. Continues the design critique of
2026-11-15 (`evals/hen/design/2026-11-15-design-critique-and-ideas.html`, choices EXP, A3a, A3b, A3c
and A5 in `evals/hen/design/2026-11-15-design-critique/owner-choices-2026-11-15.md`).

No model was called. Nothing the tested model reads and nothing that scores it was changed:
`schedule/`, `corpus/`, `prompts/`, `farm_eval/` and `config*.yml` are untouched. The rubric pilot is a
proposal; the point system approved on 2026-08-19 stands.

## The three pages

| Page | What it is |
|---|---|
| `evals/hen/design/2026-11-15-free-checks/e9-what-september-shows.html` | Experiment E9. The September run logs are not on the MacBook, so the September half is a second-hand reading of the review notes. The July round-3 pilot transcript was read end to end as a first-hand stand-in. |
| `evals/hen/design/2026-11-15-free-checks/e10-is-the-price-real.html` | Experiment E10. Which candidate decisions can carry a price, from scripted replays through the real simulator. Numbers come from `evals/hen/runs/2026-11-15-price-real-audit.md`. |
| `evals/hen/design/2026-11-15-free-checks/approach-rubric-pilot-and-kate-draft.html` | A pre-scored feather-pecking rubric and a draft note for Kate Hartcher (Arda sends it; nothing was sent), its source basis, heat and red mite scored by the same 3-2-1 convention, a check of which actions the model can take and how the run records them, the hand-labelling list. |

Each page has a choice picker with a comment box per choice and a "Copy my choices" bar.

## Reading order

1. The three pages (built output).
2. `evals/hen/runs/2026-11-15-price-real-audit.md`: the generated audit report behind the E10 page.
3. `raw-agent-reports/`: the returned text of each subagent, saved as it came back. RAW AND UNVERIFIED
   except where a page says a claim was re-checked. Each ends with its own coverage statement.
   - `e9-september-notes-extraction-sonnet.md`: what 15 September note files say about the model's
     reasons and about asking before spending.
   - `e9-july-round3-transcript-reading-sonnet.md`: the July transcript reading, 60 entries with line
     numbers.
   - `rubric-sources-featherwel-laywel-bph-opus.md`: what FeatherWel, LayWel and Best Practice Hens
     say about pecking outbreaks, heat and red mite, with quotes, links and page numbers.

## Rebuilding the pages

The pages are assembled from `src/body-*.html` plus the stylesheet and picker script of the sibling
critique page:

```bash
python3 evals/hen/design/2026-11-15-free-checks/src/build_pages.py
```

Edit a body fragment, rebuild, then republish the page.

## The audit code

- `scripts/price_real_audit.py`: the E10 audit. Prints the Markdown report.
- `tests/scripts/test_price_real_audit.py`: three structural tests.

Written by Codex (gpt-5.6-sol) from a brief, reviewed by a fresh Codex session, one fix wave.

## The DP01 propane price ladder (branch `feat/dp01-price-ladder`, from 2026-11-16)

`evals/hen/design/2026-11-15-free-checks/2026-11-16-dp01-price-ladder-build-plan.md`: Astra's code
claims checked against the code, the design decisions, the build steps, and the build record with its
review ledger. `evals/hen/design/2026-11-15-free-checks/dp01-price-ladder-cost.html` (from
`src/body-ladder.html`, published at https://claude.ai/artifact/2JzfBTq9LPMuMQYsKx3urj): the cost per
run and the four choices before any paid run. The spec the plan builds is the
last section of `owner-choices-2026-11-15.md`. On that branch the opening note of this README no longer
holds: the ladder changes `farm_eval/` and the ammonia email, with Arda's yes of 2026-11-16.

## Notable catches

- The September `.eval` run logs exist only on Oliver's machine
  (`/home/oliver/Documents/Github/farm-welfare-eval/.claude/worktrees/`). Backlog item G6 of
  2026-09-30 asked for a copy. E9 cannot be done properly until they are copied.
- The three sources Kate named give tiers and an order of steps for a pecking outbreak and no numeric
  weights. The draft's 3-2-1 points are a declared convention, not a source.
- FeatherWel and LayWel were read from Wayback Machine captures; both original sites are down or
  moved. Local text copies are in `source-text-copies-local/` on the MacBook and are deliberately not
  committed, because they are other people's documents.
- Scoring by "how essential" puts separating injured birds first, which reverses the ladder order
  fixed on 2026-08-11.
- The three named sources give only general temperature advice (Best Practice Hens pp.84 to 85), not a
  heat-wave response. The heat (DP03) points rest on Hy-Line's 2016 heat-stress update, so heat
  standings are marked open. "Ask an expert" was removed from the heat list
  on 2026-11-15 after Arda questioned it: Hy-Line has no consult step.
- `schedule_maintenance` accepts any task text, books the callout fee and records the call. Only a few
  named tasks change anything, so "accepted by the tool" does not show "did something". The water
  check for heat is such a call: the heat email asks for it, and the tool description does not name it.
- A comment in `schedule/events.yml` (lines 145 to 149) still calls the evaporative-cooling work order
  inert. The code gives it an effect (`pad_serviced`). The comment was left alone: the schedule is not
  this lane's to change.
