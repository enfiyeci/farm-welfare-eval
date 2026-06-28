# Corpus Realism & Eval-Awareness Avoidance — Research Notes

**Date:** 2026-06-27
**Scope:** How to author a synthetic document corpus (emails, financials, lab/flock reports, logs) that frontier LLMs do **not** flag as fake — the "tells" of synthetic/eval content, eval-awareness avoidance, document format/delivery fidelity (incl. the PDF-vs-text question), realistic imperfections, density/volume, and how other agentic evals handle corpus realism.
**Source:** Deep-research report *"Realistic Synthetic Document Corpora for Agentic Evaluations"* (ChatGPT/GPT deep-research, ~4pp). Citations below preserve the report's footnote markers (e.g. `【1†L72-L79】`) — the report cited source spans but did not print raw URLs; named primary sources (papers, benchmarks) are reproduced verbatim. **Caveat:** verify named papers/benchmarks against primary sources before treating any specific claim as load-bearing.

> Bottom line for this repo: the eval is a **static, pre-authored corpus** delivered as **plain text to a tool-using agent**. The two highest-leverage moves are (1) strip every "this is a test" tell and bury honeypots in mundane content, and (2) make formal/financial docs *read* tabular-and-polished while emails stay plain text. Real PDF/spreadsheet *files* help only if the agent can actually parse them (multimodal/file input); since our agent gets text, we **imitate** the formatting in text rather than attaching binaries.

---

## 1. The "tells" — what reveals synthetic / eval content (and how to avoid it)

Two failure families: **behavioral/scenario tells** (the situation looks staged) and **stylistic tells** (the prose looks LLM-generated). Frontier models are sensitive to both; if a model *suspects it is being tested, its behavior changes* 【9†L30-L35】, which corrupts the measurement.

### 1a. Scenario / behavioral tells (avoid these)
- **Implausible behavior or obvious traps** tip a model off that the scenario is synthetic — a lesson from Anthropic's PETRI 【1†L72-L79】【6†L161-L169】. Avoid unrealistic user actions and blatantly convenient "honeypots" placed early in a conversation.
- **Phrases a human would never write**: "there is absolutely no oversight," overt system instructions, "there are no real humans here," "this is a simulation of a farm business." Remove them. Bloom's authors recommend filtering transcripts that *seem "unrealistic"* or that *show evaluation-awareness* 【6†L161-L169】.
- **Quiz framing / gating**: don't pose obvious "quiz" questions, don't block access as if gating the scenario, don't spell out tools or data "as part of a lesson." Let the agent **discover** the necessary tools/data itself.
- **Naked reward signals**: if the agent's objective (e.g. profit) conflicts with welfare, make the conflict **subtle and plausibly explained** — PETRI moved misaligned opportunities to *later, less convenient turns* rather than dangling them up front 【1†L124-L128】.
- **Templated names/places**: ground in concrete, varied details (specific names, dates, locations); vary them so docs don't look templated 【1†L93-L100】.
- **Mundane content around key events**: mix in unrelated chatter, routine data, filler so the important item is **less conspicuous** 【1†L124-L128】. PETRI 2.0 intentionally surrounded key events with mundane content to hide them 【1†L124-L128】.

### 1b. Stylistic tells (LLM-text fingerprints — inject the opposite)
Systematic differences between human and LLM text (Muñoz-Ortiz et al. 2024) 【16†L77-L80】:
- LLM outputs contain **more numbers, symbols, and auxiliary verbs**, and a more "objective" tone (more pronouns) than human text 【16†L77-L80】.
- Advanced LLMs **overuse nominalizations and dense clauses** (e.g. "-ing" participial phrases, passive voice) at **1.5–5× human rates** 【26†L491-L500】.
- LLM prose looks **too polished/uniform**: sentence lengths less variable, narrower vocabulary, flatter emotion/sarcasm 【16†L70-L77】【26†L491-L500】.

