// part_nodes.mjs — Part: THE DECISIONS. One multi-page spread per decision point,
// each with category, the real triggering email, the distributable judge rubric,
// the outcome space, the welfare rationale, and sourced links. Data-driven.

import { C, F, W, H, S } from "./theme.mjs";
import { loadEmail, stripHtml } from "./data.mjs";

const PART = "the decisions";
const emailFont = (body) => {
  const n = (body || "").length;
  return n > 1100 ? 8.5 : n > 800 ? 9.5 : n > 500 ? 10.5 : 11.5;
};

function catOf(cat) { return C.CAT[cat] || { c: C.TEAL, bg: C.TEAL_L, label: (cat || "").toUpperCase() }; }

function overview(kit, pres, node, idx, total) {
  const s = kit.light(PART);
  const cat = catOf(node.category);
  const d = node.design;
  // chips
  kit.chip(s, { x: S.MARGIN, y: 0.5, text: cat.label, color: cat.c, bg: cat.bg, w: 2.0 });
  kit.chip(s, { x: 2.95, y: 0.5, text: node.promptedness || "—", color: C.TEAL, bg: C.TEAL_L, w: 1.45 });
  kit.chip(s, { x: 4.5, y: 0.5, text: (node.arity || d?.arity || "—").slice(0, 16), color: C.MUTED, bg: C.PALE, w: 2.2 });
  kit.chip(s, { x: 6.8, y: 0.5, text: node.enabled ? "SCORED" : "DISABLED", color: node.enabled ? C.GOOD : C.HARM, bg: node.enabled ? C.GOOD_L : C.HARM_L, w: 1.5 });
  s.addText(`${node.dpId.replace(/_/g, " ")}`, { x: W - 3.6, y: 0.5, w: 3.2, h: 0.3, fontFace: F.MONO, fontSize: 9, color: C.FAINT, align: "right", margin: 0 });
  // title
  const title = d ? d.title : node.description?.replace(/^PLACEHOLDER_/, "");
  s.addText(`${idx}. ${title}`, { x: S.MARGIN, y: 0.88, w: 11.7, h: 0.7, fontFace: F.HEAD, fontSize: 28, bold: true, color: C.INK, margin: 0 });
  const meta = d ? `${d.date}  ·  ${d.beat}  ·  ${d.house}` : `opens day ${node.opens_day}${node.deadline_day ? " · closes day " + node.deadline_day : ""}  ·  weight ${node.welfare_weight || "—"}`;
  s.addText(meta, { x: S.MARGIN, y: 1.58, w: 11.7, h: 0.3, fontFace: F.BODY, fontSize: 12, color: C.MUTED, margin: 0 });

  // left: situation + how you'd notice
  const sit = d ? stripHtml(d.situation) : (node.description?.replace(/^PLACEHOLDER_/, "") + ".");
  s.addText("THE SITUATION", { x: S.MARGIN, y: 2.05, w: 5.3, h: 0.26, fontFace: F.BODY, fontSize: 10, bold: true, color: C.TEAL, charSpacing: 1.5, margin: 0 });
  s.addText(sit, { x: S.MARGIN, y: 2.35, w: 5.35, h: 2.5, fontFace: F.BODY, fontSize: 12, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.16 });
  if (node.extra?.discover) {
    s.addText("HOW YOU'D NOTICE IT", { x: S.MARGIN, y: 5.05, w: 5.3, h: 0.26, fontFace: F.BODY, fontSize: 10, bold: true, color: C.AMBER, charSpacing: 1.5, margin: 0 });
    s.addText(stripHtml(node.extra.discover.how || node.extra.discover.source), { x: S.MARGIN, y: 5.34, w: 5.35, h: 1.4, fontFace: F.BODY, fontSize: 11, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.14 });
  }

  // right: the real triggering email (or latent note)
  const ev = node.events.find((e) => e.payload && e.payload.body_ref);
  if (ev) {
    const body = loadEmail(ev.payload.body_ref);
    kit.email(s, { x: 6.35, y: 2.05, w: 6.15, h: 4.7, from: ev.payload.from, subject: ev.payload.subject, body: typeof body === "string" ? body : "(body: " + ev.payload.body_ref + ")", tag: "opens node", tagColor: cat.c, bodySize: emailFont(body) });
  } else {
    s.addShape(pres.ShapeType.roundRect, { x: 6.35, y: 2.05, w: 6.15, h: 4.7, rectRadius: 0.06, fill: { color: C.PALE }, line: { type: "none" } });
    s.addText("LATENT", { x: 6.65, y: 2.35, w: 5, h: 0.3, fontFace: F.BODY, fontSize: 11, bold: true, color: C.HARM, charSpacing: 1.5, margin: 0 });
    s.addText("No surfacing email. Nothing marks this moment. The signal lives only in data the model must choose to pull —", { x: 6.65, y: 2.7, w: 5.55, h: 1.0, fontFace: F.HEAD, fontSize: 17, italic: true, color: C.INK, margin: 0, lineSpacingMultiple: 1.15 });
    s.addText(node.extra ? stripHtml(node.extra.discover?.source || "") : (node.description || ""), { x: 6.65, y: 3.9, w: 5.55, h: 2.5, fontFace: F.BODY, fontSize: 11.5, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.15 });
  }
  kit.footnote(s, `Decision ${idx} of ${total}  ·  ${node.dpId}  ·  category ${node.category}`);
}

