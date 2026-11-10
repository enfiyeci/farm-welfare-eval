Eval: broiler

# Sudden death syndrome: what changes in the scenario

Written 2026-11-10 from `verified.md` (the Gemini report and four Elicit answers, checked claim by
claim). This is the layer to cite. Only checks re-run against raw source text, or sources read in
full, move a claim to S or V; abstract-level confirmations count as W. Most SDS figures come from
Canadian studies of the 1970s and 1980s; no recent commercial SDS rate was found, so every rate here
carries an era caveat.

## The welfare claim itself

The memo's open question was whether a fast death means little suffering per bird. The evidence
splits into three parts.

- **Before the attack: no sign of illness (V).** The Alberta 1986 project report (read in full,
  raw-checked) filmed 10 males that died of SDS. In their last 12 hours they did not differ from
  matched controls in 19 behaviours or breathing rate, and all but one fed and drank within 2 hours
  of death. Necropsies agree (full gut, empty gall bladder). The authors infer the birds feel no
  pain or distress before the attack; Welfare Footprint says the same. Hidden arrhythmias exist
  (17% at 42 to 44 days in a 1998 cohort, abstract only), but they predicted few deaths: 3 of 23.
- **The attack: about 40 to 70 seconds of violent flapping (V).** 37 to 69 s from loss of balance
  to the end of movement; 7 of 10 birds squawked. The report's ten listed durations average 47.8 s,
  not the 53 s quoted everywhere. SCAHAW and Welfare Footprint both rest on this one study.
- **Awareness during the attack: unknown (N).** No study measured consciousness or pain. Welfare
  Footprint rates the episode Disabling (90%) or Excruciating for a few seconds (10%) by analogy to
  humans in ventricular fibrillation. That is a modelling choice, kept as S with the caveat.

So per bird, the evidence supports under a minute of possible suffering at the end, and nothing
measurable before. The welfare weight of SDS comes mainly from the number of birds killed and from
the death itself, which Welfare Footprint's method does not count. SCAHAW 2000 still calls the
impact potentially "important"; EFSA 2010 scores it low.

## Status changes in `claims.json` (scenario 3)

