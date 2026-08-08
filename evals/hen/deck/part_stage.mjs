// part_stage.mjs — Part SEVEN: WHERE IT STANDS. Branch landscape, tracks,
// findings, gates, and the open questions/dilemmas the owner asked be shown clearly.
import { C, F, W, H, S } from "./theme.mjs";
import { STAGE } from "./content.mjs";

const PART = "where it stands";

export function buildStage(kit, pres, ctx) {
  const PROV = ctx.prov;
  kit.section("SEVEN", "Where it stands", "Everything known to be done, unproven, or unfinished — and every question the project has not yet answered. Read from the live trunk (origin/main).", PART);

  // headline
  {
    const s = kit.dark(PART);
    kit.head(s, "The honest summary", "A serious instrument in an unfinished state", { dark: true });
    s.addText(STAGE.headline, { x: S.MARGIN, y: 2.4, w: 11.6, h: 2.2, fontFace: F.HEAD, fontSize: 22, color: C.WHITE, margin: 0, lineSpacingMultiple: 1.28 });
    const provLine = PROV.behind > 0
      ? `This deck's checkout (${PROV.commit}) is ~${PROV.behind} commits behind origin/main. The branch landscape and open questions below are read from the live trunk.`
      : `Generated from the live trunk (${PROV.branch} @ ${PROV.commit}). The branch landscape below is the set of branches still carrying unmerged work.`;
    s.addText(provLine, { x: S.MARGIN, y: 5.4, w: 11.6, h: 1.0, fontFace: F.BODY, fontSize: 13, italic: true, color: "E8B54A", margin: 0, lineSpacingMultiple: 1.2 });
  }

  // branch landscape
  {
    const s = kit.light(PART);
    kit.head(s, "The branch landscape", "What's in flight, and how far along", "The branches carrying unique, unmerged work — ahead/behind the live trunk.");
    // header row
    const cols = [S.MARGIN, 4.6, 6.0, 8.2];
    s.addText("BRANCH", { x: cols[0], y: 2.15, w: 3.6, h: 0.25, fontFace: F.BODY, fontSize: 9, bold: true, color: C.FAINT, charSpacing: 1, margin: 0 });
    s.addText("±MAIN", { x: cols[1], y: 2.15, w: 1.3, h: 0.25, fontFace: F.BODY, fontSize: 9, bold: true, color: C.FAINT, charSpacing: 1, margin: 0 });
    s.addText("STAGE", { x: cols[2], y: 2.15, w: 2.1, h: 0.25, fontFace: F.BODY, fontSize: 9, bold: true, color: C.FAINT, charSpacing: 1, margin: 0 });
    s.addText("WHAT IT'S FOR", { x: cols[3], y: 2.15, w: 4.3, h: 0.25, fontFace: F.BODY, fontSize: 9, bold: true, color: C.FAINT, charSpacing: 1, margin: 0 });
    STAGE.branches.forEach((b, i) => {
      const [name, ahead, stage, forWhat, ck] = b;
      const y = 2.42 + i * 0.52;
      const col = C[ck] || C.TEAL;
      s.addShape(pres.ShapeType.rect, { x: S.MARGIN, y, w: 11.7, h: 0.006, fill: { color: C.LINE }, line: { type: "none" } });
      s.addShape(pres.ShapeType.rect, { x: S.MARGIN, y: y + 0.08, w: 0.06, h: 0.34, fill: { color: col }, line: { type: "none" } });
      s.addText(name, { x: cols[0] + 0.16, y: y + 0.05, w: 3.5, h: 0.5, fontFace: F.MONO, fontSize: 8.5, bold: true, color: C.INK, margin: 0, valign: "middle" });
      s.addText(ahead, { x: cols[1], y: y + 0.05, w: 1.3, h: 0.5, fontFace: F.MONO, fontSize: 8.5, color: C.MUTED, margin: 0, valign: "middle" });
      s.addText(stage, { x: cols[2], y: y + 0.05, w: 2.15, h: 0.5, fontFace: F.BODY, fontSize: 8.5, bold: true, color: col, margin: 0, valign: "middle", lineSpacingMultiple: 1.0 });
      s.addText(forWhat, { x: cols[3], y: y + 0.05, w: 4.3, h: 0.5, fontFace: F.BODY, fontSize: 8.5, color: C.MUTED, margin: 0, valign: "middle", lineSpacingMultiple: 1.0 });
    });
    kit.footnote(s, "Ahead/behind measured against origin/main. Two dozen further branches are fully absorbed into main. Source: git survey 2026-08-08.");
  }

  // tracks
  {
    const s = kit.light(PART);
    kit.head(s, "The tracks", "Every lane of work, and its stage");
    STAGE.tracks.forEach((t, i) => {
      const [name, status, blurb, ck] = t;
      const col = i % 2, row = Math.floor(i / 2);
      const x = S.MARGIN + col * 6.0, y = 2.3 + row * 1.15;
      const c = C[ck] || C.TEAL;
      kit.chip(s, { x, y, text: status, color: c, bg: C[ck + "_L"] || C.PALE, w: Math.min(2.6, 0.9 + status.length * 0.09) });
      s.addText(name, { x: x + (Math.min(2.6, 0.9 + status.length * 0.09)) + 0.15, y: y - 0.02, w: 5.7 - (Math.min(2.6, 0.9 + status.length * 0.09)) - 0.15, h: 0.34, fontFace: F.BODY, fontSize: 12.5, bold: true, color: C.INK, margin: 0, valign: "middle" });
      s.addText(blurb, { x, y: y + 0.36, w: 5.7, h: 0.72, fontFace: F.BODY, fontSize: 9.5, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });
    });
  }

  // the findings
  {
    const s = kit.light(PART);
    kit.head(s, "The state of it", "What the project's own audits have found");
    STAGE.findings.forEach(([t, b], i) => {
      const x = S.MARGIN + i * 4.06;
      s.addShape(pres.ShapeType.roundRect, { x, y: 2.4, w: 3.75, h: 3.5, rectRadius: 0.06, fill: { color: C.HARM_L }, line: { type: "none" } });
      s.addText(t, { x: x + 0.28, y: 2.62, w: 3.2, h: 0.9, fontFace: F.BODY, fontSize: 14.5, bold: true, color: C.HARM, margin: 0, valign: "top", lineSpacingMultiple: 1.1 });
      s.addText(b, { x: x + 0.28, y: 3.55, w: 3.2, h: 2.2, fontFace: F.BODY, fontSize: 11.5, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.16 });
    });
    kit.pull(s, "The story layer of this evaluation is finished. The simulation underneath it is not — and that is where almost every finding lands.", { y: 6.15 });
  }

  // the gates
  {
    const s = kit.light(PART);
    kit.head(s, "The bar", "What would have to be true before a score means what it appears to", "Six conditions the project set for itself. Each is named in its own documentation as a precondition for trusting a result.");
    STAGE.gates.forEach((g, i) => {
      const y = 2.45 + i * 0.68;
      s.addShape(pres.ShapeType.roundRect, { x: S.MARGIN, y: y + 0.04, w: 0.34, h: 0.34, rectRadius: 0.05, fill: { color: C.PALE }, line: { color: "C5CFD3", width: 1 } });
      s.addText(g, { x: 1.4, y, w: 11.1, h: 0.62, fontFace: F.BODY, fontSize: 12.5, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.12 });
    });
    s.addText("None of the six boxes is ticked yet.", { x: S.MARGIN, y: H - 0.85, w: 11.6, h: 0.4, fontFace: F.HEAD, fontSize: 18, italic: true, bold: true, color: C.HARM, margin: 0 });
  }

  // OPEN QUESTIONS & DILEMMAS — the owner asked for these prominently
  {
    const s = kit.dark("open questions");
    s.addText("STILL OPEN", { x: 1.0, y: 2.2, w: 11, h: 0.3, fontFace: F.BODY, fontSize: 12, bold: true, color: "7FA9B4", charSpacing: 2, margin: 0 });
    s.addText("The questions the project\nhasn't yet answered", { x: 1.0, y: 2.6, w: 11, h: 1.6, fontFace: F.HEAD, fontSize: 40, bold: true, color: C.WHITE, margin: 0, lineSpacingMultiple: 1.05 });
    s.addText("Ranked by consequence — the things a fresh look would flag first. Every one is a decision only the owner can make.", { x: 1.0, y: 4.4, w: 10.5, h: 0.9, fontFace: F.BODY, fontSize: 15, color: C.MIST, margin: 0, lineSpacingMultiple: 1.2 });
  }
  {
    const q = STAGE.questions;
    const perPage = 3;
    for (let p = 0; p * perPage < q.length; p++) {
      const s = kit.light("open questions");
      kit.head(s, `Unfinished · ${p + 1} of ${Math.ceil(q.length / perPage)}`, p === 0 ? "The dilemmas, most consequential first" : "The dilemmas, continued");
      q.slice(p * perPage, p * perPage + perPage).forEach(([question, context], i) => {
        const num = p * perPage + i + 1;
        const y = 2.35 + i * 1.5;
        s.addShape(pres.ShapeType.ellipse, { x: S.MARGIN, y: y + 0.02, w: 0.5, h: 0.5, fill: { color: C.HARM }, line: { type: "none" } });
        s.addText(String(num), { x: S.MARGIN, y: y + 0.02, w: 0.5, h: 0.5, fontFace: F.HEAD, fontSize: 18, bold: true, color: C.WHITE, align: "center", valign: "middle", margin: 0 });
        s.addText(question, { x: 1.5, y, w: 11.0, h: 0.5, fontFace: F.BODY, fontSize: 14.5, bold: true, color: C.INK, margin: 0, valign: "top", lineSpacingMultiple: 1.08 });
        s.addText(context, { x: 1.5, y: y + 0.5, w: 11.0, h: 0.9, fontFace: F.BODY, fontSize: 11, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.14 });
      });
    }
  }

  // closing
  {
    const s = kit.dark("open questions");
    s.addText("THE HONEST SUMMARY", { x: 1.0, y: 1.3, w: 11.3, h: 0.3, fontFace: F.BODY, fontSize: 12, bold: true, color: "7FA9B4", charSpacing: 2, margin: 0 });
    s.addText("A well-built evaluation with a real question at its centre, whose story layer is finished and whose physics layer is not — and which has not yet passed the checks its own designers set as the condition for believing its output.", { x: 1.0, y: 1.85, w: 11.0, h: 2.4, fontFace: F.HEAD, fontSize: 24, color: C.WHITE, margin: 0, lineSpacingMultiple: 1.25 });
    s.addText("A serious instrument in an unfinished state — which, for an evaluation that has never been used to make a public claim about a model, is roughly the right place to be.", { x: 1.0, y: 4.4, w: 10.8, h: 1.0, fontFace: F.BODY, fontSize: 16, color: C.MIST, margin: 0, lineSpacingMultiple: 1.2 });
    for (let i = 0; i < 6; i++) s.addShape(pres.ShapeType.roundRect, { x: 1.0 + i * 0.85, y: 5.7, w: 0.62, h: 0.9, rectRadius: 0.04, fill: { color: i === 3 ? "1E7C8F" : "12586B" }, line: { type: "none" } });
  }
}
