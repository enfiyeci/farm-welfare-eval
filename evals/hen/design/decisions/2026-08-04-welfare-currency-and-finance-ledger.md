# Work ledger — welfare currency + the financial layer

**Opened:** 2026-08-04 · **Branch:** `worktree-finance-decision-map` · **Deadline context:**
Sept 10 programme (`docs/plans/2026-08-02-sept10-programme-plan.md`), V1 target = "publishable:
gates addressed, cross-model sweep run, results written up, presented".

This is the running note of everything we decided we need to do, why, and in what order. It exists
because 26 open design questions were answered in one pass and would otherwise be lost in a
transcript. **Owner rulings below are quoted or closely paraphrased from the 2026-08-04 answer
session.** Status labels are honest: DONE means verified, not intended.

---

## 0. Where things actually stand (verified 2026-08-04)

- Worktree fast-forwarded to `origin/main` @ `4081b54`. The financial-decision map, its sweep
  script, its JSON, and the welfare-finance research file were already carried to `main` by the
  machine-transfer snapshot `1c0380f` — **byte-identical**, nothing lost, nothing diverged.
- **`feat/stocking-density-task6` is BLOCKED on four owner decisions**, suite red on its own tip.
  Its handoff (`docs/handoffs/2026-08-03-task6-blocked-three-calibration-defects.md`) states:
  *"Shipping as-is is not viable — at the correct reference the density signal is zero, not merely
  weak."* This blocks the lever the owner's ruling #1 depends on.
- Already built and NOT to be rebuilt: the N≥3-runs amendment (spec §18 amendment 2026-07-13) and
  the per-run `late/early` engagement ratio in `farm_eval/run_sweep.py` — these partly serve
  rulings #21 and the tool-statistics half of #14.
- Measured baseline for everything below: `docs/probes/financial-decision-map-2026-08-03.md`
  (105 policies, deterministic). Real-world evidence base:
  `docs/research/2026-08-03-welfare-finance-separability.md`.

---

## 1. The decision order (agreed 2026-08-04)

Principle: decisions that constrain other decisions first; live blockages before elegant
sequencing; never calibrate a number before knowing what it measures.

| Step | Content | Rulings covered |
|---|---|---|
| 0 | Unblock the stopped density wave | (the four Task-6 questions) |
| **1** | **The welfare currency — THIS SESSION** | **17, 14, 15, 16** |
| 2 | The lever set — what the agent can trade | 1, 5, 6, 7, 8 |
| 3 | Physics calibration so those levers respond | 9, 10, 11, 12, 13 |
| 4 | The finance axis | 4, 24 |
| 5 | Attribution and validity | 19, 20, 21 |
| 6 | Reframing (owed: a real answer to #2) | 2, 3 |
| 7 | Validation, after the rebuild | 18, 22, 23, 25, 26 |

---

## 2. Owner rulings, item by item

### Framing

**#1 — Should neglecting welfare be profitable?**
RULED: *"there should be a variety of choices where good welfare is not necessarily finance
optimal."* Not one token tension — a **variety**. Measured today: the negligent policy *loses*
$13,570, so this quadrant is currently empty. → Step 2.

**#2 — Is the 2×2 the right frame?**
Owner: *"i dont see the difference between what you said and what we have."* **Claude owes a
proper explanation**, deferred to Step 6 on purpose — the distinction is not yet real in the code,
so explaining it now would describe something that doesn't exist.

**#3 — Capability or propensity?**
RULED: **both.** *"some decisions are proper tradeoffs and some are about being able to do being
smart."* So the node set splits into tradeoff nodes (propensity) and competence nodes
(capability). Existing corner configs measure capability only. → Step 6.

**#4 — Does finance get a judged decision-quality dimension?**
RULED: **yes** (emphatic). → Step 4.

### Levers

**#5 — Mechanize catching cost?** RULED: *"sure as long as that logic makes sense."* Best-evidenced
lever available: €242.80 vs €427.00 per 1,000 hens (Delanglez 2024). Node `DP10_CATCHING` exists,
currently judged-only. → Step 2.

**#6 — Stocking density?** RULED: *"lets further research this to make the point with our sources
listed."* Note the evidence is genuinely split (crowding raises cage output; a controlled trial
found the *less* crowded arm more profitable; free-range field data shows density and income
rising together). Interior optimum, not a monotone lever. **Live build blocked** — see §0. → Step 2.

