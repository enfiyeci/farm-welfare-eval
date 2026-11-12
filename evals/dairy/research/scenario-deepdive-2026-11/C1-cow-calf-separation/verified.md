Eval: dairy

# When to separate calf and cow: the Gemini answer, checked claim by claim

Written 2026-11-11. Input: `raw/2026-11-10-gemini.md` (Gemini Deep Research, "Detailed research 3.1
Pro", core prompt from `prompts.md`). What changes in the scenario is in `adjudicated.md`; cite that,
not this file or `raw/`.

## How it was checked

An extractor cut the raw answer to 22 claims that could change how the scenario is scored (claim key
ids C1-A1 to C1-C5) and three Sonnet verifier groups checked them against their sources:

- **Group A, separation distress in calf and cow (10 claims).** Weary and Chua 2000 read in full
  from a verbatim PDF (the Fig. 3 page also viewed as an image); Mac, Lomax and Clark 2022
  (PMC10164485) and Daros et al. 2014 read in full from Europe PMC XML. ⚠️ Stěhulová et al. 2008
  and Flower and Weary 2001 are closed: abstracts only (SLU Pure record and PubMed).
- **Group B, benefits and health risks of longer contact, gradual separation (7 claims).** Beaver
  et al. 2019 (systematic review), Quigley's Calf Note #247, Zipp and Knierim 2020 read in full;
  Vogt et al. 2025 read except Tables 4 to 6, the supplement and the reference list ⚠️. ⚠️ Van et
  al. 2023 read through grep of abstract, results and discussion; ⚠️ Vogels 2013 abstract only;
  ⚠️ the three Wagner papers (2012, 2013, 2015) are closed and were reached only through EFSA, a
  same-lab thesis (read in part) and search-engine fragments.
- **Group C, US practice, rules and the milk cost (5 claims).** The 6-page USDA APHIS colostrum
  brief read in full; ⚠️ NAHMS Dairy 2014 Report 1 (268 pages) and the Dairy 2007 calf report (168
  pages) read only at the separation tables and the text around them; 9 CFR 1.1 and 7 CFR
  205.237 to 205.241 read whole from eCFR XML; Asheim et al. 2016 read in full; ⚠️ Mogensen et al.
  2022 abstract only (ScienceDirect HTTP 403); ⚠️ state law checked only by two web searches.

The EFSA 2023 calves opinion (`efsa7896.txt`) and FARM v5 (`farm-v5-pages.txt`) were read in full
on 2026-11-10; the verifiers re-read only the passages they cite.

Before writing any row that changes a status, I opened the passage in the verifier's saved text
and read it myself: the NAHMS brief (page 2 viewed as an image, Figure 2), NAHMS Part I tables
C.2.b and C.2.c, the Dairy 2007 separation table, Weary and Chua's abstract, Tables 1 and 2 and the
diarrhoea result, the Daros methods and results, the Mac 2022 results and discussion, the
Stěhulová abstract, Beaver's Johne's passages and its abstract, EFSA calves lines 284 to 294, 5160
to 5187, 5460 to 5472 and 5497 to 5512, the Calf Note passages on Beam 2009 and Lora 2019, the
Vogt abstract and conclusion, 9 CFR 1.1, 7 CFR 205.239, FARM v5 lines 5948 to 5958, Asheim's
abstract, model tables 4 and 5 and survey-group passage, and the Mogensen abstract. Those rows are
marked **raw-checked**. Everything else is the verifier's reading.

An abstract-level confirmation counts as W (weak), never S or V.

## What the check found about the raw answer

- **The US practice figures are spliced from three surveys.** "67.6% under 12 h" is the 1991
  NDHEP bar of the NAHMS trend chart; "21.9% at 12 to 24 h" is the 2007 bar for 12 hours or more;
  "10.5% at 24 h or more" is the share of heifer calves separated at 12 to 24 hours in Dairy 2007.
  The 2014 survey covered 17 states and 1,261 operations, not "104 operations across 13 states",
  and has no 24-hour cut. Only the 3.6 h to first colostrum is right (**raw-checked**).
- **Weary and Chua figures misread.** "8.2% of standing time" with the head out of the pen is the
  6-hour group's figure (8 ± 2%); the 4-day group's is 30 ± 5%. Calf call rates did not differ
  between ages. The "generous bucket milk before separation to ensure satiety" design is not in the
  paper; it is the Daros study that held milk constant (**raw-checked**).
- **Wrong paper.** The "three times more vocalisation over 72 h" is Mac, Lomax and Clark 2022 (an
  Australian pasture study, about 106 days against within 24 h, 6 cows per group), not Flower and
  Weary 2001, which observed 24 h (**raw-checked**).
- **Overstatements.** Daros separated calves at 42 days, analysed 8 calves and ran in 2012; the
  paper says the bias after separation was "similar" to the bias after dehorning (p = 0.27, a
  non-significant difference, not an equivalence test), so "statistically indistinguishable" and
  "settled" go beyond it. The Stěhulová abstract has no "pacing" and says cow heart rate was not
  affected by calf age or post-separation contact; the claim that heart rate betrays distress
  managers cannot see has no support in it.
- **Disease claims stretched.** Beaver 2019 does not call hygiene "far more important" than
  nursing, never uses "true vectors" and says nothing about pooled colostrum and Johne's. Its "OR
  0.1" for Cryptosporidium is one Italian study; 3 of 9 studies found contact raised the risk.
  Beaver has no Salmonella result. The raw leaves out EFSA's counterpoint on Johne's.
- **Wrong or second-hand citations.** The Calf Note is cited for EFSA's contact-duration ladder,
  which it does not contain. Its 38% failure of passive transfer is Vogels 2013 (Victoria,
  Australia; most farms fed extra colostrum) or a farm-level pooled figure in Van 2023; it is
  neither a "day 1" figure nor a rate for unassisted calves. Mogensen 2022 is cited through an EFSA
  copy, Asheim 2016 through a different paper (Knierim et al. 2020).
- **Wrong details.** Wagner's artificially reared heifers were group-reared, not isolated, and the
  dam-reared heifers were the more submissive ones (read as better social competence); the fear
  and restraint claims were found in no readable source. Vogt's second method was a gradual cut in
  contact time, not fence-line weaning, and its headline is no difference between methods. FARM v5
  does not say nursing must be "properly monitored". Asheim's model farm had 24.6 to 30.2 cows on
  40.3 ha, not 40 cows; "economically optimal" is Knierim's word.
- **Unsourced.** "Less than 1% of conventional US dairies" use contact systems, calf crush injuries
  and cow aggression to alien calves, and the prevalence labels in the raw's Table 2 have no
  citation. "No state law" has no legal source.

## Part 1: the seven claims (C1 to C7)

| Claim | Verdict | What the sources say | Read |
|---|---|---|---|
| C1. Most US dairies separate within a few hours (C1.1) | Confirmed; raw figures wrong | NAHMS Dairy 2014 (USDA APHIS, 17 states, 1,261 operations, survey 2014, published 2016). By operations: under 1 h 10.6%, under 6 h 56.2%, under 12 h 71.5%, 12 h or more 28.5%. By heifer calves: under 1 h 26.0%, under 6 h 76.7%, 12 h or more 12.0%. Medium herds (100 to 499 cows, the class of a 250-cow herd): 12 h or more 24.2% of operations, 21.2% of calves; large herds 6.1%. First colostrum at 3.6 h on average. The trend chart: under 12 h was 67.6% (1991), 68.7% (1996), 75.4% (2002), 78.1% (2007), 71.5% (2014). Dairy 2007: 55.9% of operations (65.6% of heifer calves) removed calves before nursing. | Brief read in full, Part I and Dairy 2007 tables, **raw-checked**. ⚠️ Part I and Dairy 2007 read only at these tables. |
| C2. Later separation, more distress; cows too (C1.2) | Confirmed in direction, with limits | Weary and Chua 2000 (Canada, 27 Holstein pairs, 9 per group, separation at 6 h, 1 d, 4 d, observed to 21 h): 4-day calves had the head out of the pen 209 s per 40 min against 36 s (6 h), made 22.6 against 6.4 moves; calf call rate did not differ. 4-day cows called 34.8 times per 40 min against 7.9 and 7.4, about four times as often, and at a higher pitch. Stěhulová 2008 (Czech Republic, 46 pairs, 1, 4, 7 d): older calves and cows reacted more; calf heart-rate rise lasted longer when separation was later; cow heart rate rose in all cows regardless of age. Flower and Weary 2001 (24 pairs, 1 d against 14 d): cows and calves reacted more after 14 days. The "4 days to 6 to 10 weeks" window is EFSA's synthesis (lines 5507 to 5512). | Weary and Chua full text, **raw-checked**. Stěhulová, Flower ⚠️ abstracts. EFSA **raw-checked**. |
| C3. Benefits of contact grow with its length | Partly | EFSA 2023 calves concludes: vitality after hours, weight gain after 4 days, less diarrhoea after 2 weeks, social competence after 12 weeks (certainty 66 to 100%); no evidence for 3 to 8 weeks. In EFSA's own Table 43 both diarrhoea rows cite Weary and Chua 2000, whose longest contact was 4 days; no 2-week diarrhoea study is listed there. Weary and Chua: diarrhoea treatment 5.5 ± 1.7 days in the first 4 weeks (6 h), 4.0 ± 0.7 (1 d), 2.0 ± 1.2 (4 d), heifers only (16 calves), P = 0.08, a trend. Beaver 2019: across studies, scours and mastitis showed beneficial or no effects of suckling. Social competence at 12 weeks rests on Wagner 2012 to 2015, closed. | EFSA, Weary and Chua, Beaver abstract **raw-checked**. ⚠️ EFSA Table 43 read as flattened text; Wagner unreadable. |
| C4. Early separation and Johne's, Salmonella | Mixed | Johne's: Beaver 2019 (70 studies; 14 on Johne's, all cross-sectional or questionnaire): none found higher prevalence in herds allowing contact, except one univariable result; calving-area hygiene should come first. EFSA: contact is "expected" to aid transmission (Vass-Bognár 2022), and farms suckling calves on foster cows had higher odds of testing positive (Nielsen 2008a,b); EFSA agrees separation alone will not control the disease. Salmonella: EFSA Table 43 notes heavy faecal shedding in the first 24 h after calving, no size; Beaver found no Salmonella study meeting its criteria. Cryptosporidium (Beaver): 2 of 9 studies protective (one OR 0.1), 4 no difference, 3 higher risk with contact. | Beaver Johne's passages, EFSA 5160 to 5176 and 5462, **raw-checked**. Crypto detail: verifier read. |
| C5. Milk cost (C1.3) | Partly | Mogensen 2022 (Danish organic scenario model) via EFSA: 7.1% loss at 9,000 kg ECM per cow per year, full-time contact for 13 weeks (1,207 L calf intake) against restricted bucket feeding (462 L). Its own abstract states 85% of milk produced delivered with full-time contact over 91 days against 93% with low bucket feeding; where 7.1% comes from is unread. Asheim 2016 (Norway, linear-programming model of a dual-purpose farm, 24.6 to 30.2 cows): farm profit NOK 373,289 with no suckling, 394,247 at 3 days, 400,357 at 7 weeks, 361,738 at 13 weeks (October calving); the health inputs come from seven long-suckling farms and are called uncertain. Labour: 5 h (7 weeks) and 10 h (13 weeks) less calf work per calf, assumed. No US cost estimate found. | EFSA and Mogensen abstract, Asheim full text, **raw-checked**. ⚠️ Mogensen full text unread. |
| C6. Public opinion (C1.4) | Not checked | Judged not score-moving. The raw's citations here look mis-numbered. | |
| C7. No US law; FARM v5 sets no time | Confirmed for federal law and FARM; state law not proven | The Animal Welfare Act definition of "animal" (9 CFR 1.1) excludes farm animals used for food or fiber. USDA organic (7 CFR 205.239) sets no separation or contact time; it allows individual pens for dairy young stock until weaning and keeps newborn dairy cattle off pasture for up to six months. FARM v5 sets no separation time; it lists "Bottle feeding, nursing from the dam, tube feeding" as acceptable colostrum methods with no condition attached, and requires colostrum within 6 hours of birth. Two web searches found only veal-calf confinement laws. | 9 CFR 1.1, 205.239, FARM **raw-checked**. ⚠️ State law: search summaries only. |

## Part 2: what the calf and the cow experience

| Question | Finding | Read |
|---|---|---|
| Calf response by age | Weary and Chua: calves were quiet for the first few hours and responded mainly after 9 h; observation ended at 21 h. Head-out time as a share of standing time rose from 8 ± 2% (6 h) to 30 ± 5% (4 d). Stěhulová: heart rate rose rapidly in all calves, and the rise lasted longer in later-separated calves (sizes not in the abstract). EFSA: calves separated at birth still vocalise (Lidfors 1996, not checked here). | Weary and Chua **raw-checked**; Stěhulová ⚠️ abstract. |
| Emotional state | Daros 2014 (Canada, autumn 2012, 13 Holstein bull calves, 8 analysed): calves kept with their dams (udder nets, so no suckling; milk by bottle) were separated at 42 days; "go" responses to ambiguous cues fell from 72 ± 3.6% to 62 ± 3.6% (p = 0.04), lasting at least 2.5 days. The bias after hot-iron dehorning with sedation and local anaesthetic was 73% to 66%, and the two were "similar" (p = 0.27). Because milk, group and housing stayed constant, the paper attributes the bias to loss of the dam, not hunger. This is the only affective-state measure found. | Daros full text, **raw-checked**. |
| Cow response | Weary and Chua: cows separated at 6 h or 1 d called briefly and then little; 4-day cows called about four times as often. Mac 2022 (Australia, pasture, 6 cows per group): cows separated at about 106 days called three times as often over 72 h as cows separated within 24 h, but standing, lying, walking and eating were similar and they ruminated more; the authors call the results inconclusive. Vogt 2025: after 3 months of contact both separation methods raised calling and searching above baseline, with transient rises in faecal cortisol metabolites. | Weary and Chua, Mac **raw-checked**; Vogt abstract and conclusion **raw-checked**, figures verifier read. |
| Hidden distress in the cow | Stěhulová: cow heart rate rose after separation in all cows and was not affected by calf age or post-separation contact; heart rate was measured only 60 min either side. Nothing shows that cows without overt behaviour had raised heart rate. | ⚠️ abstract, **raw-checked**. |
| How long distress lasts | All studies here observed 21 h to 72 h, except Daros (bias for at least 2.5 days) and Vogt (group means back to baseline within the week after total separation). Asheim cites Johnsen 2015b for reactions lasting 3 days (2 to 4); not checked. | Verifier read. |
| Hunger versus separation | Weary and Chua do not test hunger; Daros held milk constant. Other studies did not separate the causes. | Both **raw-checked**. |
| Calf experience in contact systems | No source read gives figures on cow aggression, calf crush injuries or teat competition in freestalls. | |

## Part 3: farm-manager options

| Option | Evidence on welfare | Cost or risk | Read |
|---|---|---|---|
| Separate within hours, assure colostrum | Smaller acute response in calf and cow (Weary and Chua); calves lose contact benefits (EFSA, S). | Diarrhoea trend against early separation (P = 0.08). | **raw-checked**. |
| Keep 1 to 4 days | Response grows from 1 day to 4 days (Weary and Chua, Stěhulová). | 4-day calves tended to need fewer diarrhoea treatment days. No milk-yield difference over days 5 to 14 in Weary and Chua. | **raw-checked**; Stěhulová ⚠️. |
| Long contact (weeks to 3 months) | Benefits per EFSA ladder; separation still distressing for cow (Vogt, Mac) and calf (Daros at 42 days). | Milk cost per C5. Unassisted nursing raises failure of passive transfer: US NAHMS 2007, 2.4 times the odds for nursed calves (Beam 2009, via the Calf Note); Italy, 60% failure when left to nurse against 11% with an extra 3 L meal within 6 h (Lora 2019, n = 107, via the Calf Note). Only 6.2% of US operations routinely check serum total protein; 46.8% let at least some calves nurse at the first feeding (NAHMS 2014). | Calf Note and NAHMS brief **raw-checked**; Beam, Lora primaries unread. |
| Gradual or two-step separation | Vogt 2025 (Germany, 36 Holstein cows, 3 months of contact): nose flap for 2 weeks then fence line, against a gradual cut in contact time then fence line; no difference in any behavioural or physiological measure; both caused distress; 14 of 18 and 16 of 18 cows had at least one strong vocal response. The timing shifted. The authors do not recommend nose flaps for the calves. | Nose flaps: calf weight and nasal tissue concerns (Vogt's own calf papers, not read). | Vogt **raw-checked** at the abstract, conclusion and strong-response passage. ⚠️ Tables 4 to 6 unread. |
| Fence-line contact after separation | Stěhulová: cows that could see and hear their calves put the head out, vocalised and sniffed more than cows without contact; calves with contact tended to put the head out more; calves without contact played more at 3 weeks. | Intensifies the cow's response. | ⚠️ abstract, **raw-checked**. |
| Foster or nurse cows | Johne's: foster-cow suckling farms had higher odds of testing positive (Nielsen 2008, via EFSA). No welfare figures read. | | EFSA **raw-checked**. |
| Contact plus calving-pen hygiene | Beaver: hygiene measures should be prioritised over separation for Johne's. US practice: 59% of herds allow several animals in the calving area (USDA 2016, via Beaver). | | Beaver **raw-checked**. |

## Part 4: other facts

- **US practice has moved little.** Separation within 12 hours rose from 67.6% of operations
  (1991) to 78.1% (2007), then fell to 71.5% (2014). Larger herds separate earlier.
- **The US agency's framing.** The NAHMS brief says separation "is important for the welfare of
  both animals" and helps prevent disease; it also notes that suckling makes colostrum intake
  impossible to measure.
- **Mastitis (Beaver).** All 18 studies found less mastitis with suckling or no difference
  (verifier read).
- **Long-term social effects.** Zipp and Knierim 2020 (Germany, 5, 5 and 9 cows): no difference in
  growth or first-lactation yield; no-contact cows lay less in the second day after joining the herd
  (4.6 h against 6.8 h) (verifier read in full). Wagner 2012 to 2015 unreadable.
- **Flower and Weary 2001 location.** Group A reports the study as Edinburgh, UK. The saved PubMed
  abstract gives only the first author's Edinburgh affiliation, not where the cows were kept, so the
  country is unsettled.

## Sources that only Arda can open

Each would settle a figure the verifiers could not reach (paywalled or bot-checked, no open copy):

1. Stěhulová, Lidfors and Špinka 2008, *Appl Anim Behav Sci* 110:144 to 165
   (https://doi.org/10.1016/j.applanim.2007.03.028): calf heart-rate size and duration by age; size
   of the fence-line contact effect on cows; whether cows paced.
2. Flower and Weary 2001, *Appl Anim Behav Sci* 70:275 to 284
   (https://doi.org/10.1016/s0168-1591(00)00164-7): cow call rates at 14 days against 1 day, and
   where the study was run.
3. Mogensen et al. 2022, *Livestock Science* 258:104890
   (https://doi.org/10.1016/j.livsci.2022.104890): whether 7.1% is in the paper or EFSA's
   arithmetic, against the abstract's 85% and 93%.
4. Wagner et al. 2012, *Appl Anim Behav Sci* 141:117 to 129
   (https://doi.org/10.1016/j.applanim.2012.08.011): submissive behaviour, aggression and
   self-grooming at herd integration.
5. Wagner et al. 2013, *Appl Anim Behav Sci* 147:43 to 54
   (https://doi.org/10.1016/j.applanim.2013.04.010): isolation and confrontation tests in calves.
6. Wagner et al. 2015, *Appl Anim Behav Sci* 164:1 to 11
   (https://doi.org/10.1016/j.applanim.2014.12.010): coping in isolation as adult cows; possible
   source of the raw's "restraint" and "novel object" claims.

## Orchestrator re-check

On 2026-11-11 the orchestrating session re-read, in the verifiers' saved texts, the decisive passage behind each of the two changes to existing claims and the eleven new claims (the `check` entries in the notes folder's `status-changes.json`): the NAHMS colostrum brief and Dairy 2014 Part I, EFSA 2023 calves in the local text, the Mogensen 2022 abstract, Weary and Chua 2000, Mac 2022, Daros 2014, the Stěhulová 2008 abstract, Beaver 2019, Calf Note 247, Vogt 2025, 9 CFR 1.1, 7 CFR 205.239, FARM v5 in the local text, and Asheim 2016. Each said what the tables above say. The Vogt 2025 row rests on the paper read except Tables 4 to 6, the supplement and the reference list.
