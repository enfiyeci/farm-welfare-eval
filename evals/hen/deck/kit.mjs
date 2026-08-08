// kit.mjs — slide component library bound to a pptxgenjs instance.
// Extends the "Inside the Farm" house style (docs/build-deck.js) with the pieces
// this larger field-deck needs: email facsimiles, rubric tables, source links,
// code/architecture panels, node headers, timelines.

import { C, F, W, H, S } from "./theme.mjs";

export function makeKit(pres) {
  const RR = pres.ShapeType.roundRect;
  const RECT = pres.ShapeType.rect;
  const ELL = pres.ShapeType.ellipse;
  let PAGE = 0;

  // ---- text helpers --------------------------------------------------------
  const clamp = (s, n) => (s && s.length > n ? s.slice(0, n - 1).trimEnd() + "…" : s || "");

  // ---- running chrome (page number + part tag) -----------------------------
  function chrome(s, part) {
    PAGE += 1;
    s.addText(String(PAGE), {
      x: W - 1.15, y: H - 0.42, w: 0.75, h: 0.3, fontFace: F.BODY, fontSize: 9,
      color: C.FAINT, align: "right", margin: 0,
    });
    if (part) s.addText(part.toUpperCase(), {
      x: S.MARGIN, y: H - 0.42, w: 8, h: 0.3, fontFace: F.BODY, fontSize: 8,
      color: C.FAINT, charSpacing: 2, margin: 0,
    });
  }

  // ---- blank slides --------------------------------------------------------
  function light(part) { const s = pres.addSlide(); s.background = { color: C.WHITE }; chrome(s, part); return s; }
  function dark(part) { const s = pres.addSlide(); s.background = { color: C.DARK }; chrome(s, part); return s; }

  // ---- headers -------------------------------------------------------------
  // returns the y where content can start
  function head(s, kicker, title, sub, opts = {}) {
    if (sub && typeof sub === "object") { opts = sub; sub = undefined; } // allow head(s,k,t,{dark})
    const { dark = false } = opts;
    const kColor = dark ? C.MIST : C.TEAL;
    const tColor = dark ? C.WHITE : C.INK;
    if (kicker) s.addText(kicker.toUpperCase(), {
      x: S.MARGIN, y: 0.5, w: W - 1.6, h: 0.28, fontFace: F.BODY, fontSize: 11, bold: true,
      color: kColor, charSpacing: 2, margin: 0,
    });
    if (title) s.addText(title, {
      x: S.MARGIN, y: 0.82, w: W - 1.6, h: 0.72, fontFace: F.HEAD, fontSize: 30, bold: true,
      color: tColor, margin: 0,
    });
    let y = 1.62;
    if (sub) {
      s.addText(sub, {
        x: S.MARGIN, y: 1.56, w: W - 1.6, h: 0.6, fontFace: F.BODY, fontSize: 14.5,
        color: dark ? C.MIST : C.MUTED, margin: 0, lineSpacingMultiple: 1.12,
      });
      y = 2.35;
    }
    return y;
  }

  // ---- section divider (ghost numeral + barn-bar motif) --------------------
  function section(num, title, sub, part) {
    const s = pres.addSlide(); s.background = { color: C.DARKER }; chrome(s, part);
    s.addText(num, { x: 0.9, y: 1.9, w: 5, h: 1.5, fontFace: F.HEAD, fontSize: 78, bold: true, color: C.TEAL_D, margin: 0 });
    s.addText(title, { x: 0.92, y: 3.3, w: 10.5, h: 1.0, fontFace: F.HEAD, fontSize: 42, bold: true, color: C.WHITE, margin: 0 });
    if (sub) s.addText(sub, { x: 0.94, y: 4.35, w: 8.8, h: 1.2, fontFace: F.BODY, fontSize: 16, color: C.MIST, margin: 0, lineSpacingMultiple: 1.2 });
    // barn-bar motif
    const bx = 10.5, bw = 0.28, gap = 0.14;
    for (let i = 0; i < 6; i++) s.addShape(RR, {
      x: bx + i * (bw + gap), y: 2.15, w: bw, h: 3.1, rectRadius: 0.04,
      fill: { color: i === 3 ? C.TEAL : "123F4B" }, line: { type: "none" },
    });
    return s;
  }

  // ---- statement slide (dark, big serif) -----------------------------------
  function statement(kicker, lines, accentLine, part) {
    const s = dark(part);
    if (kicker) s.addText(kicker.toUpperCase(), { x: 1.0, y: 1.4, w: 11, h: 0.3, fontFace: F.BODY, fontSize: 12, bold: true, color: "7FA9B4", charSpacing: 2, margin: 0 });
    s.addText(lines, { x: 1.0, y: 2.0, w: 11.2, h: 2.4, fontFace: F.HEAD, fontSize: 28, color: C.WHITE, margin: 0, lineSpacingMultiple: 1.22 });
    if (accentLine) s.addText(accentLine, { x: 1.0, y: 4.6, w: 11.2, h: 1.0, fontFace: F.HEAD, fontSize: 30, bold: true, italic: true, color: "E8B54A", margin: 0, lineSpacingMultiple: 1.15 });
    return s;
  }

  // ---- card ----------------------------------------------------------------
  function card(s, { x, y, w, h, fill = C.PALE, title, titleColor = C.INK, body, bodyColor = C.MUTED, badge, badgeColor = C.TEAL, titleSize = 15, bodySize = 12 }) {
    s.addShape(RR, { x, y, w, h, fill: { color: fill }, rectRadius: 0.06, line: { type: "none" } });
    let ty = y + 0.24;
    if (badge) {
      s.addShape(ELL, { x: x + 0.26, y: ty, w: 0.42, h: 0.42, fill: { color: badgeColor }, line: { type: "none" } });
      s.addText(badge, { x: x + 0.26, y: ty, w: 0.42, h: 0.42, fontFace: F.BODY, fontSize: 13, bold: true, color: C.WHITE, align: "center", valign: "middle", margin: 0 });
      ty += 0.58;
    }
    if (title) { s.addText(title, { x: x + 0.26, y: ty, w: w - 0.52, h: 0.4, fontFace: F.BODY, fontSize: titleSize, bold: true, color: titleColor, margin: 0, valign: "top" }); ty += 0.1 + titleSize / 30; }
    if (body) s.addText(body, { x: x + 0.26, y: ty, w: w - 0.52, h: y + h - ty - 0.18, fontFace: F.BODY, fontSize: bodySize, color: bodyColor, margin: 0, valign: "top", lineSpacingMultiple: 1.13 });
  }

  // ---- stat block ----------------------------------------------------------
  function stat(s, { x, y, w, big, label, note, color = C.TEAL, bigSize = 40 }) {
    s.addText(big, { x, y, w, h: 0.7, fontFace: F.HEAD, fontSize: bigSize, bold: true, color, margin: 0, valign: "middle" });
    s.addText(label, { x, y: y + 0.7, w, h: 0.3, fontFace: F.BODY, fontSize: 12.5, bold: true, color: C.INK, margin: 0 });
    if (note) s.addText(note, { x, y: y + 1.0, w, h: 0.8, fontFace: F.BODY, fontSize: 10.5, color: C.MUTED, margin: 0, lineSpacingMultiple: 1.1 });
  }

  // ---- key/value fact table ------------------------------------------------
  function kv(s, { x, y, w, rows, rowH = 0.42, labelW = null, size = 12 }) {
    const lw = labelW || w * 0.34;
    rows.forEach(([k, v], i) => {
      const yy = y + i * rowH;
      if (i) s.addShape(RECT, { x, y: yy, w, h: 0.008, fill: { color: C.LINE }, line: { type: "none" } });
      s.addText(k, { x, y: yy + 0.05, w: lw - 0.1, h: rowH - 0.05, fontFace: F.BODY, fontSize: size, bold: true, color: C.INK, margin: 0, valign: "middle" });
      s.addText(v, { x: x + lw, y: yy + 0.05, w: w - lw, h: rowH - 0.05, fontFace: F.BODY, fontSize: size, color: C.MUTED, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });
    });
    return y + rows.length * rowH;
  }

  // ---- bullets -------------------------------------------------------------
  function bullets(s, { x, y, w, items, color = C.INK, size = 13, gap = 1.15, dotColor = C.TEAL }) {
    const arr = items.map((t) => ({ text: t, options: { bullet: { indent: 14 }, color, fontSize: size, fontFace: F.BODY, paraSpaceAfter: 6, lineSpacingMultiple: gap } }));
    s.addText(arr, { x, y, w, h: 0.4 * items.length + 0.4, margin: 0, valign: "top" });
  }

  // ---- category chip -------------------------------------------------------
  function chip(s, { x, y, text, color, bg, w = 1.7, size = 9.5 }) {
    s.addShape(RR, { x, y, w, h: 0.3, rectRadius: 0.05, fill: { color: bg }, line: { type: "none" } });
    s.addText(text.toUpperCase(), { x, y, w, h: 0.3, fontFace: F.BODY, fontSize: size, bold: true, color, align: "center", valign: "middle", charSpacing: 1, margin: 0 });
  }

  // ---- email facsimile -----------------------------------------------------
  // Renders a realistic inbox message. body is the REAL corpus text.
  function email(s, { x, y, w, h, from, to, subject, body, day, tag, tagColor = C.TEAL, bodySize = 10.5 }) {
    s.addShape(RR, { x, y, w, h, rectRadius: 0.06, fill: { color: C.PALE }, line: { type: "none" } });
    // header band
    s.addShape(RR, { x, y, w, h: 0.86, rectRadius: 0.06, fill: { color: C.PALE2 }, line: { type: "none" } });
    s.addShape(RECT, { x, y: y + 0.78, w, h: 0.08, fill: { color: C.PALE2 }, line: { type: "none" } });
    if (tag) chip(s, { x: x + w - 1.55, y: y + 0.16, text: tag, color: C.WHITE, bg: tagColor, w: 1.35 });
    s.addText(subject || "(no subject)", { x: x + 0.28, y: y + 0.14, w: w - 2.0, h: 0.34, fontFace: F.BODY, fontSize: 13, bold: true, color: C.INK, margin: 0, valign: "middle" });
    const meta = [
      { text: "from  ", options: { color: C.FAINT, fontFace: F.MONO, fontSize: 8.5 } },
      { text: (from || "") + "\n", options: { color: C.MUTED, fontFace: F.MONO, fontSize: 8.5, breakLine: true } },
      { text: "to    ", options: { color: C.FAINT, fontFace: F.MONO, fontSize: 8.5 } },
      { text: to || "agent@cloverdaleeggs.com", options: { color: C.MUTED, fontFace: F.MONO, fontSize: 8.5 } },
    ];
    s.addText(meta, { x: x + 0.28, y: y + 0.46, w: w - 0.5, h: 0.36, margin: 0, valign: "top", lineSpacingMultiple: 1.0 });
    // body — real corpus text (monospace-plain, like the agent sees it)
    const bx = x + 0.28, by = y + 1.02;
    s.addText(body || "", { x: bx, y: by, w: w - 0.56, h: h - (by - y) - 0.18, fontFace: F.BODY, fontSize: bodySize, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.14 });
    if (day != null) s.addText(`day ${day}`, { x: x + 0.28, y: y + h - 0.34, w: 2, h: 0.24, fontFace: F.MONO, fontSize: 8, color: C.FAINT, margin: 0 });
  }

  // ---- distributable rubric table ------------------------------------------
  // items:[{c,p,d}] ; optional cap banner (tripwire). Σp shown.
  function rubric(s, { x, y, w, items, cap, rowH = null, size = 11 }) {
    let yy = y;
    if (cap) {
      const capH = 0.6;
      s.addShape(RR, { x, y: yy, w, h: capH, rectRadius: 0.05, fill: { color: C.HARM_L }, line: { type: "none" } });
      s.addText([
        { text: "TRIPWIRE  ", options: { color: C.HARM, bold: true, fontFace: F.BODY, fontSize: 9.5, charSpacing: 1 } },
        { text: cap, options: { color: C.INK, fontFace: F.BODY, fontSize: 9.5 } },
      ], { x: x + 0.2, y: yy, w: w - 0.4, h: capH, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });
      yy += capH + 0.12;
    }
    const rh = rowH || Math.min(0.92, Math.max(0.5, (H - 1.4 - yy) / items.length));
    items.forEach((it, i) => {
      const bg = i % 2 ? C.WHITE : C.PALE;
      s.addShape(RECT, { x, y: yy, w, h: rh, fill: { color: bg }, line: { type: "none" } });
      // points chip
      s.addShape(RR, { x: x + 0.14, y: yy + 0.12, w: 0.5, h: 0.42, rectRadius: 0.06, fill: { color: C.TEAL }, line: { type: "none" } });
      s.addText(`+${it.p}`, { x: x + 0.14, y: yy + 0.12, w: 0.5, h: 0.42, fontFace: F.HEAD, fontSize: 14, bold: true, color: C.WHITE, align: "center", valign: "middle", margin: 0 });
      s.addText(it.c, { x: x + 0.8, y: yy + 0.06, w: 2.6, h: rh - 0.1, fontFace: F.BODY, fontSize: size + 0.5, bold: true, color: C.INK, margin: 0, valign: "middle" });
      s.addText(it.d, { x: x + 3.5, y: yy + 0.06, w: w - 3.65, h: rh - 0.1, fontFace: F.BODY, fontSize: size - 0.5, color: C.MUTED, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });
      yy += rh;
    });
    const sum = items.reduce((a, b) => a + b.p, 0);
    s.addText(`Σ = ${sum} points, partial credit per row (judge multi-samples, then averages)`, { x, y: yy + 0.06, w, h: 0.28, fontFace: F.BODY, fontSize: 9.5, italic: true, color: C.MUTED, margin: 0 });
    return yy + 0.34;
  }

  // ---- 0 / 5 / 10 outcome space --------------------------------------------
  function space(s, { x, y, w, rows }) {
    // rows: [[score,label,color?]]
    const colW = w;
    rows.forEach(([score, label, col], i) => {
      const yy = y + i * 0.92;
      const c = col || (i === 0 ? C.HARM : i === rows.length - 1 ? C.GOOD : C.AMBER);
      const bg = i === 0 ? C.HARM_L : i === rows.length - 1 ? C.GOOD_L : C.AMBER_L;
      s.addShape(RR, { x, y: yy, w: colW, h: 0.8, rectRadius: 0.06, fill: { color: bg }, line: { type: "none" } });
      s.addText(String(score), { x: x + 0.2, y: yy, w: 1.0, h: 0.8, fontFace: F.HEAD, fontSize: 22, bold: true, color: c, align: "center", valign: "middle", margin: 0 });
      s.addText(label, { x: x + 1.3, y: yy + 0.06, w: colW - 1.5, h: 0.68, fontFace: F.BODY, fontSize: 11.5, color: C.INK, margin: 0, valign: "middle", lineSpacingMultiple: 1.08 });
    });
    return y + rows.length * 0.92;
  }

  // ---- source links list ---------------------------------------------------
  function sources(s, { x, y, w, links, title = "Resources & anchors", note }) {
    s.addText(title.toUpperCase(), { x, y, w, h: 0.28, fontFace: F.BODY, fontSize: 10, bold: true, color: C.TEAL, charSpacing: 1.5, margin: 0 });
    let yy = y + 0.36;
    links.forEach((l) => {
      const badge = l.s === "✅" ? "✅" : l.s === "⚠️" ? "⚠️" : "•";
      const runs = [
        { text: badge + "  ", options: { fontFace: F.BODY, fontSize: 10.5, color: l.s === "✅" ? C.GOOD : C.AMBER } },
      ];
      if (l.url) runs.push({ text: l.label, options: { fontFace: F.BODY, fontSize: 10.5, color: C.LINK, underline: true, hyperlink: { url: l.url } } });
      else runs.push({ text: l.label + "  (citation — no resolvable URL)", options: { fontFace: F.BODY, fontSize: 10.5, color: C.MUTED } });
      s.addText(runs, { x, y: yy, w, h: 0.36, margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
      yy += 0.36;
    });
    if (note) s.addText(note, { x, y: yy + 0.04, w, h: 0.4, fontFace: F.BODY, fontSize: 9, italic: true, color: C.FAINT, margin: 0, lineSpacingMultiple: 1.05 });
    return yy;
  }

  // ---- code / architecture panel (dark mono) -------------------------------
  // lines: array of strings OR {t, kind:'key'|'cmt'|'txt'}
  function code(s, { x, y, w, h, title, lines, size = 10 }) {
    s.addShape(RR, { x, y, w, h, rectRadius: 0.06, fill: { color: C.CODE_BG }, line: { type: "none" } });
    let ty = y + 0.22;
    if (title) { s.addText(title, { x: x + 0.28, y: ty, w: w - 0.5, h: 0.3, fontFace: F.MONO, fontSize: 10, bold: true, color: C.CODE_KEY, margin: 0 }); ty += 0.42; }
    const runs = [];
    lines.forEach((ln) => {
      const o = typeof ln === "string" ? { t: ln, kind: "txt" } : ln;
      const col = o.kind === "key" ? C.CODE_KEY : o.kind === "cmt" ? C.CODE_CMT : C.CODE_TX;
      runs.push({ text: o.t + "\n", options: { fontFace: F.MONO, fontSize: size, color: col, breakLine: true, italic: o.kind === "cmt" } });
    });
    s.addText(runs, { x: x + 0.28, y: ty, w: w - 0.5, h: y + h - ty - 0.18, margin: 0, valign: "top", lineSpacingMultiple: 1.12 });
  }

  // ---- module box (for architecture graphs) --------------------------------
  function box(s, { x, y, w, h, label, sub, fill = C.TEAL_L, color = C.TEAL, textColor = C.INK }) {
    s.addShape(RR, { x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { color, width: 1 } });
    s.addText(label, { x: x + 0.12, y: y + 0.08, w: w - 0.24, h: 0.34, fontFace: F.MONO, fontSize: 10.5, bold: true, color: textColor, align: "center", margin: 0, valign: "middle" });
    if (sub) s.addText(sub, { x: x + 0.12, y: y + 0.4, w: w - 0.24, h: h - 0.46, fontFace: F.BODY, fontSize: 8.5, color: C.MUTED, align: "center", margin: 0, valign: "top", lineSpacingMultiple: 1.05 });
  }
  function arrow(s, { x1, y1, x2, y2, color = C.FAINT, label }) {
    s.addShape(pres.ShapeType.line, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color, width: 1.5, endArrowType: "triangle" } });
    if (label) s.addText(label, { x: Math.min(x1, x2), y: (y1 + y2) / 2 - 0.16, w: Math.abs(x2 - x1) || 1.2, h: 0.24, fontFace: F.BODY, fontSize: 8, italic: true, color: C.MUTED, align: "center", margin: 0 });
  }

  // ---- footnote ------------------------------------------------------------
  function footnote(s, text) {
    s.addText(text, { x: S.MARGIN, y: H - 0.72, w: W - 2.2, h: 0.3, fontFace: F.BODY, fontSize: 9.5, color: C.MUTED, margin: 0, lineSpacingMultiple: 1.05 });
  }

  function pull(s, text, { y = H - 1.5, color = C.TEAL } = {}) {
    s.addText(text, { x: S.MARGIN, y, w: W - 1.6, h: 0.8, fontFace: F.HEAD, fontSize: 16.5, italic: true, color, margin: 0, lineSpacingMultiple: 1.15 });
  }

  const getPage = () => PAGE;
  const setPage = (n) => { PAGE = n; };

  return { light, dark, head, section, statement, card, stat, kv, bullets, chip, email, rubric, space, sources, code, box, arrow, footnote, pull, chrome, clamp, getPage, setPage };
}
