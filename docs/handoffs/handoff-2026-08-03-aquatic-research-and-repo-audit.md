# Handoff: aquatic eval research (Rethink Priorities) + farm-eval repository audit
> Written: 2026-08-03 · Branch: `docs/aquatic-research-and-repo-audit` (branched from `origin/main` @ 7be85e3) · Status: active

## What was done this session

- **Deep dive on Rethink Priorities' farmed-aquatic-animal research, and the primary sources they cite,
  producing a reading list for an aquaculture version of this eval.** Output:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-08-03-aquatic-farm-reading-list.md`. **Verified**
  — the file exists and is committed on this branch.
- **Seven source PDFs were downloaded and five were read end to end** (both RP salmon reports, both RP AI-in-
  aquaculture reports, and the IMR Laksvel protocol); two RP shrimp reports were read in part. **Verified** —
  the reading list's own coverage statement records exactly which, and the ⚠️ markers throughout mark every
  claim that rests on less than a full read.
- **Three adversarial Codex review rounds on the reading list** (the 3-round cap was reached). 21 findings
  raised across rounds 1 and 2 and 1 in round 3; all accepted and fixed. **Verified** — findings JSON files
  were written and read; the mutation guard showed no unintended repo changes.
- **Full repository structure audit**, delivered as a 16-page PDF:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/farm-eval-repo-audit.pdf`, built with the `pdf-design` skill
  (swiss preset). **Verified** — `build_pdf.py` exited 0 and the rendered pages were inspected visually.
- **Two layout bugs found and fixed during the PDF build**, and appended to the skill's learnings file at
  `/Users/ardaenfiyeci/.claude/skills/pdf-design/LEARNINGS.md`. **Verified** — the file was written and the
  corrected PDF re-rendered clean.

## Goal for next session

- The aquatic work needs a decision about **where it lives in the repo** before more of it accumulates, and
  the existing `docs/` tree needs a lifecycle split before a third generation of material lands in it. "Done"
  for the immediate next step is: `docs/` reorganised so a reader can tell from the path alone whether a
  document is still true.
- **First action:** read `/Users/ardaenfiyeci/Desktop/farm-eval/docs/farm-eval-repo-audit.pdf` section 07
  ("Proposed reorganization"), then ask the owner to confirm Move 1 before touching anything. Move 1 is
  mechanical, touches no code, and the test suite should be run after it regardless.

## Decisions made

- **Both salmon and shrimp are in scope** (owner, this session). The reading list recommends salmon first with
  shrimp as a second environment; the owner's answer was "probably both", so the sequencing is still open but
  the single-species framing is not.
- **Jurisdiction and certification set for a fictional aquatic farm are deliberately NOT decided yet.** The
  owner said this will follow further research and may end up bespoke rather than modelled on a real country.
  Do not pick one to unblock yourself — the reading list §D explains why assembling compliance rules from
  multiple jurisdictions produces a farm that cannot satisfy its own ledger.
- **Delousing is welfare-versus-welfare, not welfare-versus-profit.** This was the first draft's framing and it
  is wrong: sea lice themselves harm salmon, and both regulation and economics push toward treating. Do not
  rebuild the decision-register framing on a profit axis — the correct tensions are listed in §0 of the
  reading list.
- **Do not trust web-page summaries of research reports for numbers.** The first draft was built from
  summarised pages and had the shrimp un-ionised ammonia threshold wrong by roughly ten times (it gave
  "<1 mg/L"; the source says 0–0.1 mg/L, no more than 0.31). Reading the PDFs is what caught it. Do not
  reintroduce figures from search results without opening the source.
- **The RP "welfare range" estimates are not a cross-species conversion factor.** Multiplying an episode
  headline by them to compare a salmon run against a hen run is invalid — different quantities. Do not retry
  this; RP itself calls the numbers placeholders.
- **BarentsWatch data can calibrate baselines but not causal action effects.** It is observational and
  self-reported; treatment is not randomly assigned. Do not fit action-to-state response coefficients to it —
  take effect sizes from the experimental literature in reading-list §C instead.
- **`farm_eval/judge/scorer.py` (1,453 lines) should NOT be split during a reorganization.** It is covered by
  32 test files and four adversarial review waves, and a refactor of the scoring path risks changing scores.
  Split it when a feature needs it, not because a tidy-up noticed it.
- **This branch deliberately excludes the other 17 untracked files in the working tree** (the field guide PDF,
  the pptx, three HTML pages, two build scripts, the inheritance probe, the debrief-label directories). They
  belong to other efforts and the owner has not yet decided commit/ignore/delete for them.

## Open questions

- Which species is built first, and whether both share one repository. The audit's §07 Move 4 lays out three
  options and argues option B (one shared `farm_eval/`, parallel `worlds/<species>/` content trees) is where
  the architecture already points — but that rests on the "no farm content hardcoded in logic" rule having
  actually held. **That assumption is untested; verify it before betting on it.**
- Whether the owner wants Moves 1–3 of the reorganization at all, and in what order.
- What happens to the 17 undecided untracked files, and to `docs/farm-eval-repo-audit.pdf` itself — it is a
  generated output now committed into `docs/`, which is the exact habit the audit criticises.
- Whether to prune the 29 branches and 15 worktrees (one detached HEAD, one locked).
- Whether RP's "How AI is affecting farmed aquatic animals, Part 3: Welfare Effects" has been published yet.
  It was announced but unpublished as of this session, and it is the report closest to this project's thesis.

## References

- Reading list: `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-08-03-aquatic-farm-reading-list.md`
- Repository audit PDF: `/Users/ardaenfiyeci/Desktop/farm-eval/docs/farm-eval-repo-audit.pdf`
- This handoff: `/Users/ardaenfiyeci/Desktop/farm-eval/docs/handoffs/handoff-2026-08-03-aquatic-research-and-repo-audit.md`
- Branch: `docs/aquatic-research-and-repo-audit`, branched from `origin/main` at commit `7be85e3`
- Remote: https://github.com/enfiyeci/farm-welfare-eval
- Existing backlogs this work should not duplicate:
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/cleanup-backlog.md` and
  `/Users/ardaenfiyeci/Desktop/farm-eval/docs/future-work.md`
- RP's fish-welfare index (entry point to everything in the reading list):
  https://rethinkpriorities.org/cause-area/fish-welfare/
- Access-request form for RP's gated *Strategies for helping farmed shrimp*: https://forms.gle/Nb4qhvCpUyM4ujJ46
- BarentsWatch developer portal (owner needs to create the account; OAuth2 client-credentials):
  https://developer.barentswatch.no/docs/fishhealth/
- Source PDFs were downloaded to a session scratchpad that will not survive. All of them are re-downloadable
  from the URLs in the reading list; none are committed.

## Load these skills next

- `pdf-design` — if any further document deliverable is produced; read its `LEARNINGS.md` first, it now carries
  three lessons from this session.
- `superpowers:brainstorming` — before designing the aquatic environment, since that is new creative work.
- `handoff` — when this next stretch of work ends.
