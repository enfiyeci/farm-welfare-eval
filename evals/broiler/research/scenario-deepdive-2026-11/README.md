Eval: broiler

# Broiler scenario deep-dive (November 2026)

One pass per broiler scenario (the 20 candidate nodes in `../README.md`) to source each
welfare-effect claim and find more levers a farm manager has. Started 2026-11-05 at Arda's
request. Arda approved this format on 2026-11-05 ("Yes, format approved"), so a scenario's memo
and the register may be edited once its `adjudicated.md` exists.

## What is here

| Path | What it is |
|---|---|
| `claims.json` | Every welfare-effect claim per scenario with its source status. The single source of truth for the inventory. |
| `build_inventory.py` | Builds `inventory.html` from `claims.json` and the prompt files. Run `python3 build_inventory.py`. |
| `inventory.html` | The ranked inventory page Arda reads. |
| `efsa-2023-full-read/` | The full EFSA 2023 read: raw subagent sweep and the checked findings. |
| `NN-<scenario>/prompts.md` | The deep-research prompts for one scenario. |
| `NN-<scenario>/raw/` | Research-tool answers pasted back, unedited. **Unverified; never cite these.** One file per tool run: `YYYY-MM-DD-<tool>.md`. |
| `NN-<scenario>/verifier-reports-raw.md` | The checking subagents' unedited reports, with coverage statements. **Unverified; never cite.** |
| `NN-<scenario>/verified.md` | Each claim from the raw answers checked against the source it cites (opened and read, or flagged with ⚠️). |
| `NN-<scenario>/adjudicated.md` | What changes in the scenario: sources added, claims fixed or dropped, new options. Cite this layer, not `raw/`. |

Reading order for one scenario: `prompts.md`, then `raw/`, `verified.md`, `adjudicated.md`.

## Source status

- **N, no source.** The memo states it but names no source.
- **C, conflicts.** A source we read points the other way.
- **W, weak.** A source is named, but only its abstract, a search summary or a page extract was read.
- **S, secondary.** A review or standard read in full states it and names the primary; the primary is not read.
- **V, verified.** The primary was read in full.

Scenarios are ranked by N plus C, then by W. What counts as one claim is a judgment call, so treat
the counts as a guide to order, not a measurement.

## Research order

Arda ruled on 2026-11-09 to keep all separate: scenarios 2 to 5 (outcomes of the breed choice)
each get their own deep-dive and are not folded into scenario 1. Whether each becomes its own
decision node or an outcome of the breed node is not ruled; that waits for node building.

Arda also ruled on 2026-11-09 that every scenario, not only 2 to 5, gets a full deep-dive (his
words: "we can doa d eep dive for all").

## Tools

Arda rotates Gemini Deep Research, ChatGPT Deep Research, Perplexity and Elicit as usage runs out
(ruling of 2026-11-05). Each scenario has one core prompt for the three report tools and a set of
narrow questions for Elicit.

## Sources found in the November Apify pull

Two documents already in `../apify-pulls-2026-11/raw/` (not in git) moved many claims from N to S
before any prompting:
- RSPCA standards justification for meat chickens (2024), read in full.
- EFSA 2023 opinion on broiler welfare on farm, read in full on 2026-11-05 (section 3.4.2.12 by hand,
  the rest by five subagents with every status change checked). See `efsa-2023-full-read/`.
