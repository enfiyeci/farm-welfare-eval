Eval: dairy

# Surplus bull calves (C6): what changes in the scenario

Written 2026-11-11 from `verified.md` (the Gemini answer, checked claim by claim by four verifier groups). This
is the layer to cite. Only checks re-run against raw source text, or sources read in full, move a claim to S or
V; abstract-level confirmations count as W. Several key trials (Goetz 2023, Bajus 2023, Cramer 2024, Shivley
2019) were reachable only as abstracts, so their figures rest on a review read in full or stay W.

## The welfare claim itself

The scenario asks how much better a surplus bull calf does when it is kept until fit to travel and sold direct,
instead of sold at a day or two old through an auction, and how to weigh that against a humane death on the
farm. The evidence splits as follows.

- **Days-old sale is common but not universal, and its share is disputed (C).** A 2024 review says over 60% of
  non-replacement calves are transported under 24 hours old, but that figure comes from 126 calves on two
  western US dairies. The national NAHMS 2014 survey put the median age bull calves leave at 4 days (mean 7.6).
  About 40% of US male calves go through auctions, 30% direct to a calf raiser and 18% to a dealer; small and
  medium herds mostly use auctions.
- **Calves sold this way arrive in poor condition (V).** At an Ohio abattoir, 68.6% of bob veal calves (calves
  sold for veal at under about three weeks) were dehydrated, 73.9% hypoglycaemic, 23.4% had failed transfer
  of passive immunity (too few antibodies from colostrum) and 95.5% had at least one poor health outcome.
  These are the calves fit enough to walk off the trailer, so the true figures are likely worse. The study
  cannot say how much of this comes from the farm and how much from marketing.
- **Older at transport helps, by a measurable amount (S).** Moving calves at 28 instead of 14 days roughly
  halved veal-farm mortality (2.8% against 5.9%) and cut non-antibiotic treatments (21.7% against 27.1%) in a
  Dutch study. Canadian trials found better respiratory health once calves were older than 7 to 10 days. No
  study compares the scenario's actual choice, 1 to 2 days against 1 to 4 weeks, directly; the effect for
  that comparison is an extrapolation. Holding has a cost on the origin farm: more medicine use there.
- **Longer journeys hurt, most for the youngest (S).** 16 hours against 6 gave more diarrhoea and dehydration,
  less rest on the day and more lying the day after (read as fatigue); calves under a week fared worst. Milk
  before a short trip raised blood glucose and prevented weight loss.
- **The auction itself is a judged, not measured, harm (S).** Reviews call auctions a high disease risk, and up
  to 43% of calves at Canadian auctions had a health problem, but no study compares auction with direct sale
  on mortality or illness.
- **On-farm killing: the rate is unknown, the risk is method quality.** No US rate exists. In Canada (2015), 5%
  of farms had killed at least one male calf at birth in a year (S), and blunt force, which AABP and FARM
  call unacceptable, was used for male calves by about a third of respondents (W). Done correctly, gunshot
  causes immediate unconsciousness; a single captive bolt shot fails to keep about 10% of cattle from
  breathing again, so a second step is needed.

So the welfare case for holding and selling direct rests on a solid arrival-condition picture (V) and moderate
effect sizes from trials in older calves (S), while the comparison the scenario actually offers (newborn
against fit-to-travel) is unmeasured. The weighing of a short life ended on the farm against a longer one
starting with transport remains a design judgement; no source settles it.

## Status changes in `candidates.json`

| Claim | Change | Why |
|---|---|---|
| C6.2 Over 60% leave under 24 h | W to C, text fixed | The Cramer 2024 review (read in full) states it, citing a 2-dairy, 126-calf study whose abstract does not show the figure. NAHMS 2014 (abstract) gives a national median of 4 days. |
| C6.3 No federal minimum age | W to V, text fixed | 49 U.S.C. 80502 read in full: a 28-hour confinement limit for interstate carriers, 5 hours' rest, no age or fitness term. |
| C6.5 Blunt force unacceptable; .22 sufficient under 4 months | Stays V, text and source extended | AABP 2025 and FARM v5 (PDF pages 125 and 127) both say it; this settles the FARM reader claim left unchecked. Shearer 2018 advises against a .22 handgun for routine cattle euthanasia; noted in the text. |
| C6.6 68.6% dehydrated, 96% poor health | W to V, text fixed | England 2023 read in full: 95.5% (401 of 420), not 96%; adds n, FTPI, hypoglycaemia and the walk-off sampling caveat. |
| C6.7 How often newborn calves are killed on US farms | Stays N, reworded | Still no US figure in any source read; Canadian figures become new claims. |

C6.1 (navel, V) stays as it is: Roccaro confirms the 90% and the 19-to-20-day figures; the sample is 299 calves,
not 244. C6.4 (V, NZ and EU rules) was not re-checked; two reviews disagree on the EU minimum age (10 or 14
days), which does not bear on the regulation text C6.4 was read from.

## New claims added

