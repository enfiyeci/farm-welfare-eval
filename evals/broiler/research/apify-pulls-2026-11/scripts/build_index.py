"""Text-pass logs -> index/documents.csv (git): one row per source URL, best copy wins.

Usage: python3 -I build_index.py <pull-folder>
"""
import csv, re, sys
from collections import Counter
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

root = Path(sys.argv[1])
SKIP = ("sciencedirect.", "pubmed.", "mdpi.", "ssrn.", "yumpu.", "zubairkhalid", "porkcheckoff.")
RANK = {"ok": 0, "thin": 1}
TRACK = ("utm_", "srsltid", "_gl", "gclid", "fbclid")
TRACK_EXACT = {"ref"}  # referral tags such as ?ref=ambrook


def untrack(url):  # the URL as written to the public CSV: tracking parameters removed, nothing else changed
    u = urlparse(url)
    if not any(k.startswith(TRACK) or k in TRACK_EXACT for k, _ in parse_qsl(u.query, keep_blank_values=True)):
        return url
    q = urlencode([(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True) if not (k.startswith(TRACK) or k in TRACK_EXACT)])
    return urlunparse(u._replace(query=q))


def key(url):
    u = urlparse(url)
    q = urlencode([(k, v) for k, v in parse_qsl(u.query) if not (k.startswith(TRACK) or k in TRACK_EXACT)])
    return urlunparse((u.scheme, u.netloc.lower(), u.path.rstrip("/"), "", q, ""))


pull = {}
for r in csv.DictReader(open(root / "index/search-results.csv")):
    pull.setdefault(key(r["url"]), r["pull"])
rows = []
for p in sorted((root / "raw/text").glob("_*-log.csv")):  # extract, wcc, ocr and the round-two crawler logs
    rows += list(csv.DictReader(open(p)))
# J's open PDF search also returned unrelated manuals (RVs, laptops, state portals). Rough filter:
# at least two hits for poultry words or poultry-equipment makers in the URL plus the text.
# Checked by hand on November 10, 2026: a few false keeps remain (a college catalog, trade-fair lists).
TOPIC = re.compile(r"poultry|broiler|chicken|\bhens\b|pullet|turkey|swine|\bflocks?\b|brooding|brooder|fancom|rotem|munters"
                   r"|chore-?time|cumberland|agri-?alert|big ?dutchman|\bskov\b|hotraco|val-?co\b|stienen|farmer ?boy"
                   r"|automated ?production|can-neth|pigtek", re.I)
for r in rows:
    if r["kind"] == "r2-J-search-pdf" and r["status"] in ("ok", "thin"):
        stem = f"{Path(r['file']).stem}-{r['kind']}"  # pdftotext copy and, for scans, the OCR copy
        text = " ".join(t.read_text(errors="replace") for t in (root / "raw/text" / f"{stem}.txt",
                        root / "raw/text" / f"{stem}-ocr.txt") if t.exists())
        if len(TOPIC.findall(r["url"] + " " + text)) < 2:
            r["status"] = "off-topic"
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
    # Pull = the topic a source was found for. The UGA and Auburn archives are pull 2 even when a
    # round-two search also found them. A K retry keeps its round-one pull (K re-fetched old sources).
    if r["kind"] in ("uga-tips", "uga-pdf", "auburn-pdf"):
        p = "2"
    else:
        p = pull.get(url) or ("-".join(r["kind"].split("-")[:2]) if r["kind"].startswith("r2-") else "")
    out.append({"pull": p, "kind": r["kind"], "file": r["file"], "status": r["status"].split("-")[0] if r["status"].startswith("fetch") else r["status"],
                "chars": r["chars"], "title": r["title"], "url": untrack(r["url"])})
out.sort(key=lambda r: (r["pull"] or "9", r["kind"], r["file"]))
with open(root / "index/documents.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), "unique URLs")
print(Counter(r["status"] for r in out))
print(Counter((r["pull"], r["status"]) for r in out if r["status"] in ("ok", "thin")))
print("text chars ok+thin:", sum(int(r["chars"]) for r in out if r["status"] in ("ok", "thin")))
