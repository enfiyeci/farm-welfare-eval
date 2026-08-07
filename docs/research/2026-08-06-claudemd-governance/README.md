# CLAUDE.md governance research — 2026-08-06

Deep research on the best-practice protocol for keeping an auto-loaded agent instruction file
(`CLAUDE.md` / `AGENTS.md`) coherent across many git branches, worktrees, and two machines — and an
evaluation of three proposed fixes. Commissioned after `CLAUDE.md` was found to have drifted into
five versions across live branches (the stale breed-label incident), and after a "provably
contained" claim was written without running the proof.

> Delegated research. Coverage statement and ⚠️ flags are the subagent's own, verbatim. Two official
> Anthropic pages came back as full verbatim reproductions (high confidence); the community pages
> came back as small-model extractions (flagged ⚠️); one source was unreachable. NOT independently
> re-read at source.

## Bottom line

**The drift is a content-placement problem, not a merge problem, and the strongest-supported fix is
Fix 3: shrink `CLAUDE.md` to stable conventions + pointers, and move the living "current state"
narrative into one committed, single-owner status doc** (the `docs/LANES.md` pattern already is
this). Anthropic's own memory docs say `CLAUDE.md` should hold only "facts Claude should hold in
every session," target **under 200 lines**, and `/doctor` actively *strips* derivable current-state
content (directory layouts, dependency lists, architecture overviews) while keeping pitfalls,
rationale, and conventions. A hand-maintained "Current state / what's been built" narrative is
exactly the volatile, per-branch-edited content the file is not meant to carry; the community name
for what happens when many agents each rewrite it is **write amplification** — the precise 5-version
stale-label failure observed here.

- **Fix 1** (verification claims carry their command) — sound, aligned with Anthropic's
  "concrete enough to verify" principle, but addresses the *unverified-assertion* class, not
  branch-drift. Keep as a standing evidence rule.
- **Fix 2** (diff CLAUDE.md vs main at handoff) — best practice is silent; a reasonable interim
  guard that treats the symptom. Once Fix 3 removes the volatile prose, the diff shrinks to near-zero
  and the step becomes trivial. Interim only.
- **Fix 3** — strongly supported; the structural cure. Adopt it, with an explicit single-owner /
  gated-append rule for the status doc so it doesn't itself write-amplify.

## Recommended protocol (the agent's, to decide against)

1. Cut the "Current state" narrative out of `CLAUDE.md`; replace with pointers (build plan + DONE
   markers, `docs/specs/`, git log, test suite, `docs/probes/`). Keep only stable
   conventions/invariants/gotchas. Well under 200 lines.
2. Living status in one committed single-owner doc (extend `docs/LANES.md`), gated append,
   canonically on main. Not `CLAUDE.local.md` (doesn't cross machines/worktrees), not auto memory
   (machine-local).
3. If Claude + Codex both read the repo, use one canonical file + `@import`/symlink, never two
   hand-maintained copies. (Anthropic documents `@AGENTS.md` import or `ln -s AGENTS.md CLAUDE.md`.)
4. Keep Fix 1 as a standing rule: any claim asserting verification names the command + date.
5. Fix 2 as interim drift-guard; after step 1, downgrade to "the branch-vs-main CLAUDE.md diff
   should be empty; investigate if not."
6. For contract drift (the "provably contained" class), lean on git/CI as mechanical truth — the
   diff, `git merge-base --is-ancestor`, the typecheck — not prose.

The full report is in [report.md](report.md), including Q1–Q5 and the per-fix evaluation with
sourcing.

## Cross-machine constraint worth pinning

`CLAUDE.md` crosses machines only through ordinary git (there is no special sync). **Auto memory does
NOT cross machines** (machine-local; shared across worktrees of one repo only). So anything that must
be identical on both Macs has to be a committed file reconciled on one branch — which is why the
status doc must be committed, not memory.
