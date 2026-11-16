"""Assemble this folder's three HTML pages from body fragments.

Each page is: the <title> and fonts, the stylesheet and picker script taken from the sibling
FarmBench Design Critique page (so the three pages share its look and its "Copy my choices" bar),
and one body fragment from src/. Run from anywhere:

    python3 evals/hen/design/2026-11-15-free-checks/src/build_pages.py
"""
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent
SIBLING = OUT.parent / "2026-11-15-design-critique-and-ideas.html"

PAGES = {
    # output file: (title, storage key, first line of the copied text, body fragment)
    "e9-what-september-shows.html": (
        "FarmBench September Reading", "farmbench-free-checks-e9-v1",
        "FarmBench free check E9, what September shows (page of 2026-11-15):", "body-e9.html"),
    "e10-is-the-price-real.html": (
        "FarmBench Price Audit", "farmbench-free-checks-e10-v1",
        "FarmBench free check E10, is the price real (page of 2026-11-15):", "body-e10.html"),
    "approach-rubric-pilot-and-kate-draft.html": (
        "FarmBench Approach Rubric Pilot", "farmbench-free-checks-rubric-v1",
        "FarmBench approach rubric pilot and draft for Kate (page of 2026-11-15):", "body-rubric.html"),
}

EXTRA_CSS = """
/* additions for the free-checks pages; every colour is a token from the block above */
.status{display:inline-block;font-family:"Schibsted Grotesk",sans-serif;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;padding:2px 7px;white-space:nowrap}
.status.no{background:var(--warn-soft);color:var(--warn)}
.status.yes{background:var(--accent-soft);color:var(--accent)}
.status.open{background:transparent;color:var(--muted);box-shadow:inset 0 0 0 1px var(--rule)}
.letter{background:var(--sheet);padding:22px 26px;max-width:74ch;font-size:16.5px}
.letter p{max-width:none}
.wt{display:grid;grid-template-columns:minmax(0,1fr) 64px;gap:10px;align-items:center}
.wt-track{height:10px;background:var(--rule)}
.wt-track i{display:block;height:10px;background:var(--bar)}
.wt .v{font-family:"IBM Plex Mono",monospace;font-size:14px;text-align:right;font-variant-numeric:tabular-nums}
td.q-cell{min-width:220px}
.copybtn{font-family:"Schibsted Grotesk",sans-serif;font-size:13px;font-weight:700;padding:7px 12px;background:var(--accent);color:var(--on-accent);border:0;cursor:pointer;margin-top:10px}
.copybtn:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
"""

def main() -> None:
    sib = SIBLING.read_text(encoding="utf-8")
    style = re.search(r"<style>.*?</style>", sib, flags=re.S).group(0)
    style = style.replace("</style>", EXTRA_CSS + "</style>")
    script = re.search(r"<script>.*?</script>", sib, flags=re.S).group(0)
    head_links = "\n".join(re.findall(r"<link[^>]+>", sib[: sib.index("<style>")]))
    for name, (title, key, first_line, body) in PAGES.items():
        frag = HERE / body
        if not frag.exists():
            print(f"skip {name}: {body} not written yet")
            continue
        js = script.replace("farmbench-design-critique-v1", key).replace(
            "FarmBench design critique choices (page of 2026-11-15):", first_line)
        assert key in js and first_line in js, f"{name}: script substitution failed"
        page = (
            f"<title>{title}</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            f"{head_links}\n{style}\n\n<div class=\"wrap\">\n{frag.read_text(encoding='utf-8')}\n</div>\n\n"
            '<div class="bar-fixed"><span id="count"></span><button id="copy" type="button">Copy my choices</button></div>\n'
            '<textarea id="out" hidden aria-label="Your choices as text"></textarea>\n'
            f"{js}\n"
        )
        (OUT / name).write_text(page, encoding="utf-8")
        print(f"wrote {name}: {len(page)} bytes")

if __name__ == "__main__":
    main()
