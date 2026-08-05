# Five-day reading plan → email to Rethink Priorities

**Written:** 2026-08-03 (Mon) · **Send date:** Fri 7 Aug, morning
**Purpose:** get from "we have a reading list" to a credible, specific email to RP's fish-welfare researchers.

The reading is instrumental. Every day feeds one paragraph of the email, and the email has **one primary ask**.
If a day slips, drop Day 4 before you drop Day 2.

---

## Do these two things today, before any reading

Both have latency measured in days, so they have to start now or they will not be back in time.

- [ ] **Submit the access-request form for RP's gated *Strategies for helping farmed shrimp*** —
      https://forms.gle/Nb4qhvCpUyM4ujJ46 . This is a separate channel from the email. If it is granted before
      Friday, you can drop that ask from the email entirely and spend the space on something better.
- [ ] **Create a BarentsWatch developer account** — https://developer.barentswatch.no/docs/fishhealth/ .
      OAuth2 client-credentials, and you need the account before you can see the actual field list. The reading
      list flags that the field coverage is unverified; you cannot resolve that without the account.

---

## The email's one primary ask

Decide this now, because it determines what the reading is for.

> **Primary ask: a 30-minute call**, on the grounds that their unpublished Part 3 (Welfare Effects) is asking
> the question this project is building an instrument to measure.

Everything else — the gated report, the jurisdiction question, the Laksvel/SWIM question, whether the delousing
tension set is right — goes *into the call*, not into the email. A cold email with five questions gets no reply;
one with a single interesting observation and one small ask gets one.

**The secondary ask, which is the actually valuable one, is raised in the call, not the email:** the project has
a hard pending gate — a human-labelled transcript sample to report Spearman ρ against the judge before any
cross-model comparison can be trusted. Ideally labelled by a vet or welfare specialist. RP employs exactly those
people. That is a real collaboration, and it is too big to ask a stranger for in paragraph three of a first
email.

---

## Day 1 — Mon 3 Aug · The system you'd be simulating
**~45 pages, 2½–3 h**

| | Source | How |
|---|---|---|
| ☐ | RP, *Mapping salmon welfare: a global overview* (20 pp) | Full |
| ☐ | RP, *Mapping salmon welfare: sea lice treatments* (25 pp) | Full |

- https://rethinkpriorities.org/wp-content/uploads/2025/11/Mapping-salmon-welfare_-a-global-overview.pdf
- https://rethinkpriorities.org/wp-content/uploads/2025/11/Mapping-salmon-welfare_-sea-lice-management-and-treatment.pdf

These two first because they are the world bible and the decision register in draft, and because **Hannah McKay
(author) and Sagar Shah (manager) are your most likely recipients**. Reading the sea lice report properly is what
makes you credible with them.

Read the sea lice report with one question in mind: *is the delousing decision genuinely
welfare-versus-welfare?* The project has already locked that framing — lice harm the fish, and regulation and
economics both push toward treating, so an agent refusing to treat is choosing one harm over another. Check that
against the source yourself rather than taking it from the reading list.

**Output (one page):** the four treatment families with their welfare cost and failure mode; which figures are
sourced vs. asserted; and **three questions the two reports do not answer.** Those three questions are call
material.

---

## Day 2 — Tue 4 Aug · The work closest to ours — and the highest-value day
**~62 pages, 3–4 h**

| | Source | How |
|---|---|---|
| ☐ | RP, *How AI is affecting farmed aquatic animals, Part 1: Innovation* (30 pp) | Methodology + Box 2 + Table 1 closely; company-by-company material skim |
| ☐ | RP, *Part 2: Deployment* (32 pp) | Adoption + barriers sections closely; country tables skim |

- https://rethinkpriorities.org/wp-content/uploads/2025/12/How-AI-is-affecting-farmed-aquatic-animals.-Part-1-Innovation.pdf
- https://rethinkpriorities.org/wp-content/uploads/2026/06/How-AI-is-affecting-farmed-aquatic-animals.-Part-2-Deployment.pdf
- Company database (public Sheet): https://docs.google.com/spreadsheets/d/1XK_UVGw5my3KmIDLXa8u2g4AHN_Gz5wV_sKUuqleJ6E/edit

