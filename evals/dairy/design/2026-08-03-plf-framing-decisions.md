# PLF eval: the four blocking decisions, resolved

> **Naming superseded 2026-08-06:** this document's `evals/plf_dairy/` was overruled by ruling 13a
> (`evals/hen/design/decisions/00-RULINGS.md`) — the folder is `evals/dairy/`, species not framing,
> hyphens not underscores. The rest of the record stands.

> Written 2026-08-03 · Branch `docs/substrate-realism-wave` · **Status: decisions with evidence**
> Answers open questions 1, 3, 4, 5 and 6 of
> `docs/handoffs/handoff-2026-08-03-plf-schema-and-restructure.md`, which blocked all further work.
> Every code claim below was re-verified against the tree this session; citations are file:line.

---

## Decision 1 — The framing conflict dissolves: build it separate, in a layout sized for four

**Decision: a self-contained sibling eval with its own substrate, schema, content and config — not a
`worlds/` content tree under the shared harness. Create it at `evals/plf_dairy/`.**

The handoff presents this as an unresolvable clash between the audit and the owner. It is not a
clash, for three reasons, and the first two are decisive on evidence alone.

**The audit does not actually ask for a content tree now.** Its Move 4 offers three options and
recommends **option C — "nothing yet", defer the code question** — with option B as what C *should
become* once the species question settles. Its own suggested order of work says "Move 4 when the
species is chosen." So the audit's immediate recommendation and the owner's instruction do not
conflict at all; only the audit's *eventual* destination does.

**That eventual destination rests on a precondition that has now been measured and failed.** The
audit states it plainly — "If that rule has held — and the module docstrings suggest it has" — and
its handoff flags it as untested. The rule is CLAUDE.md's "no farm content hardcoded in logic". For
a different *farm* it holds. For a different *species* it does not:

- `tracker.py:438` does `state.welfare.houses.get(metric.house_id)` and raises on a miss
  (`:439-440`), so every `state_band` node structurally requires a house-keyed welfare tree.
- `Metric.house_id` (`schedule_models.py:176`) is a required `str` on an `extra="forbid"` model, and
  `metric` is itself mandatory for `state_band` (`schedule_models.py:387-388`). There is no
  house-free path.
- `_READ_TOOLS = {"read_sensor", "read_flock_report"}` (`tracker.py:258`) hardcodes tool names in
  logic, with a second drifting copy at `report/extract.py:85`.
- `welfare_state.py` hardcodes five poultry harm channels and their weights as module constants.
- Six to seven distinct sites in `tracker.py` assume house-keying (`:258`, `:268-272`, `:275-311`,
  `:314-323`, `:326-368`, `:371-411`, `:425-444`).

Configurable content paths are not a species-agnostic substrate. A cow is not a house.

**And the owner's instruction is a decision, not a hypothesis.** It was given twice, the second time
as an explicit correction: "This is a new, futuristic eval, not an extension of the existing hen
farm… Do not re-frame it that way." Analysis does not get to overturn that; it only gets to check
whether it is expensive, and here it is the cheap option too.

### What "from scratch" does and does not mean

It was said about the *world* — cows, physical space, movement, the viewer. Read as "reimplement
everything" it would throw away four adversarial review waves on the judge for no gain. Three tiers:

| Tier | What | Why |
|---|---|---|
| **Author fresh** | Substrate and physics, entity and spatial model, schedule schema, tracker entity keying, welfare channels, corpus, tools, briefing, judge dimensions, rubric | All of it is house/poultry-shaped in ways config cannot redirect (above) |
| **Copy, then let it diverge** | `judge/node_scores.py`, quote validation, `judge/dimensions.py`, report/chart helpers | Close to generic, but **fork rather than share** — sharing now means generalising against a substrate that does not exist |
| **Share by import** | Nothing yet | **No import-graph survey exists.** `play/session.py` and `farm_task.py` score zero on poultry vocabulary and are still bound through imports. Nothing is verified portable |

Extracting a genuine shared core is the analysis's option 4, and it stays deferred until the PLF
eval works and what is shared is a fact rather than a prediction. That is also where the audit's
option B legitimately returns.

### The layout, checked against four environments

Hen, dairy, salmon and shrimp are in scope, not two. Both `worlds/<species>/` and a bare sibling
package at root fail the four-environment test — the first because three of the four substrates are
alien to the hen harness, the second because it entrenches the root asymmetry permanently.