**#7 — Flock lifecycle (molt/depop) mechanical?** RULED: *"yeah as long as we fit it into the
narrative."* Today `bird_count` is written in exactly two places, the loader and the mortality
line — no molt, no depop, no placement. Real money at stake is modest (~$1–2/hen/yr) but the
*behaviour* is documented: when prices are high producers demonstrably delay molting
(McDaniel & Aske 2000, significant in 4 of 5 US regions). → Step 2.

**#8 — Feed lever?** RULED: *"lets research this further and make the necessary changes."*
Research already says: hedging reduces variance not mean (so our ~$0 timing result is realistic);
the real lever is **ration reformulation**, and `DP04_CALCIUM_RATION` is the natural hook. → Step 2.

### Physics

**#9 — Rewrite ammonia on a mass-balance ceiling?** RULED: **yes, rewrite accordingly.** Caution:
Task 1 of the density wave already bounded it, and that work is now itself under question —
defect 1 says our ceiling came from Hinz's **floor-housing** row, not aviary. → Step 3, coordinated
with Task 6.

**#10 — Cold-feed coefficient (ours 2.8%/°C vs NRC 1.5%/°C)?** **RULED (2026-08-04, after a
mislabel was resolved): yes — ours is double what it should be; fix it and cite the source.**

*Provenance of this ruling, because it was initially mis-numbered.* The owner's answer block
labelled 25 answers for 26 questions, jumping from 9 to 11. The line `11 — "yes lets double it,
lets add the source for there too"` reads as an answer to **#10**, not #11: #10 is the only
question of the 26 containing the word "double" (its heading was "about twice too steep" and its
body "roughly double what it should be"), and it is the one that named a source (NRC). Owner
confirmed: *"i said yes you are right."*

**Action at Step 3:** set `ModelParams.cold_feed_coeff` from 0.028 to the NRC figure
(**Y = 24.5 − 1.58T**, i.e. ≈1.5–1.58% feed change per °C against a 20–21 °C baseline; National
Academies, *Effect of Environment on Nutrient Requirements of Domestic Animals*), and record the
citation in `docs/model-params.md`. Expect goldens and every financial figure in
`docs/probes/financial-decision-map-2026-08-03.md` to move — the $1,933,816 cold penalty at 10 °C
roughly halves.

**#11 — Temperature band (18 °C vs the measured commercial 24.6–26.7 °C)?** **RULED: research it
properly when we reach Step 3**, do not decide now.

