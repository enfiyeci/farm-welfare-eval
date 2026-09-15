# Reviewer digest

The short version of the nodes pack: about 300 words per scored decision, for outside reviewers who asked for "the decision list" and would not read the 96,000-word pack. First written for Lukas Jasiūnas (Healthier Hens) in September 2026; the ordering puts the bird-side decisions first and the honesty and paperwork decisions last, with a boundary note between them.

One file per enabled node, plus:

- `00-front-matter.md`: what FarmBench is, the farm in five lines, how welfare is counted, what feedback helps, and the one open design question (what the model should be told about welfare).
- `99-boundary-note.md`: the note inserted before the three honesty groups.

Each node file has the same five fields: what happens, what it costs the birds (or the people), what we reward, what we would like the reviewer to check, and a one-line evidence summary. Every number comes from the corresponding page in `docs/design-review/coworker/`, which in turn was checked against the simulation files or the cited source; do not edit a number here without changing it there.

Build: `./venv/bin/python docs/build-reviewer-digest.py` writes `docs/reviewer-digest.md` (and a `.docx` when pandoc is installed). The build fails if an enabled node in `config.yml` has no digest file, or if a digest file has no enabled node behind it. The reading order and group headings live in the script's `ORDER` list.

Two things are said once in the front matter and deliberately not repeated per node: every score was measured on the August 2026 build, and no current version has yet faced a live model.
