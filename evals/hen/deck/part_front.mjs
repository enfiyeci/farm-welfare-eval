// part_front.mjs — cover, contents, provenance, the premise, the question.
import { C, F, W, H, S } from "./theme.mjs";

export function buildFront(kit, pres, ctx) {
  const { nodes, events, dims } = ctx;
  const PROV = ctx.prov;
  const enabled = nodes.filter((n) => n.enabled).length;
  const emailCount = (events.events || []).filter((e) => e.payload?.body_ref).length;
  const weighted = dims.filter((d) => Number(d.weight) > 0).length;
  const gates = dims.length - weighted;

  // 1 — cover
  {
    const s = pres.addSlide(); s.background = { color: C.DARK };
    s.addText("THE COMPLETE FIELD RECORD · GENERATED FROM THE REPOSITORY", { x: 0.9, y: 0.95, w: 11.5, h: 0.3, fontFace: F.BODY, fontSize: 11.5, bold: true, color: "7FA9B4", charSpacing: 2, margin: 0 });
    s.addText("Inside the Farm,\nEnd to End", { x: 0.86, y: 1.35, w: 11.5, h: 2.2, fontFace: F.HEAD, fontSize: 54, bold: true, color: C.WHITE, margin: 0, lineSpacingMultiple: 1.02 });
    s.addText("Every subsystem, every day, every decision — the farm-welfare alignment\neval read straight out of its own source.", { x: 0.9, y: 3.55, w: 10.5, h: 1.0, fontFace: F.BODY, fontSize: 19, color: C.MIST, margin: 0, lineSpacingMultiple: 1.2 });
    // barn-bar motif
    for (let i = 0; i < 6; i++) s.addShape(pres.ShapeType.roundRect, { x: 0.9 + i * 1.02, y: 5.0, w: 0.78, h: 1.2, rectRadius: 0.05, fill: { color: i === 3 ? "1E7C8F" : "12586B" }, line: { type: "none" } });
    s.addText("Cloverdale Egg Farms, Complex 2  ·  Verdon Springs, Iowa\n518 simulated days  ·  " + enabled + " scored welfare decisions  ·  ~592,000 hens", { x: 7.4, y: 5.15, w: 5.1, h: 1.1, fontFace: F.BODY, fontSize: 12, color: "7FA9B4", margin: 0, lineSpacingMultiple: 1.35 });
    s.addText(`generated from ${PROV.branch} @ ${PROV.commit} · ${PROV.date}`, { x: 0.9, y: 6.9, w: 11.5, h: 0.3, fontFace: F.MONO, fontSize: 9, color: "5E7C83", margin: 0 });
  }

  // 2 — how to read this
  {
    const s = kit.light("orientation");
    kit.head(s, "How to read this", "Eight parts, one source of truth", "Every figure, email, rubric and price on the following pages is read from the repository at build time. Re-run the generator after a change and the deck refreshes.");
    const parts = [
      ["ONE", "The decisions", "All 23 decision points — category, the real triggering email, the judge's rubric, the outcome space, and sourced links."],
      ["TWO", "The walk", "The 518 days as the agent lives them — the actual inbox, the open windows, the branches, session by session."],
      ["THREE", "The world", "Cloverdale: the company, six barns, the cast, the money, and the four red lines nobody states."],
      ["FOUR", "How it runs", "The loop, the eighteen tools, and everything hidden from the model on purpose."],
      ["FIVE", "The codebase, wired", "Env core, the reactive substrate, the adapter, the judge — module by module, and the seams that join them."],
      ["SIX", "The judge", "Ten dimensions, the node-score headline, the quote-evidence gate — and where the code diverged from the spec."],
      ["SEVEN", "Where it stands", "The branch landscape, what's done, and the open questions the project hasn't yet answered."],
      ["EIGHT", "Sources", "The load-bearing anchor register, with working links, behind every compliance number and rubric."],
    ];
    parts.forEach(([n, t, d], i) => {
      const col = i % 2, row = Math.floor(i / 2);
      const x = S.MARGIN + col * 6.0, y = 2.5 + row * 1.05;
      s.addText(n, { x, y, w: 1.1, h: 0.6, fontFace: F.HEAD, fontSize: 20, bold: true, color: C.TEAL_D, margin: 0, valign: "top" });
      s.addText(t, { x: x + 1.1, y: y - 0.02, w: 4.6, h: 0.32, fontFace: F.BODY, fontSize: 14, bold: true, color: C.INK, margin: 0 });
      s.addText(d, { x: x + 1.1, y: y + 0.3, w: 4.7, h: 0.7, fontFace: F.BODY, fontSize: 10, color: C.MUTED, margin: 0, valign: "top", lineSpacingMultiple: 1.08 });
    });
  }

  // 3 — the premise
  {
    const s = kit.light("orientation");
    kit.head(s, "The premise", "Three sentences, then four hundred pages of detail");
    const items = [
      ["1", "We built a fake egg farm.", "Six barns, ~592,000 hens, a manager, a vet, a private-equity owner pushing for cost cuts, and seventeen months of weather, prices and problems — all written in advance.", C.TEAL, C.TEAL_L],
      ["2", "We handed it to an AI to run.", "It is told it is the farm's operations software. It gets tools: read a sensor, adjust ventilation, order feed, book the vet, send an email. Then time starts moving.", C.AMBER, C.AMBER_L],
      ["3", "We watched what it did.", "Twenty-two moments arrive where the cheap option quietly hurts the animals. Nobody flags them. Everything is recorded in a ledger the model cannot see.", C.HARM, C.HARM_L],
    ];
    items.forEach(([n, t, b, c, bg], i) => {
      const x = S.MARGIN + i * 4.06;
      kit.card(s, { x, y: 2.4, w: 3.75, h: 2.8, fill: bg, badge: n, badgeColor: c, title: t, body: b, titleSize: 16, bodySize: 12 });
    });
    kit.pull(s, "The point is not whether the model knows the right answer if you ask it. It is what it does when nobody frames the question.", { y: 5.5 });
  }

  // 4 — by the numbers
  {
    const s = kit.light("orientation");
    kit.head(s, "By the numbers", "What was actually built");
    const stats = [
      [String(events.events?.length || 0), "scheduled events", "emails, pricing shifts, seeds, the audit", C.TEAL],
      [String(emailCount), "authored emails wired to events", "each written by hand; most deliberately boring", C.AMBER],
      [String(nodes.length), "decision points", "23 defined, " + enabled + " enabled, 1 disabled (broken)", C.HARM],
      [String(dims.length), "judge dimensions", `${weighted} weighted + ${gates} validity gates`, C.TEAL],
      ["16", "tools", "the model's entire ability to see and act (+ end_day)", C.TEAL],
      ["0", "hints", "nothing mentions welfare, ethics, or scoring", C.HARM],
    ];
    stats.forEach(([big, label, note, c], i) => {
      const col = i % 3, row = Math.floor(i / 3);
      kit.stat(s, { x: S.MARGIN + col * 4.05, y: 2.4 + row * 2.15, w: 3.6, big, label, note, color: c });
    });
    kit.footnote(s, "Every figure read straight out of the repository at build time: schedule/events.yml, config.yml, corpus/, judge/dimensions/.");
  }

  // 5 — provenance / colophon (the honesty slide about staleness)
  {
    const s = kit.dark("orientation");
    kit.head(s, "Provenance", "What this deck is, and is not", { dark: true });
    s.addText(PROV.note, { x: S.MARGIN, y: 2.4, w: 11.5, h: 2.0, fontFace: F.BODY, fontSize: 15, color: C.MIST, margin: 0, lineSpacingMultiple: 1.3 });
    kit.card(s, { x: S.MARGIN, y: 4.6, w: 5.7, h: 1.7, fill: "16454F", title: "Generated from", titleColor: C.WHITE, body: `${PROV.branch}\n@ ${PROV.commit}  ·  ${PROV.date}\n${PROV.behind > 0 ? "~" + PROV.behind + " commits behind origin/main" : "the current trunk (origin/main)"}`, bodyColor: C.MIST, bodySize: 12 });
    kit.card(s, { x: 6.8, y: 4.6, w: 5.7, h: 1.7, fill: "16454F", title: "Re-generate after any change", titleColor: "E8B54A", body: "node build.mjs  — reads the current checkout and rebuilds every page. Review the affected slides after each refresh.", bodyColor: C.MIST, bodySize: 12 });
  }

  // 6 — the question
  kit.statement("The question underneath",
    "If you give a capable AI system genuine operational control over living creatures, a believable commercial reason to cut corners, and no reminder that anyone is watching —",
    "does it still look after them?", "orientation");
}
