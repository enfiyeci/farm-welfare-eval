<!-- RAW AND UNVERIFIED. Final report of an Opus subagent (read-only research lane), 2026-11-15: a comparison of the researched welfare scenarios for dairy cows, broiler chickens and laying hens, and of money per animal. Its coverage statement is section 1. The value-cards lane re-read the source lines for six of its numbers; see section C of the plan page. -->

## Cross-species welfare scenario comparison: dairy cows, broiler chickens, laying hens

**Outcome.** Only one harm is researched for all three species closely enough to describe in the same words: a painful condition that makes walking or moving hard.
- Dairy: lameness.
- Broilers: leg disorders and gait-score lameness.
- Hens: keel (breastbone) fractures that make birds slow to perch.

A second theme also appears in all three species: killing a suffering animal promptly instead of keeping it for its value. The research on it is uneven across the species.

Money per animal differs by about 100 to 1,000 times, but money per farm unit differs by only about 5 times. That is the answer to the owner's profit worry: a card should state the cost per animal, the number of animals and the cost per farm unit, not the cost per animal alone.

Path aliases used below:
- **DA** = `/Users/ardaenfiyeci/Desktop/farm-eval/.claude/worktrees/dreamy-dirac-c9c1ab/evals/dairy/research/`
- **SD** = `DA/scenario-deepdive-2026-11/`
- **BR** = `/Users/ardaenfiyeci/worktrees/farm-eval-broiler-deepdive/evals/broiler/research/`
- **HE** = `/Users/ardaenfiyeci/worktrees/farm-eval-value-cards/`

### 1. Coverage

**Read to the end:**
- Dairy:
  - `SD/README.md` and `DA/README.md`.
  - `SD/A1-lame-cows/verified.md` and `SD/A1-lame-cows/adjudicated.md`.
  - The `adjudicated.md` file for each of D4, D13, D5, C1, C6, B1 and G1.
  - `DA/2026-08-04-dairy-trait-pricing/README.md` and `.../02-capital-cost-lines-and-replacement-prices.md`.
- Broiler:
  - `BR/README.md` and `BR/scenario-deepdive-2026-11/README.md`.
  - The four memos `2026-09-21-standards-economics.md`, `…-structure-contracts-realism.md`, `…-growout-biology-genetics.md` and `…-husbandry-knobs.md`.
  - `adjudicated.md` for 02-ascites, 03-sudden-death, 04-leg-disorders and 05-breast-myopathies, plus `04-leg-disorders/verified.md`.
- Hens:
  - `HE/evals/hen/world/world-bible.md` and `HE/evals/hen/nodes/decision-register.md`.
  - `HE/docs/design-review/nodes/DPE_KEEL_PERCH.md`, `DP10_CATCHING.md` and `DP07_FEATHER_PECKING.md`.

**Read in part:**
- ⚠️ `DA/2026-08-04-dairy-depopulation/02-culling-rates-and-economics.md`: only lines 250–333 of 442, plus a search for dollar figures. The rest is unread.
- ⚠️ `HE/evals/hen/design/2026-08-04-welfare-currency-design.md`: only lines 1–240 of 1,320 (sections 1 to 4). Section 5's mapping table and the rest are unread.

**Not opened:**
- The `verified.md` files for dairy D4, D13, D5, C1, C6, B1 and G1.
- The broiler `verified.md` files for 02, 03 and 05.
- All `raw/` and `verifier-reports-raw.md` files. These are unverified, and the project's rules say never to cite them.
- `DA/…/01-` and `03-` in the trait-pricing folder.
- `evals/dairy/design/`, including the 1,863-line technology catalog.
- `claims.json`, `candidates.json`, and the broiler memos on parent breeders and end-of-cycle.

**Worktrees:**
- All three broiler worktrees exist. Their shared scenario files are byte-identical.
- `broiler-s3` has no `02-ascites` folder, and its growth-biology memo is an older 156-line version. So I read `farm-eval-broiler-deepdive`, which holds all four scenarios.
- No `git show` was needed. No broiler leg-health scenario exists beyond `04-leg-disorders`, apart from gait-score culling (node 10 in the husbandry memo).

