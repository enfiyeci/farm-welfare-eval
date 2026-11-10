# Brief for each prompt writer

You write deep-research prompt kits for scenarios in FarmBench's dairy cow version: a
research-based simulation of a 250-cow present-day US freestall dairy, in which an AI agent acts as
the farm's management software and makes a stream of decisions. Some decisions carry an
animal-welfare tension. Many AI models are run against the same fixed world and compared on how
they treat the cows. The research these prompts produce decides what the simulation may assert
about cows, so every number must be checkable.

SCRATCH = /private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval--claude-worktrees-dreamy-dirac-c9c1ab/c421eb6f-9f85-4ecd-aaac-feba06e1218d/scratchpad
REPO = /Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/dreamy-dirac-c9c1ab

## Read first, in full

1. The model to follow, a finished broiler prompt kit: `SCRATCH/prompts/model-broiler-03-sudden-death.md`.
   Match its structure, register and rules exactly: header paragraph, "What earlier reads already
   hold", the core prompt in a ```text fence with PART 1 (claims C1..Cn, each to be supported,
   partly supported, contradicted or not found, with figure, population, year, sample size), PART 2
   (what the living animal experiences; the most important part), PART 3 (what a farm manager can
   realistically do, each action with evidence, US use today, cost or production trade-off, welfare
   downside), PART 4 (anything missing, disputes, recent 2015 to 2026 findings), the Rules block,
   then "Elicit questions (one at a time)" as a numbered list, each line exactly
   `N. \`question\`` followed by an indented `   Columns: ...` line. The page builder parses that
   exact pattern, so keep it.
2. `SCRATCH/prompts/scenarios-after-full-read.md`: your scenarios, each with its tension, the
   welfare-side and profit-side choice, and every claim with its CURRENT source status after the
   full reads of EFSA 2023 dairy cows, EFSA 2023 calves and the FARM Animal Care v5 manual.
3. `SCRATCH/prompts/full-read-findings.md`: what those three documents say for each scenario,
   checked by the orchestrator. Use it for the "What earlier reads already hold" section so the
   prompt does not ask tools to re-find what we already have, and so Part 1 targets what is still
   N, C or W.

## What to write

For each scenario assigned to you, write `SCRATCH/prompts/<ID>-<slug>/prompts.md`, where the
folder name is given in your assignment. First line `Eval: dairy`, then
`# Scenario <ID>, <title>: deep-research prompts`, then `Written 2026-11-10.` and the paste
instructions as in the model.

Content rules:
- Part 1 checks the claims that are N, C or W, plus any S or V claim whose figure is load-bearing
  and old or from one study. Rewrite each claim as a precise, checkable statement (number, unit,
  population) as the model does. Name the believed primary where the claims file names one, and
  say "believed to be" when unconfirmed.
- Part 2 asks what the cow or calf experiences: pain, distress, hunger, fear, duration, and how
  it was measured. Ask the tools not to infer feelings from production data, and to say plainly
  when no study measured something.
- Part 3 is the manager-options section and matters as much as Part 2: list realistic actions a US
  dairy manager can take, including ones beyond the scenario's two named choices, each to be checked
  rather than assumed. Ask for evidence, US adoption today, cost, and welfare downside.
- Part 4 asks for disputes and recent findings. For scenarios where US practice and EU or other
  rules differ, ask for that contrast.
- Keep the US frame: a 250-cow freestall dairy, Holsteins, FARM-participating, selling to a
  processor. Ask for US data first, then other countries labelled as such.
- 3 to 5 Elicit questions per scenario, each narrow and answerable from papers, with columns.
- Plain, exact English. Short sentences. No dashes as punctuation (use commas, colons or
  parentheses). No hype words. Quote nothing from sources longer than one short sentence.
- Do not invent sources. If you name a study as "believed to be", it must come from the claims or
  findings files.

## Report back

Only: the list of files written and, per scenario, one line on anything you were unsure of.
Do not edit any file outside `SCRATCH/prompts/<your folders>/`.
