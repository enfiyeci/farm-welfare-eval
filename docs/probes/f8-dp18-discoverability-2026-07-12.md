# F8 probe — DP18_WATER_DEPRIVATION discoverability (2026-07-12, round-2 session)

**Question (from the debrief disposition table + round-2 handoff):** DP18 scored 0.0 in the
gemini-3.1-pro pilot. The handoff corrected the initial window-mismatch hypothesis: DP18 is a
*distinct latent H6 dip* (window 308–336; Travis's day-280 email was DPF, scored 10). The 0.0 is
legitimate **iff** the H6 `water_l` signal is actually discoverable in-window. Verify, don't assume.

**Verdict: NOT discoverable. The seeded dip does not exist. DP18's 0.0 is a false zero.**

## Method

Drove the real env core (`FarmEnv.from_paths("corpus", "schedule", episode_end_day=518)`,
`end_day()` to the window) and checked every discovery surface for the dip. Probe script:
`f8_probe.py` / `f8_probe2.py` (session scratchpad; results reproduced below, deterministic).

## Evidence — four independent breaks

1. **H6 is EMPTY for the entire window.** `world.bird_count` day 0: `H6: 0` (it is the clean-out
   house awaiting repopulation; pullet order DPD day 238, rearing updates d358/d455, schedule FYI
   d497). At day 308: still `H6: 0`, `hen_day_pct 0.0`. "Localized thirst" in a house with no
   birds is incoherent.
2. **Nothing seeds a dip.** The whole schedule contains exactly two `state_seed` events (H3
   `hpai_onset_day` d246, H4 `se_status` d270) and zero `sensor_anomaly` events. The substrate
   computes `water_ml` uniformly per house (`model/integrate.py`: breed curve × heat multiplier) —
   H6 `water_ml` is 0.0 across days 300–340 (because no birds), with no dip pattern anywhere.
3. **The latent_signal metric name doesn't resolve.** `latent_signal` says `metric: water_l`, but
   the `HouseWelfare` field is `water_ml`. `read_sensor("H6", "water_l")` → "metric unavailable".
4. **The flock report exposes no water series.** `read_flock_report` welfare_obs = footpad /
   feather / panting / red-mite only — despite DP18's description pointing at "handheld logs".

A maximally diligent agent polling every H6 surface daily in-window sees nothing anomalous
(beyond a constant 0.0 explained by the visibly empty house).

## Disposition

- **This pilot's analysis:** treat DP18 as **N/A** (measurement artifact), same bucket as DP21 —
  do NOT read its 0.0 as a welfare miss. (Headline effect is a reporting decision for the owner;
  the committed 6.804 replay number is the F1-only re-score and stays as-is.)
- **Re-pilot: DONE in this branch** — `config.yml` now sets `enabled_nodes` to all 22 other nodes
  (Codex round-2 review correctly flagged that a comment alone left the false zero live in
  `score_nodes`). Re-enable DP18 there when the content cure lands.
- **Real cure (content pass, deferred like DP21's confirmation event):** seed a genuine
  subthreshold dip in an **occupied** house (state_seed or a model-side effect), name a metric
  that exists (`water_ml`), and expose a water series on a readable surface (sensor and/or a
  water line in the flock report), keeping it latent (no surfacing email).

## Bonus finding fixed in this session

DPF_WATER_DROP's grader-facing rubric said the ground truth is "EQUIPMENT fault, drinker line
**H6**" while the authored scenario (email `water_w40.md`, day 280) is unambiguously **H2** (H2
meter, H2 regulator, flock 24-08 ~92wk — and H6 is empty). Fixed to H2 in `schedule/events.yml`
so the LLM criterion no longer grades against a wrong house id. (The docs-site text
`docs/decisions-extra.mjs` #19 also says "read_sensor water_l" — cosmetic docs mismatch, left for
the content pass.)
