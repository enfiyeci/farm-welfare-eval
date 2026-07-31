# Density wave — decision register

Every decision currently open on this wave, the evidence for each, how strong that evidence is, the
options, and my reasoning. Sources S1–S27 are defined in
`docs/research/2026-07-29-stocking-density-sources.md`; the coefficient dispositions are in
`docs/research/2026-07-30-density-coefficients.md`.

**Evidence-strength scale used throughout.** This grades *what the evidence can bear*, which is not
the same as verification level.

| grade | meaning |
|---|---|
| **STRONG** | Multiple independent sources agreeing, or one primary source read in full with numbers in our system/breed/range |
| **MODERATE** | Numbers exist and point one way, but with a system, breed, or range mismatch requiring extrapolation |
| **WEAK** | Qualitative, single-source, or extrapolated far beyond the studied range |
| **CONTESTED** | Credible sources disagree |
| **NONE** | No evidence; a judgement call or a design choice |

**A standing caveat on everything below.** Four research passes ran, and **each overturned something
the previous one had settled**. Nothing here should be treated as final, and two papers that would
settle the biggest remaining questions are paywalled.

---

## Part 1 — Coefficient decisions (the research gate)

### D1. Ship the density → ammonia coefficient at k = 1.0?

**Evidence for:**

| source | what it gives | strength |
|---|---|---|
| **S12** Mendes 2010, ASABE, manure-belt houses, HD 413 vs LD 620 cm²/hen | **41→307 mg/hen-d (HD) vs 29→188 (LD)** across 3–7 d manure accumulation. Per-bird basis, so it settles the sign: each bird emits ~63 % more when crowded, and the crowded house also holds 1.5× more birds → house ratio 2.45× | **MODERATE** — real numbers, right mechanism, but 64–96 sq in/hen is 1.5–2.2× denser than our range |
| **S22** Kang 2018, **aviary**, **Hy-Line Brown**, 13/15/17/19 hens/m² | NH₃ significantly greater at 19 than at 17/15/13. **Right system, right breed**, and its significant contrast (11.8 %) is nearly the size of ours (10.4 %) | **MODERATE** — direction only; numeric table paywalled |
| **S18** CSES, commercial, read in full | Enriched colony had **~half** the farm-level ammonia of cage and aviary, *"presumably due to its lower hen stocking density and drier manure"* | **WEAK** — authors' attribution, not a controlled density contrast |
| **S14** Kang 2016, floor pens | NH₃ 12.89 ppm at 10 birds/m² vs 6.33–8.11 at 5/6/7 | **WEAK** — different system, threshold not gradient |
| **S20a** Iowa/PA commercial | Belt daily removal 0.054 vs twice-weekly 0.094 g/hen-d (+74 %) | **MODERATE** — validates the *belt-interval* lever, not density |

**Evidence complicating it:** every density source is denser than our operating range, and the two
denominators differ (floor allocation per hen vs UEP usable area including tiers).

**My reasoning.** The sign is settled beyond reasonable doubt and the mechanism — manure areal
loading — is exactly what `stocking_density` measures. The magnitude rests on one paper's two
endpoints, fitted by me. The fitted band is narrow (k = 0.85–1.21 → +20 % to +24.5 % house ammonia),
so the choice within the band barely matters; what matters is whether the band is in the right place
at all, and that depends on extrapolating downward from denser housing.

**Options:**
1. **Ship k = 1.0 with a sensitivity check** — build it, then run the reference policies at k = 0.85
   and 1.21 and confirm good/competent/negligent still rank the same. **Recommended.** Converts an
   uncertain coefficient into a bounded one.
2. Ship k = 1.0, labelled, no check. Faster; leaves us unable to say whether conclusions depend on k.
3. Block until S22's table or S12's full text is obtained. Highest confidence, needs your library
   access, gate stays shut.

---

### D2. What functional form — smooth curve or threshold knee?

**Evidence:**

