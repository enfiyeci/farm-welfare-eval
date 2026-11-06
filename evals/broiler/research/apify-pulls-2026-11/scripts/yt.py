"""YouTube dataset -> index/youtube-videos.csv (git) and raw/text/youtube/*.txt (not git)."""
import csv, json, sys, collections
from pathlib import Path
root = Path(sys.argv[1]); src = Path(sys.argv[2])
d = json.load(open(src))
tdir = root / "raw/text/youtube"; tdir.mkdir(parents=True, exist_ok=True)
rows = []
for x in d:
    subs = x.get("subtitles") or []
    en = [s for s in subs if (s.get("language") or "").startswith("en")] or subs
    s = en[0] if en else {}
    text = (s.get("plaintext") or "").strip()
    if text:
        (tdir / f"{x['id']}.txt").write_text(
            f"SOURCE: {x['url']}\nTITLE: {x.get('title')}\nCHANNEL: {x.get('channelName')}\nDATE: {x.get('date')}\n"
            f"TRANSCRIPT: {s.get('type')} {s.get('language')}\n\n{text}\n")
    q = x.get("input") or x.get("fromYTUrl") or ""
    rows.append({"id": x["id"], "query": q, "title": x.get("title"), "channel": x.get("channelName"),
                 "date": (x.get("date") or "")[:10], "duration": x.get("duration"), "views": x.get("viewCount"),
                 "transcript": f"{s.get('type')}/{s.get('language')}" if text else "none",
                 "transcript_chars": len(text), "url": x["url"]})
idx = root / "index/youtube-videos.csv"
labels = {r["id"]: r for r in csv.DictReader(open(idx))} if idx.exists() else {}
for r in rows:  # keep the grower_type labels added by hand-checked passes
    old = labels.get(r["id"], {})
    if "grower_type" in old:
        r["grower_type"], r["label_note"] = old["grower_type"], old.get("label_note", "")
with open(idx, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows), "rows;", sum(r["transcript"] != "none" for r in rows), "with transcript;",
      sum(r["transcript_chars"] for r in rows), "transcript chars")
print(collections.Counter(r["transcript"] for r in rows).most_common(8))
print(collections.Counter(r["query"] for r in rows).most_common(30))
