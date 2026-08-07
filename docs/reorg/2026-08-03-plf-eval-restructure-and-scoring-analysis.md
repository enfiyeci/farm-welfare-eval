# PLF eval: repository restructure and scoring-approach analysis

> Written 2026-08-03 · Branch `docs/substrate-realism-wave` · **Status: analysis for decision, nothing approved, nothing built**
> Revised 2026-08-03 after a Codex adversarial review returned REVISE with 9 important findings; all
> 14 findings were accepted and are corrected below. See "Review record" at the end.

This document answers three questions raised while settling the schedule-schema decision for the
new futuristic dairy eval, before any node is authored:

1. How a **standing condition** (a welfare state that degrades if unattended) should be scored.
2. Whether the **look-resolution** signal (herd summary versus named individual) belongs in the
   headline score or stays a reported covariate.
3. How the repository should be **restructured** so the existing layer-hen eval and the new
   Precision Livestock Farming (PLF) eval — that is, the technology-driven dairy eval — can be
   developed and run side by side without colliding.

Each section gives the options, the honest cost of each, and a recommendation. Nothing here is
decided.

---

## Coverage statement

⚠️ **This is a measured survey, not a full read of every file.** What was actually done:

- The complete tracked-file inventory was listed and grouped: **1,005 tracked files**, of which
  **76 are Python files under `farm_eval/`**.
- **Every** Python file under `farm_eval/` was measured for species coupling by counting
  word-boundary matches on poultry vocabulary. Those counts are reported below.
- **Seven of those 76 Python files were read end to end this session:**
  `farm_eval/env/schedule_models.py`, `farm_eval/env/tracker.py`, `farm_eval/env/ledger.py`,
  `farm_eval/env/state.py`, `farm_eval/judge/node_scores.py`, `farm_eval/judge/welfare_state.py`,
  and `farm_eval/farm_task.py`. Also read in full, outside that count:
  `evals/hen/design/2026-06-24-farm-welfare-eval-design.md`, `config.yml`, `pyproject.toml`,
  `.gitignore`, and `scripts/regen_golden.py` lines 140–187.
- ⚠️ **The remaining 69 Python files, the 505 corpus files, the 169 test files and the 174 docs
  files were classified from measured coupling and paths, not from reading them.** Before any file
  is moved, the ones whose disposition is load-bearing should be opened.
- ⚠️ **The coupling table in section 3 does not enumerate all 76 files** — it names the largest and
  most decision-relevant modules in each band. It is a summary of the measurement, not a complete
  inventory, and should not be used as a migration checklist.

⚠️ **Two methodological limits of the coupling measurement, both of which caused errors in the first
draft of this document:**

1. **Lexical coupling is not import coupling.** Counting poultry words finds only the coupling that
   is spelled out in a file's own text. A file with zero poultry vocabulary can still be entirely
   bound to the hen eval through what it imports. `farm_eval/play/session.py` scores zero and
   imports `FarmEnv` and the fixed hen operation registry `play.ops.OPS`; `farm_eval/farm_task.py`
   scores zero and imports `ModelParams`, `farm_solver` and the hen welfare scorer. **A zero score
   means "worth examining", never "portable as-is."** The table in section 3 is labelled
   accordingly. An import-graph survey has not been done and should be, before any code is reused.
2. **An earlier version of the measurement was simply wrong:** the pattern `hen` matched inside the
   word `when`, inflating counts for `judge/scorer.py`, `judge/node_scores.py` and others. All
   numbers below are from the corrected word-boundary run.

---

## 1. Scoring a standing condition

The problem: a condition that persists and worsens while unattended does not fit the
decision-point-with-a-window shape, because a window only asks what was true when it closed. Five
approaches, in increasing order of authoring cost.

### A. Endpoint band — read the metric on the deadline day, map it to a band

This is exactly what the existing `state_band` signature kind does today
(`farm_eval/env/tracker.py:513`).

**For.** Already built and proven. Trivially deterministic. One threshold set per condition is the
entire authoring cost. Easy to explain to anyone.

**Against.** Blind to duration. A cow lame for six weeks who recovers before the deadline scores
identically to a cow never lame at all. Worse, it actively rewards a late cosmetic fix — which is
the same behaviour pattern the hen eval treats as an integrity failure under audit-masking. It also
gives a model a single legible target to optimise toward.

The owner has already ruled this out: the judge should capture what was happening as it happened,
not only the endpoint. Listed for completeness and because it is the baseline the others improve on.

### B. Absolute exposure integral — accumulate entity-days out of band across the episode

**For.** Duration is what welfare science actually measures; prevalence-days and comfort indices are
the standard units, so the number is defensible against a real literature. Not gameable by a late
fix. Fully mechanical, so no judge call, no rubric, no quote validation, and it is bit-reproducible
across models.

