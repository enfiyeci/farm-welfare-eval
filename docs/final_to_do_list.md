# final_to_do_list — the design-then-build ledger

**Owner process ruling (2026-08-11):** the next few sessions are **design-only**. We work
through the decision queue below; the owner rules; each ruling turns into concrete to-dos in
§2. Design changes to md files (the review pack, `docs/future-work.md`, specs, this file)
still land during the design sessions. Code and content changes do **not** — they accumulate
here and are implemented in **one big to-do run** (normal SDD discipline, one worktree per
lane) once the decision queue is cleared.

## 1. Decision queue (owner rulings pending)

Full basics + tradeoffs for each were presented in the 2026-08-11 adjudication session.
Statuses move to RULED as decisions land; the ruling's output moves to §2.

| # | Decision | Status |
|---|---|---|
| D1 | N24 build-readiness score 3 → 5 in the pack | PENDING |
| D2 | Confirm the score holds: DP16 trust 3, DP01 trust 7, DP21 trust 8 | PENDING |
| D3 | Pack Part 3 "Honesty to the public" trio in chronological order (DPN → DP21 → DP13 now; principle = follow final chronology) | PENDING |
| D4 | DP21 drugless-treatment residue arming: default unnamed-drug antibiotic treatment to amoxicillin 5-day withdrawal | PENDING |
| D5 | DP05 red mite: mite outcome channel alone, or channel + narrowed vet-reason list (and the accepted reasons) | PENDING |
| D6 | DP12 masking cure: house constraint / minimum-sustain exemption / disclosed-raise exemption / combination | PENDING |
| D7 | DP13 egg-test subsystem (`order_egg_test` driving the 21 CFR 118.6 track) — go/no-go, scoped to the one node | PENDING |
| D8 | DP19 recordkeeping/incident-log tool — go/no-go in principle (new tool surface) | PENDING |
| D9 | DPF grader ground-truth block (per-node objective-state handed to the grader) — go/no-go | PENDING |
| D10 | DP06 revival: go/no-go + does credit require a signal-justified call + re-date into the desert (~day 380–410) | PENDING |
| D11 | DP07 feather model mitigation inputs (enrichment/ration/lighting/density become live) — go/no-go | PENDING |
| D12 | DP08 molt physics (`feed_ration` → body condition/mortality) — go/no-go | PENDING |
| D13 | DP14 real depop event + method-argument matcher — go/no-go (AVMA-2026 refresh is already a standing to-do) | PENDING |
| D14 | DPN economics: NAE premium sales channel + seeded colibacillosis mortality — go/no-go | PENDING |
| D15 | DP15 depop-on-report world event — go/no-go (content pass) | PENDING |
| D16 | DP10 firming: contractor reply re-offering the cheaper crew, or a second grader criterion | PENDING |
| D17 | DP13 Anita email de-advocacy rewrite (content pass) — yes/no | PENDING |
| D18 | Respace-pass menu scope: which of options B/C/D/E enter as intended (A + entry itself RULED IN 2026-08-11; see `docs/future-work.md` §Respace) | PENDING |
| D19 | Concurrent-open-windows covariate (respace option F): pull forward as a standalone task now, or into the big run | PENDING |
| D20 | Fact question: does the laptop hold unpushed commits? | PENDING |

## 2. To-dos for the big implementation run

### Standing (already ruled or recorded — no further decision needed)
- [ ] AVMA 2026 Guidelines: read Chapter 6 (Poultry) properly, then refresh DP14's citation +
  tier vocabulary (`docs/future-work.md` §Refresh DP14's AVMA citation).
- [ ] DP21 rubric re-base on US residue law (task_15bf7c81 — owner started it; fold in if
  unfinished at big-run time).
- [ ] Re-run the irregular-spacing audit with **open-windows-per-day** as the metric, not
  surfacing-events-per-beat (root cause of the cluster miss; eval-awareness backlog).
- [ ] Respace core move A: re-date DP13 off the verified 21 CFR 118.5 testing calendar
  (verify the CFR first — desert ~365–385 vs 40–45-wk ~161–196), with the full re-dating
  sweep (emails, world bible, pack, goldens) in the content pass.

### From rulings (accumulates as §1 decisions land)
- (empty — populate as rulings arrive)

## 3. Owned by other lanes (tracked there, not here)
- DP20 staffing curve + fatigue — staffing redesign lane (handoff 2026-08-07, P11 build plan).
- DP18 four-piece cure — queued content pass; coordinate with `feat/stocking-density`
  (H6 placement event lives there).
- `fix/judge-multiset-tier` — pair-approved, merges after the round-4 wave.
