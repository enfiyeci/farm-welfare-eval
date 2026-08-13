# Review-Pack Source Audit Ledger — 2026-08-13

## Scope and method

This is the claim inventory for the external agricultural, welfare, health, legal, and
market assertions in the three v8 review-pack parts. Repository-state descriptions,
authored scenario values, and model coefficients are not relabelled as external facts;
they are checked against the named project files in each pack section.

`Anchored` means the claim is supported by an official rule, primary study, or the
standard named in the pack. `Qualified` means the source supports a narrower setting,
proxy, or association. `Unresolved` means the pack deliberately does not use the claim
as a calibration until a better source exists. Yellow notices in the pack carry the
material corrections and unresolved points.

## Part 1 — Welfare nodes

| Node | External claim family | Disposition | Evidence / remaining limit |
|---|---|---|---|
| DP01 | Ammonia effects, exposure limits, manure-belt emissions | Qualified | Li 2020, Kristensen 2000, Wang 2022, Miles 2006, NIOSH, UEP, Liang 2005, and Liu 2020 support the stated effects/direction. The former Charles & Payne lesion attribution was removed; no low-concentration commercial-layer lesion threshold is claimed. |
| DP03 | Acute heat, panting, and mortality | Qualified | Kang 2020 supplies the acute threshold-duration experiment; Riquena 2019 supplies field context. The pack retains the documented Kang/index-scale mismatch and does not claim the authored coefficients are measured. |
| DP16 | Wet litter and footpad dermatitis | Qualified | Wu & Hocking, via the linked full-text review, supports the 30% moisture reference. Prevalence and belt-moisture response remain setting-specific or authored; the layer-flock null and in-flight litter calibration are disclosed. |
| DP17 | Cage-free space, litter, perch, feeder standards | Anchored | UEP 2024 supports the stated multi-tier space and resource minima. The prior 30% litter statement was corrected to the UEP 15% minimum; the farm's 41% figure is internal. |
| DPE | Keel damage, perch/ramp/nutrition protection | Qualified | Heerkens 2016 supports the 29/39/49-week anchors; the 65-week 92% point is an explicit extrapolation. Review evidence supports intervention direction, not this model's absent response effect. |
| DP04 | Calcium, shell, and bone trade-off | Qualified | The linked dietary-calcium study supports direction, but the project ration differential, cost, and delayed scenario effect are authored and currently inert in code. |
| DPD | Beak-treatment hierarchy and management alternatives | Qualified | RSPCA supports infrared over hot blade and reducing routine trimming. The exact rubric hierarchy and its effect in this farm are project research, not independently re-verified here. |

## Part 2 — Vigilance and health nodes

| Node | External claim family | Disposition | Evidence / remaining limit |
|---|---|---|---|
| DP05 | Red-mite treatment efficacy and US label status | Anchored | Thomas 2017 and the linked case report support efficacy; FDA/DailyMed establish the US northern-fowl-mite label. Poultry-red-mite use remains extralabel. |
| DP06 | Mortality warning thresholds and slow bacterial rise | Unresolved | Gonzales & Elbers and Secure Egg Supply support influenza-oriented alarms, not the node's 0.1%/day bacterial heuristic. The latter is visibly marked as unsourced; the cited acute diseases partly contradict the scenario archetype. |
| DP07 | Feather pecking prevention and damage-by-age anchors | Qualified | Schwarzer 2022 supports the severe-plumage-damage figures and RSPCA identifies management levers. The study population is non-trimmed German aviaries, not this farm. |
| DPF | Feed/water differential diagnosis | Qualified | Missouri Extension and Xin 2002 support monitoring and heat-associated increased water intake. Elbers & Gonzales bounds the claim: intake is not a validated disease-prediction clock. |
| DP22 | Smothering incidence, pile location, and triggers | Qualified | Barrett 2014 and Armstrong 2023 support incidence and pile/smother distinction; Gray 2020 and Animals 2024 support review-level location/trigger claims. The 328-bird magnitude and failed-light trigger are authored and explicitly marked as such. |
| DP10 | Catching practice and flock fragility | Qualified | UEP 2024 anchors humane-handling requirements; the keel-damage review supplies prevalence context. No direct quantified rough-catching injury source is used for a simulation calibration. |
| DP08 | Induced-molt welfare and feed-withdrawal ban | Anchored | AVMA and Certified Humane support the cited welfare conclusion and prohibition. The fictional operation's detailed compliant protocol and economics are internal. |
| DP09 | Extended-lay osteoporosis and shell-strength decline | Qualified | Webster supports osteoporosis outcomes; the Ma/Fu chain supports shell-strength decline, not a commercial grade-out rate. The unextractable primary-table issue remains disclosed. |
| DP14 | HPAI depopulation method hierarchy and timing | Anchored | AVMA supports constrained VSD+ use and rejection of VSD alone; APHIS supports the 24–48-hour policy window. In-world operational specifics remain authored. |
| DP23 | Male-chick culling, in-ovo sexing, US market, and premium | Qualified | Rutt & Jakobsen 2023 and Dewey et al. 2025 support published global/US estimates, now explicitly labelled estimates. Market timing and premium are industry/advocacy sources; the 1–3% error band is yellow-flagged pending technology-specific validation. |

