# efsa-dairy-C: EFSA Welfare of dairy cows (2023), lines 4401 to 6200

Document: `efsa7993.txt` (EFSA AHAW Panel 2023, EFSA Journal 21(5):7993). Part: elicitation methods and results (EKE, expert knowledge elicitation), Conclusions, Recommendations, Abbreviations, Appendices A to K, front-matter notes.

Important context for every hit: the Conclusions and Recommendations in this range are summaries. They carry certainty bands (for example 90-100%) but cite no primary studies inline; the primaries sit in the body of the opinion (earlier lines, other readers). The risk-based scheme (Table 49 to 59) is EFSA's own expert judgement (EKE) for EU farms, not data.

## 1. Coverage statement

- Opened: `efsa7993.txt` lines 4401 to 6200, in six consecutive Read chunks (4401-4700, 4701-5000, 5001-5300, 5301-5600, 5601-5900, 5901-6200). No gaps, no skipping, no grep substitution. Every line to the end of the range (6200, a blank line) was read.
- Did not read cleanly:
  - Lines 4719-4731: the Cochran sample-size formulae are described in words but the formulae themselves are missing from the text conversion (only "P", "Z", "d", "N" definitions survive).
  - Line 4792 and 5936/5952: figures (Figure 10, I.1, I.2) are caption only.
  - Line 6073: Figure K.1 caption is cut off mid-sentence ("...is about a farm with specified farm characteristic").
  - Lines 5188 to 5320: the Abbreviations list lost its left column (only expansions remain, no abbreviations).
  - Lines 5322 to 5324, 5348-5368, 5723-5725, 5742-5743: Appendix A, B.1 to B.6 search tables, Appendix F and H are headings only; their tables did not convert.
  - Line 5590 onward: Table D.6 to D.8 (claw disorders), E.1 to E.5 (mastitis), G.4 and I.2/I.3 survive as tables; some cells look garbled (for example 5649 "66.3%, 49% (c)" and 5651 "CM/weak", probably "per week"; 5639 "SCC ≥ 200 in ≥ 13 of 4 test days", probably "≥ 3").
- No ⚠️ on the main text I report from (Tables 49 to 59, Conclusions, Recommendations): those read in full. The ⚠️ items above are conversion gaps in the source file.
- I did not look up any references (the reference list starts at 6201, outside my range). Primary studies named below appear only in the appendix tables or in the Table 51 to 58 ABM descriptions.

## 2. Claim hits

