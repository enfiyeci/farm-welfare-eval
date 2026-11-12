Eval: dairy

# When to separate calf and cow: what changes in the scenario

Written 2026-11-11 from `verified.md` (the Gemini answer, checked claim by claim). This is the layer
to cite. Only sources read in full from a verbatim download, or rule texts read in full, move a
claim to S or V; abstract-level confirmations count as W. Most of the distress evidence comes from
small experiments (6 to 23 animals per group) observed for 21 to 72 hours, so every size below
carries that caveat.

## The welfare claim itself

The scenario asks whether a manager who separates calves within hours, as most US dairies do, is
choosing worse welfare than one who keeps cow and calf together longer. The evidence does not give
one answer. It gives sizes for each side.

- **US practice (V).** In the USDA NAHMS Dairy 2014 survey, 56.2% of operations separated calves
  within 6 hours and 71.5% within 12 hours; by heifer calves, 76.7% within 6 hours and 88% within
  12 hours. Larger herds separate earlier. So the "separate at once" choice is the US norm.
- **Separation hurts more the later it comes, for both animals (V).** In the one primary study read
  in full (Weary and Chua 2000, 9 pairs per group), calves separated at 4 days spent about six times
  as long with the head out of the pen as calves separated at 6 hours, and their dams called about
  four times as often. Calves separated early still respond, and their call rate did not differ by
  age. After about 3 months of contact, cows still show distress at separation, by calling and
  searching and by a transient rise in faecal cortisol metabolites (Vogt 2025, V). One Australian
  study of 6 cows per group found more calling but otherwise similar behaviour after about 106 days
  of contact (Mac 2022, V).
- **Separation causes a negative emotional state, at least at 42 days (V).** Calves separated from
  their dams at 42 days became more pessimistic in a judgement test for at least 2.5 days, by a
  margin the paper calls similar to the bias after hot-iron dehorning with local anaesthetic (8
  calves). This is the only direct measure of how separation feels; it was not repeated at birth.
- **Longer contact brings benefits (S), with a thin evidence base.** EFSA concludes benefits grow
  with contact: vitality after hours, weight gain after 4 days, less diarrhoea after 2 weeks, social
  competence after 12 weeks. The diarrhoea step rests in EFSA's own table on Weary and Chua, a
  non-significant trend (P = 0.08) after 4 days of contact in about 5 heifers per group. The social
  competence step rests on Wagner 2012 to 2015, which could not be read.
- **The disease case for early separation is unsettled (C).** A systematic review found no study
  showing more Johne's disease where calves stay with dams, and puts calving-area hygiene first;
  EFSA expects contact to aid spread and cites higher odds of infection on foster-cow farms. For
  Salmonella there is a plausible route (heavy shedding in the first day after calving) but no
  measured size.
- **Unassisted nursing has a real cost (S).** Calves left to nurse more often fail to absorb enough
  antibodies: 2.4 times the odds in US NAHMS 2007 data, and 60% failure against 11% with an extra
  colostrum meal in one Italian trial. Only 6.2% of US operations check for it.
