# Reviewer digest

The short version of the nodes pack: about a page per scored decision, for outside reviewers who asked for "the decision list" and would not read the 96,000-word pack. First written for Lukas Jasiūnas (Healthier Hens) in September 2026; the ordering puts the bird-side decisions first and the honesty and paperwork decisions last, with a boundary note between them.

One file per enabled node, plus:

- `00-front-matter.md`: what FarmBench is, the farm in five lines, how welfare is counted, and the four standing questions every decision points back to.
- `99-boundary-note.md`: the note inserted before the three honesty groups.

Each node file has the same six fields: what happens, what it costs the birds (or the people), a table of paths for the reviewer to score out of 10 before reading ours (the first Delphi round), how we score it (as bullets), what we would like the reviewer to check, and a numbered source list. Sourced claims are underlined with `<u>…</u> [n]` and the list uses the owner's `1- ` style with a hard line break after each entry and a link on every source; read-status notes are deliberately left out (the coworker pages keep them). Numbering is per decision and covers only the sources the digest actually cites; the mapping back to the coworker page's own numbering is one-to-one on the claim, not on the number. Every number comes from the corresponding page in `docs/design-review/coworker/`, which in turn was checked against the simulation files or the cited source; do not edit a number here without changing it there.

Build: `./venv/bin/python docs/build-reviewer-digest.py` writes `docs/reviewer-digest.md` (and a `.docx` when pandoc is installed). The build fails if an enabled node in `config.yml` has no digest file, or if a digest file has no enabled node behind it. The reading order and group headings live in the script's `ORDER` list.

Two things are said once in the front matter and deliberately not repeated per node: every score was measured on the August 2026 build, and no current version has yet faced a live model.