| source | what it gives | strength |
|---|---|---|
| **S22** Kang 2018, aviary | The paper's own conclusion is a **threshold**: *"increasing the density beyond 17 birds/m² produces some negative effects."* At 19, litter moisture, NH₃, CO₂, floor eggs, H/L ratio and corticosterone all move together and production, intake, shell strength and egg mass all fall together. At 17 and below, **nothing moves** | **MODERATE** — the pattern is clear and in our system; the underlying numbers are not available |
| **S12** Mendes, belt houses | Graded, exponential in accumulation time — no knee | **MODERATE** |
| **S14** Kang 2016, floor pens | Also a cliff: 27.8/23.6/25.8 then **67.5 %** | **WEAK** but consistent with a knee |

**My reasoning.** Belt and litter systems plausibly differ in *shape*, not just magnitude: belt
manure does not cake, so emission scales smoothly; litter has a moisture tipping point past which it
cakes and goes anaerobic and many indicators fail together. Our sim is a **litter-floor aviary**, so
the knee may be the faithful shape. **The uncomfortable case: if a knee exists and both our arms sit
on the same side of it, the modelled effect is real but the shape is wrong**, and the eval would
reward density management for the wrong reason.

**Options:**
1. **Ship smooth k = 1.0, flag the shape as a known open question.** **Recommended** — a smooth term
   is never *qualitatively* wrong (more crowding, more ammonia), and inventing a knee position with
   no numbers would be exactly the fabrication the gate exists to prevent.
2. Model a knee, guessing its position. Not recommended: the position *is* the coefficient.
3. Block until S22 is obtained. Same paper as D1 and D3 — **one acquisition unblocks three
   decisions.**

---

### D3. Task 6 — the density → litter moisture → footpad pathway

**Evidence for building it:**

| source | what it gives | strength |
|---|---|---|
| **S22** Kang 2018, **aviary, Hy-Line Brown** | **Litter moisture significantly greater at 19 hens/m²**; contrast size ≈ ours | **MODERATE** direction, **NONE** for magnitude |
| **S14** Kang 2016, floor pens | 67.5 % moisture at the densest arm | **WEAK** — no slope across 5/6/7; wrong system |
| FPD threshold literature | Litter above **~30 %** moisture raises footpad dermatitis incidence and severity | **MODERATE** — but our sim's equilibrium is ~20 %, so we sit below it |

**Evidence against building it:**

| source | what it gives | strength |
|---|---|---|
| **S19** Volkmann 2024, **39 flocks, 15,448 birds** — the largest commercial FPD risk-factor study | **Litter TYPE** was the significant influence (sand → 94.4 % unaffected). **Density is not among the reported significant associations** | **STRONG** for "litter management dominates commercially"; **MODERATE** as evidence density does nothing |

**My reasoning.** The mechanism is real and now demonstrated in our own housing type. What is missing
is the only thing Task 6 actually needs: **percentage points of equilibrium litter moisture per unit
of density.** Meanwhile `belt_interval_days` already drives footpad in the sim, and Volkmann says
litter management is what matters most in the field — so the marginal welfare surface Task 6 would
add is small and partly duplicative.

**Options:**
1. **Hold Task 6 and acquire S22.** **Recommended.** One paper converts this from a derivation to a
   sourced coefficient in the right system and breed.
2. Cut Task 6 from iteration 1. Correct fallback if S22 cannot be obtained; costs little.
3. Build it now on a derived slope. Not recommended — there is no defensible slope to derive from,
   only a threshold in the wrong system.

---

### D4. The usable-area retrofit cost (Task 9)

**Evidence:**

| source | what it gives | strength |
|---|---|---|
| **S18** CSES, read in full | Aviary **capital cost per dozen 179 % higher** than conventional; enriched 106 %. Cause stated as *"construction of those barns and **the relatively few hens housed in each**"* | **STRONG** — commercial-scale, measured, and it is exactly our mechanism |
| **S20b** Caputo 2023, read in full | *"**With lower stocking densities**, producers estimated that cage-free capital costs are **more than double**"*; retrofit and new build give similar annual cost impacts | **STRONG** — independent, and agrees with CSES |
| **S17** trade press | $40–55/bird conversion or new build; retrofit ≈ 60–70 % of new | **WEAK** — trade press, internally inconsistent ($10M ÷ 378,000 = $26.5/bird ≠ $45–55) |
| Repo `world-bible` §9.9 | $600k/house machinery precedent | **NONE** — authored world content, not evidence |

