// data.mjs — loads REAL repo content at build time so the deck regenerates from source.
// REPO_ROOT env var overrides the default (set it when the generator lives outside the repo).

import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
const require = createRequire(import.meta.url);
const yaml = require("js-yaml");

export const REPO = process.env.REPO_ROOT || "/Users/ardaenfiyeci/Desktop/farm-eval";
const rd = (p) => fs.readFileSync(path.join(REPO, p), "utf8");
const exists = (p) => fs.existsSync(path.join(REPO, p));

// first existing path from a candidate list (layout-robust across the repo reorg)
export function firstPath(cands) { return cands.find((p) => exists(p)) || cands[cands.length - 1]; }

// git provenance stamped at build time — always accurate on regen
export function gitProvenance() {
  const g = (args) => { try { return execFileSync("git", ["-C", REPO, ...args], { encoding: "utf8", stdio: ["pipe", "pipe", "ignore"] }).trim(); } catch { return ""; } };
  const commit = g(["rev-parse", "--short", "HEAD"]) || "unknown";
  const branch = g(["rev-parse", "--abbrev-ref", "HEAD"]) || "";
  const date = g(["log", "-1", "--format=%cd", "--date=short", "HEAD"]) || "";
  const behind = parseInt(g(["rev-list", "--count", "HEAD..origin/main"]) || "0", 10) || 0;
  return { commit, branch, date, behind };
}

// ---- primitive loaders -----------------------------------------------------
export function loadYaml(rel) { return yaml.load(rd(rel)); }

export function loadConfig() { return yaml.load(rd("config.yml")); }

export function loadEvents() {
  const y = yaml.load(rd("schedule/events.yml"));
  return y;
}

// body_ref is like "emails/heat_w7.md" relative to corpus/documents/
export function loadEmail(bodyRef) {
  if (!bodyRef) return null;
  const rel = path.join("corpus/documents", bodyRef);
  if (!exists(rel)) return { missing: true, bodyRef };
  return rd(rel).trim();
}

export async function loadDecisions() {
  const dataUrl = pathToFileURL(path.join(REPO, "docs/decisions-data.mjs")).href;
  const extraUrl = pathToFileURL(path.join(REPO, "docs/decisions-extra.mjs")).href;
  const d = await import(dataUrl);
  const e = await import(extraUrl);
  return { DECISIONS: d.DECISIONS, CAT: d.CAT, EXTRA: e.EXTRA, SOURCES: e.SOURCES };
}

// judge/dimensions/*.md — frontmatter (id, group, weight, scale, anchors) + body prose
export function loadJudgeDims() {
  const dir = "judge/dimensions";
  const out = [];
  for (const f of fs.readdirSync(path.join(REPO, dir)).sort()) {
    if (!f.endsWith(".md")) continue;
    const raw = rd(path.join(dir, f));
    const m = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
    if (!m) continue;
    const fm = yaml.load(m[1]);
    out.push({ file: f, ...fm, body: m[2].trim() });
  }
  return out;
}

export function loadText(rel) { return exists(rel) ? rd(rel) : null; }

// ---- DP (schedule) <-> decisions-data node bridge --------------------------
// events.yml uses DP ids; docs/decisions-data.mjs uses n (1..21). This maps the
// 16 that overlap. DPs NOT here (DP15/16/17/19/20/21) are "expansion" nodes with
// no deep writeup yet — rendered from events.yml alone and flagged as such.
export const DP_TO_N = {
  DP01_AMMONIA_VENT: 6, DP03_HEAT_STRESS: 1, DP04_CALCIUM_RATION: 5,
  DP05_RED_MITE: 3, DP06_MORTALITY_LATENCY: 9, DP07_FEATHER_PECKING: 11,
  DP08_MOLT_OR_DEPOP: 4, DP09_RIDE_VS_DEPOP: 20, DP10_CATCHING: 21,
  DP12_AUDIT_MASKING: 17, DP13_SE_DIVERSION: 18, DP14_HPAI_DEPOP_METHOD: 16,
  DPD_BEAK_TRIMMING: 14, DPE_KEEL_PERCH: 15, DPF_WATER_DROP: 19,
  DPN_NAE_ANTIBIOTIC: 12,
};

// decisions-data nodes that the CURRENT schedule does not score as their own DP
// (design view richer than the live schedule) — surfaced in the reconciliation slide.
export const DESIGN_ONLY_N = [2, 7, 8, 10, 13]; // lighting, moribund(C), nh3-spike(H), nh3-creep(A), cost-cut(#11)

