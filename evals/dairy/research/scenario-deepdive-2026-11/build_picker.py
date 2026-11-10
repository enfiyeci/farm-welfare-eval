"""Build picker.html from candidates.json. Run: python3 build_picker.py"""
import html
import json
from pathlib import Path

HERE = Path(__file__).parent
D = json.loads((HERE / "candidates.json").read_text())
ORDER = ["N", "C", "W", "S", "V"]
LABEL = {"N": "No source", "C": "Conflicts", "W": "Weak", "S": "Secondary", "V": "Verified"}
CAT = {"false_binary": "False binary", "welfare_profit": "Welfare vs profit", "welfare_cost": "Welfare cost",
       "integrity": "Integrity", "initiative": "Initiative", "epistemic": "Epistemic"}
# Firm hen register (evals/hen/nodes/decision-register.md, category balance line).
HEN = {"false_binary": 5, "welfare_profit": 4, "welfare_cost": 3, "integrity": 4, "initiative": 3, "epistemic": 2}
REC = {"build": "Build", "later": "Later", "drop": "Drop"}


def esc(s):
    return html.escape(str(s), quote=True)


def counts(c):
    n = {k: 0 for k in ORDER}
    for cl in c["claims"]:
        n[cl["s"]] += 1
    return n


def framing():
    out = []
    for q in D["framing"]:
        opts = "".join(
            f'<label class="fq"><input type="radio" name="{q["id"]}" value="{o["key"]}" data-label="{esc(o["label"])}"'
            f'{" checked" if o.get("rec") else ""}><span><b>{o["key"]}. {esc(o["label"])}</b>'
            f'{"<span class=rec>recommended</span>" if o.get("rec") else ""}<br>{esc(o["text"])}</span></label>'
            for o in q["options"])
        out.append(f'<fieldset class="q" data-q="{q["id"]}"><legend><span class="qid">{q["id"]}</span>{esc(q["q"])}</legend>'
                   f'<p class="muted small">{esc(q["why"])}</p><div class="fopts">{opts}</div></fieldset>')
    return "".join(out)


def corpus():
    rows = "".join(f'<tr><td><b>{esc(r["what"])}</b><br><code>{esc(r["path"])}</code></td><td>{esc(r["gives"])}</td>'
                   f'<td class="muted">{esc(r["status"])}</td></tr>' for r in D["corpus"])
    catches = "".join(f"<li>{esc(c)}</li>" for c in D["catches"])
    return rows, catches


def candidate(c):
    n = counts(c)
    chips = "".join(f'<span class="chip s-{k}" title="{LABEL[k]}">{k}{n[k]}</span>' for k in ORDER if n[k])
    claims = "".join(
        f'<li><span class="pill s-{cl["s"]}">{LABEL[cl["s"]]}</span><span class="ct">{esc(cl["t"])}</span>'
        f'<span class="src">{esc(cl["src"])}</span></li>'
        for cl in sorted(c["claims"], key=lambda x: ORDER.index(x["s"])))
    rec = c["rec"]
    rtag = '<span class="tag t-ok">recommended</span>' if rec == "build" else '<span class="tag t-plain">later</span>'
    ttag = f'<span class="tag t-{"bad" if c["type"] == "Invert" else "plain"}">{esc(c["type"])}</span>'
    hen = f' · hen analog {esc(c["hen"])}' if c["hen"] else ""
    choose = "".join(
        f'<label><input type="radio" name="{c["id"]}" value="{v}"{" checked" if v == rec else ""}>'
        f'<span>{REC[v]}{"<span class=rec>rec</span>" if v == rec else ""}</span></label>'
        for v in ("build", "later", "drop"))
    return f'''
<div class="opt" data-id="{c["id"]}" data-name="{esc(c["title"])}" data-cat="{c["category"]}">
  <div class="id">{c["id"]}</div>
  <div>
    <h3>{esc(c["title"])} {rtag} {ttag}</h3>
    <p class="what">{esc(c["tension"])}</p>
    <dl>
      <dt>Welfare</dt><dd>{esc(c["welfare"])}</dd>
      <dt>Profit</dt><dd>{esc(c["profit"])}</dd>
      <dt>Shape</dt><dd class="mono">{CAT[c["category"]]} · {esc(c["arity"])} · {esc(c["prompted"])} · root cause {esc(c["root"])}{hen} · keys on {esc(c["keys_on"])}</dd>
    </dl>
    <details><summary>{len(c["claims"])} welfare claims <span class="chips">{chips}</span></summary><ul class="claims">{claims}</ul></details>
  </div>
  <div class="choose">{choose}</div>
</div>'''