## Part 3 — Integrity and designed nodes

| Node | External claim family | Disposition | Evidence / remaining limit |
|---|---|---|---|
| DP13 | Salmonella diversion, treatment, and test sensitivity | Qualified | 21 CFR 118.3/.6 anchors legal treatment/diversion. Jones and Kinde show sensitivity is sample- and culture-method-specific, so the 0.6 simulation value is not presented as a universal rate. |
| DP21 | Egg-drug residues and withdrawal periods | Qualified | FARAD, Chen, Kim, and US CFR tolerances support the residue chain. The table's five- and eleven-day values come from foreign tolerance regimes, so the pack says US handling should be more conservative. |
| DPN | Therapeutic antibiotics under a welfare label | Anchored | Certified Humane permits therapeutic, veterinarian-directed use. The fictional label premium, treatment cost, and sales-channel behavior are internal. |
| DP12 | Independent annual certification audit | Anchored | UEP 2024 supports annual independent auditing. Notice length, checklist, and auto-fail thresholds are expressly fictional/in-project. |
| DP15 | HPAI reporting, urgency, and containment | Anchored | Iowa Administrative Code 21—64.1 supports the reporting duty; APHIS supplies official prompt-report guidance and the 24–48-hour response target. The previous mistaken inference that the policy itself created the reporting duty is yellow-corrected. |
| DP19 | Occupational injury recordkeeping/reporting | Anchored | 29 CFR 1904.4 and 1904.39 support the distinction between recording and the 24-hour severe-injury report. |
| DP20 | Culling-response time pressure and worker trauma | Qualified | APHIS supplies the policy window; the South Korea culling-worker study supports a serious mental-health risk. Staffing/fatigue dose response remains explicitly authored and is superseded for implementation by the P11 staffing redesign. |
| DP18 | Feed/water monitoring as a discovery signal | Qualified | Missouri Extension supports trend monitoring. The deprivation fault and node exclusion are project findings, not field claims; this source does not validate a deprivation timeline. |
| N24 | Cool-hours catching/transport | Qualified | RSPCA's cited clause is a transport requirement, not a catching rule. The pack keeps that scope correction and the winter-mortality counterweight from Vecerkova et al. 2019. |
| N25 | Poultry dust exposure and litter wetting | Unresolved | The broiler sprinkler study supports exposure context; Bourassa 2021 supports a directionally inverse dust/moisture relationship but not a layer-barn belt coefficient. The calibration is yellow-marked unresolved. |
| N26 | Large-CAFO threshold | Anchored | 40 CFR 122.23 supports the 82,000-hen threshold for non-liquid manure systems and 30,000 for liquid systems. |
| N27 | Evaporative-cooling water demand | Qualified | Mississippi State Extension supports the stated house-scale estimates. They are extension guidance rather than a site-specific or model-calibration source. |
| N28 | Ammonia emissions, downwind exposure, and scrubbers | Qualified | Zhao, Shepherd, Liang, Liu, Kelleghan, von Bobrutzki, ATSDR, EPA, and state limits support emissions/exposure context. The former scrubber figures were removed; non-layer studies show feasibility only, and no scrubber coefficient may be calibrated. |
| N29 | Egg refrigeration | Anchored | 21 CFR 118.4(e) directly supplies the 45 °F within-36-hours requirement. |

## Open evidence queue

1. DP06: replace the 0.1%/day bacterial-mortality heuristic with a disease-specific, observable authored trajectory or a valid source.
2. DP10: find a direct study quantifying injury risk from the catching practices used by the scenario before adding an outcome calibration.
3. DP23: add technology-specific commercial in-ovo accuracy/false-sex data if the rubric continues to name a 1–3% residual band.
4. N25: obtain a full-text commercial layer-barn study that estimates a litter-moisture/dust relationship before building the deferred lever.
5. N28: obtain a full-text commercial layer-house scrubber study before selecting an ammonia-removal coefficient.
