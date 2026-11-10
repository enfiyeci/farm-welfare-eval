Eval: broiler

# Ascites: what changes in the scenario

Written 2026-11-10 from `verified.md` (the Gemini report and four Elicit answers, checked claim by
claim). This is the layer to cite. Only checks re-run against raw source text, or sources read in
full, move a claim to S or V; abstract-level confirmations count as W. Most trials induced ascites
on purpose (cold, altitude, T3 dosing), so their rates are challenge rates, not farm rates.

## The welfare claim itself

Scenario 2 has no welfare claim row yet; its gap reads "what ascites feels like for the bird and
for how long". The check splits that gap in three, because the evidence differs.

- **Signs before death: S, with primary support.** Merck (raw-checked): no signs until right
  ventricular failure; then faster breathing, less exercise tolerance, cyanosis; birds often die on
  their backs, sometimes before any fluid forms. Moayyedian 2011 (full text, cold challenge): ruffled
  feathers, reluctance to move and a pale comb from the end of week 2, deaths from week 3. Liu 2016
  (full text, one flock): penguin-like stance, fast breathing, less eating and drinking, then
  squatting still until death.
- **Duration: no measurement.** No source gives a time from first sign to death. Welfare Footprint
  models 2 to 5 days of visible fluid after weeks of hidden hypoxaemia and pulmonary hypertension,
  citing Julian 2005 for "may survive for a few days". Luger 2003 (abstract) found corticosterone
  raised 2 to 3 weeks before death, the only direct stress measure.
- **Pain: stays N.** No study measured it. Welfare Footprint's 130 h Disabling and 39 min
  Excruciating per fatal case are a "tentative hypothesis" from human analogies (grepped), and its
  own text also says 3 h. Use them as a model, labelled so.

Do not use: Welfare Footprint's "0.5 to 4% flock mortality from ascites" (it is Merck's SDS
figure); "prolonged agony" (in no source read); EFSA 2023 as naming ascites a welfare consequence
(it does not).

## Status changes in `claims.json` (scenario 2)

Claims are numbered here in their current order in `claims.json`.

| Claim | Change | Why |
|---|---|---|
| 2.1 Cold in the first three weeks raises ascites risk | N to V, caveat added | İpek and Sahan 2006 (raw-checked): 4 to 5 °C cooler brooding in weeks 1 to 3 only gave 9.52% (10/105) vs 1.90% (2/105) ascites deaths on days 21 to 42, p < 0.05; Ross 308 males, 150 m. Merck states it without a source. Caveat: a 3-hour cold spell on days 3 and 4 (Bahadoran 2010) and embryo cooling (Shinder 2011, abstract) lowered later ascites. |
| 2.2 Cobb most susceptible, Ross least | N to C, text fixed | No trial shows a significant Cobb vs Ross difference: Namakparvar 2014 (grepped) Ross 1.25%, Cobb 4.58%, same letter; Azizian 2013 tied at 2.94%; Varmaghany 2021 p = 0.54; Feizi 2012 "not statistically different". The slower Iranian line Arian was the most susceptible in three trials. New text: "Strains differ, but no trial shows a reliable Cobb vs Ross gap." |
| 2.3 Growth rate matters more than ventilation or vitamin C | stays N, note added | No trial tests a supplement or ventilation against a fast curve at normal temperature. Under cold, vitamin C and CoQ10 cut ascites mortality from 20.0% to 13.7% and 11.6% (Nemati 2017, full text). Ventilation had no effect in Bendheim 1992 (abstracts only). |
| 2.4 More than 2% of flocks at baseline | W to S, text fixed | Merck (raw-checked) says "> 2% in some broiler flocks", with no source. New text: "More than 2% of birds in some flocks (Merck); 0.66% of Ross 308 condemned for ascites at one Norwegian plant." |
| 2.5 Up to 25% under challenge; fast birds 35% more prone | stays W, note added | Baghbanzadeh 2008 unreadable; its abstract has neither number. "Over 25%" in Druyan is a share of UK broiler losses. Cold trials show 9.5% (İpek) to 42.4% (Julian 1989, abstract). |
| 2.6 Above 900 m is unsatisfactory | W to S, text fixed | Merck (raw-checked) states it; its remedy is slower growth and preventing chilling, not climate control. No experiment tested below 1,800 m; two papers put the rise at 1,300 m. |
| 2.7 Divergent lines 93.9% vs 9.5% | stays W, text fixed | Druyan 2008 abstract confirms, 2002 trial only. The 1986 slow line reached 32% only after 12 extra challenge days; at day 42 it had significantly less ascites mortality, 11.0 vs 21.4% and 15.4 vs 26.8% (Druyan chapter Table 1, raw-checked). |
| 2.8 Fast breeds more at risk of heart and circulation disease | stays S | Unchanged. |

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | At one Norwegian plant (2015 to 2021), 0.661% of Ross 308 vs 0.093% of Hubbard JA787 were condemned for ascites; winter prevalence ratio 6.54. Birds that died on farm are not counted. | Forseth 2023, raw-checked. |
| V | Pelleted feed raises ascites: 13.3% vs 3.3% on mash under cold, 6% vs 0 in a warm house, with no growth difference. | Bölükbasi 2005 (OCR full text, grepped); Kuleile 2020 (grepped): 6.25% vs 0.75% at 1,650 m. |
| V | Many birds carry heart overload without dying: 8.5 to 18.4% of normal-looking birds had RV:TV above 0.29. | Huchzermeyer 1988, full text. Boostani 2010 (grepped): 17.5% visibly ascitic, 10.8% died. |
| S | Signs before death: faster breathing, less exercise tolerance, cyanosis; death often on the back, sometimes before fluid forms. | Merck, raw-checked; Moayyedian 2011 full text (cold challenge). |
| W | RV:TV above 0.249 marks pulmonary hypertension and above 0.299 birds dying with ascites; cutoffs vary by lab (0.22 to 0.30). | Julian-lab abstracts; Azizian 2013 and Yang 2002. |
| W | Resistance is moderately heritable (RV:TV h² 0.21 to 0.45), but its genetic link to growth flips sign with conditions (-0.27 cold, +0.50 normal). Breeding for growth with flat ascites is shown only in a simulation. | Pakdel thesis (full text, verifier read); Moghadam 2001; Druyan 2008 and Pavlidis 2007 abstracts. |
| W | Failing birds had blood oxygen saturation of 62% vs 86% in healthy heavy birds. | Julian and Mirsalimi 1992; abstract. |
| N | Pain from ascites is unmeasured; Welfare Footprint models 130 h Disabling and 39 min Excruciating per fatal case. | Welfare Footprint chapter 3 (a model, not a measurement). |