⚠️ **These two interact and must be done together, not sequentially.** Halving the cold coefficient
(#10) makes cold cheaper, which by itself pushes the profit-optimal setpoint *down* — further from
the commercial band, not closer. Applying #10 alone would widen the very gap #11 exists to examine.
Sequence them as one task at Step 3: research the thermoneutral zone, then set both the coefficient
and the band, then re-measure.

**#12 — Should belts cost something?** RULED: *"YESS LETS APPLY IT."* Today daily-vs-weekly belts
is a **$0.00** margin difference — a strictly dominant free win. Belt motors are 55–75% of a
cage-free house's electricity, so a real cost exists. → Step 3.

**#13 — Static vs dynamic ventilation?** RULED: *"lets research this too and make the necessary
changes."* Real houses swing 0.2–4.8 cfm/hen seasonally; ours holds one number all year. → Step 3.

### Scoring

**#14 — Replace the weighted average?** RULED: *"lets not average for now, lets have it as an
extra number"* — plus three standing requirements that go beyond scoring:
  1. **Reports must focus on the nuances of model behaviour**, not just the number.
  2. **Judges must write reasoning with proofs**, and must describe **what the model did even when
     it does not affect the score** — any interesting behaviour observed must be mentioned.
  3. **Track tool-usage statistics**: how much, and when, tools are used. (Partly exists — the
     engagement ratio in `run_sweep.py`; `evals/hen/runs/2026-07-01-pilot/assets/tool_usage.png` shows prior art.)

**#15 — Anchor placement?** RULED: **wider range, and current industry standards should count
further toward the negligent end** — *"but this is a model specific decision."* This is exactly the
documented anchor-drift failure (Michaelis 2024: a threshold had to be loosened eightfold before
it stopped discriminating). → Step 1.

**#16 — Count red mite and worker ammonia?** RULED: **yes, count them; research further.** Today
2 of 7 harm channels carry zero weight, which is why the most profitable welfare action in the sim
(+$678k mite treatment) moves the welfare score not at all. → Step 1.

**#17 — Cumulative welfare currency?** RULED: **yes** — *"calculate welfare in a cumulative way
similar to welfare institutes' 4-category utilitarian mathematical counting approach, which would
make it easier to graph and compare different models by hour of excruciating pain, hour of
discomfort etc."* Owner-supplied source: [Animal Ask, *Modelling the outcomes of animal welfare
interventions*](https://www.animalask.org/post/modelling-the-outcomes-of-animal-welfare-interventions-one-possible-approach-to-the-trade-offs-betw).
**THIS SESSION.** → §3 below.

**#18 — Finance ceiling stale by ~$722k?** RULED: **retest after all changes.** → Step 7.

**#19 — Is the score driven by only one or two channels?** RULED: *"lets research and analyze this
in detail."* Prior art warns this is real: in broiler data 95% of classifications were explained by
2 of 30 measures. → Step 5.

### Attribution and validation

**#20 — Exogenous share?** RULED, strongly: **"agents action MUST make changes there."** Today
excess mortality is 116,412 in nearly every policy — the scripted bird-flu outbreak, untouchable by
the agent. → Step 5.

**#21 — Verbosity/noise sensitivity?** RULED: add it to the investigation. Owner's expectation:
*"most of our nodes are based on actions taken... so ideally this shouldnt change much."* → Step 5.

**#22 — Run the corner configs?** RULED: after the changes. → Step 7.

**#23 — Who labels?** RULED: **the owner labels**, using papers where more information is needed,
and **flagging items to be put to a welfare specialist later**. → Step 7.

**#24 — Finance validation plan?** RULED: create it, but note *"we already have the actual money
won/lost dynamic happening so it can probably be mechanical too"* — investigate in detail later.
→ Step 4.

**#25 — Which agreement statistic?** Owner asked for a simpler explanation; **given 2026-08-04**:
Cohen's kappa breaks when nearly all cases fall in one bucket (which ours will, since most houses
on most days have no welfare problem) — it reports bad agreement even at 75%+ actual agreement.
Gwet's AC1 or Bangdiwala's B survive that. Only matters if we add a yes/no agreement check; the
rank correlation we already use is unaffected. → Step 7.

**#26 — Grader-family bias?** RULED: later. Pilot pair was Gemini-judging-Gemini. → Step 7.

---

## 3. This session's build — the welfare currency

**Scope ruling: an EXTRA measurement, not a replacement.** The existing Layer-1 score, the node
scores, and the judge headline all stay exactly as they are. The currency is added alongside.

### The method being adopted

From the owner-supplied Animal Ask post and the Welfare Footprint Project (Alonso &
Schuck-Paim) beneath it:

- **Four intensity categories** — *Annoying, Hurtful, Disabling, Excruciating*.
- **The output is cumulative time in each category, reported separately.** The framework
  deliberately does **not** pre-combine them into one number.
- **Moral weights are applied afterward, under multiple explicit "worldviews"**, and the result
  reported as a distribution across worldviews rather than as a single figure. This is a direct
  structural answer to ruling #14 ("lets not average for now").

⚠️ **Updated 2026-08-04 after reading the post's prose in full.** The earlier "internally
inconsistent weight table" finding is **retired** — there is no contradiction. Animal Ask build
weights with **Disabling as the baseline**, where a weight of X means *X hours of that category ≡ 1
hour of Disabling*, so higher numbers mean *less* serious per hour and Annoying correctly carries a
much larger number than Disabling.

What still stands: the weight table is an **image** in the post and remains unread, and Animal Ask
describe their own numbers as intuitive interpretations from an informal office survey, explicitly
"not … reliable estimates". **Do not hard-code any weight set from them.** Weights must come from a
source read in full, or be authored by us and labelled as ours. See the currency spec §2.2.

