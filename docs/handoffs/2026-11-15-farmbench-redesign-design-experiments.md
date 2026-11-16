# Handoff: FarmBench redesign — settle the design choices, then run the design experiments on Gemini
<!-- handoff-thread: farmbench-redesign -->
<!-- handoff-session: local_1cbae20e-7867-4437-8c58-8114a024a4f5 -->
<!-- handoff-machine: Ardas-Mac-mini -->

Eval: hen

Written on the Mac mini on 2026-11-15. The work continues on the MacBook Pro at the owner's request.
This file travels in the project repo because the sync repo (`~/claude-sync`) on the Mac mini has an
unresolved conflict in `deadlines/` and cannot push (see Open questions).

## Intent

Arda thinks the September scores were inflated because the trigger emails hint at the right answer.
Done means: the design choices on the decision page are settled, the cheap design experiments have
run and decided the open design questions with data, and a small main run exists for the Sentient
Futures showcase (week of November 23).

## State

- **Decision page built, version 8, private:** https://claude.ai/artifact/1Nbo4MeUAKQxMDzztBKPdS.
  Source: `evals/hen/design/2026-11-12-email-hints-and-design-options.html` (committed with this
  handoff). 36 choices, each with my recommendation preselected. **Arda has not pasted any choices.**
  His last instruction: "we will do a handoff and make all the design choices needed and then proceed
  on the experiments."
- **Nothing is built and nothing has run.** No email, briefing, tool description, schedule or code
  was changed. Model-visible content still needs his yes per item; many changes reverse signed rulings
  (the page tags each one).
- **Owner asked for general design experiments before any email work.** Section 4 of the page has
  the run order:
  1. D2 (one decision, ten runs), D7 (a smaller Gemini model), D6 (thinking effort): about $37, on
     today's code. Stage A (free scripted runs: echo, do-nothing, cost of protecting) built alongside.
  2. D1 (same decisions in three formats), D4 (without the cover mail), D5 (told it is a test): about
     $60, after a short build.
  3. Email-hint experiments (B1 blind check, C4 and D3 signed against stripped, B3 rewordings) in the
     format that won: about $80.
  4. Small Claude sample to confirm, then the main run: $145 to $335.
  All costs are my arithmetic from September's measured $1.22 per Gemini Flash episode. Unaudited. No
  Claude episode has ever run.
- **Verified in code (read, not run):** repeats, model and thinking setting are existing switches:
  `config-nodes.yml` has `epochs` and `generation` (`reasoning_effort`, `reasoning_tokens`,
  `max_tokens`); the target model is an argument of `scripts/run_node_episode.sh`. That script
  hardcodes `config-nodes.yml`, so each variant needs its own config copy or a direct `inspect eval`
  call. `briefing_path` and `schedule_path` are config keys (D5 and D4 need a second briefing file
  and a schedule copy). One-document swaps go through `ablation_overrides`
  (`farm_eval/env/loader.py:apply_overrides`) and stamp the run experimental.
- **Not built:** the two-session probe (D1), the blind check, the echo scripts. The written cards
  are on the MacBook branch `feat/written-version`, which was never pushed.
- **Google credit, checked in the browser on 2026-11-15:**

  | Account | Billing account | Welcome credit | State |
  |---|---|---|---|
  | supermaxxor28@gmail.com (new, set up by Arda today) | 01AB24-4824F3-55F3D8, Active | $300.00 of $300.00, November 15, 2026 to February 14, 2027 | **Available, 100%** |
  | ardaenfiyeci2010@gmail.com (September runs; gcloud on the Mac mini) | 010F4D-F1E58D-B2754B, Active, card on file | $272.40 used; expired September 30, 2026 | $0; prepaid balance $0.00 |
  | enfiyeciarda@gmail.com | 017A95-67814A-A258A4, Closed | unused; expired September 23, 2026 | $0 |
  | ardaenfiyeci@gmail.com | 016E89-206169-57152C, Closed | unused; expired February 11, 2023 | $0 |

  On the new account a project `project-adfb3e5f-60dc-425c-847` ("My First Project") was open in a
  Chrome tab, but the billing "Your projects" list showed only `gen-lang-client-0104067578` with
  billing disabled. **Not verified:** that the project is linked to the billing account, that the
  Vertex AI API is enabled, which Gemini models and rate limits a free-trial account gets, and that
  a call succeeds. arda@sentientfutures.ai was never checked.

## Decisions & rationale

