"""Website Content Crawler dataset (raw/wcc/*.json) -> raw/text/*-wcc.txt plus raw/text/_wcc-log.csv.

Usage: python3 -I wcc_text.py <pull-folder> <dataset.json>
Pages from sites we chose to skip (paywalls, abstract-only, off-topic) are left out.
"""
import csv, json, re, sys
from pathlib import Path
from urllib.parse import urlparse

SKIP = ("sciencedirect.", "pubmed.", "mdpi.", "ssrn.", "yumpu.", "zubairkhalid", "porkcheckoff.")
root = Path(sys.argv[1]); items = json.load(open(sys.argv[2]))
out = root / "raw" / "text"
rows = []
for n, x in enumerate(items, 1):
    url = x.get("url") or (x.get("crawl") or {}).get("loadedUrl") or ""
    host = urlparse(url).netloc
    title = " ".join(((x.get("metadata") or {}).get("title") or "").split())[:150]
    text = (x.get("markdown") or x.get("text") or "").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    if any(s in host for s in SKIP):
        status = "skipped"
    elif len(text) < 400:
        status = "failed"
    else:
        status = "ok" if len(text) >= 1500 else "thin"
    name = f"w{n:03d}"
    if status in ("ok", "thin"):
        (out / f"{name}-wcc.txt").write_text(f"SOURCE: {url}\n\n{text}\n")
    rows.append({"file": f"wcc/{name}", "kind": "wcc", "http": (x.get("crawl") or {}).get("httpStatusCode", ""),
                 "status": status, "chars": len(text), "title": title, "url": url})
with open(out / "_wcc-log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r["status"] for r in rows))