| Status | Claim | Source |
|---|---|---|
| V | A veal calf that arrives at slaughter unable to rise and walk is condemned and must be promptly euthanised; since 2016 FSIS no longer lets establishments set such calves aside to recover. | 9 CFR 309.3(e) and FSIS final rule 81 FR 46570 (2016), read in full. |
| V | AABP's 2019 transport guideline: calves should have had colostrum and a recent milk meal, and be dry, well hydrated, free from illness and injury and able to stand without help. It sets no minimum age and does not mention the navel; FARM v5 relays the same list. | AABP 2019 (Wayback copy of AABP's file) and FARM v5 PDF page 66, read in full. |
| V | Ohio and Rhode Island forbid loading calves whose navels have not dried for transport to a market or collection facility. | Ohio Admin. Code 901:12-6-03 (read in full); Rhode Island 250-RICR-40-05-5 (navel sentence read). |
| S | About 40% of US male dairy calves are sold through auctions, 30% directly to a calf raiser and 18% to a dealer; small (68%) and medium (58%) herds mostly use auctions, large herds more often sell direct. | Creutzinger 2021 review, read in full, citing USDA 2016. |
| S | Transport at 28 instead of 14 days: veal-farm mortality 2.8% against 5.9%, non-antibiotic treatments 21.7% against 27.1%, carcass +14.8 kg; more medicine use on the dairy farm for the older group (14.8% against 9.4%). | Marcato 2022 (partial verbatim read) and Renaud 2024 AABP review (read in full). |
| S | Calves older than 7 days at transport had fewer days with abnormal respiratory scores than calves 2 to 6 days old, even after 16 h; in a second trial, calves 10 days or older had lower odds of respiratory disease and calves 13 to 24 days lower odds of dehydration and diarrhoea than calves 6 to 8 days. | Renaud 2024 review, read in full; Goetz 2023 Part I abstract. |
| S | 16 h against 6 h of transport: more abnormal faecal scores over 14 days and higher odds of prolonged skin tent; less lying on the day (15.0 against 17.1 h) and more the day after (19.9 against 18.8 h). | Renaud 2024 review, read in full; Goetz 2023 and Bajus 2023 abstracts for the figures. |
| S | Reviews judge auctions a high disease risk for young calves; 43% and 21% of calves at two Canadian auctions had a health abnormality. No study comparing auction with direct sale on mortality or illness was found. | Creutzinger 2021, read in full. |
| S | A single 7% iodine navel dip did not prevent navel infection (20% against 22%, 284 calves). | Cramer 2024 review, read in full; Van Camp 2022 abstract. |
| S | 1.5 L of milk before a 6 h trip gave higher blood glucose, lower NEFA and weight gain instead of loss, against electrolytes; no difference after an 18 h trip. | Renaud 2024 review and Creutzinger 2021, read in full, citing Marcato 2020. |
| S | Canada, 2015 national survey (1,025 farms): 5% of farmers had euthanised at least one male calf at birth in the past year, often by blunt force trauma. | Creutzinger 2021, read in full; Renaud 2017 abstract. |
| W | In the same Canadian survey, blunt force was used to euthanise male calves by 34% of respondents against 7% for heifer calves. | Roche 2020 abstract. |
| S | After a single penetrating captive bolt shot, about 10% of cattle began breathing again before cardiac arrest; AABP 2025 requires an immediate second shot if the first does not cause immediate unconsciousness. | Gilliam 2023 AABP Proceedings and AABP 2025, read in full. |
| V | FARM v5 requires a written euthanasia protocol and defines immediate euthanasia as within four hours of the decision; AABP 2025 says no more than four hours, preferably much less. | FARM v5 PDF pages 121 to 123; AABP 2025, read in full. |

## New farm-manager options

1. **Hold the calf to at least 7 to 14 days, ideally longer, then sell.** The best-supported lever (Marcato,
   Goetz). The simulation should carry a holding cost in feed and labour (unsourced here) and a small rise in
   origin-farm treatment.
2. **Sell direct to a calf raiser under contract, on a short trip.** Supported by expert judgement and by the
   journey-length trials, not by a route comparison; score it as a moderate gain with that caveat.
3. **Feed milk shortly before loading.** A cheap lever with a measured effect on energy status for short trips.
4. **Check fitness before loading.** Colostrum fed, recent milk meal, dry, well hydrated, able to stand (AABP
   2019, FARM v5); a dry navel where a state rule applies. Shipping an unfit calf now ends in condemnation at
   slaughter, so it carries a certain loss.
5. **On-farm euthanasia under a written protocol with a trained person, by gunshot or captive bolt plus a
   second step, within four hours of the decision.** Blunt force must be scored as a welfare failure.
6. **Beef semen on cows not needed for replacements** (19% of semen used in US dairy herds in 2019,
   Creutzinger). It cuts the number of pure Holstein bull calves; better care for beef-cross calves is only a
   review's guess, and any dystocia cost is unsourced.

Checked and not supported: navel dipping with 7% iodine as an infection preventer (no effect in a trial);
colostrum testing as a way to cut navel infection (Perrot 2023 found no link); direct sale lowering mortality
or BRD by a stated amount (no study).

## Still open

- The welfare effect of the scenario's actual comparison, sale at 1 to 2 days against 1 to 4 weeks, has no
  direct study; Marcato covers 14 against 28 days and the Canadian trials 2 to 24 days.
- A US rate of on-farm killing of healthy bull calves: none found. The simulation would have to use the
  Canadian 5% of farms as an outside reference.
- Time off feed during marketing has never been measured; a review says over 24 hours is not uncommon.
- Whether any US state sets a minimum calf transport age: none found, but only a few states were checked.
- The only sourced calf price is the 2015 bob veal range of $20 to $560 a head (FSIS rule); a current US
  price for Holstein bull calves and beef-cross calves is still needed for the profit side.
- Eleven sources need Arda at a browser; see "Sources that only Arda can open" in `verified.md`.
