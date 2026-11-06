"""Text-pass logs -> index/documents.csv (git): one row per source URL, best copy wins.

Usage: python3 -I build_index.py <pull-folder>
"""
import csv, sys
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

root = Path(sys.argv[1])
SKIP = ("sciencedirect.", "pubmed.", "mdpi.", "ssrn.", "yumpu.", "zubairkhalid", "porkcheckoff.")
RANK = {"ok": 0, "thin": 1}
TRACK = ("utm_", "srsltid", "_gl", "gclid", "fbclid")


def key(url):
    u = urlparse(url)
    q = urlencode([(k, v) for k, v in parse_qsl(u.query) if not k.startswith(TRACK)])
    return urlunparse((u.scheme, u.netloc.lower(), u.path.rstrip("/"), "", q, ""))


pull = {}
for r in csv.DictReader(open(root / "index/search-results.csv")):
    pull.setdefault(key(r["url"]), r["pull"])
rows = []
for log in ("_extract-log.csv", "_wcc-log.csv"):
    p = root / "raw/text" / log
    if p.exists():
        rows += list(csv.DictReader(open(p)))
best = {}
for r in rows:
    url = key(r["url"])
    if any(s in urlparse(url).netloc for s in SKIP):
        r["status"] = "skipped"
    k = (RANK.get(r["status"], 2), -int(r["chars"] or 0))
    if url not in best or k < best[url][0]:
        best[url] = (k, r)
out = []
for url, (_, r) in best.items():
    p = pull.get(url) or ("2" if r["kind"] in ("uga-tips", "uga-pdf", "auburn-pdf") else "")
    out.append({"pull": p, "kind": r["kind"], "file": r["file"], "status": r["status"].split("-")[0] if r["status"].startswith("fetch") else r["status"],
                "chars": r["chars"], "title": r["title"], "url": r["url"]})
out.sort(key=lambda r: (r["pull"] or "9", r["kind"], r["file"]))
with open(root / "index/documents.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), "unique URLs")
print(Counter(r["status"] for r in out))
print(Counter((r["pull"], r["status"]) for r in out if r["status"] in ("ok", "thin")))
print("text chars ok+thin:", sum(int(r["chars"]) for r in out if r["status"] in ("ok", "thin")))
