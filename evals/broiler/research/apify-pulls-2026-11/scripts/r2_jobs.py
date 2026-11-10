"""Pick F job ads (raw/r2-F/indeed-*.json, linkedin-*.json) -> index/job-ads.csv (git).

Usage: python3 -I r2_jobs.py <pull-folder>
One row per ad: where it came from, title, company, place, date, pay as posted, and a rough
`topic` label: poultry (a poultry word or a poultry company in the title, company or
description), kitchen (the word broiler pulled in a cook or kitchen ad), or other.
Ad descriptions stay in raw/.
"""
import csv, glob, json, re, sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
POULTRY = re.compile(r"poultry|broiler|chicken|hatcher|pullet|\begg|\bhens?\b|turkey|perdue|pilgrim|sanderson|tyson"
                     r"|wayne|koch foods|mountaire|peco|foster farms|cal-maine|amick|case farms|george'?s|simmons", re.I)
KITCHEN = re.compile(r"\bcook|chef|kitchen|line cook|restaurant|dishwasher|grill", re.I)


FISH = re.compile(r"fish|aquacultur|salmon|trout", re.I)  # fish hatcheries match "hatcher" and "egg"


def topic(title, company, text):
    if FISH.search(title + " " + company):
        return "other"
    if KITCHEN.search(title):
        return "kitchen" if not POULTRY.search(company) else "poultry"
    return "poultry" if POULTRY.search(" ".join((title, company, text[:3000]))) else "other"


rows = []
for f in sorted(glob.glob(str(root / "raw/r2-F/indeed-*.json"))):
    for x in json.load(open(f)):
        t, c, d = x.get("positionName") or "", x.get("company") or "", x.get("description") or ""
        rows.append({"source": "indeed", "id": x.get("id", ""), "title": t, "company": c,
                     "location": x.get("location") or "", "posted": (x.get("postingDateParsed") or "")[:10],
                     "pay": x.get("salary") or "", "query": x.get("urlInput") or "",
                     "topic": topic(t, c, d), "url": x.get("url") or ""})
for f in sorted(glob.glob(str(root / "raw/r2-F/linkedin-*.json"))):
    for x in json.load(open(f)):
        t, c, d = x.get("title") or "", x.get("companyName") or "", x.get("descriptionText") or ""
        link = (x.get("link") or "").split("?")[0]  # drop LinkedIn tracking parameters
        rows.append({"source": "linkedin", "id": x.get("id", ""), "title": t, "company": c,
                     "location": x.get("location") or "", "posted": x.get("postedAt") or "",
                     "pay": x.get("salary") or "", "query": (x.get("inputUrl") or "").split("&")[0],
                     "topic": topic(t, c, d), "url": link})
with open(root / "index/job-ads.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), Counter((r["source"], r["topic"]) for r in rows))
print("with pay:", Counter(r["source"] for r in rows if r["pay"]))
