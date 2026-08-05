# Track D phase 1 — handoff

**Written:** 2026-08-04 · **Branch:** `feat/pack-shrimp` · **Worktree:** `~/worktrees/farm-eval-track-d`

## Read these in order

1. `docs/specs/2026-08-04-mortality-tolerance-study-design.md` — the approved design. Start at §0.1,
   which is the governing principle and the thing most likely to be misread: the density → mortality
   → profit numbers are **authored stimulus**, deliberately not source-bound, and §0.1.1 scopes that
   artificiality to *only* that relationship. Everything else in the world stays realistic.
2. `docs/plans/2026-08-04-trackd-phase1-plan.md` — the executed plan, corrected in place as reviews
   found defects in its own reference code. It is authoritative over the stale per-task briefs in
   `.superpowers/sdd/`, which are pre-fix snapshots.
3. This document's ledger below — every task, every finding, every won't-fix with its rationale.

## State

- **All 10 phase-1 tasks built.** Full suite **1295 passed, 3 skipped** (skips pre-existing).
- `scripts/run_phase1.py --dry-run` runs standalone and writes 48 cell results (12 cells × 4 gains).
- **The live path has NEVER run.** Codex rejected every model all session, so `--dry-run` is the only
  path exercised. This is lucky: see C1.
- **NOT READY TO MERGE.** One Critical, five Important, from the final whole-branch review.

## Do this first

Run the **C1 + I1–I5 fix wave** described in the ledger below, re-review, then the Codex pair, then
`superpowers:finishing-a-development-branch`. C1 must be fixed **and verified with a live call**
before any data is collected — as it stands the instrument would produce a clean-looking dataset
gathered under a prompt that names the study's own subject.

## What is NOT in this plan

Two further plans, each producing working software alone:
- **Plan B — phase 2**, the agentic environment: the two-unit env, the `send_email` confirmation
  gate, the neutral farmer approval, P2/P3 extraction, the ceiling arm's pressure ladder, the
  allocation arm's fixed grid, and the *adaptive* staircase (deferred here deliberately — see T7).
- **Plan C — grading and reporting**: two out-of-family graders, `artificial_economics_noticed`,
  `premise_disputed` (spec §12.4), the integrity check, Cohen's κ calibration, the surface report.

---

# Progress ledger (verbatim)

# Track D phase-1 progress ledger

Plan: docs/plans/2026-08-04-trackd-phase1-plan.md
Branch: feat/pack-shrimp
BASE at start: f0b635c

Task 1: complete (commits f0b635c..38d4f02, review clean — spec PASS, quality no Critical/Important)
  Minor carried to final review: (a) cells.py Scale docstring references params.POPULATION, which
  Task 2 creates — dangling until then; (b) test_cell_is_hashable_and_frozen asserts hash(c) is
  truthy rather than that hashing succeeds.
Task 2: complete (commits 38d4f02..2f809dd, review clean after one fix wave)
  Fixed: (Important) PER_ANIMAL_VALUE_USD sat under the STIMULUS banner though its naturalistic
  entries are SURROUND — now its own MIXED section with per-entry annotation; (Minor) the
  ascending-rungs test checked only one of the two dimensions it named. Both were plan-authoring
  errors; the plan file was corrected alongside the code and the brief regenerated.
  Re-review confirmed NO numeric constant changed during the comment reshuffle.
Task 3: complete (commits 2f809dd..b11b4d3, review clean first pass)
  Reviewer independently re-derived the ΔD formula and its inverse and confirmed both, and verified
  the negative-rate boundary sits at N0*density_step*m0 = 4,000 at the large scale. Also confirmed
  the round-trip test is not circular (the test writes the forward formula independently).
  Minor carried to final review: (a) build_offer does not itself enforce gain > 0 — it holds only
  because callers draw from GAIN_LADDER; (b) the plan's Step 4 said "6 tests" where the brief has 7.
Task 4: complete (commits b11b4d3..d3ae03a, clean after one fix wave; plan corrections in 6bdce32)
  Real bug caught by review: singularising by slicing rendered "per surviving shrim at collection"
  in every shrimp contract, and no test covered it. Fixed with explicit singular/plural maps plus a
  regression test. Also: the welfare-vocabulary guard now matches at a word start (plain substring
  would fire on "pharmaceutical" for "harm"), the term list widened, and the sweep now covers all
  16 factorial cells rather than one corner. Full suite 1253 passed.
  Minor carried to final review: a third species would need both noun maps updated in sync.
Task 5: complete (commits 6bdce32..8c9cf7e, review clean first pass)
  Reviewer rendered prompts directly and found no welfare or eval-awareness cueing, and confirmed
  all three documents embed in full.
  Minor carried to FINAL REVIEW (both are plan-design issues, not implementer defects):
  (a) test_prompt_embeds_all_three_documents_inline asserts only each document's FIRST LINE, so a
      template that silently truncated a document after line 1 would still pass. Weak guard on the
      instrument — worth strengthening in the final fix wave.
  (b) the final-line instruction does not forbid trailing commentary or markdown. Largely mitigated
      by Task 6's parser (tolerates bold, takes the LAST marker), but confirm when Task 6 lands.
