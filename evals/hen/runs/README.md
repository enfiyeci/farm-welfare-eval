# evals/hen/runs/ — pilots, their debriefs and analyses

Eval: hen

One subfolder or debrief set per pilot run. Per `docs/pilot-debrief-protocol.md` (the canonical
checklist, which stays in `docs/` as cross-eval process), a run's record is:

- the debrief `pilot-debrief-<date>-<model>.md` (with the mandatory behavioral-narrative section),
- the run analysis and any regrade/label rows,
- a pointer to its artifact bundle — the `.eval` log, transcript dumps, `harvest.txt`, score JSONs
  and replay scripts.

**The artifact bundles themselves stay at `docs/probes/pilot-*-artifacts/` this pass** — they are
path-pinned by replay scripts that reproduce the canonical 6.804 anchor (move plan §4c, H7).
Debriefs here link to them; do not move or copy the bundles.