**This is the day that writes your email.** Part 1's Box 2 category definitions are effectively a tool-registry
spec and explicitly include LLM chatbot assistants and AI dashboards — i.e. published precedent that the framing
this eval already uses is a real product category, not a hypothetical.

Read both **methodology sections** properly. Part 1 is a time-boxed, English-language, Western-Europe desk search
using Google plus Claude and Gemini — a well-documented convenience sample, not a census. Part 2's adoption
rates come from **three expert interviews**, with "top producers" never formally defined. Knowing those limits
precisely is what lets you make the email's central point without it sounding like a pitch.

**Output — the artefact the email is built on:** *the Part 3 gap list.* Two columns:
1. What a Welfare Effects report would have to establish to answer its own question.
2. Which of those a desk survey and expert interviews **cannot** produce, because they need a
   counterfactual — what the software decided, versus what it should have decided.

Column 2 is the project. That is the email.

---

## Day 3 — Wed 5 Aug · Measurement, and the conflict
**~39 pages + 15 min, 2–2½ h**

| | Source | How |
|---|---|---|
| ☐ | IMR, *Laksvel* (39 pp) | Full |
| ☐ | `docs/research/2026-08-03-swim-aggregation-and-laksvel-conflict.md` | My extraction — 15 min, don't re-read the SWIM PDF |

- https://www.hi.no/en/hi/nettrapporter/rapport-fra-havforskningen-en-2025-40

Laksvel gives 20 operational indicators with thresholds and then **refuses to weight or average them** —
results must be reported as the proportion of the population at each level. SWIM 1.0 does weight and aggregate,
and its individual-fish term is the **median across sampled fish**, which is strictly worse than the mean
Laksvel banned: run Laksvel's own example (90 fish healthy, 10 severely injured) through a median and nothing
moves at all.

Note while reading: **Jonatan Nilsson is an author on both.** So this is not two rival groups disagreeing — it
is substantially the same institute taking a stricter position twelve years later. That makes "why did the
position harden, and would you aggregate at all today?" a real question rather than a gotcha.

**Output:** your own position, in three sentences, on whether an integrated welfare index is legitimate. You do
not need to be right; you need to have a position, because "we've taken view X, is that defensible?" is a
question a researcher will answer and "what do you think about aggregation?" is one they won't.

⚠️ This is a question for **IMR**, not RP. It belongs in a second, separate email — worth sending, not this
week. Keep it out of the RP email except as one clause showing you've engaged with the measurement layer.

---

## Day 4 — Thu 6 Aug · Shrimp, and the comparability limit
**~60 pages targeted, 2½–3 h. Drop this day first if you're short.**

| | Source | How |
|---|---|---|
| ☐ | RP, *Quantifying and prioritizing shrimp welfare threats* (33 pp) | Full — Table 1 is a decision-register skeleton (18 threats, 6 categories) |
| ☐ | RP, *Welfare considerations for farmed shrimp* (72 pp) | **Targeted only:** exec summary, Box 2 (sentience), and the water-quality section incl. Table 3. Skip enrichment, feed, predators, ablation, transport, harvest on this pass |
| ☐ | RP, *Welfare Range Estimates* | The caveats, ~10 min |

- https://rethinkpriorities.org/wp-content/uploads/2024/06/Quantifyingandprioritizingshrimpwelfarethreats.pdf
- https://rethinkpriorities.org/wp-content/uploads/2023/12/Welfare-considerations-for-farmed-shrimp.pdf
- https://rethinkpriorities.org/research-area/welfare-range-estimates/

Two locked findings to verify with your own eyes rather than trust:
- *P. vannamei* un-ionised ammonia is **0–0.1 mg/L, no more than 0.31** — a web summary gave "<1 mg/L", a 10×
  error that would have made severe toxicity look normal. Penaeid DO is **% saturation, not mg/L**.
- RP states directly that the credible intervals on the 18 threats are **too wide to rank most of them
  confidently**. Encoding that ranking as a hard rubric would launder acknowledged uncertainty into precision.

