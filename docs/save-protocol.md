# The file-save protocol

Eval: cross

Ruled 2026-08-06 (ruling 13d, `evals/hen/design/decisions/00-RULINGS.md` after the reorg;
`docs/decisions/00-RULINGS.md` before it). Six rules, kept deliberately small. They govern every
document written anywhere in this repo, including under `evals/`.

1. **Every new document gets a `YYYY-MM-DD-` prefix** unless it is a living reference document. The
   date prefix IS the lifecycle declaration: dated means "true when written; archive when
   superseded."
2. **Living reference documents are a closed, named list.** Adding to the list is a deliberate act,
   never a default. The list as of this pass: `docs/README.md`, `docs/save-protocol.md`,
   `docs/STATUS.md`, `docs/LANES.md`, `evals/hen/world/world-bible.md`,
   `evals/hen/world/model-params.md`, `evals/hen/nodes/decision-register.md`, and the per-folder
   `README.md` files.
3. **Every document declares its eval in one line at the top**: `Eval: hen | dairy | salmon |
   shrimp | cross` — greppable, changeable without moving anything, honest about mixed files.
4. **Research outputs go to a dated topic folder with a README as the first file** (the existing
   de facto habit, now written down).
5. **No document is written into a folder that has no README** explaining what the folder holds.
6. **Session status goes in one committed status doc — `docs/STATUS.md` — never in `CLAUDE.md`**
   (= ruling 12). Boundary: STATUS answers "what is built and in what state"; `docs/LANES.md`
   answers "who is working where right now."