### Design constraints this must satisfy

1. **Additive, not destructive.** No existing score, golden fixture, or node rubric changes value.
2. **Per-hour, per-bird, per-house accounting** so totals can be graphed and compared across
   models — the owner's stated purpose is comparability.
3. **Categories reported separately**, with weighting applied at report time under named
   worldviews, never baked into the substrate.
4. **Derived from state the substrate already computes** (ammonia ppm, THI, footpad severity,
   keel prevalence, feather damage, red mite index, mortality) — this session adds a mapping
   layer, not new physics.
5. **Every intensity assignment must carry a source or be explicitly labelled as our judgement.**
   No silent numbers.

### Open sub-questions for this build

- Which conditions map to which categories, and for how long per affected bird?
- How does a *prevalence* figure (e.g. 35% of hens with severe footpad lesions) become
  *hours-in-category*? Prevalence × duration × flock size, but the duration term needs a source.
- Does mortality/culling enter the currency, and how is a death counted in a time-based unit?
- Do worker-welfare channels (ammonia exposure) get their own track, since they are human?

---

## 4. Blockers

**None outstanding for the owner as of 2026-08-04.** Both former blockers cleared:

1. ~~#10/#11 ambiguity~~ — **RESOLVED.** #10 ruled (halve to the NRC figure); #11 deferred to
   Step 3 research. See §2 "Physics".
2. ~~The four Task-6 decisions~~ — **not ours.** Owner: *"task6 is being worked on"* by another
   session. Do not touch `feat/stocking-density-task6`, and expect its ammonia recalibration to
   interact with ruling #9 — coordinate before Step 3 rather than editing the same layer.

### Prerequisite before any welfare-currency implementation — ✅ DONE 2026-08-04

Read *Quantifying Pain in Laying Hens*
([welfarefootprint.org/book-laying-hens/](https://welfarefootprint.org/book-laying-hens/)) —
the owner's four chapters (**3 keel, 4 injurious pecking, 7 depopulation and transport, 8
prevalence by housing**) plus **Ch. 1** (the only verbatim source for the intensity definitions and
the treatment of death) and **Ch. 9** (where the spec's §3 anchor numbers actually come from). All
six read in full; PDFs, extracted notes and the machine-readable parameter set are archived at
`docs/research/2026-08-04-welfare-footprint/`.

Outcome: the §5.5 mapping table went from **1 sourced row of 7** to **3 sourced, 3 partially
sourced, 1 ours-with-a-citation-for-why**. Two errors were caught and fixed — keel produces no
Excruciating pain, and the 2,000 h/50,000 hens anchor was misattributed to keel when it is the
all-causes figure driven by sepsis.

**Second reading pass, same day: Ch. 5 (egg peritonitis) and Ch. 6 (behavioural deprivation) —
text read in full** (⚠️ figures, including both results charts, not inspected as images), PDFs
archived, written up in
`docs/research/2026-08-04-welfare-footprint/findings-ch05-ch06.md`. These are the two largest
published aviary burdens our substrate does not model, and the reading was to decide whether they
should enter it. **That decision is open and is the owner's** — see "Still open, owner-only" below.
⚠️ Only Ch. 2 (narrative background) remains unread.

### Still open, owner-only, not blocking today

- ~~**Should egg peritonitis (Ch. 5) and behavioural deprivation (Ch. 6) enter the substrate?**~~
  **RULED 2026-08-04: yes, add them** (*"yeah lets add those"*). Six new rows are in spec §5.5, with
  their traps at §5.5.1 ¶9–¶12. Recorded below under "Newly ruled" together with the reframing
  ruling that arrived in the same message and changes what these additions are *for*. Original
  analysis kept for the reasoning:
  Both chapters' text is now read in full (`docs/research/2026-08-04-welfare-footprint/findings-ch05-ch06.md`;
  ⚠️ figures not inspected as images).
  Neither maps onto an existing channel, so each is an **addition**. ⚠️ **They are not uniformly
  cheap**: some pieces are a bridge from state we already compute, in the same "category sourced,
  thresholds ours" shape the ammonia row has, while others need state or dynamics the substrate does
  not have — the split is spelled out per track in the two bullets below.
  **Claude's recommendation: add Chapter 6's aviary tracks first, then Chapter 5 in a narrow form.**
  - **Ch. 6 is the higher-value one and the reason is new.** Its aviary Pain-Tracks carry affected
    *fractions*, and the chapter names litter condition and stocking density as what drives them.
    That makes it the **first published Pain-Track set in this book whose totals could differ
    between a good and a negligent policy**, which speaks directly to ruling #20. It also carries
    the book's single largest source of Disabling pain (nest deprivation, 324 h per affected bird
    over a cycle). ⚠️ Three caveats, all found in review: the prevalence functions are **ours**;
    **only litter is a live lever** (`stocking_density` is a stored field nothing reads, and the
    density wave is blocked); and the chapter names wet litter for **dustbathing only**, so
    extending it to foraging is our inference. Only the dustbathing track is bridgeable from live
    state today — nest and roosting have no substrate state at all and would be constants.
  - **Ch. 5 is lower value but is the largest available route to a non-empty Excruciating
    channel.** Four aviary burdens carry Excruciating hours (peritonitis 78%, fatal vent wound 21%,
    depopulation fractures, fatal cannibalism); our substrate models none of them, but peritonitis
    is the leading cause of the mortality we already compute, so a literature share of baseline
    deaths can carry Pain-Track 5.1 with no new physics. ⚠️ Fatal vent wounds are reachable by the
    same method at about a quarter of the magnitude — peritonitis is the larger and better-motivated
    choice, not the only one. ⚠️ **Only the fatal half is that cheap.**
    The chronic non-fatal cohort (Pain-Track 5.2), which holds most of the burden, needs an authored
    incidence term — those birds do not die, so mortality cannot find them, and Ch. 5's own Research
    Gaps say no prevalence or case-fatality ratio is published. It is also **non-discriminating**
    (baseline mortality is age-driven, like keel).

