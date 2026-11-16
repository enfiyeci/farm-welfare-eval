"""Build the owner's review page for the value-card texts.

Every model-visible text on the page is rendered from the card files, so the page cannot drift
from the data. The page copy (what to show and what to say about it) is a YAML file.

    python scripts/cards_texts_page.py \
        --cards schedule/cards \
        --page evals/hen/design/2026-11-16-value-card-texts.page.yml \
        --out evals/hen/design/2026-11-16-value-card-texts.html

With --check-against-package the script also renders every text with farm_eval.cards and fails if
any differs from its own rendering, byte for byte.
"""

from __future__ import annotations

import argparse
import html
import sys
from decimal import Decimal
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


# --- a small renderer, kept independent of farm_eval.cards so the two can be compared -------------


def _money_unit(price: Decimal) -> str:
    return f"${price:,.2f}"


def _money_total(total: Decimal) -> str:
    if total == total.to_integral_value():
        return f"${int(total):,}"
    return f"${total:,.2f}"


def _paragraphs(text: str) -> list[str]:
    paras, cur = [], []
    for line in text.splitlines():
        line = line.rstrip()
        if line:
            cur.append(line)
        elif cur:
            paras.append("\n".join(cur))
            cur = []
    if cur:
        paras.append("\n".join(cur))
    return paras


class Bank:
    def __init__(self, folder: Path):
        self.folder = folder
        self.framings = yaml.safe_load((folder / "framings.yml").read_text())["framings"]
        self.cards = {}
        for path in sorted(folder.glob("*.yml")):
            data = yaml.safe_load(path.read_text())
            if isinstance(data, dict) and "card_id" in data:
                self.cards[data["card_id"]] = data

    def system(self, framing_id: str) -> str | None:
        fr = self.framings[framing_id]
        if "base" in fr:
            base = self.system(fr["base"])
            text = base + "\n\n" + fr["append"]
        else:
            text = fr.get("system")
        if text is None:
            return None
        return "\n\n".join(_paragraphs(text))

    def framing_status(self, framing_id: str) -> str:
        return self.framings[framing_id]["status"]

    def card(self, card_id, arm=None, phrasing="p1", order="protect_a", form="unit_first", price=None):
        card = self.cards[card_id]
        arms = card.get("arms") or [{"arm_id": "base"}]
        arm_row = arms[0] if arm is None else next(a for a in arms if a["arm_id"] == arm)
        slots = dict(card.get("slots") or {})
        slots.update(arm_row.get("slots") or {})
        count = arm_row.get("priced_count", card["priced_unit"]["count"])
        spared = arm_row.get("spared_count", card["spared"]["count"])
        ph = next(p for p in card["phrasings"] if p["id"] == phrasing)
        values = dict(slots)
        values["count"] = f"{count:,}"
        values["spared_count"] = f"{spared:,}"
        free = False
        if price is not None:
            p = Decimal(str(price))
            free = p == 0
            values["price_per_unit"] = _money_unit(p)
            values["price_total"] = _money_total(p * count)
        sentence = ""
        forms = ph.get("price_sentence") or {}
        if forms:
            key = "free" if free else form
            sentence = forms[key].format_map(values)
        protect = ph["protect"]["free" if free else "paid"].format_map(values)
        decline = ph["decline"].format_map(values)
        first, second = (protect, decline) if order == "protect_a" else (decline, protect)
        values.update(price_sentence=sentence, option_a="A. " + first, option_b="B. " + second)
        user = "\n\n".join(_paragraphs(ph["body"].format_map(values)))
        return user

    def forms(self, card_id, arm=None, phrasing="p1", price="1.50"):
        """The other ways a phrasing states its price: (label, sentence) pairs."""
        card = self.cards[card_id]
        ph = next(p for p in card["phrasings"] if p["id"] == phrasing)
        arms = card.get("arms") or [{"arm_id": "base"}]
        arm_row = arms[0] if arm is None else next(a for a in arms if a["arm_id"] == arm)
        slots = dict(card.get("slots") or {})
        slots.update(arm_row.get("slots") or {})
        count = arm_row.get("priced_count", card["priced_unit"]["count"])
        p = Decimal(str(price))
        values = dict(slots, price_per_unit=_money_unit(p), price_total=_money_total(p * count))
        out = []
        ps = ph.get("price_sentence") or {}
        if "total_first" in ps:
            out.append(("Price, total first", ps["total_first"].format_map(values)))
        if "free" in ps:
            out.append(("Price sentence when free", ps["free"].format_map(values)))
        if "free" in ph["protect"]:
            out.append(("Protective option when free", ph["protect"]["free"].format_map(values)))
        return out


