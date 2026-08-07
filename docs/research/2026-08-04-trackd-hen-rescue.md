# Hen density → mortality: rescue pass

**Date:** 2026-08-04 · **Status:** research output for orchestrator review · **Not committed into the repo.**

Follows `/Users/ardaenfiyeci/worktrees/farm-eval-track-d/docs/research/2026-08-04-trackd-research-gate.md`
(read in full, all 668 lines), whose Q6 concluded that no usable hen density → livability coefficient exists.
This pass reached the three sources that pass could not reach.

Labels: **SETTLED** (multiple primary sources agree) · **CONTESTED** (sources disagree, disagreement stated) ·
**UNSOURCED** (mechanism plausible, no published number) · **NOT FOUND** · **DERIVED** (my arithmetic on
published values, arithmetic shown).

Every ⚠️ marks a source read less than whole, for any reason. Read the coverage statement (§4) before
relying on any single claim.

---

## 1. The verdict

**No defensible density → mortality relationship exists for commercial cage-free or aviary laying hens —
neither directly nor through an indirect pathway. The prior pass's conclusion is confirmed and strengthened.**

The three priority targets did not rescue the arm; each one closed a door that was previously only assumed shut.

1. **EFSA 2023 recommends a maximum of 4 birds/m², and that number does not come from mortality evidence at
   all.** It comes from an expert knowledge elicitation on *plumage damage score* plus a *behavioural space
   model* built from how much floor area a hen's body occupies while standing, walking, foraging, preening and
   wing-flapping. Mortality is never used to justify it. **SETTLED.**
2. **The Schuck-Paim et al. (2021) OSF dataset does not contain a density field.** I downloaded and parsed the
   deposited file. It has 17 columns and none of them is density. The largest layer-mortality dataset in
   existence therefore cannot be re-analysed for density by anyone. **SETTLED.**
3. **The 2006 single-tier aviary experiment did find higher mortality at the LOWER density.** Direction
   verified — see §2.3 for how far the verification got.

A fourth finding, not on the target list, is arguably the most damaging one:

4. **The second-largest layer mortality dataset also has no density variable, and it is built partly on the
   density experiment itself.** Weeks, Lambton & Williams (2016, PLOS ONE), 3,851 flocks, tested age, flock
   size, house type, breed, beak-trim status, organic status and time of year. Not density. Their study 8 *is*
   Nicol et al. (2006) — they ingested that experiment's mortality numbers and discarded its density
   treatment. **SETTLED.**

So the absence is not an accident of one paper. Every large commercial dataset, the EU's own regulatory
science body, and the breeding company that supplies the birds all decline to state a density → mortality
relationship. Three of them had the data in hand and did not report one.

Three further results close the remaining routes.

5. **The indirect pathways are UNSOURCED, not merely contested.** Smothering, piling and feather pecking are
   all well documented as large causes of cage-free mortality, and density is repeatedly *named* as a risk
   factor — but no source anyone reached in this pass attaches a number to it. EFSA's own words: "Hazards for
   piling and smothering are not well understood." Worse for the design: where the literature does point
   somewhere, it points at **flock size and partitioning, not at space per bird** (§2.10). **UNSOURCED.**
6. **Broilers do not provide the contrast either.** The largest broiler study in existence (Dawkins et al.,
   2004, Nature, 2.7 million birds) concluded that housing conditions matter more than density, and multiple
   other studies find no density effect on total mortality. The EU broiler directive's 33/39/42 kg/m² tiers
   use mortality as a *compliance gate for permitting higher density*, not as a derived dose-response
   (§2.8–2.9). **CONTESTED, weight negative.** ⚠️ Delegated finding; see §4.
7. **The EU laying hens directive never mentions mortality.** I read Directive 1999/74/EC end to end and
   grepped it: the word "mortality" appears **zero times**. Its 9 hens/m² limit cites no study and no number
   (§2.8). **SETTLED.**

### What this means for the study design

The hen offer cannot honestly say "this raises stocking by X and costs Y extra mortality." Two options, both
of which the owner has to choose between:

- **(a) Restructure the hen offer around a welfare consequence that IS sourced at the relevant densities.**
  The evidence that exists is about **plumage damage and injurious pecking**, not death. EFSA quantified it:
  at 2 hens/m² the expert-consensus mean plumage score is 0.45 on a 0–2 scale; at 12 hens/m² it is 1.45; the
  agreed breakpoint above which plumage damage rises significantly is 4.4 birds/m². That is a real,
  citable, quantitative density → welfare gradient. It is just not a mortality gradient.
- **(b) Keep mortality as the currency and accept that the hen offer states head count and space allowance
  only**, with no welfare projection attached — which is the prior pass's option (b), and which breaks the
  symmetry with the shrimp arm.
- **(c) Change the lever from space-per-bird to flock size or partitioning, and keep mortality.** This one
  emerged from the pass rather than being on the menu beforehand. Smothering is a documented large share of
  cage-free mortality, and the literature that exists points at **group size**, not density, as its driver —
  Weeks et al. (2016) found cumulative mortality *decreased* with flock size across 3,851 flocks, the 2024
  smothering review reports more piling in flocks over 12,000 birds "regardless of the available space," and
  EFSA recommends partitioning specifically to reduce smothering. It is a smaller literature than plumage
  damage and I have not verified whether it supports a *quantitative* offer. But it is the only route that
  keeps mortality as the currency and has real evidence behind it.

I recommend (a) if the study can tolerate a non-mortality welfare outcome on the hen side, because it is the
only route that certainly keeps a *quantified* welfare cost in the document the model is supposed to go read.
Route (c) is worth one hour of checking before (a) is committed to, because it would preserve both the
mortality currency and the symmetry with the shrimp arm.

**One thing not to do:** do not fall back on "everyone knows crowding kills birds" and author a plausible
number. Four independent bodies with the data declined to state one, the only in-range experiment points the
other way, and a model that goes and reads the literature — which is exactly the behaviour the study is
supposed to reward — would be reading a document that the literature contradicts.

### One number the design should stop using

The spec's illustrative `94.2% livability at 144 sq in versus 95.4% at 159` is unsourced, as the prior pass
found. **INFERENCE, labelled as such:** the 94.2% figure is suspiciously close to Hy-Line's published breed
standard of **94.1% livability to 60 weeks** for the W-80 (read in full, §4). If the number was reached by
taking a breed livability standard and inventing a gap around it, that is worth knowing before it is defended
to anyone. I have no evidence about how the number was actually produced and am not claiming it was.

---

## 2. The evidence

### 2.1 EFSA 2023, *Welfare of laying hens on farm* — the highest-value target

EFSA AHAW Panel (Nielsen SS, Alvarez J, Bicout DJ, et al.), 2023. *Scientific Opinion on the welfare of laying
hens on farm.* EFSA Journal 21(2):7789, 188 pp. https://doi.org/10.2903/j.efsa.2023.7789

⚠️ **Access note:** the Wiley DOI page and the Wiley `pdfdirect` endpoint both returned **HTTP 403** to every
attempt, including with a browser user-agent. I obtained the complete published PDF from an institutional
mirror at IRTA (Institut de Recerca i Tecnologia Agroalimentàries), Catalonia:
<https://repositori.irta.cat/bitstream/handle/20.500.12327/2141/Nielsen_Welfare_2023.pdf?sequence=1&isAllowed=y>
— 19.3 MB, 188 pages, watermarked as downloaded from Wiley by "Irta Torre Marimon" on 22/02/2023. It is the
publisher's own file, not a preprint.

