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

**#10 — Cold-feed coefficient (ours 2.8%/°C vs NRC 1.5%/°C)?** **UNANSWERED.**

**#11 — Temperature band (18 °C vs the measured commercial 24.6–26.7 °C)?** Owner wrote *"yes lets
double it, lets add the source for there too."* ⚠️ **AMBIGUOUS — do not act.** Neither #10 nor #11
is a "double it": matching NRC means roughly *halving* our cold coefficient, and the temperature
question was whether to move the target *up*. **Blocking clarification needed before either
constant is touched.**

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
     engagement ratio in `run_sweep.py`; `docs/pilot/assets/tool_usage.png` shows prior art.)

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

⚠️ The fetched copy of the Animal Ask post came back **truncated**, and its extracted worldview
weight table is **internally inconsistent** with the post's own worked sentence (the table shows
Annoying weighted above Disabling; the prose says higher intensity carries the higher weight).
**Do not hard-code any weight set from that extraction.** Weights must be taken from a
source read in full, or authored by us and labelled as ours.

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

## 4. Blockers requiring the owner

1. **#10/#11 ambiguity** — which coefficient, which direction. Nothing in Step 3 can start
   without it.
2. **The four Task-6 decisions** (ammonia belt response, belt→moisture curve, the water-input
   reference, and whether the density wave continues or is re-planned).
