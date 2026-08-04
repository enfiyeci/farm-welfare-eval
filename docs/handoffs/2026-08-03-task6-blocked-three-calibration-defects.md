# Handoff: Task 6 is blocked behind three stacked calibration defects — owner decisions needed first

> Written 2026-08-03 · Branch `feat/stocking-density-task6` (pushed) · Supersedes
> `docs/handoffs/2026-08-03-task5-density-litter-moisture.md` for next steps.
>
> **START BY ASKING THE OWNER THE FOUR DECISIONS IN "Next action". Do not write code first.**

## Intent

Make stocking density an emergent, tempting decision so the eval can separate adequate welfare play
from excellent, with the difference carried by the world rather than the judge. Task 5 (density wets
the litter) is built; Task 6 (wet litter raises ammonia) was meant to be a small increment. It is not:
investigating it surfaced three defects that sit *underneath* it, one of which voids Task 5's signal.

## State

- **No code changed this session.** Four commits, all docs/research. Suite is at its expected
  pre-existing state and both corpus guards are clean (see References for exact numbers).
- **Task 6 remains BLOCKED**, now for different and better-understood reasons than the plan records.
- **Three defects found, all verified at source by reading the Groot Koerkamp thesis and Hinz 2010
  directly** (not taken on a subagent's report). All written up with numbers, quotes and page
  references in `docs/research/2026-08-03-nh3-moisture-decomposition.md` — **read that document, it is
  the substance of this session and this handoff deliberately does not repeat it.**
  1. §9 — our 9.2–47.4 ppm "aviary" ammonia ceiling is Hinz's **floor-housing** row; the belt response
     looks 2–3× high at long intervals.
  2. §2 — the belt→litter-moisture curve claims 45 % at weekly belts; measured reality is 14–20 %.
  3. §3 — `litter_loading_ref_hens_m2 = 21.4` is attributed to the wrong house; correcting it to 23.0
     drops the overstocked lot to 159.8 against a 160.0 capacity, so **crowding stops costing anything.**
- **All three requested sources were obtained by the owner and are archived** under
  `docs/research/sources/` (Hinz, Miles, Mendes). Every acquisition gap from earlier in the session is
  closed except the *Transactions* version of Mendes, which is superseded by the conference paper.

## Decisions & rationale

- **The "surplus-only" route for Task 6 is RETRACTED, and must not be rebuilt.** I proposed applying
  the moisture coefficient only to density-driven moisture above the belt-only equilibrium; it was
  numerically attractive (all three anchors byte-identical, +60–77 % ammonia when overstocked). Then
  reading Ch. 7 eq. (9) at source killed the premise: it is **one multivariate fit**, so each
  coefficient is already a partial effect holding the others constant, and applying the moisture term
  to full moisture is the *intended* use, not a double count. Recorded in §1 of the research doc.
- **The plan's own "most likely correct" option (bound the litter equilibrium) does not work.** Measured
  with the real code: any cap below 60 eats Task 5's pinned gradation, because the density surplus is a
  flat +16.9 points. Gaps at belts 1–5 collapse to [15, 10, 5, 0, 0] at a 30 % cap. Don't re-derive this.
- **Defects 1 and 2 are the same lever and should be one recalibration task, done BEFORE Task 6** —
  Task 6 adds a term to the very layer defect 1 mis-calibrates, and defect 2 changes what the capacity
  in defect 3 must be calibrated against. Fixing in any other order re-does the work.
- **Fixing defect 2 probably HELPS the wave rather than competing with it** — this is the least obvious
  and most useful conclusion of the session. Belt interval is currently doing the litter-wetting job
  that density is supposed to do. Bound the belt curve to measured reality and density becomes the main
  thing that wets litter, which is exactly what the wave wants.
- **Worked in a forked branch, not `feat/stocking-density`.** The owner confirmed another session is
  active on that branch in the main checkout, so I forked `feat/stocking-density-task6` from it at
  `a4f8866` rather than switching or force-adding a second worktree. Consequence: this branch will need
  reconciling with whatever the other session commits.
- **New standing owner rule, saved to memory** (`always-give-clickable-links`): every URL, paper, DOI or
  source mentioned must be a clickable markdown link, especially ones the owner is asked to fetch.
  Prompted by me handing over an unclickable path — and by my having *fabricated* a plausible-looking
  source URL once, which resolved to an unrelated article. Never guess a URL.

## Open questions

**These four are the reason this handoff exists. All are the owner's, none are the implementer's.**

1. **Fix the ammonia belt response (defect 1)?** Costs a recalibration touching all five houses and the
   goldens. Note the specific mismatch: Nimmermark's 32–38 ppm was measured at **winter minimum
   ventilation**, but `_eq_belt` asserts it at **baseline ventilation** — that operating-point mismatch
   is the defect, not simply "the anchor is wrong". *(The winter conditions are agent-read from
   Nimmermark, not source-verified — verify before acting on it.)*
2. **Bound the belt→litter-moisture curve (defect 2)?** Changes footpad for all five houses and may
   remove belt interval as a footpad lever — someone must check whether an authored decision depends on
   that link.
3. **Fix Task 5's water-input reference (defect 3), and how?** Options and costs are in the research
   doc's recommendations. Reopens landed, Codex-APPROVED work either way, because the "Sourced" label on
   21.4 is false regardless of whether the numbers move.
4. **Does the wave continue, or get re-planned?** Pause density and spin the calibration fixes into
   their own wave / absorb them into this wave / ship as-is. **Shipping as-is is not viable** — at the
   correct reference the density signal is zero, not merely weak. My recommendation is to pause and
   re-plan, since the calibration fixes are worth doing for the eval regardless of density.

Also still open from before, flagged not acted: merging `feat/stocking-density` to main (gate not met,
and Task 5 is now in question — I'd say no); the disposition of `feat/flock-cop-reads-integrity` and
`feat/phase-c5-judge-v2`, pushed without review two sessions ago; and a rebase, since
`feat/stocking-density` forked from a commit behind `origin/main`.

## Next action

**Ask the owner decisions 1–4 above, and wait.** Present them in plain terms with the costs — the owner
has twice asked for detailed plain-language explanations rather than option chips, so lead with prose
and a recommended sequencing (defects 1+2 as one task → defect 3 → Task 6). Do not open an editor until
they answer; every path forward changes review-approved work, and picking one silently would be wrong.

## References

- **The substance of this session:** `docs/research/2026-08-03-nh3-moisture-decomposition.md`
  (§1 the retraction · §2 the belt curve · §3 the provenance error · §6a Kang 2016 · §8 Miles
  coefficients + derived turnover · §9 the Hinz misattribution · §10 the Mendes interaction ·
  recommendations at the end)
- **Sources, now archived:** `docs/research/sources/` — `Hinz-2010-Landbauforschung-60-3-*.pdf`
  (article is PDF pp. 32–43; German; extracted text alongside as `Hinz-2010-article-text-*.txt`),
  `Miles-2011-high-litter-moisture-suppresses-NH3-volatilization.pdf`,
  `Mendes-2010-ASABE-1009252-density-x-manure-accumulation-time.pdf`. The Groot Koerkamp thesis is NOT
  committed — re-download from https://edepot.wur.nl/210633 (155 pp, open).
- **Branch:** `feat/stocking-density-task6` on `enfiyeci/farm-welfare-eval`, forked from
  `feat/stocking-density` at `a4f8866`. Commits: `986120f`, `cc1c283`, `730ccd0`, `3106542`.
- **The plan and its merge gate:** `docs/plans/2026-07-29-stocking-density-plan.md` — Task 6 at
  1451–1513, the BLOCKED status at 1495–1565, the merge gate at 37–51. **Its "three options" section is
  now partly superseded** by the research doc; read both.
- **Code the decisions touch:** `farm_eval/env/model/layers/{ammonia,litter,density}.py`,
  `farm_eval/env/model/params.py`, `tests/env/model/test_layer_ammonia.py:57–68` (the misattributed
  ceiling), `tests/env/test_density_reference_is_wired.py:121` (the pinned gradation).
- **Environment gotchas that cost time this session:**
  - Expected suite state is **3 failed, 1324 passed, 2 skipped** — the 3 failures are the known Task-13
    goldens/reference tests. A *fourth* failure is yours.
  - `pyproject.toml` already sets `addopts = "-q"`, so passing `-q` yourself makes it `-qq` and
    **silently suppresses the count line**. Run bare `pytest --tb=no -rN`.
  - A fresh worktree has no `farm_eval/judge/rubric.yml` (gitignored), so `test_rubric_sync.py` skips.
    Run `node docs/build-rubric.mjs` to restore that guard.
  - `venv` in the worktree is a **symlink to the main checkout's venv**. Do not `pip install` into it —
    it is shared with the other session. There is no PDF page-extraction tool available as a result.
  - Put an explicit `cd <worktree> &&` in every shell call; the working directory reverts to the main
    checkout on its own.

## Load these skills next

- `superpowers:test-driven-development` — every task on this wave is written test-first.
- `superpowers:subagent-driven-development` — delegation is owner-approved for this build.
- **Standing trap:** a test that exercises a layer directly does NOT guard the wiring.
  Mutation-check every wiring test — delete the wiring, watch it go red, restore it.