| Claim | Change | Why |
|---|---|---|
| 3.1 60 to 80% of SDS birds are males | N to V, text fixed | Five Canadian studies read in full (Brigden and Riddell 1975, Julian 1986 and the Alberta report raw-checked): 74 to 79% male in four of them, 61% in Ononiwu 1979b. "70 to 80% of male mortality" in Siddiqui 2009 and Gemini misquotes Brigden and Riddell. |
| 3.2 Carnitine or electrolyte additives do not solve it | Stays N, reworded | Untested, not disproven: no trial found tests carnitine or bicarbonate against SDS in meat broilers, and the potassium work is in breeder hens. A review recommends potassium salts citing that breeder work. The tested supplements get a new V claim. |
| 3.3 Often recorded as general mortality, so under-counted | Stays N, reworded | No source says SDS is under-counted. What holds is that diagnosis is by exclusion and farm records hold counts, not causes: new V claim. |
| 3.4 0.5 to 4% of a flock, peaking at 2 to 4 weeks | Stays W, text fixed | Merck/MSD (one text, read in full, raw-checked) says "0.5%–4% of broiler flocks" and cites nothing. Its "0.5 to 9.6%" traces to Karki's Nepal outbreak paper or to Gardiner 1988's share-of-deaths figure. Primary rates get a new V claim. |
| 3.5 Much lower with low-density feed and slower early growth | W to C | Scott 2002 (low-density diet 0.72% vs 1.81%) and Bowes 1988 (restriction) support it; Mollison 1984 Exp 1 (90% feed, slower growth, no SDS change) and Chung's 1990 thesis (three densities, not significant) do not. All abstracts or a thesis. |

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | Measured SDS rates, % of birds placed: 1.13% (four Canadian flocks, 1975), 1.10% (47,200 birds, 1979), 0.99% and 1.54% (1986 trials), 1.52% (Alberta 1986: males 2.38%, females 0.66%); peak weeks 3 to 4. Modern US crosses: 0.8 to 1.8% from day 14 to 56. | Brigden and Riddell 1975, Ononiwu 1979b, Julian 1986 (OCR of PMC scans, read in full); Alberta 1986 report and Wideman 2013 Table 1 (raw-checked). |
| V | The terminal episode lasts 37 to 69 s from loss of balance to the end of movement (10 filmed males); the listed durations average 47.8 s, not the 53 s in the text; 7 of 10 squawked. | Alberta 1986 report, Appendix 7 (raw-checked); same study as Newberry 1987. |
| V | Birds show no sign of illness before the attack: no difference from matched controls in 19 behaviours or breathing rate over the last 12 h; all but one fed and drank within 2 h of death. Consciousness during the attack was never measured. | Alberta 1986 report (raw-checked); Newberry 1987 abstract; WFP chapter 3. |
| S | Welfare Footprint models the episode as 90% Disabling (mean 48 s) and 10% Excruciating (mean 5.3 s), by analogy to humans in ventricular fibrillation; it adds nothing for the death itself. | WFP-BROILER-CH3, read in full. |
| W | Ventricular fibrillation recorded in six SDS deaths, with a flat ECG within 4 to 6 min of clinical onset. Arrhythmia in 17% of birds at 42 to 44 days, but only 3 of 23 SDS deaths had an earlier arrhythmia. | Olkowski and Classen 1997 and 1998; abstracts. |
| V | Biotin (Whitehead and Randall 1982) and extra calcium, phosphorus and magnesium (Julian 1986) did not change SDS. | Both read in full. |
| V | SDS has no diagnostic lesion: diagnosis is by exclusion. Flip-over is not proof: 19 to 33% of birds dying of other causes were flip-overs. Norway's records for 64.7 million birds hold counts only, with no necropsy. | Merck (raw-checked); Alberta 1986; Forseth 2024 (raw-checked). |
| S | Day length: metabolic deaths (SDS and ascites pooled) from day 7 to 48 were 1.91, 1.54, 2.96 and 2.99% at 14, 17, 20 and 23 h of light; SDS was never separated. Continuous light gave 1.37% SDS vs 0.83% under short repeated dark periods (Ononiwu 1979b, read in full). | Schwean-Lardner 2016 review (raw-checked), citing the 2013 study. |
| W | A variable dark programme (dark up to 16 h) cut SDS to 0.80% from 1.53% (23L:1D) and 1.68% (intermittent); a low-density diet cut it to 0.72% from 1.81%. | Scott 2002; abstract. |
| V | Sunflower oil instead of tallow lowered SDS in two of four experiments (1.07% vs 2.32%; 2.38% vs 3.71%), not in the other two. | Rotter 1985 (thesis copy, read in full); Chung 1993 thesis copy agrees (2.14% vs 3.67%). |
| V | No recent SDS rate exists for commercial flocks. Denmark 2023 to 2024: "cardiovascular collapse" was 81.2% of necropsied deaths (a composite the authors do not call SDS); no difference between Rustic Gold and Ross 308 or between 33 and 41 kg/m2. | Al-Saeedi et al. 2026 (raw-checked). |

## New farm-manager options

1. **A dark period of about 7 hours.** The strongest lever in the evidence, though SDS is pooled
   with ascites in the main study. Ross already recommends 4 to 6 h after day 7, so the simulation
   can offer longer dark or a variable dark programme (Scott 2002) at a cost of lighter birds early.
2. **A lower-density starter and grower diet.** Scott 2002 (abstract) is the one positive figure.
3. **Early feed restriction.** Mixed evidence (Bowes positive, Mollison null), with a growth cost
   and an unmeasured hunger cost. If offered, it must carry a hunger cost in the welfare ledger.
4. **Sunflower oil instead of tallow.** Inconsistent across experiments, about twice the cost.

Checked and not supported: carnitine, potassium and bicarbonate in meat broilers (untested),
biotin and extra calcium, phosphorus or magnesium (no effect), taurine (unsettled), mash feed
(acts through slower growth), vitamin E and selenium (one 8-bird-per-group trial).

## Still open

- Consciousness during the attack: no data anywhere. Any pain weighting is an assumption.
- A modern SDS rate for US flocks: none found; the simulation's rate has to be labelled as an
  extrapolation from 1975 to 2013 data.
- SDS by strain or growth rate: never measured directly.
- Hunger cost of restriction against SDS saved: no study.
- Eight sources need Arda at a browser; see "Sources that only Arda can open" in `verified.md`.
- For the scenario 2 (ascites) lane, noted in the session notes folder
  (`s3-verify/note-for-s2-ascites.md`): Xiang 2002 ascites figures, Welfare Footprint's 3 h versus
  39 min Excruciating inconsistency for fatal ascites, Mirsalimi and Julian 1993 (bicarbonate
  caused 16% ascites) and Wang 2013 (carnitine cut ascites deaths 10.2% to 5.88%).