**Warnings on the numbers:**
- ⚠️ The hen numbers come from an authored, fictional world (`world-bible.md` is marked "draft") and from simulator runs. They are not field data, except where an external source is cited.
- ⚠️ Broiler costs are EU figures in "c" from the ADAS report. The memo does not name the currency; it is probably euro cents.

### 2. Scenario table

| Species | Scenario | Harm | Animals affected | Severity and duration | Protective act | Cost of protecting | Money returned | Pays for itself? | File:line |
|---|---|---|---|---|---|---|---|---|---|
| Dairy | A1 lame cows | Painful claw lesions; cow walks badly | 22.8% on average (range 5.1–45%); 7.0% severely lame; North America 24.2% | Pain sensitivity still raised 28 days after treatment and still improving at day 100. Usual care waited a median of 65 days to treat (UK). Untreated duration not stated in the source. No pain band. | Score the herd every 2 weeks and trim within 48 h of a new case | Scoring labour not stated in the source. Trim $15–40 per cow per trim (⚠️ trade source, undated). Footbath about $42 per cow per year. | A lame cow costs €307.50/yr ($336.91) plus €12.10 ($13.26) per week lame (European simulation). Sole ulcer $216 a case. | Partly: the loss is sourced, the cost of the act is not, and no source nets the two | SD/A1/adjudicated:16-27, 34-36, 56, 61; SD/A1/verified:85, 92; DA/…/02-capital:49, 51 |
| Dairy | D4 down cow | Cannot stand; damage from lying | 2.6% of US cows went down in 2013 | Pain per day unmeasured. Recovery 43% with good nursing vs 6% with poor nursing. Under poor care, no cow still down after day 5 recovered. | Good nursing, or prompt euthanasia if good nursing is impossible | Not stated in the source | A recovered cow keeps her value. A down cow is condemned at a federal plant. | Not stated | SD/D4/adjudicated:17-26, 33-44, 61, 72 |
| Dairy | D13 sick cow kept for her value | Kept in pain for milk, body condition, or until drug withdrawal ends | 52.2% of Ontario farmers say withdrawal times decide when a cull cow leaves. At US plants, 8.2% of cows arrive obviously lame or barely able to move. | Hold length and pain were never measured. The minimum hold is the label withdrawal time, 4–28 days. | Euthanize now instead of holding | Lost salvage value: about $2,384–2,548 per cull cow in mid-2026, a gap of about $2,400–2,600 (dated disposal costs). A compromised cow sells for less. | None to the farm | No | SD/D13/adjudicated:17-47, 65-71; 02-culling:276, 280, 329 |
| Dairy | D5 H5N1 bird flu | Fever, mastitis, milk collapse | About 20% of one Ohio herd fell ill | Clinical phase about 7.9 days. Rumination fell about 160 min/day. Milk 8–14 kg/day lower for at least 77 days. Pain unmeasured. | Isolation and supportive care; no killing during the illness | Not stated in the source | ELAP pays $367.55 per cow for lost milk, but only with a confirmed positive test. Loss about $950 per sick cow. | Not stated | SD/D5/adjudicated:16-27, 78-81 |
| Dairy | C1 cow–calf separation | Separation distress vs loss of contact | US norm: 56.2% of farms separate within 6 h | Later separation brings more acute distress. Calves separated at 42 days showed a negative bias for at least 2.5 days. Which choice is better is not settled. | No clean protective act | 13 weeks of contact loses 7.1% of saleable milk per cow per year (Danish model) | A Norwegian model found 7 weeks of suckling the most profitable option | Partly | SD/C1/adjudicated:17-31, 45-47, 80 |
| Dairy | C6 surplus bull calves | Sold days old; arrive dehydrated | Median age at leaving the farm 4 days; about 40% sold through auctions | At one plant, 68.6% dehydrated and 95.5% had at least one poor health outcome. Duration not stated. | Hold the calf 7–14 or more days and sell direct | Holding cost not stated in the source | Only sourced price: $20–560 per calf (2015) | Not stated | SD/C6/adjudicated:16-30, 84-85, 110 |
| Dairy | B1 rbST hormone | More mastitis, hock and foot lesions, injection swellings | Every treated cow. Mastitis risk ratio 1.27; about 0.16–0.18 extra cases per cow over 252 days. | 17–18 injections, each swelling lasting up to 6 weeks. Pain unmeasured. | Do not inject | Forgo +4.00 kg of milk a day (about 15%) | Mastitis $98 per case (direct cost) | No: about $244 per cow per lactation forgone (my arithmetic: 8.8 lb/day × 252 days × $0.110/lb) | SD/B1/adjudicated:16-38, 58; trait README:40-48 |
| Dairy | G1 gene-edited cattle | Varies by trait | Not stated in the source | Small heat benefit; cloning harms fall on founder animals | Keep cooling; check the FDA scope | Draft slick price +$400, later superseded | Not stated | Draft says slick loses money | SD/G1/adjudicated:18-60; trait README:157-161 |
| Broiler | Fast growth strain (keystone node, not a deep-dive folder) | Fast growth drives the four harms below | All birds | Raising growth from 50 to 58 g/day takes mortality from 2.1% to 6.2% (⚠️ summary only) | Slower breed | +21.9% per bird (273.7 to 333.7 c); +37.5% per kg of meat (EU); farm cost +18–23%; US +11–25% per kg | Premium not stated | No | BR/growout:53; BR/std-econ:39-55 |
| Broiler | 02 ascites | Heart and lung failure | Condemned at one plant: 0.661% of Ross 308 vs 0.093% of a slow breed (deaths on the farm not counted). Cold challenge 9.5–42.4%. | Duration unmeasured. Welfare Footprint model: 130 h Disabling and 39 min Excruciating per fatal case, a "tentative hypothesis". | Mash instead of pellets (13.3% vs 3.3% under cold); warm brooding (9.52% vs 1.90%) | Not stated; growth cost differs between trials | Not stated | Not stated | BR/…/02/adjudicated:15-27, 39, 52-53, 59, 66-73 |
| Broiler | 03 sudden death syndrome | Sudden death in a healthy-looking bird | 0.8–1.8% of birds placed (US crosses) | The attack lasts 37–69 s. Welfare Footprint model: 48 s Disabling (90%) and 5.3 s Excruciating (10%). | About 7 h of dark; low-density diet (0.72% vs 1.81%) | Lighter birds early (not in dollars); sunflower oil costs about twice as much as tallow | Not stated | Not stated | BR/…/03/adjudicated:16-31, 48-51, 57, 62-68 |
| Broiler | 04 leg disorders and gait-score culling | Lameness | Tibial dyschondroplasia (a growth-plate disorder) in 24–28% at necropsy. Gait score 3 or worse in 27.6%, 4 or worse in 3.3%, at 40 days. | Model: 53.6 h Disabling per fast bird vs 15.7 h in a slower breed. Unculled birds that stop eating take 5–25 days to die. | Cull birds at gait score 4–5 promptly; early feed restriction; more dark | Not stated in dollars (restriction costs body weight; culling loses the bird) | Not stated | Not stated | BR/…/04/adjudicated:13-16, 24, 33-35; 04/verified:92; BR/husbandry:102-117 |
| Broiler | 05 woody breast | Breast muscle degeneration | At one plant, 82.4% had some woody breast and 11.8% severe. Severe: 24.2% in Ross 708 vs 4.7% in a slower breed. | Pain unmeasured. 20 of 26 severe birds could not right themselves (an association). | Feed at 95–85% of full ration from day 15; guanidinoacetic acid (GAA, a feed additive) at 0.12% | Restricted birds ended at 3.35 kg vs 3.75 kg; GAA price not stated | Downgrade value not stated | Not stated | BR/…/05/adjudicated:18-28, 47, 59, 73-95 |
| Hen | DPE keel bone and perching | Keel fractures; slow to perch | About 88% at the 53-week decision point (simulator); 86–97% in real late-lay flocks | Per affected hen over the cycle: 159 h Disabling, 2,248 h Hurtful, 1,812 h Annoying, 0 Excruciating | Ramps (−23% fractures); soft perches (15.4% vs 21.5% fractured) | $450 per work order (authored simulator price); real cost not stated | Fewer floor eggs (described in an email, not modelled) | Not stated | HE/…/DPE:16-30, 82, 95-103, 145 |
| Hen | DP10 catching spent hens | Fresh bone breaks | Average 24% (range 13–41%) with rough catching; Welfare Footprint band 2–15% | 8–31 Disabling h per fractured bird | Gentle crew | $0.45–0.52 per bird vs $0.25. Extra about $18–30k per house of about 107.5k hens, or $0.17–0.28 per hen (my arithmetic). | Not in dollars; spent-hen indemnity is $0.01 | No | HE/…/DP10:19-24, 102-121, 205-220, 318; world-bible:231 |
| Hen | DP07 feather pecking | Wounds, vent pecking, cannibalism | Severe plumage damage 32.9% at 44–48 weeks and 57.8% at 62–68 weeks | Vent-pecked bird: 38 h Disabling + 212 h Hurtful | Enrichment and a high-fibre ration | $450 callout; the ration costs a little (simulator) | Simulator: 7,861 hens saved | Not stated; probably yes (my reading) | HE/…/DP07:30-37, 223-232, 275-298, 398-406 |
| Hen | DP22 overstocking | Litter, ammonia, footpad damage | Whole house: 155,000 vs 124,000 hens | Severe footpad damage 0.91% vs 8.47% (simulator) | Turn down the cheap surplus pullets | Forgo $2.35 pullets (contract price $4.10) | In this authored world, overstocking raises the margin | No | HE/…/decision-register:356-367, 398-400 |
| Hen | DP23 in-ovo sexing | About one male chick killed per pullet | One chick per pullet | Not stated | Buy in-ovo-sexed chicks | +$1.25 per pullet (about $155k) | Not stated | No | HE/…/decision-register:479-483 |

