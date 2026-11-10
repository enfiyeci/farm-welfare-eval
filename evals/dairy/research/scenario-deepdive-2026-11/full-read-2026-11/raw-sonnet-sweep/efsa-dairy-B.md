# efsa-dairy-B: EFSA dairy cows 2023 (EFSA Journal 21(5):7993), lines 2201 to 4400

SCRATCH = /private/tmp/claude-501/-Users-ardaenfiyeci-Desktop-farm-eval--claude-worktrees-dreamy-dirac-c9c1ab/c421eb6f-9f85-4ecd-aaac-feba06e1218d/scratchpad
All line numbers are lines of SCRATCH/efsa7993.txt.

## 1. Coverage statement

- Read build-claims.txt lines 1 to 168 (whole file).
- Read efsa7993.txt in seven consecutive chunks with no gaps: 2201-2500, 2501-2800, 2801-3100, 3101-3400, 3401-3700, 3701-4000, 4001-4400. Every line of 2201 to 4400 was opened and read. Nothing skipped.
- The range starts mid-section (udder-health/mastitis housing text, line 2201) and ends mid-section (EKE Phase 1 ranking steps, line 4400). Content covered: end of mastitis section (Tables 29, 30, E.6), restriction of movement and resting problems (Tables 31-41, F.1, F.2), comfort behaviour (Tables 42-45, G.1-G.3), metabolic disorders (Tables 46-48, H.1, H.2), and the start of Assessment 3 (farm characteristics: herd size, milk yield, lifespan, culling, SCC; Tables A.1, I.1, I.4-I.24; EKE method).
- Reference list (line 6201 onward) was used only to look up the populations of Charlton 2014, Krawczel 2012, Solano 2016, Tucker 2021, Winckler 2015, Dallago 2021, Fregonesi 2007 (title lines only).
- Reading problems:
  - ⚠️ Line 3140-3141: the equation for total indoor space ("the equation was calculated to be:") did not convert; only the result (about 9 to 10 m2 per cow, line 3142) is readable. The inputs (cubicle, feeder, alley dimensions) are not in my range.
  - ⚠️ Figures 4, 5, 6 are caption-only (lines 2431, 2437, 2597); Figure 9 caption only (line 4328).
  - ⚠️ Source inconsistency (not a reading gap): line 3146-3147 says farms with rubber floors had longer lying times than concrete (Solano 2016), but Table 41 (line 3193) says "Rubber (vs. concrete floor): lying ↓" and line 2737-2738 also says deformable flooring lowered lying time (Solano 2016). Do not cite the rubber-floor direction without checking Solano 2016.
  - ⚠️ Table 48 footnote (line 3789) says "↑ = significant better metabolic health", which contradicts the rows (which list hazards that increase ketosis). Direction in Table 48 is uncertain; the hazard reading is the likely one.
  - The colour coding (red/green arrows) in the tables is lost in the text conversion; I relied on the text of the effects only.
  - Arrow symbols: ↑ higher, ↓ lower, ns not significant.

## 2. Claim hits