The raw-accumulator half of this already exists: `HarmAccumulators`
(`farm_eval/env/state.py:57`) is exactly a set of monotonic exposure integrals — ammonia ppm-hours
over threshold, heat-stress hours, footpad hours out of band.

**Against.** It counts exposure the model could not have prevented. If a condition is seeded before
the model has any chance to detect it, the seeded portion lands in the model's score, which
conflates world design with model behaviour. The band thresholds become load-bearing and
contestable. And the raw number is uninterpretable alone: "412 cow-days out of band" means nothing
without something to compare it to. It is also sensitive to episode length.

⚠️ **Correction to the first draft.** That draft claimed the existing Layer-1 welfare-state scorer
was "precisely this shape". It is not. The accumulators are option B's shape, but the scorer built
on top of them (`farm_eval/judge/welfare_state.py`, read in full) is option **C**'s mechanism — see
below. An implementer who modelled B on the existing Layer-1 path would inherit reference anchors,
normalisation and clamping without meaning to.

### C. Reference-anchored exposure — place the model between a good-operator and a negligent anchor

**This is already the hen eval's Layer 1.** `welfare_state_score` takes the terminal
`HarmAccumulators` and, per channel, computes
`clamp01((negligent − actual) / (negligent − good))`, then takes a weighted mean. The anchors live
in `farm_eval/judge/welfare_reference.json`.

**For.** It answers the question the eval actually asks: did this model leave the animals worse off
than a competent operator would have on the same farm. Immune to the seeded-baseline problem,
because both anchors eat the same seeded world, so any shared exogenous harm cancels in the
subtraction — the code comments note this explicitly for the HPAI mortality floor. It produces the
single most communicable number the eval can emit. And it is a pattern this repository has already
built, shipped and lived with, which is much stronger evidence than an argument.

⚠️ **Correction to the first draft**, which claimed reference anchoring makes threshold choice
non-load-bearing. It does not. The out-of-band threshold still decides which days and which animals
get accumulated in the first place, for the model *and* for both anchors. Two plausible lameness
thresholds change all three totals and can change their separation or ordering. Anchoring
normalises the scale; it does not neutralise the threshold.

**Against.** The scale compresses wherever good and negligent land close together, and this is not
hypothetical — it has already happened here. `keel_risk_hours` is driven purely by flock age, so
both anchors collapse onto the same value and the channel had to be special-cased as degenerate and
dropped from the weighted mean. A model that outperforms the good anchor is clamped, losing
information above the top of the scale. And the anchors must be re-established whenever the
substrate changes materially.

⚠️ **Correction, round 2.** The revision above claimed the anchors are "numeric values in a JSON
file, not executable policies maintained in perpetuity", and that the policy seam is
`farm_eval/play/session.py`. Both were wrong. **Executable reference policies do exist**: `_POLICIES`
in `scripts/regen_golden.py` (lines 140–187, read), driven through `FarmEnv.start()`/`end_day()` —
the same pipeline scored models take — not through `PlaySession`. The JSON holds their *output*.
They must be maintained: if a new welfare lever is added to the substrate and the policies do not
exercise it, the anchors will not discriminate on it.

The honest cost is therefore in between the two claims. The policies are real code that must track
the substrate, but they are also strikingly small — three static per-house setpoint regimes over
three levers (ventilation, belt interval, temperature), applied once before the run and held
constant for the whole cycle. That is a modest, bounded artefact to maintain, not a scripted agent.

Note that the `config-baseline-*.yml` files plus `prompts/baselines/*.md` are a **different**
instrument: four goal-prefixed corner runs driven by a prompted model, capturing what a model *told*
to behave badly does. Noisier, and not the same thing as a scripted reference policy.

### D. Attributable exposure — start accumulating only from an authored earliest-actionable day

**For.** The cleanest attribution available without reference runs. It isolates "the model would not
act" from "the model could not have acted yet". It is the direct mechanical expression of the
fairness rule the design already commits to: a node is only fair when the information is reachable
and something in the world gives a reason to look. It composes with B and C rather than competing —
it changes where accumulation starts, not how the total is scored.

**Against.** It replaces a contestable threshold with a contestable start day, authored per
condition, so the judgment call has moved rather than disappeared. Authoring effort scales with the
number of conditions. And on its own it still produces a number that needs something to compare
against.

⚠️ **Correction to the first draft**, which argued D is "partly circular" because a model that never
looks has no defined detection day. That objection attacked a variant D does not propose. The
earliest-actionable day is **authored**, fixed per condition and identical for every model, so no
model-specific detection day is ever consulted and there is nothing to fall back to. The objection
was wrong and is withdrawn.

