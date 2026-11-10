"""Round two, pick I: transcript datasets -> raw/text/youtube/<id>.txt and the transcript columns
of index/youtube-videos.csv (other columns, grower_type included, are kept).

Usage: python3 -I r2_transcripts.py <pull-folder> <dataset.json>...
Later datasets win when a video appears twice (run I2 retried I1's other-language videos).
"""
import csv, json, sys, collections
from pathlib import Path
from urllib.parse import urlparse, parse_qs

root = Path(sys.argv[1])
got, fail = {}, {}
for src in sys.argv[2:]:
    for x in json.load(open(src)):
        vid = x.get("video_id") or parse_qs(urlparse(x.get("url", "")).query).get("v", [""])[0]
        text = (x.get("non_timestamped") or "").strip()
        if x.get("success") and text:
            got[vid] = x; fail.pop(vid, None)
        elif vid not in got:
            fail[vid] = x.get("error_type") or "unknown"

idx = root / "index/youtube-videos.csv"
rows = list(csv.DictReader(open(idx)))
tdir = root / "raw/text/youtube"; tdir.mkdir(parents=True, exist_ok=True)
n = 0
for r in rows:
    x = got.get(r["id"])
    if not x or r["transcript"] != "none":
        continue
    kind = "auto_generated" if str(x.get("is_generated")) == "True" else "user_generated"
    text = x["non_timestamped"].strip()
    (tdir / f"{r['id']}.txt").write_text(
        f"SOURCE: {r['url']}\nTITLE: {r['title']}\nCHANNEL: {r['channel']}\nDATE: {r['date']}\n"
        f"TRANSCRIPT: {kind} {x.get('language_code')} (johnvc/youtubetranscripts, round two)\n\n{text}\n")
    r["transcript"], r["transcript_chars"] = f"{kind}/{x.get('language_code')}", len(text)
    n += 1
with open(idx, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(n, "transcripts added;", len(fail), "videos still without:", collections.Counter(fail.values()))
print(collections.Counter(r["transcript"] for r in rows).most_common(12))