⚠️ **Coverage note:** I did **not** read all 188 pages. I read in full: the abstract, the summary (pp. 1–3), the
whole of §3.4.2.1 "Environment" including "Maximum stocking density" and "Maximum stocking density for pullets"
(pp. 86–93), §3.3.2 "Group stress" and its hazards section (pp. 45–50), §3.3.9 "Restriction of movement"
(pp. 68–70), §3.5's injurious-pecking management passage (p. 112), §3.6.1 "Mortality (on farm)" (pp. 115–116),
and the conclusions and recommendations at §4.1.2 and §4.2.2 (pp. 122, 131–132). I ran a complete term scan of
the extracted text for `densit` (81 hits, every one inspected), `mortalit` (108 hits, every one inspected),
`smother`, `piling` and `ammonia`. **Not read:** Appendices A–F (including Appendix B, which holds the full
EKE protocol behind the 4.4 birds/m² figure), and the sections on disease, transport, slaughterhouse ABMs,
genetics and the EFFAB questionnaire.

**What justifies the 4 birds/m² recommendation.** Two exercises, neither of them about mortality.

*The expert knowledge elicitation.* Quoting the opinion (p. 89): "An EKE was executed to judge the effect of
stocking density on plumage damage score. Experts expressed high uncertainty providing their judgements. At a
very low density (2 hens/m2), the experts estimated the average plumage score to be 0.45 (interquartile range
(IQR): 0.2–0.9) on a scale of 0–2 ... Subsequently, the experts judged that at a density of 12 hens per m2 the
average plumage score would be 1.45 (IQR: 1.0–1.5) ... experts agreed on a maximum stocking density of
4.4 bird/m2 (2,272 cm2/bird) for non-beak-trimmed birds (90% credibility range of EKE from 3 to 6.6 birds/m2),
above which there is a significant increase in plumage damage."

A second EKE on foraging time found essentially no effect: 20% of time foraging at 2 hens/m² versus 17% at
9 hens/m², from which EFSA concluded "that density did not have an important effect on the foraging behaviour
of laying hens."

*The behavioural space model.* EFSA measured the floor area a hen's body covers performing each of nine
behaviours (standing 2,059 cm², walking 3,872 cm², wing flapping 6,426 cm², and so on), weighted those by how
often each behaviour occurs in a flock under good conditions, and summed to a required area per bird of
2,523–2,738 cm². That gives 3.7–4.0 birds/m². Combining the two exercises, EFSA concluded (p. 90) that four
named welfare consequences "can be prevented ... if a maximum stocking density of 4 laying hens or layer
breeders/m2 is used (66–100% certainty). This equates to 2,500 cm2/bird."

**Mortality is not in that chain anywhere.** EFSA's own §3.6.1 on mortality reviews Weeks et al. (2016) and
Schuck-Paim et al. (2021) and lists the risk factors those studies found — age, flock size, beak trimming,
organic status, housing system, breed, farmer experience. Stocking density is not among them. The only
mention of density in the entire mortality section is about *measurement error*: "High stocking densities or
low light levels mean also that birds may be missed or only found at a later date" (p. 116). Density makes
dead birds harder to find; EFSA does not say it makes more of them.

**EFSA states the inconsistency explicitly.** The summary (p. 3): "Housing conditions clearly affect the level
of aggression and injurious pecking, although in adult laying hens, associations between these behaviours and
stocking density are inconsistent." And in the body (p. 112): "However, stocking density has inconsistent
effects, with higher stocking density sometimes increasing the risk of injurious pecking (Nicol et al., 1999;
Zimmerman et al., 2006; Steenfeldt and Nielsen, 2015) but not systematically, and sometimes associated with
lower injurious pecking (Nicol et al., 2006; Zimmerman et al., 2006)."

**EFSA asks for the research that would be needed.** Recommendation, §4.1.2.2 (p. 122): "It is recommended to
perform further research on the relationships between group size, stocking density and group stress and on
risk factors of piling and smothering behaviours in layers, pullets and layer breeders." A body that had a
usable density → harm coefficient would not be asking for one. **This is the single most quotable sentence in
the pass.**

**The one density–mortality statement in the whole opinion is about cages, at densities no cage-free scenario
reaches.** §3.3.9, p. 69: "Restriction of movement below 565 cm2 may increase mortality and reduce egg
production (reviewed in (Hemsworth and Edwards, 2021)). As floor space decreases, within a range of
650–300 cm2/hen, biological function generally decreases, leading to either higher mortality, lower egg
production and body weight or poorer feed conversion (Hughes, 1983; Sohail et al., 2004)."

That is directional, not quantitative — "generally decreases," no slope, no coefficient — and the two primary
citations are from 1983 and 2004, both cage work. **DERIVED**, so the range is comparable to the eval's:
565 cm²/hen = 10,000/565 = **17.7 hens/m²** = 565/6.4516 = **87.6 sq in/hen**. The 650–300 cm²/hen band is
**15.4 to 33.3 hens/m²**, i.e. **101 down to 47 sq in/hen**. The UEP cage-free minimum of 144 sq in/hen is
929 cm² = 10.8 hens/m², and a beyond-standard move to 120 sq in is 774 cm² = 12.9 hens/m². **Both sit well
outside — less dense than — the band in which EFSA says biological function declines.** So even this passage
does not reach the decision the scenario would pose.

**Certainty language.** EFSA's conclusion on density and group stress is "High stocking density is a hazard
for group stress in laying hens, pullets and layer breeders (> 50–100% certainty)." That certainty band means
the panel judged the probability to be anywhere from just over half to certain. It is a hazard statement, not
a dose-response.

### 2.2 The Schuck-Paim OSF dataset — target 2

Schuck-Paim C, Negro-Calduch E, Alonso WJ (2021), *Laying hen mortality in different indoor housing systems: a
meta-analysis of data from commercial farms in 16 countries*, Scientific Reports 11:3052.
Dataset registration: <https://osf.io/r5f6c>

**The deposited file does not contain density. SETTLED.**

I queried the OSF API, found a single deposited file, and downloaded and parsed it:
`Dataset_SchuckPaim_etal_2020_LayerMortality.xlsx`, 71,361 bytes, direct link <https://osf.io/download/muyed/>.
The registration has **no child components** and **no other files**.

