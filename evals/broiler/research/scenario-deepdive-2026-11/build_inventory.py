"""Build inventory.html from claims.json and the per-scenario prompts.md files."""
import html
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "claims.json").read_text())
ORDER = ["N", "C", "W", "S", "V"]
LABEL = {"N": "No source", "C": "Conflicts", "W": "Weak", "S": "Secondary", "V": "Verified"}


def esc(s):
    return html.escape(s, quote=True)


def counts(sc):
    c = {k: 0 for k in ORDER}
    for cl in sc["claims"]:
        c[cl["s"]] += 1
    return c


def rank_key(sc):
    c = counts(sc)
    return (-(c["N"] + c["C"]), -c["W"], sc["no"])


def prompt_blocks(folder):
    text = (folder / "prompts.md").read_text()
    core = re.search(r"```text\n(.*?)```", text, re.S).group(1).strip()
    elicit = re.findall(r"^\d+\. `(.+?)`\n\s+Columns: (.+)$", text, re.M)
    return core, elicit


scenarios = sorted(DATA["scenarios"], key=rank_key)
rows = []
for rank, sc in enumerate(scenarios, 1):
    c = counts(sc)
    chips = "".join(
        f'<span class="chip s-{k}" title="{LABEL[k]}">{c[k]}</span>' if c[k] else '<span class="chip empty">0</span>'
        for k in ORDER
    )
    claims = "".join(
        f'<li><span class="pill s-{cl["s"]}">{LABEL[cl["s"]]}</span>'
        f'<span class="ct">{esc(cl["t"])}</span><span class="src">{esc(cl["src"])}</span></li>'
        for cl in sorted(sc["claims"], key=lambda x: ORDER.index(x["s"]))
    )
    extra = ""
    if sc.get("gaps"):
        extra += '<p class="sub">Gaps</p><ul class="plain">' + "".join(f"<li>{esc(g)}</li>" for g in sc["gaps"]) + "</ul>"
    if sc.get("leads"):
        extra += '<p class="sub">Already downloaded, not read yet</p><ul class="plain">' + "".join(
            f"<li>{esc(g)}</li>" for g in sc["leads"]) + "</ul>"
    kind = '<span class="kind">outcome of breed choice</span>' if sc["kind"] == "outcome" else ""
    first = ' <span class="now">first deep-dive</span>' if sc["no"] == 4 else ""
    rows.append(f"""
<details class="row" id="s{sc['no']}"{' open' if sc['no'] == 4 else ''}>
  <summary>
    <span class="rank">{rank}</span>
    <span class="name"><b>{esc(sc['title'])}</b>{first}<small>Node {sc['no']} · {esc(sc['family'])} {kind}</small></span>
    <span class="chips">{chips}</span>
  </summary>
  <div class="body"><ul class="claims">{claims}</ul>{extra}</div>
</details>""")

totals = {k: sum(counts(s)[k] for s in scenarios) for k in ORDER}
legend = "".join(f'<li><span class="pill s-{k}">{LABEL[k]}</span>{esc(DATA["status_key"][k])}</li>' for k in ORDER)
new_src = "".join(
    f'<li><a href="{esc(s["url"])}">{esc(s["name"])}</a>. {esc(s["read"])}</li>' for s in DATA["new_sources"])

core, elicit = prompt_blocks(HERE / "04-leg-disorders")
elicit_html = "".join(
    f'<div class="q"><button type="button" class="copy" data-target="e{i}">Copy</button>'
    f'<p id="e{i}" class="qt">{esc(q)}</p><p class="cols">Add columns: {esc(cols)}</p></div>'
    for i, (q, cols) in enumerate(elicit, 1))

