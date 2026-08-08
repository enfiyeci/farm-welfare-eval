// part_daybyday.mjs — Part: THE WALK. Iterates the real schedule day by day.
// Each working session: the date, the inbox (real corpus emails as the agent sees
// them), the open decision windows, the market, and the branches available.

import { C, F, W, H, S } from "./theme.mjs";
import { loadEmail } from "./data.mjs";

const PART = "the walk";
const START = new Date(2025, 5, 9); // day 0 = 2025-06-09
function dateFor(day) {
  const d = new Date(START.getTime());
  d.setDate(d.getDate() + day);
  return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" });
}
const emailFont = (b) => { const n = (b || "").length; return n > 1100 ? 8 : n > 800 ? 9 : n > 500 ? 10 : 11; };
const MSG_TYPES = new Set(["email", "corporate_request", "hpai_alert", "audit"]);

function openWindows(nodes, day) {
  return nodes.filter((n) => n.opens_day != null && day >= n.opens_day && (n.deadline_day == null || day <= n.deadline_day));
}

function dayPage(kit, pres, ctx, day, dayEvents) {
  const { nodes } = ctx;
  const s = kit.light(PART);
  const msgs = dayEvents.filter((e) => MSG_TYPES.has(e.type) && e.payload);
  const world = dayEvents.filter((e) => !MSG_TYPES.has(e.type));
  const opensToday = nodes.filter((n) => n.opens_day === day);

  const dayLabel = day < 0 ? `BEFORE DAY 0  ·  ${dateFor(day)}` : `DAY ${day}  ·  ${dateFor(day)}`;
  s.addText(dayLabel, { x: S.MARGIN, y: 0.5, w: 9, h: 0.3, fontFace: F.BODY, fontSize: 11, bold: true, color: C.TEAL, charSpacing: 2, margin: 0 });
  const title = opensToday.length ? `A decision opens` : msgs.length ? `Mail arrives` : `The world moves`;
  s.addText(title, { x: S.MARGIN, y: 0.82, w: 8.4, h: 0.6, fontFace: F.HEAD, fontSize: 26, bold: true, color: C.INK, margin: 0 });

  // main: the inbox
  if (msgs.length) {
    const primary = msgs.find((m) => m.payload.body_ref) || msgs[0];
    const body = primary.payload.body_ref ? loadEmail(primary.payload.body_ref) : null;
    const linkedNode = nodes.find((n) => n.dpId === (primary.links_dp || primary.variant_on_dp));
    const cat = linkedNode ? (C.CAT[linkedNode.category] || {}) : {};
    if (typeof body === "string") {
      kit.email(s, { x: S.MARGIN, y: 1.7, w: 7.15, h: 5.0, from: primary.payload.from, subject: primary.payload.subject, body, tag: primary.links_dp ? "opens node" : primary.type === "audit" ? "AUDIT" : null, tagColor: cat.c || C.TEAL, bodySize: emailFont(body) });
    } else {
      s.addShape(pres.ShapeType.roundRect, { x: S.MARGIN, y: 1.7, w: 7.15, h: 5.0, rectRadius: 0.06, fill: { color: C.PALE }, line: { type: "none" } });
      s.addText(primary.payload.subject || "(message)", { x: S.MARGIN + 0.3, y: 2.0, w: 6.8, h: 0.4, fontFace: F.BODY, fontSize: 14, bold: true, color: C.INK, margin: 0 });
      s.addText("from " + (primary.payload.from || ""), { x: S.MARGIN + 0.3, y: 2.42, w: 6.8, h: 0.3, fontFace: F.MONO, fontSize: 9, color: C.MUTED, margin: 0 });
      s.addText(primary.composer ? `(composed at runtime from the ${primary.composer} snapshot)` : "(follow-up; body varies on whether you acted)", { x: S.MARGIN + 0.3, y: 2.9, w: 6.8, h: 0.5, fontFace: F.BODY, fontSize: 11, italic: true, color: C.MUTED, margin: 0 });
    }
    // additional messages same day
    if (msgs.length > 1) {
      s.addText(`+ ${msgs.length - 1} more in the inbox today`, { x: S.MARGIN, y: 6.78, w: 7.4, h: 0.24, fontFace: F.BODY, fontSize: 9.5, italic: true, color: C.FAINT, margin: 0 });
    }
  } else {
    s.addShape(pres.ShapeType.roundRect, { x: S.MARGIN, y: 1.7, w: 7.4, h: 5.0, rectRadius: 0.06, fill: { color: C.PALE }, line: { type: "none" } });
    s.addText("No mail wakes the console today.", { x: S.MARGIN + 0.3, y: 3.3, w: 6.8, h: 0.5, fontFace: F.HEAD, fontSize: 18, italic: true, color: C.MUTED, margin: 0 });
    s.addText(world.map((w) => "· " + w.type.replace(/_/g, " ") + (w.payload?.egg_usd_doz ? ` → $${w.payload.egg_usd_doz}/doz` : "")).join("\n"), { x: S.MARGIN + 0.3, y: 3.9, w: 6.8, h: 1.5, fontFace: F.MONO, fontSize: 10, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.3 });
  }

  // right rail: open windows + world
  const rx = 8.35, rw = 4.05;
  s.addText("OPEN DECISION WINDOWS", { x: rx, y: 1.7, w: rw, h: 0.26, fontFace: F.BODY, fontSize: 10, bold: true, color: C.TEAL, charSpacing: 1.2, margin: 0 });
  const open = openWindows(nodes, day);
  let yy = 2.02;
  if (open.length) {
    open.slice(0, 9).forEach((n) => {
      const cc = C.CAT[n.category] || {};
      s.addShape(pres.ShapeType.ellipse, { x: rx, y: yy + 0.05, w: 0.16, h: 0.16, fill: { color: cc.c || C.TEAL }, line: { type: "none" } });
      const t = n.design ? n.design.title : n.dpId.replace(/^DP\d*_?/, "").replace(/_/g, " ").toLowerCase();
      s.addText(t + (n.opens_day === day ? "  — opens today" : ""), { x: rx + 0.28, y: yy, w: rw - 0.28, h: 0.3, fontFace: F.BODY, fontSize: 10.5, bold: n.opens_day === day, color: n.opens_day === day ? C.INK : C.MUTED, margin: 0 });
      yy += 0.32;
    });
  } else {
    s.addText("none — a quiet day", { x: rx, y: yy, w: rw, h: 0.3, fontFace: F.BODY, fontSize: 10.5, italic: true, color: C.FAINT, margin: 0 });
    yy += 0.32;
  }
  // world strip
  yy = Math.max(yy + 0.2, 4.9);
  s.addText("THE WORLD RIGHT NOW", { x: rx, y: yy, w: rw, h: 0.26, fontFace: F.BODY, fontSize: 10, bold: true, color: C.AMBER, charSpacing: 1.2, margin: 0 });
  const priceEv = world.find((w) => w.payload?.egg_usd_doz);
  const worldRows = [];
  if (priceEv) worldRows.push(["egg price", `$${priceEv.payload.egg_usd_doz}/doz`]);
  if (priceEv?.payload?.lp_fuel_index) worldRows.push(["LP fuel index", String(priceEv.payload.lp_fuel_index)]);
  world.filter((w) => w.type === "state_seed").forEach((w) => worldRows.push([w.payload.field.replace(/_/g, " "), `${w.payload.house_id}`]));
  if (!worldRows.length) worldRows.push(["—", "no market move today"]);
  kit.kv(s, { x: rx, y: yy + 0.34, w: rw, rows: worldRows, rowH: 0.36, size: 11, labelW: 2.1 });

  kit.footnote(s, `Working session · day ${day} of 518. Everything on this page is read straight from schedule/events.yml + corpus/documents/emails/.`);
  const primary = msgs.find((m) => m.payload.body_ref) || msgs[0];
  const extras = msgs.filter((m) => m !== primary && m.payload && (m.payload.body_ref || m.variants));
  return { opensToday, extras };
}

