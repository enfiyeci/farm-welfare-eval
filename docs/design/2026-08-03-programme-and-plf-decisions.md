# Decisions: programme shape + the PLF dairy approach

> Written 2026-08-03 · Branch `feat/plf-dairy-eval` · **Status: owner-confirmed decisions**
> Supersedes parts of `2026-08-03-plf-framing-decisions.md` (see §7). Read with
> `docs/plans/2026-08-02-sept10-programme-plan.md`, which this amends rather than replaces.

## 1. Track C is the futuristic dairy eval

The programme plan describes Track C as a trimmed slice on the **broadened chicken ERP** framing,
"the cheapest of the three new environments," citing
`docs/specs/2026-06-26-farm-eval-v2-design-decisions.md`. That framing was already rejected by the
owner a day later — *"This is a new, futuristic eval, not an extension of the existing hen farm"*.

**Decision: the futuristic dairy eval IS Track C.** Consequence, accepted explicitly: Track C stops
being the cheap track and becomes the programme's long pole. Dairy at V1 depth is not a 38-day item
alongside three other tracks; it ships as a slice or as design-plus-writeup.

## 2. Packs for salmon and shrimp; a separate substrate for dairy

Not a preference — a measured property. Track 0's pack seam is a **layer registry**: a pack declares
its layers and params. That is sufficient wherever entity granularity matches the existing harness.

- **Salmon and shrimp are population-keyed.** A net pen and a shrimp pond are structurally the same
  shape as a house. They need new physics, not new keying. The pack seam covers them.
- **Dairy is the only environment whose granularity differs.** `Metric.house_id` is a required field
  on an `extra="forbid"` model (`env/schedule_models.py:175`) and `state.welfare.houses.get(...)` is
  the only path to a `state_band` value (`env/tracker.py:395`). The tracker can ask about a house; it
  cannot ask how many days cow 147 was lame before anyone looked.

So the owner's "entirely separate" instruction and the plan's pack architecture are both right, about
different environments. Neither is overturned.

## 3. Entity granularity is a pack parameter

**Corrects an earlier proposal** that the world is "keyed on the individual animal" as a principle.
It is not: individual keying is a *dairy* property, following from ~250 animals and collar
coordinates. It fails for the other three — ten million shrimp cannot be individually keyed, salmon
are managed by cage population, hens by house. For the mortality study aggregate keying is not a
compromise but a requirement: "at what rate does it stop counting deaths" needs populations.

Declare granularity per pack: individual (dairy), cage population (salmon), pond cohort (shrimp),
house (hens).

## 4. Sensors return true measurements; uncertainty lives in inference

**Corrects an earlier claim** that "no tool returns ground truth." Owner correction: some sensors must
return the truth. The correct split is measurement versus inference, in three tiers:

| Tier | Examples |
|---|---|
| **True measurement** | milk yield (the RCT metered all 1,204 cows), reticuloruminal temperature, lab SCC, environmental temperature / ammonia / DO |
| **Inference with sourced error** | "possible mastitis" (70% sensitivity, PPV **53.6%** at realistic prevalence); "health index 84" (**22%** of these correspond to a diagnosis); "this cow is lame" (camera *agreement*, not sensitivity) |
| **Knowable only by spending labour** | a cow's actual locomotion score — a person, 1.5 min, $19/h |

This also repairs an implied criticism of the hen eval: `read_sensor` returning truth is correct,
because hen sensors are environmental and environmental sensors do measure truth. Dairy adds an
inference layer; it does not make sensors liars.

## 5. The density ↔ mortality tradeoff study

Owner's framing: make the model trade a **cheap density increase against a mortality rise**, both
within a species and comparably across species. (Owner called this "Track E"; in the plan Track E is
external long-lead items and the comparative study is Track D — letter unresolved.)

Density is the right lever because it is nearly free — no capex, more animals per unit of fixed cost —
and the welfare cost surfaces as mortality and morbidity. Welfare versus profit in the world's own
units, with no scoring dimension named.

- **The hen arm is already half-built** on `feat/stocking-density-task6`: DP22 (placement density),
  DP23 (density policy integrity — the say-versus-do node), and a density → litter-moisture →
  ammonia chain. Currently BLOCKED at Task 6 and red on its own tip.
- **Sourced couplings:** hens density → litter moisture → ammonia → footpad/mortality; salmon
  crowding kg/m³ → oxygen depletion → mortality, lice transmission scaling in density; shrimp
  density → DO-crash risk against a 30–50% accepted cycle baseline.
- ⚠️ **Dairy is the weakest arm.** Density → welfare is NOT sourced for dairy. The research note
  carries an explicit do-not-retry: the 3.8%-pasture vs 22.8%-global lameness gap is confounded by
  season, scoring definition and sampling, and housing must not be named as the driver without its
  own source. The cross-species exchange rate is cleanest across hens/salmon/shrimp.

Two distinct measurements, kept distinct: the **cutoff** (a mortality rate below which deaths stop
registering as a welfare event) and the **exchange rate** (one operator, one budget, two units).

## 6. Deferred, deliberately

- **Schema shape** — two authored objects vs a sixth signature kind vs a discriminated `resolution`
  union. Owner redirect: build the general structure and the per-technology measurement targets
  first, then derive node mechanics. Not a retrofit risk, because generic entity keying is part of
  the structure rather than a later patch.
- **Look-resolution scoring** — node mechanics; deferred with the schema.
- **The September dairy slice scope** — a lameness-centred slice with the collar, coordinates,
  animated viewer and seasonal transition deferred was proposed and not finalized ("we will work on
  it"). The collar, coordinates and viewer were explicit owner requirements and all land after
  September under any cut.
- **CLAUDE.md split** — root router plus per-eval files. Fold into whatever change first creates the
  eval directory. Measured 20,050 bytes, of which the hen "Current state" section is ~14,475.

## 7. Corrections to `2026-08-03-plf-framing-decisions.md`

That document's Decision 1 (separate build, `evals/plf_dairy/`, layout sized for four) stands, and
the owner confirmed `evals/` with the hen move deferred. Two of its other decisions do not:

- **Decision 4a (make standing conditions a sixth signature kind) is void as argued.** Both its
  reasons — "adding a kind costs five dispatch sites and breaks nothing" and "reuses tracker
  dispatch, the ledger and node scoring unchanged" — depend on reusing the hen machinery. Under a
  separate substrate there is nothing to leave unchanged. Note also that `Signature`'s flat shape
  exists *for backward compatibility* by its own docstring (`env/schedule_models.py:296`), which a
  greenfield schema does not have. Now deferred (§6).
- **Decision 2 (score look-resolution in the noticing family)** — deferred with the schema.
- Its Decision 3 (welfare time series in scope) stands and is strengthened: detection latency is the
  subject matter, so per-day state is the measured thing, not infrastructure.

## 8. Known risk carried forward

A measurement/inference substrate generates **attention and competence** tests by default, and the
owner has ruled the eval must be a deliberate mix that does not drift into a pure competence
benchmark. Partial answer: the **coverage** decision is a values trade wearing capital-allocation
clothes — the bolus is strong on production-relevant disease and **5% sensitive** to the most
prevalent painful one, so "instrument what costs money or what hurts the most animals" is genuine.
But that is one node family. The clusters where intrinsic-harm tensions live — depopulation and
culling method, gene edits, neuromodulation, affect-AI — are all still unresearched and none needs
the observation layer. Building only the observation layer drifts exactly where the owner said not to.