page = f"""<title>Broiler Claim Inventory</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: one reading column; a ranked list of expandable scenario rows, then the prompt kit. */
:root {{
  --bg: #f3f5f2; --panel: #ffffff; --fg: #1d2420; --muted: #5b665f; --line: #d9ded8; --accent: #2f5d50;
  --N: #b3261e; --N-bg: #fbe9e7; --C: #a3540a; --C-bg: #fdf0e1; --W: #7a6400; --W-bg: #f8f2d6;
  --S: #2b5a8a; --S-bg: #e5eef8; --V: #2d6a3e; --V-bg: #e3f2e6;
  --display: "Newsreader", Georgia, serif; --body: "IBM Plex Sans", system-ui, sans-serif; --mono: "IBM Plex Mono", ui-monospace, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #141917; --panel: #1c2320; --fg: #e3e8e4; --muted: #9aa69f; --line: #2f3833; --accent: #8fc4b3;
  --N: #f2a29b; --N-bg: #3a1f1d; --C: #f0b77c; --C-bg: #3a2a18; --W: #e2cf73; --W-bg: #332e17;
  --S: #9cc2ea; --S-bg: #1c2b3b; --V: #9fd4ab; --V-bg: #1c3222; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #141917; --panel: #1c2320; --fg: #e3e8e4; --muted: #9aa69f; --line: #2f3833; --accent: #8fc4b3;
  --N: #f2a29b; --N-bg: #3a1f1d; --C: #f0b77c; --C-bg: #3a2a18; --W: #e2cf73; --W-bg: #332e17;
  --S: #9cc2ea; --S-bg: #1c2b3b; --V: #9fd4ab; --V-bg: #1c3222; color-scheme: dark; }}
body {{ background: var(--bg); color: var(--fg); font: 15px/1.55 var(--body); }}
.wrap {{ max-width: 920px; margin: 0 auto; padding-block: 32px 64px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 28px; }}
h1, h2 {{ font-family: var(--display); font-weight: 600; text-wrap: balance; margin: 0; line-height: 1.15; }}
h1 {{ font-size: 2.1rem; }} h2 {{ font-size: 1.45rem; }}
p {{ margin: 0; max-width: 68ch; }}
a {{ color: var(--accent); }}
.lede {{ display: grid; gap: 10px; }}
.eyebrow {{ font: 500 0.75rem var(--mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); }}
.totals {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.pill, .chip {{ font: 500 0.72rem var(--mono); border-radius: 4px; white-space: nowrap; }}
.pill {{ padding: 2px 7px; }}
.chip {{ display: inline-grid; place-items: center; min-width: 26px; height: 24px; }}
.chip.empty {{ color: var(--line); }}
{''.join(f'.s-{k} {{ color: var(--{k}); background: var(--{k}-bg); }} ' for k in ORDER)}
section {{ display: grid; gap: 12px; }}
.legend, .plain {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 6px; }}
.legend li {{ display: grid; grid-template-columns: 92px 1fr; gap: 10px; align-items: baseline; }}
.plain li {{ padding-left: 14px; position: relative; }}
.plain li::before {{ content: "–"; position: absolute; left: 0; color: var(--muted); }}
.head {{ display: grid; grid-template-columns: 34px 1fr auto; gap: 12px; padding: 0 14px; font: 500 0.7rem var(--mono); color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }}
.head .chips span {{ width: 26px; text-align: center; }}
.list {{ display: grid; gap: 6px; }}
.row {{ background: var(--panel); border: 1px solid var(--line); border-radius: 6px; }}
.row summary {{ display: grid; grid-template-columns: 34px 1fr auto; gap: 12px; align-items: center; padding: 10px 14px; cursor: pointer; list-style: none; }}
.row summary::-webkit-details-marker {{ display: none; }}
.row summary:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
.rank {{ font: 600 1.1rem var(--display); color: var(--muted); font-variant-numeric: tabular-nums; }}
.name {{ display: grid; min-width: 0; }}
.name small {{ color: var(--muted); font-size: 0.8rem; }}
.kind {{ font: 0.72rem var(--mono); color: var(--muted); border: 1px dashed var(--line); border-radius: 4px; padding: 0 5px; margin-left: 4px; }}
.now {{ font: 500 0.72rem var(--mono); color: var(--panel); background: var(--accent); border-radius: 4px; padding: 1px 6px; justify-self: start; margin: 2px 0; }}
.chips {{ display: flex; gap: 4px; }}
.body {{ border-top: 1px solid var(--line); padding: 12px 14px 16px 60px; display: grid; gap: 8px; }}
.claims {{ margin: 0; padding: 0; list-style: none; display: grid; gap: 10px; }}
.claims li {{ display: grid; grid-template-columns: 92px 1fr; column-gap: 10px; }}
.claims .pill {{ grid-row: span 2; align-self: start; text-align: center; }}
.ct {{ min-width: 0; }}
.src {{ color: var(--muted); font-size: 0.82rem; }}
.sub {{ font: 500 0.72rem var(--mono); text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin-top: 6px; }}
.kit {{ background: var(--panel); border: 1px solid var(--line); border-radius: 6px; padding: 18px; display: grid; gap: 14px; }}
.kit h3 {{ margin: 0; font: 600 1rem var(--body); }}
pre {{ margin: 0; white-space: pre-wrap; overflow-wrap: anywhere; font: 0.8rem/1.5 var(--mono); background: var(--bg); border: 1px solid var(--line); border-radius: 4px; padding: 12px; max-height: 340px; overflow: auto; }}
.copy {{ justify-self: start; font: 500 0.8rem var(--body); color: var(--panel); background: var(--accent); border: 0; border-radius: 4px; padding: 6px 12px; cursor: pointer; }}
.copy:focus-visible {{ outline: 2px solid var(--fg); outline-offset: 2px; }}
.q {{ display: grid; grid-template-columns: auto 1fr; gap: 4px 12px; align-items: start; }}
.q .cols {{ grid-column: 2; color: var(--muted); font-size: 0.82rem; }}
.qt {{ font-family: var(--mono); font-size: 0.82rem; }}
.notes li {{ max-width: 68ch; }}
@media (max-width: 560px) {{
  .head {{ display: none; }}
  .row summary {{ grid-template-columns: 26px 1fr; }}
  .chips {{ grid-column: 2; }}
  .body {{ padding-left: 14px; }}
  .claims li, .legend li {{ grid-template-columns: 1fr; row-gap: 4px; }}
  .claims .pill {{ grid-row: auto; justify-self: start; }}
}}
</style>
<div class="wrap">
  <header class="lede">
    <span class="eyebrow">FarmBench · broiler · as of {DATA['as_of']}</span>
    <h1>Which broiler welfare claims have a source</h1>
    <p>Every welfare-effect claim in the 20 candidate broiler scenarios, taken from the six research memos of September 21 and checked against two documents found in the November Apify pull. Scenarios are ranked by claims with no source or a conflicting source, then by claims resting on weak sources.</p>
    <div class="totals">{''.join(f'<span class="pill s-{k}">{totals[k]} {LABEL[k].lower()}</span>' for k in ORDER)}</div>
  </header>

  <section>
    <h2>What the labels mean</h2>
    <ul class="legend">{legend}</ul>
    <p class="src">What counts as one claim is my judgment, so read the counts as an order, not a measurement. Standards thresholds, costs and food-safety claims are left out; only claims about what happens to the birds are counted.</p>
  </section>

  <section>
    <h2>Ranked scenarios</h2>
    <div class="head"><span>#</span><span>Scenario</span><span class="chips">{''.join(f'<span>{k}</span>' for k in ORDER)}</span></div>
    <div class="list">{''.join(rows)}</div>
  </section>

  <section class="notes">
    <h2>What changed while building this</h2>
    <ul class="plain">
      <li>Two documents already in the Apify pull moved 26 claims from "no source" to "secondary":</li>
      {new_src}
      <li>Six memo claims now conflict with a source: darkness helping mainly by slowing growth (RSPCA points to activity instead), the gait-score-3 triage (RSPCA culls at 3), string as enrichment (RSPCA advises against it), the U-shaped feed-withdrawal curve (EFSA 2004 found no definitive food-safety evidence), skip-a-day being worse (Morrissey 2014 found no difference), and "no welfare-correct thinning" (EFSA 2023 suggests thinning when litter cannot be kept dry).</li>
      <li>Later on 2026-11-05 the rest of EFSA 2023 was read in full, and every status change was checked against its text. It moved 13 more claims: nine to "secondary" and four to "conflicts" (the single density threshold, damage above 30% litter moisture, sitting 70 to 80% of the time, and high-fibre bulk making birds ill). Details are in efsa-2023-full-read/checked-findings.md.</li>
      <li>On 2026-11-06 the Gemini Deep Research report on leg disorders was checked claim by claim (twelve subagents, every status change re-checked against raw source text). Scenario 4 lost all four of its unsourced claims: two now conflict, one is secondary and one is verified, and four new claims were added. See 04-leg-disorders/verified.md and adjudicated.md.</li>
      <li>Scenarios 2 to 5 are outcomes of the breed decision, not choices of their own. The September handoff suggested folding them into scenario 1. Counted together, that family has 16 unsourced or conflicting claims, the most of any.</li>
    </ul>
  </section>

  <section id="kit">
    <h2>First deep-dive: leg disorders</h2>
    <p>Paste the core prompt into whichever of Gemini, ChatGPT or Perplexity has usage left. Ask Elicit the four narrow questions one at a time. Then paste each tool's whole answer back to me; I check every figure against the source it cites before anything changes in the scenario.</p>
    <div class="kit">
      <h3>Core prompt (Gemini, ChatGPT, Perplexity)</h3>
      <button type="button" class="copy" data-target="core">Copy prompt</button>
      <pre id="core">{esc(core)}</pre>
      <h3>Elicit questions</h3>
      {elicit_html}
    </div>
  </section>
</div>
<script>
document.querySelectorAll('.copy').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var el = document.getElementById(b.dataset.target), label = b.textContent;
    function done(t) {{ b.textContent = t; setTimeout(function () {{ b.textContent = label; }}, 1600); }}
    function selectIt() {{ var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); done('Selected, press copy'); }}
    if (navigator.clipboard && navigator.clipboard.writeText) {{
      navigator.clipboard.writeText(el.textContent).then(function () {{ done('Copied'); }}, selectIt);
    }} else {{ selectIt(); }}
  }});
}});
</script>
"""
(HERE / "inventory.html").write_text(page)
print("wrote inventory.html;", {k: totals[k] for k in ORDER})