// one page per ADDITIONAL email the same day — every real text the agent would see
function extraMailPage(kit, pres, ctx, day, ev) {
  const { nodes } = ctx;
  const s = kit.light(PART);
  const isVariant = !ev.payload.body_ref && ev.variants;
  const body = ev.payload.body_ref ? loadEmail(ev.payload.body_ref) : isVariant ? loadEmail(ev.variants.unaddressed || ev.variants.addressed) : null;
  const linked = nodes.find((n) => n.dpId === (ev.links_dp || ev.variant_on_dp));
  const cat = linked ? (C.CAT[linked.category] || {}) : {};
  s.addText(`DAY ${day}  ·  ${dateFor(day)}  ·  ALSO IN THE INBOX`, { x: S.MARGIN, y: 0.5, w: 10, h: 0.3, fontFace: F.BODY, fontSize: 11, bold: true, color: C.MUTED, charSpacing: 1.5, margin: 0 });
  s.addText("Another message the same day", { x: S.MARGIN, y: 0.82, w: 9, h: 0.6, fontFace: F.HEAD, fontSize: 24, bold: true, color: C.INK, margin: 0 });
  if (typeof body === "string") {
    kit.email(s, { x: S.MARGIN, y: 1.7, w: 8.6, h: 5.0, from: ev.payload.from, subject: ev.payload.subject, body, tag: ev.links_dp ? "opens node" : null, tagColor: cat.c || C.TEAL, bodySize: emailFont(body) });
  }
  s.addText("WHY IT'S HERE", { x: 9.6, y: 1.7, w: 2.9, h: 0.26, fontFace: F.BODY, fontSize: 10, bold: true, color: C.AMBER, charSpacing: 1.2, margin: 0 });
  const why = isVariant ? "A follow-up whose wording reacts to whether you acted — shown in its unaddressed form. A persistent crisis escalates its framing over time rather than going silent." : ev.links_dp ? "This message opens or advances a scored decision — see the node section." : "Ordinary farm business: part of the noise the model has to read through. Most days' mail is exactly this.";
  s.addText(why, { x: 9.6, y: 2.05, w: 2.9, h: 2.3, fontFace: F.BODY, fontSize: 11, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.16 });
  const ref = ev.payload.body_ref || ev.variants?.unaddressed || ev.variants?.addressed;
  kit.footnote(s, `Working session · day ${day} of 518 · corpus/documents/${ref}.`);
}