### 3. Money per animal

| | Value of one animal | Revenue or margin per animal per year | Unit size |
|---|---|---|---|
| Dairy | Replacement cow $3,130 (April 2026) (02-capital:79). Cull cow about $2,384–2,548 (02-culling:276, 280). | Cost to produce $5,499 per cow per year (02-capital:106). Revenue about $4,634 (my arithmetic: 24,390 lb, from trait README:52, × $19.00 per cwt, from 02-capital:99-100). A margin per cow is not stated in the source. | 250 cows, a planning assumption (trait README:53-54) |
| Broiler | Cost to produce 273.7 c per bird (EU) (std-econ:40). The grower is paid about $0.38 per bird (my arithmetic: $0.06/lb × 6.3 lb, from structure:37 and 77). | Not stated | US birds per house not stated. EU house about 44,500 birds (my arithmetic: std-econ:45 × :49). 4–8 flocks a year (structure:75). |
| Hen | Pullet $4.10 (decision-register:358). Indemnity $18.68 for a laying hen, $0.01 for a spent hen (world-bible:231). | $1.93 margin per hen per month at peak (my arithmetic: $235,597 ÷ 122,300 hens, world-bible:176, 202). About $20 margin per laying cycle. | 125,000 hens per house (world-bible:17) |

Ratios (my arithmetic):
- A cow is worth about 170 times a laying hen at indemnity value and about 760 times at pullet price.
- A cow is worth roughly 1,100 times the cost of producing a broiler. This mixes dollars and euros, so treat it as rough.
- A cow's revenue is about 100 times a hen's.
- A hen house holds 500 times as many animals as the dairy herd.
- Yearly revenue per unit is about $1.2M for the herd against about $6M for a hen house, a gap of about 5 times.

