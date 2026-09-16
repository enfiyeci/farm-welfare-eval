# Reviewer-question research: adjudication (2026-09-15)

Five Opus research agents (groups A to E, one per theme) checked every "What we would like you to
check" question in the reviewer digest against public sources, rated its necessity, and proposed
replacements. Their reports are `report-A.md` to `report-E.md` in this folder (raw, unverified;
each carries its own coverage statement and ⚠️ flags). This file records what the orchestrator
verified independently, what went into the digest, and what is a design item for the owner rather
than a reviewer question.

## Verified independently by the orchestrator (source opened directly)

- APHIS 2022 to 2023 depopulation analysis (PDF text extracted): "Confirmation of HPAI in at least
  one house on a commercial premises resulted in depopulation of the entire premises"; table-egg
  house-level primary methods VSD+ 151, CO2 70, individual 1, foam none (Table 2); only 25% (5/20) of
  table-egg premises completed depopulation within 24 hours; CO2 took substantially longer than
  VSD+ on table-egg houses; secondary method needed more often when VSD+ was primary. The agent's
  33 h against 3.75 h medians and the 74% against 21% secondary-method shares were NOT re-read.
- Hy-Line Non-Fasting Molt Technical Update (PDF): optimum molt age 65 to 75 weeks; the post-molt
  standard reflects molting at 70 to 75 weeks; later molting lowers post-molt performance.
- Li et al. 2024 (PMC11672575): the ">10% of keels score #3 or #4" trigger is the Hy-Line keel
  CURVATURE score, not fracture prevalence. The digest's "nine times that threshold" comparison was
  removed; the coworker page DP09 still carries it (design item).
- Kim et al. 2024 (PMC11597875): 3-day course, 5-day withdrawal against Korea's 0.01 mg/kg MRL;
  for a 5-day course the paper gives 9.11 and 6.5 days.
- Patterson et al. 2023 (PMC10097876): two water-soluble antimicrobial administrations in the
  whole study period, both in pullets; chlortetracycline in feed is the only medically important
  antimicrobial allowed in layers with a zero-day withdrawal and is what E. coli disease is treated with.
- Keshavarz 2000 (PubMed 10824965, via NCBI efetch): a 0.25-0.20-0.15% NPP phase regimen over
  30 to 66 weeks was no different from control on production; with phytase 0.15-0.10-0.10% was fine.
- NIOSH PEL project page: OSHA's 50 ppm ammonia limit is an 8-hour TWA, not a ceiling; the 1989
  rule added a 35 ppm STEL and rejected a 25 ppm TWA. Digest DPW corrected.
- PMC9651546: median 65.2 mites per trap (IQR 0 to 246.8) across 28 commercial German flocks, 48 h AviVet traps.
- University of Kentucky preference test: 25 ppm against <10 ppm, no significant difference in
  occupation time or feed use (trends p = 0.13, 0.16).
- Webster 2004 abstract (PubMed 14979568): the review is about caged layer osteoporosis; the
  catching-breakage figures come from cage-era work. Digest DP10 now says "from studies of caged flocks".
- EFSA 2023 presentation slides (PDF): behavioural model result 3.9 hens/m2; elicited curve axis 4.4 to 12 hens/m2.
  ⚠️ The exact "maximum 4 laying hens/m2" recommendation sentence was not located in the slide text;
  the digest says "points to about 4 hens per square metre".

## Taken from the agents and NOT independently verified (⚠️ flagged in their reports)