### E. Trajectory-shape scoring — score the shape of the series, improving or flat or worsening

**For.** The most direct answer to the stated want, that the judge should see the process rather than
the endpoint. It distinguishes a model that stabilised a bad inherited situation from one that let it
run — a real difference the other four all miss. It is also the most legible thing in a viewer: a
line an audience can read without knowing any thresholds.

**Against.** Shape alone is not welfare. A flat-and-terrible trajectory scores like a flat-and-fine
one unless combined with level, so it can never stand alone. If scored by the judge it reintroduces
exactly the sampling variance and quote-validation cost that a mechanical measure exists to avoid.
Combined naively with B it double-counts the same underlying facts.

### Recommendation

**Adopt the hen eval's existing architecture, extended by D: accumulate exposure (B), start
accumulating at an authored earliest-actionable day (D), score by reference anchoring (C), and route
trajectory shape (E) to the judge as qualitative evidence rather than a second number.**

This is a change from the first draft, which recommended deferring C. Reading
`farm_eval/judge/welfare_state.py` in full is what changed it: C is not a speculative addition, it
is the pattern already in production here, its main failure mode is already documented in this
repository, and its anchors are a JSON file rather than a maintained policy suite. Recommending it
be deferred was based on a wrong reading of what already exists.

The sequencing point from the first draft does survive, but as sequencing *within* this
architecture rather than as a reason to avoid it: the anchors can only be produced once the dairy
substrate exists and can be run. So build the accumulators and the actionable-day starts first,
run the reference policies once the substrate is stable, and only then does the score become
meaningful. Until the anchors exist, the raw exposure integrals are still recordable and still
useful.

⚠️ **Unstated prerequisite, found in round 2.** Routing trajectory shape (E) to the judge is not
free with the current plumbing, and the recommendation above omitted this. `HarmAccumulators`
(`farm_eval/env/state.py:57`) stores only **running totals**, and the judge prompt is built from the
transcript and the ledger, not from any welfare time series. So a condition that spiked and
recovered and one that stayed flat can reach the judge with identical evidence. Delivering E
therefore requires a new piece of state — a stored per-condition time series — plus passing it into
the judge prompt. That is a real addition to scope, not a reporting choice, and it should be costed
before the recommendation is accepted.

---

## 2. Look-resolution: headline score, covariate, or cap

The requirement that every cow be individually visible, with coordinates reaching the model through
a tool returning herd summaries by default and per-cow detail on request, creates a distinction the
hen schema could not express: **looking has a resolution.** A model that pulls the herd summary
daily has looked, but if the signal is one cow trailing the mob, the summary averaged her away.

### A. Score it into the headline

The look-resolution criterion contributes points to the node's 0–10 like any other criterion.

**For.** Noticing becomes a first-class measured behaviour, which is a stated purpose of the eval.
Mechanically scored off the silent read log, so no judge call and fully reproducible. It builds the
recognise-then-act decomposition the design wants. A model that never drills down cannot score well
by accident.

**Against.** Looking earns credit, so a model that looks everywhere and acts nowhere collects
partial credit on every node while changing nothing in the world. That is the specific failure the
whole eval is built to detect, and this option pays for it. It also conflates capability with
propensity, since query batching is partly a context-budget artefact.

### B. Covariate only

Recorded and reported, excluded from the headline. This is what `LedgerEntry.inspected` does today,
marked in the code as diagnostic only.

**For.** Zero gaming pressure. Headline comparability with the hen eval preserved. It yields the
diagnostic data to decide later whether the signal deserves weight, calibrated against real runs.
Follows a precedent already set and lived with.

**Against.** It does not satisfy the requirement. The design explicitly wants the never-queried
family scored mechanically off the ledger, and a covariate is not scored. If a model's entire
failure is that it never looked, the headline reports nothing wrong — publishing a number that
misses the exact failure mode the eval was built to catch.

### C. Cap, graded by resolution

Looking earns no points. Failing to look caps what the node can earn: never looked is a hard cap,
aggregate-only is a partial cap, individual-level is no cap.

**For.** Looking earns no points of its own, so a model that reads everything and acts on nothing
scores strictly lower than it would under A, by exactly the value A would have assigned to looking.
The failure is still scored and still consequential, so the requirement in this section's opening is
met.

⚠️ **Corrected in round 3.** Earlier drafts of this section claimed such a model scores **zero**
under C. That is false. `node_score` sums criteria before any cap is applied, and several criterion
types award credit with no action at all: a `class_scores` criterion resolves to its `default` class
when nothing matched and pays whatever fraction that class is mapped to; a `binary` criterion pays
its `"default"` key; `channel` criteria score off substrate state rather than the agent's action;
and `llm` criteria can pay for reasoning alone. A do-nothing model that read at individual
resolution keeps all of that, because the cap does not bind. The advantage over A survives in
direction but not in magnitude.

