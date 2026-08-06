# Prompt for the other computer — 2026-08-06

Paste the block below into a fresh Claude Code session on the second Mac. It is self-contained:
it verifies the commit, points at the rulings, and opens three lanes that cannot collide with the
five running on the first machine.

---

```
We are splitting the farm-welfare-eval project across two machines. This machine takes three
lanes; the other machine runs five. The lanes were chosen so that no two of them write the same
files — read docs/LANES.md for the full ownership table before you touch anything.

Repo:   git@github.com:enfiyeci/farm-welfare-eval.git
Branch: docs/decision-briefs
Commit: ca24da4053151f207ed3901e8efd2d7539542c82

FIRST: verify that commit is fetchable (git fetch && git cat-file -t <sha>). Do not touch
anything until it verifies.

THEN read, in this order:
  1. docs/decisions/00-RULINGS.md  — the owner's answers to all eleven decision briefs. This is
     authoritative; where it contradicts a brief, it wins.
  2. docs/LANES.md                 — the lane plan, the file-ownership table, and the one rule
     that matters: exactly ONE lane owns farm_eval/env/model/ and the golden regeneration, and
     it is not on this machine.
  3. docs/decisions/README.md      — the index, for background on how the briefs are structured.

THE HARD CONSTRAINT: nothing on this machine may write to farm_eval/env/model/**, params.py,
config.yml, schedule/events.yml, the golden fixtures, or either reference artifact. Those belong
to the litter-drying lane on the other machine. All three lanes here are docs-only or additive.

YOUR THREE LANES. Create a separate git worktree for each, off current main, at
~/worktrees/<name>. One session per worktree, never two.

  LANE A — aquatic          ~/worktrees/fwe-aquatic     branch feat/aquatic-outreach (exists)
    A separate eval from the layer-hen one, so it shares no files. The branch already carries
    rescued RP outreach planning and SWIM research. Pick it up from what is committed there.

  LANE B — validation-gate  ~/worktrees/fwe-validation  branch docs/validation-gate (new)
    Docs only. This is the long pole for the project's "result" demo and it is entirely
    independent of engineering, which is why it is here.
      - Finish the expert labelling pack (docs/expert-labeling-pack.md) so a domain expert could
        actually sit down and use it cold.
      - Prepare the eval-awareness instrument: 15 blind sheets, 120 cells, needing Cohen's
        kappa >= 0.6.
      - Draft outreach for finding an actual vet or poultry-welfare specialist to label
        transcripts. This is the single task on the whole project that needs a person who is
        neither the owner nor a model. Treat finding that person as the deliverable.

  LANE C — research-backlog ~/worktrees/fwe-research    branch docs/research-backlog (new)
    Docs only, writes only under docs/research/. Chase the sources five previous research passes
    could not reach. In priority order:
      - EFSA 2023, Welfare of laying hens on farm:
        https://efsa.onlinelibrary.wiley.com/doi/10.2903/j.efsa.2023.7789
        Top gap across five passes. The EFSA Journal is fully open access, so the 403 is
        bot-blocking rather than a paywall — try a real browser. It may carry an authoritative
        quantitative space-allowance threshold, which several open design questions need.
      - Campe et al. 2018, Poult. Sci. 97:358-367  https://pubmed.ncbi.nlm.nih.gov/29177490/
        Abstract only so far. Analyses the German aviary dataset that may be the source of our
        feather-damage anchors and may contain a density term.
      - Sirovnik et al. 2018, feeder space and aggression:
        https://doi.org/10.1016/j.applanim.2017.09.017  (paywalled)
      - Bell & Weaver, Commercial Chickens Meat and Egg Production, 5th ed. (2002). Not online.
        Needs a library copy. It is the source of the 0.03 hours-per-hen automated-complex
        figure that the farm's whole 13-14 FTE staffing reconciliation rests on, and Anderson
        quotes it in one sentence without saying whether it is per cycle or per year.

RESEARCH DISCIPLINE — this project has been burned by it twice, so it is not optional:
  - Read every source end to end before asserting anything from it. Not from the abstract, not
    from a search snippet, not from memory.
  - Flag ANY partial read with a literal warning sign character on the claim itself, naming the
    source and what was missing (paywalled, 403, would not extract, truncated, read in part).
  - End every research document with an explicit coverage statement: what you opened, what you
    read to the end, what you could not reach and why.
  - Every source gets a full clickable markdown link.
  The two burns: a calibration coefficient was matched to operating conditions nobody had read,
  and a model coefficient turned out ~14x too large and the wrong sign once the source's methods
  pages were finally OCR'd and read.

GIT RULES ON THIS PROJECT:
  - Work on a branch, never directly on main. One session per worktree.
  - Commits end with:  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
  - Commit AND push when a task finishes — the owner moves between machines, and unpushed work
    is stranded work. Ask before pushing.
  - Update the lane's row in docs/LANES.md whenever its status changes, in the same breath.

Start by reading the three documents, then tell me which lane you are opening and what you found
in it. Do not start all three at once.
```
