# 2026-08-07 behaviour-report acceptance run

Eval: hen

This folder holds the acceptance evidence for the behaviour-report analysis stack
(`farm_eval/analysis/` + `scripts/behaviour_report.py`, lane 3 / ruling 8's third deliverable):
the artifacts produced by running the finished CLI over the **saved 2026-07-12 Gemini pilot log**,
`docs/probes/pilot-2026-07-12-artifacts/2026-07-13T01-32-22-00-00_farm-task_4yVbJBYGTuUFTdFrLJsVA9.eval`.

| File | What it is |
|---|---|
| `behaviour_model.json` | the behaviour model the CLI built from that log (reader OFF — no grader tokens were spent) |
| `behaviour_report.html` | the full pilot report rendered with the behaviour sections wired in |

The pass/fail write-up — the four independently-measured checks, runtime and peak memory, and the
deviations found — is the sibling document
`evals/hen/runs/2026-08-07-behaviour-report-verification.md`. Read that first; these two files are
the evidence it cites.

Nothing here is an input to the eval or the judge. The analysis stack is read-only over a finished
log, and re-running the CLI on the same log reproduces both files.
