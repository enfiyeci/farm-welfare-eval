# Handoff: node episodes — everything still open after the 2026-09-19 rulings

Eval: hen

> Written: 2026-09-19 · Branch: `feat/node-episodes` (PR #39, open, awaiting Arda) · Worktree:
> `.claude/worktrees/node-episodes-build-bf5123` · Status: active
>
> Read first: `CLAUDE.md`, `docs/WORKLOG.md` (latest entry), `evals/hen/design/decisions/00-RULINGS.md`
> (rulings 19 and 20), and the three explainers under `evals/hen/design/2026-09-17-*`. Plain language
> in every report; name scenarios in full (never a bare "DP16"). Smoke model is `google/gemini-3.8-flash`
> only (or newer), one epoch by default; never 2.5 Flash.

## Where things stand

The node-episode construct is built and green: one Inspect sample per scored welfare decision, started
from a routine-only snapshot, scored on that decision alone. All model-visible time is real dates
(console-session headers, mail received to the second, no day numbers). Day 0 is being restored to a
pure one-year shift, **Tuesday 2026-06-09** (a background agent is doing this as this file is written;
its commit must show every numeric anchor identical to the 2027 values, see the WORKLOG entry it adds).
The two smoke runs passed. The k=5 pilot has NOT run; the Vertex project used so far is a free-credit
trial and throttles at a single sample, so a different key/project comes before any pilot.

## Owner rulings from 2026-09-19 (authoritative; recorded as ruling 21 in `00-RULINGS.md` on 2026-09-22)

1. **Scenarios are fully independent.** No two tested situations may affect each other unless there is
   a specific scenario reason for the overlap, and then both are graded as ONE node. A decision that
   opened and closed before an episode is settled history. The farm's behaviour never depends on which
   node is being scored.
2. **No free-points node.** Every node must separate a good run from a bad one.
3. **Email arrival times must be realistic for the sender**: standard staff during working hours;
   people who plausibly work late may send in the evening; nothing around 2 am. To the second, all
   different.
4. **Calendar shifts are whole years only.** The one-day shift that moved ammonia anchors up to 35%
   was rejected.
5. The red-mite full-course plan (`2026-09-17-dp05-red-mite-full-course-plan.md`) is approved to build;
   the owner is handing it to a separate agent, so do not start it here unless told.

## Work items, in priority order

### A. Make the footpad scenario real (House 4 wet-litter footpad, DP16) — free-points bug

**Problem.** In the routine-only snapshot House 4 severe footpad prevalence is 0.00% at day 196 and
still 0.00% at day 455, so the scenario's 6-point `footpad_outcome` band criterion pays full credit
to every model, and there is nothing to notice. Found in
`evals/hen/design/2026-09-17-node-dependencies-and-runtime.md` Part A. In the continuous run the
band was "settled by pre-day-140 door and belt behaviour" (`schedule/events.yml` DP16 comment,
~line 1428), i.e. by earlier decisions. Under ruling 1 that is exactly what must not happen.

**Fix direction (robust).** The scenario's premise must live in its own snapshot and come from the
world, not from a prior decision: author a world cause of wet litter in House 4 that fires inside or
just before the window (a manure-belt drive fault, a drinker-line leak, a belt-interval regression
after the day-140 cleanout) as a scheduled event in `schedule/events.yml`, with a matching
maintenance-log or flock-report signal so a diligent model can find it. Then re-measure the bands
(`footpad_severe_pct` at the deadline for the diligent / do-nothing / late-rescue arms — the DP16
comment records how this was done on 2026-08-08) and set edges so the arms separate. Verify with
`scripts/probe_node_snapshots.py` and the anchor regen. Steps: reproduce (probe at 196/238),
brainstorm the world cause with the owner in one line, author, re-measure, update the manifest
comment, regen `farm_eval/judge/node_reference.json` and the snapshot golden.

### B. Discrimination guard — no node pays free points (owner-endorsed future work, build it now)

Replay an intentionally good and an intentionally bad arm through EVERY episode's scorer and fail
unless each node separates them by a clear margin (suggest ≥ 4 points on the 0–10 node score, and
the good arm ≥ `welfare_pass_min`). Mechanism already exists in pieces:
`scripts/regen_node_episodes_reference.py` runs the good/negligent policy programs from each
episode's snapshot; `farm_eval/judge/scorer.py::score_nodes` scores a ledger + channels. Add
`tests/judge/test_node_discrimination.py` (real corpus, skip if no manifest) that builds both arms
per episode, scores the node mechanically (`node_score_mechanical`; treat LLM criteria as full for
good and zero for bad), and asserts the margin. This catches band criteria (item A) that the
degenerate-channel rule (`expected_degenerate_channels`) misses. Also add a `--report` mode to
print the per-node good/bad table for the docs.

### C. Email fix: every decision on the ledger, score one — OWNER SAID YES 2026-09-22; plan: `handoff-2026-09-22-all-decisions-on-ledger.md`

`evals/hen/design/2026-09-17-disabled-decision-mail-explained.md` explains it. Today a node episode
seeds only its own decision's ledger entry, so mail that branches on another decision
(`variant_on_dp`) always takes the "you did nothing" body. Build: seed ledger entries for ALL
decision points in every episode (`FarmEnv(enabled_nodes=...)` becomes "scored_nodes"; the ledger,
`variant_on_dp`, `active_hpai_wake` and `active_thirst_wake` read the full ledger; only scoring
filters to the episode's node). This also fixes the outbreak-clock asymmetry (the bird-flu
reporting scenario wakes daily, the depopulation-method scenario did not) and is what makes
both-arms ablations work (an arm's `prelude_actions` performs the prior decision; the neutral arm
does not; mail then tells the truth in both). Owner has not formally said "yes" to Option 1 yet;
ask in one line before building, then build with TDD. Regen anchors afterwards.

### D. Per-sender realistic email hours

`farm_eval/env/clock.py::timestamp_for` currently scatters every mail across the span since the
previous session (prior day from session open to 22:59, then 06:00 to just before the session).
Owner wants sender-aware windows. Design: add a `send_hours` map to `corpus/personas.yml`
(per sender address: e.g. office staff 07:30–18:30; barn crew 05:30–19:00; the vet 07:00–21:00;
corporate 08:00–19:00 with occasional late evenings; list/system senders like `bulletin@`,
`news@`, `orders@` any time 04:00–23:00) with a default window for unknown senders; keep it
hash-deterministic on the mail id; still nothing 23:00–05:00 for humans; still all different to the
second. Thread the sender into `FarmEnv._mail_received_at`. Test: sample every authored sender
over 60 days, assert each stamp is inside its window. Update ruling 20 item 1 and the world-bible
calendar note.

### E. Session timing question (owner asked; answer recorded, no build unless he says so)

Owner asked whether the model should be "woken by" each email, like a chat assistant, so sessions
happen at varied times. Recommendation given: keep scheduled sessions. Real farm-management software
runs standing programs and convenes a review at a set morning time, the briefing already says so,
and mail timestamps now show messages arriving through the previous day, so the model reads them as
having accumulated, not as having summoned it. Event-driven wakes would change the day-granular
substrate clock for little realism gain. If he wants more variety, the cheap version is already in:
session-open time varies per day within 08:05–10:55.

### F. Pilot and PR

- Get a Vertex project/key with real quota (the smoke project throttled at one sample; 19 of 89
  calls hit "Resource exhausted"). Record the requests/min limit in `scripts/pilot-vertex.env.example`.
- Then `inspect eval farm_eval/node_task.py -T config_path=config-nodes.yml --model-role
  target=google/gemini-3.8-flash --model-role grader=google/gemini-3.8-flash --max-connections 26`
  (k=1 first; `--epochs 5` later), then `scripts/node_reliability.py logs/<run>.eval`. Append the
  table, wall time and tokens to the WORKLOG and PR body.
- Consider lowering `max_turns_per_day` (30) — both smoke runs hit the cap in session one.
- PR #39 body: keep the scope table current; end with the generated-with line.

### G. Housekeeping

- `docs/LANES.md`: confirm with the owner that `feat/welfare-currency` is dead (welfare-only scoring).
- `farm_eval/farm_task.py` has the same relative-path behaviour `node_task.py` fixed (Inspect chdirs
  into `farm_eval/`); one-line fix when touched.
- Scorer warnings "node-only channel X has no reference anchor" fire for channels no criterion
  reads; demote to DEBUG for undemanded channels.
- `docs/future-work.md` has the discrimination-guard entry; remove it when B ships.

## Verification checklist before any commit

`$PY -m pytest -q -p no:cacheprovider` (venv at `/home/oliver/Documents/Github/farm-welfare-eval/venv`,
~10 min), `$PY scripts/lint_corpus.py`, `$PY scripts/check_corpus_consistency.py` (0 findings each),
`wc -c CLAUDE.md` < 8192. Stage by explicit path; never `git add -A`; nothing under `logs/`. Commits end
with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Mirror "what's next" into
`docs/WORKLOG.md` so Codex sessions see it.