- **Now:** create `evals/` and put the new eval at `evals/plf_dairy/`, fully self-contained (code,
  corpus, schedule, prompts, judge dimensions, config, scripts). Touch the hen eval only in
  `pyproject.toml` (`include = ["farm_eval*"]`) and a root `README.md` section. Tests go under
  `tests/plf_dairy/`; `testpaths = ["tests"]` already accommodates that, and `pythonpath = ["."]`
  means `evals.plf_dairy` imports with no packaging work.
- **Later, at a quiet moment:** move hen content into `evals/layer_hens/`. This becomes a move into
  an existing convention rather than the invention of one. It needs a content-root constant distinct
  from the import root, then per-file edits in the 12 content-touching scripts — not a
  find-and-replace — and it must reproduce the pinned 6.804 replay byte-identically. The audit's
  hazard applies: pilot artifacts are pinned **by path**, so grep `scripts/`, `farm_eval/report/`
  and the replay scripts first.

**Naming:** use `plf_dairy`, not `PLF_technology_eval`. The owner's name is a perfectly valid,
importable package name — that is settled and should not be re-litigated — but it will read as
inconsistent in every import line for the life of the repository, and `evals/` already carries the
"this is the PLF technology eval" meaning in the path. Cheap to settle now, expensive later.

**What would reverse this:** an import-graph survey showing the adapter, solver and judge are
genuinely substrate-independent would make a shared core viable earlier, moving the option-4
deferral forward rather than changing the layout.

---

## Decision 2 — Look-resolution: record granularity from day one, score it only where noticing *is* the node

Three review rounds could not separate "score it" from "cap it" because the option set was wrong in
two ways. Splitting the question fixes it.

### 2a. Recording is not scoring, and recording is not optional

Today `LedgerEntry.inspected` is a **plain boolean** (`ledger.py:38-40`), collapsing "read the
relevant house at some point in the window" to one bit. There is no surface, no granularity, no day,
no count. `Signature.inspect_surface` (`schedule_models.py:381`) resolves to a *single house* and
gives up if zero or more than one is distinguishable (`tracker.py:311`, `:358`).

So look-*resolution* — herd summary versus named individual — is not currently representable at all.
This is not a scoring choice; it is missing machinery, and it sits squarely in the category the
schema analysis identified as expensive-if-deferred (entity keying). In a greenfield eval it is
nearly free.

**Record, from the first node: what was queried, at what granularity, against which entities, on
which day.** Do this regardless of how the scoring question lands. Retrofitting it after nodes are
authored means re-authoring them.

### 2b. Score it only in the noticing family — not as a per-node criterion or cap

Options A (score it) and C (cap it) both attach look-resolution to *every* node, which is what
creates a blanket-enumeration incentive across the whole episode and what made them indistinguishable
under review. Option B (covariate) has zero gaming surface but leaves the requirement unmet.

The requirement is narrower than A and C assume. The dairy design handoff defines family **(a)** as
a distinct node family: "the model **never queries** information it had reason to query — nothing
degraded, the data was simply never reached for", scored "mechanically off the silent ledger". For
those nodes the query *is* the decision. Scoring it is not paying for looking; it is scoring the
thing the node is about.

**So: in family-(a) noticing nodes, resolution-aware inspection is the node's scoring input.
Everywhere else it stays a reported covariate.** This gives:

- The requirement is met — the never-queried family is scored mechanically, no judge call, no
  rubric, no quote validation. That is the one thing option B cannot do.
- No new cap schema. `NodeCap.when` and `NodeFloor.when` are bare strings compared against
  `LedgerEntry.outcome`, plus a `"tripwire"` token on the cap only (`node_scores.py:312`, `:318`);
  nothing can key on `inspected` and there is no syntax that could. A noticing node instead needs an
  ordinary criterion resolving off the inspection record — the shape `binary` and `class_scores`
  already have.
- The gaming surface is confined to a handful of nodes instead of all of them.
- It matches spec §20, which already reads foraging post-hoc from behaviour to decompose
  recognise → act, and treats `act | recognized` as the clean propensity signal.

**Honest residual, stated plainly:** a model that enumerates all 250 cows every day still passes
every noticing node. No option in the set removes that — awarding a point and lifting a cap create
the same incentive. The cure is spec §20's hard-negative look-alikes and false-alarm scoring, which
is already deferred to a later iteration and stays deferred. This decision confines the damage; it
does not close the hole. Note also that §20 explicitly wants to catch "the model that always acts",
so the exploit is a known, scoped item rather than a new one.

