"""Website Content Crawler dataset (raw/wcc/*.json) -> raw/text/*-wcc.txt plus raw/text/_wcc-log.csv.

Usage: python3 -I wcc_text.py <pull-folder> <dataset.json> [<prefix> <kind>]
Round one used the defaults (prefix w, kind wcc). Round two passes its own, for example
`kw r2-K-wcc`, which writes kw001-r2-K-wcc.txt and raw/text/_r2-K-wcc-log.csv.
Pages from sites we chose to skip (paywalls, abstract-only, off-topic) are left out.
Bot-check pages (Anubis, Cloudflare) and pages served with an HTTP error code (400 or
higher, such as a site's own "404 - Not Found" page) count as failed. Rows that only saved a file
(PDF or DOCX) have no text here; that file goes through extract.py instead.
"""
import csv, json, re, sys
from pathlib import Path
from urllib.parse import urlparse

SKIP = ("sciencedirect.", "pubmed.", "mdpi.", "ssrn.", "yumpu.", "zubairkhalid", "porkcheckoff.")
BOT = ("Making sure you're not a bot", "Verify you are human", "Just a moment...")
root = Path(sys.argv[1]); items = json.load(open(sys.argv[2]))
prefix, kind = (sys.argv[3], sys.argv[4]) if len(sys.argv) > 4 else ("w", "wcc")
log = "_wcc-log.csv" if kind == "wcc" else f"_{kind}-log.csv"
out = root / "raw" / "text"
rows = []
for n, x in enumerate(items, 1):
    url = x.get("url") or (x.get("crawl") or {}).get("loadedUrl") or ""
    host = urlparse(url).netloc
    title = " ".join(((x.get("metadata") or {}).get("title") or "").split())[:150]
    text = (x.get("markdown") or x.get("text") or "").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    http = (x.get("crawl") or {}).get("httpStatusCode")
    if any(s in host for s in SKIP):
        status = "skipped"
    elif isinstance(http, int) and http >= 400:
        status = "failed"
    elif len(text) < 400 or any(b in text[:600] for b in BOT):
        status = "failed"
    else:
        status = "ok" if len(text) >= 1500 else "thin"
    name = f"{prefix}{n:03d}"
    if status in ("ok", "thin"):
        (out / f"{name}-{kind}.txt").write_text(f"SOURCE: {url}\n\n{text}\n")
    rows.append({"file": f"{kind}/{name}", "kind": kind, "http": (x.get("crawl") or {}).get("httpStatusCode", ""),
                 "status": status, "chars": len(text), "title": title, "url": url})
with open(out / log, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r["status"] for r in rows))
