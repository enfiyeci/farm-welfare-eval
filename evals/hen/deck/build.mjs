// build.mjs — assembles the full "Inside the Farm, End to End" deck from real repo data.
// Run: REPO_ROOT=/path/to/farm-eval node build.mjs   (defaults to the owner's checkout)
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");

import { makeKit } from "./kit.mjs";
import { buildNodes as loadNodeData, loadJudgeDims, gitProvenance } from "./data.mjs";
import { buildFront } from "./part_front.mjs";
import { buildNodes } from "./part_nodes.mjs";
import { buildDayByDay } from "./part_daybyday.mjs";
import { buildWorld, buildHarness } from "./part_world.mjs";
import { buildCodebase } from "./part_codebase.mjs";
import { buildJudge } from "./part_judge.mjs";
import { buildStage } from "./part_stage.mjs";
import { buildSources } from "./part_sources.mjs";

const data = await loadNodeData();
const dims = loadJudgeDims();
const g = gitProvenance();
const prov = {
  ...g,
  note: g.behind > 0
    ? `This deck was generated from ${g.branch} @ ${g.commit}, which is ~${g.behind} commits behind origin/main. The engine renders whatever checkout it runs in — re-run against a pulled origin/main to make it fully current. The project-stage section is read from the live trunk and says so.`
    : `This deck was generated from ${g.branch} @ ${g.commit} — the current trunk. Every figure, email, rubric and price is read from the repository at build time, so a re-run after any change refreshes the deck. Review the slides affected by what you changed.`,
};
const ctx = { ...data, dims, prov };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "farm-eval";
pres.title = "Inside the Farm, End to End";
const kit = makeKit(pres);

buildFront(kit, pres, ctx);      // orientation
buildNodes(kit, pres, ctx);      // ONE   — the decisions
buildDayByDay(kit, pres, ctx);   // TWO   — the walk
buildWorld(kit, pres, ctx);      // THREE — the world
buildHarness(kit, pres, ctx);    // FOUR  — how it runs
buildCodebase(kit, pres, ctx);   // FIVE  — the codebase, wired
buildJudge(kit, pres, ctx);      // SIX   — the judge
buildStage(kit, pres, ctx);      // SEVEN — where it stands + open questions
buildSources(kit, pres, ctx);    // EIGHT — sources

const out = process.env.DECK_OUT || "inside-the-farm-full.pptx";
await pres.writeFile({ fileName: out });
console.log(`wrote ${out} — ${kit.getPage()} chromed content pages (+ dividers/cover)`);
