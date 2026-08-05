# 09 · Housekeeping: two pushes and three archives

**Blocks:** nothing important. Five minutes of decisions.
Grouped because none of them deserves its own file.

---

## 9a · Push `3ba31cf` (the staffing lever map) or hold it?

**What it is:** an 18 KB analysis document, `docs/staffing-lever-map.md`, committed on
`feat/litter-ammonia-recalib` at 10:48 today. It is the **one commit on that branch that has not left
this machine.**

**Why it's not already pushed:** its Codex review never finished. Round 1 of that review caught a real
error — the claim that staffing could never be profitable, which re-measurement falsified by finding the
13–14 FTE notch. Round 2's result was never seen.

**The tradeoff, and it's a small one:**

- **Push now** — the work is safe on the remote and reachable from your other machine. Risk: if the
  review comes back with findings, amending a pushed commit is awkward, because force-push is blocked by
  a global safety hook. You'd add a follow-up commit instead, which is slightly messier history.
- **Hold** — you keep the option to amend cleanly. Risk: it exists in exactly two places, this machine's
  git and `~/Desktop/farm-eval-rescue/`. A disk failure or an over-enthusiastic cleanup loses it.

**My recommendation: push it.** Messy history is a trivial cost; a lost 18 KB analysis is not. And a
follow-up commit is perfectly normal — the "clean amend" you're preserving is worth less than the
redundancy you're giving up. Note also that the content is already known to contain at least one
falsified claim, so nobody should be treating it as final regardless.

**Ask yourself:** would I rather have slightly untidy history, or a single point of failure on work I
can't easily reproduce?

---

## 9b · Push the `claude-sync` repo (the spectator session's two commits)?

**What it is:** two commits in your `claude-sync` repo — the spectator dashboard's SDD decision record
(every review finding and adjudication from nine tasks) and its completion report. Both stranded on this
machine.

**Why it's waiting:** your standing rule is that pushes always ask first, so the session correctly
stopped.

**The tradeoff:** essentially none. This is a notes-and-handoffs repo, not code. Nothing depends on it,
nothing breaks either way. The only question is whether you want that decision record available on your
other machine.

**My recommendation: push it.** It's the provenance record for a nine-task review wave. Losing it means
losing the reasoning behind decisions you'd otherwise have to re-derive.

**Ask yourself:** do I move between machines enough that I'd want this there? (Based on your cross-machine
rule existing at all — yes.)

---

## 9c · Archive three finished sessions?

Three sessions have nothing left to do. Archiving stops their process, cleans up their worktree, and they
can still be reopened from the Archived list later — so this is reversible.

| Session | State | Safe to archive? |
|---|---|---|
| **DONE · Spectator dashboard** | Work fully merged to `main`; branch deleted | Yes, once you've decided 9b |
| **CLOSING · Non-finite guards** | Work committed as `3ba31cf`; I deleted its working directory | Yes, once it answers whether round 2 of its review found anything |
| **CLOSING · H6 refpolicy** | Work merged as `421528b`; I deleted its working directory | **Not yet** — it's recovering the staffing design argument, which exists nowhere else |

**On those deleted working directories:** that was my error. I removed two `.claude/worktrees/` directories
in the cleanup without checking whether they were live sessions' working directories. Both were clean and
held no unique commits, and everything either session committed is safe and verified — but they can no
longer run shell commands, which is why they're closing rather than continuing.

**My recommendation:** archive the spectator session once 9b is answered. Archive the non-finite-guards
session once it replies about round 2. **Wait on the H6 session** until its staffing analysis is recovered
— that's genuinely unrecorded work and archiving it first would lose it.

**Ask yourself:** is there anything in these windows I'd want to re-read later? If so, archiving still
keeps it — the sessions remain reopenable. The only irreversible thing is unrecorded reasoning, which is
why the H6 one waits.

---

## The one-line version

Push both (9a, 9b). Archive two of three now, and the H6 session after it hands back its staffing
analysis.