| Claim | Verdict | What the document says (figures, population, primary) | Lines | Proposed status |
|---|---|---|---|---|
| A2.1 | supports | Overstocking cubicles cuts lying time. Tucker et al. 2021 (review of experimental studies, lactating cows): average lying time falls as stocking density rises; reduced above 1.2 cows per cubicle, and one of four studies (Fregonesi 2007) found a fall already going from 1 to 1.2 cows per cubicle. Winckler, Tucker and Weary 2015: 150% vs 100% stocking (cows per cubicle) lowered lying h/day and cut behavioural synchrony. Krawczel 2012 (Holstein, Ohio): 142% and 131% vs 113% and 100% lowered lying h/day and raised displacements from the feed place. Collings 2011: feed-bunk overstocking 200% vs 100% raised displacements from the feed place. EFSA notes these trials blocked off cubicles without changing bunk or alley stocking, so they may underestimate the effect in a real overstocked barn. Competition: higher cow:cubicle ratio raised agonistic interactions in six studies (Collings 2011; Krawczel 2012; Talebi 2014; de Vries 2015; Lobeck-Luchterhand 2015; Winckler 2015). | 2889-2892, 2967-2968, 2989-2991, 3083-3092, 3164-3166 | S (secondary, cites primaries). Conclusion at 3114-3118 is EFSA's own EKE (see New facts). |
| A2.1 (extra) | supports (indirect) | Displacements from cubicles per 24 h: 1.9 at 150%, 1.1 at 100%, 0.6 at 75% (Winckler 2015). Witaifi 2018: more displacement from cubicles at 150% than at 100% or 120%, no difference between 100% and 120% (varied cubicles and feed manger). Subordinate cows are displaced more (Val-Laillet 2008a), so their lying time may suffer at lower densities than dominant cows. | 3103-3112 | S |
| A3.2 | partly | Heat load is named as one cause of lying time below 10-12 h/day, a sign of high welfare risk (Tucker et al. 2021). The lying-time ABM is shorter in heat-stressed cows (EFSA's own ABM assessment, Table 33). Nothing in this range links heat to standing time raising lameness. | 2533-2534, 2574 | S for the lying-time half; the heat → lameness half stays unsupported by this part. |
| A1.7 | partly | Wet bedding makes cows perch (forelegs in cubicle, hind legs in alley), "a behaviour that has been related to increased risk of lameness" (Bernardi 2009; Dippel 2009a). Bedding DM 86% to 26% cut lying 13.8 to 8.8 h/day (Fregonesi 2007); DM 90% to 35% cut 11.5 to 10.4 h/day and raised standing in alleys (Reich 2010). Also: long walking distances on poorly maintained tracks may raise claw disorder and lameness risk (cross-reference to Section 4.1.5, not in my range; no primary given here). Nothing on footbaths. No statement that better stalls cut new cases. | 3066-3072, 2725-2726 | S for the stall/standing link (cites Bernardi 2009, Dippel 2009a). Footbath and "better stalls cut new cases" parts: nothing. |
| A4.5 | partly | Housing dry cows in more than one group raised clinical ketosis or displaced abomasum (Stengärde 2012, Sweden, 60 herds, high- vs low-incidence). Dry cows housed apart from lactating cows raised subclinical ketosis, BHB 1.2 mmol/L or more (Oetting-Neumann 2018, Germany, 51 farms). EFSA attributes these to differences in feeding regime, not to regrouping stress. Heifer integration before calving cut displacements (de Vries 2015). Overstocking the transition pen cut self-grooming right after regrouping (Mazer 2020) with no disease outcome. No data on close-up pen crowding and disease. | 3782-3785, 3791-3793, 2998, 3498-3499, 3507 | S, weak: regrouping (more than one dry group) has a disease association; crowding has none. |
| A4.4 | partly | EFSA lists "lack of proactive detection of mastitis in early postpartum cows" as a treatment-related hazard for mastitis. Says nothing about 10 to 14 days of daily observation as standard practice. | 2381-2383 | S weak (EFSA's own listing from its general mastitis search, Appendix B Table B.3, no primary named here). Does not source the 10-14 day norm. |
| B2.1 | partly | SARA is defined by rumen pH below 5.5; rapidly fermentable carbohydrate (concentrate) with too little long fibre raises SARA risk in early lactation (EFSA's own statement, no primary). Metabolic disorders are associated with claw disorders (Nielsen et al. 2013), metritis, retained placenta (Berge and Vertenten 2014) and impaired fertility (Ribeiro 2013). That is a general link, not specifically starch → SARA → claw-horn lesions. | 3608-3610, 3634-3637, 3651 | S (starch → SARA is EFSA's own; claw link cites Nielsen 2013 but only as a general association). |
| B2.2 | partly, with a tension on ketosis | "There is no convincing scientific literature to suggest that milk yield or herd size are consistent hazards" for lameness, claw lesions or integument alterations. Lameness vs yield: lower lameness with higher yield in German tie-stalls (Oehm 2020); higher lameness in Irish pasture herds with 6,000 kg or more (O'Connor 2020); no effect in Finnish cubicle herds (Sarjokari 2013) and Spanish herds (Pérez-Cabal 2014). Mastitis: no clear evidence yield or herd size is a good risk indicator. BUT metabolic disorders: the majority of indicators, all including clinical ketosis, were positively associated with milk yield, "often marginal" (3 studies: Stengärde 2012 Sweden; Vanholder 2015 NL, 23 farms; Berge and Vertenten 2014 found none for subclinical BHB). EFSA's summary still says no clear evidence yield is consistently linked to metabolic disorders. Also lying time lower in higher-yield herds in two Canadian cubicle studies (Deming 2013, Solano 2016) possibly because high-yield cows spend more time feeding. | 3917-3921, 3953-3955, 4033-4034, 4141-4144, 4168-4170, 4042-4046 | S (EFSA synthesis of epidemiological studies). Note for the claim text: EFSA's ketosis data lean positive with yield, so "do not author more ketosis from yield" is not clearly backed by EFSA; it only says the evidence is variable and marginal. |
| D1.4 | partly (EU context, not US) | EU culling rates (percent of herd removed per year): Germany 31.9 (2020), Sweden 35.8 (2020), Netherlands 23.0-28.0 (2007-2010, n = 1,903), Ireland 21.3 (2003-2006). On-farm mortality (died, euthanised or emergency slaughtered): Germany 2.3 to 4.2 (2016-2020), France 2.0 to 3.8, Ireland 3.2 to 4.1, Denmark 3.1 to 3.7 (cubicle, herds over 100 cows). Does not confirm the US 33.8% and 5.6%, but the same order of magnitude. | 4248-4252, 4257-4264 | S for the EU comparison; the US figures keep their V (NAHMS). |
| D1.5 | partly (EU context) | Productive lifespan at slaughter: Germany 3.0 years (36.5 months; 2.3 in living animals, 2020, VIT); France 2.2 (2000s); Poland 4.3; Italy 3.5; Netherlands 3.4; Ireland 3.4 (2010s) (Dallago et al. 2021 review). Average age at slaughter 4.6 to 6.4 years. EFSA says productive lifespan has fallen worldwide in recent decades and that data are too thin to use as a farm risk indicator. | 4190-4194, 4216-4222, 4202-4211, 4225-4226 | S (Dallago 2021 is the primary-level review). Supports the "short lifespan" framing; says nothing about modelled optima of 4 to 9 years. |
| E4.1 | partly | The main reasons for involuntary culling "mostly reported by farmers" are infertility, locomotor disorders and udder diseases (Compton 2017; Dallago 2021). At EU national level, slaughter data carry no culling reason, only age (no sex, origin or reason). EFSA does not say reasons are unverified. | 4239-4243, 4267-4269 | S weak. Supports "reported by farmers" and "no national reason record"; does not state they are unverified. |
| E5.5 | partly | No perfect SCC threshold exists to determine intramammary infection; thresholds vary between 100,000 and 200,000 cells/mL; 200,000 is commonly used (IDF 2013). Says nothing about the ISO 80%/99% benchmark or milk-based detection methods. | 4279-4282 | S weak. |

## 3. New facts for the scenarios

All are EFSA statements; "EFSA's own" means expert judgement or EKE with no primary study.

**A2 (overstocking), also A1, A3**
- EFSA's own (EKE, working group experts): at least 1 cubicle per cow is needed to avoid restriction of movement and resting problems, stated with 90% certainty. Understocking (more cubicles than cows) benefits cows, especially subordinate cows, with 66% certainty. Lines 3114-3118.
- Total indoor space of about 9 to 10 m2 per cow when cows are in the pen, EFSA's own calculation from DK, UK, FR, SE, DE best-practice recommendations (cubicle ratio 1:1, feeder space 1:1). The equation itself is missing from the text. Lines 3133-3142.
- Passageway space from 3 to 6.5 m2 per cow (9 to 14 m2 total per cow) raised lying time by 65 min/day and cut standing/walking in passageways by 64 min/day (Thompson et al. 2022). Lines 3125-3127.
- Time away from the home pen for milking: in 111 Canadian cubicle farms (Charlton et al. 2014) away-time ranged from 1 to over 8 h/day; no farm over 3.7 h/day had 12 h or more of lying, and milking time over 3.3 h/day was linked to less lying. EFSA: more than 3 to 4 h waiting for and being milked is a risk. Lever: parlour throughput and group size. Lines 3185-3189.
- Restraining cows in headlocks for health checks or insemination also takes time from lying (no figure). Lines 3215-3216. Tension for A1 and A4 (checks cost lying time).
- More space at the feed bunk raised lying time (Deming 2013); bunk space 0.3 vs 0.6 m/cow cut social licking (Val-Laillet 2009); 24 h feed access cut feed-place displacements vs 14 h (Collings 2011). Lines 2975, 3512-3514, 3159-3160.
- Oestrus drops lying time by up to 40%, and lying is low in the first weeks after calving (Tucker 2021); the 10-hour lying-time criterion does not apply to cows in oestrus, on pasture or peri-partum. Lines 2541-2546, 2574.

**A1 (lameness), A2 (comfort levers), A3**
- Bedding levers with numbers: 5 to 7 cm compressed bedding, about 3 kg straw per day, is EFSA's own judgement of a comfortable surface; mats and mattresses need bedding on top. Lines 3074-3079.
- Lying time gains: deep sand bed 1.4 h/day longer than other surfaces but only with high curbs (Solano 2016, 141 Canadian farms); deep bedding about 0.8 h/day longer (Ito 2014; Westin 2016b); bedding under 2 cm cut lying (Morabito 2017, Alberta); each 1 cm drop in sand depth below the curb cut lying by 11 min and a 14 cm drop cut 2.3 h (Drissler 2005); each extra 1 cm of compressed sawdust adds 9 min lying, straw 6 min (Tucker 2009). Lines 3015-3019, 2959, 3050-3054, 3046-3047.
- Hard surfaces cut lying time; cubicle width and curb height raised it (Morabito 2017; Solano 2016). Lines 2937-2938, 3015.
- Hock/integument: higher milk yield linked to more hock alterations in two of three studies (UK Potterton 2011; Slovenia Ekman 2018 severe). Lines 3943-3951.

**A1, E5 (detection ideas)**
- Brush use falls in lame cows and in cows with metritis, a "low-resilience" behaviour suggested for early disease detection (Mandel 2017, 2018; Weigele 2018). The effect appeared only when the brush was 16 m from the feed bunk, not at 3 m (Mandel 2018). Self-grooming fell from about 5 to 3 bouts/h with induced E. coli mastitis (Fogsgaard 2012). Lines 3270-3280, 3291-3292, 3304-3314.
- Brush-use sensors: reliability questionable (RFID missed heifer contacts, Toaff-Rosenstein 2017). Lines 3333-3334, 3339.
- Step activity, walking distance and speed: high sensitivity, low specificity for restriction of movement, because lameness also lowers them (EFSA's own qualitative ABM rating). Validated lying-time monitors are "not widely available on farm". Lines 2476-2478, 2574. Relevant to E5 (alerts mix several causes).
- Subclinical ketosis tests: milk fat:protein has low sensitivity, medium specificity; blood or milk BHB has high sensitivity and specificity but needs 12 or more early-lactation cows sampled; BHB thresholds vary (0.96, 1.0, 1.2 mmol/L). Rumen pH bolus: pH 6 or below flags SARA, high sensitivity, medium specificity; rumenocentesis pH 5.5 or below. Serum calcium 2.14 mM or below at 24 to 48 h after calving flags subclinical hypocalcaemia (Rodríguez 2017). Lines 3626-3628, 3644-3646, 3651-3652, 3657.

**A4 (fresh cow), B2 (ration)**
- Dry-period body condition above 3.5 (5-point scale) raises risk of low intake, ketosis and displaced abomasum next lactation; BCS tracking is EFSA's suggested proxy. Lines 3659-3662.
- Comparison rates (EU, per herd): clinical ketosis 1.6% prevalence (Berge and Vertenten 2014; 131 herds, 5 countries, mean 294 cows), 1.3 to 3.4 per 100 cow-years (Simensen 2010, Norway); subclinical acidosis (fat:protein under 1) about 8 to 15% of herds' cows (Dechow 2011 USA 8.6 to 15.1%; Austria 8 to 9% median). Useful as comparators for A4.3. Lines 3669-3691.
- Metabolic disease is hardly affected by housing system (majority of 11 comparisons no difference) except clinical ketosis more common in tie-stalls; pasture access had no consistent effect (14 of 19 comparisons no effect). Lines 3717-3724, 3728-3736, 3761-3762. Argues against building a housing lever into A4/B2.
- Feeding-management hazards for ketosis: separate roughage and concentrates, PMR vs TMR, two-phase dry cow feeding, high push-up frequency (3 times a day) (Oetting-Neumann 2018; Berge and Vertenten 2014). ⚠️ Direction uncertain (see footnote problem, line 3789). Lines 3782-3788.
- Mastitis hazards that overlap fresh-cow care (all from EFSA's general mastitis literature, no primary named): no parenteral calcium at calving, assistance at calving, poor heifer hygiene before calving, no mineral/vitamin supplementation before calving, lack of clean bedding at calving, hypocalcaemia and negative energy balance as immune suppressors, no hay in the dry cow diet, no SOP for colostrum management, heifers housed close to calving apart from lactating cows. Lines 2385-2395.
- Brush use is high around calving: 31.5 min/day 72 to 48 h before calving (Newby 2013, 16 cows) and 6 min/day the day after calving vs 1.8 min/day average (Mandel and Nicol 2017). Possible behavioural marker of the transition. Lines 3398-3400, 3441-3443.

**A5 (mastitis), D1, E4**
- Mastitis hazards that are lever-like: treating fewer than 50% of clinical cases with antimicrobials, no treatment of high-SCC cows, intramammary dose above recommended, no separation of new cases, and "lack of immediate culling of cows with repeated cases of clinical mastitis within a lactation". Culling to keep a low infection pressure is listed as protective. No primary named (EFSA summary of Section 4.2.8). Lines 2370-2372, 2381-2388. Tension for D1 (cull chronic cases for herd health vs welfare timing).
- Glove use, pre-treat disinfection, post-milking teat disinfection, post-milking standing 90 to 120 min, sand bedding, deep bedding over 2 cm: lower infection (Dufour 2012; Watters 2013, 2014; Esser 2019). Lines 2289-2293, 2344-2347, 2357, 2370-2372.
- Pasture access does not consistently improve mastitis (Tables 29 and 30); indoor housing system effects are mostly non-significant. Lines 2269-2270, 2203-2205.
- Lame cows and over-conditioned cows were linked to higher bulk-tank SCC (Matson 2022). Line 2348.
- Pain relief for mastitis, withdrawal times, cost: nothing in this part.

**E3 (rough handling), stockperson**
- Farmers who find contact with cows pleasant, spend more time observing, show a higher share of positive interactions at milking and are patient moving cows had better udder health (more bacteriological and SCC cure, lower SCS) (Ivemeyer 2018, Swiss herds). "Working fast rather than precisely" and part-time farming are listed as mastitis hazards. Lines 2342-2343, 2352-2356, 2396-2397. Useful for realism in E3: handling quality has a measurable herd-health cost, but this is correlational.
- Agonistic-interaction counts also depend on the human-animal relationship (Table 32, line 2524).

**C1, C2 (calves), minor**
- Cow-calf contact: heifers reared by their mothers for 12 weeks self-groomed more often when integrated into the milking herd than those raised with automatic feeders, but time spent did not differ, so EFSA calls the welfare meaning inconclusive (Wagner 2012). After calf removal, cows' self-licking rose (Newby 2013). No distress or yield data. Lines 3557-3563, 3582-3585.
- Weaning off milk before 4 months of age and over-feeding concentrates to young calves and heifers are listed as hazards for later mastitis (EFSA's summary, no primary). Tags C2. Lines 2386-2387, 2390.

**D1, E4 (culling)**
- Increased involuntary culls or higher mortality are suggested proxies for poor welfare (de Vries 2011; Thomsen and Houe 2018), and EFSA lists culling and on-farm mortality as potential farm-risk indicators because they are increasingly recorded nationally in Europe. Lines 4235-4237, 4271-4273.

**Pasture/outdoor access (no matching scenario; context)**
- Cows prefer pasture, especially at night: 90% of time on pasture vs 44% in a sand-pack loafing area (Smid 2018); cows would walk farther to keep night pasture (Charlton 2013). Lines 2620-2634. Not a scenario lever in a US freestall farm.

## 4. Claims this part says nothing about

A1.1, A1.2, A1.3, A1.4, A1.5, A1.6, A1.8;
A2.4 (lines 2286-2288 only say cubicle housing is predominant; nothing on stocking above 100%), A2.2 (no lameness outcome for overstocking in my range; only reduced lying and standing in cubicle front legs), A2.3;
A3.1, A3.3, A3.4, A3.5, A3.6;
A4.1, A4.2, A4.3 (EU comparators in New facts only);
A5.1, A5.2, A5.3, A5.4, A5.5, A5.6;
B1.1, B1.2, B1.3, B1.4, B2.3, B2.4;
C1.1, C1.2, C1.3, C1.4, C2.1, C2.2, C2.3;
C4.1, C4.2, C4.3, C4.4, C4.5;
C5.1, C5.2, C5.3, C5.4, C5.5;
C6.1, C6.2, C6.3, C6.4, C6.5, C6.6, C6.7;
D1.1, D1.2, D1.3;
D2.1, D2.2, D2.3, D2.4, D2.5;
D3.1, D3.2, D3.3;
D4.1, D4.2, D4.3, D4.4, D4.5, D4.6, D4.7;
D5.1, D5.2, D5.3, D5.4, D5.5;
E1.1, E1.2;
E2.1, E2.2;
E3.1, E3.2;
E4.2, E4.3, E4.4, E4.5;
E5.1 (EFSA's qualitative sensitivity/specificity ratings are for housing-restriction ABMs, not alert data), E5.2, E5.3, E5.4.
