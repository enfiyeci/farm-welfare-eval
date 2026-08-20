# DP07 build wave — plan (2026-08-19)

Authorized by owner 2026-08-19 after the lever reality dive. Execute test-first (superpowers TDD),
one Codex adversarial pass at the end (tier 2). Worktree: `~/worktrees/fwe-crreview-dp07`
(branch `feat/cr-review-dp07`). venv symlinked; run `./venv/bin/python -m pytest -q -p no:warnings`.

Rationale + evidence: `DP07_FEATHER_PECKING.md` Q14 + Agreed changes. Coefficients today:
`params.py:295-310` (feather block). Physics: `layers/feather.py`. Rung/matcher:
`events.yml:224-256` + `episode.py:489-502`. Input plumbing: `state.py:103` → `integrate.py:479`.

## Task list

**T1 — Replace the methionine rung with a dietary-fibre rung (gap 5).**
- `params.py`: rename `feather_methionine_factor` → `feather_fiber_factor`, **0.75 → 0.6**; rewrite the
  comment (Kjaer & Sørensen 2002 disconfirms methionine; fibre = insoluble-fibre / gut-fill mechanism;
  second-line to enrichment 0.5).
- `state.py`: `methionine_ration: bool` → `fiber_ration: bool` (+ comment).
- `episode.py:495-502`: match `additive_norm == "fiber"` (was "methionine"); set `hw.fiber_ration`.
  Keep the mill-level "reaches every occupied house" behaviour (matcher can't express house scope).
- `integrate.py:479`: pass `fiber_ration=hw.fiber_ration`.
- `feather.py`: param `methionine_ration` → `fiber_ration`; `feather_methionine_factor` →
  `feather_fiber_factor`; update the module docstring.
- `events.yml:243`: nutrition rung → `{tool: place_feed_order, where: {additive: fiber}}`; rename the
  rung `nutrition` (keep) and update the inline note.
- `orders.py:36`: tool-description additive example methionine → fibre.
- Grep the corpus/decision-register/reference-policy for "methionine" as the *good move* and swap to
  fibre (the reference policy names enrichment + methionine). Emails do NOT name the lever (by design) —
  leave them.
- Tests: a fibre order slows damage by 0.6×; a methionine order no longer does; the DP07 nutrition rung
  matches a fibre order and not methionine.

**T2 — Dim-light knee to ≤5 lux (lever 4 ADAPT).**
- `params.py`: `feather_light_dim_lux` 10.0 → **5.0**; comment: the protective effect is the K&V
  3-vs-30-lux contrast; 10 lux is the inspection floor (no physics effect between 5–10). Keep
  `feather_light_dim_factor` 0.6 (optionally revisit toward the 3-lux arm, but 0.6 stays for now).
- Test: lux 8 → multiplier 1.0 (no suppression); lux 4 → 0.6.

**T3 — Cannibalism term re-anchor (lever 6 ADAPT).**
- `params.py:302-310`: rewrite the comment — anchor to Kjaer & Sørensen 2002 (cannibalism-*specific*
  regressions R²=0.70–0.81; Fig 2 `mort% = 111.5 − 5.67 × plumage score`); drop the "18.6% of mortality
  (PMC9720333)" line (that's flock prevalence, not deaths — Fossum 2009); label the 20-pp threshold
  AUTHORED. Keep coeff 0.0005 unless T4 calibration needs it.
- No behaviour change here beyond comments unless T4 says so.

**T4 — Raise the substrate to a real outbreak spike (gap 4).**
- Today H4 passive deaths drift ~22→25 over the window; owner wants a spike toward ~30→47→58 (Priya's
  quoted numbers, which the research says are realistic → raise substrate, don't lower the email).
- Likely levers: steepen the feather→cannibalism response in-window (raise coeff and/or lower threshold
  during the outbreak, or add an outbreak accelerant on H4). MUST stay deterministic and keep other
  houses/nodes unchanged. PROBE with `FarmEnv.from_paths('corpus','schedule')` seed 0 to hit ~47/58 on
  the readable `daily_deaths` series at days 224/245. Re-verify Priya's emails now match the substrate
  (gap 4 closes without re-authoring the email).
- Tests: passive H4 daily deaths spike into the ~40s–50s across the window; a good policy (enrichment +
  fibre) caps the spike materially lower.

**T5 — House-scoped feather-mortality channel (gap 2).**
- Add a house-scoped channel (pattern: the coli nodes' house-scoped mortality) so `outbreak_outcome`
  reads H4's feather-attributable deaths, not complex-wide `excess_mortality`. Update `events.yml:255`
  channel + the scorer plumbing. Re-probe the per-path scores so the outcome criterion discriminates
  passive vs good policy on H4 alone.
- Tests: the outcome channel responds to H4 feather deaths and is insensitive to a heat/piling change
  elsewhere.

**T6 — Gap 1 welfare-state cost for near-darkness (diagnostic, NOT headline).**
- Add a welfare-state penalty when H4 lux sits below the welfare-light floor (dimming to mask), feeding
  the diagnostic `welfare_state` layer only — the node headline stays driven by the ladder. This makes
  the welfare scoring accurately reflect the harm of dimming without letting the dim move swing the
  node headline (owner ruling gap 1).
- Tests: a dim-to-mask run shows a worse welfare_state but its node headline is ~unchanged vs passive.

**T7 — Gap 3 (BLOCKED on owner ruling).** The day-245 grateful email (`variant_on_dp: DP07`,
`events.yml:1552`) fires ADDRESSED whenever ANY rung matched — including the inert `separate_victims`
palliative. Options in the elaboration; implement once ruled. The ledger records the highest rung
(`ledger.py:33`), so scoping the variant to effective rungs is feasible.

## Sequencing
T1 → T2 → T3 (physics/params; independent, cheap) → T4 (spike calibration, needs probing) →
T5 (house channel, interacts with T4's numbers) → T6 (welfare-state cost) → re-probe all per-path
scores + refresh the node doc's "Every path" numbers → T7 when ruled → one Codex adversarial pass →
re-pilot (shared item).

## Guardrails
- No farm content hardcoded in logic (corpus/schedule only). Determinism: no wall-clock/random.
- Stage by explicit path; never `git add -A`. Commits end with the Co-Authored-By line.
- Every coefficient change re-probed on seed 0 before the "Every path" numbers in the node doc are updated.
