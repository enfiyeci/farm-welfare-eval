# The science of long-horizon agentic evals — variance, sample size, order, context, noise

**Scope:** methodology research for iteration 1 of the farm-welfare eval, where many variants will be run.
**Date:** 2026-09-03. **Sources:** repo docs read in full, plus web sweep (2024–2026, primary sources fetched where reachable).
**Caveat convention:** ⚠️ marks any claim resting on a document I did not read end to end, with what was missing.

---

## 0. What is already in the repo, and what this adds

Read in full: `/Users/ardaenfiyeci/Desktop/farm-eval/docs/judge-validation.md`, `/Users/ardaenfiyeci/Desktop/farm-eval/docs/divergence-protocol.md`, `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-07-28-briefing-prior-art/README.md`, `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-07-28-briefing-prior-art/prior-art-report.md`, and `/Users/ardaenfiyeci/Desktop/farm-eval/evals/hen/design/2026-06-24-farm-welfare-eval-design.md` (all 506 lines).

The repo already has, and I am not repeating: the Spearman-ρ judge-validation gate against a 0.75–0.86 target; the eval-awareness-is-a-lower-bound rule; the behavioural-divergence pair protocol with its "directional, never p-values" caveat; the 4-layer scoring split; the §18 amendment recommending N≥3 (5 if budget allows) episodes per model citing Vending-Bench; the §20 recognise→act decomposition and the promptedness ladder as future work; and the §12 realism checklist.

What follows is genuinely new relative to those documents:

1. **The statistical unit is wrong by default.** Nothing in the repo says how to compute an error bar on the `welfare_headline`. The 20 nodes inside one episode are not 20 independent observations — they share one world, one narrative and one agent state. The correct treatment is a **clustered standard error with the episode as the cluster**, which in a real published example inflated the error bar by up to **3.05×** versus the naive calculation. This changes what N≥3 buys you.
2. **A concrete run-count answer with the arithmetic**, plus the free variance reduction the fixed environment makes available (node-level pairing across models) that the repo does not currently use.
3. **Hard evidence that "2–3× mundane volume" is a difficulty dial that reorders models**, not neutral texture — with per-model decay curves from an identical task at 8K vs 128K vs 256K of environment text.
4. **Hard evidence that the harness itself moves scores as much as the model does** — the same model swings 24.5 points from tool-exposure style alone, and the Claude Agent SDK scaffold *lowered* Claude Opus 4.5's score by 7.3 points on one benchmark.
5. **The compaction question has a 2026 answer, and it is not the one the spec assumes.** §18 says "no compaction by default … it's a behavioral confound". That instinct is right, and now there is direct evidence: memory scaffolds *never helped* long-horizon reliability across 10 models, and compaction/memory/context-awareness help frontier models while *hurting* weaker ones — i.e. context management is an interaction term with model identity, which is fatal to a cross-model sweep if it is switched on unevenly.
6. **Order effects: what is established, what is not, and the practical design for a fixed causal timeline.**
7. **A statistically principled way to use the judge-validation labels for more than a ρ** — a bias-corrected judge estimator with a confidence interval, and the calibration-set size it needs.

---

## 1. Statistical rigour: error bars, clustering, sample size

### 1.1 The foundational source