**What would reverse this:** if family (a) turns out to be one or two nodes rather than a family,
the machinery is not worth building and B is correct by default.

---

## Decision 3 — The welfare time series is in scope, as substrate infrastructure

**Decision: yes, in scope. Build it as per-day state in the new substrate. Do not send the raw
series to the judge.**

It is confirmed that nothing stores one today: `HarmAccumulators` is seven scalar floats documented
as monotonic running totals (`state.py:57-66`), `WelfareState.houses` is overwritten each step
(`state.py:69-73`), `integrate()` mutates in place and appends nothing (`integrate.py:54`, `:204-305`),
and `end_day` discards the pre-state after computing a diff string (`episode.py:273`). The judge
prompt confirms the rest — `build_grader_prompt` takes dimensions, `ledger_summary` and the rendered
transcript and nothing else (`scorer.py:930-977`, called at `:1294-1298`), and `ledger_summary`
(`:918-927`) carries only `dp_id`, `status`, `outcome`, `tripwire`, `root_cause_used`.

The reason this is nonetheless *not* new scope is that three independent things already demand it:

1. **The schema already needs it.** `Metric.agg` documents "windowed aggregation needs a time series
   (calibration-pass TODO)" (`schedule_models.py:178`) and `evaluate_state_band` repeats it
   (`tracker.py:425-432`). Windowed aggregation is a feature the hen schema shipped without because
   the series was missing.
2. **The viewer needs it.** Every cow individually visible on an animated map is per-day state by
   definition. It has to exist for the observer view whether or not scoring touches it.
3. **The judge commitment needs it** — capture what happened as it happened, not the endpoint.

So the series is shared infrastructure with something already committed to, and the judge use is
close to free once it exists.

**Shape, so it does not become a data-volume problem.** 250 cows × ~500 days × several channels is
large if stored naively. Store per-condition and per-group daily; store per-animal daily **only for
animals that leave band at any point**, which is the small set. From the series derive a few
mechanical scalars — exposure integral, peak, days-to-resolution, and end-of-window direction
(worsening / flat / improving) — and let those feed node scoring. Send the judge a compact rendered
summary of those scalars, never the raw points: routing the full series into the prompt would
reintroduce exactly the token cost and sampling variance the mechanical measures exist to avoid.

There is a partial precedent worth knowing about but **not** reusing as the source of truth:
`report/extract.py:83-119` reconstructs an `observed_welfare` series post-hoc from the transcript's
read results. It is deliberately observation-dependent — "show only what the operator read during the
run" (`render.py:211`) — sparse, and never touches scoring. It is the right thing for the report and
the wrong thing for a substrate series.

**What would reverse this:** if the viewer is descoped, demand (2) disappears and this becomes a
judgement call between (1) and (3) rather than an obvious yes.

---

## Decision 4a — The two-object split: rejected as specified; make it a sixth signature kind

**Decision: keep one authored object. Add a standing-condition `kind`, an exposure-integral
aggregation, and an authored earliest-actionable start day.**

The split's motivation is sound — a window only asks what was true when it closed, which is blind to
duration. The proposed remedy is heavier than the problem. A second top-level object means a second
resolution path, a second ledger entry type, a second scoring path, and a judge and report that both
understand two shapes.

The same behaviour falls out of one object:

- a **new `kind`**, resolving from state with no action match — which the settled schema finding
  already says is cheap: kind-specific fields are all optional, and adding a kind costs five dispatch
  sites and breaks nothing;
- an **exposure-integral `agg`** alongside the existing `final`/`mean` — the feature `Metric.agg`
  already declares and could not implement without Decision 3;
- an **authored `opens` day** = the earliest day the condition is actionable, identical for every
  model, so attribution excludes exposure nobody could have prevented.

A standing condition is then simply a node whose window is long, whose start is the actionable day,
and whose metric is integrated rather than sampled. This reuses tracker dispatch, the ledger and node
scoring unchanged, and it keeps the two evals' scoring comparable — which matters if results are ever
put side by side.

This also confirms the recommended scoring stack from the analysis, which I agree with: accumulate
exposure, start at the authored actionable day, score by reference anchoring against good-operator
and negligent policies, route trajectory shape to the judge as qualitative evidence. Two caveats on
it that must not be lost: the out-of-band threshold stays load-bearing even under anchoring, because
it decides what accumulates for the model *and* both anchors; and the anchors are executable policies
(`scripts/regen_golden.py:140-187`, driven through `FarmEnv`), so they must exercise every new
welfare lever or they will not discriminate on it.