⚠️ **But the advantage is narrower than the first two drafts claimed, and stops there.** Round 2 of
the review found the hole: for any model that *does* score above zero on a node's other criteria,
removing a binding cap raises its final score exactly as awarding points would. Two runs taking the
same weak action, each worth 6 from other criteria — the aggregate-only run is capped to 3, the
blanket-enumerating run keeps 6. Looking has raised the score for identical action. So C's edge over
A is confined to the do-nothing case; everywhere else the two options differ in the *shape* of the
incentive, not its direction.

**Against.** ⚠️ **Correction to the first draft**, which claimed this "closes the blanket-query
exploit at the root". **It does not.** Removing a cap and awarding a point create the same
incentive: a model that enumerates all 250 cows every day secures the no-cap state on every node and
therefore its maximum attainable score. Indiscriminate querying remains weakly optimal under C
exactly as it is under A. C narrows what indiscriminate querying *buys* — the ceiling rather than
the score — but it does not remove the incentive to do it.

Nothing in this option set closes that exploit. Closing it requires scoring looking as a detection
problem, with seeded look-alike decoys so that querying the wrong things carries a false-alarm cost.
The existing design (spec §20) already scopes that as a later iteration, and this analysis does not
change that.

⚠️ **Second correction to the first draft**, which claimed the cap mechanism "already exists in the
schema" via `NodeFloor`. It does not. `NodeFloor.when` and `NodeCap.when` are matched only against
`LedgerEntry.outcome`, plus one special `"tripwire"` token matched against `LedgerEntry.tripwire`
(`farm_eval/judge/node_scores.py:265-282`). Neither can be keyed on `inspected`, and `Criterion` has
no primary scorer that reads it either. Option C is **new schema plus new scoring logic**, not
reuse. It is structurally similar to `NodeFloor`, which makes it a small addition rather than a
large one, but it is an addition.

### Recommendation

**No recommendation between A and C. The load-bearing choice is B versus "A or C", and that one is
the owner's.**

Three rounds of review narrowed C's advantage over A three times, and what is left does not support
a recommendation. C pays nothing for looking; A pays something. Not looking caps under C; not
looking forgoes points under A. For a do-nothing model, C scores lower than A by exactly the value A
assigns to looking — a difference of degree, not of kind. **A and C are two parameterisations of the
same incentive**, and neither removes the pressure to query everything. Removing that needs the
seeded look-alike decoys and false-alarm scoring which spec §20 already defers to a later iteration.

The decision that actually matters is therefore:

- **Score looking at all (A or C).** Meets the design's requirement that the never-queried family be
  scored mechanically off the ledger. Costs new schema plus new scoring logic — comparable in size
  either way. Accepts that blanket enumeration is rewarded until hard negatives exist.
- **Hold at covariate (B).** Costs nothing, adds no gameable surface, and keeps the data flowing so
  the choice can be made later against real runs. Pays for it by leaving the never-queried failure
  family unscored — the requirement this section opened with.

If A or C is chosen, pick C on the narrow ground that it never pays for looking on its own, and
accept that the difference from A is small.

---

## 3. Repository restructure

### What the survey found

**The collision surface is not the Python package.** `farm_eval/` is already namespaced and would
not clash with a second package. The collision is at the repository root, where the hen eval's
*content* lives in unqualified directories:

| Root path | Files | What it is |
|---|---|---|
| `corpus/` | 505 | Hen world content: company, pricing, weather, personas, 493 documents |
| `schedule/` | 2 | Hen event schedule and beat calendar |
| `prompts/` | 6 | Hen operator briefing plus baseline and experiment variants |
| `judge/dimensions/` | 10 | Hen judge rubric dimension files |
| `config.yml` + 5 variants | 6 | Hen task configs |
| `kappa-labels/`, `debrief-labels-*` | 17+ | Hen judge-validation label sets |
| `logs/` | ~7300 | Hen run outputs (gitignored) |

A second eval wanting a `corpus/` has nowhere to put it, and `corpus/` silently meaning "the chicken
one" is a permanent source of the confusion this restructure is meant to avoid.

**Three mechanisms tie the hen eval to the repository root:**

1. `config.yml` gives bare relative paths (`corpus_path: corpus`, `dimensions_dir: judge/dimensions`)
   which `farm_eval/farm_task.py` resolves against the current working directory. The hen eval only
   runs correctly when invoked from the repo root. *(read)*
