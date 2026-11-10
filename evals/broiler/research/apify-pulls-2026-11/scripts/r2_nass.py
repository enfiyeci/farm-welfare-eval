"""Pick C: NASS Poultry Slaughter annual summaries (raw/r2-C/pslaan*.txt) -> index/fsis-condemnations.csv.

Usage: python3 -I r2_nass.py <pull-folder>
One row per (year, cause): US young chickens condemned post-mortem by cause, in head, from the
"Young Chickens Condemned Post-Mortem by Cause and Month" table (FSIS inspection data published
by NASS), with the US young chickens slaughtered (head) for the same year as the denominator.
Each release carries two annual totals (this year and last); the newest release wins.
Miscellaneous is NASS footnote 1/: inflammatory process (cellulitis), plant-rejected carcasses,
missing viscera, or ascites fluid. Unknown (added 2021) is birds removed with no cause given.
"""
import csv, re, sys
from pathlib import Path

root = Path(sys.argv[1])


def nums(s):
    return [None if v in ("-", "(Z)", "(D)", "(NA)") else float(v.replace(",", "")) for v in s.split()]


def us_totals(lines, title, unit_words):
    """{cause: {year: value}} from the US rows of the named table's annual-total columns."""
    out, cause, cols, inside = {}, None, None, False
    for line in lines:
        if line.startswith(title):
            inside = True
            continue
        if inside and line.startswith(("Young Chickens", "Mature Chickens", "Turkeys", "Ducks")) and not line.startswith(title):
            inside = False
        if not inside:
            continue
        if ":" in line and re.search(r"\d{4} Total", line):
            cols = [c.strip() for c in line.split(":")[1:]]
            continue
        m = re.match(r"^([A-Z][A-Za-z ]+?)(?: \d/)?\s*:\s*$", line.rstrip())
        if m:
            cause = m.group(1).strip()
            continue
        if line.startswith("United States") and ":" in line and cols and cause:
            vals = nums(line.split(":", 1)[1])
            for c, v in zip(cols, vals):
                y = re.match(r"(\d{4}) Total", c)
                if y:
                    out.setdefault(cause, {})[int(y.group(1))] = v
    return out


CAUSES = {"Tuberculosis", "Leukosis", "Septicaemia", "Airsacculitis", "Synovitis", "Tumors", "Bruises",
          "Cadaver", "Contamination", "Overscald", "Miscellaneous", "Unknown", "Total"}
rows = {}
for f in sorted(root.glob("raw/r2-C/pslaan*.txt")):
    release = 2000 + int(re.search(r"pslaan(\d+)", f.name).group(1))
    lines = f.read_text(errors="replace").splitlines()
    causes = us_totals(lines, "Young Chickens Condemned Post-Mortem by Cause", "number head")
    head = us_totals(lines, "Young Chickens Slaughtered and Total Live Weight", "1,000 head")
    slaughtered = head.get("Slaughtered", {})
    for cause, years in causes.items():
        if cause not in CAUSES:  # rows from neighbouring tables
            continue
        for y, v in years.items():
            rows[(y, cause)] = {"year": y, "cause": cause, "head_condemned": None if v is None else int(v),
                                "young_chickens_slaughtered_1000_head": slaughtered.get(y) and int(slaughtered[y]),
                                "source": f.name, "release_year": release}
out = sorted(rows.values(), key=lambda r: (r["year"], r["cause"]))
with open(root / "index/fsis-condemnations.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for r in out:
    if r["year"] >= 2024:
        print(r)