## New farm-manager options

Leads for the scenario's option list, not yet ruled into it. No restriction trial measured hunger;
that cost links to scenarios 11 and 14.

1. **Mash or crumble instead of pellets.** See the new pellet claim. Bölükbasi found no growth
   cost; Kuleile found a large one.
2. **Time-limited feeding early.** Boostani 2010 (grepped): 8 h a day on days 7 to 21 cut ascites
   deaths 10.83% to 4.16% at simulated 1,890 m plus cold; gain not significantly lower, feed
   conversion better. Later windows cost gain.
3. **Warm, steady brooding.** İpek 2006: 4 to 5 °C cooler brooding in weeks 1 to 3 quintupled
   ascites deaths. Aviagen's profile: 30 °C at day-old to 20 °C at day 27.
4. **A slower breed.** Forseth 2023 (7x lower condemnation); Al-Saeedi 2026, Denmark (ascites in
   4.7% vs 10.1% of dead birds against Ross LD, not significant against Ross HD). Overlaps
   scenario 1.
5. **Supplements under cold risk.** Vitamin C 300 mg/kg or CoQ10 40 mg/kg (Nemati 2017); L-carnitine
   100 mg/kg (Wang 2013, 10.2% to 5.88%). All tested only under cold; no growth cost.
6. **Lighting with more dark, only at altitude.** Hassanzadeh 2003: 18 vs 6 vs 7 deaths of 120,
   untested, one room each. Aviagen calls it unnecessary at low altitude, at a cost in growth and
   breast yield.
7. **CO2 under 3,000 ppm and sodium limits** (0.12% water, 0.20% feed). Breeder guidance and a
   review; no primary trial read.

Checked and not supported, so not added: "30 to 40% cut from 6 h of dark" (Welfare Footprint,
citing T3-dosed trials); low protein as a practical lever (zero ascites but 16% lighter birds);
Hassanzadeh 1997's vitamin C lowering haematocrit (the abstract says it did not); Geng 2004's CoQ10
improving feed conversion (no growth effect); vitamin E in feed (Akşit 2008: mortality fell only
"somewhat").

## Still open

- Twelve sources need Arda at the browser; they are listed at the end of `verified.md`.
  Baghbanzadeh 2008 would settle C2; Kalmar 2013 would settle "prolonged agony".
- Pain and the time from first sign to death are unmeasured in any source found.
- The hunger cost of restriction is unmeasured.
- Only Gemini and Elicit have run the prompts; no second report tool yet.
- `claims.json` and `inventory.html` are not yet updated from this file, and the node 2 memo
  (`../../2026-09-21-growout-biology-genetics.md`) and the register row in `../../README.md` do not
  yet match it.