def picks():
    out = []
    for f in D["families"]:
        cs = [c for c in D["candidates"] if c["family"] == f["id"]]
        out.append(f'<div class="opt-group">{f["id"]}. {esc(f["name"])} <span class="muted">({len(cs)})</span></div>')
        out.extend(candidate(c) for c in cs)
    return "".join(out)


total = len(D["candidates"])
rec_build = sum(c["rec"] == "build" for c in D["candidates"])
all_claims = [cl for c in D["candidates"] for cl in c["claims"]]
nclaims = len(all_claims)
nN = sum(cl["s"] in ("N", "C") for cl in all_claims)
rows, catches = corpus()
tally = "".join(
    f'<div class="trow" data-cat="{k}"><span class="tl">{v}</span><span class="tm"></span>'
    f'<span class="tn mono"><b class="js-n">0</b> picked · hen {HEN[k]}</span></div>' for k, v in CAT.items())

page = f'''<!doctype html>
<!-- Eval: dairy. Written 2026-11-10 by build_picker.py from candidates.json. Do not edit by hand. -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dairy Scenario Picker</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{
  --paper:#F4F4F2; --panel:#E9EAE6; --ink:#16181A; --muted:#575B60; --rule:#D3D5D0;
  --accent:#B8321B; --accent-bg:#F6E3DE; --ok:#2C6636; --ok-bg:#DFEDE1; --warn:#7A5300; --warn-bg:#F3E8CF;
  --bar:#3B3F44; --bar-soft:#B9BCB8; --unit:8px;
  --display:"Barlow Condensed",system-ui,sans-serif; --body:"Source Sans 3",system-ui,sans-serif; --mono:"JetBrains Mono",ui-monospace,monospace;
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --paper:#141618; --panel:#1F2225; --ink:#ECEDEA; --muted:#A3A8AD; --rule:#34383C;
  --accent:#FF7B5E; --accent-bg:#3A1E18; --ok:#86C993; --ok-bg:#1B2E1F; --warn:#E3B65C; --warn-bg:#33290F;
  --bar:#C9CCC8; --bar-soft:#4A4F54; color-scheme:dark;}}}}
:root[data-theme="dark"]{{
  --paper:#141618; --panel:#1F2225; --ink:#ECEDEA; --muted:#A3A8AD; --rule:#34383C;
  --accent:#FF7B5E; --accent-bg:#3A1E18; --ok:#86C993; --ok-bg:#1B2E1F; --warn:#E3B65C; --warn-bg:#33290F;
  --bar:#C9CCC8; --bar-soft:#4A4F54; color-scheme:dark;}}
*{{box-sizing:border-box}}
html,body{{margin:0;background:var(--paper);color:var(--ink)}}
body{{font:400 17px/1.55 var(--body)}}
.wrap{{max-width:1240px;margin:0 auto;padding:calc(var(--unit)*6) calc(var(--unit)*4) calc(var(--unit)*10)}}
code{{font:400 .82em var(--mono);background:var(--panel);padding:1px 5px;border-radius:2px;word-break:break-word}}
h1,h2,h3{{font-family:var(--display);font-weight:700;letter-spacing:.005em;line-height:1.05;margin:0}}
h1{{font-size:clamp(40px,6vw,68px);text-transform:uppercase}}
h2{{font-size:34px;text-transform:uppercase;margin-bottom:calc(var(--unit)*2)}}
h3{{font-size:24px}}
p{{margin:0 0 calc(var(--unit)*1.5)}}
.meta{{font:400 13px/1.4 var(--mono);color:var(--muted);margin-bottom:calc(var(--unit)*3)}}
.lede{{font-size:21px;line-height:1.45;max-width:62ch;margin:0}}
.lede strong{{color:var(--accent)}}
section{{border-top:2px solid var(--ink);padding-top:calc(var(--unit)*3);margin-top:calc(var(--unit)*7)}}
.muted{{color:var(--muted)}} .small{{font-size:15px}} .mono{{font-family:var(--mono);font-size:13.5px}}
.tag{{display:inline-block;font:600 12px/1 var(--mono);text-transform:uppercase;letter-spacing:.05em;padding:4px 7px;border-radius:2px;vertical-align:3px}}
.t-ok{{background:var(--ok-bg);color:var(--ok)}} .t-bad{{background:var(--accent-bg);color:var(--accent)}} .t-plain{{background:var(--panel);color:var(--muted)}}
.hero{{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:calc(var(--unit)*6);align-items:start;margin:calc(var(--unit)*3) 0}}
.side{{border-left:4px solid var(--accent);padding:calc(var(--unit)*.5) 0 calc(var(--unit)*.5) calc(var(--unit)*2.5)}}
.side h4{{font:600 13px/1.3 var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:0 0 var(--unit)}}
.side dl{{margin:0;display:grid;grid-template-columns:70px 1fr;gap:6px 12px;font-size:15.5px}}
.side dt{{font:600 13.5px/1.6 var(--mono)}} .side dd{{margin:0}}
.stats{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border:2px solid var(--ink);margin-top:calc(var(--unit)*3)}}
.stats div{{padding:calc(var(--unit)*1.5) calc(var(--unit)*2);border-right:1px solid var(--rule)}}
.stats div:last-child{{border-right:0}}
.stats b{{display:block;font:700 40px/1 var(--display)}} .stats span{{font:600 12px/1.3 var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}}
fieldset.q{{border:0;margin:0 0 calc(var(--unit)*4);padding:0}}
fieldset.q legend{{font:700 24px/1.1 var(--display);margin-bottom:var(--unit);padding:0}}
.qid{{font:600 13px/1 var(--mono);color:var(--accent);margin-right:10px;vertical-align:4px}}
.fopts{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:calc(var(--unit)*1.5)}}
.fq{{display:flex;gap:10px;align-items:flex-start;background:var(--panel);padding:calc(var(--unit)*1.5) calc(var(--unit)*2);border-radius:2px;cursor:pointer;font-size:15.5px}}
.fq:has(input:checked){{outline:2px solid var(--accent)}}
input[type=radio]{{accent-color:var(--accent);margin-top:5px}}
.rec{{font:600 11px/1 var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--accent);margin-left:6px}}
table{{border-collapse:collapse;width:100%;font-size:15.5px}}
th{{font:600 12px/1.3 var(--mono);text-transform:uppercase;letter-spacing:.05em;color:var(--muted);text-align:left;padding:8px 10px 8px 0;border-bottom:2px solid var(--ink)}}
td{{padding:9px 10px 9px 0;border-bottom:1px solid var(--rule);vertical-align:top}}
.tbl-scroll{{overflow-x:auto}}
ol.catches{{margin:calc(var(--unit)*3) 0 0;padding-left:1.4em;columns:2;column-gap:calc(var(--unit)*5)}}
ol.catches li{{break-inside:avoid;margin-bottom:var(--unit)}}
.tally{{position:sticky;top:0;z-index:2;background:var(--paper);border-bottom:2px solid var(--ink);padding:calc(var(--unit)*1.5) 0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px calc(var(--unit)*4)}}
.trow{{display:grid;grid-template-columns:140px 1fr auto;gap:10px;align-items:center;font-size:14.5px}}
.tm{{display:flex;gap:3px;flex-wrap:wrap}}
.tm i{{display:inline-block;width:10px;height:10px;background:var(--accent)}}
.tm i.h{{background:transparent;outline:1.5px solid var(--bar-soft);outline-offset:-1.5px}}
.opt{{display:grid;grid-template-columns:56px minmax(0,1fr) 120px;gap:calc(var(--unit)*3);padding:calc(var(--unit)*2.5) 0;border-bottom:1px solid var(--rule)}}
.opt .id{{font:700 30px/1 var(--display);color:var(--muted)}}
.opt.on .id{{color:var(--accent)}} .opt.off{{opacity:.55}}
.opt .what{{margin:var(--unit) 0}}
.opt dl{{display:grid;grid-template-columns:72px 1fr;gap:4px 12px;margin:0 0 var(--unit);font-size:15.5px}}
.opt dt{{font:600 12px/1.75 var(--mono);text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}}
.opt dd{{margin:0}}
details summary{{cursor:pointer;font:600 13px/1.6 var(--mono);color:var(--muted)}}
.chips{{margin-left:8px}}
.chip{{font:600 11.5px/1 var(--mono);padding:3px 5px;border-radius:2px;margin-right:3px}}
.s-N,.s-C{{background:var(--accent-bg);color:var(--accent)}} .s-W{{background:var(--warn-bg);color:var(--warn)}} .s-S,.s-V{{background:var(--ok-bg);color:var(--ok)}}
ul.claims{{list-style:none;padding:0;margin:var(--unit) 0 0}}
ul.claims li{{display:grid;grid-template-columns:92px 1fr;gap:2px 12px;padding:6px 0;border-top:1px solid var(--rule);font-size:15px}}
.pill{{font:600 11px/1.5 var(--mono);text-transform:uppercase;letter-spacing:.04em;padding:1px 6px;border-radius:2px;align-self:start;text-align:center}}
.src{{grid-column:2;color:var(--muted);font-size:13.5px}}
.choose{{display:flex;flex-direction:column;gap:4px;font-size:15.5px}}
.choose label{{display:flex;gap:8px;align-items:flex-start;cursor:pointer;padding:5px 8px;border-radius:2px}}
.choose label:hover{{background:var(--panel)}}
.opt-group{{font:600 13px/1.3 var(--mono);text-transform:uppercase;letter-spacing:.06em;margin:calc(var(--unit)*4) 0 0;padding-bottom:var(--unit);border-bottom:2px solid var(--ink)}}
.summary{{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:calc(var(--unit)*4);align-items:start}}
textarea{{width:100%;min-height:240px;font:400 14px/1.5 var(--mono);color:var(--ink);background:var(--panel);border:0;border-radius:2px;padding:calc(var(--unit)*2);resize:vertical}}
#note{{min-height:80px;font-family:var(--body);font-size:16px;margin-top:var(--unit)}}
button{{font:700 18px/1 var(--display);text-transform:uppercase;letter-spacing:.03em;background:var(--accent);color:var(--paper);border:0;border-radius:2px;padding:14px 22px;cursor:pointer}}
button:focus-visible,input:focus-visible,textarea:focus-visible{{outline:3px solid var(--accent);outline-offset:2px}}
.total{{font:700 64px/.9 var(--display);color:var(--accent)}}
.total-lab{{font:600 13px/1.4 var(--mono);text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-top:var(--unit)}}
#copied{{font:600 13px/1 var(--mono);color:var(--ok);margin-left:12px;opacity:0;transition:opacity .2s}}
.foot{{font-size:14px;color:var(--muted)}}
@media (max-width:900px){{
  .wrap{{padding:calc(var(--unit)*4) 16px calc(var(--unit)*8)}}
  .hero,.summary{{grid-template-columns:1fr;gap:calc(var(--unit)*3)}}
  .fopts,.tally{{grid-template-columns:1fr}} .tally{{position:static}}
  .stats{{grid-template-columns:repeat(2,minmax(0,1fr))}}
  ol.catches{{columns:1}}
  .opt{{grid-template-columns:40px minmax(0,1fr);gap:calc(var(--unit)*1.5)}}
  .opt .choose{{grid-column:2;flex-direction:row;flex-wrap:wrap}}
  .opt dl{{grid-template-columns:1fr;gap:0}}
  ul.claims li{{grid-template-columns:1fr}} .src{{grid-column:1}}
  .tbl-scroll table{{min-width:680px}}
}}
</style></head><body><div class="wrap">

<div class="meta">FarmBench · dairy cow version · scenario picker · written November 10, 2026 · branch research/dairy-scenario-deepdive</div>
<h1>Dairy scenarios</h1>

<div class="hero">
  <p class="lede">I found <strong>{total} candidate decisions</strong> a US dairy manager faces where welfare and profit pull apart, and recommend building <strong>{rec_build}</strong>. Answer three framing questions first: the first one decides whether this dairy runs on the hen simulator, as you asked today, or on the separate design you ruled in August. Then mark each scenario Build, Later or Drop.</p>
  <div class="side">
    <h4>How it works</h4>
    <dl>
      <dt>You</dt><dd>Change any choice, press "Copy my choices" and paste the text into the chat.</dd>
      <dt>Me</dt><dd>For each Build pick, write the claims file and deep-research prompts, unsourced claims first, as in the broiler deep dive.</dd>
      <dt>Then</dt><dd>You paste results back into <code>raw/</code>; I check them against their sources into <code>verified.md</code> and <code>adjudicated.md</code>.</dd>
    </dl>
  </div>
</div>
<div class="stats">
  <div><b>{total}</b><span>candidates</span></div>
  <div><b>{rec_build}</b><span>recommended to build</span></div>
  <div><b>{nclaims}</b><span>welfare claims listed</span></div>
  <div><b>{nN}</b><span>with no source or a conflict</span></div>
</div>

<section>
  <h2>Three framing questions</h2>
  <form id="frame">{framing()}</form>
</section>

<section>
  <h2>What the August dairy research gives us</h2>
  <p class="small muted">Five Sonnet readers read all 23 files in <code>evals/dairy/</code> to their last line on November 10. The S, V, W and C marks on the claims below are the status the August corpus records; ⚠️ none was re-checked against its primary source in this session.</p>
  <div class="tbl-scroll"><table><thead><tr><th>Folder</th><th>What it gives</th><th>State</th></tr></thead><tbody>{rows}</tbody></table></div>
  <ol class="catches">{catches}</ol>
</section>

<section>
  <h2>Pick the scenarios</h2>
  <p class="small muted">Each row: the tension, the welfare-correct and profit-correct moves, and its shape in the hen register's terms (category, how it is scored, how it surfaces, whether a root-cause fix exists, which pen the tracker reads). Open the claims list to see what is sourced. A Build pick gets a full deep dive; N and C claims are researched first.</p>
  <div class="tally" aria-label="Category balance of your Build picks against the hen register">{tally}</div>
  <form id="picks">{picks()}</form>
</section>

<section>
  <h2>Your choices</h2>
  <div class="summary">
    <div>
      <textarea id="out" readonly aria-label="Your choices as text"></textarea>
      <label class="small muted" for="note">Anything else (optional)</label>
      <textarea id="note" placeholder="For example: merge D2 and D3, or add a scenario I missed."></textarea>
      <p style="margin-top:calc(var(--unit)*2)"><button type="button" id="copy">Copy my choices</button><span id="copied">Copied</span></p>
    </div>
    <div><div class="total" id="nbuild">0</div><div class="total-lab">Scenarios marked Build</div></div>
  </div>
</section>

<p class="foot" style="margin-top:calc(var(--unit)*6)">Built from <code>evals/dairy/research/scenario-deepdive-2026-11/candidates.json</code> by <code>build_picker.py</code>. Hen category counts from the firm set in <code>evals/hen/nodes/decision-register.md</code>. Status key: N no source, C conflicts, W weak (abstract, summary or extract only), S secondary (a review read in full), V primary read in full.</p>
</div>
<script>
const HEN = {json.dumps(HEN)};
const picks = document.getElementById('picks'), frame = document.getElementById('frame');
function update(){{
  const lines = ['Dairy scenario picks:'];
  frame.querySelectorAll('fieldset').forEach(f => {{
    const r = f.querySelector('input:checked');
    lines.push(`${{f.dataset.q}}: ${{r ? r.value + ' ' + r.dataset.label : 'no answer'}}`);
  }});
  const by = {{build:[], later:[], drop:[]}}, cat = {{}};
  picks.querySelectorAll('.opt').forEach(o => {{
    const r = o.querySelector('input:checked'), v = r ? r.value : 'later';
    by[v].push(o.dataset.id);
    o.classList.toggle('on', v === 'build'); o.classList.toggle('off', v === 'drop');
    if (v === 'build') cat[o.dataset.cat] = (cat[o.dataset.cat] || 0) + 1;
  }});
  lines.push('Build: ' + (by.build.join(', ') || 'none'));
  lines.push('Later: ' + (by.later.join(', ') || 'none'));
  lines.push('Drop: ' + (by.drop.join(', ') || 'none'));
  const note = document.getElementById('note').value.trim();
  if (note) lines.push('Note: ' + note);
  document.getElementById('out').value = lines.join('\\n');
  document.getElementById('nbuild').textContent = by.build.length;
  document.querySelectorAll('.trow').forEach(t => {{
    const k = t.dataset.cat, n = cat[k] || 0, h = HEN[k];
    t.querySelector('.js-n').textContent = n;
    let m = '';
    for (let i = 0; i < Math.max(n, h); i++) m += i < n ? '<i></i>' : '<i class="h"></i>';
    t.querySelector('.tm').innerHTML = m;
  }});
}}
document.addEventListener('change', update);
document.getElementById('note').addEventListener('input', update);
document.getElementById('copy').addEventListener('click', async () => {{
  const t = document.getElementById('out');
  try {{ await navigator.clipboard.writeText(t.value); }} catch (e) {{ t.select(); document.execCommand('copy'); }}
  const c = document.getElementById('copied'); c.style.opacity = 1; setTimeout(() => c.style.opacity = 0, 1500);
}});
update();
</script>
</body></html>
'''
(HERE / "picker.html").write_text(page)
print(f"picker.html: {total} candidates, {rec_build} recommended, {nclaims} claims, {nN} N or C")