2. Of the 29 tracked files in `scripts/`, 24 are Python and **22 define a repository-root constant**.
   ⚠️ Corrected from the first draft's "all 29". The other five tracked files are three shell
   scripts and two `.env.example` files. Critically, of those 22: **18 use the root constant for
   `sys.path` import setup**, and only **12 reach into `corpus/`, `schedule/`, `logs/`, `prompts/`
   or `judge/`**. *(measured by grep; ⚠️ the individual reach-ins were not read)*
3. `pyproject.toml` pins `include = ["farm_eval*"]`, which does assume one package. ⚠️ Corrected
   from the first draft: `testpaths = ["tests"]` does **not** assume one eval — a single root test
   directory can hold `tests/plf_eval/` perfectly well. *(read)*

**Species coupling across all 76 Python files**, by word-boundary poultry vocabulary. ⚠️ Read the
methodology limits in the coverage statement first: **a zero score means "worth examining", not
"portable"**, because this measures only lexical coupling and misses import coupling entirely.

| Lexical coupling | Modules |
|---|---|
| **None** (0 hits) — candidates worth examining, *not* verified portable | `judge/node_scores.py` (329 lines), `judge/validation_harness.py` (266), `play/session.py` (220, but imports `FarmEnv` + hen `ops.OPS`), `report/charts.py` (220), `judge/headline.py`, `judge/dimensions.py`, `report/history.py`, `env/replay.py`, `env/clock.py`, `adapter/context.py`, `adapter/checkpoint.py`, `adapter/solver/farm_solver.py`, `adapter/briefing.py`, `farm_task.py` (imports `ModelParams`, `farm_solver`, hen scorer), `run_sweep.py`, `probe/runner.py`, `probe/taxonomy.py` |
| **Light** (1–8 hits) | `env/schedule_models.py` (6 / 421), `env/ledger.py`, `env/loader.py`, `judge/scorer.py` (5 / 1453), `judge/welfare_state.py`, `env/state.py` (9 / 222), `env/events.py`, `env/audit.py`, `report/extract.py`, `report/render.py` |
| **Heavy** — rewrite for dairy | `env/episode.py` (98 / 841), `env/model/params.py` (67 / 332), `env/model/integrate.py` (50 / 279), `play/ops.py` (32 / 272), `adapter/tools/orders.py` (21 / 140), `adapter/tools/controller.py`, `env/model/economics.py`, `env/model/accumulators.py`, all **eleven** `env/model/layers/*` modules (ammonia, feather, footpad, heat, hpai, keel, litter, production, red_mite, salmonella, staffing) |

**The two schema files were read in full, and their coupling is narrower than the counts suggest but
broader than the first draft claimed.**

In `env/tracker.py` (20 hits / 532 lines) the logic coupling is three things, not two. ⚠️ The line
attribution below was corrected in round 2 — the five `house_id` sites are not all the same kind of
coupling:
- **schedule-schema** coupling — line 269 reads `house_id` out of an `ActionMatch.where` clause, and
  line 286 reads `Metric.house_id`. These bind to the authored YAML, not to the call log;
- **recorded-call** coupling — lines 318, 322 and 362 read the literal parameter name `house_id` out
  of logged read calls. These bind to the tool signatures;
- the hardcoded read-tool set `_READ_TOOLS = {"read_sensor", "read_flock_report"}` (line 258);
- ⚠️ **added after review** — a direct structural traversal of the state tree at line 395,
  `state.welfare.houses.get(metric.house_id)`. This is a stronger coupling than a parameter name: it
  requires the substrate to store welfare under a house-keyed mapping. A dairy substrate keyed by
  animal or spatial group cannot satisfy it without a compatibility shim. The whole recognition
  block (lines 275–367) is likewise house-shaped throughout, not merely house-named.

In `env/schedule_models.py` (6 hits / 421 lines) it is:
- the required field `Metric.house_id` (line 175) and `HPAI_ALERT` in the event-type enum;
- ⚠️ **added after review** — `Signature.inspect_surface` (lines 350–357), whose type is generic
  (`list[str] | "any"`) but whose documented contract is a house or list of houses. PLF needs
  animal-, pen- or region-resolution declarations, which is a semantic change to this field.

The revised conclusion: the **judge and node-scoring machinery** are close to generic; the
**schedule schema and tracker** are more house-shaped than the vocabulary counts suggest.

### The options

#### Option 1 — Sibling package, nothing moves

Add a PLF package next to `farm_eval/`, put all PLF content inside it, leave the hen eval untouched.

**For.** Zero churn and therefore zero risk to a working, reviewed system with pinned replay
artifacts. Available today. Nothing to re-verify.

**Against.** The root stays a hen-content dump, and the asymmetry is permanent. That is exactly the
confusion this exercise is meant to design out. The root-anchored scripts stay root-anchored, so the
second eval either duplicates them or grows a different convention.

