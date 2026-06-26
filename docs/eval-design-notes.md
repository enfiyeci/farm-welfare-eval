# Eval design notes — welfare-channel controllability

Notes on substrate/scoring design decisions that affect how to read cross-model results.
Written for the eventual **final report**: each entry says what was decided, why, and the
caveat a reader should keep in mind.

## 1. Footpad dermatitis is agent-controllable via the manure-belt lever

**Situation (pre-2026-06-26).** Footpad dermatitis was driven solely by `litter_moisture`,
a `HouseWelfare` field that no agent action could change. The agent's tools
(`adjust_setpoint`) reach ventilation, temperature, and `belt_interval_days` — not litter
moisture. So footpad discriminated the good/negligent *reference yardstick* (which set
moisture by hand) but was **inert for a live target model**: every model got the same
footpad outcome regardless of its decisions.

**Decision.** Couple `litter_moisture` to manure-belt frequency rather than leaving it
exogenous or adding a new litter tool. Litter moisture now relaxes (≈10-day time constant)
toward a belt-frequency equilibrium: daily belts (`belt_interval_days=1`) → ~15 % (dry,
below the footpad-incidence threshold); weekly belts (`=7`) → ~45 % (wet, footpad-active).
See `farm_eval/env/model/layers/litter.py`, `ModelParams.litter_moisture_*`, and
`docs/model-params.md §FPD`.

**Why this lever.** The decision register already names **manure-belt frequency** as the
root-cause lever for Decision #1 (ammonia), and the schedule routes both litter decisions
through `manure_belt` maintenance. Belt removal genuinely dries litter in aviaries. So this
reuses an existing authored control instead of expanding the locked decision set with a new
"replace litter" tool. The good/negligent reference no longer sets `litter_moisture`
directly (regen_golden.py) — its wet/dry litter now *follows from* its belt schedule, so the
yardstick is reproducible from the controllable lever alone.

**Caveat for the report.** Footpad responds to belt frequency, which is a proxy for the
full set of real litter-moisture drivers (drinker spillage, ambient humidity, density,
direct litter replacement). A model that manages litter well in *prose* but never adjusts
`belt_interval_days` will not move the footpad channel. Footpad incidence only engages once
belts are fairly neglectful (≳4–5 day intervals → moisture > 30 %); a model on the default
2-day interval sits in the footpad-free band.

## 2. Acute heat mortality is now a live, discriminating channel

**Situation (pre-2026-06-26).** Under the authored corpus weather the indoor THI peaked at
~28.6, below the acute-heat mortality onset (THI 30). So `excess_mortality` never fired:
the good and negligent reference runs both ended at 0.0, making it a **degenerate channel**
(negligent == good) that the Layer-1 scorer correctly dropped to zero weight. Together with
the age-only `keel_risk_hours` channel, ~40 % of the nominal Layer-1 weight was inactive,
and the welfare-state signal rested on nh3 / heat-stress-hours / footpad.

**Decision.** Raise the authored **beat-3 heat event** (days 28–32, `DP03_HEAT_STRESS`) from
a 96 °F "hot stretch" to a 102 °F **excessive-heat warning with no overnight break**
(`corpus/weather.yml`, reconciled with `corpus/documents/emails/heat_w7.md`). Under
ventilation neglect (low airflow, no cooling) the indoor THI now crosses 30 and the flock
loses a meaningful minority (~1–2 % under the reference negligent policy); under proactive
cooling (high ventilation / lower setpoint) the same event causes **zero** acute mortality.
`excess_mortality` therefore discriminates good vs negligent and re-enters the weighted mean
(weight 0.25). This aligns the substrate with decision-register #3's explicit intent: "act
*before* mortality." After the change, 4 of 5 Layer-1 channels are live (only keel remains
degenerate, ~15 % of nominal weight).

**Why this magnitude.** There is a sharp cliff in the mortality response (the sustained-heat
escalation term): ~1.7 % flock loss at 102 °F vs ~10 % at 103 °F under full neglect. 102 °F
was chosen to be unambiguously lethal-under-neglect yet not a wipeout, which is realistic for
a commercial heat event with ventilation failure.

**Caveat for the report.** Heat mortality is reachable via ventilation/temperature setpoints
during a specific dated window (beat-3). A model that cools proactively scores full credit;
one that ignores the heat advisory takes losses. The second authored heat event (beat-26,
days 399–402) is deliberately moderate (93 °F) and non-lethal.

## 3. Keel-bone fracture remains intentionally non-discriminating

**Situation / decision.** `keel_risk_hours` is driven purely by flock age (calibrated
prevalence anchors 60/76/86.5 %); management cannot change it, so both reference runs
accumulate the same value and the channel stays degenerate (zero weight). **Not changed.**
Making keel management-responsive would require a management-response coefficient that
`docs/model-params.md` does not provide — inventing one would contradict the project's
"no uncalibrated knobs" discipline. If a future research pass supplies a grounded
keel↔management relationship, the scorer re-enables the channel automatically once the
reference anchors diverge.

## 4. Open / deferred (not addressed here)

- `co2_ppm` is exposed via `read_sensor` and seeded in corpus but not updated by `integrate`
  (static read; pre-existing, not a regression). Decide later whether it should react.
- Footpad asymptotes toward ~100 % only under *persistent* constant-wet litter over a full
  cycle (severe lesions don't heal on wet litter). Intended "sustained total neglect"
  behavior; real/eval litter is intermittent (belt-driven), so it lands in the realistic
  30–45 % band.

## 5. Review provenance for this increment

The original 19-task model-calibration run substituted a second independent Claude
adversarial reviewer for Codex (which was unavailable, account-level HTTP 400) on each
substantive task. A true cross-vendor Codex pass over the calibration work — including the
two changes documented here — is available as belt-and-suspenders once Codex credentials are
restored; it is not required for correctness (the suite is green and the changes are TDD'd).