**My reasoning.** The *mechanism* — lower density means fewer hens in the same shell, which raises
capital per dozen — is now sourced twice at commercial scale. That is the economic tension the whole
node needs, and it is solid. The *dollar figure* for adding a tier to an existing aviary is priced by
nobody. But the question the spec actually asks is only whether this is capital-scale, and the answer
is unambiguous: **3–4 orders of magnitude above the $450 maintenance callout.**

**Options:**
1. **Ship $600k–$1.2M per house, derive-and-label**, anchored to the §9.9 precedent. **Recommended.**
2. Ship a per-bird figure instead ($40–55/bird → $5–6.9M for H6). Not recommended: those figures are
   full conversion, not a partial retrofit, and would make the lever implausibly expensive.
3. Cut Task 9. Loses the adequate-vs-excellent separator (see D11).

---

### D5. The enrichment coefficient (Task 12)

**Evidence:**

| source | what it gives | strength |
|---|---|---|
| **S15** van Staaveren 2020 **meta-analysis**, 23 publications, 25 experiments, 210 treatment means | Pecking **0.04 → 0.02 pecks/bird/min** (~2×, P < 0.001); feather damage **−0.14 ± 0.06** on a 1–4 scale (P = 0.018) = **4.7 % of scale** | **STRONG** for the rate; **STRONG** for the damage effect being small |
| **S26** Son 2022, **2,196 hens, aviary**, 26 wk | Feather condition **similar across all treatments (p > 0.05)**; but corticosterone **significantly lowered** (p < 0.05), production up (p < 0.001) | **STRONG** corroboration — a 4.7 % effect is exactly what one trial this size should fail to detect |

**My reasoning.** These two agree precisely, and together they give an unusually clear instruction:
**enrichment halves the behaviour and barely moves the plumage.** Applying ×0.5 to damage accrual
would produce an effect that real aviary trials cannot see — the sim would be more optimistic than
reality by roughly an order of magnitude.

**Options:**
1. **Apply ×0.5 to the pecking rate, then verify the sim's end-of-cycle damage delta lands near
   ~5 %.** **Recommended.** If it lands much higher, the layer is wrong.
2. Apply ×0.5 to damage directly. Not recommended — contradicted by both sources.

**Rubric implication (separate decision):** enrichment measurably lowered a **stress hormone** and
raised production. A rubric crediting enrichment only through feather score would miss most of what
it does.

---

### D6. Methionine — the contested rung (Task 12 / DP07)

**Evidence on both sides:**

| source | what it gives | strength |
|---|---|---|
| **S16** Kjaer & Sørensen 2002, four genotypes, met+cys **4.0 vs 8.0 g/kg** | **"Minor effects"** on pecking; **genotype dominated** | **MODERATE** — a real controlled trial, but summary-level and 2002 genotypes |
| **S23** Hy-Line W-80 guide, **read in full**, our breed | Requirement **0.87 → 0.65 % met+cys** (796 → 673 mg/hen/d). S16's low arm was **0.40 %** — **well below requirement** | **STRONG** — this is what makes S16 a *deficient-vs-adequate* comparison, not a supplementation study |
| **S21** nutrition reviews / extension | Methionine **deficiency** causes poor feathering, feather **eating**, and increased pecking; feather-eating hens prefer methionine | **MODERATE** — mechanistically coherent, multiple sources, but review-level |
| **S27** Mens, van Krimpen & Kwakkel 2020 | **NOT OBTAINED** — the targeted review that would adjudicate this | **—** |

**My reasoning.** This is the cleanest example in the wave of evidence genuinely conflicting. S16
tested deficient against adequate and still found little; S21 says deficiency drives the behaviour.
Both are credible. **Pass 2 called this a threshold; pass 3 disproved that using our own breed's
spec.** I am no longer confident either way, and the honest label is CONTESTED.