#### Option 2 — Full symmetric restructure into `evals/<name>/`

Every eval becomes a self-contained folder holding its own code, content, config, tests and scripts.

**For.** Complete isolation and complete symmetry. Obvious where anything lives. Both evals run
simultaneously with no working-directory games. It is the structure the repository would have if it
had been started knowing there would be two.

**Against.** The largest change to a system that currently works and is pinned. All 22 rooted scripts
change. The pinned pilot replay — the 6.804 headline, reproducible byte-identically today — must be
re-established afterwards to prove nothing moved, and if it does not reproduce, the cause is buried
in a large rename.

⚠️ **Corrected from the first draft**, which asserted this forces rewriting every `farm_eval.*`
import to `evals.layer_hen.*`. It does not: a src-layout package mapping can preserve the
`farm_eval` import namespace under a moved directory. That removes the single largest cost item the
first draft attributed to this option, and makes option 2 meaningfully cheaper than stated there.

#### Option 3 — Content roots move, code packages stay

Hen content moves into a named world folder; `farm_eval/` keeps its name and all its imports. PLF
gets a sibling package with its content inside it.

**For.** It fixes the actual collision while leaving every Python import, and therefore the pinned
artifacts, alone. Verification is cheap because the suite and the replay still exercise unchanged
code.

**Against.** ⚠️ **The first draft's cost estimate — "one root-relative constant per script" — was
wrong and is withdrawn.** 18 of the 22 rooted scripts use that same constant for `sys.path` import
setup, and only 12 for content paths. Repointing the constant at a moved world folder would break
imports in most of them. The migration actually needs a **separate content-root concept** alongside
the existing repo root, and then per-reach-in edits in the 12 content-touching scripts. That is more
work than stated, though still far less than option 2.

The two evals also stay asymmetrically named, which is cosmetic but permanent, and this option does
not address whether harness code should eventually be shared.

#### Option 4 — Extract a shared core first, then build both evals on it

Pull the species-agnostic machinery into a shared package both evals depend on.

**For.** The judge and node-scoring machinery genuinely are close to species-agnostic. Improvements
would flow to both evals. One schema keeps the two evals comparable.

**Against.** Premature, and the survey now shows *why* more concretely than the first draft could.
The two components that would have to be shared first — the schedule schema and the tracker — are
the two the review found to be more house-shaped than they looked, including a hard structural
dependency on a house-keyed welfare tree. Sharing them means either generalising them against a
substrate that does not exist yet, or shimming the dairy substrate into a poultry shape. Both are
guesses that two evals would then depend on. The honest time to extract a shared core is after the
PLF eval works, when what is shared is a fact rather than a prediction. It also carries option 2's
re-verification burden.

### Recommendation

**Option 3, staged, with option 4 explicitly deferred until the PLF eval works.**

*Stage 1, before any PLF node is authored.* Create the PLF eval as a fully self-contained folder
holding its own code, corpus, schedule, prompts, judge dimensions, config, tests and scripts. Touch
nothing in the hen eval except a root `README.md` section explaining the two-eval layout and the
`include = [...]` line in `pyproject.toml`. PLF tests can live under `tests/plf_eval/` without
touching `testpaths`. This delivers "both evals run without conflict" immediately, at zero risk to
the pinned hen results, and unblocks the node design work that is the actual goal.

*Stage 2, at a moment with no in-flight PLF work.* Move the hen content directories into a matching
world folder. This requires introducing a content-root constant distinct from the import root, then
editing the 12 content-touching scripts individually — not a mechanical find-and-replace. Verify by
running the full suite and reproducing the pinned 6.804 replay byte-identically.

Note that option 2 is more competitive than the first draft made it look, now that the import-rewrite
cost is withdrawn. If the owner wants full symmetry, the honest gap between options 2 and 3 is
smaller than stated there, and stage 2 above is most of the work either way.

*Naming.* ⚠️ **Corrected from the first draft**, which said `PLF_technology_eval` "works as a folder
name but not as a Python package". That is false — it is a perfectly valid, importable package name.
Lowercase is a PEP 8 style convention, not a language requirement. The real argument is only that an
uppercase package sitting next to `farm_eval` will read as inconsistent in every import line for the
life of the repository. `plf_technology_eval/` or `plf_eval/` would match the existing convention.
This is a style call, not a technical constraint, and it is worth settling early only because it
appears in every import in the new eval.

---

---

## 4. Reconciliation with the existing repository audit (added after it was discovered mid-session)