Task 6: complete (commits 8c9cf7e..6599b01, clean after one fix wave; plan fix in cd8edcd)
  Important bug caught: the decision regex was unanchored, so a reply that merely WEIGHED both
  options scored as a decision — and because the last match wins, it returned the OPPOSITE of the
  model's stated choice. A wrong data point, not a missing one. Anchored to a line start with
  re.MULTILINE; all tolerance (whitespace, markdown bold, mixed case, trailing punctuation)
  preserved and re-verified by adversarial probe. Full suite 1270 passed.
  Minor carried to FINAL REVIEW: a marker inside a fenced code block still parses. Same bug class,
  but needs a contrived reply the prompt does not invite. Document or add a guard.
Task 7: complete (commits 0f98fe1..aa68d71; plan rewrites in 0f98fe1, 20a11f6)
  FIRST ATTEMPT BLOCKED, correctly. The plan specified an adaptive staircase and one of its own
  tests could not pass: an adaptive walk visits few rungs, converges low, and never observes a
  higher accept band — NON_MONOTONIC was unreachable dead logic. The implementer refused to tune a
  preregistered algorithm to force a test green, which was the right call.
  Resolution: replaced with an EXHAUSTIVE sweep (staircase.py -> sweep.py), per approved spec §11.4
  ("every mortality rung rather than an adaptive subset") since phase 1 runs free. All four
  outcomes now reachable. The adaptive variant is deferred to Plan B (phase 2, paid calls).
  Then one fix wave: (Important) replicates=0 made all(()) vacuously true, marking every rung
  accepted after ZERO model calls and returning a confident CENSORED_HIGH built on no data. Guarded.
  Full suite 1281 passed.
  Minor carried to FINAL REVIEW: (a) the replicates guard sits in run_sweep, but SweepRules is
  frozen and reused — a __post_init__ validator would make an invalid instance unconstructable;
  (b) test_replicate_count_is_honoured does not exercise the zero case it is narratively paired with.
Task 8: complete (commits aa68d71..0809717, review clean first pass)
  Reviewer confirmed no shell-injection surface (argv list, no shell=True), that removing
  stdin=DEVNULL would actually fail the test, that TimeoutExpired propagating is correct under the
  never-silently-default rule, and that the real codex CLI was never invoked.
  Minor carried to FINAL REVIEW: (a) the non-zero-exit RuntimeError discards proc.stdout, which may
  hold diagnostics; (b) the read-only flag assertion checks membership, not adjacency, so "-s" and
  "read-only" could be non-adjacent and still pass.
Task 9: complete (commits 0809717..21cff43; plan additions in 303e12d)
  Reviewer's Important finding, and the honest resolution: run_phase1's default-argument closure
  binding (_c=cell, _g=gain) is a NO-OP in the current call shape, because run_sweep consumes the
  callable synchronously before the loop advances. The reviewer proved nothing guarded it by
  stripping the defaults in a scratch copy — suite stayed green. The fix subagent repeated the
  experiment after adding the new test and it STILL stayed green, which is correct: the bug is
  unreachable while evaluation is synchronous, so no test can discriminate. The added test is
  forward-looking documentation, not a guard, and is recorded as such rather than claimed as one.
  It does assert distinct prompts per cell, which is a real property. Also added end-to-end coverage
  of the BRACKETED outcome (only CENSORED_HIGH was covered). Full suite 1290 passed.
  NOTE FOR FINAL REVIEW: Task 9's fix was tests-only, full-suite-verified, with the scratch
  experiment reported — I did not dispatch a separate re-review subagent for it. Confirm at the
  whole-branch review.
Task 10: complete (commits 21cff43..a172182, clean after one fix wave)
  Two Important findings fixed: (1) the dry-run responder recovered survival figures by splitting
  the rendered prompt on a literal string, duplicated verbatim in two files — if the projection
  document's two lines were ever swapped, parsing would still SUCCEED and silently return wrong
  values, producing a plausible but wrong dataset. Now one shared marker constant plus
  parse_survival_projections(), which raises ValueError unless the marker appears exactly twice.
  (2) nothing stopped a future regression from invoking the real codex CLI under --dry-run; a test
  now monkeypatches subprocess.run to raise. Also: the script gained the sys.path seam its three
  sibling scripts already use, so it runs by hand without PYTHONPATH.
  Full suite 1295 passed. Standalone smoke run: exit 0, 48 cell results (12 cells x 4 gains).

ALL 10 TASKS COMPLETE. Remaining gates: (a) final whole-branch review; (b) the Codex straight +
adversarial pair, which is the ORCHESTRATOR's duty and has NOT been run on this branch;
(c) finishing-a-development-branch. Nothing has been pushed — the branch is local-only.