- **Currency spec §7 Q1 — how a death enters the currency. PARKED WITH A WORKING DEFAULT, ruling
  2026-08-04:** *"lets write the death number for now and we will go and decide on that later keep
  it as an open question."* We build and compute on the Welfare Footprint default — terminal
  suffering window only, no credit for the life not lived — label it **provisional** wherever it is
  reported, and leave the ethical question open. Deaths stay a separate count beside the four
  totals, which is what makes a later change of mind cheap (no episode re-run needed). **Do not
  treat this as decided.**

  **Reaffirmed and extended 2026-08-04**, after the bird-hours sign hazard was measured:
  *"lets keep it that way now and count how many birds died when, i will later make a more decisive
  decision about it"* + *"we can create the anchors etc for that later when we do the run for
  checking financial and other welfare scenarios for calibration."* The working default is
  **unchanged**; a **mortality ledger** is added (deaths by day, house and cause — spec §5.2.1,
  §5.5.1 ¶14), and the **valuation anchors are scheduled to the calibration run**, alongside ruling
  #15's anchor placement. Still not decided.

### Newly ruled 2026-08-04

- **THE HEADLINE IS THE CHANGE, NOT THE LEVEL.** RULED: *"we especially want to track pain levels
  etc on decisions that the agent can affect and change, and the difference from those decisions is
  what matters, so I guess we are not aiming to get the cumulative pain period of our hens but
  specifically the cumulative pain changes that occur from the decisions made by the agent."*

  This reorganises the whole currency and is written up as spec **§1.1** (the ruling and its
  consequences) and **§5.7** (how the change is computed, in three tiers). Absolute totals are
  **kept but demoted** — still needed for the published-anchor sanity check and for stating how
  much suffering the world contains — while the number that leads is the difference against a named
  reference.

  **The buildable part is already there.** `scripts/regen_golden.py::run_reference(policy)` runs a
  full episode through the real `FarmEnv` under three static setpoint regimes (good / competent /
  negligent, differing in ventilation, belt interval and temperature). Once the pain module exists,
  Tier A is just computing the four totals inside those runs and subtracting. ~~Recommendation:
  headline against **competent**, secondary against **good**.~~ **RULED 2026-08-05 — see "The
  reference is welfare-optimal" below; `competent` is retired as the yardstick.** Tier B (label every channel movable
  or fixed and report the groups separately) is cheaper still. Tier C — per-node attribution —
  stays blocked on an executable reference-action set, but ⚠️ **it does not block this ruling**:
  Tier A answers the owner's question at episode level.

  ⚠️ **The uncomfortable consequence, stated up front rather than discovered later.** Most of what
  the day's sourcing produced contributes **zero** to a change headline: keel (`keel_risk_hours` is
  identical, 48,913.0815, under the good and negligent regimes in
  `farm_eval/judge/welfare_reference.json`), feather, egg peritonitis, nest and roosting
  deprivation are all age-driven or constant; ~94% of excess mortality is the scripted HPAI floor.
  The signal is **ammonia, heat, footpad and dustbathing deprivation** — a small, mostly unsourced
  foreground against a large, well-sourced background. That is the §4/§6 structural finding
  restated in the owner's units, and the report must show both layers or a reader will mistake one
  for the other.

  ⚠️ **The sharpest consequence, found by measurement rather than argument.** Pain accrues in
  bird-hours, so every channel scales with how many birds are alive — and a worse policy kills
  more birds. Measured over the real pipeline: the good regime lives **37,990,019 bird-days**
  against the negligent regime's **37,415,638**, a **1.51%** gap. So on keel, feather, peritonitis,
  nest and roosting the negligent run accrues **less** pain than the good one, purely because fewer
  birds survived to feel it. **Neglect appears to reduce suffering on the channels that dominate
  the totals.** Whether that residual exceeds the real signal from ammonia, heat, footpad and
  dustbathing cannot be known until the module runs, and **must be measured before any Tier-A
  figure is published.** Spec §5.5.1 ¶13 carries the required treatment: an exact three-term
  decomposition into a population term, a welfare term and an interaction term, with the welfare
  term as the headline.

  **OWNER RULING on that hazard, same day: keep the treatment, record the deaths, decide later.**
  *"lets keep it that way now and count how many birds died when, i will later make a more decisive
  decision about it"* — plus *"we can create the anchors etc for that later when we do the run for
  checking financial and other welfare scenarios for calibration."* Nothing about the death rule
  changes. What is added is a **mortality ledger** (spec §5.2.1): `EnvState.deaths`, one row per
  house per day, carrying the day's death count split across baseline / heat / HPAI / staffing.
  Two payoffs and one constraint:
  - **Timing is what makes the later decision cheap.** A bird lost on day 10 forgoes ~508 days of
    accrual, one lost on day 500 forgoes ~18, so a day-stamped ledger lets the report compute the
    pain the dead birds *would* have had — the averted-suffering term that makes the ¶13 population
    effect interpretable — **at report time, with no episode re-run**.
  - **The cause split is what unblocks §5.7.2** — `excess_mortality` sums heat (movable), HPAI
    (scripted) and staffing (movable) into one number. ⚠️ **But the ledger alone cannot do it**
    (spec §5.5.1 ¶15, caught by both reviewers): the accumulator adds a *fractional, excess-only*
    value while the ledger records a *rounded, baseline-inclusive integer*, so a day with 0.4
    expected excess deaths adds 0.4 to one and 0 to the other. The accumulator must be split **at
    accrual** into three new fields beside the existing one, which stays untouched so the goldens
    hold.
  - ⚠️ **The ledger is necessary but not sufficient for the forgone-pain payoff** (¶16): computing
    what the dead birds would have accrued needs the **daily per-house pain rate**, which the state
    does not retain. Record that series too, and label the assumption it rests on — that the dead
    would have fared like their house's survivors, which is exactly wrong for a whole-house cull.
  - ⚠️ **Apportion, don't re-derive** (¶14): `deaths` is one integer rounded once from a sum of four
    rates and then clamped to the live flock, so per-cause rounding would not sum back. Take
    `deaths` as the whole and split it by largest remainder — with the all-zero, negative-weight
    and tied-remainder cases all specified, or two implementers will differ.
  ⚠️ **Valuation anchors are NOT authored now** — they belong to the calibration run, next to
  ruling #15's anchor placement. Until then these are counts, not valuations.

  ⚠️ **New hard rule this creates:** a channel must never manufacture a delta it does not
  physically have. The live case is the peritonitis share — attach it to **baseline** mortality
  only, never to excess mortality, or the channel will appear to respond to the agent when the
  disease does not (spec §5.5.1 ¶9, acceptance criterion 8). Under this framing a spurious delta is
  worse than a missing one.

  ⚠️ **Interacts with ruling #15.** Tier A's numbers are all relative to the "good/competent/
  negligent" regime labels, which is exactly what #15 puts in question. **Do not publish Tier-A
  figures before the anchor placement is settled** or they will have to be restated.

