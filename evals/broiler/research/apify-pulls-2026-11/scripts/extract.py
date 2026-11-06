"""Extract text from raw/pdf and raw/html into raw/text, and write an extraction log.

Usage: python3 -I extract.py <pull-folder>
"""
import csv, html, re, subprocess, sys
from html.parser import HTMLParser
from pathlib import Path

root = Path(sys.argv[1])
out = root / "raw" / "text"
out.mkdir(parents=True, exist_ok=True)

SKIP = {"script", "style", "noscript", "svg", "nav", "footer", "header", "form", "iframe", "template"}
BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "table", "td", "th", "dd", "dt", "pre", "blockquote"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.title, self.in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag == "title":
            self.in_title = True
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag == "title":
            self.in_title = False
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        elif not self.skip:
            self.parts.append(data)


def clean(s):
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    lines = [l.strip() for l in s.split("\n")]
    s = "\n".join(l for l in lines)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def read_log(path):
    rows = {}
    if path.exists():
        for line in path.read_text(errors="replace").splitlines():
            f = line.split("\t")
            if len(f) >= 4:
                rows[f[0]] = (f[1], f[2], f[3])
    return rows


results = []
for kind in ("pdf", "html", "html-rescue", "uga-tips", "uga-pdf", "auburn-pdf"):
    log = read_log(root / "raw" / kind / "_log.tsv")
    for name, (code, ctype, url) in sorted(log.items()):
        src = root / "raw" / kind / name
        dest = out / (src.stem + "-" + kind + ".txt")
        status, title, chars = "", "", 0
        if code != "200" or not src.exists() or src.stat().st_size == 0:
            status = f"fetch-failed-{code}"
        else:
            head = src.read_bytes()[:5]
            try:
                if head.startswith(b"%PDF") and subprocess.run(["pdfinfo", str(src)], capture_output=True).returncode != 0:
                    text, status = "", "broken-pdf"  # usually cut off by the download timeout
                elif head.startswith(b"%PDF"):
                    r = subprocess.run(["pdftotext", "-layout", "-q", str(src), "-"], capture_output=True, timeout=120)
                    text = r.stdout.decode("utf-8", "replace")
                    status = "ok" if r.returncode == 0 else f"pdftotext-error-{r.returncode}"
                elif kind.endswith("pdf"):
                    text, status = "", "not-a-pdf"
                else:
                    p = Text()
                    p.feed(src.read_bytes().decode("utf-8", "replace"))
                    text, title, status = "".join(p.parts), clean(p.title), "ok"
            except Exception as e:  # one bad file must not stop the batch
                text, status = "", f"error-{type(e).__name__}"
            text = clean(text)
            chars = len(text)
            if status == "ok" and chars < 400:
                status = "too-short"  # empty or near-empty: scanned PDF, script-only page
            elif status == "ok" and chars < 1500:
                status = "thin"
            if text:
                dest.write_text(f"SOURCE: {url}\n\n{text}\n")
        results.append({"file": f"{kind}/{name}", "kind": kind, "http": code, "status": status,
                        "chars": chars, "title": title[:150], "url": url})

with open(out / "_extract-log.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
    w.writeheader()
    w.writerows(results)

from collections import Counter
print(Counter((r["kind"], r["status"].split("-")[0] if r["status"].startswith("fetch") else r["status"]) for r in results))
