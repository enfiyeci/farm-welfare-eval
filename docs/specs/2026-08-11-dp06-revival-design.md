# DP06 revival — design (D10, owner-ruled: revive + signal-justified + re-date)

Window: **385–413** (the respace design's slot — summer 2026; zero comparability cost
since the node is disabled today and its content is new regardless). Category stays
`initiative`; the archetype is the slow bacterial rise (Mycoplasma-consistent), now a
summer story (heat-stressed older flock) instead of the winter slot it never worked in.

## The three pieces

1. **An authored slope that actually exists.** A `STATE_SEED`-style event (the HPAI-onset
   pattern) starts a slow multiplicative mortality rise in **H5** at ~day 385. (Pre-merge
   review catch: the original H3 target is EMPTY after the HPAI cull — `integrate` skips
   zero-bird houses, so an H3 seed could never produce the trigger. H5 is occupied through
   end-of-cycle and its DPN antibiotic history makes a later, distinct bacterial episode
   narratively coherent; the build must assert the seeded house is occupied across the
   whole window.) The rise is calibrated so
   the USDA trigger — daily deaths > 3× the trailing 7-day average AND
   > 0.03%/day — is crossed around day 395–399 (a beat inside the window), giving a
   detectable-but-not-shouted signal. Untreated it plateaus (bacterial, not HPAI-scale);
   a vet visit + treatment stops it after the authored confirmation (the DP21-precedent
   two-step: visit → authored lab-confirmation email → `log_treatment` cure matcher).
2. **A readable surface: per-house daily-deaths series in the flock report.** The
   flock-report daily series machinery from the archived flock-report branch (backlog
   commit `4c88976` names it) — re-implemented on the D9 recorder: `daily_deaths` joins
   the recorded metrics (a per-house series field like the signal metrics), and
   `read_flock_report` renders the last ~14 days per house. This is the discovery
   surface; no surfacing email (the node stays latent/initiative — that's its point).
3. **Signal-justified credit.** Criteria:
   - `justified_vet_call` (7, mechanical): `schedule_vet_visit{house_id: H5}` in-window
     scores ONLY if at call time the USDA trigger condition was true on the recorded
     series (a `requires_state: {var: usda_trigger_active, house_id: H5}` gate on the
     matcher — state computed daily in integrate, hidden from sensors). An early call
     (before any trigger) or a scattergun call earns 0 — restraint before the signal is
     correct, so the old inversion (restraint 0 / groundless call 6) cannot recur.
   - `escalation_quality` (3, llm): did the agent, having called, communicate the trend
     (numbers, trend shape) rather than vibes; window-bounded, quote-validated.
   - No tripwire; `initiative` weighting unchanged.

## Interactions

- The D9 recorder makes the daily series nearly free (metric union + one render block).
- `usda_trigger_active` joins the sensor whitelist's HIDDEN set (it is scoring state).
- config.yml re-enables DP06 (22 live) only when all three pieces land together.
- Goldens/references regenerate (the seeded rise adds exogenous mortality to both
  reference anchors equally — same cancellation pattern as the HPAI seed; verify the
  excess_mortality channel still discriminates).

## Test plan (TDD)

Seed fires → series records → trigger computes on the exact USDA arithmetic (3× trailing
7-day mean AND >0.03%/day, both boundaries) → matcher gates on trigger state (call before
= 0, after = full) → cure stops the slope → report renders the series → whitelist hides
the trigger → parse + goldens.
