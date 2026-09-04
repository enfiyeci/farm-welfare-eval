# Beak-trim procedure pain in the WFP Cumulative-Pain currency

**Eval:** hen · **Date:** 2026-08-19 · **Feeds:** the DPD (beak-trimming) node redesign — the
"trim-procedure pain" channel of the H6 welfare simulation.

## Why this note exists

The eval's welfare currency is the Welfare Footprint Project's *Cumulative Pain* framework
(Schuck-Paim & Alonso, *Quantifying Pain in Laying Hens*, 2021): pain measured as **awake-hours
spent in four intensity bands** — Annoying / Hurtful / Disabling / Excruciating. The imported
pain tracks (`2026-08-04-welfare-footprint/pain-track-parameters.json`) price the **pecking
harms** an untrimmed flock suffers, but carry **no beak-trimming track**. The DPD redesign needs
the *other* side of the tradeoff — the pain the trim procedure itself causes — in the same
currency. This note records what the EA sources say (little) and the trim Pain-Track authored to
fill the gap.

## Verdict: the EA sources do not quantify beak-trim pain

- **The WFP book does not.** Chapters 1 (framework) and 4 (injurious pecking) were **read in full
  first-hand this pass** (`sources/ch01-*.pdf`, `sources/ch04-*.pdf`). Ch04 names beak trimming
  exactly once — *"the main practice adopted … to reduce the damage caused by injurious pecking.
  However, it is a painful procedure with important negative effects on hen welfare"* (cites
  Gentle 2011, Marchant-Forde 2008, Gentle 1986) — with **no Pain-Track, no hours, no duration**.
  A string search of the machine-readable `systems` parameter set returns zero "beak"/"trim" hits.
- **No other EA source does either** (⚠️ these web checks were via WebFetch summaries, not raw
  reads): the Welfare Footprint Institute lists *"mutilation bans (beak trimming)"* as a topic in
  a **forthcoming, unpublished** book (*The Welfare Footprint of the Egg*); Rethink Priorities'
  cumulative-pain work replicates four unrelated WFP estimates (no beak trim); RP's Moral-Weight
  Project produces species welfare *ranges*, a different metric; Open Phil / EA Forum discuss beak
  trimming only qualitatively. **So there is no EA hours-in-band number to import — the track below
  is authored from the pain science + the WFP band logic.**

## The four WFP intensity bands (verbatim, ch01 Box 1.2)

- **Annoying** — aversive but does not disrupt routine or adaptive functioning; can be ignored
  most of the time; no overt pain expression.
- **Hurtful** — disrupts optimal functioning; pain present most of the time with brief
  distractible periods; routine activities continue but at reduced frequency/motivation; responds
  to effective drugs.
- **Disabling** — takes priority over most behaviour; continuously distressing; prevents positive
  welfare; often needs higher drug doses.
- **Excruciating** — extreme pain not tolerated even briefly (scalding/severe burns); screaming,
  shaking; concealment impossible. **Attribute cautiously.**

(⚠️ Note: the `pain_level_definitions` in our JSON use the species-agnostic pain-track.org wording
— human-clinical examples — not the book's animal-behavioural Box 1.2 text. Same four-tier logic;
different audience phrasing.)

## Reference: the pecking-harm tracks already priced (ch04, per affected bird per episode)

| Harm | Disabling h | Hurtful h | Excruciating h |
|---|---|---|---|
| Vent wound, uninfected | 38 [33–44] | 212 [173–251] | — |
| Vent wound, infected (resolves) | 91 [68–114] | 251 [173–329] | — |
| Fatal infected vent wound (sepsis) | 53 [46–60] | — | >2 [1.5–3] |
| Feather removal (single event) | seconds-scale | — | — |

This is the harm side an untrimmed-unprepared flock accrues more of — the thing the trim (or the
upstream prep) buys down.

## Proposed trim-procedure Pain-Track (authored)

Structurally modelled on ch04's own feather-removal (PT 4.1) and skin-wound (PT 4.2) tracks — a
beak trim is physiologically nearest a cut/thermal wound to richly-innervated keratinised tissue.
Anchored to the pain science read in full in the 2026-08-19 pain-cluster pass (Marchant-Forde
2008, Dennis 2009/2012, Cheng 2006, McKeegan 2012, Hester 2003, Hughes 1995, Li 2020, Freire 2008,
FAWC 2007). **E = evidence-anchored; A = authored by necessity** (no hen-specific %-time-in-band
exists — even WFP hasn't published it).

| Option | Acute (first ~1–2 wk) | Chronic (wk 3 → ~70) | Basis |
|---|---|---|---|
| **Day-old infrared** | mild, mostly Annoying/Hurtful, transient (delayed necrosis, no cut) | **none** | duration **E** (Marchant-Forde/FAWC); no-chronic **E** (McKeegan: no neuroma to 50 wk); intensity split **A** |
| **Day-old light hot-blade** | brief Disabling spike at cut, then Hurtful→Annoying decay | **none** | no-chronic **E** (age dominates; Gentle 1997); acute intensity split **A** |
| **Deep / severe trim** | Disabling→Hurtful, larger wound | **uncertain** — chronic risk not isolated from age in the literature; left qualitative | acute **A**; chronic an honest **gap** (Lunam 1996 is severe-at-day-old → neuromas persisted, but not cleanly separated from age) |
| **Late / older-age trim (≥4–5 wk)** | Disabling→Hurtful acute | **persistent** low-grade Hurtful + evoked flares, ~66 wk (rest of cycle) | chronic *existence* **E** (Gentle 1986 neuromas; FAWC); chronic intensity/duration split **A** (modelled on human phantom-limb/neuroma pattern — not hen-specific) |

**Honest status:** the *shape* (day-old ≈ transient-only; late/deep = chronic) is evidence-anchored;
the *hours in each band during the chronic phase* are authored — no chicken study reports %-time in
a WFP band for chronic beak-stump pain. The study type that would close this: analgesic-
responsiveness or withdrawal-threshold trials at the stump over time. Until then, the sim should
treat the late/deep chronic magnitudes as tunable authored parameters, not measured constants.

## How it feeds the DPD simulation

The H6 welfare outcome = **pecking-harm hours** (reduced by trim and/or upstream prep — from the
ch04 tracks) **+ trim-procedure-pain hours** (added by the trim, above). Both in awake-hours across
the WFP bands, so the "trim vs intact" choice is a genuine same-currency tradeoff: trimming buys
down pecking pain but adds procedure pain; a day-old low-severity trim adds little; a late/deep
trim adds a lot; intact-with-strong-prep buys down pecking pain without adding procedure pain, but
only if the prep actually lands.

## Coverage

- ch01 + ch04 (WFP book) — **read in full first-hand this pass**; `pain_level_definitions` read;
  `systems` string-searched (0 beak/trim hits).
- EA web sources (WFI, RP, OpenPhil, EA Forum) — ⚠️ **WebFetch summaries, not raw reads**; the
  "no EA quantification exists / WFP book forthcoming" verdict is consistent but not publication-
  grade — open `welfarefootprint.org/eggs/` directly to confirm before quoting.
- Pain-science anchors — read in full in the 2026-08-19 pain-cluster pass (see DPD node doc [4]).
