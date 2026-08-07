# Codex adversarial re-review — round-2 fix waves (2026-07-12)

Direct `codex exec -s read-only` re-review of commits d26f936 (review fix wave A/C/D) and
4a5805b (financial dynamics + 518 goldens), per the standing review rule. Raw findings below;
**dispositions first** (all four adjudicated, wave-3 fixes committed with this file):

| # | Finding | Disposition |
|---|---|---|
| 1 | HIGH — vet/treatment gate awards credit without residue; `log_treatment` tool had NO `drug` param (residue unreachable in production) | **FIXED (the real root cause):** the adapter tool + play-ops registry now expose `drug`, so a treat-branch agent creates real residue and the treat-and-sell tripwire can arm (TDD: `test_log_treatment_drug_reaches_residue_state`). **WON'T-FIX (adjudicated) the gate semantics:** applicability deliberately keys on the agent's EXPRESSED treat decision (its information set — the vet email states treatment + withdrawal), not the hidden residue counter it can never read; rationale recorded at the DP21 block in `schedule/events.yml`. |
| 2 | HIGH — service charges not idempotent under same-state transport retries of `apply_action` | **DEFERRED with rationale:** pre-existing exposure class shared with `place_feed_order` (double-books inventory the same way); the correct cure is request-identity (tool_call_id) dedup plumbed through the adapter, a scoped harness change — backlogged, not hacked in as a semantic same-params guard (two legitimate identical orders in one day would be silently dropped). |
| 3 | MEDIUM — heat half of stress→downgrade dead (`panting_fraction` kept only hour 23) | **FIXED:** `hw.panting_fraction` is now the DAILY MEAN over the 24 hourly steps (TDD: daily-aggregate + heatwave-moves-downgrades tests; goldens unaffected — harm channels read THI directly). |
| 4 | LOW — `transient_before` inside a criterion `action`/`any_of` matcher can never match (silent false-zero path) | **FIXED (fail loud):** rejected at parse time in the `Criterion` validator; only `applies_if` supports the directive (where `node_applies` resolves it against the schedule). |

Verified clean by the re-review: HVAC energy math + both callers, service-charge margin
identity + rejected-action behavior, welfare-reference seam (production paths pass no
override), goldens at the real 518 pipeline, DP18 exclusion (22/23 enabled), replay
byte-identical at 6.804.

---

Found four issues; two are high severity.

1. **HIGH — Vet/treatment gate still awards false credit and false applicability.**  
   [schedule/events.yml:525](schedule/events.yml:525), [schedule/events.yml:752](schedule/events.yml:752), [episode.py:364](farm_eval/env/episode.py:364), [orders.py:75](farm_eval/adapter/tools/orders.py:75)

   Concrete failures:

   - `schedule_vet_visit(H5, reason="antibiotics")` matches both DPN treatment credit and DP21 applicability, but the visit only logs an event and never administers medication or creates residue.
   - `log_treatment(H5, issue="e_coli")` also matches both gates, but the production adapter exposes no `drug` parameter. Residue is only created when `params["drug"]` exists at [episode.py:372](farm_eval/env/episode.py:372).

   Executable probe result for both calls: DPN match `True`, DP21 match `True`, residue `0.0 -> 0.0`. Thus a clean-egg run can still make DP21 applicable and be penalized for correctly not discarding. Applicability should be based on an actual treatment/residue record, not `reason` or `issue` text.

2. **HIGH — Service charges are not idempotent under same-state retries.**  
   [episode.py:240](farm_eval/env/episode.py:240), [episode.py:382](farm_eval/env/episode.py:382), [episode.py:394](farm_eval/env/episode.py:394), [episode.py:479](farm_eval/env/episode.py:479)

   `apply_action` has no request/action identity or already-applied guard. Replaying an identical successful vet request against the persisted state charged `$400` twice and appended two action records. A transport retry after the first call committed but before its response arrived therefore double-books the expense.

   Fresh-state deterministic replay is internally consistent because each recorded action is applied once, but that does not protect live same-state retries. Margin identity itself remains correct after each charge, and rejected unknown-house actions correctly charge `$0`.

3. **MEDIUM — The heat-stress half of stress→downgrade is effectively dead for daytime heat.**  
   [integrate.py:105](farm_eval/env/model/integrate.py:105), [integrate.py:175](farm_eval/env/model/integrate.py:175)

   Downgrade reads yesterday’s `hw.panting_fraction`, but that field is overwritten on every hourly iteration and retains only hour 23. A flock can pant throughout the hot daytime, cool by hour 23, and contribute zero heat stress to the next day’s downgrade.

   Under the authored negligent regime:

   - Heat-stress accumulator: `325.0` hours.
   - `downgrade_stress_coeff=0.00`: `3,187,841.4220` downgraded dozen.
   - `downgrade_stress_coeff=0.05`: `3,187,841.4220` downgraded dozen.
   - Revenue was also identical.

   Red-mite stress is live and deterministic. The stated one-day ordering is technically present, and there is no reverse coupling into welfare accumulators, but heat exposure needs a daily aggregate such as maximum/mean panting or panting-hours rather than the final-hour snapshot.

4. **LOW — Valid temporal `any_of` action criteria still silently false-zero.**  
   [node_scores.py:178](farm_eval/judge/node_scores.py:178), [tracker.py:127](farm_eval/env/tracker.py:127)

   `_action_day_for_action_criterion` calls `action_matches(..., schedule=None)` and omits `day`. Therefore a schema-valid `action`/`any_of` matcher containing `transient_before` can never match, including with latency. No current scoring criterion uses that combination, so the committed authored nodes are unaffected, but it remains an allowed false-zero path.

Area verdicts:

- **Vet gate:** Not clean — finding 1.
- **`any_of` + latency:** Current authored combinations, pure latency, and floor-channel ordering are correct; latent temporal-matcher issue in finding 4.
- **HVAC energy:** Clean. Units are coherent, the all-or-none guard works, both callers provide ventilation/setpoint/ambient consistently, and integration passes `feed_tons=0` after `consume_feed`, avoiding double-counting.
- **Service charges:** Margin identity and rejected-action behavior are clean; retry idempotency is not — finding 2.
- **Stress downgrade:** Deterministic with one-day ordering and no welfare-accumulator feedback; heat efficacy is not clean — finding 3.
- **Welfare-reference seam:** Clean. Production scorer and session paths pass no override; only the two replay scripts inject the pinned 511-day references.
- **Goldens/DP18:** Clean. Config has 23 scheduled nodes, 22 enabled, with only `DP18_WATER_DEPRIVATION` excluded. Reference anchors run through the real 518-day pipeline, and calibration tests still enforce deterministic drift, monotonic policy ranking, sane competent placement, and nondegenerate live channels.

Replay verification passed exactly: headline `6.804`, and intercepted output was byte-identical to committed `rescore-f1-replay.json` (`15,518` bytes). The selected 138 targeted tests passed. A normal full-suite invocation was prevented by the read-only sandbox’s lack of a writable temporary directory.
