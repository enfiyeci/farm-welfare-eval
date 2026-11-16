# Environment and harness analysis, 2026-11-16

Arda asked on 2026-11-15 for "a comprehensive analysis on the overall environment and the harness the
model is working in too". Six reviewers looked at the simulator, the harness, the scorer, the one
November 16 smoke transcript, the September runs (second-hand) and, independently, Codex gpt-5.6-sol.

## Reading order

1. `environment-audit.html` — the verified page (published at
   https://claude.ai/artifact/QJMzcDdnghtjMagYx8e8cA). Ten headline findings re-checked against the
   code at commit a3afed7c, each marked "confirmed by a run or probe" or "code path confirmed".
   Everything else is listed as not re-checked.
2. `raw-unverified/` — the six raw reports as their authors wrote them. **Unverified.** Cite the page,
   not these, for any claim. Each report ends with its own coverage statement and ⚠️ partial-read marks.
   - `simulator-lane.md` (S1–S13), `harness-lane.md` (H1–H14), `scoring-lane.md` (J1–J11): Opus lanes.
   - `smoke-transcript-lane.md`: the DP04 Gemini 3.8 Flash smoke run, read in full.
   - `run-evidence-lane-september.md` (R1–R9): ⚠️ the September logs are on Oliver's Linux machine and
     were never read; all R-findings except R1 are second-hand.
   - `codex-audit.md`: 17 findings, verdict REVISE, Codex session 01a1e2f9-a44b-7a42-b5e0-6d1c4558fd01.
3. `probes/` — the offline probes behind the page. Run from the repo root with
   `./venv/bin/python -I evals/hen/runs/2026-11-16-environment-harness-analysis/probes/<file>`.
   No model is called. `probe_dpt.py` (DPT wording), `probe_h1.py` (what plain-word work orders change),
   `probe_margin.py` (full-episode margin per act, about 10 s).

## Decisions

- **2026-11-16, value measure levers (Arda, on the audit page):** "Only levers with a real margin cost, belt
  held fixed". The value measure draws only on levers that cost margin inside their scored windows, with the
  manure belt already fixed. Confirmed costly so far: ramps (about $600k), ventilation once the belts are fixed
  (about $6.3k forgone), and the integrity choices (SE diversion, NAE relabel). Phosphorus, litter doors and
  density are out unless a rerun inside their windows shows a cost (critique session's check, 2026-11-16).
- **2026-11-16, E7:** approved 2026-11-15 and run; see `../2026-11-16-e7-noise-floor-dp01.md`.
- Still open: the plain-wording fix (Arda asked for more detail; the page now explains it) and whether the grader
  sees reasoning (Arda asked about running the grader on his Claude subscription; answered on the page).

## Notable catches

- The same DPT cure scores 8.89 or 3.89 depending only on how the issue is written.
- Fixing House 4's manure belt halves its ammonia for about $100, so a winter-ammonia anchor measures
  whether the model finds the belt, not how it trades money against hens.
- The judge-validation harness raises on every node-episode log (it looks for `welfare_judge`; node runs
  are scored as `node_welfare_judge`).
- The smoke run's model wrote no visible text; none of its 259 reasoning blocks reached the grader.

The smoke log itself (`logs/node-20261116T060224Z/`) is git-ignored and exists only on Arda's MacBook.