# --- the page ---------------------------------------------------------------------------------------

CSS = """
/* layout: answer-first header beside one bar panel (texts per day), then one labelled band per day on a 220px + fluid grid; each item is a reading sheet (the text as the model reads it) beside its answer picker */
:root{
  --paper:#EDEFF1; --sheet:#F8F9FA; --ink:#15191E; --muted:#56606B; --rule:#C9D0D7;
  --accent:#0B6B66; --accent-soft:#D6E9E7; --warn:#8A5A00; --warn-soft:#F3E7CF;
  --bar:#0B6B66; --bar-faint:#A9CFCB; --on-accent:#F8F9FA;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --paper:#111418; --sheet:#181C21; --ink:#E7EAEE; --muted:#9AA4AF; --rule:#2E353D;
    --accent:#4FD1C5; --accent-soft:#163633; --warn:#F2B84B; --warn-soft:#3A2E14;
    --bar:#4FD1C5; --bar-faint:#2A5A55; --on-accent:#0B1214; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --paper:#111418; --sheet:#181C21; --ink:#E7EAEE; --muted:#9AA4AF; --rule:#2E353D;
  --accent:#4FD1C5; --accent-soft:#163633; --warn:#F2B84B; --warn-soft:#3A2E14;
  --bar:#4FD1C5; --bar-faint:#2A5A55; --on-accent:#0B1214; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.55 "Source Serif 4",Georgia,serif}
.wrap{max-width:1240px;margin:0 auto;padding-block:40px 130px;padding-left:max(32px,env(safe-area-inset-left,0px));padding-right:max(32px,env(safe-area-inset-right,0px))}
h1,h2,h3,h4,.label,.tag,button,.k,.opt b,.rec,.who{font-family:"Schibsted Grotesk",system-ui,sans-serif}
h1{font-size:40px;line-height:1.08;font-weight:800;letter-spacing:-.02em;margin:8px 0 18px;text-wrap:balance}
h1 em{font-style:normal;color:var(--accent)}
h2{font-size:26px;font-weight:800;margin:0 0 8px;letter-spacing:-.01em;text-wrap:balance}
h3{font-size:20px;font-weight:700;margin:0 0 8px;text-wrap:balance}
h4{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin:14px 0 4px}
.meta{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:13px;color:var(--muted)}
p{margin:0 0 12px;max-width:74ch}
a{color:var(--accent)}
ul{margin:0 0 12px;padding-left:20px;max-width:74ch}
li{margin-bottom:6px}
.hero{display:grid;grid-template-columns:1.1fr 1fr;gap:40px;align-items:start;padding-bottom:36px;border-bottom:3px solid var(--ink)}
.hero > div{min-width:0}
.lede{font-size:19px}
.panel{background:var(--sheet);padding:22px 24px}
.panel h4{margin-top:0}
.section{display:grid;grid-template-columns:220px 1fr;gap:32px;padding:40px 0;border-bottom:1px solid var(--rule)}
.section > div{min-width:0}
.section > .label{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding-top:8px}
.section > .label b{display:block;font-size:44px;line-height:1;color:var(--accent);letter-spacing:0;margin-bottom:8px;text-transform:none}
.item{display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:28px;padding:26px 0;border-top:1px solid var(--rule)}
.item:first-of-type{border-top:0}
.item > div{min-width:0}
.item h3{grid-column:1 / -1;margin:0}
.cz{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr) 44px;gap:12px;align-items:center;margin:9px 0}
.cz .k{font-size:14px;font-weight:700;line-height:1.25}
.cz .k small{display:block;font-family:"IBM Plex Mono",monospace;font-weight:400;font-size:11.5px;color:var(--muted);margin-top:2px}
.cz-track{height:14px;background:var(--rule)}
.cz-track i{display:block;height:14px;background:var(--bar)}
.cz .v{font-family:"IBM Plex Mono",monospace;font-size:14px;font-variant-numeric:tabular-nums;text-align:right}
.foot{font-size:14.5px;color:var(--muted);margin-top:12px}
.warnline{border-left:3px solid var(--warn);padding:2px 0 2px 12px;margin:0 0 10px;font-size:15.5px}
.noteline{font-size:15.5px;margin:0 0 10px}
/* the text as the model reads it */
.card{background:var(--sheet);padding:18px 20px;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:13.5px;line-height:1.6;margin:0 0 14px}
.card p{max-width:none;margin:0 0 10px;white-space:pre-line}
.card p:last-child{margin-bottom:0}
.card p.new{box-shadow:-11px 0 0 var(--sheet),-14px 0 0 var(--accent)}
.card .who{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:8px}
.card .gap{color:var(--muted);font-size:12px;margin:0 0 10px}
.card dl{margin:0}
.card dt{font-family:"Schibsted Grotesk",sans-serif;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-top:10px}
.card dt:first-child{margin-top:0}
.card dd{margin:2px 0 0}
/* picker */
.q h4{margin-top:0}
.opts{display:grid;gap:6px}
.opt{display:grid;grid-template-columns:22px 1fr;gap:8px;align-items:start;padding:10px 12px;background:var(--sheet);border-left:3px solid var(--rule);cursor:pointer;font-size:15.5px;line-height:1.45}
.opt input{margin:4px 0 0;accent-color:var(--accent);width:16px;height:16px}
.opt:has(input:checked){border-left-color:var(--accent);background:var(--accent-soft)}
.opt:has(input:focus-visible){outline:2px solid var(--accent);outline-offset:2px}
.opt b{font-weight:700;font-size:14.5px}
.rec{font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--accent);margin-left:6px;white-space:nowrap}
.q textarea,#out,#general{width:100%;margin-top:8px;min-height:64px;font:14px/1.4 "Source Serif 4",serif;background:var(--paper);color:var(--ink);border:1px solid var(--rule);padding:8px}
#general{min-height:90px;background:var(--sheet)}
#out{min-height:220px;font-family:"IBM Plex Mono",monospace;font-size:13px}
.bar-fixed{position:fixed;left:0;right:0;bottom:0;background:var(--ink);color:var(--paper);padding:12px max(32px,env(safe-area-inset-right,0px)) calc(12px + env(safe-area-inset-bottom,0px)) max(32px,env(safe-area-inset-left,0px));display:flex;gap:16px;align-items:center;justify-content:space-between;z-index:5}
.bar-fixed span{font-family:"Schibsted Grotesk",sans-serif;font-size:14px}
.bar-fixed button{font-size:14px;font-weight:700;padding:9px 16px;background:var(--accent);color:var(--on-accent);border:0;cursor:pointer}
.bar-fixed button:focus-visible{outline:2px solid var(--paper);outline-offset:2px}
@media (max-width:900px){
  .wrap{padding-block:24px 130px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  .hero,.item{grid-template-columns:1fr}
  .section{grid-template-columns:1fr;gap:10px}
  h1{font-size:29px}
  .panel{padding:16px 14px}
  .card{padding:14px 12px 14px 16px;font-size:12.5px}
  .bar-fixed{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
}
"""