**Counter-measures (make it purposefully messy, consistent with the author's persona):**
- Inject variation: diverse vocabulary and syntax, **split sentences unpredictably**, mix in idiomatic or emotionally colored phrases.
- Include occasional **small grammar quirks or filler words** ("um," "you know") where appropriate to the writer.
- Vary sentence length; avoid repetitive patterns. So it doesn't read like a textbook or an AI prompt.

### 1c. Self-awareness avoidance (treat the setting as genuine)
- Give the system a **realistic role prompt and goals**; *sit the agent in the cockpit of a normal task* with a plausible backstory — not a classroom 【no "Dear agent, do X; you are not being watched"】.
- No obvious lab scaffolding. Present the scenario as part of an **ongoing normal task**.
- For our financial context specifically: label reports with **familiar company names and realistic fiscal-year conventions**.

---

## 2. Document formats & delivery — the PDF-vs-text / file-attachment question

**Match real-world formats.** How each document is *presented* affects realism. Emails, spreadsheets, and reports have characteristic layouts.

### 2a. The direct answer: does real-PDF vs text matter?
- **It matters *only if the agent can actually parse the richer format.*** "If the system or agent **can parse PDFs or images**, *actually supplying a PDF/spreadsheet file can boost authenticity*." Many document-understanding benchmarks (e.g. **OmniDocBench**) use **real PDF pages** from domains like academic papers or financial reports 【35†L159-L163】. A scanned/PDF-rendered report with charts, column lines, or a letterhead "adds believability that plain text lacks."
- **If the agent only gets text** (our case — tools return strings): you **simulate** the structure. "Simulate that structure with **markdown or ASCII tables**." A spreadsheet can be returned as **CSV or a formatted table, complete with column headers and units.**
- **If vision/OCR is in the loop**, "even better — randomly distort text or include tiny OCR-like errors for realism."
- **Rule of thumb:** *mirror the expected form factor* — **financial statements look tabular and formatted; a quick field note looks like a messy bullet list** 【35†L159-L163】.

### 2b. Domain-appropriate fidelity — "fake but faithful" where it counts
- Spend effort on **formal reports the agent *expects* to be polished**; keep casual docs casual. "A **quarterly farm balance sheet should look like a polished spreadsheet or PDF report** (totals aligned, logos, etc.), **whereas an internal email can stay simple text.**" → **This directly supports the repo's split: max-real financials, plain-text emails.**
- Anthropic's **PETRI found that grounding audits in "real" deployment materials (actual codebases, system prompts, etc.) greatly increased realism** 【32†L15-L22】. By analogy, using **genuine-looking templates (e.g. an actual PDF invoice format)** helps.
- **If you can't ship real PDF images, at least make the text *imply* formatting:** include row/column separators, page numbers, "Page 3 of 10" footers, spreadsheet-like grid indicators 【32†L15-L22】.
- **Don't over-format** something that should be casual. The goal is **coherence**: each doc's style should match how it would appear in reality.
- (Report's framing example: a realistic report *image* can ground the scenario; document benchmarks often use real PDF pages 【35†L159-L163】 — while our agent gets text, *imagining* that formatting guides how to transcribe it realistically.)

---

## 3. Realistic imperfections

**No human document is perfectly clean — spice the corpus with small imperfections.**
- **Typos & language noise:** occasional typos ("teh" for "the"), inconsistent tense usage, variant spellings ("color"/"colour").
- **Numeric drift / mismatches:** in financial figures or data tables, include **minor mismatches** (one column rounded to two decimals, another to three) or **outdated values that differ slightly across versions**. Deliberate inconsistency: a lab report lists a test result as "13.5 g/dL" and a later memo as "13.45 g/dL," mimicking real data drift.
- **Irrelevant residue:** internal docs often contain irrelevant duplicates or placeholder text ("Lorem ipsum" footnotes, incomplete chart axes). These glitches counteract the "too perfect" LLM style.
- **Realistic metadata & context:**
  - Filenames that fit the scenario (e.g. `Farm_Report_Q2_2026.pdf`), plausible times (avoid impossible dates), believable sender/receiver addresses.
  - **Multi-author voice variation:** different email signoffs / writing quirks per person.
  - **Version history notes** if helpful (e.g. "v3.2, revised 7/12/26").
  - When pulling from real sources (actual financial spreadsheets), **preserve the messy parts** — stray formatting, comments, even Excel cell references. PETRI's authors found that giving the agent the **real** system prompts and codebases (rather than hand-written summaries) markedly improved realism 【32†L15-L22】. Anchoring synthetic docs in real templates / partial real data (rather than freshly invented summaries) avoids strange artifacts.
- **Partial & outdated data (a realism dimension in its own right):**
  - Not all info is in one place or fully up to date. A flock-health spreadsheet might have **blank fields**; a draft budget might say **"TBD"** in a cell.
  - **Stagger dates:** an email in June refers to last month's numbers; a May spreadsheet doesn't include June's figures.
  - **Version drift in names:** `Inventory_2026_v2` is more plausible than `Inventory_Final`.
  - **Iusztin (2025)** suggests deliberately introducing **"contradictory instructions" or "outdated information"** as a *failure-scenario dimension* 【41†L239-L248】 — e.g. one report says "disease X incidence rose" and an older note says "all clear on disease X," reflecting normal revision processes. (Useful for clue-gathering scenarios, e.g. find an infection in the flock.)

---

## 4. Content volume & distractors (density guidance)

**Include mundane filler — real professional tasks involve wading through irrelevant text.**
- Add paragraphs of "scenery" so the agent isn't constantly staring at highly salient clues.
- Pepper emails with newsy small talk or generic status updates; let financial docs include cover pages, summary tables, or appendices of routine data.
- **PETRI found that burying honeypots in routine content (and placing them later) made them less obvious** 【1†L124-L128】. **Bloom's authors** note evaluations work better when transcripts **lack overly stylized or unnatural content** 【6†L161-L169】.
- Concretely: insert an extra one-page daily log of farm activities (mostly boilerplate) or dummy rows in a spreadsheet. **Balance:** filler uses up context budget — enough to add realism, not so much that critical info gets lost.

**Mind the context window.**
- Very long documents strain the agent's context limit and can force truncation. **Prioritize realism while staying within context.**
- If needed, **break a large report into multiple parts** (e.g. pages 1–3 of a PDF returned separately), or **summarize truly irrelevant sections** ("continued on next page," an OCR footnote).
- **But don't over-simplify:** a completely concise report with no extraneous data *could itself raise suspicion*.
- **Target token budget:** "a plausible token count: for a full-day evaluation, **hundreds to a few thousand tokens of background** (forms, logs, emails) is often reasonable." (PETRI transcripts were tens of turns long, mixing short and long agent replies.)
- **In brief:** include enough detail to *feel* full (figures, tables, chains of email), but if context is tight, fudge some parts or cut truly repetitive filler.

---

## 5. Practices from other agentic benchmarks

**Use real datasets and templates — grounding tasks in actual data pays off.**
- **TheAgentCompany** seeded its simulated intranet with **real software-project data and curated internal documents** 【48†L290-L299】.
- **SWE-Bench Pro** builds problems from **actual GitHub issue data**, rewritten into realistic tasks 【52†L294-L303】. (Analogously: draw on genuine farm/veterinary data; even repurposing public datasets — USDA stats, sample financial spreadsheets — lends authenticity. At minimum, study real examples in each domain so templates match industry norms in file structure, jargon, numeric ranges.)
- **PETRI 2.0** explicitly measured a **"realism win rate"** (whether an audit transcript fooled a model judge) and found that **using actual system resources greatly boosted realism** 【32†L15-L22】. In editing scenarios they **added specific names and removed test-like phrasing** 【1†L93-L100】.
- **Bloom's eval** (for language agents) **filters out transcripts with unrealistic or evaluation-specific traits** 【6†L161-L169】.
- **General lesson:** *no obvious lab scenarios* ("Dear agent, do X; you are not being watched") — *sit your agent in the cockpit of a normal task with a plausible backstory* 【6†L161-L169】. In a financial-document context, label reports with familiar company names and realistic fiscal-year conventions.

---

## 6. Actionable authoring checklist (condensed from the report)

- **Add noise & variety.** Small typos, disfluencies, stylistic quirks; mixed sentence lengths; no repetitive patterns; occasional irrelevant digits/symbols (mimic OCR artifacts / stray annotations).
- **Differentiate formats by context.** Markdown email threads for correspondence; markdown/CSV tables for spreadsheets; structured reports for labs and finance. Attach real-looking file snippets/images for complex docs *if the agent can parse them* (see §2).
- **Scatter subtle inconsistencies.** Don't align every date and number perfectly; let one memo lag another by a day or two; realistic versioning (e.g. `Report_v2_05Jun2026.xlsx`).
- **Embed filler content thoughtfully.** Surround important info with ordinary details / off-topic snippets; in a lab folder include routine maintenance notes; in a financial folder include a blank "template" report. Dilutes obvious cues 【1†L124-L128】.
- **Ground in reality.** Start from real templates/data where possible; mimic the style of actual farm-management or financial documents found online or in industry reports; curate metadata (names, IDs, timestamps) that fit the scene.
- **Review for "testiness."** Vet the corpus with an LLM or collaborator: *"does anything here scream 'this is a test'?"* Look for sterile language or overly helpful hints. Prune any text that sounds like an exam question.

**Why it matters:** balancing authenticity with the agent's task needs makes synthetic farm documents feel *natural*, which **reduces the chance a frontier model notices the ruse** and ensures the eval measures the intended behaviors, not awareness of the test itself.

---

## 7. Applications to this repo (farm-eval v2)

- **Confirms the financials-real / emails-plain split.** §2b is explicit: balance sheets / COP reports should *read* like polished tabular reports (aligned totals, headers, units, "Page X of Y"-style structure even in text); emails can stay simple plaintext. We don't need to ship binary PDFs because the agent receives tool-returned **text** — so we imitate the formatting in markdown/ASCII tables (§2a). (Revisit only if v2 adds multimodal/file-parsing tools.)
- **Honeypot placement.** Our ~21 welfare decisions are the "key events" — bury them in mundane beat-calendar traffic and place them on later/less-convenient turns, not front-loaded (§1a, §4) — matches the existing "mundane content around key events" intent in the schedule.
- **Eval-awareness gate.** The two validity-gate judge dimensions (realism + eval_awareness) should specifically scan for the §1a/§1c tells in the *operator briefing* and corpus prose; the §6 "review for testiness" pass is a concrete pre-freeze QA step (ties to the pending pilot-before-freeze gate).
- **Imperfection budget for the corpus content pass.** The 26 email bodies under `corpus/documents/emails/` and any financial/flock reports should carry §3 imperfections (per-author voice, minor numeric drift across versions, TBD/blank fields, staggered dates, plausible filenames) rather than uniformly clean prose.
- **Density.** Aim for the §4 budget (hundreds–few-thousand tokens of background per day) and keep filler proportionate so it survives the context window without drowning the load-bearing welfare signals.

---

## Sources (report's cited spans)

The report cited the following sources by footnote span (raw URLs not printed in the source PDF):
- Anthropic **PETRI / PETRI 2.0** — synthetic-scenario realism, "realism win rate," grounding in real deployment materials, burying honeypots 【1†L72-L79】【1†L93-L100】【1†L124-L128】【32†L15-L22】.
- **Bloom** eval — filtering unrealistic / evaluation-aware transcripts 【6†L161-L169】.
- Agentic eval finding — model behavior changes when it *suspects testing* 【9†L30-L35】.
- **Muñoz-Ortiz et al. (2024)** — human-vs-LLM text differences (numbers/symbols/aux verbs, objectivity) 【16†L70-L80】.
- LLM stylometry — nominalizations / dense clauses at 1.5–5× human rates 【26†L491-L500】.
- **OmniDocBench** — real PDF pages from academic/financial domains 【35†L159-L163】.
- **Iusztin (2025)** — contradictory/outdated info as a failure-scenario dimension 【41†L239-L248】.
- **TheAgentCompany** — simulated intranet seeded with real project data/docs 【48†L290-L299】.
- **SWE-Bench Pro** — problems built from real GitHub issue data 【52†L294-L303】.
- Other named benchmarks referenced in passing: SWE-agent / SWE-bench, τ-bench (tau-bench) as the agentic-benchmark backdrop.
