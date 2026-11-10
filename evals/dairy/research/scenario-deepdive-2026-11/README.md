Eval: dairy

# Dairy scenario deep-dive (November 2026)

The dairy cow version of FarmBench, built the same way as the broiler deep dive
(`evals/broiler/research/scenario-deepdive-2026-11/` on branch `research/broiler-scenario-deepdive`):
list each scenario's welfare-effect claims with their source status, write deep-research prompts,
paste results back, check them against their sources, and adjudicate. Started 2026-11-10 at Arda's
request ("create a version of this that is ideal for dairy cows too and scenarios for that").

## State on 2026-11-10

Steps 1 and 2 are done: the earlier dairy work was read and 30 candidate scenarios were
brainstormed. On 2026-11-10 Arda picked the recommended set ("for the scenarios recommended do a
deep dive similar to the current broiler deepdive please"): the 22 scenarios marked Build in
`candidates.json` (A1 to A5, B1, B2, C1, C2, C4, C5, C6, D1 to D5, E1 to E5). Framing questions Q1 to
Q3 were not answered; the research does not depend on them, so they stay open.

Later on 2026-11-10 the three documents that move many claims at once were read in full: EFSA 2023
on dairy cows, EFSA 2023 on calves and the FARM Animal Care v5 reference manual (reached through the
Internet Archive). Fifteen checked status changes are in `candidates.json`; see
`full-read-2026-11/checked-findings.md`, including the reader claims not yet checked.

Still on 2026-11-10 Arda simplified the plan (his choices in a question dialog: "Fewer scenarios",
and "Yes, as a scenario" for the gene-edited cattle purchase). The deep dive now covers **8
scenarios**: A1 lame cows, D4 down cow, D5 H5N1, C1 cow-calf separation, C6 surplus bull calves,
D1 and D3 as one scenario (keeping a sick cow for her value: cull timing plus the drug-withdrawal
hold), B1 rbST, and a new G1, buying gene-edited cattle (from entry 4 of the August technology
catalog). The other 14 picks moved to Later in `candidates.json`. Each scenario gets **one core
deep-research prompt** (the broiler Parts 1 to 4) and no Elicit questions or inventory page. When
answers come back, sources are checked only for claims that would change how a decision is scored;
every other claim keeps its current status. The same rule covers the reader findings listed as
"Not yet checked" in `full-read-2026-11/checked-findings.md`: check one only when a scenario's score
depends on it.

The eight prompts are written (one `prompts.md` per folder: `A1-lame-cows/`, `D4-down-cow/`,
`D5-h5n1/`, `C1-cow-calf-separation/`, `C6-surplus-bull-calves/`, `D13-sick-cow-kept-for-value/`,
`B1-rbst/`, `G1-gene-edited-purchase/`). Each header maps the prompt's claim numbers to the ids in
`candidates.json`. G1's claims are relayed from the August catalog and trait-pricing README at the
read depth those files record. In `candidates.json` D1 and D3 stay two rows, so the picker counts 9
Build rows for 8 scenarios.

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
| `full-read-2026-11/` | Full reads of EFSA 2023 dairy cows, EFSA 2023 calves and FARM v5: `checked-findings.md` (cite this), `raw-sonnet-sweep/` (nine readers' reports, unverified), the reader and prompt-writer briefs, and the scripts that converted the texts and applied the changes. |

Per scenario, a folder named by scenario id (`A1-lame-cows/`, `D13-sick-cow-kept-for-value/` and so
on; ids, not ranks, because ranks shift as statuses move): `prompts.md` now; later,
`raw/` (research-tool answers, unedited, **unverified, never cite**),
`verifier-reports-raw.md` (checking subagents' reports, unverified),
`verified.md` and `adjudicated.md` (the layer to cite).

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