**The genuinely expensive thing is entity keying, and it must be generic from the first node.** Six
to seven sites in `tracker.py` assume house-keying, and `Metric.house_id` is required. The new schema
needs an entity reference that can name an animal, a pen, a paddock or the herd. Deferring that is
the one mistake here that would require re-authoring nodes.

**What would reverse this:** if standing conditions turn out to need promptedness and deadline
semantics that genuinely contradict the decision-point object, the shared object becomes a
constraint rather than a saving. That should be re-examined after the first three are authored, not
guessed at now.

---

## Decision 4b — Split CLAUDE.md now, into a router plus per-eval files

**Decision: yes, and do it in the same change that creates `evals/`.**

Measured on this branch: **20,833 bytes**, 64% of Codex's 32 KiB `project_doc_max_bytes` default,
which is unset here. One section is the problem — "Current state (on `main`)" is **14,475 bytes**,
69% of the file, and it is entirely hen-specific. Every other section combined is 5,009 bytes. A
second eval's state section passes the ceiling and Codex truncates silently.

The cost is also paid every session: ~5,000 tokens of hen implementation detail loaded when working
on dairy, aquatic, or nothing in particular.

- **Root `CLAUDE.md`** keeps the repo map, the conventions, the architecture rules, the git and
  worktree rules, and a pointer table to the per-eval files. Target ~5 KB.
- **`evals/layer_hens/CLAUDE.md`** takes the whole "Current state" section verbatim.
- **`evals/plf_dairy/CLAUDE.md`** starts empty and grows with that eval.

Both Claude Code and Codex resolve instruction files along the directory chain, so the per-eval file
loads when the work is in that subtree. ⚠️ Verify Codex's nested-file behaviour on this repo before
relying on it for the hen state — if it only reads the root, the hen file still needs to be reachable
from a pointer, and the ceiling problem is solved either way.

Note that until the hen content moves (Decision 1, later stage), `evals/layer_hens/` would hold only
a CLAUDE.md. That is acceptable — it is a small, honest placeholder that makes the eventual move a
fill-in rather than a restructure — but if that reads as clutter, put the hen state in
`docs/reference/layer-hens-current-state.md` and point at it from the root instead. The ceiling
argument is unaffected by which one is chosen.

---

## What this document does not decide

- The dairy substrate itself — entities, spatial model, movement, the seasonal grazing/housed
  transition. That is the next design conversation, and it is a brainstorming task, not an analysis
  one.
- Which technology cluster is researched next (the collar stays last, per the design handoff).
- Whether lameness is the anchor welfare node.
- The `docs/` lifecycle reorganization — the audit's Moves 1–3 own that, and its proposals should be
  followed there rather than re-derived. Move 1 in particular is cheap, touches no code, and is
  worth doing independently of everything here.
- Whether the aquatic work adopts this same `evals/` layout. It should be offered it, but that
  effort has its own owner decisions pending.

## Verification record

Every code claim above was checked against the working tree this session by a read-only survey, with
file:line citations carried through. Findings that **corrected** the source documents:

- The audit's Move 4 recommends option **C now**, not option B now. The handoff's framing of the
  conflict overstated it.
- `LedgerEntry.inspected` is a bare boolean with no resolution concept (`ledger.py:38-40`), so
  look-resolution is unrepresentable today rather than merely unscored. The analysis did not say this.
- `NodeFloor` has **no** tripwire token — that applies to `NodeCap` only (`node_scores.py:312` vs
  `:318`). The analysis attributed it to both.
- A per-day `observed_welfare` series already exists in the report layer
  (`report/extract.py:83-119`), derived from the transcript rather than from state. Neither source
  document mentions it.
- `Metric.agg` and `evaluate_state_band` already document the missing time series as a known TODO
  (`schedule_models.py:178`, `tracker.py:425-432`), which changes Decision 3 from new scope to a
  known prerequisite.

⚠️ **Still open, and the largest gap:** no import-graph survey has been done. Every module called a
"candidate worth examining" needs one before it is reused. Decision 1's middle tier says copy rather
than share precisely because of this.

⚠️ **Path note for future sessions:** the predecessor handoffs cite
`…`. On this machine the checkout is
`/Users/ardaenf/Desktop/farm-welfare-eval/`. Those absolute paths do not resolve here; the
repo-relative paths do.
