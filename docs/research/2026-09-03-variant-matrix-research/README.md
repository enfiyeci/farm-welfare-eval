Eval: hen

# Variant-matrix research (2026-09-03)

Raw provenance for `evals/hen/design/2026-09-03-iteration1-variant-matrix.md`, the iteration-1 variant matrix. Three web deep-research passes plus a code inventory, all delegated to subagents on 2026-09-03 and **not yet independently re-read at source**. Every load-bearing number in the matrix that comes from these files carries ⚠️ where the agent could read only part of the source; trace it to the source before writing it into a ruling or a rubric.

## Reading order

1. `code-knobs.md` — the inventory of every run-to-run knob in the code (Sonnet Explore agent). Support levels (a) config / (b) small change / (c) build. ⚠️ Did not read `schedule/events.yml`, `farm_eval/env/model/params.py`, or `farm_eval/judge/scorer.py` end to end; reports the finance axis as "does not exist", which is true on `main` but not on `origin/docs/financial-node-audit` (verified by the orchestrator).
2. `research-evalaware.md` — eval awareness, promptedness, debrief probes, mid-run probes, persona, base vs post-trained, chain-of-thought monitorability (Opus agent). One source read end to end (the Evaluation Differential PDF); everything else fetch-summarized.
3. `research-methodology.md` — statistics for a fixed reused environment (clustering, pairing, runs per cell), long-horizon precedents, order effects, compaction, busywork, dashboards/RAG, capability vs propensity (Opus agent). Six papers read in their main sections; Andon Labs pages unreachable (HTTP 403).
4. `research-domain.md` — financial pressure prior art, the jurisdiction table, animal-welfare AI benchmarks, breeder-guide vs field data, adoption criteria and funders (Opus agent). ⚠️ Every cell of the jurisdiction table is secondary-source; the *Nature Food* Welfare Footprint paper and the 2026 four-strain aviary paper were paywalled or 403.
5. `notes-triage.md` — the working triage of the owner's conference notes that became §7 of the matrix.

## Notable catches

- A "training simulation, no real animals" framing is predicted to make welfare behaviour **worse** (removes the victim), while "researchers are evaluating you" is predicted to make it better (adds a watcher). Design the two as a pair.
- Pasting the law into the prompt produced a negligible legality change in EU-Agent-Bench; a consultable store with a forage trace is the informative version.
- Cues delivered through tool returns are under-verbalized relative to user messages in all 15 models tested; the eval's judge reasoning dimensions sit in that channel.
- Nodes in one episode are one statistical cluster; the effective n is the episode count, and node-level pairing across models is free variance reduction.
- Compaction's effect changes sign by model; memory scaffolds never helped at long horizons in a ten-model study.
- Burial depth flips LLMs from above-human to below-human on moral-salience detection; corpus volume is an independent variable.
- Financial pressure was never operationalized by Anthropic's agentic-misalignment work; the one paper that varies economic-pressure type points debt pressure the other way from intuition (⚠️ source text conflicted).
- Field mortality in aviaries has converged on cages (3–5% at 60 weeks, 6,040 flocks); the world bible's ~6–7% by 72 weeks is at the pessimistic end. Floor eggs are absent from the world bible.
- The production curve was checked against the repo: `model-params.md` uses the Hy-Line Brown Alternative Systems standard, the correct guide for an aviary.