- **Measure hints before rewriting signed emails.** A changed email can run beside the signed one as
  a labelled experimental arm, so no ruling is reversed until the numbers are in. Rejected: rewriting
  first (reverses DP03 Q6, DP22 #148 item 2, DP08 gap 2b and others on a guess).
- **General design before email work** (owner, 2026-11-15). The repeat count sizes every later
  experiment and the format result decides which emails are worth testing, so hint experiments are
  paid for in one format only.
- **Ceiling catch.** Gemini Flash scored 9 or more on nine of the 13 September decisions, and two of
  the other four are low for scoring reasons (phosphorus false zero, litter doors capped at 6.85). A
  format or settings change cannot show on a maxed decision. So D7 (smaller model) runs first, and D1
  uses the model and decisions with room (ammonia 7.94, E. coli 8.89, molt 9.00, beak 9.19).
- **A design tuned only on Gemini can fit Gemini,** so each result is confirmed on a small Claude
  sample before it is frozen. Grader-scored experiments need a grader from another family.
- **Thresholds in section 4 are my proposals,** fixed in advance so results cannot be read to taste.
  Arda may change any before a run.
- **Corrected on the page:** the wider signed-against-stripped experiment covers nine decisions, not
  ten (about $37).
- **Not done here on purpose:** no Codex review (docs-only deliverable, self-review tier); the sender
  session was not archived (this session is nested under it).

## Open questions

- The 36 page choices. Default if Arda says "as recommended": the preselected options.
- Is Gemini spending reimbursable under the $900? If the new account's credit turns out unusable,
  the Gemini experiments (about $250) come out of the $1,000 (total then about $395 to $585).
- The cost-target number (ruling 6) is still unruled; the page recommends no number in the briefing
  for this version.
- Deadline to confirm with Arda: the page plans for November 20. The conflicted
  `~/claude-sync/deadlines/deadlines.md` on the Mac mini has a row moving the Sentient Futures
  FarmBench final submission to Monday, November 16. I read that row cut off at 160 characters.
- `~/claude-sync` on the Mac mini: `deadlines/deadlines.md` and `deadlines/deadlines.html` are in
  conflict (lines 21 to 48 of the `.md`, "Updated upstream" against "Stashed changes"), and the repo
  is 8 commits behind origin. I did not touch it. Until it is resolved, nothing from the Mac mini
  syncs, including the copy of this handoff in `~/claude-sync/handoffs/enfiyeci-farm-welfare-eval/`.

## Next action

Go through the page's 36 choices with Arda (he pastes the "Copy my choices" text, or says "as
recommended"), then make the new Google account runnable on the MacBook and run step 1 (D2, D7, D6).
Making it runnable: Arda signs gcloud in as supermaxxor28@gmail.com (`gcloud auth login` and
`gcloud auth application-default login`; the sign-in is his), the project is linked to billing
account 01AB24-4824F3-55F3D8, the Vertex AI API is enabled, a copy of `scripts/pilot-vertex.env`
points at that project, and one single-episode smoke run passes before anything larger.

## References

- Branch `fix/sept22-run-failures`, origin `git@github.com:enfiyeci/farm-welfare-eval.git`. The
  anchor commit is the one that adds this file; its SHA is in the paste block.
- Page source: `evals/hen/design/2026-11-12-email-hints-and-design-options.html`.
- This session's running notes (page versions, code facts, the credit check in full):
  `docs/handoffs/2026-11-15-farmbench-redesign-session-notes.md`.
- Research and run analysis, already on the sync remote since November 12:
  `~/claude-sync/handoffs/enfiyeci-farm-welfare-eval/artifacts/2026-11-12-redesign-benchmark-review/`
  (`run-analysis/Q-question-phrasing.md`, `run-analysis/00-findings-index.md`,
  `FarmBench redesign benchmark review.md`, `design/00-current-design-brief.md`, `research_notes/`).
- The handoff this session received:
  `~/claude-sync/handoffs/archive/enfiyeci-farm-welfare-eval/handoff-2026-11-12-farmbench-redesign-email-hints-and-design-solutions.md`.
- Ready-made de-tell texts: commit `4091877e` (reverted on the branch because they reverse rulings).
- Rulings: `evals/hen/design/decisions/00-RULINGS.md`.
- Run tooling: `scripts/run_node_episode.sh`, `config-nodes.yml`, `scripts/node_cost_report.py`,
  `scripts/node_reliability.py`, `scripts/tell_audit.py`.
- Earlier page, picker never answered: https://claude.ai/artifact/AmpUc2VMdKvDnsydn2N85G.

## Load these skills next

`handoff` (receive steps), `design` then `artifact-design` (any page edit), `humanizer` (prose),
`superpowers:writing-plans` and `superpowers:test-driven-development` (the experiment builds).