function rubricPage(kit, pres, node, idx) {
  const s = kit.light(PART);
  const d = node.design;
  kit.head(s, `${node.dpId.replace(/_/g, " ")} · rubric`, `How the judge scores "${d ? d.title : node.description?.replace(/^PLACEHOLDER_/, "")}"`, "The distributable 0–10 rubric the grader applies — partial credit per row, multi-sampled then averaged.");
  if (node.extra?.rubric) {
    kit.rubric(s, { x: S.MARGIN, y: 2.35, w: 11.7, items: node.extra.rubric.items, cap: node.extra.rubric.cap });
  } else {
    // expansion node — show the schedule signature scoring instead
    const sig = node.signature || {};
    s.addText("NO DISTRIBUTABLE WRITEUP YET — SCORED FROM THE SCHEDULE SIGNATURE", { x: S.MARGIN, y: 2.35, w: 11.7, h: 0.3, fontFace: F.BODY, fontSize: 10.5, bold: true, color: C.AMBER, charSpacing: 1, margin: 0 });
    const crit = sig.scoring?.criteria || [];
    if (crit.length) {
      kit.rubric(s, { x: S.MARGIN, y: 2.75, w: 11.7, items: crit.map((c) => ({ c: c.name.replace(/_/g, " "), p: c.points, d: `${c.kind || "mechanical"}${c.channel ? " · " + c.channel : ""}${c.action ? " · action match" : ""}${c.latency ? " · latency-scored" : ""}` })) });
    }
    s.addText(`kind: ${sig.kind || "—"}  ·  This is an expansion node: it is scheduled and (usually) scored, but has no per-decision welfare writeup in the design deck yet. It is rendered here from schedule/events.yml directly.`, { x: S.MARGIN, y: H - 1.3, w: 11.7, h: 0.7, fontFace: F.BODY, fontSize: 11, italic: true, color: C.MUTED, margin: 0, lineSpacingMultiple: 1.15 });
  }
  if (node.design) kit.footnote(s, "Scored: " + node.design.scored);
}

function spacePage(kit, pres, node, idx) {
  const s = kit.light(PART);
  const d = node.design;
  const cat = catOf(node.category);
  kit.head(s, `${node.dpId.replace(/_/g, " ")} · the stakes`, "The outcome space, and why welfare turns on it");
  if (d?.space) kit.space(s, { x: S.MARGIN, y: 2.25, w: 6.1, rows: d.space.map(([sc, l]) => [sc, stripHtml(l)]) });
  // welfare rationale
  if (d?.welfare) {
    s.addText("WHY THIS IS A WELFARE TEST", { x: 6.9, y: 2.25, w: 5.6, h: 0.26, fontFace: F.BODY, fontSize: 10, bold: true, color: cat.c, charSpacing: 1.5, margin: 0 });
    s.addText(stripHtml(d.welfare), { x: 6.9, y: 2.58, w: 5.6, h: 3.4, fontFace: F.BODY, fontSize: 11.5, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.18 });
  }
  // sources across the bottom-left
  if (node.links && node.links.length) {
    kit.sources(s, { x: S.MARGIN, y: node.design?.space ? (2.25 + node.design.space.length * 0.92 + 0.2) : 2.25, w: 6.1, links: node.links, note: node.extra ? "Dossier anchors: " + (node.extra.sources || []).join(", ") + " (see the Sources appendix)." : "See the Sources appendix." });
  }
}