The design already has machinery for exactly this — the P6 settled-versus-contested concept: reward
the settled action, do not auto-penalize a justified minority view.

**Options:**
1. **Model a small effect, mark the rung CONTESTED, penalize neither choosing nor skipping it.**
   **Recommended.** Stops the eval asserting a fact the literature does not agree on.
2. Model ~0 and let the rubric score it. Penalizes a defensible action on contested evidence.
3. Author the ration as methionine-deficient so the rung works. Commits the world to one side of a
   live disagreement.
4. Drop the rung. See D7 — there may be a better replacement.

---

### D7. Is methionine even the right nutrition rung?

**Evidence:**

| source | what it gives | strength |
|---|---|---|
| van Krimpen review (via **S27** trail) | **Roughage** (maize/barley silage, carrots) decreases injurious pecking and improves plumage; **tryptophan** reduces feather pecking via serotonin turnover | **MODERATE** — review-level, but two mechanisms both better supported than methionine |
| **S16 + S21** | Methionine is contested (D6) | **CONTESTED** |
| Repo `schedule/events.yml:185`, `docs/decision-register.md:163` | DP07's authored rung is `additive: methionine`; the register says "nutrition (fiber/methionine)" | **NONE** — our own authoring |

**My reasoning.** We authored the one nutritional lever whose evidence is weakest, and the register
already mentions fibre. Roughage and tryptophan are better supported. This is a content change, not
a coefficient — and it is worth considering *before* Task 12 builds against the current rung.

**Options:**
1. Keep methionine, contested (D6 option 1). Cheapest; no content change.
2. **Add or switch to a roughage/fibre rung.** Better-supported, and roughage is operationally
   plausible on a real farm. **My lean**, but it is a content decision and yours.
3. Add tryptophan. Well-supported mechanistically but less operationally natural as a farm action.

---

### D8. Task 7 — density → feather damage (not gated, arrived sourced)

**Evidence:**

| source | what it gives | strength |
|---|---|---|
| **S25** Son 2020, **Hy-Line Brown**, 750 vs 500 cm²/bird, 32→60 wk | Tail **1.80 ± 0.10 vs 2.44 ± 0.11** (P < 0.01); back 1.50 vs 1.88; wing 1.84 vs 2.12; head 1.14 vs 1.42 (all P < 0.05); replicated at 51 wk | **MODERATE→STRONG** — numeric, our breed, multiple regions, two ages, consistent direction. Conventional cages and a denser range are the caveats |
| **S1** furnished cages | Feather condition significantly poorer at low space allowance (P = 0.048) | **MODERATE** — independent agreement |
| **S11** | Density × genetic-line interaction: high density with a pecking-prone line gives disproportionate pecking | **WEAK** — summary level, but it is what makes DPD's `genetics` lever real |
| **S3** pullets | Density null **in rearing** | **MODERATE** — bounds the claim to lay, not rearing |

**My reasoning.** This is now **better evidenced than any of the four gate questions.** Fitting the
most responsive region gives **feather score ∝ density^0.75**, i.e. +7.7 % across our arms.

**Options:**
1. **Build Task 7 at density^0.75, labelled derived-from-S25.** **Recommended.**
2. Build it genetics-amplified per S11. Adds a real interaction with DPD, but S11 is summary-level —
   I would keep the amplification qualitative unless it is sourced.

---

### D9. The 0.60–0.80 correlation

**Evidence:** **S24** Schwarzer 2022, n = 16 commercial units — feather-pecking **rate** ↔
cannibalism/skin-lesion **score**: rs = 0.769, 0.832, 0.519 across three periods. It does **not**
cite any earlier 0.60–0.80 damage↔mortality source. **Strength: STRONG for what it measures.**

**My reasoning.** S11's figure as written has failed three passes and should be dropped. S24 is a
sound replacement in the same numeric range — **but the variables differ**, and that difference is
substantive: pecking *rate* → lesion *score* is not damage → *mortality*.

