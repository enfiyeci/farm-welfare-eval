# Inside the Farm, End to End — the full field deck

A ~370-page PowerPoint that reflects the **entire farm-eval project**, generated from the
repository so it stays honest and refreshable. It is meant both to show people the project
and to see, at a glance, what stage it's at.

## What's in it (eight parts)

1. **The decisions** — all 23 decision points: category, the real triggering email, the
   distributable judge rubric, the outcome space, the settled-vs-contested evidence, sourced links.
2. **The walk** — the 518 days as the agent lives them: every authored email as a facsimile,
   the open decision windows, the market, session by session.
3. **The world** — Cloverdale: company, six barns, the cast, the money/COP, the four red lines.
4. **How it runs** — the loop, the sixteen tools, the blind spots.
5. **The codebase, wired** — env core, the reactive substrate, the adapter, the judge — module
   by module, with the load-bearing seams. (Includes the shipped-vs-spec judge divergence.)
6. **The judge** — ten dimensions, the node-score headline, the quote-evidence gate.
7. **Where it stands** — the branch landscape, the tracks, the findings, the gates, and the
   ranked **open questions & dilemmas**.
8. **Sources** — the anchor register with working links.

## Regenerating it (your "every 4–5 big changes" workflow)

The generator reads the repo at build time, so a rerun picks up code/schedule/node/corpus/judge
changes automatically. After a batch of changes:

```bash
cd <this-dir>
npm install            # first time only (pptxgenjs + js-yaml)
REPO_ROOT=/absolute/path/to/farm-eval npm run build
# -> writes inside-the-farm-full.pptx
```

`REPO_ROOT` defaults to `/Users/ardaenfiyeci/Desktop/farm-eval`; set it if the generator lives
elsewhere or you point it at a different checkout (e.g. a freshly pulled `origin/main`).

Then **manually review the slides affected by what you changed** — e.g. edit a decision node →
check its 3–4 pages in Part ONE and its day pages in Part TWO; change the judge → Part SIX.

## What reads what (the data spine)

| Deck content | Source it reads |
|---|---|
| decision nodes, rubrics, outcome space, confidence | `docs/decisions-data.mjs`, `docs/decisions-extra.mjs` |
| which nodes are scheduled / enabled | `schedule/events.yml`, `config.yml` |
| every email facsimile | `corpus/documents/emails/*.md` (via each event's `body_ref`) |
| judge dimensions + weights + anchors | `judge/dimensions/*.md` |
| working links / anchor register | `docs/research/SOURCES.md` |
| world facts, architecture, project stage | `content.mjs` (authored; see its header for provenance) |

## Files

- `build.mjs` — orchestrator (imports the parts, writes the pptx)
- `theme.mjs` — palette + fonts + layout tokens (the "Inside the Farm" house style)
- `kit.mjs` — the slide component library
- `data.mjs` — loaders that read the live repo (+ the DP↔node bridge, per-node links)
- `content.mjs` — authored prose for the non-data sections (world, architecture, stage)
- `part_*.mjs` — one module per part

## Two things to know before you show it

- **Provenance.** The deck stamps the checkout it was built from. It was first generated from a
  branch ~63 commits behind `origin/main` (which carries a repo reorg into `evals/hen/`). The
  project-stage section is sourced from the live trunk and says so. Rebuild against a pulled
  `origin/main` (set `REPO_ROOT`) to make the whole deck current.
- **The judge divergence** (Part SIX) is a real, code-verified finding: the shipped headline is
  the per-decision node-criteria mean, not the spec's dimension-weighted mean.