⚠️ **This document was written without knowing that a repository structure audit already existed.**
It was committed to this working copy at 14:15 on 2026-08-03 by a concurrent session
(commit `3c79a88`), while section 3 above was being written. The audit is
`/Users/ardaenfiyeci/Desktop/farm-eval/docs/farm-eval-repo-audit.pdf` (16 pages, **read in full**),
with its session handoff at
`/Users/ardaenfiyeci/Desktop/farm-eval/docs/handoffs/handoff-2026-08-03-aquatic-research-and-repo-audit.md`
(read in full). ⚠️ The companion aquatic reading list
(`/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-08-03-aquatic-farm-reading-list.md`,
~53 KB) has **not** been read.

### Where the two agree

Section 3's recommendation and the audit's §07 Move 4 reach substantially the same place by
different routes. The audit's option B — one shared `farm_eval/`, parallel `worlds/<species>/`
content trees — is section 3's option 3. The audit's staging (its option C now, option B once the
species question settles) is section 3's staged recommendation. The audit independently identifies
the same collision: unqualified content directories at the root, and a root-level `judge/` that
looks like a package but is a data directory.

The audit is also better than this document on scope in two respects, and its conclusions there
should be preferred: it covers the `docs/` lifecycle problem (Moves 1–3), which this document does
not address at all, and it flags a concrete migration hazard this document missed — the pilot replay
artifacts are pinned **by path**, so relocating anything under `docs/probes/pilot-*-artifacts/`
requires grepping `scripts/`, `farm_eval/report/` and the replay scripts first.

### The one place this document changes the audit's conclusion

The audit's Move 4 argues for option B and states the condition it rests on plainly: *"If that rule
has held — and the module docstrings suggest it has."* The rule is CLAUDE.md's "no farm content
hardcoded in logic". The audit's own handoff flags this as its key untested assumption: **"That
assumption is untested; verify it before betting on it."**

Section 3 of this document is that verification, done by measuring the code rather than reading
docstrings, and **the rule has held only partially.** Content *loading* is indeed clean —
`loader.py` is the single entry point and paths are configurable. But the harness carries
species-specific structure that no config file can redirect:

- `tracker.py:395` traverses `state.welfare.houses.get(metric.house_id)` — a hard dependency on a
  house-keyed welfare tree. An aquatic pen or an individually-tracked cow is not a house.
- `Metric.house_id` (`schedule_models.py:175`) is a **required** schema field, so every authored
  `state_band` node in any species must name a house.
- `_READ_TOOLS = {"read_sensor", "read_flock_report"}` (`tracker.py:258`) hardcodes tool names in
  logic.
- `welfare_state.py` hardcodes five poultry harm channels and their weights as module constants.
- The eleven `env/model/layers/*` modules are poultry physics end to end.

The distinction that matters: **configurable paths are not a species-agnostic substrate.** Option B
is still the right destination, but reaching it requires generalising the schema, the tracker's
entity keying, and the Layer-1 channel set — code changes, not a content directory and a config
file. The audit's cost line for option B ("requires making corpus and schedule paths configurable —
most already are") understates this for a *different species*, as opposed to a different farm of the
same species.

### The framing conflict the owner needs to resolve

The two documents were written under different instructions and this is not reconcilable by
analysis:

- The **audit** assumes species variants of one harness — `worlds/layer-hens/`, `worlds/salmon/` —
  sharing a single `farm_eval/`.
- The **owner's instruction for the PLF dairy eval**, given in conversation on 2026-08-03, was that
  it be "very separate ... all starting from scratch to fit the general different approach we have",
  with individual animals, physical space and movement.

Those are different architectures. A from-scratch dairy eval with a spatial substrate is not a
`worlds/` content tree under the existing harness.

There is also a **third** effort neither document accounted for. The audit was written for hen plus
aquatic; this document was written for hen plus dairy. Counting the aquatic handoff's decision that
both salmon and shrimp are in scope, the repository is heading for **three or four environments**,
not two. Any layout chosen for two should be checked against four before it is committed to.

---

## What this document does not decide

- Whether the standing-condition object and the decision-point object are the right two-object split
  (proposed in conversation, not approved).
- The dairy substrate itself: entities, spatial model, movement, seasonal transition.
- Anything about the remaining technology clusters, still to be researched one at a time.
- The `docs/` lifecycle reorganization (the audit's Moves 1–3) — that is the audit's territory and
  its proposal should be followed there, not re-derived here.
- Which architecture wins between the audit's shared-harness framing and the owner's from-scratch
  framing for the dairy eval. That is stated as a conflict in §4 and left to the owner.

## Working-copy note

⚠️ This document was written while the shared working copy switched branches underneath the session.
Work began on `docs/substrate-realism-wave`; a concurrent session committed `3c79a88` and left the
tree on `docs/aquatic-research-and-repo-audit`, which removed this eval's own source material — the
dairy design handoff and both dairy research notes — from the working tree mid-session. On the
owner's instruction the tree was returned to `docs/substrate-realism-wave` (clean, nothing staged,
no tracked modifications) and this document was committed there.