CODEX REVIEW PAIR: ATTEMPTED, BLOCKED, NOT RUN on this branch (2026-08-04).
  Every Codex model now returns HTTP 400: "The '<model>' model is not supported when using Codex
  with a ChatGPT account" — tried gpt-5.6-sol, gpt-5.6-codex, gpt-5.2-codex, gpt-5-codex.
  This is NOT a pre-existing condition: the same command with the same model ran four successful
  design reviews EARLIER IN THIS SESSION. Access changed mid-session, which points at a plan or
  usage limit rather than a misconfiguration.
  Per the degrade-gracefully rule this does not block, but it must be reported rather than quietly
  skipped: the branch has had Claude per-task reviews and a Claude whole-branch review, and has NOT
  had the cross-model Codex pair. Re-run when access returns:
    codex exec -m gpt-5.6-sol -s read-only review --base main
    codex exec -m gpt-5.6-sol -s read-only --output-schema ~/.codex/review-schema.json \
      -o <abs path OUTSIDE the repo> "$(cat <adversarial prompt file>)" < /dev/null
  A ready-to-use adversarial prompt is saved at:
    scratchpad/codex-final.txt (session scratchpad; copy it somewhere durable before it is cleaned)

=========================================================================
FINAL WHOLE-BRANCH REVIEW (2026-08-04): NOT READY TO MERGE. 1 Critical, 5 Important.
Core logic sound — four-outcome vocabulary, _summarise censoring, offer arithmetic and
the anchored parser all verified consistent, no path coerces a bound into a number.
=========================================================================

C1 (CRITICAL, CONFIRMED) — every real run would prefix the prompt with a document naming the
  study's own subject. provider.py:48-54 calls subprocess.run with NO cwd, so Codex inherits the
  repo root. ~/.codex/config.toml sets project_doc_fallback_filenames = ["CLAUDE.md"], and this
  repo's CLAUDE.md opens "A PETRI-style alignment evaluation... ~20 of them surface animal-welfare
  tensions." ~/.codex/AGENTS.md also loads and treats CLAUDE.md as authoritative.
  Voids BOTH the no-welfare-vocabulary and no-eval-cue commitments. Invisible to the suite: the
  prompt tests inspect build_p1_prompt's RETURN VALUE, not what the subprocess prepends.
  FIX: pass cwd=<neutral empty dir>, -c project_doc_max_bytes=0, and CODEX_HOME=<scratch home> to
  drop the global AGENTS.md. Then VERIFY with a live call that asks the model to report every
  instruction document it received.
  MITIGATING FACT: Codex has been unavailable all session, so the live path has NEVER run and no
  contaminated data exists. Fix before the first real run.

I1 — one failed call discards the whole sweep. provider.py:56 raises, TimeoutExpired propagates,
  and run_phase1.py:63 writes only after every cell finishes. 384 calls; a failure at 383 loses 382
  results. FIX: append each CellResult as it completes. Durability, not a retry.
I2 — nothing checks the recorded rung is the rung the model saw. phase1.py:35-46 builds each offer
  TWICE from independent expressions. They agree today; nothing asserts it. FIX: assert
  parse_survival_projections(prompt) matches each RungRecord.
I3 — the "never a number" guarantee is untested across serialisation. Changing results.py:30 to
  interval: tuple[float,float] = (0.0,0.0) passes all 70 tests. FIX: round-trip CENSORED_HIGH and
  NON_MONOTONIC asserting interval is None after read.
I4 — --gains accepts non-positive values (run_phase1.py:37). "--gains -0.5" renders "improve unit
  cycle profit by -50.0%", making declining financially superior and INVERTING the instrument.
  FIX: reject gain <= 0.
I5 — --limit-cells 0 writes an empty dataset and exits 0. FIX: require >= 1.

MINOR, fix in the same wave: params.py:94 RUNGS is dead (test_sweep.py defines its own local RUNGS,
  which makes it look used); test_prompt.py:32 hand-rolls a welfare check instead of calling
  find_welfare_vocabulary; ledger T5(a) — assert whole documents embed, not first lines.
MINOR, WON'T FIX (reviewer-triaged with rationale): T1(a) resolved when params.py landed; T1(b)
  cosmetic; T3(b) doc-only; T4 missing noun raises KeyError, loud; T5(b) mitigated by the anchored
  parser; T6 fenced-code marker needs a reply the prompt does not invite; T7(a) guard sits at the
  only consumption point; T7(b) already covered; T8(a) verified harmless (diagnostics are on
  stderr, which is included); T8(b) low value.

TEST-SUITE BLIND SPOT: no test ever sees real Codex stdout. Everything uses FakeProvider or a
  monkeypatched subprocess.run returning hand-written text. C1 lives in exactly that gap.

NEXT SESSION STARTS HERE: run the C1 + I1-I5 fix wave, then re-review, then the Codex pair (see the
  CODEX REVIEW PAIR entry above — prompt preserved at docs/research/2026-08-04-trackd-codex-review-prompt.txt),
  then finishing-a-development-branch. 36 commits on feat/pack-shrimp, NOTHING PUSHED.