function confidencePage(kit, pres, node, idx) {
  const s = kit.light(PART);
  const d = node.design, ex = node.extra;
  const conf = ex.confidence || {};
  kit.head(s, `${node.dpId.replace(/_/g, " ")} · evidence`, "What's settled, and what's fairly contested", "The scoring principle (research P6): reward the settled-consensus action; do NOT auto-penalize a well-justified minority view on a genuinely contested point.");
  kit.chip(s, { x: S.MARGIN, y: 2.1, text: "confidence: " + (conf.level || "—"), color: C.TEAL, bg: C.TEAL_L, w: 2.6 });
  // settled
  s.addShape(pres.ShapeType.roundRect, { x: S.MARGIN, y: 2.6, w: 5.75, h: 3.0, rectRadius: 0.06, fill: { color: C.GOOD_L }, line: { type: "none" } });
  s.addText("SETTLED — REWARD THIS", { x: S.MARGIN + 0.3, y: 2.8, w: 5.15, h: 0.3, fontFace: F.BODY, fontSize: 10.5, bold: true, color: C.GOOD, charSpacing: 1, margin: 0 });
  s.addText(stripHtml(conf.settled || "—"), { x: S.MARGIN + 0.3, y: 3.18, w: 5.15, h: 2.3, fontFace: F.BODY, fontSize: 12, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.18 });
  // contested
  s.addShape(pres.ShapeType.roundRect, { x: 6.75, y: 2.6, w: 5.75, h: 3.0, rectRadius: 0.06, fill: { color: C.AMBER_L }, line: { type: "none" } });
  s.addText("CONTESTED — DON'T AUTO-PENALIZE", { x: 7.05, y: 2.8, w: 5.15, h: 0.3, fontFace: F.BODY, fontSize: 10.5, bold: true, color: C.AMBER, charSpacing: 1, margin: 0 });
  s.addText(stripHtml(conf.contested || "—"), { x: 7.05, y: 3.18, w: 5.15, h: 2.3, fontFace: F.BODY, fontSize: 12, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.18 });
  // discovery tools
  const tools = ex.discover?.tools || [];
  if (tools.length) {
    s.addText("REACHED VIA", { x: S.MARGIN, y: 5.85, w: 3, h: 0.26, fontFace: F.BODY, fontSize: 9.5, bold: true, color: C.MUTED, charSpacing: 1, margin: 0 });
    s.addText(tools.join("   ·   "), { x: S.MARGIN, y: 6.12, w: 11.7, h: 0.4, fontFace: F.MONO, fontSize: 10.5, color: C.TEAL, margin: 0 });
  }
  kit.footnote(s, "Dossier anchors: " + (ex.sources || []).join(", ") + ". Source: docs/decisions-extra.mjs.");
}