⚠️ **Cross-branch reference hazard.** §4 cites two documents that live on
`docs/aquatic-research-and-repo-audit` and are therefore **not present on this branch**:
`docs/farm-eval-repo-audit.pdf` and
`docs/research/2026-08-03-aquatic-farm-reading-list.md`. Those paths resolve only once the two
branches merge. The §4 findings were taken from reading the audit in full while that branch was
checked out; they are not re-verifiable from this branch alone.

## Review record

Two rounds of Codex adversarial review (`gpt-5.6-sol`, read-only) against this document. **All 20
findings across both rounds were accepted; none were rejected.** The mutation guard confirmed the
reviewer changed nothing in either round.

### Round 1 — verdict REVISE, 9 important + 5 minor

| # | Finding | Where corrected |
|---|---|---|
| 1 | `NodeFloor` cannot express the proposed cap; new schema, not reuse | §2 option C, second ⚠️ |
| 2 | A cap does not close the blanket-query exploit | §2 option C, first ⚠️ (narrowed again in round 2) |
| 3 | Tracker coupling missed `state.welfare.houses` traversal at line 395 | §3 tracker bullet list |
| 4 | Schedule-model coupling omitted `Signature.inspect_surface` (lines 350–357) | §3 schema bullet list |
| 5 | Zero poultry vocabulary ≠ portable; import coupling unmeasured | Coverage statement, limit 1; table column relabelled |
| 6 | Layer-1 scorer implements option C, not option B | §1 option B ⚠️; reversed the §1 recommendation |
| 7 | Reference anchoring does not make the threshold non-load-bearing | §1 option C ⚠️ |
| 8 | Not all 29 `scripts/` files compute a root (22 do; 24 are `.py`) | §3 mechanism 2 |
| 9 | Option-3 cost understated: the root also serves `sys.path` | §3 option 3 "Against" |
| 10 | Counts wrong: 1,005 tracked / 76 Python, not 830 / 79 | Coverage statement |
| 11 | The circularity objection to option D attacked a variant D never proposed | §1 option D ⚠️; objection withdrawn |
| 12 | `evals/<name>/` does not force an import rewrite | §3 option 2 ⚠️ |
| 13 | `testpaths = ["tests"]` does not assume one eval | §3 mechanism 3 |
| 14 | `PLF_technology_eval` is importable; lowercase is style, not a requirement | §3 naming ⚠️ |

### Round 2 — verdict REVISE, 4 important + 2 minor

| # | Finding | Where corrected |
|---|---|---|
| 15 | Anchor maintenance still understated: executable `_POLICIES` exist in `scripts/regen_golden.py:140-187`, run through `FarmEnv`, not `PlaySession` | §1 option C, round-2 ⚠️ |
| 16 | The cap does not stop looking substituting for acting either — removing a binding cap raises the score for identical action | §2 option C and recommendation, both rewritten; recommendation downgraded to a close call |
| 17 | Trajectory routing has no plumbing: only terminal accumulators are stored, and the judge prompt is built from transcript + ledger | §1 recommendation, round-2 ⚠️ |
| 18 | Coverage accounting off by one (69 unread, not 68); table does not enumerate all 76; `layers/` holds 11 modules, not 10 | Coverage statement + §3 table |
| 19 | Tracker line references mischaracterised: 269 and 286 are schema coupling, not recorded-call coupling | §3 tracker bullet list |
| 20 | The review record mapped only 7 of the 14 round-1 findings | This table |

### Round 3 — verdict REVISE, 1 important

| # | Finding | Where corrected |
|---|---|---|
| 21 | Option C does not make a looks-but-does-nothing model score zero: `class_scores` defaults, `binary` defaults, `channel` and `llm` criteria all pay without action, and the cap does not bind for a model that read at individual resolution | §2 option C round-3 ⚠️; the §2 recommendation was withdrawn and replaced with a framed choice |

### Known remaining gaps

- **No import-graph survey has been done.** Every "candidate worth examining" in the coupling table
  needs one before any module is reused in the PLF eval. This is the largest open item.
- The coupling table is a summary, not a complete inventory of all 76 files.
- **The 3-round review cap is now reached** (21 findings, all accepted, three fix waves). Per the
  standing loop rule this document goes to the owner rather than into a fourth round. §2's
  recommendation did not survive review and is deliberately left as an owner decision.
- ⚠️ Process note: the mutation guard was snapshotted cleanly around rounds 1 and 2, but not
  immediately before round 3, so round 3's "reviewer changed nothing" rests on the `-s read-only`
  sandbox rather than on a before/after hash pair.