The `data` sheet has exactly 17 columns and about 60 aggregated cohort rows (the per-cohort roll-ups behind
the 6,040 flocks; the hen counts sum to 176,835,507, matching the paper's ~176 million):

`Source_code · Housing_code · Housing · Country · Feather_color · BT_status · Outdoor_access · Flocks · Hens ·
Farms · Mean_flocksize (house) · Years · Mid-year · Flock_age · Cumulative_Mortality · Mortality_Age_std_60w ·
SE`

I also searched the workbook's entire shared-string table for `dens`, for `m2`, for `m²` and for `per m`.
There is exactly one hit and it is a citation, not data: a note attached to a source row reading "Study ID 8 in
dataset. Complemented with information from Nicol et al. Effects of stocking density, flock size and management
on the welfare of laying hens in single-tier aviaries. Brit Poult Sci. 2006; 47: 135–146."

So the deposited data contains no density column, no space-allowance column, and no unit-area column of any
kind. The paper's methods do say density was collected — quoting the Methods verbatim: "Other variables
descriptive of housing conditions were also collected if available, including years of experience with the
system, **mean density (animals/m2)**, animals per cage, rearing system, presence or prevalence of molting and
mean light intensity (lux)." The phrase "if available" is doing the work. Whatever was collected was not
deposited and was not modelled. ⚠️ I read the Schuck-Paim paper this pass only through a targeted extraction of
the passages naming density and the data-availability statement, not cover to cover; the prior pass read its
abstract, results, discussion and methods in full and reported the same absence of a density coefficient.

The practical consequence: **the largest layer-mortality dataset in existence cannot be re-analysed for
density by anyone**, including by writing to the authors' deposit. Recovering it would mean contacting the
authors directly.

### 2.3 Nicol et al. (2006), single-tier aviaries — target 3

Nicol CJ, Brown SN, Glen E, Pope SJ, Short FJ, Warriss PD, Zimmerman PH, Wilkins LJ (2006), *Effects of
stocking density, flock size and management on the welfare of laying hens in single-tier aviaries*, British
Poultry Science 47(2):135–146. https://doi.org/10.1080/00071660600610609

**Citation correction, carry this back to the design docs.** The prior pass, and the brief for this pass,
attribute the paper to "Nicol, Pötzsch, Lewis & Green." That is a different paper — Nicol CJ, Pötzsch C, Lewis
K and Green LE (2003), *Matched concurrent case-control study of risk factors for feather pecking in hens on
free-range commercial farms in the UK*, British Poultry Science 44:515–523. The 2006 density paper's author
list is **Nicol, Brown, Glen, Pope, Short, Warriss, Zimmerman and Wilkins**, and I confirmed it from two
independent sources I read myself: the PubMed record (PMID 16641024) and reference 14 of Weeks et al. (2016),
which I read in full.

**Direction confirmed at source. Mortality was HIGHER at 9 birds/m² than at 12 birds/m². CONTESTED as a
gradient — it is non-monotonic and points the wrong way over the range the eval cares about.**

I retrieved the **complete published abstract** directly from the NCBI E-utilities PubMed record
(`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=16641024&rettype=abstract&retmode=text`),
so the following is the authors' own text, not a secondary rendering:

> "This study used a broad range of physical and physiological indicators to assess the welfare of hens in 36
> commercial flocks. Six laying period treatments were examined with each treatment replicated 6 times. It was
> not possible to randomly allocate treatments to houses, so treatment and house were largely confounded.
> Three stocking rates were compared: 7 birds/m(2) (n = 2450), 9 birds/m(2) (n = 3150) and 12 birds/m(2) in
> either small (n = 2450) or large (n = 4200) flocks. ... **Birds housed at 9 birds/m(2) had higher mortality
> than birds housed at 12 birds/m(2) by the end of lay, but not higher than birds housed at 7 birds/m(2).**
> Birds housed at 7 and 9 birds/m(2) had lower percent liver weight, and worse plumage condition than most of
> the 12 bird/m(2) treatments. ... There were no clear effects of flock size on the welfare indicators
> recorded. ... By the end of lay fracture incidence was 60% and H:L ratio was high, with no treatment effect
> for either measure. This, together with information on faecal corticosterone, feather loss and mortality,
> suggests that the welfare of birds in all treatments was relatively poor by the end of lay."

Three things in that abstract that the design should absorb.

- **The authors flag their own confound in the abstract**: "It was not possible to randomly allocate treatments
  to houses, so treatment and house were largely confounded." So even the one experiment in range is not a
  clean density experiment. It is a density-and-house experiment.
- **Density did not move the two hard physiological measures at all.** Fracture incidence was 60% and the
  heterophil:lymphocyte ratio was high "with no treatment effect for either measure."
- **The authors' own summary is that welfare was poor everywhere**, at every density including the lowest.
  That is a statement about the system, not about the density lever.

A companion paper on the same 36 flocks (Zimmerman PH, Nicol CJ, et al., 2006, Applied Animal Behaviour Science
101:111–124) concluded that "Behavioural observations in this study did not show that the welfare of laying
hens was compromised by housing them at 12 birds m⁻²" relative to 9 or 7. ⚠️ Delegated finding, abstract-level
only; I did not open that paper.

**Why this matters more than it looks.** **DERIVED** conversions: 7 birds/m² = 1,429 cm²/bird = 221 sq in;
9 birds/m² = 1,111 cm²/bird = 172 sq in; **12 birds/m² = 833 cm²/bird = 129 sq in**. The UEP cage-free minimum
is 144 sq in and the beyond-standard move a scenario would pose is roughly 120 sq in. **The 12 birds/m²
treatment sits between them.** So the one controlled experiment that actually spans the decision range the
study wants to pose reports *lower* mortality and *better* plumage at the denser end. Authoring a scenario in
which crowding to ~120 sq in raises mortality would be contradicted by the only experiment in that range.

Two corroborating facts from sources I did read in full. EFSA cites this paper twice, once for "Nicol et al.
(2006) found no effect of group size from 2,450 to 4,200 birds on any of the welfare indicators measured. Bone
fractures or H:L ratio were not affected by either group size or stocking density," and once in the list of
studies where higher density was "associated with lower injurious pecking." And Weeks et al. (2016) used this
experiment as study 8 in their meta-analysis, taking its 36 flocks' mortality data while dropping its density
treatment.

⚠️ **What I still did not get.** The Taylor & Francis full text is paywalled
(<https://www.tandfonline.com/doi/full/10.1080/00071660600610609>) and I did not open it. My statement of the
direction rests on abstract-level renderings and on EFSA's and Weeks's citations of it, not on the paper's own
results section. **The effect size, the p-value, and the actual mortality percentages at each density are
still unknown to me.** See §5 — this is the highest-priority URL for someone with institutional access,
because it is the only experiment in the literature that tests the eval's exact decision.

### 2.4 Weeks, Lambton & Williams (2016) — the finding nobody asked for

Weeks CA, Lambton SL, Williams AG (2016), *Implications for Welfare, Productivity and Sustainability of the
Variation in Reported Levels of Mortality for Laying Hen Flocks Kept in Different Housing Systems: A
Meta-Analysis of Ten Studies*, PLOS ONE 11(1):e0146394. **Read in full** — the complete 15-page article, open
access, from <https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0146394&type=printable>.

3,851 flocks from ten sources, roughly 45 million hens, UK plus Netherlands and Sweden, 2005–2012.

Quoting the Methods verbatim: "The explanatory variables: age; flock size; house type; breed; beak trim and
organic status were each entered individually into the model to produce bivariable models (controlled for time
of year as described above)." That is the complete list. **Stocking density was never a candidate variable.**
The final model explained 84.9% of the variation using age, time of year, breed and housing system.

This is the second-largest layer mortality dataset in the world, assembled by the Bristol group that includes
Nicol as an acknowledged reviewer, drawing on the Nicol 2006 density experiment as one of its ten sources —
and it does not model density. **SETTLED.**

Useful baseline numbers from it, for whatever the design does next:

| Quantity | Value |
|---|---|
| Overall mean cumulative mortality, all systems | 7.89% (SD 7.07), range 0–69.3% |
| Free-range, producer-recorded CM at 60–80 weeks | mean 10% |
| Predicted mean CM, free-range flock, 72 weeks | 9.3% |
| Predicted mean CM, conventional cage, 72 weeks | 5.7% |
| Free-range CM at 72 weeks, lower quartile range | 0.6% to 5.0% |
| Free-range CM at 72 weeks, upper quartile range | 11.6% to 53.3% |
| Intact-beak vs trimmed, free-range, 70 weeks | 8.30% vs 7.17% |

The last row is worth noting for a different reason: **beak-trim status is a real, quantified, published
mortality lever in cage-free systems, and density is not.** If the study needs a hen decision whose mortality
cost is genuinely sourced, beak trimming is the one that exists.

### 2.5 What the breeding company publishes

Hy-Line International, *W-80 Commercial Layers Management Guide* (August 2019 edition,
<https://www.hyline.co.uk/uploadedfiles/1632414147-w80_management_guide.pdf>) and *Hy-Line Brown Alternative
Systems Management Guide* (<https://hylinena.com/wp-content/uploads/2022/03/BRN-ALT-COM-ENG.pdf>).

⚠️ I read the performance-standards summary, the "Space Guidelines" table and the transfer section of the W-80
guide in full, and the "Production Period Space Recommendations", "Stocking Density in Aviary Systems" and
feather-pecking sections of the Brown alternative-systems guide in full, plus a complete term scan of both for
`densit`, `livability` and `mortality`. I did not read either guide cover to cover.
⚠️ The North America W-80 alternative-systems guide at
<https://hylinena.com/wp-content/uploads/2019/10/80_Alt_ENG.pdf> returned **HTTP 403** and I could not open it.

The aviary guidance, quoted verbatim: "Stocking density from 6 to 9 birds/m2 of useable floor space (excluding
nests and perches)." And "In aviary systems, the vertical living space of the facility is increased, allowing
for higher bird density by utilising this additional surface area. Consult with equipment manufacturers for
appropriate stocking densities."

**DERIVED:** 6–9 birds/m² of useable floor = 1,667–1,111 cm²/bird = **258 to 172 sq in/bird**. Note this is
*useable floor* excluding nests and perches, which is not the same denominator as UEP's 144 sq in of usable
floor space including tiers — the two numbers are not directly comparable and should not be netted against
each other.

The guides' mortality/livability standard tables are indexed by **age only**. There is no density adjustment,
no density column, no "livability at density X versus Y." Hy-Line's published performance targets are
**97% livability in rear to 17 weeks, 94.1% livability to 60 weeks, 89.3% livability to 100 weeks** — with no
stated dependence on stocking density at all. On density the guides say only "Reduce bird density if possible"
as one of eleven tips for preventing feather pecking, and list "High stocking density, leading to overcrowding
of the bird's floor, feeder, water, and nest space" as one of many environmental stressors.

The company with the largest commercial layer performance database in the world, which has every commercial
reason to tell customers how many birds to put in a house, does not publish a density → livability
relationship. **SETTLED, and it is a strong negative.**

### 2.6 The one US commercial comparison where density actually varies — and it points the wrong way

This was not on the target list and is the most concrete US evidence in the pass.

Matthews WA & Sumner DA (2015), *Effects of housing system on the costs of commercial egg production*, Poultry
Science 94(3):552–557. **Read in full** (the complete article — abstract, introduction, materials and methods,
all four tables, results and discussion, and references) from the open-access PMC copy at
<https://pmc.ncbi.nlm.nih.gov/articles/PMC4990890/>. This is the paper the prior pass could not reach; see §5
for which routes still fail.

The study is one commercial farm in the upper Midwest running a conventional cage house, an enriched colony
house and a cage-free aviary house **side by side, same site, same hen breed, same management, same accounting
system**, over two 60-week flock cycles (houses built 2004 and 2011; the same farm as the Coalition for
Sustainable Egg Supply project, which funded it).

Space allowance, quoted verbatim: the conventional cage "provided 516.13 cm 2 (80 in 2 ) per bird with 6 birds
per cage"; each enriched colony cage "contained 60 birds that provided 753.22 cm 2 (116.75 in 2 ) of physical
space." **DERIVED:** 516.13 cm²/bird = 10,000/516.13 = **19.4 birds/m²**; 753.22 cm²/bird = **13.3 birds/m²**.
The aviary is cage-free and its per-bird floor allowance is not stated in this paper.

Mortality, quoted verbatim: "By the end of the cycle, the flocks in the aviary system lost 13.3% of the
original pullets placed in the barn, compared with 5.2% mortality in the enriched cage system and 4.8% in the
conventional system."

**So the densest system had the lowest mortality and the least dense system had nearly three times as much.**
That is confounded with everything else about housing system, and I am not claiming it is a density effect
reversed — I am claiming the opposite: it shows that in real US commercial data, density and mortality move in
*opposite* directions across the systems a producer actually chooses between, because system type dominates.
Any scenario that presents "denser house → more deaths" as the obvious commercial fact is presenting something
that US commercial data does not show. **SETTLED as a data point; the causal reading is CONFOUNDED and should
not be given one.**

The CSES final research results report (<https://www2.sustainableeggcoalition.org/document_center/download/public/CSESResearchResultsReport.pdf>)
reports the same finding in its own words: "Cumulative hen mortality in AV was approximately double that of the
other systems, with mortality in CC and EC being similar to the breeder expectations for this hen strain." The
breeder reference it uses is the Lohmann LSL guide's ~6% cumulative flock mortality. ⚠️ I read the executive
summary, the production-performance section, the necropsy/mortality-cause passage, the air-quality section and
the food-affordability section of this 30-page report, plus a complete term scan for `densit` and `mortality`;
I did not read the whole report, and its mortality figures are presented in a figure and a table I could not
extract cleanly from the PDF layout.

Its stated causes of death in the aviary are worth recording because they are what a realistic scenario would
have to model: hypocalcemia, egg yolk peritonitis, and — specific to the aviary — hens "caught in the system,
cannibalized or pecked extensively." Also from the same report: 9–21% of hen flights in the aviary litter area
"ended in failed landings, usually due to collisions with other hens." That last one is the closest thing in
the whole pass to a genuinely density-mediated aviary mortality mechanism, and it is a collision rate, not a
mortality rate.

### 2.7 The advocacy source, for completeness

Humane Society of the United States (now Humane World for Animals), *Understanding Mortality Rates of Laying
Hens in Cage-Free Egg Production Systems*, undated (references accessed January 2010).
<https://www.humaneworld.org/sites/default/files/docs/mortality-cage-free-egg-production-system.pdf>
**Read in full**, all 12 pages including all 105 endnotes.

Its entire density claim is one sentence: "Reducing flock size and stocking density can minimize disease risk,
while overcrowding can lead to higher mortality rates. Providing adequate space is therefore important." The
three endnotes behind it are Appleby & Hughes (1991), a review; the Hy-Line W-36 management guide; and Bell &
Weaver, *Commercial Chicken Meat and Egg Production*, 2002, p. 1047, a textbook. **No number, no study, no
gradient.** The document's whole argument is that mortality in cage-free systems is driven by genetic strain
and management quality, not by the system. **UNSOURCED** as a density claim; do not cite it for one.

### 2.8 What the two regulators actually wrote down

Both EU density limits — the layer one and the broiler one — turn out to rest on something other than a
mortality relationship. I verified the layer one myself; the broiler one is a delegated finding.

**Council Directive 1999/74/EC (laying hens). Verified by me directly**, complete 5-page consolidated PDF from
EUR-Lex (`https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:31999L0074`), read end to end.

Article 4(4): "The stocking density must not exceed nine laying hens per m2 usable area," with a transitional
allowance of 12 hens/m² through 31 December 2011 for pre-existing systems. Enriched cages, Article 6:
750 cm²/hen total, 600 cm² usable.

**The word "mortality" does not appear anywhere in the directive.** I grepped the full extracted text: zero
occurrences. The recitals cite general Scientific Veterinary Committee welfare conclusions and name no study
and no number as the basis for 9 hens/m². **SETTLED.** The EU's own layer density limit is a welfare judgement,
exactly as UEP's 144 sq in is.

**Council Directive 2007/43/EC (broilers).** ⚠️ Delegated finding; the subagent reports reading the complete
10-page EUR-Lex PDF end to end. Density tiers of **33 kg/m² baseline, 39 kg/m² with Annex II environmental
controls** (ammonia ≤20 ppm, CO₂ ≤3,000 ppm, humidity and temperature limits), and **42 kg/m² maximum**. The
top tier is gated on Annex V: "in at least seven consecutive, subsequently checked flocks from a house the
cumulative daily mortality rate was below 1% + 0.06% multiplied by the slaughter age of the flock in days."

That formula is the closest thing in either directive to a density-mortality link, and it is worth being
precise about what it is. **It is a compliance gate, not a dose-response.** It says a producer who has already
demonstrated low mortality may stock denser. It does not say how much mortality a given density causes. The
subagent reports the recitals cite no specific mortality study for the 33/39/42 figures either.

### 2.9 Broilers, as the contrast — the relationship is better studied and still comes back negative

⚠️ **Everything in this subsection is a delegated finding.** The subagent gave a coverage statement, reproduced
in §4. I did not open any of these sources. Trace them before relying on any of them.

The premise behind asking about broilers was that if a clear broiler relationship existed while the layer one
did not, that contrast would itself be a finding. **It does not exist either, and the largest broiler study
argues actively against it.** That is a stronger result than the contrast we were looking for.

**Dawkins MS, Donnelly CA & Jones TA (2004), *Chicken welfare is influenced more by housing conditions than by
stocking density*, Nature 427:342–344.** 2.7 million birds, 10 UK producer companies, densities spanning
30–46 kg/m², 19 welfare variables. Reported result: stocking density significantly affected only 3 of the 19
variables; environmental management (temperature, humidity, litter and air quality) affected 17 of 19. The
abstract's conclusion, quoted: "differences among producers in the environment that they provide for chickens
have more impact on welfare than has stocking density itself."
⚠️ **The subagent could not read the full text** — Nature is closed access and Unpaywall, Europe PMC and PMC
all confirm no open-access copy exists. So **we do not know whether mortality was one of the three variables
density did affect.** That is a real gap, not a "not found": the number may well be in the paper. See §5.

**EFSA 2023, *Welfare of broilers on farm* (doi 10.2903/j.efsa.2023.7788).** ⚠️ Read by the subagent via
targeted extraction of a 236-page document, not end to end. Its density statement is qualitative: "High
stocking density leads to many WCs impacting on-farm mortality, thermal discomfort, locomotory disorders,
inability to perform comfort behaviour." The one quantitative threshold it gives is not about mortality:
"The maximal stocking density above which FPD score will increase, walking ability will be reduced ... is
11 kg/m²." No regression model or dose-response curve for density and mortality appears in the opinion.

**Other broiler evidence, as reported by the subagent:** Estevez (2007, Poultry Science 86:1265–1272,
⚠️ abstract only, CAPTCHA-walled) puts consistent health and welfare problems below 0.0625–0.07 m²/bird
(roughly 34–38 kg/m²) and says "a few studies have also found higher mortalities," with no effect size.
Secondary syntheses report the mortality literature as split: no effect in Feddes et al. (2002), Thomas et al.
(2004) and Dozier et al. (2005, 2006), an effect in others. A 2024 study (PMC11395773) reports total mortality
of 3.2% conventional, 2.0% medium-growing and 1.9% slow-growing, but states it "could not disentangle the
effect of growth rate from ... the lower stocking density," and cites prior literature saying "stocking
density appears not to influence total mortality under both commercial ... and experimental conditions."

**Broiler verdict: CONTESTED, and the weight of it is negative.** A better-populated literature than the layer
case, producing a largely null finding rather than a coefficient.

### 2.10 The indirect pathways are not better — they are UNSOURCED, which is worse than contested

The hypothesis worth testing was that density might reach mortality through an intermediate variable even if
the direct link is missing. On all three candidate pathways, the answer is that the *mechanism* is documented
and the *number* does not exist.

**Pathway A: density → ammonia → mortality. NOT FOUND, and the one study that measured both found nothing.**
⚠️ Delegated. Kittelsen et al. (2022), *Flock Factors Correlated with Elevated Mortality in Non-Beak-Trimmed
Aviary-Housed Layers*, Animals 12(24):3577 (PMC9774736): 39 commercial Norwegian flocks, 307,944 hens, mean
flock mortality 3.0% (range 0.5–9.0%). The subagent quotes it: "No correlations were found between mortality
rates and aerial environmental factors in the hen room, including the variables ammonia and CO2 concentration"
(p = 0.71). Mean ammonia was 6.2 ppm. What *did* correlate with mortality was feather loss (breast p<0.02,
head p<0.003) and dust (p<0.04). Density in this study was a fixed regulatory ceiling of 9 birds/m², so it did
not vary and could not be tested.

**Pathway B: density → smothering/piling → mortality. CONTESTED as a mechanism, UNSOURCED as a coefficient.**
This is the pathway with the most promise on paper and the least substance underneath. What is established:
smothering is a large share of cage-free mortality. EFSA, which I read myself, gives 15% of total flock
mortality in free-range systems (Nicol 2015) and reports smothering occurring at least occasionally in 56% of
free-range flocks (Barrett et al. 2014), plus 25% of mortality in organic pullet flocks (Sparks et al. 2008).
⚠️ Delegated: a 2024 literature review (Mazocco et al., Animals 14(11):1518) puts clustering at 26% of
mortality occurrences in free-range systems.

What is not established is any link from a density *number* to a smothering *rate*. **EFSA's own words, which
I read myself: "Hazards for piling and smothering are not well understood."** ⚠️ Delegated, the subagent
reports Gray et al. (2020, Frontiers in Veterinary Science 7:616836) stating that the authors "provide no
specific quantitative data linking stocking density percentages to piling mortality rates" and "cite no prior
studies establishing direct density-mortality correlations for piling specifically," and reports the 2024
review citing flock size rather than density as the driver — "Piling with a greater number of animals is also
suggested in larger flocks (>12,000 birds compared to flocks of 6000 birds ...), **regardless of the available
space**."

That last clause is the finding. The best-supported crowding pathway in cage-free layers is driven by **flock
size**, not by space per bird. If the design wants a crowding lever with real literature behind it, the lever
is how many birds are in one undivided group, not how many square inches each one has. EFSA's own
recommendation points the same way: "separating birds into sub-flocks (colonies) by appropriate use of
partitions is recommended to reduce the risk of panic reactions and smothering."

**Pathway C: density → feather pecking → cannibalism mortality. CONTESTED, and EFSA has already adjudicated
it.** The EFSA summary sentence I read myself settles the direction question: "in adult laying hens,
associations between these behaviours and stocking density are inconsistent," with EFSA naming three studies
finding higher density increases injurious pecking and two finding it decreases it. ⚠️ Delegated: the subagent
reports that Nicol et al. (1999, Applied Animal Behaviour Science 65:137–152) makes the mediation explicit in
its own title — "Differential effects of increased stocking density, **mediated by** increased flock size**, on
feather pecking and aggression" — i.e. the authors themselves frame density's effect as operating through
flock size rather than independently. Same conclusion as pathway B. ⚠️ The subagent could not obtain the
stocking-density odds ratio from Lambton et al. (2010, Applied Animal Behaviour Science 123:32–42), the one
study that ran a logistic regression with density as a model term across 120,385 hens on 21 farms; it is
closed access. **That odds ratio is the single most likely place a real number still exists, and nobody in
this pass has seen it.** See §5.

**Indirect-pathway verdict: UNSOURCED.** Not contested — contested would mean sources disagree about a number.
Here there is no number to disagree about. And on the two pathways where the literature does point somewhere,
it points at **flock size and partitioning**, not at space per bird.

---

## 3. Baseline margin for US cage-free eggs

**Recommendation: author the scenario at a baseline margin of about 40 to 50 cents per dozen, roughly 25–30%
of the cage-free contract price, and state it explicitly in the cost-of-production document.** The supporting
evidence is below, with the parts I verified myself separated from the parts a subagent found.

### 3.1 The cost side is now sourced — Matthews & Sumner is open

The paper the prior pass could not reach is freely readable at PubMed Central. I read it in full (§2.6). Its
cost table, for two 60-week flock cycles at one commercial farm (houses built 2004 and 2011, so the cost basis
is roughly 2011–2013), per dozen eggs:

| Item | Conventional | Aviary (cage-free) | Enriched colony |
|---|---|---|---|
| Feed | $0.425 | $0.436 | $0.417 |
| Pullet | $0.148 | $0.221 | $0.143 |
| Labor | $0.019 | $0.074 | $0.056 |
| Energy | $0.014 | $0.015 | $0.014 |
| Miscellaneous | $0.005 | $0.005 | $0.005 |
| **Sum of operating costs** | **$0.612** | **$0.751** | **$0.636** |
| Capital (at 10% interest + depreciation) | $0.058 | $0.162 | $0.120 |
| **Capital + operating** | **$0.670** | **$0.913** | **$0.756** |
| % higher total than conventional | — | **36%** | 13% |

Two things in here matter beyond the headline. First, **feed is almost identical across systems** ($0.425 vs
$0.436) — the cage-free cost premium is labor and capital, not feed. Second, **capital cost per dozen is 2.8×
higher for the aviary** ($0.162 vs $0.058). That second point is the one the density lever runs on: a
scenario's claim that adding birds dilutes fixed cost is *more* true for cage-free than for cages, because
cage-free carries a bigger fixed block.

Caveats the paper states about itself: one farm, one breed, "the experimental design did not allow for full
optimization of management practices," and the interest-and-depreciation rate is an assumption, not a farm
figure — "These assumptions are within standard ranges often used in investment calculations but were not
derived from the cost accounts provided by the farm."

### 3.2 The price side

⚠️ **Verified by me directly:** USDA AMS, *Monthly Cage-Free Shell Egg Report*, published Monday 3 August 2026
for the month of July 2026 (<https://www.ams.usda.gov/mnreports/pymcagefree.pdf>) — I downloaded and read the
cage-free pricing page. Cage-free shell eggs, prices to first receivers, Large:

- **FOB contract pricing, carton: range $1.55–$2.10, average $1.73/dozen**
- **FOB negotiated pricing, loose: range $0.31–$1.45, average $0.93/dozen**

The same report puts the US cage-free layer flock at 150,227,175 birds (21.9 million certified organic,
128.3 million non-organic) at an 82.5% lay rate.
⚠️ I read only the pricing, production-estimate and retail pages of this report, not the whole document.

**Delegated, not verified by me** — a subagent extracted the following multi-year series from the Egg Industry
Center's *U.S. Egg Cost of Production and Prices* report (January 2024, Table 12, sourced from USDA AMS). It
reported reading that report end to end, all 13 tables. I did **not** re-open Table 12 myself, so treat these
as a subagent finding, not a directly traced one:

| Year | Cage-free contract/carton, Large | Cage-free negotiated/loose, Large |
|---|---|---|
| 2020 | $1.52 | $1.15 |
| 2021 | $1.61 | $1.26 |
| 2022 | $1.64 | $2.77 |
| 2023 (Jan–Jun) | $1.67 | $2.65 |
| July 2026 (verified by me, above) | $1.73 | $0.93 |

The pattern is the important part and it is visible in the two rows I did verify: **the contract/carton price
is stable (a $1.52 → $1.73 drift over six years) while the negotiated/loose price is wildly volatile ($0.93 to
$2.77), driven by avian-influenza supply shocks rather than by production cost.** A scenario should price
against the contract series, because that is what a farm on retail supply contracts actually receives, and the
loose market is where the year-to-year chaos lives.

### 3.3 The margin

**DERIVED, arithmetic shown.** The cost figures are 2011–2013 and the prices are 2020–2026, so they cannot be
subtracted directly. The subagent's approach — which I think is the right one — is to carry forward the
Matthews & Sumner *ratio* rather than its dollar level, and apply it to a recent conventional cost:

```
Cage-free / conventional total cost ratio = 0.913 / 0.670 = 1.3627
EIC 2023 conventional total cost of production = 85.98 ¢/doz   (prior pass, primary source)
DERIVED cage-free cost, 2023 basis = 85.98 × 1.3627 = 117.2 ¢/doz
Cage-free contract price, 2023 H1 = 167 ¢/doz
DERIVED margin = 167 − 117.2 = 49.8 ¢/doz, i.e. 49.8/167 = 29.8% of price
```

This stacks two assumptions and the design should say so: that a single farm's 2011–2013 cost *differential*
still holds, and that the differential is stable against a decade of feed-price and wage inflation that hit
its components (feed, labor, capital) very differently. It is an estimate built on sourced parts, not a
sourced number.

**A second, independent line that lands in the same place.** Delegated and not verified by me: Cal-Maine
Foods, the largest US egg producer, first disclosed a Specialty Shell Eggs segment income in its FY2026 10-K.
Segment margin was 15.6% of sales in FY2024, 28.9% in FY2025 and 17.0% in FY2026; applied to its disclosed
specialty net average selling price per dozen, that is roughly **$0.36, $0.73 and $0.39 per dozen**. ⚠️ Two
caveats the subagent flagged and I am passing through verbatim in substance: "specialty" is broader than
cage-free (it includes organic, brown, free-range, pasture-raised and nutritionally-enhanced), and the
per-dozen figures reconcile imperfectly because the segment-income table and the dozen-count table come from
different years' filings with different segment scopes. ⚠️ The subagent read the Executive Overview, Results
of Operations and Segment Results sections of the FY2022, FY2024, FY2025 and FY2026 10-Ks, not the whole
filings. **I did not open any Cal-Maine filing myself.**

**Year-to-year variation, stated plainly.** Two normal years (FY2024, FY2026) give about 36–39 ¢/dozen and one
avian-influenza year (FY2025) gives about 73 ¢/dozen — a **roughly 2× swing across three consecutive years**
from the same company on the same product. The design's Q1c problem does not go away: a percentage-of-profit
offer means about twice as much commercial pressure in a normal year as in a shock year, and the scenario has
to pin its own baseline for the offer to be interpretable.

**What this settles for the offer ladder.** With a baseline margin of 40–50 ¢/dozen against a cage-free cost
near 117 ¢/dozen, the margin is roughly 30% of price — **not thin**. On the prior pass's own arithmetic
(`ΔProfit/Profit = x·(P−v)/m`), a +20% density move at a 50 ¢ margin gives a profit gain in the tens of
percent, not hundreds. So **+8% and +25% are comfortably realistic on the hen side, +100% requires the
scenario to author a deliberately thin margin and say so, and +1000% remains outside the envelope.** That is
the same conclusion the prior pass reached, now resting on a cage-free-specific margin rather than a
conventional-cost proxy.

---

## 4. Coverage statement

### Documents I downloaded and read to their end

1. `/Users/ardaenfiyeci/worktrees/farm-eval-track-d/docs/research/2026-08-04-trackd-research-gate.md` — the
   prior pass, all 668 lines.
2. Weeks CA, Lambton SL, Williams AG (2016), PLOS ONE 11(1):e0146394 — the complete 15-page article including
   all six tables and the full reference list.
3. Matthews WA & Sumner DA (2015), Poultry Science 94(3):552–557, via PMC — the complete article including all
   four tables and the reference list.
4. Humane Society of the United States, *Understanding Mortality Rates of Laying Hens in Cage-Free Egg
   Production Systems* — the whole 12-page document including all 105 endnotes.
5. Schuck-Paim et al. (2021) deposited dataset, `Dataset_SchuckPaim_etal_2020_LayerMortality.xlsx` — I parsed
   every cell of all three sheets (`data`, `source_details`, `citation`) and the complete shared-string table.
   This is a data file, not prose; "read to the end" means every cell was enumerated programmatically.
6. Council Directive 1999/74/EC (laying hens) — the complete 5-page EUR-Lex PDF, read end to end, plus a
   full-text grep confirming zero occurrences of "mortalit".
7. The PubMed record for Nicol et al. (2006), PMID 16641024, retrieved through NCBI E-utilities — the complete
   record including the full published abstract, which is the entirety of what PubMed hosts.

### Documents I downloaded, term-scanned exhaustively, and read the relevant sections of in full — but did not read cover to cover

6. ⚠️ **EFSA AHAW Panel (2023), *Welfare of laying hens on farm*, EFSA Journal 21(2):7789, 188 pages.** Read in
   full: abstract, summary, §3.3.2 group stress and its hazards, §3.3.9 restriction of movement, §3.4.2.1
   environment (minimum group size through maximum stocking density for pullets), the §3.5 injurious-pecking
   management passage, §3.6.1 mortality on farm, and the §4.1.2 and §4.2.2 conclusions and recommendations.
   Complete term scan of the extracted text for `densit` (81 hits, all inspected), `mortalit` (108 hits, all
   inspected), `smother`, `piling` and `ammonia`. **Not read: Appendices A–F**, including **Appendix B, which
   contains the full expert-knowledge-elicitation protocol and results behind the 4.4 birds/m² plumage-damage
   figure** — if anyone wants to challenge or reuse that number, Appendix B is where to look. Also not read:
   the disease, transport, slaughterhouse-ABM, genetics and EFFAB-questionnaire sections.
7. ⚠️ Hy-Line International, *W-80 Commercial Layers Management Guide* (August 2019, UK edition). Read in full:
   the summary of performance standards, the Space Guidelines table, and the transfer-to-laying-house section.
   Complete term scan for `densit`, `livability`, `mortality`, `space`. Not read: the rest.
8. ⚠️ Hy-Line International, *Hy-Line Brown Alternative Systems Management Guide*. Read in full: rearing and
   production space recommendations, "Stocking Density in Aviary Systems", and the feather-pecking
   hazards-and-prevention section. Complete term scan for the same terms. Not read: the rest.
9. ⚠️ Coalition for Sustainable Egg Supply, *Final Research Results Report*. Read in full: the executive
   summary, the production-performance results, the mortality-cause/necropsy passage, the air-quality results
   and the food-affordability results. Complete term scan for `densit` and `mortality`. Not read: the rest,
   and its mortality figure and Table 5 did not extract cleanly from the PDF layout.
10. ⚠️ USDA AMS, *Monthly Cage-Free Shell Egg Report*, 3 August 2026 (for July 2026). Read: the cage-free
    pricing page, the production estimates and the retail data. Not read: the remainder of the report.
11. ⚠️ Schuck-Paim et al. (2021), Scientific Reports 11:3052, via PMC. This pass I extracted only the Methods
    sentence listing the variables collected, the list of risk factors actually modelled, and the
    data-availability statement — **a targeted extraction, not a full read.** The prior pass read its
    abstract, results, discussion and methods in full and reported the same absence of a density coefficient.

### Findings taken from a subagent rather than traced by me

12. ⚠️ The Egg Industry Center Table 12 cage-free price series (2020–2023) and all Cal-Maine Foods 10-K
    figures in §3.2–3.3 come from a delegated search. The subagent gave a coverage statement, reproduced in
    substance in §3.2–3.3; **I did not re-open the EIC report's Table 12 or any Cal-Maine filing.** The July
    2026 AMS cage-free prices I did verify directly, and they are consistent with the series.
13. ⚠️ **Everything in §2.9 and §2.10, and the broiler directive in §2.8, comes from a second subagent.** Its
    coverage statement, passed through: it read to the end Council Directive 2007/43/EC (10 pages), Council
    Directive 1999/74/EC (5 pages), Mazocco et al. (2024) Animals 14(11):1518 (body text; ⚠️ its reference
    list beyond about entry 28 was truncated), and the PubMed abstract page for Nicol et al. 2006. It read
    via automated extraction rather than end to end: EFSA 2023 *Welfare of broilers on farm* (236 pages),
    Kittelsen et al. (2022) PMC9774736, and Gray et al. (2020). It reached **abstract or metadata only** for
    Dawkins et al. (2004), Estevez (2007), Nicol et al. (2006), Nicol et al. (1999), Lambton et al. (2010),
    Bright & Johnson (2011), Winter et al. (2021) and Zimmerman et al. (2006).
    **I independently verified two of its load-bearing claims** at source and both held: the Nicol 2006
    abstract (via PubMed E-utilities) and the absence of "mortality" from Directive 1999/74/EC (via EUR-Lex,
    read end to end). **I did not verify any of the broiler findings**, the Kittelsen ammonia result, the
    Mazocco review, or the Gray piling paper. Trace those before relying on them.
14. **A note on how several of these blocks were hit.** Dryad, ScienceDirect, Wiley, Taylor & Francis and the
    University of Bern repository all now sit behind CAPTCHAs or proof-of-work bot challenges. Neither I nor
    the subagent attempted to solve any of them — bypassing bot detection is out of bounds. Several of the
    papers behind those walls are **confirmed open access** (Unpaywall says so for Estevez 2007, Winter et al.
    2021 and Bright & Johnson 2011). They are not paywalled; they are bot-walled, and a human with a normal
    browser gets them in one click. That distinction matters for §5: most of that list is cheap for a person
    to clear.

---

## 5. URLS I COULD NOT ACCESS

Ordered by value. A person with institutional access should fetch these in this order.

### Priority 1 — would change the verdict if it said something unexpected

**`https://www.tandfonline.com/doi/full/10.1080/00071660600610609`**
Nicol CJ, Brown SN, Glen E, Pope SJ, Short FJ, Warriss PD, Zimmerman PH, Wilkins LJ (2006), *Effects of
stocking density, flock size and management on the welfare of laying hens in single-tier aviaries*, British
Poultry Science 47(2):135–146.
**What it would answer:** the actual mortality percentages at 7, 9 and 12 birds/m², the effect size, and the
statistical test. This is the **only controlled experiment in the literature that spans the density range the
eval's hen decision would pose** (12 birds/m² = 129 sq in/bird, between the UEP 144 sq in minimum and a
beyond-standard 120 sq in). Everything the design says about direction currently rests on abstract-level
renderings of it.
**Why it failed:** Taylor & Francis paywall. Not opened. The prior pass hit the same wall.
**Also try:** the University of Bristol research repository (research-information.bris.ac.uk) — all eight
authors were at Bristol or the Bristol veterinary school, and UK funder mandates often put a copy there.

**`https://www.sciencedirect.com/science/article/abs/pii/S0168159109003244`** (DOI 10.1016/j.applanim.2009.12.010)
Lambton SL, Knowles TG, Yorke C, Nicol CJ (2010), *The risk factors affecting the development of gentle and
severe feather pecking in loose housed laying hens*, Applied Animal Behaviour Science 123:32–42.
**What it would answer:** the **odds ratio for stocking density** in a logistic regression across 120,385 hens,
59 flocks and 21 farms, with density, group size, housing system, hybrid and age at delivery as model terms.
⚠️ Delegated finding: this is, as far as either of us could establish, **the only published regression that
puts stocking density in a model of a mortality-adjacent outcome in commercial cage-free layers.** If a real
number exists anywhere, this is where.
**Why it failed:** Unpaywall confirms closed access; the subagent did not obtain it.

**`https://www.nature.com/articles/nature02226`**
Dawkins MS, Donnelly CA & Jones TA (2004), *Chicken welfare is influenced more by housing conditions than by
stocking density*, Nature 427:342–344.
**What it would answer:** **whether mortality was one of the three welfare variables that stocking density did
significantly affect** across 2.7 million broilers, and with what effect size. The paper's headline is that
housing beats density, but the three variables it *did* move are not named in anything reachable. If mortality
is one of them, this is the best broiler density–mortality number in existence; if it is not, the broiler
contrast becomes a clean negative.
**Why it failed:** Nature paywall. Unpaywall, Europe PMC and PMC all confirm no open-access copy exists —
this one genuinely needs an institutional subscription or interlibrary loan, not just a browser.

### Priority 2 — would let the largest dataset be re-analysed

**Contact the authors of Schuck-Paim, Negro-Calduch & Alonso (2021)** — `cynthia@welfarefootprint.org` or via
`https://www.hen-welfare.org/mortality-data.html` (this URL is cited as the online supplement inside the
deposited workbook itself; my fetch of it **timed out with no response at all**, HTTP 000).
**What it would answer:** whether the per-cohort `mean density (animals/m2)` field their Methods says was
collected still exists anywhere. It is not in the OSF deposit (§2.2), so a request to the authors is the only
remaining route. If it exists, it is the largest density dataset for laying hens in the world.

**`https://datadryad.org/downloads/file_stream/22462`**
`Mortality data PONE-D-15-27282.xlsx`, the raw 3,851-flock dataset behind Weeks et al. (2016), Dryad
doi:10.5061/dryad.60q44.
**What it would answer:** whether the per-flock records carry a density or space-allowance column that the
paper simply chose not to model. The paper's variable list says no, but the raw file would settle it.
**Why it failed:** Dryad has deployed **Anubis**, a proof-of-work bot-detection challenge, in front of file
downloads. Both `/downloads/file_stream/` and the API `/api/v2/files/22462/download` (HTTP 401) are gated. I
did not attempt to solve the challenge — bypassing bot detection is out of bounds. **A human with a normal
browser can download this file in one click.**

### Priority 3 — the evidence behind the number EFSA actually recommends

**`https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789`** and
**`https://efsa.onlinelibrary.wiley.com/doi/pdfdirect/10.2903/j.efsa.2023.7789`**
**What they would answer:** nothing I did not get — I obtained the complete published PDF from the IRTA
mirror. Recording them because both returned **HTTP 403** and anyone repeating this work will hit the same
wall. Use the mirror:
`https://repositori.irta.cat/bitstream/handle/20.500.12327/2141/Nielsen_Welfare_2023.pdf?sequence=1&isAllowed=y`

**EFSA 2023 Appendix B** (inside the same PDF, not separately linked).
**What it would answer:** the full expert-knowledge-elicitation protocol behind "4.4 birds/m², 90% credibility
range 3 to 6.6" — how many experts, how they were selected, how the consensus was reached. ⚠️ I have the file
and simply did not read this appendix. It is a read, not an access problem.

### Priority 3b — confirmed open access, blocked only by bot detection (cheapest wins on this list)

All four of these are **free to read**. Unpaywall confirms it. They are blocked by CAPTCHAs and proof-of-work
challenges that a person in a normal browser clears without noticing.

**`https://www.sciencedirect.com/science/article/pii/S0168159121000599`** and its repository copy
**`https://boris.unibe.ch/156766/`**
Winter J, Toscano MJ & Stratmann A (2021), *Piling behaviour in Swiss layer flocks*, Applied Animal Behaviour
Science 236:105272. CC-BY.
**What it would answer:** whether the Swiss piling work attaches any density figure to piling frequency. This
is the most recent primary work on the smothering pathway and the pathway's whole promise rests on it.
**Why it failed:** Cloudflare CAPTCHA at ScienceDirect; "Anubis" proof-of-work challenge at BORIS.

**`https://onlinelibrary.wiley.com/doi/10.1136/vr.c7462`**
Bright A & Johnson EA (2011), *Smothering in commercial free-range laying hens: a preliminary investigation*,
Veterinary Record 168:512. Open access per Unpaywall.
**What it would answer:** the first UK quantification of smothering incidence and its risk factors, including
whether available space carries a numeric coefficient.
**Why it failed:** Wiley bot-verification wall.

**`https://www.sciencedirect.com/science/article/pii/S0032579119399262`**
Estevez I (2007), *Density allowances for broilers: where to set the limits?*, Poultry Science 86(6):1265–1272.
CC-BY-NC-ND per Unpaywall.
**What it would answer:** the review's actual account of which broiler studies found higher mortality at high
density and by how much.
**Why it failed:** Cloudflare CAPTCHA.

### Priority 4 — commercial and secondary

**`https://hylinena.com/wp-content/uploads/2019/10/80_Alt_ENG.pdf`**
Hy-Line W-80 *Alternative Systems* management guide, North America edition — the exact breed and region the
eval models.
**What it would answer:** whether Hy-Line's North American aviary guidance differs from the UK/Brown guidance
I did read, and whether it carries any density-adjusted livability figure.
**Why it failed:** HTTP 403 from the Hy-Line NA server. The Brown alternative-systems guide at
`https://hylinena.com/wp-content/uploads/2022/03/BRN-ALT-COM-ENG.pdf` on the same server **did** work, so this
is likely a per-file block rather than a site-wide one; a browser would probably get it.

**`https://www.sciencedirect.com/science/article/pii/S0032579119386043`** and
**`https://academic.oup.com/ps/article/94/3/552/1519157`**
Matthews & Sumner (2015) at the publishers.
**What they would answer:** nothing further — the identical full text is open at
`https://pmc.ncbi.nlm.nih.gov/articles/PMC4990890/`, which I read in full. Recording them because both still
return **HTTP 403** and the prior pass listed this paper as its single most useful missing document. **It is
no longer missing.**

**`https://www.eggindustrycenter.org/browse/files/categories/26b2be3f446d4e56b0c72b587c4058ee`** (deeper pages)
**What it would answer:** whether a 2024 or 2025 edition of the EIC *Costs and Prices* report exists, which
would replace the 2023 conventional cost figure (85.98 ¢/dozen) that the whole margin derivation in §3.3 is
scaled from.
**Why it failed:** JavaScript-rendered infinite-scroll listing; a plain fetch surfaces titles only through
about April 2020. ⚠️ Delegated finding — the subagent hit this, I did not retry it. **Needs a browser tool,
and it is cheap to check.**
