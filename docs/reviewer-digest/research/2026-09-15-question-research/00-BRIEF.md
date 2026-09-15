# Brief for the reviewer-question research (2026-09-15)

## Context
FarmBench is an animal welfare benchmark: an AI model runs a simulated commercial cage-free egg farm
(Iowa, six aviary houses of ~125,000 Hy-Line Brown hens, UEP 2024 certified) for a 17-month flock cycle
and faces 29 scored welfare decisions. A short "reviewer digest" (one page per decision) is being sent to
Lukas Jasiūnas, co-founder and former Head of Research of Healthier Hens (a Charity Entrepreneurship
charity, 2021 to 2024, that worked on cage-free hen welfare on commercial farms in Kenya: keel bone
fractures and feed fortification, on-farm welfare assessment by palpation and radiography, thermal
stress, feed and water access, biosecurity; priced interventions in Welfare Footprint pain-hours).
He is a chemical engineer by training, not a vet and not a US industrial egg operator.

Each digest page ends with a field "**What we would like you to check.**" holding one to four questions
for him. The owner's instruction: those questions must be things that CANNOT simply be looked up online.
If public sources answer a question, we should look it up ourselves and either drop the question or
turn it into "the literature says X; does that match what you have seen?". The owner also wants us to
brainstorm additional relevant open-ended questions and to judge whether each question is actually
necessary (would the answer change the design or the scoring?).

## Files
Worktree root: /Users/ardaenf/worktrees/fwe-reviewer-digest
- Digest pages: docs/reviewer-digest/<NODE>.md (read in full)
- Full coworker page behind each: docs/design-review/coworker/<NODE>.md (read in full; its
  "Open questions" and "Sources" sections matter most)
Do NOT write anything inside the worktree. Write your report to the scratchpad path given in your task.

## For each node assigned to you
1. Read both files end to end.
2. For EACH question in the digest's "What we would like you to check" field:
   a. Search the web (several queries, primary sources preferred: peer-reviewed papers, extension
      services, UEP/certification texts, industry guides, regulator pages). Classify:
      - ANSWERABLE ONLINE: give the answer in two to four sentences with 1 to 3 source links.
      - PARTLY: say what public sources settle and what remains a matter of judgment or field experience.
      - NOT ANSWERABLE ONLINE: explain why only experience or expert judgment can answer it.
   b. Necessity: HIGH (the answer would change the scenario, a threshold, or the scoring), MEDIUM
      (would improve realism or confidence), LOW (nice to know; recommend dropping).
   c. If the question is already answered by a source the coworker page itself cites, say so.
3. Propose 1 to 3 ADDITIONAL open-ended questions for this node that (i) a welfare scientist with
   on-farm cage-free experience could answer, (ii) cannot be looked up, and (iii) would change the
   design or scoring if answered. Mine the coworker page's "Open questions" section for candidates.
   Prefer questions about: whether the scenario as authored is realistic, whether the scored best path
   is really best for the birds, thresholds and magnitudes that are authored rather than measured,
   and what a real manager would do.
4. Give a one-line overall verdict per node: keep / rewrite / drop each existing question, and which
   new ones to add.

## Rules
- Read every source you cite in full where possible; where you could not (paywall, truncation,
  abstract only), mark the claim with ⚠️ and say what was missing. Do not fill gaps with plausible
  reconstructions.
- End your report with a COVERAGE STATEMENT: which files and web sources you opened, which you read
  end to end, which you could not reach.
- Plain prose, no em dashes or en dashes. Every URL as a markdown link.
- Return the full report as your final message AND write it to your scratchpad path.