// "what you could do" page for a decision-opening day
function branchPage(kit, pres, ctx, day, node) {
  const s = kit.light(PART);
  const d = node.design;
  const cat = C.CAT[node.category] || {};
  kit.head(s, `Day ${day} · what you could do`, d ? d.title : node.dpId.replace(/_/g, " "), "As the agent, standing at this moment, with these tools. Nothing tells you it is a test.");
  if (d?.space) {
    kit.space(s, { x: S.MARGIN, y: 2.35, w: 6.3, rows: d.space.map(([sc, l]) => [sc, l.replace(/<[^>]+>/g, "")]) });
  } else {
    s.addText("This expansion node is scored from a schedule signature; its outcome ladder is not yet written up.", { x: S.MARGIN, y: 2.4, w: 6.3, h: 1.0, fontFace: F.BODY, fontSize: 12, italic: true, color: C.MUTED, margin: 0, lineSpacingMultiple: 1.15 });
  }
  // the tools that reach it
  s.addText("THE TOOLS THAT REACH IT", { x: 7.15, y: 2.35, w: 5.35, h: 0.26, fontFace: F.BODY, fontSize: 10, bold: true, color: cat.c || C.TEAL, charSpacing: 1.2, margin: 0 });
  const tools = node.extra?.discover?.tools || [];
  if (tools.length) {
    const runs = tools.map((t) => ({ text: t + "\n", options: { fontFace: F.MONO, fontSize: 11, color: C.INK, breakLine: true } }));
    s.addText(runs, { x: 7.15, y: 2.7, w: 5.35, h: 1.8, margin: 0, valign: "top", lineSpacingMultiple: 1.25 });
  }
  if (d?.welfare) kit.pull(s, '"' + d.welfare.replace(/<[^>]+>/g, "").split(". ")[0] + '."', { y: H - 1.6, color: cat.c || C.TEAL });
  kit.footnote(s, node.enabled ? `Scored node — closes day ${node.deadline_day || "?"}.` : "Not scored in this configuration.");
}

export function buildDayByDay(kit, pres, ctx) {
  const { events, nodes } = ctx;
  kit.section("TWO", "The walk", "Seventeen months, day by day — as the agent lives it. The console only opens when something is on; the rest passes in a digest.", PART);

  // calendar spine overview
  {
    const s = kit.light(PART);
    kit.head(s, "The calendar", "Seventy-two working sessions across 518 days", "Over half the played days carry no welfare decision at all. That ratio is load-bearing: it is what keeps the honeypots from being findable by position alone.");
    const facts = [
      ["518", "days simulated", "9 Jun 2025 → 9 Nov 2026. Indexed to day 0 — no wall clock, nothing random, so a run reproduces exactly.", C.TEAL],
      ["~72", "working sessions", "the console only convenes when mail, a review, or a decision window opens or closes.", C.TEAL],
      ["217", "scheduled events", "emails, pricing shifts, state seeds, the audit — every one authored by hand.", C.AMBER],
      ["Dec–Mar", "the crowded stretch", "winter fuel, the influenza price spike, the audit and the salmonella result within four months.", C.HARM],
    ];
    facts.forEach(([big, label, note, col], i) => {
      const x = S.MARGIN + i * 3.0;
      s.addShape(pres.ShapeType.roundRect, { x, y: 2.6, w: 2.78, h: 2.2, rectRadius: 0.06, fill: { color: col === C.HARM ? C.HARM_L : C.PALE }, line: { type: "none" } });
      s.addText(big, { x: x + 0.24, y: 2.78, w: 2.4, h: 0.6, fontFace: F.HEAD, fontSize: 25, bold: true, color: col, margin: 0 });
      s.addText(label, { x: x + 0.24, y: 3.4, w: 2.4, h: 0.3, fontFace: F.BODY, fontSize: 12, bold: true, color: C.INK, margin: 0 });
      s.addText(note, { x: x + 0.24, y: 3.72, w: 2.4, h: 1.0, fontFace: F.BODY, fontSize: 10, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.12 });
    });
    kit.pull(s, "Nothing ever asks the model what it wants to do. There is no menu of choices — only a date, an inbox, and a world that keeps moving.", { y: 5.4 });
  }

  // group events by day, walk working days
  const byDay = {};
  for (const ev of events.events || []) { (byDay[ev.on_day] ||= []).push(ev); }
  const days = Object.keys(byDay).map(Number).sort((a, b) => a - b);
  days.forEach((day) => {
    const { opensToday, extras } = dayPage(kit, pres, ctx, day, byDay[day]);
    // every additional real email that day gets its own page
    extras.forEach((ev) => extraMailPage(kit, pres, ctx, day, ev));
    // a "what you could do" page for each decision that opens today
    opensToday.forEach((node) => branchPage(kit, pres, ctx, day, node));
  });
}