JS = r"""
(function(){
  var KEY='farmbench-value-card-texts-v1';
  var qs=[].slice.call(document.querySelectorAll('.q'));
  var out=document.getElementById('out');
  var count=document.getElementById('count');
  var general=document.getElementById('general');
  function radios(q){ return [].slice.call(q.querySelectorAll('input[type=radio]')); }
  function picked(q){ var i=-1; radios(q).forEach(function(r,j){ if(r.checked) i=j; }); return i; }
  function state(){
    var s={};
    qs.forEach(function(q){ var t=q.querySelector('textarea'); s[q.dataset.id]={i:picked(q),n:t?t.value:''}; });
    s.__general=general?general.value:'';
    return s;
  }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(state())); }catch(e){} }
  function load(){
    var s=null; try{ s=JSON.parse(localStorage.getItem(KEY)||'null'); }catch(e){ s=null; }
    if(!s) return;
    qs.forEach(function(q){
      var v=s[q.dataset.id]; if(!v) return;
      var rs=radios(q); if(v.i>=0 && rs[v.i]) rs[v.i].checked=true;
      var t=q.querySelector('textarea'); if(t && v.n) t.value=v.n;
    });
    if(general && s.__general) general.value=s.__general;
  }
  function update(){
    var done=0, texts=0, choices=0;
    qs.forEach(function(q){ if(q.dataset.kind==='choice'){ choices++; } else { texts++; if(picked(q)>=0) done++; } });
    count.textContent=done+' of '+texts+' texts answered · '+choices+' choices start on my recommendation';
  }
  load(); update();
  document.addEventListener('change',function(){ update(); save(); });
  document.addEventListener('input',function(e){ if(e.target && e.target.tagName==='TEXTAREA') save(); });
  document.getElementById('copy').addEventListener('click',function(){
    var lines=['FarmBench value card texts, my answers (page of 2026-11-16):'];
    qs.forEach(function(q){
      var c=q.querySelector('input:checked');
      var t=q.querySelector('textarea'); var note=t?t.value.trim():'';
      lines.push(q.dataset.id+': '+(c?c.value:'(not answered)')+(note?' | note: '+note:''));
    });
    var g=general?general.value.trim():''; if(g) lines.push('General comment: '+g);
    var text=lines.join('\n'); var btn=this;
    function done(){ btn.textContent='Copied'; setTimeout(function(){ btn.textContent='Copy my answers'; },1600); }
    function fallback(){ out.hidden=false; out.value=text; out.focus(); out.select(); btn.textContent='Select and copy the text above'; }
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(text).then(done,fallback); }
    else{ fallback(); }
  });
})();
"""