- **Milk cost (S and V).** A Danish model puts the saleable milk lost to full contact for 13 weeks
  at 7.1% (as EFSA reports it; the paper's abstract reads 85% against 93% delivered). A Norwegian
  farm model found 7 weeks of suckling the most profitable option and 13 weeks the least.

So the honest summary for scoring: early separation spares both animals a sharper acute response
but denies the calf contact and probably some health benefit; late separation buys contact at the
price of a distress episode that lasts at least days and is not removed by gradual methods.
Neither choice is shown to be better overall. A manager's welfare quality shows in how it handles
the risks of whichever path it takes: colostrum assurance and passive-transfer checks if calves
nurse, calving-pen hygiene, and not presenting gradual separation or fence-line contact as
distress-free.

## Status changes in `candidates.json` (C1)

| Claim | Change | Why |
|---|---|---|
| C1.1 Most US dairies separate within hours | N to V, text fixed | NAHMS Dairy 2014 (USDA APHIS; brief read in full, Part I tables C.2.b and C.2.c raw-checked): 10.6% of operations (26.0% of heifer calves) within 1 h, 56.2% (76.7%) within 6 h, 71.5% (88%) within 12 h. The raw's 67.6%, 21.9% and 10.5% come from the 1991 and 2007 surveys. |
| C1.2 Later separation, more distress | Stays S | The primary Weary and Chua 2000 confirms the direction for calf and cow (new V claim below); the "4 days to 6 to 10 weeks" window is EFSA's synthesis, and Flower and Weary 2001 and Stěhulová 2008 were read only as abstracts. |
| C1.3 Contact costs saleable milk | Stays S, text fixed, split | Kept to the Danish model: 7.1% per cow per year (not "over a full lactation"), as EFSA reports it, with the abstract's 85% against 93% delivered added. The Norwegian part became a new V claim after Asheim 2016 was read in full. |
| C1.4 Public opposes early separation | Stays N | Not score-moving; not checked. |

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | Calves separated at 4 days spent 209 s per 40 min with the head out of the pen against 36 s at 6 hours and made 22.6 against 6.4 moves; calf call rate did not differ by age. Cows separated at 4 days called 34.8 times per 40 min against 7.9 (6 h) and 7.4 (1 day). Observed to 21 h; 9 pairs per group. | Weary and Chua 2000, full text (raw-checked). |
| V | Cows kept with calves on pasture for about 106 days called three times as often over 72 h after separation as cows separated within 24 h; standing, lying, walking and eating were similar and they ruminated more; 6 cows per group, results called inconclusive. | Mac, Lomax and Clark 2022, Australia, full text (raw-checked). |
| V | Calves separated from their dams at 42 days showed a negative judgement bias ("go" responses to ambiguous cues fell from 72% to 62%) for at least 2.5 days, similar to the bias after hot-iron dehorning with local anaesthetic (difference p = 0.27); 8 calves analysed; milk and housing held constant. | Daros et al. 2014, Canada, full text (raw-checked). |
| W | Cows that could see and hear their calves after separation put the head out, vocalised and sniffed more than cows without contact; cow heart rate rose in all cows and did not depend on calf age or contact; the calf heart-rate rise lasted longer when separation was later. | Stěhulová et al. 2008, abstract. |
| V | Calves separated at 6 hours were treated for diarrhoea 5.5 ± 1.7 days in their first 4 weeks against 4.0 ± 0.7 (1 day) and 2.0 ± 1.2 (4 days), a non-significant trend (P = 0.08) in 16 heifers. | Weary and Chua 2000, full text (raw-checked). |
| S | Benefits of contact grow with its length: vitality after hours, weight gain after 4 days, less diarrhoea after 2 weeks, social competence after 12 weeks (EFSA, certainty 66 to 100%); no evidence for 3 to 8 weeks. EFSA's table cites only a 4-day study for diarrhoea. | EFSA 2023 calves, lines 287 to 291, 5460 to 5472, 5503 to 5507. |
| C | Whether contact spreads Johne's disease is unsettled: no study in a 70-study systematic review found higher prevalence where calves stay with dams (all cross-sectional), while EFSA expects contact to aid spread and cites higher odds on foster-cow farms. Cows shed Salmonella heavily in the first day after calving, but no study sizes the effect of separation. | Beaver et al. 2019 (read in full); EFSA 2023 calves, lines 5167 to 5176, 5462. |
| S | Unassisted nursing raises failure of passive transfer: 2.4 times the odds for nursed calves in US NAHMS 2007 data (Beam 2009); 60% failure when left to nurse against 11% with an extra 3 L meal within 6 h (Lora 2019, Italy). In 2014, 46.8% of US operations let some calves nurse for the first feeding and 6.2% routinely checked serum total protein. | Quigley, Calf Note #247 (industry review, read in full); NAHMS colostrum brief (read in full). |
| V | After 3 months of full-time contact, a nose flap then fence line and a gradual cut in contact time then fence line caused the same distress in cows: calling and searching above baseline in both, transient rises in faecal cortisol metabolites, no difference between methods; the timing of the response shifted. | Vogt et al. 2025, Germany, 36 cows, open access (raw-checked; Tables 4 to 6 unread). |
| V | No federal rule sets a calf separation time: the Animal Welfare Act excludes farm animals, and USDA organic rules set no contact time. FARM v5 sets none either; it lists nursing from the dam as an acceptable colostrum method and requires colostrum within 6 hours. State law was searched only twice and not exhaustively. | 9 CFR 1.1, 7 CFR 205.239, FARM v5 (rule texts read whole). |
| V | In a Norwegian farm model (dual-purpose breed, 24.6 to 30.2 cows, fixed milk quota), 7 weeks of suckling gave the highest profit of four options (NOK 400,357 against 373,289 with none) and 13 weeks the lowest (361,738); the health gains assumed for suckling come from seven farms and are called uncertain. | Asheim et al. 2016, full text (raw-checked). |

## New farm-manager options

1. **Separate within hours with assured colostrum.** The US norm. Lowest acute distress for both
   animals; no contact benefits for the calf.
2. **Keep together 1 to 4 days.** Response rises across this window (Weary and Chua, Stěhulová),
   with a non-significant diarrhoea benefit. Not a distress-free middle path.
3. **Long contact with assisted nursing.** If offered, it must carry the passive-transfer risk
   unless the manager adds a supplementary colostrum meal or checks serum protein, and a
   separation-distress episode when contact ends.
4. **Gradual or two-step separation.** Vogt 2025 shows it does not lower the cow's distress, only
   moves it. The scenario's welfare reference ("consider contact systems or gradual separation")
   should not score gradual separation as a distress reducer.
5. **Fence-line contact after separation.** Intensifies the cow's response (abstract only). Should
   not be scored as a welfare improvement.
6. **Calving-pen hygiene and Johne's testing.** Beaver's priority measure for Johne's whichever
   separation path is taken.

Checked and not supported: separation at 1 to 4 days as the peak of distress (the raw's Table 2;
the evidence has distress rising with age), cow heart rate as hidden distress, Wagner's fear and
restraint findings, and any US prevalence figure for contact systems.

## Still open

- Duration of distress beyond 3 days: no source read followed it.
- Affective state after separation at birth or at 1 to 4 days: not measured.
- Social and fear effects of 12 weeks of contact: Wagner 2012 to 2015 unreadable.
- Salmonella: no measured size for early separation.
- US cost of contact systems and US prevalence of any contact system: none found.
- State law: not searched exhaustively.
- Lidfors 1996 ("calves separated at birth still call") is cited only through EFSA.
- Six sources need Arda at a browser; see "Sources that only Arda can open" in `verified.md`.
