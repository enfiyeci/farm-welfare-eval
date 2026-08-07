# Handoff: welfare currency Step 1 — design COMPLETE, four owner rulings, ready to build
> Written: 2026-08-04 · Branch: `worktree-finance-decision-map` (pushed, `040f6b9`) · Status: active
>
> **Supersedes** `.claude/worktrees/finance-decision-map/docs/handoffs/handoff-2026-08-04-welfare-currency-step1-sources-read.md`
> (its first action, reading Ch. 5 and Ch. 6, is done). Treat that file and
> `handoff-2026-08-04-welfare-currency-step1.md` in the same folder as **stale**.

## What was done this session

- **Feather bridge ruled Approach A** and written into the spec: feathers = newly severely-damaged
  hens × **N = 1,225** [875–1,575], from Ch. 8's own 50%-plumage-loss worked example.
  **Verified** — committed `51d497a`; the per-feather cost derived from Pain-Track 4.1 reproduces
  the published aviary feather burden (0.8 / 13.9 / 180.9 h) at every printed digit.
- **Chapters 5 and 6 read end to end** (text; ⚠️ figures not inspected as images), PDFs archived,
  written up. **Verified** — committed `51d497a`; the write-up is
  `evals/hen/research/2026-08-04-welfare-footprint/findings-ch05-ch06.md`.
- **Owner ruled both chapters' channels IN.** Six new rows in spec §5.5 (dustbathing, foraging,
  nest, roosting deprivation; fatal and chronic egg peritonitis). **Verified** — committed `5c5d0b8`.
- **Owner reframed the headline** from absolute cumulative pain to the **change attributable to the
  agent's decisions**. Written as spec §1.1 (the ruling and its cost) and §5.7 (three tiers).
  **Verified** — committed `5c5d0b8`.
- **Owner ruled a mortality ledger** — deaths by day, house and cause; death rule unchanged;
  valuation anchors deferred to the calibration run. **Verified** — committed `040f6b9`.
- **Three Codex review loops run** (feather / chapters / reframing+ledger), **27 findings raised,
  all verified real against code, measured runs or the source PDFs, all fixed, none dismissed.**
  **Verified** — dispositions in spec §8.4, §8.5, §8.6 and in `findings-ch05-ch06.md` §6.
- **Suite green throughout: 1252 passed, 1 skipped.** All changes are docs-only. **Verified.**
- **Pushed.** `worktree-finance-decision-map` is at `040f6b9` on the remote, local and remote in
  sync. **Verified** — `git status -sb` clean against origin.

## Goal for next session

- Step 1 (the welfare currency) is **designed and reviewed but NOT built**. The whole thing lives
  in `evals/hen/design/2026-08-04-welfare-currency-design.md`; nothing under `farm_eval/` has changed.
  "Done" for the next increment is a working `farm_eval/env/model/pain.py` plus the mortality
  ledger, with every existing golden fixture byte-identical (acceptance criterion 1).
