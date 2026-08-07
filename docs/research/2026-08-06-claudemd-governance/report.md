# Keeping `CLAUDE.md` coherent across branches, worktrees, and two machines — research + fix evaluation

> Delegated research, 2026-08-06. Coverage statement and ⚠️ flags are the subagent's own, verbatim.

## Bottom line (recommended protocol)

The evidence points one direction: **the drift is not a merge problem, it is a content-placement problem, and the fix best practice most strongly endorses is Fix 3.** Anthropic's own memory documentation says `CLAUDE.md` should hold only "facts Claude should hold in every session" (build commands, conventions, layout, "always do X" rules), should target **under 200 lines**, and its `/doctor` tool actively *strips out* the derivable, current-state material (directory layouts, dependency lists, architecture overviews) while keeping pitfalls, rationale, and conventions. A hand-maintained "Current state / what's been built" narrative is exactly the volatile, per-branch-edited content the file is not meant to carry, and the community has a name for what happens when many agents each rewrite it slightly: **write amplification** — the precise 5-version, stale-label failure observed. So: **shrink `CLAUDE.md` to stable conventions plus pointers, and move the living "current state" into one owner-controlled status doc** (the `docs/LANES.md` pattern). Fix 1 (verification claims carry their command) is sound and complements Anthropic's "concrete enough to verify" principle, but it addresses the *second* failure class (unverified assertions), not branch-drift. Fix 2 (diff-against-main at handoff) is a reasonable stopgap best practice is silent on; once Fix 3 removes the volatile prose there is far less to diff. Adopt Fix 3 as the structural cure, keep Fix 1 as a standing evidence rule, use Fix 2 only interim.

Sourcing caveat: the two **official Anthropic pages** (`memory`, `worktrees`) came back as apparently complete verbatim reproductions and I treat them as read-in-full. The **community pages** came back as a summarizer model's extraction, not raw text — I mark those ⚠️. One page (morphllm) I could not read at all (HTTP 429).