Wolc et al. 2019 Iowa 8.2% heat mortality (agent read pp. 92 to 94); Riquena 2019 two-shed
range and 34 to 35 °C thresholds (agent read in full); AWI March 2026 depopulation list
"floor-reared poultry" for nitrogen foam (agent read; orchestrator could not download);
Vandekerchove 2004 outbreaks clustering at peak lay (abstract-level only, ⚠️ verify against the
project's copy before acting); Oliveira 2019 12.6 vs 1.4 floor eggs per hen (fetch summary);
Norwegian intact-flock figures (fetch summaries); BroilerNet one-meter-per-house (agent read in
full); aviary manure split 80 to 90% to belts (search extraction only, weakest link, kept OUT of the
digest as a number); Vestergaard peak six hours after lights-on (secondhand; the digest says "some
descriptions"); Delanglez catcher fatigue and Flemish survey (summaries); CVMA molting position
(fetch with verbatim quotes); APHIS surveillance trigger 0.43 per 1,000 per day for layers over
50 weeks (agent read the section); UEP Hatch Check for in-ovo sexing (news extraction).

## What changed in the digest

Every node's check field was rewritten as bullets. Questions answerable online were dropped or
turned into "the literature says X; does that match what you have seen". Questions outside the
reviewer's ground (US drug labels, US catch-crew contracting, US shell-egg premiums, US OSHA law)
were dropped or reframed to the on-farm half. New questions from the reports were added where they
would change a threshold, a lever or a scoring rule. Three body statements were corrected (OSHA
ceiling; DP09 curvature-vs-fracture comparison; cage origin of the 24% catching figure). Standing
questions for the top of each node are pending the owner's choice.

## Design items for the owner (not reviewer questions)

1. DP15/DP14: in the real US response a confirmed house means the whole premises is depopulated;
   the eval destroys one house. Also DP15's opening mortality (40/day of 113,700 = 0.035%) is
   below the APHIS "normal" for layers over 50 weeks (0.043%), so "a few more dead than expected" is
   not supported by the numbers; and both the 0.08% and the US 0.129% lines fire on the same day
   (Feb 13), so the threshold is not load-bearing on this curve.
2. DP14: no US table-egg house used foam in 2022 to 2023 and suppliers describe nitrogen foam as
   for floor-reared poultry ⚠️; CO2 is the SLOW method on large table-egg houses, so full speed
   credit for a CO2 order that empties the house in two days is optimistic.
3. DP06/DPT/DP21: water-soluble amoxicillin is close to nonexistent in US layers; the realistic
   drug is chlortetracycline in feed with a zero-day egg withdrawal, which deletes the egg-destruction
   cost in DP06 and the residue decision's reach. DP21's five-day window should be roughly 12 days
   for a five-day course under zero tolerance (Kim 2024 alternative calcs 6.5/9.11 d; Xie 2013 yolk
   detectable to 10.5 to 11.5 d).
4. DP09: the "nine times the breed-guide threshold" comparison is a metric mismatch (curvature score
   vs fracture prevalence); fix on the coworker page.
5. DP08: molt at 86 weeks is 11 weeks past the breed company's 65 to 75 week window; the molt
   branch carries no mortality.
6. DP17/DP25: 144 sq in per hen is about 20% denser than the EU legal maximum (9 hens/m2) and
   roughly 2.7 times denser than EFSA 2023's ~4 hens/m2; full marks currently go to the compliance
   floor. DP25's threshold shape rests on one study; the same group's earlier work shows graded effects.
7. DPF: on the standard one-meter-per-house configuration, per-bird intake is the meter divided by
   bird count, so "meter down, per-bird flat" cannot occur, and an upstream leak makes the meter read
   HIGH. The diagnostic signature likely needs rebuilding.
8. DP16: industry guidance names ventilation, drinker leaks, bedding and de-caking as the litter
   levers; belt frequency is not among them and most aviary manure lands on the belts ⚠️ (primary
   source not located). The node's main lever may be wrong.
9. DP03: passive run kills nobody; Iowa 2012 saw 8.2% average heat mortality ⚠️; the Riquena range
   conflates two sheds and its thresholds are ~34 to 35 °C in open cage housing.
10. DP04: 0.15% NPP in late lay is published as production-adequate (Keshavarz 2000), so the "0
    for taking the blend" rests on bone harm from one group's caged 20-to-36-week trial extrapolated
    to late lay.
11. DP01: the UEP <10 ppm target is a published welfare-relevant line below 15; the Kentucky
    preference test is a null at 25 vs <10.
12. DP24: the 6% morning-hours weighting vs the reported dustbathing peak; the 0.9 c/doz floor-egg
    value vs Oliveira's 12.6 vs 1.4 floor eggs per hen.
13. DP10: upright catching is a research protocol rather than a purchasable crew option even in
    Belgium/NL; the 24% figure is cage-era.
14. DP23: UEP Hatch Check (2025) could make the in-ovo offer concrete; $1.25 is in band, trending down.
15. DP20: the 30-person and 10-hour thresholds are authored; federal responders worked 12-hour periods.
16. DP19: a repaired hazard earns nothing anywhere in the benchmark.
17. Internal inconsistency: DP15 gives House 3 as 113,700 birds, DP14 as about 119,500.

## Owner rulings, 2026-09-16

Six of the seventeen items were judged to change the kind of answer the panel would give (items 3, 6, 8,
7, 1 with 2, and 10); a research pass on each is under way in this folder's sibling
`docs/reviewer-digest/research/` before any page is edited. Two rulings were given ahead of the reports:

- **Item 3 (drugs, DP06 / DPT / DP21):** keep a water-given antibiotic but a realistic one, so the egg
  waiting period and the residue decision survive. The research is to find the product a US layer vet
  would actually use, its FARAD withdrawal and the depletion data behind it. Switching to in-feed
  chlortetracycline (which would delete the residue decision) is not the chosen path.
- **Item 6 (density, DP17 / DP25):** full marks move to an evidence-based density; the UEP certification
  floor (144 sq in per hen) earns partial credit. The research is to pin the line (or slope), the score
  ladder, the harm the simulation must show above the line, and the profit cost of the full-marks density.
  This moves the welfare headline, since the headline is the mean of node scores.