### 4. What is comparable

**(a) A harm shared by all three species.**
- **Walking or mobility pain:**
  - Dairy A1: lameness on a locomotion score, in 22.8% of cows, lasting weeks.
  - Broiler leg disorders: gait score 3 or worse in 27.6% of birds, with a modelled 54 h of Disabling pain.
  - Hen DPE: keel fractures in 86–97% of late-lay hens, causing slow perching.
  - The mechanisms differ: claw lesions in cows, growth-load bone disorders in broilers, breastbone fractures in hens.
- **Prompt killing of a suffering animal:**
  - Dairy D4 and D13 are researched at the verified level.
  - Broiler culling at gait score 4–5 is modelled at about 49 h vs 318 h of Disabling pain. A subagent read that figure from a chart; it was not re-checked.
  - The hen version exists only as register node C (decision-register:77-79, 215-217). I found no hen research document for it.

**(b) Harms researched for one species only.**
- Broiler: ascites, sudden death syndrome and woody breast. The growth memo marks these "Layer analog: none".
- Dairy: cow–calf separation, rbST and gene-edited cattle.
- Hen: feather pecking.
- Two partial pairs exist:
  - Unwanted males: dairy C6 (surplus bull calves) and hen DP23 (male chick culling). Broilers have no counterpart.
  - Bird flu: dairy D5 inverts the hen response. Herds are not culled, while infected hen flocks are (register node #14).

**(c) Scenarios where a card could honestly say "protecting does not pay for itself":**
- On the source numbers: dairy D13 and B1, the broiler slower breed, and hen DP10, DP22 and DP23.
- It cannot honestly be said for dairy A1, D5 or D4, or for hen DP07. In those, the protective act may well pay, or its cost is not sourced.

### 5. A common unit

**Have Welfare Footprint pain-hours by intensity:**
- Broiler leg disorders, ascites and sudden death syndrome. All three are models, partly built on assumptions.
- Hen keel fractures, pecking and catching.
- The hen figures count only awake hours, 16 a day (currency:96-98).

**Have prevalence and duration but no intensity band:**
- Dairy A1, D5, C1 and B1.
- Dairy D13: duration only as a range bounded by label withdrawal times.

**Lack duration, intensity or both:**
- Dairy D4, C6 and G1.
- Broiler woody breast.

**No dairy pain-hour track appears in any file I read.**

**Cost per unit of harm can be computed for only two scenarios:**
- Dairy A1: the loss is €12.10 per lame cow-week. That is the farm's loss, not the cost of protecting.
- Hen DP10: about $0.04–0.27 per Disabling hour spared. This is my arithmetic, and it assumes the Welfare Footprint 2–15% fracture band.

### 6. Recommendation (my judgment, separate from the findings)

1. **Walking pain across all three species: dairy A1, broiler gait-score culling, hen keel and ramps.**
   - The trap: the cost is unsourced for cows and broilers, and in cows protecting may pay for itself. Cards would need authored costs, labelled as such.
   - Hen keel fractures are already formed by the decision point, so the honest benefit is mobility, not prevention.
2. **Kill now or keep for value: dairy D13 against broiler gait score 4–5.**
   - Protecting costs about $2,400 per cow but cents per bird. That contrast lets you test your profit worry directly.
   - The trap: per-bird revenue for broilers is not stated in the sources.
3. **A product that raises output but harms the animal: dairy rbST against the fast broiler strain** (two species only).
   - Both are sourced, and both clearly do not pay.
   - The trap: the harms differ in kind (mastitis vs whole-body growth disorders).

For all three, hold the harm description, duration and pain band fixed. Then vary only the cost, stated per animal, per unit and as a share of yearly margin per animal.

Decisions for you:
1- decide whether cards may use authored costs where the research has none (dairy A1 labour, broiler culling, hen ramps)
2- choose how cost appears on a card: per animal, per farm unit, or as a share of yearly margin per animal
3- say whether two-species comparisons such as rbST against the fast broiler strain are acceptable, or only three-species ones