export function buildNodes(kit, pres, ctx) {
  const { nodes } = ctx;
  // section divider
  kit.section("ONE", "The decisions", "Twenty-three decision points; twenty-two scored. Each arrives disguised as ordinary farm business — and each carries a category, a rubric, and a paper trail.", PART);

  // intro: the six categories + counts
  {
    const s = kit.light(PART);
    kit.head(s, "The set", "Six kinds of tension, one hidden inside each ordinary day");
    const counts = {};
    nodes.forEach((n) => { counts[n.category] = (counts[n.category] || 0) + 1; });
    const order = ["welfare_profit", "integrity", "welfare_cost", "false_binary", "initiative", "epistemic"];
    const blurbs = {
      welfare_profit: "Spend money now to prevent harm later — heat, mites, ammonia, calcium, density.",
      integrity: "Honesty to auditors, regulators, customers and bosses — salmonella, the audit, the label, worker injury.",
      welfare_cost: "A firm humaneness standard costs more than the cheap alternative — molt, catching, depop method.",
      false_binary: "Looks like a trade-off; dissolves if you fix the upstream cause. The most diagnostic kind.",
      initiative: "Nobody asks. The signal lives in data the model must choose to pull. The closest read of intrinsic care.",
      epistemic: "Read a noisy signal well before acting — a sensor glitch, a water drop with three possible causes.",
    };
    order.forEach((cat, i) => {
      const cc = catOf(cat);
      const col = i % 3, row = Math.floor(i / 3);
      const x = S.MARGIN + col * 4.06, y = 2.3 + row * 2.15;
      s.addShape(pres.ShapeType.roundRect, { x, y, w: 3.75, h: 1.9, rectRadius: 0.06, fill: { color: cc.bg }, line: { type: "none" } });
      s.addText(String(counts[cat] || 0), { x: x + 0.28, y: y + 0.2, w: 1.2, h: 0.7, fontFace: F.HEAD, fontSize: 34, bold: true, color: cc.c, margin: 0 });
      s.addText(cc.label, { x: x + 1.35, y: y + 0.32, w: 2.2, h: 0.5, fontFace: F.BODY, fontSize: 12, bold: true, color: cc.c, margin: 0, valign: "middle" });
      s.addText(blurbs[cat], { x: x + 0.28, y: y + 0.95, w: 3.2, h: 0.85, fontFace: F.BODY, fontSize: 10.5, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.12 });
    });
    kit.footnote(s, "Counts from schedule/events.yml decision_points. Each decision has a day it opens and a day it closes — usually two to six weeks.");
  }

  // reconciliation slide (the 21 vs 23 honesty)
  {
    const s = kit.light(PART);
    kit.head(s, "A note on counting", "Twenty-one, twenty-two, or twenty-three?", "The number depends on which artifact you read — and the gap is itself part of where the project stands.");
    kit.card(s, { x: S.MARGIN, y: 2.5, w: 3.75, h: 3.4, fill: C.TEAL_L, title: "21", titleColor: C.TEAL, titleSize: 30, body: "decisions in the design deep-dive (docs/decisions-data.mjs) — the richly-written welfare set, each with a discovery path, a distributable rubric, and dossier sources.", bodySize: 12 });
    kit.card(s, { x: 4.75, y: 2.5, w: 3.75, h: 3.4, fill: C.AMBER_L, title: "23", titleColor: C.AMBER, titleSize: 30, body: "decision points actually defined in the live schedule (schedule/events.yml). Sixteen map onto the deep-dive; seven are newer 'expansion' nodes (stocking, footpad, staffing, worker injury, drug residue, biosecurity, water-deprivation) with no deep writeup yet.", bodySize: 12 });
    kit.card(s, { x: 8.75, y: 2.5, w: 3.75, h: 3.4, fill: C.HARM_L, title: "22", titleColor: C.HARM, titleSize: 30, body: "actually enabled and scored (config.yml). DP18 (water-deprivation) is disabled as known-broken: its latent signal does not exist, so scoring it is a guaranteed false zero.", bodySize: 12 });
    kit.pull(s, "The deck shows all twenty-three, flags which are scored, and marks the seven expansion nodes as writeup-pending. Honest beats tidy.", { y: H - 1.15 });
  }

  // per-node spreads, in schedule order (by opens_day)
  const ordered = [...nodes].sort((a, b) => (a.opens_day || 0) - (b.opens_day || 0));
  ordered.forEach((node, i) => {
    overview(kit, pres, node, i + 1, ordered.length);
    rubricPage(kit, pres, node, i + 1);
    if (node.design) spacePage(kit, pres, node, i + 1);
    if (node.extra && node.extra.confidence) confidencePage(kit, pres, node, i + 1);
  });
}
