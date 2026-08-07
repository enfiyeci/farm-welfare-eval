# Prompt for the other computer — 2026-08-06 (revised)

Paste the block below into a fresh Claude Code session on the second Mac. The **first** job is to
push everything that machine has — this machine's folder restructuring is gated on it.

---

```
We are syncing the farm-welfare-eval project across two machines before a repo folder
restructuring. The single most important thing you can do right now is get EVERYTHING this
machine has onto the remote, because the other machine cannot start the restructure until you do.

Repo:   git@github.com:enfiyeci/farm-welfare-eval.git
Origin: git@github.com:enfiyeci/farm-welfare-eval.git

STEP 1 — PUSH EVERYTHING (do this first, report back when done):
  - For every git worktree and branch on this machine, check for uncommitted work and unpushed
    commits:  git worktree list  then per worktree  git status -sb  and
    git log --oneline @{u}..HEAD
  - Commit anything uncommitted that should travel (scoped paths, never git add -A, since other
    sessions may share a tree). Commits end with:
      Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
  - Push every branch that is ahead of origin. Ask the owner before pushing (standing rule), then
    push. If a branch has no upstream: git push -u origin HEAD.
  - Watch specifically for a branch that has diverged from its own remote (local ahead AND behind):
    do NOT force-push. Push the local tip to a new archive/ ref instead and tell the owner.
  - Report a clear inventory: every branch, whether it is fully pushed, and anything you could not
    push and why. THIS INVENTORY IS THE GATE the other machine is waiting on.

STEP 2 — only after Step 1 is reported, and only if the owner wants work done here:
  Two docs-only support lanes, each in its own worktree off current main (one session per worktree).
  Both are safe here because neither touches the layer-hen model core.

    LANE — validation-gate prep   branch docs/validation-gate
      The long pole for the eval's "result" claim, independent of engineering:
      - finish the expert labelling pack (docs/expert-labeling-pack.md) so a domain expert could
        use it cold
      - prepare the eval-awareness instrument (15 blind sheets, 120 cells, Cohen's kappa >= 0.6)
      - draft outreach to find a real vet or poultry-welfare specialist to label transcripts. This
        is the ONE task on the whole project that needs a person who is neither the owner nor a
        model. Treat finding that person as the deliverable.

    LANE — research-backlog       branch docs/research-backlog   (writes only under docs/research/)
      Chase the still-blocked sources, in priority order:
      - EFSA 2023, Welfare of laying hens on farm:
        https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789  (open access; the 403 is
        bot-blocking, a real browser will likely work; top gap across many passes)
      - Campe et al. 2018, Poult. Sci. 97:358-367  https://pubmed.ncbi.nlm.nih.gov/29177490/
      - Sirovnik et al. 2018 feeder space  https://doi.org/10.1016/j.applanim.2017.09.017 (paywalled)
      - Bell & Weaver, Commercial Chickens Meat and Egg Production, 5th ed. (2002) — not online;
        needs a library copy; it is the source of the 0.03 hours-per-hen automated-complex figure
        the 13-14 FTE staffing reconciliation rests on.

  AQUATIC IS DEFERRED. The owner's focus is finishing the hen eval; do not open the aquatic lane.

CONTEXT to read (do not re-derive):
  - evals/hen/design/decisions/00-RULINGS.md  — the owner's rulings; the goal is "finish the hen eval",
    sequenced folder-restructure -> design lanes -> finishing pilot.
  - docs/LANES.md                 — the lane plan + the restructure gate you are unblocking.
  - docs/research/2026-08-06-*    — five deep research passes just landed (litter lever, ammonia,
    CLAUDE.md governance). Delegated findings with coverage statements; trace at source before
    acting on any number.

RESEARCH DISCIPLINE (this project has been burned twice): read sources end to end before asserting
from them; flag any partial read with a literal warning-sign character on the claim, naming what was
missing; end every research doc with an explicit coverage statement; every source a clickable link.

Start with Step 1 and report the push inventory. Do not start Step 2 lanes until the owner says so.
```
