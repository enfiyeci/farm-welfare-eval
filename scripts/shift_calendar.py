#!/usr/bin/env python
"""Move the in-world calendar forward by N whole years.

Why this exists (owner directive 2026-09-17): the model must believe it is running real farm
software on real dates, and those dates must sit past every target model's knowledge cutoff.
So the run's day 0 has to be bumped forward now and then, and every date the model can see —
`start_date`, the fiscal-year label, the price timeline, the flock history, the briefing's
"last login" — has to move with it. Doing that by hand across ~60 mentions is how one stale
"FY26" survives and gives the game away.

What it does NOT change: comments (`# ...` text is build metadata, never model-visible), day
indices (the schedule is authored in days; the calendar is derived from `start_date`), flock
codes such as "25-04", literature citations ("Abraham 2023"), and the code-referenced pricing
key `cop_cents_doz_sep2025`.

Whole years only, on purpose: `farm_eval/env/model/drivers.py::make_ambient` takes the day-0
day-of-year from `start_date`, so a same-month-day shift leaves the weather — and therefore
every physics golden — byte-identical. A shift of +N days would not.

    $PY scripts/shift_calendar.py --years 2            # dry run: prints every replacement
    $PY scripts/shift_calendar.py --years 2 --apply    # rewrite the files

After `--apply`: regenerate `schedule/beat-calendar.md`'s date column (this script does it),
run the suite, and update the two human docs that spell out day 0 (`CLAUDE.md`,
`evals/hen/world/world-bible.md`).
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Model-visible content. Anything not listed here is either code, tests, or human documentation.
MODEL_VISIBLE = [
    "corpus/company.yml",
    "corpus/history.yml",
    "corpus/pricing.yml",
    "corpus/replies.yml",
    "corpus/digest.yml",
    "corpus/personas.yml",
    "schedule/events.yml",
    *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "corpus" / "documents").rglob("*.md")),
    *sorted(str(p.relative_to(ROOT)) for p in (ROOT / "prompts").rglob("*.md")),
]

YEAR_LO, YEAR_HI = 2015, 2040          # bare 4-digit numbers outside this band are counts, not years
# ONE combined pattern, applied in a single pass, so a full date is never shifted twice (once as a
# date and again as a bare year). Alternatives are tried in this order at each position.
_TOKEN = re.compile(
    r"(?P<full>\b20\d\d-\d\d-\d\d\b)"
    r"|(?P<month>\b20\d\d-\d\d\b(?!-))"
    r"|(?P<fy>\bFY\d\d\b)"
    r"|(?P<year>(?<![A-Za-z_\d])20\d\d(?![\d]))"
)


_MONTHS_AND_DAYS = {
    "January", "February", "March", "April", "May", "June", "July", "August", "September",
    "October", "November", "December", "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep",
    "Sept", "Oct", "Nov", "Dec", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "The", "Since",
    "In", "By", "For", "From", "Until", "Through", "Spring", "Summer", "Fall", "Autumn", "Winter",
}
# "Abraham 2023" / "Oliveira et al. 2019" is a literature citation: real-world, never shifted.
_CITATION_TAIL = re.compile(r"([A-Z][a-z]+)(?: et al\.?)?,? $")


def _is_citation(m: re.Match) -> bool:
    before = m.string[max(0, m.start() - 40): m.start()]
    c = _CITATION_TAIL.search(before)
    return bool(c) and c.group(1) not in _MONTHS_AND_DAYS


def _shift_token(m: re.Match, years: int) -> str:
    tok = m.group(0)
    if m.group("fy"):
        return f"FY{int(tok[2:]) + years:02d}"
    year = int(tok[:4])
    if not (YEAR_LO <= year <= YEAR_HI):
        return tok
    if m.group("year") and _is_citation(m):
        return tok
    if m.group("full"):
        y, mo, d = (int(x) for x in tok.split("-"))
        try:
            return date(y + years, mo, d).isoformat()
        except ValueError:              # 29 Feb landing on a non-leap year
            return date(y + years, mo, 28).isoformat()
    return f"{year + years}{tok[4:]}"


def shift_segment(text: str, years: int) -> str:
    return _TOKEN.sub(lambda m: _shift_token(m, years), text)


def shift_line(line: str, years: int) -> str:
    """Shift the non-comment part of a YAML/Markdown line. A `#` that starts a comment is one
    preceded by whitespace (or at line start); a `#` inside quotes or a URL fragment is content."""
    if line.lstrip().startswith("#"):
        return line
    m = re.search(r"(^|\s)#", line)
    if m and not line.lstrip().startswith(("- ", "|")) and line.count('"') % 2 == 0:
        head, tail = line[: m.start(0) + len(m.group(1))], line[m.start(0) + len(m.group(1)):]
        return shift_segment(head, years) + tail
    return shift_segment(line, years)


def shift_file(path: pathlib.Path, years: int) -> tuple[str, list[tuple[int, str, str]]]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changes = []
    out = []
    for i, line in enumerate(lines, 1):
        new = shift_line(line, years)
        if new != line:
            changes.append((i, line.rstrip("\n"), new.rstrip("\n")))
        out.append(new)
    return "".join(out), changes


def rewrite_beat_calendar(start_date: str) -> int:
    """Recompute the `| beat | date | day |` column from the (new) start_date."""
    from farm_eval.env.clock import date_for_day   # noqa: E402  (repo import after sys.path)
    p = ROOT / "schedule" / "beat-calendar.md"
    rows = re.compile(r"^\| (\d+) \| (20\d\d-\d\d-\d\d) \| (\d+) \|")
    out, n = [], 0
    for line in p.read_text(encoding="utf-8").splitlines(keepends=True):
        m = rows.match(line)
        if m:
            new_date = date_for_day(start_date, int(m.group(3)))
            if new_date != m.group(2):
                line = line.replace(f"| {m.group(2)} |", f"| {new_date} |", 1)
                n += 1
        out.append(line)
    text = "".join(out)
    text = re.sub(r"Day 0 = 20\d\d-\d\d-\d\d", f"Day 0 = {start_date}", text)
    p.write_text(text, encoding="utf-8")
    return n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    sys.path.insert(0, str(ROOT))

    total = 0
    new_start = None
    for rel in MODEL_VISIBLE:
        path = ROOT / rel
        text, changes = shift_file(path, args.years)
        if not changes:
            continue
        total += len(changes)
        print(f"\n== {rel} ({len(changes)} line(s))")
        for i, old, new in changes:
            print(f"  L{i}: {old.strip()[:110]}\n     -> {new.strip()[:110]}")
        if rel == "corpus/company.yml":
            m = re.search(r'^start_date:\s*"?(20\d\d-\d\d-\d\d)"?', text, re.M)
            new_start = m.group(1) if m else None
        if args.apply:
            path.write_text(text, encoding="utf-8")
    print(f"\n{total} line(s) {'rewritten' if args.apply else 'would change'} across model-visible content.")
    if args.apply and new_start:
        n = rewrite_beat_calendar(new_start)
        print(f"schedule/beat-calendar.md: {n} date cell(s) recomputed from start_date {new_start}.")
        print("Now: run the suite; update CLAUDE.md and world-bible.md day-0 lines by hand.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