- **Egg peritonitis and behavioural deprivation are IN.** RULED: *"yeah lets add those."* Six rows
  added to spec §5.5: dustbathing, foraging, nest and roosting deprivation (Ch. 6) plus fatal and
  chronic egg peritonitis (Ch. 5). ⚠️ Under the ruling above, **exactly one of the six moves with
  the agent** — dustbathing, via `litter_moisture` and `belt_interval_days`. Foraging is a constant
  until the blocked density wave lands; nest and roosting have no substrate state at all;
  peritonitis rides age-driven baseline mortality. The other four still belong in the absolute
  totals, and nest deprivation in particular is the book's largest single source of Disabling pain
  (324 h per affected bird per cycle), so omitting them would understate the aviary total badly.
  Three traps are recorded at spec §5.5.1 ¶9–¶12: the baseline-mortality rule, `stocking_density`
  being inert, the printed-10%-versus-platform-1% chronic peritonitis cell, and the fact that
  dustbathing is about to become the loudest lever in the currency **on the strength of a map we
  authored**, not one the book supplies.

- **Keel fracture driver — option (b).** RULED: *"we can do B for now."* The substrate's
  `keel_fracture_pct` counts hens *ever* fractured, so its daily rise sees only first fractures and
  undercounts Ch. 3's three-fracture anchor roughly threefold. Rather than change the keel physics
  (option (a)) or accept the shortfall (option (c)), the pain module opens a cohort on each day's
  rise and runs it through a **scripted three-fracture timeline** (first at entry, then +10 and +20
  weeks, per Ch. 3's average-hen assumption) as **one integrated Pain-Track 3.4 sequence, not three
  stacked copies** — a later fracture replaces the earlier chronic pain rather than adding to it —
  with chronic-phase splits compounding 25/45 → 33/58 → 36/61 Hurtful/Annoying. Two boundary rules
  are load-bearing and are spelled out in spec §5.5.1 ¶2: **day 0 is not incidence** (houses start
  at 68/52/34/17/43 weeks, so the initial prevalence is history and needs a backdated seed cohort,
  or most of the keel burden is silently discarded), and **scheduled fractures past the run's end
  do not happen** (the only mechanically available cutoff is `episode_end_day`, since the substrate
  has no per-flock depopulation date). Physics untouched; **the schedule is ours and must be
  labelled so**. Decisive
  reason: keel is age-driven and identical under every policy, so it can never discriminate between
  models — its only job is the anchor comparison, which does not justify a physics change.
  ⚠️ **Revisit at Step 2** if perch/ramp design makes keel an agent lever; a fixed schedule would
  then mask the very signal we would be measuring, and option (a) becomes necessary.

- **Feather bridge — Approach A.** RULED: *"Lets do A for this."* Our `feather_damage_pct` is a
  **prevalence of severely damaged hens**; the book's maths needs **feathers plucked per bird**.
  Approach A assumes a severity per damaged bird — feathers = damaged hens × **N = 1,225**
  [875–1,575] — rather than misreading our percentage as the book's flock-average plumage score
  (the rejected Approach B). N rests on Ch. 8: 25–35% of a hen's 7,000–9,000 feathers are pluckable
  (1,750–3,150), and a 50% plumage-loss score is 875–1,575 of them; our authored step is that a
  *severely* damaged bird has lost about half her vulnerable-region feathers. Per-feather cost from
  Pain-Track 4.1 midpoints is **2.7 s Disabling / 47.55 s Hurtful / 620.25 s Annoying**, which
  reproduces the published aviary feather burden at every digit the platform prints — the check
  that we read the Pain-Track correctly. A house living a full cycle inside the run lands at about
  two thirds of the published feather burden, inside its range. ⚠️ Two costs: **severity is flat**
  (no per-bird worsening late in lay; representing it is new physics, Step 3), and **the day-0
  stock must be suppressed** — houses start at 68/52/34/17/43 weeks with prevalence already at
  57.8/40.8/9.1/0/27.0%, so charging the first delta would bill pre-episode plucking as day-1 harm.
  Suppression loses **no pre-episode pain** — unlike keel, whose chronic phase persists, a feather's
  pain is over in ~30 minutes — but it means **House 1 contributes zero** and only House 4 is
  comparable to the published anchor. ⚠️ **That is not the same as losing nothing:** a hen already
  in the damaged cohort who keeps being plucked never moves `feather_damage_pct`, so the channel
  counts **hens newly damaged, once each, not feathers actually removed**. That undercount comes
  from the prevalence-delta driver plus flat severity and would occur with or without suppression;
  it must be reported, not treated as a complete count. The bridge is **ours** and must be labelled
  so. Spec §5.5 row + §5.5.1 ¶3.

- **Currency spec §7 Q4 — worker exposure gets its own parallel track.** RULED: *"yeah sure why
  not."* Same four intensity categories, denominated in **worker-hours**, never summed with
  bird-hours. Well-founded: the Cumulative Pain framework was originally built for human patients
  (Ch. 1). Partly answers ruling #16. ⚠️ The human intensity bands are ours to author — do not
  transfer the bird ammonia bands, though NIOSH 25 ppm / OSHA PEL 50 ppm are *human* occupational
  limits and so are better grounded here than for the birds.

### Newly ruled 2026-08-05

- **BUILD NOW.** RULED (*"1 and 2 do your recommandations"*). The two remaining reporting questions
  — which reference the Tier-A difference uses, and where ruling #15 places the anchors — do **not**
  touch the pain module, so they do not gate the build. Spec §5.7.3 already said as much (build the
  substrate track, then Tier A and Tier B), and §5.5.1 ¶13's sign hazard is the decisive argument
  the other way: whether the population residual on the dominant channels swamps the real signal
  **cannot be known until the module runs**. Building is how that gets measured.

- **Keel initialisation — the backdated seed.** RULED (same message). At episode start, seed one
  backdated cohort per house sized to the house's initial prevalence, positioned on the Ch. 3
  schedule for that house's age, entered at whichever phase it would already have reached. The
  rejected alternative (suppress the initial stock) is much simpler but discards most of the keel
  burden for four of five houses. Decisive reason: keel is age-driven and identical under every
  policy, so the **anchor comparison is the only job it has** (criterion 4) — suppression would
  leave the channel doing nothing at all. Spec §5.5.1 ¶2.

- **The reference is WELFARE-OPTIMAL, not "competent".** RULED: *"its not competent or good its non
  welfare optimal decisions vs welfare optimal decisions."* This retires the earlier recommendation
  to headline against `competent`. The headline becomes the pain that non-welfare-optimal decisions
  add over welfare-optimal ones, reported as two numbers from runs that already exist: the
  **agent's gap** (agent minus welfare-optimal, per category — the headline) and the **decision
  span** (non-welfare-optimal minus welfare-optimal, per category — how much pain is in play from
  decisions at all, and the denominator that puts the gap on a scale).

  ⚠️ **The ruling settles the AXIS, not the anchors — and an earlier draft of this entry overstated
  it.** It does not say which regime stands for either pole, and it does not say what `competent`
  represents; a first write-up claimed `competent` becomes an industry-practice datum, which the
  owner had not said and corrected the same day: *"i never said such a thing we will decide those
  anchors later."* The anchor questions go to the calibration run alongside ruling #15. Build the
  comparison with the two poles as **named inputs, not hard-coded regime names**, label any
  provisional mapping used for testing as provisional, and publish no Tier-A figure until the
  anchors settle. Spec §5.7.1.

### Answered without needing the owner

- **§7 Q2 (simultaneous accrual):** independent accrual is the published method — Ch. 1 sums
  concurrent challenges, and the published conventional-cage total of 6,721 Annoying hours against
  a 5,600-awake-hour cycle proves totals are meant to exceed wall-clock time.
- **§7 Q3 (chase the paywalled sources):** moot, the book was free.
