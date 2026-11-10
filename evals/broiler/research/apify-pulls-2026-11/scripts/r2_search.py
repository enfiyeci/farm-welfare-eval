"""Round two: one Google Search Scraper dataset -> index rows plus URL lists for plain download.

Usage: python3 -I r2_search.py <pull-folder> <pick letter> <dataset.json>
Appends the pick's rows to index/search-results.csv (pull = "r2-<pick>"; earlier rows of that
pick are replaced) and writes raw/r2-<pick>/urls-pdf.txt and urls-html.txt. Social media and
login-walled sites are dropped, as in round one; so are results whose title and snippet
mention no poultry word (off-topic hits).
"""
import csv, json, re, sys
from pathlib import Path
from urllib.parse import urlparse

root, pick, src = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
pull = f"r2-{pick}"
DROP = ("facebook.", "youtube.", "youtu.be", "instagram.", "reddit.", "linkedin.", "tiktok.", "twitter.",
        "x.com", "scribd.", "researchgate.", "academia.edu", "studocu.", "quora.", "pinterest.",
        "stock.weanimals.org", "sciencedirect.", "pubmed.", "mdpi.", "ssrn.", "yumpu.", "zubairkhalid")
TOPIC = re.compile(r"chicken|poultry|broiler|bird|hen\b|hens\b|flock|fowl|avian|grower|integrator|"
                   r"tournament|livestock|farm|shed|ammonia|tyson|perdue|pilgrim|sanderson|koch", re.I)

rows, seen = [], set()
for page in json.load(open(src)):
    q = page["searchQuery"]["term"]
    for r in page.get("organicResults") or []:
        url = r["url"]
        if url in seen:
            continue
        seen.add(url)
        rows.append({"pull": pull, "query": q, "title": r.get("title", ""), "url": url,
                     "desc": r.get("description", "")})

idx = root / "index/search-results.csv"
old = [r for r in csv.DictReader(open(idx)) if r["pull"] != pull]
with open(idx, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["pull", "query", "title", "url", "desc"])
    w.writeheader(); w.writerows(old + rows)

keep = [r for r in rows if not any(d in urlparse(r["url"]).netloc + "/" for d in DROP)
        and TOPIC.search(r["title"] + " " + r["desc"] + " " + r["url"])]
pdf = [r["url"] for r in keep if urlparse(r["url"]).path.lower().endswith(".pdf")]
html = [r["url"] for r in keep if r["url"] not in pdf]
out = root / "raw" / pull
out.mkdir(parents=True, exist_ok=True)
(out / "urls-pdf.txt").write_text("\n".join(pdf) + "\n")
(out / "urls-html.txt").write_text("\n".join(html) + "\n")
print(f"{pull}: {len(rows)} unique results, {len(rows) - len(keep)} dropped, {len(pdf)} PDFs, {len(html)} pages")
