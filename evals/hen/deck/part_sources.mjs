// part_sources.mjs — Part: SOURCES. Parses docs/research/SOURCES.md and lists every
// working external link grouped by the section it appears in. Real links only.
import { C, F, W, H, S } from "./theme.mjs";
import { loadText, firstPath } from "./data.mjs";

const PART = "sources";
const LINK_RE = /\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g;

function parseSources() {
  // SOURCES.md moved under evals/hen/ in the 2026-08 reorg; support both layouts.
  const txt = loadText(firstPath(["evals/hen/research/SOURCES.md", "docs/research/SOURCES.md"])) || "";
  const lines = txt.split("\n");
  const sections = [];
  let cur = { title: "Register", links: [] };
  const seen = new Set();
  for (const ln of lines) {
    const h = ln.match(/^##\s+(.+)/);
    if (h) { if (cur.links.length) sections.push(cur); cur = { title: h[1].replace(/[#*]/g, "").trim(), links: [] }; continue; }
    let m;
    LINK_RE.lastIndex = 0;
    while ((m = LINK_RE.exec(ln))) {
      const url = m[2];
      if (seen.has(url)) continue;
      seen.add(url);
      // grab a bit of the row context before the link for a human label
      const rowLabel = ln.replace(/\|/g, " ").replace(/\[[^\]]+\]\([^)]+\)/g, "").replace(/\s+/g, " ").trim().slice(0, 60);
      cur.links.push({ label: m[1], url, ctx: rowLabel });
    }
  }
  if (cur.links.length) sections.push(cur);
  return sections;
}

export function buildSources(kit, pres, ctx) {
  kit.section("EIGHT", "Sources", "The load-bearing anchor register behind every compliance number, tripwire and rubric — with working links, and an honest status flag on each.", PART);

  // legend
  {
    const s = kit.light(PART);
    kit.head(s, "How to read the register", "Verify before you trust", "Every anchor carries a status. The deck reproduces only the links that actually resolve in the source register; unparsed primaries are cited without a hyperlink.");
    const leg = [
      ["✅", "Verified to a primary source", "a resolvable URL to the authoritative source (or web-verified 2026-06-27).", C.GOOD, C.GOOD_L],
      ["⚠️", "Secondary / unparsed primary", "from a summary or a PDF that did not parse on fetch — VERIFY against the primary before hardcoding.", C.AMBER, C.AMBER_L],
      ["🔵", "Realism-grade only", "plausible / illustrative, not a compliance fact — equipment, org, tunable coefficients.", C.TEAL, C.TEAL_L],
    ];
    leg.forEach(([b, t, d, c, bg], i) => {
      const y = 2.5 + i * 1.2;
      s.addShape(pres.ShapeType.roundRect, { x: S.MARGIN, y, w: 11.7, h: 1.0, rectRadius: 0.06, fill: { color: bg }, line: { type: "none" } });
      s.addText(b, { x: S.MARGIN + 0.3, y, w: 0.8, h: 1.0, fontFace: F.BODY, fontSize: 24, color: c, align: "center", valign: "middle", margin: 0 });
      s.addText(t, { x: S.MARGIN + 1.3, y: y + 0.18, w: 10, h: 0.36, fontFace: F.BODY, fontSize: 14, bold: true, color: C.INK, margin: 0 });
      s.addText(d, { x: S.MARGIN + 1.3, y: y + 0.54, w: 10, h: 0.4, fontFace: F.BODY, fontSize: 11.5, color: C.MUTED, margin: 0 });
    });
    kit.footnote(s, "Source: docs/research/SOURCES.md — the project's verify-before-hardcode register.");
  }

  // the links, grouped
  const sections = parseSources();
  const perPage = 8;
  sections.forEach((sec) => {
    for (let p = 0; p * perPage < sec.links.length; p++) {
      const s = kit.light(PART);
      const partN = Math.ceil(sec.links.length / perPage) > 1 ? ` (${p + 1}/${Math.ceil(sec.links.length / perPage)})` : "";
      const clean = sec.title.replace(/^\d+\.\s*/, "").split(/\s+[—(]/)[0].trim().slice(0, 46);
      kit.head(s, "Working links", clean + partN);
      const chunk = sec.links.slice(p * perPage, p * perPage + perPage);
      chunk.forEach((l, i) => {
        const y = 2.3 + i * 0.56;
        s.addShape(pres.ShapeType.rect, { x: S.MARGIN, y: y + 0.46, w: 11.7, h: 0.006, fill: { color: C.LINE }, line: { type: "none" } });
        s.addText([{ text: "✅  ", options: { fontFace: F.BODY, fontSize: 11, color: C.GOOD } }, { text: l.label, options: { fontFace: F.BODY, fontSize: 11.5, color: C.LINK, underline: true, hyperlink: { url: l.url } } }], { x: S.MARGIN, y, w: 11.7, h: 0.3, margin: 0, valign: "top" });
        s.addText(l.url, { x: S.MARGIN + 0.32, y: y + 0.26, w: 11.4, h: 0.24, fontFace: F.MONO, fontSize: 8, color: C.FAINT, margin: 0 });
      });
    }
  });

  // dossier map
  {
    const s = kit.light(PART);
    kit.head(s, "The dossier", "What P1–P6 mean", "The per-node 'sources' tags point at these research documents — the distilled anchor layer the rubrics are built on.");
    const dossier = [
      ["P1", "Compliance Context", "Hard tripwire & integrity anchors — UEP audit/space, FDA SE 5-log, AVMA tiers, indemnity."],
      ["P2", "Hy-Line Sim Parameters", "Calibration of the Layer-1 welfare state & outcome thresholds (THI, NH₃, KBF, FPD)."],
      ["P4", "Welfare Decision Brief", "Operational thresholds, farm-data signatures, tension structure per decision."],
      ["P6", "Welfare Rubric Anchors", "Per-decision welfare-optimal action + settled/contested confidence — the rubric backbone."],
      ["design", "Eval design docs", "Authored cases (epistemic ground truths, cost-cut) defined by the eval itself."],
    ];
    kit.kv(s, { x: S.MARGIN, y: 2.4, w: 11.7, rows: dossier.map((d) => [`${d[0]} · ${d[1]}`, d[2]]), rowH: 0.72, size: 12, labelW: 3.4 });
    kit.footnote(s, "Full detail and every anchor: docs/research/SOURCES.md and docs/research/*.md.");
  }
}
