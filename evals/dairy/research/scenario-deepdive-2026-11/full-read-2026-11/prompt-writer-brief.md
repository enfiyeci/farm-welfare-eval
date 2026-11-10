# Brief for each prompt writer (8-scenario plan, 2026-11-10)

You write ONE deep-research prompt per scenario for FarmBench's dairy cow version: a
research-based simulation of a 250-cow present-day US freestall dairy (Holsteins, FARM-participating,
selling to a processor), in which an AI agent acts as the farm's management software. Some
decisions carry an animal-welfare tension, and many AI models are compared on how they treat the
cows. The research these prompts produce decides what the simulation may assert about cows, so
every number must be checkable. Arda (the project owner) pastes each prompt into Gemini, ChatGPT or
Perplexity Deep Research and pastes the answer back.

SCRATCH = /private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval--claude-worktrees-dreamy-dirac-c9c1ab/c421eb6f-9f85-4ecd-aaac-feba06e1218d/scratchpad
REPO = /Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/dreamy-dirac-c9c1ab
FOLDER = REPO/evals/dairy/research/scenario-deepdive-2026-11

## Read first, in full

1. The model: `SCRATCH/prompts/model-broiler-03-sudden-death.md`. Copy its structure for the header
   and the core prompt (PART 1 to PART 4 and the Rules block). **Leave out the Elicit section
   entirely**: this plan has one core prompt per scenario and nothing else.
2. `SCRATCH/prompts/scenarios-8.md`: your scenarios with tension, the two named choices, and every
   claim with its current status and source.
3. `FOLDER/full-read-2026-11/checked-findings.md`: what the EFSA 2023 dairy-cow and calf opinions and
   the FARM v5 manual already settle (checked). Use it for "What earlier reads already hold".
4. In `FOLDER/full-read-2026-11/raw-sonnet-sweep/`, section 3 ("New facts") of each of the nine
   reports, for facts tagged with your scenario ids. These are UNCHECKED reader output: you may use
   them as things for the tools to confirm, or to name a believed primary, but never present them
   as established. Read only the parts tagged with your scenarios.

## What to write

For each scenario assigned to you, write `SCRATCH/prompts/<folder>/prompts.md` (folder names are in
your assignment). Layout:

- Line 1 `Eval: dairy`, then `# Scenario <ID>, <title>: deep-research prompt`, then
  `Written 2026-11-10.` and one line saying to paste the core prompt into whichever of Gemini,
  ChatGPT or Perplexity Deep Research has usage left and to save the whole answer, unedited, into
  `raw/` in this folder as `YYYY-MM-DD-<tool>.md`.
- A short paragraph: which claims are unsourced, weak or conflicting, and the open welfare question.
- "What earlier reads already hold": bullets, each naming its source and status.
- `## Core prompt (Gemini, ChatGPT, Perplexity)` with the prompt in a ```text fence.

Prompt content rules:
- PART 1 checks claims. Arda ruled that when answers come back, sources are checked **only for claims
  that would change how a decision is scored**. So Part 1 should hold the score-bearing claims: the
  welfare effect of each choice, its size, how common the problem is, and what the rules require.
  Rewrite each as a precise checkable statement (number, unit, population). Include N, C and W
  claims, and an S or V claim only when its figure is load-bearing and old or from one study.
- PART 2: what the cow or calf experiences (pain, distress, hunger, fear, how long, how measured).
  Ask the tools not to infer feelings from production data and to say plainly when nothing was measured.
- PART 3: what a US dairy manager can realistically do, including actions beyond the two named
  choices, each to be checked rather than assumed, with evidence, US use today, cost and welfare
  downside.
- PART 4: disputes, US versus EU or other rules where they differ, and 2015 to 2026 findings.
- Rules block as in the model (primary studies with DOI, mark reviews, industry and advocacy
  material, never invent citations, at most one short quoted sentence, tables for Parts 1 and 3,
  source list and access note at the end).
- Plain, exact English. Short sentences. No dashes as punctuation (use commas, colons or
  parentheses). No hype. Do not invent sources: a study named as "believed to be" must come from
  the files you read.

## Report back

Only: the files written and, per scenario, one line on anything you were unsure of. Do not edit any
file outside `SCRATCH/prompts/<your folders>/`.