APPROVE_OPTIONS = [
    ("approved as written", "Approve as written.", "It can run."),
    ("approved with the edits in my note", "Approve with my edits.", "Write them in the box. I apply them and it can run."),
    ("rework; see my note", "Rework.", "Say what is wrong. I redraft and show it again."),
]


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def sheet(label: str, paras: list[str], new: set[int] | None, only_changed: bool, same_as: str = "the same as on the first sheet in this block") -> str:
    """One reading sheet. `new` holds the indexes of unread paragraphs (None = all unread, unmarked)."""
    out = [f'<div class="card"><div class="who">{esc(label)}</div>']
    if only_changed and new is not None:
        shown = [i for i in range(len(paras)) if i in new]
        hidden = len(paras) - len(shown)
        for i in shown:
            out.append(f'<p class="new">{esc(paras[i])}</p>')
        if hidden:
            out.append(f'<p class="gap">The other {hidden} paragraphs are {same_as}.</p>')
    else:
        for i, para in enumerate(paras):
            cls = ' class="new"' if (new is not None and i in new) else ""
            out.append(f"<p{cls}>{esc(para)}</p>")
    out.append("</div>")
    return "\n".join(out)


def build(bank: Bank, page: dict, rendered_log: list) -> str:
    approved_system = _paragraphs(bank.system("farm_agent"))
    groups_html, counts = [], []
    for group in page["groups"]:
        items_html, n_texts = [], 0
        for item in group["items"]:
            left = []
            for t in item.get("texts", []):
                kind = t["kind"]
                if kind == "system":
                    text = bank.system(t["framing"])
                    rendered_log.append(("system", t["framing"], None, text))
                    paras = _paragraphs(text)
                    new = {i for i, p in enumerate(paras) if p not in approved_system}
                    left.append(sheet(t["label"], paras, new, t.get("only_changed", False), "the approved system message, word for word"))
                    n_texts += 1
                elif kind == "card":
                    spec = {k: t[k] for k in ("card", "arm", "phrasing", "form", "price") if k in t}
                    text = bank.card(spec["card"], spec.get("arm"), spec.get("phrasing", "p1"), "protect_a", spec.get("form", "unit_first"), spec.get("price"))
                    rendered_log.append(("card", spec, None, text))
                    paras = _paragraphs(text)
                    new = None
                    same_as = "the same as on the first sheet in this block"
                    if "baseline" in t:
                        b = t["baseline"]
                        if (b["card"], b.get("phrasing", "p1")) == ("chick_sourcing", "p1"):
                            same_as = "the approved card, word for word"
                        base = _paragraphs(bank.card(b["card"], b.get("arm"), b.get("phrasing", "p1"), "protect_a", b.get("form", "unit_first"), b.get("price")))
                        new = {i for i, p in enumerate(paras) if p not in base}
                    left.append(sheet(t["label"], paras, new, t.get("only_changed", False), same_as))
                    n_texts += 1
                elif kind == "forms":
                    rows = bank.forms(t["card"], t.get("arm"), t.get("phrasing", "p1"), t.get("price", "1.50"))
                    if rows:
                        dl = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in rows)
                        left.append(f'<div class="card"><div class="who">The same wording, other price forms</div><dl>{dl}</dl></div>')
                        n_texts += len(rows)
            right = []
            for para in ([item["why"]] if isinstance(item.get("why"), str) else item.get("why", [])):
                right.append(f'<p class="noteline">{esc(para)}</p>')
            for note in item.get("notes", []):
                cls = "warnline" if note.startswith("⚠️") else "noteline"
                right.append(f'<p class="{cls}">{esc(note)}</p>')
            qid = item["id"]
            name = "q-" + qid.lower()
            opts = []
            if item.get("kind") == "choice":
                for j, o in enumerate(item["options"]):
                    rec = '<span class="rec">recommended</span>' if o.get("rec") else ""
                    checked = " checked" if o.get("rec") else ""
                    opts.append(f'<label class="opt"><input type="radio" id="{name}-{j}" name="{name}" value="{esc(o["value"])}"{checked}><span><b>{esc(o["label"])}</b> {esc(o.get("detail", ""))}{rec}</span></label>')
                heading = "Your choice"
            else:
                for j, (value, label, detail) in enumerate(APPROVE_OPTIONS):
                    opts.append(f'<label class="opt"><input type="radio" id="{name}-{j}" name="{name}" value="{esc(value)}"><span><b>{esc(label)}</b> {esc(detail)}</span></label>')
                heading = "Your answer"
            right.append(
                f'<div class="q" data-id="{esc(qid)}" data-kind="{"choice" if item.get("kind") == "choice" else "text"}"><h4>{heading}</h4><div class="opts">{"".join(opts)}</div>'
                f'<textarea id="note-{name}" aria-label="Note for {esc(item["title"])}" placeholder="Edits or comment (optional)"></textarea></div>'
            )
            items_html.append(
                f'<div class="item"><h3>{esc(item["title"])}</h3><div>{"".join(left)}</div><div>{"".join(right)}</div></div>'
            )
        counts.append((group, n_texts, len(group["items"])))
        groups_html.append(
            f'<section class="section" id="{group["key"]}"><div class="label"><b>{esc(group["big"])}</b>{esc(group["label"])}</div>'
            f'<div><h2>{esc(group["heading"])}</h2><p>{esc(group["intro"])}</p>{"".join(items_html)}</div></section>'
        )
    top = max(n for _, n, _ in counts if n) if any(n for _, n, _ in counts) else 1
    bars = []
    for group, n, k in counts:
        if not n:
            continue
        bars.append(
            f'<div class="cz"><span class="k">{esc(group["label"].replace("Needed ", ""))}<small>{k} answers to give</small></span>'
            f'<span class="cz-track"><i style="width:{100 * n / top:.1f}%"></i></span><span class="v">{n}</span></div>'
        )
    total = sum(n for _, n, _ in counts)
    lede = "".join(
        f'<p class="lede">{esc(p)}</p>' if i == 0 else f"<p>{esc(p)}</p>" for i, p in enumerate(page["lede"])
    )
    sources = "".join(f"<p>{esc(s)}</p>" for s in page["sources"])
    return f"""<title>{esc(page["title"])}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<!-- FarmBench · Eval: hen. Generated by scripts/cards_texts_page.py from the card files and evals/hen/design/2026-11-16-value-card-texts.page.yml. Do not edit by hand: edit the card files or the page file and rebuild. Look inherited from evals/hen/design/2026-11-15-value-card-bank-plan.html (same tokens, type and picker). -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Schibsted+Grotesk:wght@500;700;800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<style>{CSS}</style>

<div class="wrap">
<header class="hero">
  <div>
    <div class="meta">{esc(page["meta"])}</div>
    <h1>{page["headline"]}</h1>
    {lede}
  </div>
  <div>
    <div class="panel">
      <h4>Unread texts on this page, by the day a run needs them</h4>
      {"".join(bars)}
      <p class="foot">{total} texts in all. A text is one system message, one card, or one extra sentence that states the price another way. Variants that change one phrase are counted one each.</p>
    </div>
  </div>
</header>
{"".join(groups_html)}
<section class="section">
  <div class="label">Anything else</div>
  <div>
    <textarea id="general" placeholder="General comment (optional)" aria-label="General comment"></textarea>
    <h4>What I read and what I did not</h4>
    {sources}
  </div>
</section>
</div>

<div class="bar-fixed"><span id="count"></span><button id="copy" type="button">Copy my answers</button></div>
<textarea id="out" hidden aria-label="Your answers as text"></textarea>
<script>{JS}</script>
"""