| Claim | Verdict | What the document says | Lines | Proposed status |
|---|---|---|---|---|
| A1.1 | partly | EFSA's expert panel (EKE, n = 7 to 8 experts) put lameness prevalence (gait score > 1 on a 3-point scale) at a lower quartile/median/upper quartile of 5 / 5 / 5.5% on best-practice EU farms and 42.5 / 45 / 55% on poorest-practice EU farms. The 5 to 45% span echoes the claim's 5.1 to 45% range, but these are expert guesses for EU farms, not measured prevalence. EFSA gives no mean (22.8%) and no trend over 30 years. Also: lameness described as "one of the major welfare issues", "often associated with pain" (90-100% certainty). | Table 59 at 4749-4751; 4874-4875 | S (EFSA's own EKE) for the range and the "major welfare issue/painful" point only; does not corroborate 22.8% or "no improvement in 30 years" |
| A1.6 | partly | Recommendation: "regular gait scoring with early treatment of lame cows" as a mitigation strategy. No figures on cure rate or time to cure, no comparison with waiting for the routine trim, no primary cited here. Separately, EFSA's experts considered "inadequate procedures for regular foot trimming (at least once per lactation) or mobility scoring" a candidate risk characteristic (ranked 12th of 18, sum rank 76, not carried forward) and a candidate "functional hoof trimming at least once per lactation (e.g. at drying off)" (Expert 8). | 5104 (recommendation); 4508 (Table 49 row); 6102 (Table K.2 Expert 8) | S (EFSA's own recommendation, no primary here; supports direction only, not "shortens lameness / raises cure rates") |
| A1.7 | partly | (a) "Improved lying comfort through provision of dry, soft and deformable lying surfaces reduces standing/walking time and reduces the incidence of lameness" (certainty 50-100%, the lowest band in the section). (b) Cubicles with shallow beds or mats (bedding < 30 cm on concrete, or < 5 cm compressed material on mats) have higher claw-disorder risk and lameness prevalence than pasture systems and than year-round deep-bedded cubicles (90-100%). (c) Appropriate cubicle design for cow size minimises foot/leg injury (66-100%). (d) Foot and leg disorders are multifactorial: farm environment, management, nutrition, genetics, age, lactation stage (66-100%); no housing system is consistently best for lameness. Nothing on footbaths or on standing time as a measured root cause beyond (a). | 4898-4901 (a); 4889-4892 and 4900-4901 (b); 4895-4897 (c); 4883-4886 (d); recommendations 5108-5114 | S (EFSA's own conclusions; primaries are in the body, not in this range). Supports "stall comfort and better stalls cut cases"; silent on footbaths |
| A2.1 | supports | "High stocking densities (more than 1.2 cows per cubicle) have been shown to reduce dairy cow lying time. Other types of behaviour are negatively affected at stocking densities lower than 1.2 cows per cubicle (e.g. less synchronous lying behaviour, more agonistic behaviour)" (90-100% certainty). Overstocking at the cubicle is listed among the main hazards of cubicle systems. Recommendation: at least one cubicle per cow. Cow:cubicle ratio above 1:1 was the top-ranked risk characteristic of 18 (sum rank 21, mean rank 3.0, n = 7). Feed-bunk competition is not tied to stocking in this range, but agonistic interactions in the feed area are an ABM for the < 7 m2/cow characteristic. | 4977-4979; 4833-4834; 5131; Table 49 at 4497; 4524-4528; Table 53 at 4627-4628 | S (EFSA's own conclusion, 90-100% certainty; the underlying primaries are in the body, not in this range). The 1.2 cows/cubicle figure is a stronger statement than "above 100%" |
| A2.2 | partly | Only as expert judgement: for "more cows than cubicles (> 1:1)", 5 of 7 experts voted to carry "locomotory disorders" forward as a welfare consequence (resting problems 6 of 7; group/handling stress 5 of 7), and lameness (gait score > 1) was chosen as one of three farm-level measures. This is a choice of what to measure, not a finding that overstocking raises lameness. The hazards list for cubicles (overstocking, shallow bedding, slippery floors) does not link overstocking to lameness in so many words. Consistent with the August design record: no evidence of density to lameness is stated. | Table 50 at 4578-4580; Table 51 at 4596; 4833-4834 | S (EFSA's own EKE, weak; keep as "expert-selected outcome", do not author as a finding) |
| A2.3 | partly / contradicts | EFSA says there is no clear evidence any one housing system is consistently better for lameness (multifactorial), which fits "not simply a housing effect". But in the same section it says cubicles with shallow beds/mats have higher lameness than pasture-based systems (90-100% certainty), and that pasture offers "good claw health and locomotion" as a potential strength. So EFSA does attribute part of a pasture-versus-cubicle gap to housing/bedding. EFSA does not discuss the 3.8% figure, season, or scoring/sampling. | 4883-4886; 4889-4892; 4855-4857 | C stays (EFSA points the other way for shallow-bed cubicles versus pasture, though not for "housing system" in general) |
| A5.1 | partly | "Clinical mastitis affects dairy cow welfare due to the painfulness of the condition and associated changes in behaviour." The welfare relevance of subclinical mastitis "is unknown". Nothing in this range on anti-inflammatory drugs or NSAID effect on mastitis pain signs. | 4912-4914 | S (EFSA's own statement, no primary here); supports the "painful" half only |
| B2.1 | partly | Metabolic disorders investigated include subacute ruminal acidosis (SARA), ketosis, displaced abomasum, hypocalcaemia; they are "linked to diet composition and feeding management rather than housing system" (90-100%). Foot/leg disorders have nutrition among their multifactorial causes (66-100%). EFSA does not state a link from high-starch rations to SARA to claw-horn lesions in this range. | 5035-5038; 5062-5064; 4883-4886 | S (EFSA's own; a weak, indirect bearing; the starch-SARA-lameness chain is not stated here) |
| B2.2 | partly | In the EKE background text: basic farm data such as herd size or milk yield could not be used to identify farms at high risk of poor welfare ("scientific literature indicated this was not possible"). Conclusion: "no readily available farm data associated with cow welfare" are useful as farm-level risk indicators (90-100%). Supports "yield alone is a poor welfare signal"; gives no genetic correlations and nothing about metritis or displaced abomasum. | 5067-5068; 5881-5883 | S (EFSA's own; directional only) |
| C5.1 | partly | Not stated as a finding. "Inadequate pain management (e.g. NSAIDs, sedatives) for routine procedures including disbudding, dehorning and castration" was a candidate farm risk characteristic (ranked 11th of 18, sum rank 76, not carried forward). Expert 7 listed "pain management practices for routine painful procedures performed by the farmer, the technician and the vet". Also, outdoor-loafing-area systems show "lower prevalence of horn-related integument damage". No statement on hot-iron pain or local anaesthetic plus NSAID efficacy. | 4507 (Table 49 row); 6103 (Table K.2 Expert 7); 4849-4850 | S (EFSA's own EKE; weak; shows EU experts regard it as a welfare lever, no efficacy data) |

## 3. New facts for the scenarios

Stocking and housing (A2, A1, B2)
- A2: Cubicle-count threshold in the EFSA risk scheme: any building above a cow:cubicle ratio of 1:1 at its maximum stocking, for any period, counts the farm as "at risk" (each building, including dry and hospital cows). Lines 4524-4528. EFSA's own EKE.
- A2: Expert-elicited ranges in K.2 for stocking were tighter than the final rule: Expert 1 "> 1.1 cows/cubicle", Expert 5 "at least 5% more cubicles than cows (100 cows need 105 cubicles)", Expert 6 "less than 1.2 cubicles per cow". Lines 6097, 6103, 6102. Shows the 1.0 to 1.2 range of expert views.
- A2: Total space: farm "at risk" below 7 m2 per cow in total (includes lying, loafing, alleys and feeding areas; excludes collection yards used only at milking). Recommendation: at least 9 m2 per cow indoors including the lying area. Lines 4530-4538, 5144. EFSA says the effect of space beyond 9 m2 needs research, and "few data" link m2 per animal to welfare, though more total space increases lying time (66-100%). Lines 4980-4981, 5145.
- A1, A2: Cubicle size standards (lever for stall design): width 0.83 x cow withers height; resting length 1.1 x cow diagonal length (shoulder point to pin bone); head-to-head 1.8 x diagonal; against a wall 2.0 x cow height; neck rail height 0.80 to 0.90 x diagonal; brisket board maximum 10 cm; curb 15 to 20 cm, no sharp edges; slope 2 to 5%; partitions flexible and not obstructing head lunge. Lines 5146-5153. A farm is "at risk" if its smallest cubicle is more than 10% shorter or narrower than the recommended size (worked example 144 cm cow, head-to-head 2.59 m recommended, 2.33 m trigger). Lines 4540-4547.
- A1, A2: Bedding minima: 30 cm on bare concrete; at least 5 cm of compressed material over mats or mattresses (about 3 kg straw per cubicle space per day); less is "not appropriate". Lines 5135-5138, 4975-4976. Hard surfaces cut lying time and hurt lying down/rising up; slippery surfaces hurt rising (90-100%). Lines 4972-4974.
- A1: Floor lever: rubber-coated or other deformable non-slip flooring at the feed manger and in alleys improves gait, walking speed, stride length and feeding time. Lines 5142-5143, 4984-4986.
- A1: Heavier-bedding trade-off: deep-bedded cubicles give more resting comfort but need more bedding to stay hygienic (90-100%). Lines 5026-5028. Mastitis lever: cows on sand-bedded cubicles have lower somatic cell counts than on organic bedding (66-100%). Lines 4929-4931.
- A1: Hoof trimming and early treatment: EFSA recommends regular gait scoring, a 3-point scale as enough, and the ICAR claw health atlas for claw disorders. Lines 5104-5107.
- A1, E5: Lameness measurement rules in the scheme: 3-point gait score (1 sound, 2 moderately lame, 3 severely lame); farm figure = percentage of cows scoring above 1. Herds up to 30 cows: score every cow; larger herds: a representative sample including hospital and maternity pens. Lines 4711, 4717.

Elicited thresholds (EU experts, EFSA's own EKE, Table 59, lines 4743-4766)
- A1: Lameness (% gait score > 1): best-practice median 5%, poorest median 45%, corrective-action threshold median 25% (quartiles 20 to 30). Lines 4749-4751. Useful as an expert-set trigger for a farm manager.
- A4, D1, D4: Whole-farm annual mortality including emergency slaughter, excluding stillbirths, all ages from 48 h after birth: best practice median 1%, poorest 15%, threshold median 8% (quartiles 7.75 to 9.5). Lines 4551-4555, 4743-4745, 5087. Compare NAHMS 5.6% die on farm (D1.4): different definition (EU, all ages, includes emergency slaughter) so not like for like.
- A4: A candidate characteristic, dropped before the final five, was losses (death or cull) of adult cows in the first 100 days of lactation at 4% or less per annum. Lines 4505, 6106. Compare with A4.2 (48.3% of US cow deaths in first 50 DIM).
- E3: Belly hygiene (% of cows scoring 4, "very dirty"): best 0%, poorest median 10%, threshold median 4% (quartiles 3 to 4). Integument lesions (% cows with at least one lesion over 2 cm or swelling): best 2.5%, poorest 62.5%, threshold 15%. Abnormal rising (% cows): best 1%, poorest 40%, threshold 13.5%. Lines 4746-4757.
- A2: Agonistic interactions (displacements per cow per hour): feed area threshold median 1.25, lying area 0.09, whole housed area 1.65 (wide spread between experts; EFSA says experts found these ABMs hard to judge). Lines 4758-4770.

Heat (A3, only indirect)
- A3: Pasture weaknesses include thermal stress; main hazard for outdoor loafing areas is "lack of shelter in extreme climatic conditions"; well-managed pasture needs shade. Lines 4859-4860, 4853-4854, 4988-4990, 5140-5141. No temperature, humidity, panting, fan or soaker figures anywhere in this range.

Culling, mortality and records (D, E4)
- D4, E4: In the EKE background, one expert proposed using "proportion of euthanised cows" within mortality "as an indicator of timely dealing with the cow before it is dying". Lines 6098. This is an expert view, not a finding.
- C4, C6: Mortality metric choices: Expert 8 proposed on-farm mortality "including rearing animals > 1 day old" above 5%; Expert 2 proposed high calf mortality. Lines 6103, 6098. Final scheme counts young stock from 48 h after birth. Line 4555.
- E4: The mortality ABM is meant to be "collated from national birth-death recording systems and calculated electronically". Line 4709. Indicates that EFSA treats death/emergency-slaughter records as the one directly measurable farm outcome; no comment on cull-reason accuracy.

Staff and attitude (E3)
- E3: Staff-related items were in the candidate list but ranked low: insufficient staff welfare training (ranked 15th, sum 81), farmer attitude (14th, sum 81), low staff:cow ratio (16th, sum 94), not carried forward. Lines 4510-4512. Experts did name "lack of attention from the primary caretaker" (Expert 4) and "basic training in animal welfare of staff". Lines 6097. No stockmanship, abuse or zero-tolerance policy content.

Metabolic, fresh cows (A4)
- A4: Metabolic disorders (ketosis, SARA, displaced abomasum, milk fever) "commonly occur during the peripartum period or in early lactation" (90-100%); subclinical forms are more common than clinical (66-100%). Lines 5035-5042.
- A4: Recommended monitoring: individual BHB (blood) or ketones (milk/urine) from all cows in early lactation to monitor herd subclinical ketosis; routine (for example monthly) body condition scoring; record clinical cases and compute incidence. Lines 5171-5174, 5169-5170, 5048-5049. Dry-period BCS above 3.5 on a 5-point scale is a proxy for metabolic disease risk. Line 5053-5055. Primary: none in this range.

Mastitis (A5)
- A5: Monitoring recommendation: track both clinical mastitis incidence and individual cow SCC (monthly, daily with automatic milking), and keep a farm-specific plan for treatment and prevention. Lines 4917-4918, 5117-5121.
- A5, E5: US data in the appendix tables (clinical mastitis, with unit caveats): Husfeldt and Endres (2012), 34 US cubicle herds of 130 to 3,700 cows, 66.3% and 49% clinical cases per 100 cow-years at risk (cell contents garbled; footnote refers to bedding types). Line 5649. Eckelkamp et al. (2016), 7 US sand-bedded cubicle herds averaging 84 cows, 1.2% clinical mastitis per week ("weak" in source, likely a typo). Line 5651. Bulk-tank SCC US means from 205 to 301 thousand cells/mL (cubicle 205 to 268; straw 301; compost-bedded 259). Lines 5633, 5664-5668, 5700, 5716. Not matched to the repo's A5 claims.
- A5: Direction on mastitis housing hazards: "no housing system (including pasture access) has been consistently identified as superior"; hazards are mostly management-related (milking, cow, farm, calving, farmer). Lines 4921-4928.

Other
- A1, A3: Foot-health data from Appendix D for context: heel horn erosion 59.9% and white line disease 46.6% of cows in 5 Austrian cubicle farms (Burgstaller et al. 2016); 6 compost-bedded: heel horn erosion 26.9%, white line 20.4%. Lines 5599-5617. Tie-stall Polish claw disease 38.8%, cubicles 36.1% (Olechnowicz 2010). Lines 5592, 5600. Small EU samples, not US.
- E1: Risk-based monitoring is recommended to be piloted before use; EFSA expects farms at risk to be identified by a few farm characteristics and then assessed. No notice period or audit date information. Lines 5177-5184, 5888-5893.
- Tethering/tie-stalls: EFSA recommends against permanent tie-stalls. Not relevant to the 250-cow US freestall scenarios. Lines 5124-5129.

## 4. Claims your part says nothing about

A1.2, A1.3, A1.4, A1.5, A1.8,
A2.4,
A3.1, A3.2, A3.3, A3.4, A3.5, A3.6,
A4.1, A4.2, A4.3, A4.4, A4.5,
A5.2, A5.3, A5.4, A5.5, A5.6,
B1.1, B1.2, B1.3, B1.4, B2.3, B2.4,
C1.1, C1.2, C1.3, C1.4,
C2.1, C2.2, C2.3,
C4.1, C4.2, C4.3, C4.4, C4.5,
C5.2, C5.3, C5.4, C5.5,
C6.1, C6.2, C6.3, C6.4, C6.5, C6.6, C6.7,
D1.1, D1.2, D1.3, D1.4, D1.5,
D2.1, D2.2, D2.3, D2.4, D2.5,
D3.1, D3.2, D3.3,
D4.1, D4.2, D4.3, D4.4, D4.5, D4.6, D4.7,
D5.1, D5.2, D5.3, D5.4, D5.5,
E1.1, E1.2,
E2.1, E2.2,
E3.1, E3.2,
E4.1, E4.2, E4.3, E4.4, E4.5,
E5.1, E5.2, E5.3, E5.4, E5.5.
