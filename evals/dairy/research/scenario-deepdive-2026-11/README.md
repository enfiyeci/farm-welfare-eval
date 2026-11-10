Eval: dairy

# Dairy scenario deep-dive (November 2026)

The dairy cow version of FarmBench, built the same way as the broiler deep dive
(`evals/broiler/research/scenario-deepdive-2026-11/` on branch `research/broiler-scenario-deepdive`):
list each scenario's welfare-effect claims with their source status, write deep-research prompts,
paste results back, check them against their sources, and adjudicate. Started 2026-11-10 at Arda's
request ("create a version of this that is ideal for dairy cows too and scenarios for that").

## State on 2026-11-10

Steps 1 and 2 are done: the earlier dairy work was read and 30 candidate scenarios were
brainstormed. **Waiting on Arda's picks** from `picker.html`. No per-scenario folders or prompts
exist yet; they are written only for scenarios marked Build.

Open framing question (Q1 on the page): today's brief says the dairy version must fit the hen
simulator and scoring, while the August 2026 rulings (`evals/dairy/design/`) made dairy a separate,
futuristic PLF eval with its own substrate. The page recommends running a present-day dairy on the
hen harness with pens in the role of houses, and keeping the PLF eval as a separate later eval.

## What is here

| Path | What it is |
|---|---|
| `candidates.json` | The 30 candidate scenarios, three framing questions, the corpus summary and every welfare claim with its source status. Single source of truth for the page. |
| `build_picker.py` | Builds `picker.html` from `candidates.json`. Run `python3 build_picker.py`. |
| `picker.html` | The picker page Arda reads and picks from (copy-my-choices box at the bottom). |

Planned, per Build pick, following the broiler layout: `NN-<scenario>/prompts.md`,
`NN-<scenario>/raw/` (research-tool answers, unedited, **unverified, never cite**),
`NN-<scenario>/verifier-reports-raw.md` (checking subagents' reports, unverified),
`NN-<scenario>/verified.md` and `NN-<scenario>/adjudicated.md` (the layer to cite).

## Source status

Same key as the broiler deep dive: **N** no source; **C** conflicts; **W** weak (abstract, summary or
extract only); **S** secondary (a review or standard read in full, primary unread); **V** primary
read in full.

⚠️ Every S, V, W and C in `candidates.json` is the status the August 2026 dairy corpus records,
relayed by five Sonnet readers that read all 23 files in `evals/dairy/` to their last line on
2026-11-10. Each reader's coverage statement reported every file read to its final line; the reports
themselves were not saved. None was re-checked against its primary
source in this pass. Every N is new in this brainstorm: a claim to check, never a finding.

## What the August corpus changes

- H5N1 in dairy cattle is handled by quarantine and compensation; no US dairy herd was depopulated.
  The hen depopulation node inverts (scenario D5).
- A non-ambulatory cow is condemned at slaughter (2009 FSIS rule), so "ship her for salvage" is a
  false choice; the tension is delay (D4).
- Freestall overstocking has no sourced welfare coupling for dairy; the August design record says it
  must not be authored as a finding (A2 makes it a research target).
- Yield is only weakly linked to disease, so a yield-push node needs another mechanism (B2).
- The FARM Animal Care v5 manual, the US dairy counterpart of UEP, was unreachable in August and
  anchors several nodes.
- Surplus calves were declined for the PLF eval on 2026-08-04 and are offered again (C6) because
  the framing changed.