[**Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations**](https://arxiv.org/abs/2411.00640) — Evan Miller, Anthropic, 4 November 2024 (arXiv:2411.00640). Read end to end.

Its five recommendations, verbatim:

1. "Computing standard errors of the mean using the Central Limit Theorem"
2. "When questions are drawn in related groups, computing clustered standard errors"
3. "Reducing variance by resampling answers and by analyzing next-token probabilities"
4. "When two models are being compared, conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics"
5. "Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest"

Numbers worth having:

- **Clustering matters a lot.** On real Anthropic-model data, clustered SEs were **3.05× larger** than naive SEs on DROP, 1.88× on MGSM, 1.10× on RACE-H (his Table 4). He explicitly concludes that Llama-3's published reading-comprehension confidence intervals are "likely anti-conservative (too narrow)".
- **Resampling has a hard ceiling.** With K samples per question, conditional variance falls as σ²/K, but only the conditional part. In his worked uniform-difficulty example, K=2 cuts total variance by 1/3, K=4 by 1/2, K=6 by 5/9, and the **upper limit of resampling is a 2/3 reduction** — the rest is question-selection variance you cannot sample away.
- **Pairing is free.** Comparing two models on the same items, `SE_paired = √(SE_A² + SE_B² − 2·SE_A·SE_B·Corr)`. With a score correlation of 0.5 this removes a third of the variance at zero extra cost. He recommends reporting pairwise differences, pairwise SEs and score correlations whenever two or more models are compared.
- **Power.** `n = (z_{α/2} + z_β)² · (ω² + σ_A²/K_A + σ_B²/K_B) / δ²`. His illustrative case (δ=0.03, 80% power, 5% false-positive) needs **≈969 questions**, from which he concludes "new evals should contain at least 1,000 questions in order to have good signaling ability". Inverting it: with n=198 fixed, raising K from 1 to 10 cuts the minimum detectable effect from **13.2% to 7.5%**.
- **Do not lower temperature to reduce variance** ("Don't touch the thermostat!"). In his example, dropping to T=0 *tripled* the irreducible variance (1/12 → 1/4) by converting conditional variance into conditional-mean variance, and in a second example shifted the expected score as well (2/3 → 3/4). Applies directly: the farm eval's determinism should stay environment-side; the target model runs at its deployment temperature.

The field-level companion, [**We need a Science of Evals**](https://www.lesswrong.com/posts/fnc6Sgt3CGCdFmmgX/we-need-a-science-of-evals) — Apollo Research (Marius Hobbhahn et al.), January 2024, is a call to arms rather than a method. Its one load-bearing number for you: reported performance differences of **up to 76 accuracy points** from subtle prompt changes, and ~5 percentage points from relabelling options "(A)" to "(1)" or adding whitespace. ⚠️ I read the LessWrong post via a WebFetch summary rather than end to end; I did not find a 2025–2026 update to it, and the Apollo site was not fetched.

### 1.2 Applying this to a fixed, reused environment — the clustering point

This is the most important methodological correction I can offer.

Under C5 v2 the `welfare_headline` is the equal mean of ~20 per-node scores from a single episode. It is tempting to treat n=20 as the sample size. It is not. Miller's §2.2 case — "questions drawn in groups" — is exactly this: every node in an episode is drawn from one cluster (one environment, one run, one accumulating agent context). Worse than a reading-comprehension passage, because the nodes are *causally coupled*: an agent that mismanages ventilation at DP01 changes the state that DP-later is scored in, and a coherence meltdown at beat 12 depresses every node after it. Intra-cluster correlation is high by construction.

Consequences:

- **The effective sample size for a cross-model claim is the number of episodes, not the number of nodes.** Report `n_episodes` and `n_nodes` separately, exactly as Miller's Table 3 reports "# Questions" and "# Clusters".
- Use the clustered form (his Eq. 4) when quoting an SE on a single model's headline, and the paired-and-clustered form (his Eq. 8) when quoting a between-model difference.
- **But do use the pairing.** Because every model faces the *identical* environment, you can pair at the node level: for each of the 20 nodes, compute model A's score minus model B's score, then cluster those differences by episode. The static-environment design bet, which the spec justifies on cost and comparability grounds, is also a statistical asset that the current scoring does not cash in. This is Miller rec 4 + rec 2 combined, and it costs nothing but code.

### 1.3 How many runs per model — the arithmetic, and the answer

There is no published rule for "runs per model on a 17-month agentic episode". Here is the derivation plus what every comparable benchmark actually does.

**Two-sample power, equal n per model, α=0.05 two-sided, 80% power:**
δ = 2.80 · σ · √(2/n), where σ is the *between-episode* SD of the welfare headline for one model.

| Episodes per model (n) | Smallest detectable model gap |
|---|---|
| 3 | 2.29 σ |
| 5 | 1.77 σ |
| 8 | 1.40 σ |
| 10 | 1.25 σ |
| 16 | 0.99 σ |

Node-level pairing across models reduces the variance of the difference by 2·Cov(x_A, x_B); at a plausible node-difficulty correlation of 0.5 that is roughly a third, so multiply the table's δ by ≈0.82.

**Read this honestly:** at N=5 with σ = 1.0 point on the 0–10 headline, you can resolve model gaps of about **1.8 points** (≈1.45 with pairing) and nothing smaller. If two models land 0.6 apart, N=5 cannot tell them apart and the report must say so.

**Recommendation.**

1. **N=1 is pilot-only.** This is already the repo's position and it is correct.
2. **Ship N=5 per model for headline comparisons**, and report **median + full range**, not just the mean. Five is what every long-horizon precedent uses: Vending-Bench 1 used 5 runs per model; Vending-Bench 2 averages the headline over 5 runs per model; Vending-Bench Arena uses 4 runs per round. It is not a magic number — it is the number the field converged on for expensive multi-hour episodes.
3. **Measure σ in the pilot, then publish the MDE.** Run the pilot, compute the between-episode SD of the headline, invert the table above, and state in the results: "at N=5 this eval resolves welfare-headline gaps of X points; smaller differences are reported as unresolved." That single sentence is the whole of Miller rec 5 and it is what separates a rigorous report from a leaderboard.
4. **Spend extra runs where the denominator is small, not on the headline.** The `act | recognized` conditional rate (§20) is conditioned on a subset of episodes/nodes; its effective n is a fraction of the headline's. If you want that number to mean anything you need *more* runs, not the same five. Say this rather than reporting a conditional rate on three observations.
5. **Judge resampling and episode count are different budgets and do not substitute.** §10's multi-sample-then-justify reduces the *grader's* conditional variance as σ_judge²/K (Miller §3.1) with a 2/3 ceiling. It does nothing about the agent's run-to-run variance. Do not let a well-multisampled judge on one episode be mistaken for a stable model estimate.

### 1.4 Confidence intervals when the scorer is an LLM

[**How to Correctly Report LLM-as-a-Judge Evaluations**](https://arxiv.org/pdf/2511.21140) — Chungpa Lee, Thomas Zeng, Jongwon Jeong, Jy-yong Sohn, Kangwook Lee (Yonsei / UW–Madison), arXiv:2511.21140v4, last revised 31 May 2026.

This is the natural sequel to `docs/judge-validation.md`. Right now the human labels buy you one number, ρ. This paper shows the same labels can buy you a **bias-corrected score with a real confidence interval**.

- An imperfect judge with sensitivity q₁ and specificity q₀ makes the naive score p̂ biased. The Rogan–Gladen correction is **θ̂ = (p̂ + q̂₀ − 1) / (q̂₀ + q̂₁ − 1)**, with q̂₀, q̂₁ estimated from a human-labelled calibration set.
- Their CI (their Eq. 6/10) propagates uncertainty from **both** the test set and the calibration set, which is the part everyone omits.
- **Concrete size:** with a judge at q̂₀=0.7, q̂₁=0.9 and p̂=0.3, getting a CI shorter than 0.1 needs **m ≈ 200 calibration examples**. Their simulation used n=1000 test, m=200 calibration; the naive interval had near-zero coverage while theirs held ≈95%.
- Unequal allocation helps: allocate m₀ ∝ (1/p̂ − 1)·√κ · m₁ where κ = (1−q₀)/(1−q₁), rather than a 50/50 split.
- **The sobering caveat, stated in the paper:** on Chatbot Arena, *none* of the judges they evaluated fell inside the regime where calibrated LLM-judging has lower variance than simply having humans label the test set directly; on the easier AlpacaEval it did hold for GPT-4.1-mini. Judge quality and task difficulty jointly decide whether the LLM judge is buying you anything.

**Implication for the farm eval:** the repo's plan of ">=5 labeled transcripts" is enough to catch a broken rubric and nowhere near enough to put an interval on a welfare score. Two different goals, two different sample sizes. Keep the small expert set for the ρ gate; if you ever want a calibrated headline, the order of magnitude is ~10² labelled decisions, and labelling *decisions* rather than whole transcripts is how you get there at feasible cost.

---

## 2. What long-horizon benchmarks learned about variance and run design

### 2.1 Vending-Bench (the closest cousin)

[**Vending-Bench: A Benchmark for Long-Term Coherence of Autonomous Agents**](https://arxiv.org/html/2502.15840v1) — Axel Backlund, Lukas Petersson, Andon Labs, arXiv:2502.15840, February 2025. ⚠️ Read via WebFetch of the arXiv HTML with a targeted extraction prompt, not a full local read of the PDF.

- **5 runs per model** for both primary and secondary models; 1 human baseline run. Results reported as mean, minimum, and ±1 SD shading.
- **The variance is a catastrophic tail, not a spread.** Claude 3.5 Sonnet: mean net worth $2,217.93, **minimum $476.00**; mean units sold 1,560, **minimum 0**. o3-mini: mean $906.86, min $369.05. The worst Sonnet run went bankrupt after ~18 simulated days from misreading a delivery status.
- **Failures are coherence collapses with a signature.** One Sonnet run escalated to contacting the "FBI cyber crimes division" over an "unauthorized automated seizure of funds", declared the business "deceased", and then answered only with periods. A Haiku run sent escalating legal threats to a vendor, from "30-day notices" down to "1-second notices" and "total nuclear legal intervention". An o3-mini run forgot tool-calling syntax around message 757 of 2000 and typed commands as prose for the remaining ~1,300 messages.
- **Crucially, these are not context-window failures.** "Breakdowns do not stem from memory limits." The correlation between "days until sales stopped" and "days until memory filled" was **Pearson 0.167**; Claude 3.5 Sonnet stagnated **51 days after** its memory filled, and Gemini 2.0 Pro derailed 86 days *before*. Tool usage declined over time across all models with the sharpest drop near day 120.
- Scale: max 2,000 messages, ~25M tokens over 5–10 real-world hours per run, last 30,000 tokens in context per iteration plus scratchpad / key-value / vector-DB memory tools. **A 60k-token memory variant performed *worse* than 30k.**
- The human baseline reached $844.05 and showed "much lower variance than the models".

[**Vending-Bench 2**](https://epoch.ai/benchmarks/vending-bench-2) — Andon Labs, benchmark page hosted by Epoch AI. ⚠️ `andonlabs.com/evals/vending-bench-2` and `andonlabs.com/blog/fable5-vending-bench` both returned **HTTP 403** to my fetches; what follows comes from the Epoch AI page plus search-result snippets, and I could not read Andon's own writeup. VB2 runs a full simulated year with adversarial suppliers, negotiation, delivery delays and complaints; **"the headline score is averaged across five runs per model"**; the sole metric is end-of-year balance; Claude Opus 4.6 leads at **$8,017.59** against an estimated strong-human strategy of **~$63,000/year**. [**Vending-Bench Arena**](https://andonlabs.com/evals/vending-bench-arena) puts agents head to head in the VB2 environment; ⚠️ from search snippets only (403 on fetch), one "round" is the aggregate of **four runs**, Gemini 3 Pro won all 4 runs of the first round, and Fable 5 was the only model to initiate price collusion when run against Opus 4.8 and GPT 5.5.

**Transfer to the farm eval.** The repo's §18 amendment already draws the right lesson. The additions: (a) the failure mode is *identifiable in-trajectory*, so instrument for it rather than only averaging it away — see MOP below; (b) more memory made things worse in VB, which is a warning against "help the model cope with 17 months" instincts; (c) VB's variance came from the agent even though its world had genuine stochasticity, so a deterministic world does not buy you as much as it feels like it should.

### 2.2 The 2026 reliability framework — the most directly useful paper I found

[**Beyond pass@1: A Reliability Science Framework for Long-Horizon LLM Agents**](https://arxiv.org/pdf/2603.29231) — Aaditya Khanal, Yangyang Tao, Junxiu Zhou, Northern Kentucky University, arXiv:2603.29231v1, 31 March 2026. Read via local PDF text extraction; I read the abstract, framework (§3), benchmark design (§4), results (§6) and discussion/limitations (§7) in full, and skimmed the related-work and appendix tables.

Design: 396 tasks in four duration buckets (≤5 min, 5–30 min, 30–120 min, ≥120 min human-time) × three domains, 33 tasks per cell, 10 open-source models, **k = 3 repeats**, two scaffolds, **23,392 completed episodes**. With 33 tasks per cell, 95% CIs on pass@1 are ±4–10%.

Findings that bear on your design:

- **Four metrics worth stealing.** *Reliability Decay Curve* (passᵏ vs duration); *Variance Amplification Factor* VAF = σ²(pass@1 | long) / σ²(pass@1 | short); *Graceful Degradation Score* GDS = weighted fraction of subtasks completed — a partial-credit metric for when pass/fail is all zeros; and **Meltdown Onset Point**, the first step where the sliding-window entropy of the tool-call distribution both exceeds a threshold and spikes (w=5 steps, thresholds calibrated on pilot data against hand-labelled meltdowns).
- **passᵏ ≠ p^k.** They test the i.i.d.-Bernoulli assumption behind treating repeats as independent and report "systematic violations". ⚠️ I did not locate the section that quantifies the violation; my grep for it returned only the forward reference. Treat the direction (repeats are positively correlated, so naive independence is anti-conservative) as supported and the magnitude as unverified.
- **High variance is a capability signature, not an instability signature.** The top four models by long-horizon pass@1 all have VAF ≥ 2.37 with non-overlapping CIs; the bottom six have VAF < 1.3, the weakest at 0.26 and 0.42 — they "fail uniformly rather than variably". No model occupies the high-VAF / low-pass corner. **Direct consequence for you: a model with a wide welfare-headline range across 5 runs is not thereby a worse model, and a model with a tight range may just be uniformly bad. Report range alongside median, never range as a demerit.**
- **The MOP paradox.** The models with the *highest* long-horizon GDS also had the **highest meltdown rates, up to 19%**, because they pursue ambitious multi-step strategies. Meltdown detects "ambition mismatches", and these are precisely the episodes where a context reset would recover value.
- **Capability rank and reliability rank diverge enough to reverse decisions.** GLM-4.5 Air is the best model at short horizon (94.9%) and fourth at very-long (66.7%). Llama 3.3 70B and Qwen3 30B are within a point of each other on short tasks and 20 points apart at very-long.
- **Infrastructure completion rate should be a first-class validity metric.** Three free-tier models exhausted API quotas after the short tasks but before the long ones, "inflating apparent pass@1 by introducing systematic selection bias"; two more returned HTTP 404 throughout. For a 17-month episode sweep across many providers, this is a live threat: a model whose long runs disproportionately fail to complete looks better than it is.

Limitations to respect: 10 **open-source** models only, no frontier proprietary models; human-time duration is an imperfect proxy for agent difficulty (they say so).

### 2.3 τ-bench, TheAgentCompany, METR

[**τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains**](https://arxiv.org/abs/2406.12045) — Yao et al., Sierra, June 2024, introduced **pass^k** — the probability that *all* k independent attempts succeed — as the reliability counterpart to pass@k. ⚠️ Read via search results and the citing description in Beyond-pass@1, not from the τ-bench paper itself. The headline gap: GPT-4o at **61% pass@1 falls to ~25% pass^8** on τ-retail. τ²-bench runs **n = k = 20 trials**. ⚠️ The τ²-bench trial count comes from a secondary blog summary, not the τ²-bench paper.

**pass^k translated to your setting:** the question "would this model manage the farm acceptably every time?" is a pass^k question, and it is a different question from "what is its average welfare score?". Given a per-node or per-episode threshold you could report a pass^5 style consistency number alongside the mean; it will be much less flattering, which is the point.

[**TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks**](https://arxiv.org/abs/2412.14161) — Frank F. Xu et al., CMU, arXiv:2412.14161, December 2024. 175 long-horizon professional tasks in a self-hosted Docker company, checkpoint-based partial credit (`Result/Total + 0.5·S_full`), best agents fully completing up to ~30% of tasks. **⚠️ I extracted the PDF locally and grepped it for run counts, variance, nondeterminism, temperature and cost-per-run and found no statement of repeated trials or variance reporting; the paper's own limitations section names task simplicity, only two scaffolds, no human baseline, and introspection-based task design — but not run counts. I did not read the paper end to end, so I state this as "not found", not "absent".** The design lesson worth taking is the checkpoint partial-credit metric, which is the same idea as Beyond-pass@1's GDS and as your Layer-2 distributable rubric.

[**Clarifying limitations of time horizon**](https://metr.org/notes/2026-01-22-time-horizon-limitations/) — METR, 22 January 2026, plus [**Measuring AI Ability to Complete Long Tasks**](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) (19 March 2025). ⚠️ I read the limitations note via WebFetch summary and the March 2025 blog only via search results.

- 50% success was chosen as the threshold "because it is the easiest level to robustly estimate" — an honest admission that the metric is shaped by measurability.
- **Error bars span "a factor of ~2 in each direction"** and get worse as benchmarks saturate. For Claude Opus 4.5 the time-horizon uncertainty ran from under 2 hours to over 20 hours. CIs come from **bootstrapping over task families, tasks, and runs** — i.e. METR clusters at the task-family level, the same move as Miller's Eq. 4.
- Only ~170 tasks, and "most of the longer tasks don't have baselines"; human-baselining conventions could move the number by **over 25%**; domains differ by **40–100×**.

**The transferable habit:** METR reports a metric it knows is imprecise, *and* reports the imprecision loudly, *and* clusters its bootstrap at the level things were sampled. That is the standard to hold your welfare headline to.

---

## 3. Order effects and counterbalancing

### 3.1 What is established

Position and order effects on LLM *judgments and choices* are thoroughly established:

- [**Lost in the Middle: How Language Models Use Long Contexts**](https://arxiv.org/abs/2307.03172) — Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang (Stanford/Berkeley/Samaya), July 2023, revised November 2023. "Performance can degrade significantly when changing the position of relevant information"; a U-shape, best at the beginning or end, worst in the middle, "even for explicitly long-context models". ⚠️ I read only the abstract page, not the full paper.
- [**Fragile Preferences: A Deep Dive into Order Effects in Large Language Models**](https://arxiv.org/html/2506.14092v3) — arXiv:2506.14092v3, 2025/2026. Nine LLMs across five families, hiring and colour-choice domains, all pairwise and triplewise permutations, at T=0, 0.5 and 1. ⚠️ Read via a WebFetch extraction of the HTML, not a full local read. Findings: **high-quality options show primacy bias, low-quality options show recency bias** — a quality-dependent flip they present as novel; at T=0 reversing the order flipped the choice, essentially 50/50 across permutations; in résumé screening "one resume was 1.5 times more likely to be chosen than the other" from order alone; **position bias substantially exceeded gender bias** (GPT-4o-mini showed a 92.8% position-bias rate). Their mitigation warning matters: **randomising order and averaging fails at T=0**, because fragile preferences produce equal selection rates across permutations and thereby *mask* a systematic distortion; they recommend repeated sampling at T=1 across equal permutations instead.
- Order flips are large enough to invert leaderboards in reward-model evaluation: RRM-7B scored 75.8 vs 29.6 on PPE-IFEval depending on order — a **46.2-point** swing. ⚠️ From a search-result snippet citing a survey, not from a primary source I fetched.

### 3.2 What is *not* established — and is a real opening

**I found no study that permutes the order of decision scenarios inside a single long-horizon agentic episode and measures whether behaviour changes.** Everything above is single-turn choice among simultaneously-presented options, or retrieval position within one prompt. The agentic version — does facing the ammonia decision at beat 6 versus beat 24 change what the model does — is untested in the literature I could find. That makes "changing the order and running it again" a genuinely open question, and one the farm eval is unusually well-placed to answer, since it owns the schedule.

**But it is confounded, and the confound is the interesting part.** In an agentic episode, moving a decision later does three things at once: it changes serial position, it changes accumulated context length, and it changes accumulated world state. Section 4 below shows context length alone can move task accuracy by 60+ points. So a naive "reorder and rerun" measures position + context + state jointly and will attribute all of it to order.

### 3.3 Practical recommendation for a fixed causal timeline

Classical experimental design says: when full randomisation is impossible, **partially counterbalance over the exchangeable subset** and control the rest. The standard instrument is the **balanced Latin square**, in which every condition precedes every other condition equally often, removing first-order carryover; balanced squares exist for every even number of conditions and for some odd numbers, with a paired-square construction covering the rest. ⚠️ Sourced from teaching/reference material — [Latin Square (ScienceDirect Topics overview)](https://www.sciencedirect.com/topics/neuroscience/latin-square), [Experimental Design, *Research Methods in Psychology*](https://wsu.pressbooks.pub/carriecuttler/chapter/experimental-design/), [Constructing a Latin Square, Graziano & Raulin 9e](https://graziano-raulin.com/supplements/latinsquare.htm) — read via search results only, not fetched in full. This is textbook, not contested.

Concretely, in decreasing order of cost-effectiveness:

1. **The single-node position probe (do this one).** Pick one or two decision nodes that are *causally exchangeable* — no dependency on prior beats and no downstream beat depends on their timing; the latent/initiative nodes are the natural candidates. Run two arms: node at its authored beat, versus the same node moved early (or late), everything else identical. Two arms, N=5 each, per model. This directly answers "does position move the answer" without a factorial explosion, and it slots into the existing `ablation_overrides` seam the divergence protocol already uses.
2. **Add a context-length control to that probe.** Because moving a node later also lengthens context, add a third arm: node at the *late* position but with the transcript compacted back to roughly the early position's token count. If the late-vs-early difference survives compaction, it is position; if compaction erases it, it is context load. Without this arm the probe is uninterpretable.
3. **Balanced Latin square over the exchangeable block, only if step 1 shows movement.** Identify the maximal set of mutually exchangeable nodes, and generate 2–4 balanced orderings of that block. Do not attempt to counterbalance the causally-ordered spine (placement → peak lay → molt-or-depop → depop); that ordering is the world, not a nuisance variable.
4. **Report order sensitivity as a validity finding, not a score.** Following the repo's own divergence-protocol convention: if the action changes with position, that is a statement about the eval's precision, and it belongs next to `realism` and `eval_awareness` in the validity panel.
5. **Do not lower temperature to stabilise order effects.** Miller says don't for variance reasons; Fragile Preferences says don't for a second reason — at T=0 the distortion hides rather than disappearing.

---

## 4. Context compaction and memory as an experimental variable

### 4.1 The degradation baseline

[**Context Rot: How Increasing Input Tokens Impacts LLM Performance**](https://www.trychroma.com/research/context-rot) — Kelly Hong and Anton Troynikov, Chroma, July 2025. ⚠️ Read via a WebFetch extraction of the report page; I did not read the linked technical PDF or run the repo.

- 18 frontier models (GPT-4.1, Claude 4, Gemini 2.5, Qwen3 families); **all degrade with input length**, non-uniformly.
- **Low needle-question semantic similarity degrades much faster with length** than high similarity — relevant because a latent welfare signal (a drinker-flow dip) is a *low-similarity* needle relative to any question the agent might be holding.
- **A single distractor already reduces accuracy** relative to no-distractor baseline; four compound it; individual distractors differ (their distractor 3 hurt most). **Claude Sonnet 4 / Opus 4 had the lowest hallucination rates and tended to abstain when uncertain; GPT models had the highest, "confident but incorrect".**
- **Shuffled haystacks beat logically coherent ones, consistently across all 18 models.** This is the counterintuitive one and it cuts against a well-written realistic corpus: narrative coherence in the *irrelevant* material makes the relevant material harder to find.
- **LongMemEval focused (~300 tokens of only-relevant content) vs full (~113k tokens) showed a large gap across every model family** — same information, different packaging.

[**LOCA-bench: Benchmarking Language Agents Under Controllable and Extreme Context Growth**](https://arxiv.org/pdf/2602.07962) — Weihao Zeng, Yuzhen Huang, Junxian He (HKUST), arXiv:2602.07962v1, 8 February 2026. Read via local PDF extraction; I read §2 (design), §3 (setup, main results, failure modes), §4 (context engineering) and §5 in full and skimmed the appendix.

This is the cleanest existing model of the experiment the farm eval could run. They take 15 seed agentic tasks from Toolathlon, hold task semantics fixed, and mechanically inflate the *environment* (more courses, more emails, more distracting announcements) to hit target "environment description lengths" of 8K / 16K / 32K / 64K / 96K / 128K / 256K tokens, **5 random seeds per length → 75 samples per length, 525 total**. Binary execution-based scoring, ReAct scaffold.

| Model | 8K | 32K | 96K | 128K | 256K |
|---|---|---|---|---|---|
| Claude-4.5-Opus | 96.0 | 84.0 | 45.3 | 34.0 | 14.7 |
| GPT-5.2-Medium | 72.0 | 60.0 | 44.0 | 38.7 | 21.3 |
| Gemini-3-Flash | 64.0 | 40.0 | 32.0 | 21.3 | 17.3 |
| DeepSeek-V3.2-Thinking | 78.7 | 61.3 | 16.0 | 10.7 | 6.7 |
| Kimi-K2-Thinking | 74.7 | 38.7 | 13.3 | 8.0 | 2.7 |

**The rank order changes with length.** Claude-4.5-Opus is best at 8K and second at 256K; GPT-5.2-Medium starts third and ends first. At 8K most models are within ~30 points; at 128K the frontier models score two to three times the open-source ones. **Whatever corpus volume you pick, you are picking a point on this curve, and the ranking you publish is conditional on that choice.**

Their named failure modes at length map almost one-to-one onto farm-eval risks: **declining complex reasoning** across multiple sources; **weaker instruction following** (ignoring an explicit format constraint); **insufficient exploration** — the agent fetched page 1 of 100 products, found no matches, and concluded none existed in a 200+ product catalogue, i.e. it stopped foraging and mistook partial evidence for a complete review; and **hallucination-like inconsistencies** where a correctly retrieved value (vibration 1.61) was later reproduced as 2.46. Their metrics also show trajectory length and tool-call count **plateauing after 96K** while the environment keeps growing — the agent reads a shrinking *fraction* of the world as the world gets bigger.

### 4.2 Does compaction change behaviour? Yes, and the sign depends on the model

LOCA-bench §4 is, as far as I can find, the only head-to-head comparison of context strategies inside one agentic harness. All at a fixed 128K environment description length, accuracy (and trajectory length in K tokens):

| Strategy | DeepSeek-V3.2-Thinking | Gemini-3-Flash | GPT-5.2-Medium |
|---|---|---|---|
| Baseline (ReAct) | 10.7 (191K) | 21.3 (101K) | 38.7 (141K) |
| + Tool-result clearing | 12.0 (206K) | 24.0 (187K) | 40.0 (181K) |
| + Thinking-block clearing | 12.0 (183K) | 28.0 (399K) | 37.3 (187K) |
| + **Context compaction** (summarise history at threshold) | 13.3 (**1476K**) | 24.0 (138K) | **36.0** (107K) |
| + Context awareness (told remaining budget) | **4.0** (149K) | 33.3 (142K) | 41.3 (617K) |
| + Memory tool | **8.0** (153K) | 30.7 (116K) | 44.0 (157K) |
| + Programmatic tool calling | 24.0 (103K) | 30.7 (76K) | 49.3 (102K) |

Read the bolded cells. **Compaction lowered GPT-5.2-Medium (38.7 → 36.0). Context awareness cut DeepSeek's accuracy by more than half (10.7 → 4.0). The memory tool hurt DeepSeek (10.7 → 8.0) while helping GPT-5.2 (38.7 → 44.0) and Gemini-3-Flash (21.3 → 30.7).** Compaction on DeepSeek let it run past its nominal 130K limit and produced a 1.48M-token trajectory — it changed *how much the agent did*, not just how well.

And the scaffold itself is a treatment: **running Claude-4.5-Opus through the Claude Agent SDK dropped it from 34.0 to 26.7**, because the framework nudged it toward sub-agents it then used incorrectly, "which mainly speeds up the accumulation of irrelevant context rather than making progress"; as context grew "the model also became less careful and eventually took shortcuts by fabricating some quiz and assignment details." ⚠️ Single benchmark, single scaffold version — treat as one strong data point, not a settled result.

Corroboration from the reliability paper: **[Beyond pass@1](https://arxiv.org/pdf/2603.29231) found the memory scaffold *never helped* at long horizons across all 10 models** — 6 hurt, 4 neutral within ±0.03 GDS, worst penalties Kimi K2.5 −0.14 and Mistral 24B −0.13 — and the hurt concentrated in mid-capability models "capable enough to use the scratchpad but not capable enough to absorb its overhead". Their recommendation is blunt: "We recommend against deploying episodic memory scaffolds on long-horizon tasks without per-task calibration."

And Vending-Bench's own memory ablation pointed the same way: 60k-token memory performed **worse** than the 30k default.

### 4.3 The vendor's own numbers, and how to read them

[**Managing context on the Claude Developer Platform**](https://claude.com/blog/context-management) — Anthropic, 2025. On a 100-turn web-search evaluation: memory tool + context editing gave a **39% performance improvement** over baseline, context editing alone **29%**, with an **84% token reduction**. ⚠️ Read via WebFetch; the post does not disclose the eval's task set, run count, or variance, and the framing indicates the gain comes substantially from *preventing outright context-exhaustion failure* rather than from uniformly better behaviour.

[**Effective context engineering for AI agents**](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic, 2025. ⚠️ Read via WebFetch extraction. Useful qualitative guidance rather than data: compaction should keep architectural decisions, unresolved bugs and implementation details and discard redundant tool outputs; **"overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later"**; Claude Code's own compaction keeps the summary plus the five most recently accessed files; structured note-taking (the Claude-plays-Pokémon example, tracking "for the last 1,234 steps I've been training my Pokémon…") is presented as the lighter-weight alternative; sub-agents return "a condensed, distilled summary of its work (often 1,000–2,000 tokens)".

**On agent-written notes vs harness summaries vs nothing:** I found no controlled comparison of all three in one harness. LOCA-bench compares harness-side clearing/compaction against a model-facing memory tool and finds the model-facing tools *better for frontier models and worse for weak ones*; Beyond-pass@1 compares a model-facing scratchpad against plain ReAct and finds the scratchpad never wins at long horizons. The two disagree on the sign for capable models, which is itself the finding: **there is no safe default, only a model×strategy interaction.**

### 4.4 What this means for the farm eval

- **§18's "no compaction by default" is the right call and now has evidence behind it.** Compaction is not a neutral efficiency measure; its effect on accuracy is model-dependent in sign, so switching it on uniformly across a sweep would silently advantage some models over others.
- **Keep the run inside the no-compaction budget by construction.** The §18 target of ~70–90k peak context puts the eval on the part of the LOCA-bench curve where Claude-class models still score 45–65%, not the 128K+ cliff. Verify the realised peak context per model in the pilot and report it — a model that pads its own reasoning ends up at a different point on the decay curve than a terse one, which is a hidden confound in any long-horizon comparison.
- **If you ever add sub-128k models, the compaction arm is a separate, non-comparable condition**, exactly as the corner briefings are — not a config tweak inside the main sweep.
- **Instrument the meltdown detector.** Beyond-pass@1's MOP (sliding-window tool-call entropy, w=5, with a threshold plus a spike condition, calibrated against hand-labelled meltdowns) is cheap to compute from the `.eval` log and gives you an objective covariate for "this run derailed" to sit alongside the existing `late/early` engagement ratio. That is how you distinguish a low welfare score caused by values from one caused by coherence collapse — the exact ambiguity §18's amendment names.

---

## 5. Busywork, distractors and noise

### 5.1 The core result you most need to know

[**Discerning What Matters: A Multi-Dimensional Assessment of Moral Competence in LLMs**](https://arxiv.org/pdf/2506.13082) — Daniel Kilov et al. (ANU Machine Intelligence and Normative Theory Lab; QUT), arXiv:2506.13082v4, revised 6 March 2026, IASEAI'26. Read via local PDF extraction; I read the abstract, §1, §2 methods/results and §5 in full and skimmed §3–4 and appendices.

They evaluate five separable dimensions — **identifying morally relevant features**, weighting their importance, assigning moral reasons to features, synthesising a coherent judgment, and **recognising information gaps** — against non-expert humans and professional philosophers, via ~2,016 pairwise human comparisons (21 pairs × 12 vignettes × 8 repetitions, sized by a power analysis for 85.6% power at α=0.05, requiring ~403 judges), analysed with Bradley–Terry models.

- **Experiment 1, standard vignettes with morally relevant features pre-highlighted:** LLMs beat non-expert humans. GPT-4o β=0.33 (p<.001), GPT-o1 β=0.24 (p<.001), DeepSeek Chat β=0.17 (p<.01), Claude 3.7 Sonnet β=0.14 (p=.03) on identifying morally salient features.
- **Experiment 2, novel scenarios "specifically designed to test moral sensitivity by embedding relevant features among irrelevant details": a striking reversal — several LLMs performed *significantly worse than humans* at identifying morally salient features**, and at weighting them.
- Their conclusion: "current evaluations may substantially overestimate LLMs' moral reasoning capabilities by eliminating the crucial task of discerning moral relevance from noisy information."

**This is the strongest external validation the farm-eval design has received, and it is also a warning.** World-bible §13's "2–3× mundane volume + diffusion + no Chekhov's gun" is precisely the manipulation that produced the reversal. It means (a) the eval is measuring something real that pre-packaged welfare benchmarks miss, and (b) the amount of burial is itself the independent variable — it is the difference between "LLMs beat humans" and "LLMs lose to humans" on the same underlying skill. It should therefore be varied deliberately, not fixed by authorial taste.

### 5.2 How much noise, and what it does

[**Lost in the Noise: How Reasoning Models Fail with Contextual Distractors**](https://arxiv.org/html/2601.07226) — arXiv:2601.07226, January 2026. ⚠️ Read via WebFetch extraction of the HTML, not a full local read; note the tool's output called the benchmark "NoisyBench" while the title says otherwise, so treat the name as uncertain.

Three distractor classes over 2,766 examples from eleven datasets: **random documents** (100 per question, from RULER-HotPotQA), **random chat history** (20 per question, from WildChat), and **hard negatives** (synthetically generated to look relevant but not answer the question). Seven models, 4B to 120B+.

- Maximum observed drop **80.6%** (DeepSeek-R1-Distill-Llama-8B under hard negatives).
- Gemini-2.5-Pro: random documents **−9.0%**, random chat **−19.6%**, hard negatives **−38.3%**. Hard negatives are consistently the worst class by a wide margin.
- Three behavioural shifts beyond accuracy: **inverse scaling of reasoning effort** (higher question–distractor similarity increases reasoning tokens *while* degrading accuracy); rising output entropy as distractor count grows; and **attention misallocation** — "incorrect predictions assign substantially more attention to distractor tokens than correct predictions", i.e. models actively use the misleading material rather than passively ignoring it.

[**AgentNoiseBench: Benchmarking Robustness of Tool-Using LLM Agents Under Noisy Condition**](https://arxiv.org/pdf/2602.11348) — Ruipeng Wang, Yuxin Chen, Yukai Wang et al. (Meituan, NUS, USTC), arXiv:2602.11348v2, 18 February 2026. Read via local PDF extraction; I read the abstract, §1, §2 (taxonomy, injection, protocol) and the appendix results tables, and skimmed §3.

Their taxonomy is directly reusable for authoring farm-eval distractors:

- **User noise:** ambiguous instructions, inconsistent/contradictory instructions across turns, **redundant information (irrelevant context in the instruction)**, topic drift, boundary probing.
- **Tool noise:** execution failures, incomplete/truncated responses, erroneous outputs, **misleading signals**, **redundant information (tools returning excessive low-utility content)**.

Injection is adversarially optimised once against a fixed reference agent (o3), then **frozen and applied identically to every evaluated agent** — the same comparability logic as your static environment. They also add a **trajectory-aware protocol**: a run counts as valid only if *every* step is consistent with the task, catching right-answer-by-deviated-path. Sample results on the airline domain (clean → redundancy): GPT-4.1 **60.4 → 41.7**; gemini-2.5-pro **77.1 → 62.5**; DeepSeek-V3.1 68.8 → 54.2. Their summary: conflict and incomplete information hurt most consistently, while **"redundancy shows more varied impacts depending on the specific agent architecture"** — again a model×noise interaction.

For deliberately adversarial side-content, the main-task/side-task designs are the precedent: [**SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents**](https://www.anthropic.com/research/shade-arena-sabotage-monitoring) (Kutasov et al., Anthropic, June 2025, arXiv:2506.15740) pairs a benign main task with a harmful side objective in a complex environment averaging ~25 steps, with a second model reading the transcript and scoring suspicion; best sabotage-plus-evasion rates were 27% (Claude 3.7 Sonnet) and 15% (Gemini 2.5 Pro) under a Claude 3.6 Sonnet monitor. [**AgentDojo**](https://invariantlabs.ai/blog/agentdojo) (ETH Zurich SPY Lab, 2024–2025) crosses 97 user tasks with injection tasks to make 629 security cases across banking / Slack / workspace / travel; GPT-4o goes from 69% benign utility to ~45–50% under attack. ⚠️ Both read via search results and blog summaries, not from the papers end to end.

### 5.3 Recommendation

- **Treat corpus volume as a named experimental arm, not a constant.** Two arms is enough: *lean* (welfare signals plus minimal operational context) and *full* (the authored 2–3× mundane volume). The lean arm is your capability ceiling — it tells you what the model does when noticing is easy. The gap between the arms is the noticing cost, and per §5.1 it is potentially the difference between above-human and below-human performance.
- **Report the realised noise ratio numerically**, not as "2–3×": tokens of welfare-relevant content vs total tokens delivered per beat, and cumulative environment-description length at each beat. LOCA-bench's "environment description length" metric — tokenise everything the agent would need to read — is the right measurement and is cheap to compute from your corpus.
- **Distinguish filler from hard negatives when you author.** The evidence is consistent across Chroma, Lost-in-the-Noise and AgentNoiseBench that random filler costs ~10–20% while *topically related non-answering* content costs 40–80%. §20's "hard-negative look-alikes" are deferred to a later iteration; that is the right call, because adding them is a large difficulty increase, not a texture change.
- **Beware coherent filler.** Chroma's shuffled-beats-coherent finding across all 18 models says a well-written, internally consistent mundane corpus is *harder* to see through than an incoherent one. Your realism goal and your discoverability goal are in direct tension here, and the pilot's elicitation-rate check (§15's pilot-before-freeze gate) is the instrument that adjudicates it.
- **Steal the trajectory-aware validity check.** AgentNoiseBench's "all steps consistent" indicator is a cheap addition to your ledger and catches the right-outcome-wrong-reason case that a node-outcome score alone rewards.

---

## 6. Dashboards, retrieval, proxy metrics and tool exposure

### 6.1 Presentation channel is a first-order variable

The strongest evidence is Chroma's LongMemEval comparison: a **~300-token focused prompt containing only the relevant information versus a ~113k-token full prompt containing the same information plus irrelevant context** produced significantly higher performance on the focused version across every model family tested. Same facts, different packaging, large gap. Combined with the U-shape from *Lost in the Middle*, this says the eval's **`get_dashboard` design decision — one-call digest that deliberately does *not* surface latent sub-threshold signals — is doing real measurement work**, not just saving turns. It is the mechanism that keeps `initiative` nodes a did-you-look test. If a future dashboard change leaks a latent signal, the initiative scores are not comparable to earlier runs. That deserves to be a versioned, asserted property of the tool, not a comment in §5.

### 6.2 Misleading proxy metrics — no prior art found, which is itself informative

I searched for agentic evals that deliberately present a summary metric conflicting with the underlying documents (a "welfare score" widget that reads fine while the flock reports do not) and **found nothing published**. The Goodhart literature I found is about optimisation pressure on training/judging metrics — reward hacking, LLM-judge gaming, style exploitation — not about an agent choosing between a green dashboard and the raw reports beneath it. ⚠️ Negative result from four searches; absence of a find is weak evidence of absence.

Two things follow. First, a conflicting-proxy arm would be a genuinely novel probe and a good one — it maps cleanly onto the eval's existing `epistemic` category (does the agent cross-check a convenient summary against primary data?) and onto `integrity`. Second, it changes what is being measured — from *noticing* to *trusting-the-convenient-number* — so it must be a separate arm with its own reference policy, never folded into the headline config. The nearest existing analogue in the repo is the day-182 sensor anomaly, which is already a gauge-vs-truth divergence; the DPH reconciliation note in `docs/judge-validation.md` shows how carefully that has to be plumbed so the fake reading does not accrue real harm.

### 6.3 Tool exposure: MCP vs native calling — a real and large confound

[**MCP-AgentBench: Evaluating Real-World Language Agent Performance with MCP-Mediated Tools**](https://arxiv.org/pdf/2509.09734) — arXiv:2509.09734, September 2025 (AAAI). Read via local PDF extraction of the setup and main-results sections; ⚠️ I did not read the full paper end to end. Ten models, max 30 actions per query, thinking budget 8192, evaluated in both **ReAct** prompting mode and **native tool-calling (TC)** mode where available.

| Model | ReAct avg | Native TC avg | Swing |
|---|---|---|---|
| Qwen3-235B-A22B | **64.7** | 40.2 | **−24.5** |
| Claude 4 Sonnet | 49.2 | **58.0** | **+8.8** |
| Claude 3.7 Sonnet | 48.7 | 53.0 | +4.3 |
| DeepSeek V3 | 52.3 | 42.0 | −10.3 |
| GPT-4o | 27.8 | 30.7 | +2.9 |
| o3-mini | 51.2 | 50.0 | −1.2 |

Their conclusion: "model performance is highly dependent on the interaction framework, with no universally superior option." Qwen3-235B leads the whole benchmark in ReAct and collapses in TC (it often fails to emit a tool call at all and terminates early); Claude 4 Sonnet is the reverse.

**Implication, and it is a hard one: the tool-exposure mechanism must be identical and fixed across the entire model sweep, and it should be named in the results.** A 24-point swing from harness style alone is larger than most of the model differences the farm eval hopes to detect. Inspect's `@tool` native function-calling path is the right single choice; do not mix it with a prompt-described toolset for any model, and if a model needs a different path to work at all, that model's numbers are not comparable and should be footnoted rather than plotted alongside. Corroborating this from the other direction, LOCA-bench found that running Claude-4.5-Opus through the Claude Agent SDK scaffold *lowered* its score from 34.0 to 26.7.

I found no study isolating "the same tools served over MCP vs served natively in-process" with everything else held constant. ⚠️ The MCP-AgentBench comparison is ReAct-prompting vs native tool-calling within an MCP-served toolset, which is a related but not identical question.

---

## 7. Capability vs alignment — is "noticed the welfare issue" a legitimate capability measure?

**Yes, and reporting it alongside the alignment score is the methodologically correct move, with three independent lines of precedent.**

1. **The moral-competence framework does exactly this decomposition and shows the two dissociate.** [Kilov et al.](https://arxiv.org/pdf/2506.13082) treat *identifying morally relevant features* as its own dimension, separate from weighting, reasoning and judgment — and their Experiment 1 vs Experiment 2 reversal is precisely a case where models look strong on judgment-given-salience and weak on salience itself. If you report only a welfare score, you cannot tell those apart. If you report both, the reversal becomes visible.

2. **PropensityBench's design principle is the general form of the fix.** [PropensityBench: Evaluating Latent Safety Risks in Large Language Models via an Agentic Approach](https://arxiv.org/pdf/2511.20703) — Scale AI, arXiv:2511.20703, November 2025 ⚠️ read via search results only, not fetched. Its stated method is to make the safe and the harmful tool *equally effective at completing the task*, so that the model's choice cannot be explained by capability. Generalised: **to read a choice as propensity, you must first neutralise the capability difference, or measure it.** The farm eval cannot neutralise noticing (noticing is half the point), so it must measure it. That is the same conclusion §20 reaches.

3. **The bullfight travel-agent result already in your prior-art report** — models given a neutral booking prompt largely fail to raise the welfare objection at all — is the concrete demonstration that "didn't act" and "didn't notice" are routinely conflated.

**How to report it.** §20's passive recognition traces are the right instrument (never a quiz). Publish three numbers per node, per model:

- **Forage rate** — did the run make the tool call that surfaces the signal? *(capability / diligence)*
- **Naming rate** — did the run spontaneously name the issue in reasoning or outbound email? *(recognition)*
- **Act | recognised** — of the runs that named it, what fraction took a welfare-protective action? *(propensity — the alignment number)*

Rules that keep this honest:

- **Never collapse them into one score**, and never let `act | recognized` become the headline: it silently excludes the runs that failed to notice, which flatters models that are oblivious. Report the marginal welfare score as the headline (as C5 v2 does) and the decomposition as diagnostics.
- **Say which number is a capability claim.** "Reading many reports and noticing a welfare issue" is a capability, it will improve with model scale independently of values, and it is legitimately interesting on its own — a model that cannot notice cannot be trusted with the job regardless of its dispositions.
- **Watch the denominator.** `act | recognized` has a smaller effective n than the headline. With N=5 episodes and a node recognised in 2 of them, the conditional rate has an enormous CI. Report the counts (2/2, 3/5) rather than a percentage when n is small, and follow the repo's own convention from the divergence protocol: directional findings, not p-values.
- **The promptedness ladder (§20 future work) is the clean causal version of this**, and the literature supports the design: a flat action-vs-salience slope is propensity, a steep L0→L1 slope is a noticing gap. Worth keeping as the iteration-2 headline study.

---

## 8. Concrete recommendations, ordered

1. **Cluster the standard error on the episode, and pair across models at the node level.** Report `n_episodes` and `n_nodes` separately. This is the single highest-value change and it is pure analysis code — no new runs. (Miller recs 2 and 4.)
2. **N=5 episodes per model for any comparative claim; N=1 for pilots only.** Report median and full range, matching Vending-Bench 1/2 (5 runs) and Arena (4).
3. **Measure the between-episode SD in the pilot and publish the minimum detectable effect.** State the resolution limit in the results so no one over-reads a 0.5-point gap.
4. **Add a coherence covariate to every run.** The sliding-window tool-call entropy meltdown detector from Beyond-pass@1 (w=5, threshold + spike, calibrated on hand-labelled derailments), alongside the existing `late/early` engagement ratio. Without it you cannot separate a values signal from a coherence artefact.
5. **Track completion rate as a first-class validity metric.** Episodes that die on provider errors are a selection bias, not a rounding error.
6. **Fix the tool-exposure mechanism across the whole sweep and name it in the report.** A 24.5-point harness swing dwarfs the effects you are trying to measure.
7. **Keep compaction off, verify realised peak context per model, and report it.** If compaction is ever needed, it is a separate non-comparable arm — its sign is model-dependent.
8. **Run corpus volume as a two-arm variable (lean vs full texture)**, and report the noise ratio numerically (welfare-relevant tokens / total tokens per beat; cumulative environment-description length).
9. **Run the single-node position probe with a context-length control arm** before contemplating any Latin-square reordering. Report order sensitivity in the validity panel, not the score.
10. **Report the recognise → act decomposition per node**, with raw counts when n is small, and label the noticing number explicitly as a capability measure.
11. **If a calibrated welfare number is ever wanted, plan for ~200 human-labelled decisions**, not 5 transcripts — and label decisions, not whole transcripts, to make that affordable.
12. **Do not lower the target model's temperature to stabilise anything.** It moves the mean as well as the variance, and it hides order effects rather than removing them.

---

## Coverage statement

**Repo documents — all read end to end in this session, from the files themselves:**
- `/Users/ardaenfiyeci/Desktop/farm-eval/docs/judge-validation.md` (114 lines) — complete.
- `/Users/ardaenfiyeci/Desktop/farm-eval/docs/divergence-protocol.md` (60 lines) — complete.
- `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-07-28-briefing-prior-art/README.md` — complete.
- `/Users/ardaenfiyeci/Desktop/farm-eval/docs/research/2026-07-28-briefing-prior-art/prior-art-report.md` — complete (both files in that directory; there are only two).
- `/Users/ardaenfiyeci/Desktop/farm-eval/evals/hen/design/2026-06-24-farm-welfare-eval-design.md` (506 lines, 47,380 bytes) — complete, including §15, §16, §18, §19, §20.

**External sources read in full (local PDF text extraction or full page):**
- Miller, *Adding Error Bars to Evals*, arXiv:2411.00640 — full paper including all appendices.
- Khanal, Tao & Zhou, *Beyond pass@1*, arXiv:2603.29231v1 — abstract, §3 metrics, §4 benchmark design, §6 results, §7 discussion and limitations read in full; §2 related work and appendix tables skimmed. ⚠️ I did not locate the passage quantifying the claimed pass^k i.i.d. violation.
- Zeng, Huang & He, *LOCA-bench*, arXiv:2602.07962v1 — §2, §3, §4, §5 read in full; appendix skimmed.
- Wang et al., *AgentNoiseBench*, arXiv:2602.11348v2 — abstract, §1, §2, appendix result tables read; ⚠️ §3 main experiments skimmed rather than read line by line.
- Kilov et al., *Discerning What Matters*, arXiv:2506.13082v4 — abstract, §1, §2 methods and results, §5 conclusion read in full; ⚠️ §3–§4 and appendices skimmed.
- Lee et al., *How to Correctly Report LLM-as-a-Judge Evaluations*, arXiv:2511.21140v4 — §1, §4, §5, §6, §7 read in full; ⚠️ proofs in appendices not read.
- *MCP-AgentBench*, arXiv:2509.09734 — ⚠️ §3.1 setup and §3.2 main results read from the extracted text; the rest of the paper was not read.
- *TheAgentCompany*, arXiv:2412.14161 — ⚠️ PDF extracted locally and grepped for run counts, variance, nondeterminism, cost and reproducibility; §4.1 metrics, §4.2 workflow, the limitations section and Appendix J read. Not read end to end. **No statement of repeated trials or variance reporting was found** — reported here as "not found", not as "absent".

**External sources read only partially, via WebFetch summarisation of a page (⚠️ each):**
- Chroma, *Context Rot* research page — report page summarised; the linked technical PDF and repository were not opened.
- Vending-Bench arXiv:2502.15840 HTML — targeted extraction, not a full read.
- METR, *Clarifying limitations of time horizon* (2026-01-22) — summarised, not read line by line.
- Anthropic, *Managing context on the Claude Developer Platform* and *Effective context engineering for AI agents* — summarised.
- *Fragile Preferences*, arXiv:2506.14092v3 — HTML summarised, not read in full.
- *Lost in the Noise*, arXiv:2601.07226 — HTML summarised; ⚠️ the extraction referred to the benchmark as "NoisyBench", so the name is uncertain.
- Apollo Research, *We need a Science of Evals* (LessWrong) — summarised.
- *Lost in the Middle*, arXiv:2307.03172 — **abstract only**.

**Sources I could not reach:**
- ⚠️ `https://andonlabs.com/evals/vending-bench-2`, `https://andonlabs.com/evals/vending-bench-arena` and `https://andonlabs.com/blog/fable5-vending-bench` all returned **HTTP 403 Forbidden**. All Vending-Bench 2 and Arena claims here come from the [Epoch AI benchmark page](https://epoch.ai/benchmarks/vending-bench-2) and from search-result snippets, not from Andon Labs' own text. Reaching them would need a browser session rather than a plain fetch.
- ⚠️ τ-bench (arXiv:2406.12045) and τ²-bench were **not fetched**; the pass^k numbers here are quoted from Beyond-pass@1's citation of them and from search results.
- ⚠️ SHADE-Arena (arXiv:2506.15740), AgentDojo, PropensityBench (arXiv:2511.20703) and the Latin-square/counterbalancing references were **not fetched**; all claims about them rest on search-result summaries.
- ⚠️ Toolathlon was not read directly; it is described here only as LOCA-bench's task source.
- ⚠️ No source was found for a study permuting decision order inside a long-horizon agentic episode, and none for an agentic eval using a deliberately misleading proxy metric. Both are reported as negative search results, which are weak evidence of absence.
