// part_codebase.mjs — Part FIVE: THE CODEBASE, WIRED. From the architecture survey.
import { C, F, W, H, S } from "./theme.mjs";
import { ARCH } from "./content.mjs";

const PART = "the codebase";

function filesTable(kit, pres, s, x, y, w, files, rowH = 0.56) {
  files.forEach(([f, d], i) => {
    const yy = y + i * rowH;
    if (i) s.addShape(pres.ShapeType.rect, { x, y: yy, w, h: 0.008, fill: { color: C.LINE }, line: { type: "none" } });
    s.addText(f, { x, y: yy + 0.04, w: 2.7, h: rowH - 0.05, fontFace: F.MONO, fontSize: 9, bold: true, color: C.INK, margin: 0, valign: "middle" });
    s.addText(d, { x: x + 2.8, y: yy + 0.04, w: w - 2.8, h: rowH - 0.05, fontFace: F.BODY, fontSize: 9.5, color: C.MUTED, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });
  });
}

export function buildCodebase(kit, pres, ctx) {
  kit.section("FIVE", "The codebase, wired", "Two layers: an Inspect-free environment core, and the Inspect adapter that makes it a runnable eval. Here is every subsystem, and the seams that join them.", PART);

  // data-flow spine
  {
    const s = kit.light(PART);
    kit.head(s, "The spine", "How one episode flows, start to finish", "From the eval command to the final score — the control path through solver, env core, the reactive model, and the judge.");
    kit.code(s, { x: S.MARGIN, y: 2.25, w: 7.6, h: 4.55, title: "one episode", lines: ARCH.spine, size: 9 });
    kit.card(s, { x: 8.3, y: 2.25, w: 4.2, h: 2.15, fill: C.PALE, title: "Two silent ledgers ride along", titleColor: C.INK, body: "The decision ledger (which actions matched which decision) and the action/read log. The judge reads both; the agent sees only tool return strings.", bodySize: 11.5 });
    kit.card(s, { x: 8.3, y: 4.6, w: 4.2, h: 2.2, fill: C.TEAL_L, title: "The key bet", titleColor: C.TEAL, body: "A deterministic reactive substrate: the world responds to the agent's actions the same way every run. No wall clock, no RNG — a run reproduces exactly. That is what makes a static, pre-authored eval realistic.", bodySize: 11.5 });
  }

  // per-subsystem
  ARCH.subsystems.forEach((sub) => {
    const s = kit.light(PART);
    const col = C[sub.color] || C.TEAL;
    kit.chip(s, { x: S.MARGIN, y: 0.5, text: sub.tag, color: col, bg: C[sub.color + "_L"] || C.TEAL_L, w: Math.min(5.5, 1.2 + sub.tag.length * 0.075) });
    s.addText(sub.name, { x: S.MARGIN, y: 0.95, w: 11.7, h: 0.7, fontFace: F.HEAD, fontSize: 28, bold: true, color: C.INK, margin: 0 });
    s.addText(sub.blurb, { x: S.MARGIN, y: 1.72, w: 11.7, h: 1.05, fontFace: F.BODY, fontSize: 12, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.14 });
    const fy = 2.9, rowH = Math.min(0.5, (6.7 - fy) / sub.files.length);
    filesTable(kit, pres, s, S.MARGIN, fy, 11.7, sub.files, rowH);
  });

  // the 5 welfare channels (Layer 1)
  {
    const s = kit.light(PART);
    kit.head(s, "The reactive substrate", "The five Layer-1 welfare channels", "The objective welfare-state score: how the animals actually ended up, accumulated hour by hour. Four are agent-controllable; one is intentionally not.");
    ARCH.channels.forEach(([name, w, note], i) => {
      const y = 2.4 + i * 0.82;
      const live = !note.startsWith("degenerate");
      s.addShape(pres.ShapeType.roundRect, { x: S.MARGIN, y, w: 11.7, h: 0.68, rectRadius: 0.05, fill: { color: live ? C.PALE : C.PALE2 }, line: { type: "none" } });
      s.addText(name, { x: S.MARGIN + 0.3, y: y + 0.04, w: 3.6, h: 0.6, fontFace: F.MONO, fontSize: 12, bold: true, color: live ? C.INK : C.MUTED, margin: 0, valign: "middle" });
      // weight bar
      s.addShape(pres.ShapeType.rect, { x: 5.2, y: y + 0.26, w: 3.0 * (w / 0.25), h: 0.16, fill: { color: live ? C.TEAL : "C6CED2" }, line: { type: "none" } });
      s.addText(`w ${w}`, { x: 8.35, y: y + 0.04, w: 0.8, h: 0.6, fontFace: F.BODY, fontSize: 11, bold: true, color: live ? C.TEAL : C.MUTED, margin: 0, valign: "middle" });
      s.addText(note, { x: 9.2, y: y + 0.04, w: 3.2, h: 0.6, fontFace: F.BODY, fontSize: 10, color: live ? C.MUTED : C.HARM, margin: 0, valign: "middle", lineSpacingMultiple: 1.05 });
    });
    kit.footnote(s, "judge/welfare_state.py — weights sum to 1.0. A channel whose good/negligent anchors coincide scores 1.0 unconditionally and drops out of the mean (keel is intentionally degenerate: management cannot move it).");
  }

  // load-bearing seams
  {
    const s = kit.light(PART);
    kit.head(s, "The seams", "The handful of places everything plugs into", "If you learn only eight things about the code, learn these.");
    ARCH.seams.forEach(([t, d], i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = S.MARGIN + col * 6.0, y = 2.35 + row * 1.12;
      s.addText(t, { x, y, w: 5.7, h: 0.3, fontFace: F.MONO, fontSize: 10.5, bold: true, color: C.TEAL, margin: 0 });
      s.addText(d, { x, y: y + 0.3, w: 5.7, h: 0.78, fontFace: F.BODY, fontSize: 10, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });
    });
  }
}