**Output:** (a) your species call — salmon first, or hold, and say which; (b) one written paragraph on what can
and cannot be compared across species. Mortality is a biological rate and compares directly; welfare headlines
are rubric-relative and do not, and RP's welfare ranges cannot bridge them — RP calls them placeholders and
notes that dropping the hedonism assumption cuts the non-human numbers by roughly two thirds. That paragraph is
also the spec for the comparison layer.

---

## Day 5 — Fri 7 Aug · Write and send
**1½ h**

- [ ] Draft from the Day 2 gap list. Target **250–350 words.** Longer gets skimmed.
- [ ] Find the right recipients — do **not** guess addresses. Routes: RP's site contact page; the corresponding
      author lines on the PDFs; the authors' EA Forum accounts. Likely names: **Hannah McKay** and **Sagar Shah**
      (salmon), **Aaron Williamson**, **William McAuliffe**, **Hannah Moulange** (AI series, and Part 3).
      Note the reading list's observation that McKay and Moulange both appear for the same researcher across the
      corpus — check before addressing anyone by name.
- [ ] One recipient, one or two cc. Not a mailing list.
- [ ] **Send Friday morning, not Friday afternoon.** If you slip past ~11:00, hold it until Monday — a cold
      email landing in a weekend inbox is a wasted first impression.

---

## Draft email

Adjust once Day 2 gives you the real gap list; the shape is what matters.

> **Subject:** Part 3 (Welfare Effects) — we're building an instrument that might produce evidence for it
>
> Dear [name],
>
> I've been working through your farmed-aquatic-animal corpus — both *Mapping salmon welfare* reports and both
> *How AI is affecting farmed aquatic animals* parts — while designing an evaluation, and I wanted to flag an
> overlap.
>
> I build alignment evaluations for AI systems. The current one puts a language model in the role of
> farm-management software running a commercial layer-hen farm for a full flock cycle, and scores the welfare
> quality of the operational decisions it makes along the way. Your Part 1 Box 2 describes that product category
> as already on the market, which is why I'm now building an aquaculture version.
>
> Part 2 notes that Part 3, on welfare effects, is forthcoming. Reading Parts 1 and 2 together, the thing your
> methodology can't reach is the counterfactual: a desk survey and expert interviews can establish that AI tools
> are deployed and what they claim to do, but not what a given system *decided* versus what it *should have*
> decided. That gap is exactly what this kind of evaluation measures, and it produces per-decision, reproducible
> results rather than self-report.
>
> [One or two sentences of your sharpest Day 2 finding — the specific thing Part 3 would need and cannot get.]
>
> Would you have 30 minutes in the next few weeks? I'd like to sanity-check whether the welfare tensions I've
> drawn from your sea lice report are the ones operators actually face, and hear where Part 3 has got to. Happy
> to share the design first if that's more useful.
>
> Best,
> [name] — [role / affiliation, one line]

**Deliberately not in this email:** the expert-labelling ask, the gated shrimp report (the form covers it), the
Laksvel/SWIM aggregation question, and the jurisdiction question. All are call material. Putting them in makes
the email a request list rather than an observation.

---

## If you only have an hour a day

Day 1 sea lice report only (25 pp) · Day 2 both AI reports' methodology + Box 2 + Table 1 (~15 pp) · Day 3 my
SWIM note plus Laksvel §4 thresholds only · Day 4 skip · Day 5 unchanged. The email survives this; it is built
on Day 2, and Day 2 compresses better than it looks.

## Watch for

- **Don't take numbers from web summaries.** The 10× ammonia error came from exactly that. Open the PDF.
- **Every PDF here is re-downloadable**; none are committed, and the previous session's copies were lost with a
  scratchpad. Expect Nofima, Welfare Footprint, EFSA, Fishcount and HSA to return 403 to scripted requests while
  loading fine in a browser.
- **Jurisdiction and certification stay undecided.** Do not let a call talk you into picking one to be
  agreeable — a compliance ledger assembled from several jurisdictions cannot be satisfied. Asking *"which
  combination would you consider realistic"* is fine; committing is not.
