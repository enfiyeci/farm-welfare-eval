"""OCR the near-empty PDFs (status too-short in raw/text/_extract-log.csv) into raw/text/*-ocr.txt
and add them to raw/text/_ocr-log.csv, which build_index.py reads alongside the other text logs.
PDFs already in that log are not read again, so a rerun only OCRs new ones.

Usage: python3 -I ocr.py <pull-folder>
Needs pdftoppm (poppler) and tesseract on PATH.
"""
import csv, subprocess, sys, tempfile
from pathlib import Path

root = Path(sys.argv[1])
out = root / "raw" / "text"
log = out / "_ocr-log.csv"
rows = list(csv.DictReader(open(log))) if log.exists() else []
done = {r["file"] for r in rows}
for r in csv.DictReader(open(out / "_extract-log.csv")):
    if r["status"] != "too-short" or not r["file"].endswith(".pdf") or r["file"] in done:
        continue
    src = root / "raw" / r["file"]
    text, status = "", "ok"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["pdftoppm", "-r", "300", "-gray", "-png", str(src), f"{tmp}/p"],
                           check=True, capture_output=True, timeout=600)
            for page in sorted(Path(tmp).glob("p*.png")):
                t = subprocess.run(["tesseract", str(page), "-", "-l", "eng"],
                                   capture_output=True, timeout=300)
                text += t.stdout.decode("utf-8", "replace") + "\n"
    except Exception as e:  # one bad file must not stop the batch
        status = f"error-{type(e).__name__}"
    text = "\n".join(l.rstrip() for l in text.splitlines()).strip()
    chars = len(text)
    if status == "ok":
        status = "too-short" if chars < 400 else "thin" if chars < 1500 else "ok"
    if text:
        (out / f"{src.stem}-{r['kind']}-ocr.txt").write_text(f"SOURCE: {r['url']}\nOCR: tesseract\n\n{text}\n")
    rows.append({"file": r["file"], "kind": r["kind"], "http": "200", "status": status,
                 "chars": chars, "title": r["title"], "url": r["url"]})
    print(r["file"], status, chars, flush=True)

with open(out / "_ocr-log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "kind", "http", "status", "chars", "title", "url"])
    w.writeheader(); w.writerows(rows)
from collections import Counter
print(len(rows), Counter(r["status"] for r in rows))