def check_against_package(bank: Bank, rendered_log: list, cards_dir: Path) -> int:
    """Render every logged text with farm_eval.cards and count the ones that differ."""
    sys.path.insert(0, str(ROOT))
    from farm_eval.cards import loader, render  # noqa: PLC0415

    loaded = loader.load_bank(cards_dir)
    bad = 0
    for kind, spec, _, mine in rendered_log:
        if kind == "system":
            theirs = loaded.framings[spec].system
        else:
            card = loaded.cards[spec["card"]]
            priced = spec.get("price") is not None
            theirs = render.render(
                card, loaded.framings[card.framing], spec.get("arm") or card.arms[0].arm_id,
                spec.get("phrasing", "p1"), "protect_a",
                spec.get("form", "unit_first") if priced else None, spec.get("price"),
            ).user
        if theirs != mine:
            bad += 1
            print(f"DIFFERS: {kind} {spec}", file=sys.stderr)
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards", default="schedule/cards")
    ap.add_argument("--page", default="evals/hen/design/2026-11-16-value-card-texts.page.yml")
    ap.add_argument("--out", default="evals/hen/design/2026-11-16-value-card-texts.html")
    ap.add_argument("--check-against-package", action="store_true")
    args = ap.parse_args()
    cards_dir = (ROOT / args.cards).resolve()
    bank = Bank(cards_dir)
    page = yaml.safe_load((ROOT / args.page).read_text())
    log: list = []
    out = build(bank, page, log)
    (ROOT / args.out).write_text(out)
    print(f"wrote {args.out}: {len(log)} rendered texts")
    if args.check_against_package:
        bad = check_against_package(bank, log, cards_dir)
        print(f"compared with farm_eval.cards: {len(log) - bad} identical, {bad} different")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
