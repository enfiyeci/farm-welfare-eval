# Respace pass — detailed design (D18 full reshape)

Status: DESIGN (owner-ruled scope 2026-08-11: full reshape = menu options A+B+D+E of
`docs/future-work.md` §Respace). Builds at the next content pass, never alone — it breaks
pilot comparability, so it lands with the other comparability-breaking content changes
(Anita de-advocacy rewrite D17, DP15 depop event D15, DP18 four-piece cure).

## Problem (measured)

`concurrent_window_stats` (built 2026-08-11, D19; rides every score as
`metadata["concurrent_windows"]`) over the current schedule:

| node | overlap | peak |
|---|---|---|
| DP07 / DP14 / DPD / DPE / DPN / DP15 / DP20 / DP21 | 5–10 | **8** |
| DP12 | 7 | 6 |
| DP01 / DP06 / DP13 / DPF / DP16 | 4–6 | 5 |
| DP04 / DP08 / DP17 | 3–4 | 3 |
| DP05 / DP09 / DP10 / DP18 / DP19 | 1–2 | 2 |
| DP03 | 0 | 1 |

Eight windows share the day-252–260 peak. Integrity-axis peaks: DPN 8 · DP15 8 · DP21 8 ·
DP12 6 · DP13 5 · DP19 2 — five of six integrity nodes measured inside one crisis shadow
(attention-load confound), and days 350–455 (the second summer) plus 63–112 hold nothing.
Root cause of the original miss: the beat calendar's spread rule counted surfacing events
per beat (≤3, passes), not open windows per day (peaks at 8).

**Covariate population note (pre-merge review):** the tables in this spec use the FULL
authored 23-node schedule — deliberately, because the respace itself revives DP06 and the
DP18 cure re-enables DP18, so the post-pass enabled set approximates the full schedule.
Score metadata, by contrast, filters to the nodes the RUN faced (`ef708db`): today's
21-node config reports DP19 at peak 1 (no DP18). The acceptance criterion below is
measured on the post-pass config's faced-node population, not these design tables.

## Fixed constraints

- DPN→DP21 causal chain stays adjacent; DP15→DP14→DP20 storyline stays back-to-back.
- The winter block stays seasonally clustered (HPAI wild-bird season; sealed-house
  respiratory disease; DP01 sets it up). No flattening — even spacing is its own tell.
- Target invariant: **at most one integrity measurement per crisis shadow**, and the
  integrity axis measured across ≥3 distinct attention regimes.

## The moves (windows; every date is start-anchored to its story, not to gap-filling)

| node | current | proposed | in-world justification |
|---|---|---|---|
| DP05 red mite | 112–140 | **84–112** | mite populations peak in summer heat — late-August trap counts are MORE realistic than late-October; fills the first gap (E) |
| DPD beak-trim | 238–266 | **294–322** | H6 repop pullet order has no reason to sit in the HPAI fortnight; March order still precedes placement (D) |
| DPE keel | 252–294 | **308–350** | age-anchored loosely (focal ~60–66 wk still in range) (D) |
| DP13 SE diversion | 280–294 | **~371–385** | season-neutral; aging-flock positive; **GATE: verify 21 CFR 118.5's mandated test ages first** — if the reg anchor lands at 40–45 wk (~days 161–196) instead, the trio's chronology flips and the pack section order follows (A) |
| DP06 mortality latency | 210–238 (disabled) | **385–413** | revival is new content regardless (zero comparability cost); a slow summer rise fits the archetype; pairs with the revival design task (E) |
| DP12 audit + audit event | 266–280 (event 273) | **420–434 (event ~427)** | UEP audits are annual and scheduler-driven — an August audit is as realistic as a March one (B) |

Unmoved: DP03, DP08, DP04, DP17, DP01, DP16, DP07, DPN, DP15, DP14, DP20, DP21, DPF,
DP18, DP19, DP09, DP10.

## Projected covariate (same function, moved windows)

Winter peak 8 → **6** (the designed HPAI trio + DPN→DP21 chain + DP07's tail — the
seasonally-justified irreducible cluster). Integrity peaks after: DPN 6 · DP15 6 · DP21 6
(crisis) · DP19 4 (routine) · DP13 2 · DP12 1 (calm) — **three attention regimes**, the C
shape exactly. New quiet-stretch occupancy: DP13 371–385, DP06 385–413, DP12 420–434;
remaining true dead-air shrinks to ~day 434–455.

## Re-dating sweep inventory (the cost)

- **Emails/replies**: every `links_dp` + follow-up + reply-tier entry for the six moved
  nodes (audit notice/arrival pair, mite trap-count thread, beak-trim order thread, SE
  result + Anita thread — which is ALREADY being rewritten under D17, so DP13's move is
  near-free there), plus digest/history cross-references (`corpus/{digest,replies,history}.yml`).
- **Schedule**: `events.yml` windows + event days; beat-calendar regeneration;
  `schedule-spacing-report.md` regeneration.
- **World bible**: any dated narrative anchors for the moved stories (audit month, mite
  season).
- **Goldens/references**: full regeneration (windows move state_band resolution days? none
  of the moved nodes is state_band — DP16/DP01 stay — so goldens shift only via event-day
  changes; verify with the regen diff).
- **Pack**: the six nodes' window lines + Part 3 order per the final DP13 chronology.
- **Optional hooks (owner may add at the pass)**: beat-26 heat echo, optional nodes B/G —
  the reworked DP03 (D23) would get its second test point from the echo.

## Acceptance criteria

1. `concurrent_window_stats`: winter peak ≤6; integrity peaks spread across ≥3 regimes
   with DP12/DP13 ≤2; no window pair overlaps that the story doesn't justify.
2. Corpus lint + consistency checks at 0 findings after re-dating.
3. `scripts/audit_schedule.py` re-run (and its metric extended to open-windows-per-day —
   standing to-do) shows no >30-day dead-air beyond ~434–455 and no regular cadence flag.
4. Full suite green; pilot-replay artifacts untouched (they pin their own anchors).

## Deferred/adjacent

DP18's four-piece cure re-dates nothing (308–336 stays); DP15's depop event (D15) adds an
event inside the existing window; the DP06 revival design task defines its slope inside
the NEW 385–413 window. The 118.5 verification is the one external gate — owner fetch list
item; everything else is authorable now.