- **First action:** ask the owner whether to start implementing, or to take one of the open
  questions below first. **Do not start building without that answer** — two open items
  (the Tier-A reference choice, and ruling #15's anchor placement) change what the implementation
  is supposed to produce, and one of them is already known to gate publication of any result.

## Decisions made

- **Feather Approach B is rejected and closed — do not retry.** Reading our
  `feather_damage_pct` (a *prevalence of damaged hens*) as the book's flock-average plumage-loss
  score is a category error.
- **Feather day-0 uses SUPPRESSION, not keel's backdated seed** — charge only the rise above each
  house's start-age prevalence. The asymmetry is principled: Pain-Track 4.1 completes ~30 minutes
  after a pluck, so a pre-episode feather carries no ongoing pain, whereas keel's chronic phase
  does. Consequence: **House 1 charges exactly zero** and only House 4 is anchor-comparable.
- **Do not write "suppression loses nothing."** It loses no *pre-episode* pain. A hen already in
  the damaged cohort who keeps being plucked never moves the prevalence, so the channel counts
  **hens newly damaged, once each, not feathers removed.** This was written wrong once and caught.
- **The peritonitis share must attach to BASELINE mortality only, never to excess mortality.**
  Excess mortality moves with policy, so a share taken across all deaths would make the disease
  appear to respond to the agent when it does not — a manufactured signal, and the single most
  misleading thing this design could do under the new framing.
- **The integer death ledger CANNOT split `harm.excess_mortality`** — this was claimed and is
  false. The accumulator adds a *fractional, excess-only* value; the ledger records a *rounded,
  baseline-inclusive* integer. Split the accumulator **at accrual** instead. Both reviewers caught
  this independently; do not re-propose the integer route.
- **The death ledger alone cannot compute forgone pain** — it needs a daily per-house pain-rate
  series, which the state does not retain. Necessary, not sufficient.
- **Rejected: fixing the bird-hours sign hazard with a fixed reference cohort** (a reviewer's
  suggestion). It breaks the substrate's physics and hides a real consequence of negligence. The
  chosen treatment is the exact three-term decomposition in spec §5.5.1 ¶13.
- **`stocking_density` is inert** — a stored field no model layer reads and no tool sets. Do not
  substitute `litter_moisture` for it to make the foraging row look alive; the chapter names wet
  litter for **dustbathing only**.
- **Chronic peritonitis: use 1% Disabling, not the printed 10%.** Third known print-vs-platform
  divergence; only 1% reproduces the chapter's own published 89 h figure.
- **Codex's bio-risk filter fires on this project's vocabulary.** An adversarial review phrased
  around avian disease and sepsis was killed by OpenAI's content filter (false positive). Rephrase
  as a measurement/software-specification review and it completes. **A filtered run is not a clean
  run — never count one as APPROVED.**
- **The Bash tool's working directory silently reverts to the main checkout between calls.** A
  `git push` issued without an absolute path pushed the wrong branch (see Open questions). Always
  use `git -C .claude/worktrees/finance-decision-map`.
- **Owner working-style corrections still in force:** no research until its section comes up in the
  agreed order; plain-language explanations with tradeoffs rather than option chips; every source
  as a clickable link; deliverable files referenced by full path on every mention.

## Open questions

- **Which reference does the Tier-A difference report against?** Recommendation on the table is
  **competent** as the headline ("better or worse than a normal operator") with **good** as a
  secondary distance-from-achievable figure. The owner has not answered.
- **Ruling #15 (anchor placement) gates every Tier-A figure.** The good/competent/negligent labels
  are ours and #15 puts them in question; publishing difference figures before the anchors settle
  means restating them. Not yet scheduled.
- **The death valuation stays open by owner instruction** — the working default (terminal window
  only, no credit for the life not lived) stands, and the **anchors are scheduled to the
  calibration run that checks the financial and welfare scenarios**, not before.
- **An accidentally pushed remote branch needs a decision.** `docs/substrate-realism-wave` — 13 of
  the owner's own earlier dairy-eval commits, previously local-only in the main checkout — was
  published to the remote by the mis-targeted push. Nothing was overwritten and none of this
  session's work is on it. The owner was told and has not said whether to delete it.
- **Keel initialisation is still unchosen** (carried over): spec §5.5.1 ¶2 recommends a backdated
  seed cohort at episode start; the simpler alternative discards most of the keel burden for four
  of five houses.
- **No per-flock depopulation date exists in the substrate**, so cohort truncation binds to
  `config.yml`'s `episode_end_day` (518). Known approximation for House 1.

## References

- **The design spec — the thing to implement:**
  `.claude/worktrees/finance-decision-map/evals/hen/design/2026-08-04-welfare-currency-design.md`
  — §1.1 the reframing ruling and what it costs · §5.2.1 the mortality ledger · §5.5 the mapping
  table including the six new rows · **§5.5.1 ¶1–¶16 the implementation traps, which is the section
  that will actually save the implementer** · §5.7 the three attribution tiers · §6 acceptance
  criteria · §7 the answered/parked questions · §8.4–§8.6 this session's review record.
- **Work ledger, all owner rulings and the decision order:**
  `.claude/worktrees/finance-decision-map/docs/plans/2026-08-04-welfare-currency-and-finance-ledger.md`
- **Source corpus (start at the README):**
  `.claude/worktrees/finance-decision-map/evals/hen/research/2026-08-04-welfare-footprint/README.md`
  · `findings.md` — the six-chapter pass · `findings-ch05-ch06.md` — the second pass, the Ch. 5/6
  Pain-Tracks and what each addition costs · `pain-track-parameters.json` — the machine-readable
  parameter set · `sources/` — eight chapter PDFs.
- **Code the implementer will touch:**
  `farm_eval/env/model/integrate.py` (the daily loop; mortality at ~lines 240–275),
  `farm_eval/env/model/accumulators.py` (`accrue_excess_mortality`),
  `farm_eval/env/state.py` (`HarmAccumulators`, `WelfareState`, the `actions` list precedent),
  `farm_eval/env/model/layers/` (feather, litter, footpad, staffing),
  `scripts/regen_golden.py` (`run_reference`, the three policy regimes),
  `farm_eval/judge/welfare_reference.json`.
- **Measurements taken this session** (re-derivable, but expensive — ~2 min per full episode):
  bird-days lived 37,990,019 (good) vs 37,415,638 (negligent), a 1.51% gap; terminal survivors
  443,634 vs 436,509; `keel_risk_hours` identical at 48,913.0815 across policies; terminal harm is
  **unchanged** whether or not `config.yml`'s `enabled_nodes` is passed to `run_reference`.
- Commits this session: `51d497a` (feather ruling + Ch. 5/6 reading), `5c5d0b8` (channels in +
  the reframing), `040f6b9` (mortality ledger). Branch pushed and in sync.
- Book, all nine chapters free: <https://welfarefootprint.org/book-laying-hens/> · parameter
  platform: <https://pain-track.org/hens>
- **Sources that defeated retrieval — do not burn time re-trying blindly:** the Animal Ask weight
  table (an image; the PDF sits behind a Wix handler with no direct file URL), the ScienceDirect
  page for Kristensen et al. 2000 (HTTP 403), the OSF preprint <https://osf.io/94bxs/>
  (JavaScript-only), the *Nature Food* paper
  <https://www.nature.com/articles/s43016-025-01213-z> (paywalled).
- ⚠️ `feat/stocking-density-task6` belongs to another session. Do not touch it. It is blocked, and
  its ammonia recalibration collides with ruling #9 — coordinate before editing that layer.
- Programme deadline context (Sept 10, four deliverables, V1 must be publishable):
  `.claude/worktrees/finance-decision-map/docs/plans/2026-08-02-sept10-programme-plan.md`

## Load these skills next

- `superpowers:test-driven-development` and `superpowers:subagent-driven-development` once the owner
  says to build — the project's standing discipline for every increment.
- `superpowers:writing-plans` first if the build is large enough to want a task-by-task plan before
  any code, which on past form it will be.