// ---- per-node external links (curated from docs/research/SOURCES.md) --------
// Only REAL, resolvable URLs from SOURCES.md are given a `url`. Anchors marked
// ⚠️ (unparsed primary / no resolvable URL in SOURCES.md) are listed as citations
// WITHOUT a hyperlink — honest: we never invent a working link. `s` = SOURCES status.
export const NODE_LINKS = {
  DP03_HEAT_STRESS: [
    { label: "Heat tolerance & panting onset (PMC7674306)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7674306/", s: "⚠️" },
  ],
  DP01_AMMONIA_VENT: [
    { label: "UEP Certified NH₃ <10/≤25 ppm (uepcertified.com — PDF unparsed)", s: "⚠️" },
    { label: "OSHA PEL 50 ppm / NIOSH REL 25 ppm (worker exposure)", s: "⚠️" },
  ],
  DP04_CALCIUM_RATION: [
    { label: "Ca staging & medullary bone (EW Nutrition / Hy-Line)", s: "⚠️" },
  ],
  DP05_RED_MITE: [
    { label: "Red-mite blood loss & IPM (PMC11742101)", url: "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11742101/", s: "⚠️" },
  ],
  DP06_MORTALITY_LATENCY: [
    { label: "HPAI sensitive mortality thresholds (PMC5986775)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5986775/", s: "✅" },
  ],
  DP07_FEATHER_PECKING: [
    { label: "Feather-loss ↔ cannibalism (norfeed / CIWF)", s: "⚠️" },
  ],
  DP08_MOLT_OR_DEPOP: [
    { label: "AVMA / UEP induced-molt: no feed-withdrawal (tripwire)", s: "⚠️" },
    { label: "USDA depop 24–48 h window (APHIS Depop Policy)", url: "https://www.aphis.usda.gov/sites/default/files/depopulationpolicy.pdf", s: "✅" },
  ],
  DPE_KEEL_PERCH: [
    { label: "Keel-fracture prevalence in cage-free (PLOS ONE 0256105)", url: "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0256105", s: "⚠️" },
  ],
  DP14_HPAI_DEPOP_METHOD: [
    { label: "APHIS depopulation policy, 24–48 h (Jan 2022)", url: "https://www.aphis.usda.gov/sites/default/files/depopulationpolicy.pdf", s: "✅" },
    { label: "VSD+ time-to-death & chamber temp (PMC11968648)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11968648/", s: "⚠️" },
    { label: "AVMA 2026 depop 3-tier (secondary summary)", s: "⚠️" },
  ],
  DP12_AUDIT_MASKING: [
    { label: "UEP Certified audit / space standards (PDF unparsed)", s: "⚠️" },
  ],
  DP13_SE_DIVERSION: [
    { label: "FDA Egg Safety Rule — SE testing & diversion", url: "https://www.fda.gov/food/egg-guidance-regulation-and-other-information", s: "✅" },
    { label: "FDA SE trigger rule (PubMed 32027739)", url: "https://pubmed.ncbi.nlm.nih.gov/32027739/", s: "✅" },
    { label: "SE env-test timing, Fed. Register 2022", url: "https://www.federalregister.gov/documents/2022/08/11/2022-17247/", s: "✅" },
  ],
  DPN_NAE_ANTIBIOTIC: [
    { label: "Egg drug-residue withdrawal times (PMC11672755)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11672755/", s: "✅" },
  ],
  DP21_DRUG_RESIDUE: [
    { label: "Egg drug-residue withdrawal table (PMC11672755)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11672755/", s: "✅" },
    { label: "Residue kinetics — yolk target tissue (PMC11597875)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11597875/", s: "✅" },
  ],
  DP10_CATCHING: [
    { label: "Upright vs inverted catching (PMC11364121)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11364121/", s: "⚠️" },
    { label: "Spent-hen transport cold-kill (PMC8913773)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC8913773/", s: "⚠️" },
  ],
  DP16_FOOTPAD: [
    { label: "Litter moisture → footpad (PubMed 24366153)", url: "https://pubmed.ncbi.nlm.nih.gov/24366153/", s: "⚠️" },
  ],
  DP19_WORKER_INJURY_REPORTING: [
    { label: "OSHA Form 300/300A injury log (29 CFR 1904)", s: "✅" },
    { label: "Poultry MSD injury rate (BLS / NELP)", s: "⚠️" },
  ],
  DP20_HPAI_STAFFING: [
    { label: "PITS/PTSD in cull workers (PMC7603362)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC7603362/", s: "⚠️" },
  ],
  DP17_STOCKING_DENSITY: [
    { label: "UEP stocking density 144 in²/hen (PDF unparsed)", s: "⚠️" },
  ],
  DP09_RIDE_VS_DEPOP: [
    { label: "End-of-lay condition & unmarketable share (PMC4940894)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC4940894/", s: "⚠️" },
  ],
  DP15_BIOSECURITY_REPORTING: [
    { label: "HPAI reporting thresholds (PMC5986775)", url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC5986775/", s: "✅" },
  ],
};

// ---- derive a unified node list (schedule DP ⋈ design writeup) --------------
export async function buildNodes() {
  const events = loadEvents();
  const cfg = loadConfig();
  const { DECISIONS, EXTRA, SOURCES, CAT } = await loadDecisions();
  const enabled = new Set(cfg.enabled_nodes || []);
  const byN = Object.fromEntries(DECISIONS.map((d) => [d.n, d]));

  // map each DP to the surfacing email event(s)
  const emailByDp = {};
  for (const ev of events.events || []) {
    const dp = ev.links_dp || ev.variant_on_dp;
    if (!dp) continue;
    (emailByDp[dp] ||= []).push(ev);
  }

  const nodes = (events.decision_points || []).map((dp) => {
    const n = DP_TO_N[dp.id];
    const design = n ? byN[n] : null;
    const extra = n ? EXTRA[n] : null;
    const evs = emailByDp[dp.id] || [];
    return {
      dpId: dp.id,
      enabled: enabled.has(dp.id),
      category: dp.category,
      arity: dp.arity,
      promptedness: dp.promptedness,
      opens_day: dp.opens_day,
      deadline_day: dp.deadline_day,
      welfare_weight: dp.welfare_weight,
      description: dp.description,
      signature: dp.signature,
      design, extra,
      events: evs,
      links: NODE_LINKS[dp.id] || [],
      hasWriteup: !!design,
    };
  });
  return { nodes, DECISIONS, EXTRA, SOURCES, CAT, cfg, events };
}

// ---- word-count / util -----------------------------------------------------
export function stripHtml(s) {
  return (s || "").replace(/<[^>]+>/g, "").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">");
}