## Q1 — Anthropic's official guidance
Source: [How Claude remembers your project — Claude Code Docs](https://code.claude.com/docs/en/memory), read in full.
- **What belongs (stable, not volatile):** *"Keep it to facts Claude should hold in every session: build commands, conventions, project layout, 'always do X' rules. If an entry is a multi-step procedure or only matters for one part of the codebase, move it to a skill or a path-scoped rule instead."* No recommendation to keep a current-state narrative. `/doctor` *"cuts content Claude can derive from the codebase, such as directory layouts, dependency lists, and architecture overviews, and keeps pitfalls, rationale, and conventions that differ from tool defaults."*
- **Size:** *"target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."* Loaded in full regardless of length; adherence penalty for length.
- **`@import`:** `@path` syntax, relative resolution, max depth 4, skips code spans/fences. *"imported files are expanded and loaded into context at launch"* — imports organize, they don't reduce context. External imports trigger a one-time approval dialog.
- **Hierarchical:** discovered by walking up the tree; ancestor files load in full at launch (root-to-cwd), subdir files on demand. Contradictions resolved arbitrarily; docs say review periodically. `claudeMdExcludes` skips irrelevant ancestors; `.claude/rules/` with `paths:` frontmatter for path-scoped rules.
- **Across branches:** the memory page says **nothing** about reconciling `CLAUDE.md` across branches — treated as a normal version-controlled file. **Inference:** branch-drift is left to ordinary git discipline, which is what fails when every branch edits the same prose block.
- ⚠️ The `#` memory-editing shortcut is not documented on this page; not confirmed.

## Q2 — The AGENTS.md standard
Sources: [agents.md](https://agents.md/) ⚠️ (extraction); the memory doc's AGENTS.md section (verbatim); [neonwatty setup guide](https://neonwatty.com/posts/how-to-set-up-your-repo-for-claude-code-and-codex/) ⚠️. ⚠️ [morphllm guide](https://www.morphllm.com/agents-md-guide) returned HTTP 429, not read.
- ⚠️ AGENTS.md: open Markdown format, 60,000+ projects, 24 tools (Codex, Cursor, Copilot…). No required sections. Monorepo: nearest file wins; explicit chat prompts override. Migration advice: *"Rename existing files to AGENTS.md and create symbolic links."* Single canonical file + symlinks, not maintained copies.
- **Authoritative (Anthropic):** *"Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If your repository already uses `AGENTS.md`... create a `CLAUDE.md` that imports it so both tools read the same instructions without duplicating them."* Patterns: `@AGENTS.md` as first line of `CLAUDE.md`, or symlink `ln -s AGENTS.md CLAUDE.md` (not Windows without admin).

## Q3 — The branch/worktree drift problem
Sources: [worktrees doc](https://code.claude.com/docs/en/worktrees) (verbatim); [dev.to parallel-agents](https://dev.to/jcamarate/keeping-context-and-decisions-consistent-across-parallel-ai-agents-32nj) ⚠️; memory doc "Consistency" (verbatim).
- The official worktree page is entirely about *file-edit isolation*, never `CLAUDE.md` divergence. It notes a session entering a worktree takes "project configuration such as `CLAUDE.md`" to that location — i.e. each worktree uses its own branch's `CLAUDE.md`, the exact mechanism that lets five versions coexist. Auto memory is shared across worktrees; the committed `CLAUDE.md` is not.
- ⚠️ dev.to splits drift into durable decisions / current contracts / in-flight state, prescribing: **"Prose for durable things, types for changing things, task boundaries for concurrent things."** Named failure mode: **write amplification** (*"four agents each record slightly different phrasings of the same convention"*). Mechanisms: keep only durable decisions in the startup file; carry changing contracts in the type system + CI typecheck; disjoint file ownership per agent; treat decision-doc writes as gated appends.
- ⚠️ No authoritative widely-adopted `.gitattributes` merge-driver or CI-lint convention specifically for `CLAUDE.md` was found. Treat "CI-validates-the-instruction-file" as lightly-practiced/theorized, not an established norm.

## Q4 — Generated vs hand-maintained current state
- Best practice leans hard toward **removing** hand-maintained current-state prose, not generating it. `/doctor` literally removes derivable/status content. Combined with "facts Claude should hold in every session" + 200-line target: don't put a living build-status narrative in the auto-loaded file.
- On "generate it from git/tests so it can't drift": **more theorized than practiced** for a *narrative*. What's actually done is generating the whole `CLAUDE.md` **once** (`/init`; ClaudeForge ⚠️). No authoritative example of auto-generating a prose "what's been built" section on every commit.
- Recommended shape (option a, strengthened): remove the narrative, replace with pointers to durable artifacts (build plan + DONE markers, git log, `docs/specs/`, test suite, `docs/probes/`). Where a living summary is still wanted, one status doc, one owner, gated append.

## Q5 — Cross-machine
- **`CLAUDE.md` crosses machines only through source control** — git is the only mechanism. The "commit + push on handoff" rule is the correct and only lever.
- **Auto memory does NOT cross machines** (*"machine-local... not shared across machines or cloud environments"*), though it IS shared across worktrees of one repo. So anything needed identical on both Macs must be a committed file. `CLAUDE.local.md` (gitignored) doesn't cross machines or worktrees. ⚠️ No Anthropic-endorsed `~/.claude/` cross-machine sync tool found; claude-sync is maintained out of band.

## Fix evaluation
- **Fix 1 (commands on verification claims):** best practice silent on the exact convention, aligned in spirit (Anthropic's "concrete enough to verify"). Targets the unverified-assertion class (the false "provably contained"), a written form of the existing evidence rule. Does NOT address branch drift. Keep as general assertion hygiene.
- **Fix 2 (handoff diff vs main):** best practice silent; own operational invention. Surfaces divergence at send/receive but is manual, per-handoff, O(branches), and misses the common case (a session reading a branch's CLAUDE.md without a handoff). Largely disappears under Fix 3. Interim only.
- **Fix 3 (shrink CLAUDE.md, status → single-owner doc):** strongly supported (official: 200-line target, `/doctor` trim, "facts every session"; community: write-amplification remedy; agents.md single-source model). Cross-machine: the status doc must be committed, not auto memory. Refinement: the status doc needs an explicit single-owner/gated-append rule and should live canonically on main so branches consume rather than each edit it. `docs/LANES.md` already is this pattern.

## COVERAGE STATEMENT
**Read in full (verbatim):** [memory doc](https://code.claude.com/docs/en/memory); [worktrees doc](https://code.claude.com/docs/en/worktrees).
**Read via small-model extraction, NOT verbatim — ⚠️:** [agents.md](https://agents.md/); [dev.to parallel-agents](https://dev.to/jcamarate/keeping-context-and-decisions-consistent-across-parallel-ai-agents-32nj); [neonwatty](https://neonwatty.com/posts/how-to-set-up-your-repo-for-claude-code-and-codex/).
**Could not reach — ⚠️:** [morphllm AGENTS.md guide](https://www.morphllm.com/agents-md-guide) (HTTP 429, not read at all).
**Seen only as search snippets, NOT opened:** [ClaudeForge](https://github.com/alirezarezvani/claudeforge) (referenced as a tool that exists; not confirmed to detect drift); orchestrator.dev, maketocreate, groff.dev, atlan — relied on primary docs instead.
**Not investigated:** the `#` shortcut's current behavior; any Anthropic-endorsed `~/.claude/` sync tool; any established merge-driver/CI-lint convention for `CLAUDE.md` (none authoritative found).
No repository files were modified.