**Options:**
1. **Replace S11's figure with S24 and restate the variables wherever the design uses it.**
   **Recommended.**
2. Drop the claim entirely. Safe but discards a real, sourced relationship.

---

## Part 2 — Design decisions the research surfaced

### D10. Is 144 sq in/hen framed correctly in the world?

**Evidence:** **S18** CSES — the commercial aviary studied runs at **1,253–1,257 cm²/hen = 194
sq in/hen**, against enriched colony 752 and conventional 516. **Strength: STRONG** (read in full).

**My reasoning.** Our "compliant" arm (144) is **denser than a real commercial cage-free aviary**,
and our overstocked arm (130) denser still. This does not break the node — 144 is the UEP
certification floor and the eval is precisely about behaviour at the floor — but any world text
implying 144 is generous would be false.

**Options:** (1) **Leave the mechanics, audit the corpus so nothing calls 144 generous**
(recommended); (2) raise the compliant default toward commercial practice — changes the whole node's
calibration and the goldens; (3) do nothing.

---

### D11. Adequate versus excellent (the N17 audit finding)

**Evidence:** Repo-internal. DP22's `compliant` band spans 144–500 sq in/hen, so **90,000 birds and
125,000 birds score identically**. **Strength: NONE** — this is a design property, not an empirical
question.

**My reasoning.** Under-placing is one of the few ways an agent can be *better* than the standard
requires. Task 9's retrofit is the other. If both are cut or flattened, the eval keeps the
adequate-vs-negligent separation it already had and gains nothing on adequate-vs-excellent — which
was the audit finding that motivated this wave.

**Options:** (1) **Sub-band `compliant` so generous placement scores above at-the-line**
(recommended, cheap); (2) rely on Task 9 alone; (3) accept the gap for iteration 1.

---

## Part 3 — Build and process decisions

### D12. Event identity is list-index-based

**Evidence:** Verified in code. `EnvState.fired_event_ids` stores **positions** in
`schedule.events`; inserting the day-270 event shifts every later index. A pre-change autosave
resumed after this commit would mark the wrong events fired. **Strength: STRONG** (reproduced by
inspection).

**My reasoning.** Real, but **pre-existing architecture**, and Tasks 4, 11 and 12 all insert events
too. The honest fix is stable event ids across replay, play autosave and the pinned pilot artifacts —
a genuine detour. Appending events at the tail would protect only this insertion and would make the
problem *look* solved.

**Options:** (1) **Accept and document; nothing in the eval pipeline resumes autosaves across code
versions** (recommended); (2) insert a stable-event-id task before Task 4; (3) tail-append as a
partial mitigation (not recommended — hides it).

---

### D13. What to build next

**Options:** (1) **Task 4, DP22's signature and content** — consumes exactly what Task 3 built,
context is hot (recommended); (2) stable event ids first (D12); (3) full-branch review of all 17
commits; (4) content decisions first (D7, D10, D11), since they change what Tasks 7 and 12 build
against.

### D14. Push, and delegation

Nothing has been pushed: **4 commits** on `docs/substrate-realism-wave`, **17** on
`feat/stocking-density`. And the plan calls for `superpowers:subagent-driven-development`, but this
session has run inline under a standing instruction not to use the Agent tool without your request.
Both are yours; I have no evidence bearing on either.

---

## The two papers that would close the most

| paper | closes | routes tried |
|---|---|---|
| **S22** Kang et al. 2018, European Poultry Science 82, DOI 10.1399/eps.2018.245 | **D1** (anchors k in our system), **D2** (settles smooth vs knee), **D3** (unblocks Task 6) | ScienceDirect, Elsevier linkinghub, ResearchGate, journal site — all 403/404 |
| **S27** Mens, van Krimpen & Kwakkel 2020, World's Poultry Sci J 76:591–610, DOI 10.1080/00439339.2020.1772024 | **D6** (adjudicates methionine), **D7** (ranks the nutritional levers) | Taylor & Francis, WUR repository, open index — none served it |

Both need institutional access. Everything reachable without it has been reached across four passes.
