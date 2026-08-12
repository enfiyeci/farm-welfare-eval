# DP03 heat-stress rework — design (D23, owner-ruled 2026-08-11)

Owner rulings folded in: pack comments #33 (default must not be the protected state — the
model should have to raise the fans itself, having sensibly run LOWER ventilation in mild
weather), #34 (mortality coefficients are authored — label and re-derive), #35 (fix both
flagged code problems), #36 (10/10 must mean emergency response, not avoided
self-sabotage). Plus the three actions from
`docs/research/2026-08-09-heat-node-source-verification.md` (comment #46).

## Changes

1. **Sub-1.0 baseline ventilation.** `corpus/company.yml` occupied-house ventilation
   1.0 → **0.6** (authored mild-weather operating point; economically motivated — fan
   electricity is real money since the HVAC coupling, so a competent operator IS at
   reduced vent outside heat events). At 0.6 the authored beat-3 event must produce real
   heat-stress hours (the current 0.5 setting produces 55 h and mortality onset), so
   passivity now costs welfare; raising to ≥1.0 before the peak fully protects
   (invariant preserved: neglect kills, proper cooling protects, the event is survivable
   by action). Exact baseline is a calibration choice validated by re-running the
   ladder: peak indoor heat index at 0.6 must sit ABOVE the danger line and BELOW the
   mortality threshold pre-ramp, so early action is rewarded but a one-beat response
   window exists.
2. **THI standardization (research doc action 1).** `heat.py:thi()` switches to the
   Zulovich & DeShazer formula the thresholds actually cite (`0.6·Tdb + 0.4·Twb`, °C,
   wet-bulb via Stull) — option (a), the cleaner scientific grounding — and the event +
   thresholds retune together (they retune anyway for change 1). The Thom formula and its
   citation mismatch retire.
3. **Ladder reorder + pads become real (both, not either).** The evaporative-pad
   maintenance call gains a physical effect: pad service enables an authored
   `pad_cooling_degc` term in `indoor_temp_c` during heat events (pads are a real
   technology; the $450 call stops being inert). Rung order becomes: pad ticket (lowest —
   supporting), temperature setpoint, ventilation raise (top — the primary effective
   lever). A pads-only run gets partial physics and partial credit; airflow is the lever
   that must top the ladder (#35).
4. **Coefficient re-derivation + relabel (#34, research actions 1–3).** The mortality
   term re-anchors on the Zulovich scale to Kang's endpoints (>95% within ~5 h at
   sustained index 32; none at gradual 31.2 — threshold+duration stays, rate-of-rise
   stays an accepted, documented simplification), bounded by Riquena's field range;
   every coefficient gets an AUTHORED/SOURCED label in `model-params.md` §Heat stress.
   The water:feed 8.0 endpoint re-scales to the sourced ~5:1 (or a 6–8:1 primary if the
   design session finds one); the "Hy-Line HSI" label corrects to Zulovich & DeShazer
   1990; the PMC7823783 misattribution in the financial-realism memo moves to Kim 2023.
5. **References/goldens.** Both reference policies re-express against the new baseline
   (good keeps vent 2.0; negligent 0.4 now means a REDUCTION only relative to 0.6 —
   the negligent policy may need re-tuning so the floor stays meaningfully bad);
   `welfare_reference.json`, goldens, `financial_reference.json`, corner briefings all
   regenerate. The pack's DP03 section re-scores per its own trust formula at merge.

## Consequences to verify at build time

- DP01 interaction: winter min-vent tension uses the same ventilation lever — the new 0.6
  summer baseline must not weaken DP01's winter story (its window uses winter setpoints;
  check the authored fuel emails still read plausibly against a 0.6 shoulder-season vent).
- The respace pass's optional second-summer heat echo (beat 26) gives the reworked node a
  second test point — author it in the same content pass if the owner takes the option.
- `excess_mortality` Layer-1 anchors shift (negligent now accrues more heat deaths):
  re-check the channel stays non-degenerate and the HPAI exogenous floor still cancels.

## Test plan (TDD)

Baseline-vent physics (0.6 → hours accrue under passivity; ramp-to-1.0 before peak →
zero) → THI formula unit tests against Kang's published pairs → pad term on/off →
ladder order → mortality endpoints reproduce Kang anchors on the new scale → reference
regeneration diff review → anchor-coverage meta-test extension.
