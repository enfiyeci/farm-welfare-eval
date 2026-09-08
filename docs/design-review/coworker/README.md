# Coworker versions of the node docs

Plain-language versions of the node design-review docs in [../nodes/](../nodes/), written
for teammates who have not worked on the project. Same facts, same real sources, same
underline-and-number citation style, but no scoring internals, no criteria questionnaire,
and no project jargon. Each page stands alone.

**Start with [00-OVERVIEW.md](00-OVERVIEW.md)**: every decision in one short paragraph,
grouped by theme, with a category / promptedness / capability label and a one-sentence
statement of the dilemma. Each entry links to its own full page.

## Conventions for these pages

- **Titles say the issue.** A reader should understand what a decision is about from its
  name alone, without it getting long (`In-ovo sexing vs culling male chicks`, not
  `Where the chicks come from`). Filenames keep the node-doc convention
  (`DP23_CHICK_SOURCING.md`) so each page maps to its source doc.
- **Sections, in order:** the decision in brief, the emails the model sees (verbatim from
  the corpus), the paths the model can take, welfare effect (in tables, using the Welfare
  Footprint pain bands where birds are the stakeholder), what the law requires, sources,
  open questions.
- **Sources are real only.** Every source row is a paper or a public web document with a
  working link. Numbers that come from the project's own simulation files are covered by a
  single plain sentence under the table, not as citation rows pointing at file paths.
- **No dash punctuation** in the prose (the verbatim emails keep whatever they have).
- **Open questions hold real gaps only**, not settled design choices. Design facts
  (a decision is prompted, the calendar will be respaced) are stated as facts, not
  questions.

## Status (2026-09-08)

- Every enabled node has a page (29, DPW and DP18 added 2026-09-08) and an overview entry.
- Reconciled twice against the build: `../2026-08-26-coworker-page-reconciliation.md` and
  `../2026-09-08-coworker-page-reconciliation.md`.
- The send-ready document is assembled by `docs/build-nodes-pack.py` (intro from
  `00-IDEA.md`, order from `00-OVERVIEW.md`, output `docs/nodes-pack.md` and `.docx`); it
  refuses to build if an enabled node has no page or no overview entry.
- `docs/check-coworker-quotes.py` checks every block-quoted email paragraph against the
  corpus word for word; run it after any corpus change.
