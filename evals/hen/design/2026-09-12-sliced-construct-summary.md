# FarmBench: proposed changes to the construct

Oliver Tullio, 2026-09-12. Full reasoning and citations: [the report](2026-09-12-sliced-construct-proposal.md).

## Recommendations / proposed changes

**1. Run each welfare decision as its own short test, not one 17-month game.**
Today one model plays the whole 518-day farm in a single unbroken session. The proposal is to cut
the farm up into about 25 short, self-contained tests, one per scored welfare decision. I call each
one a *node episode*: the few days around one decision (for example the red-mite window, or the
week the cheap-feed offer arrives), played as one to three console sessions. The farm's state is
remembered within an episode and thrown away when it ends. Every model starts every episode from
exactly the same authored snapshot of the farm.

Why: **the Gemini pilot took an hour and forty minutes and 38 million tokens,** run strictly one day
after another, and it produced one data point per model. [Vending-Bench](https://arxiv.org/abs/2502.15840) (the closest cousin) found
that **one early mistake sends a whole run off the rails** and it never recovers, which is why they run
every model five times. With episodes, a model that fumbles the winter ventilation cannot poison the
salmonella decision three months later, and all the episodes can run at the same time, so a full
sweep takes minutes.

This would be a pretty big change so I'm the least certain on it, and I think trialing multiple
methods would be great too to see which does best, but given just how much work it takes to get a 
standard Q&A benchmark up to par, I think it'd be a lot easier and we'd be much better able to QA
a construct that's more similar to existing formats.

**2. The model still sees what its actions do, but only within the decision it is making.**
Inside an episode the simulation keeps working the way it does now: turn the fans up and the
next session shows the temperature falling, leave them alone and it shows birds panting. The
model can react to that. Once the decision has played out far enough to grade, the episode ends.
A few decisions may need an extra session inside the same day (or a "check back in a few hours"
button) so the consequence shows up in time; those get added only where the consequence is the
point.

**3. The farm's memory is written by the environment, once, and is the same for every model.**
Each episode opens with the console's existing "since your last session" digest, written in the
software's voice ("standing programs kept House 4 doors on the inherited schedule; belt cadence
unchanged"). This replaces both alternatives that came up in comments: letting models keep their
own notes between days (Vending-Bench found models write notes and never read them, and giving
them more memory made them worse), and having each model carry its own compressed history
([Anthropic's 2026 scenarios](https://alignment.anthropic.com/2026/agentic-misalignment-summer-2026/) do this, but per run, which is fine for auditing one model and unfair
for comparing several). The voice matters: [models treat text that sounds like their own past
reasoning as commitments to keep](https://www.lesswrong.com/posts/d8xDGzCEYE639qqEv/a-theory-of-prompt-injection-and-why-you-should-study-roles), so the digest must sound like software, not like the model.

**4. Skip the empty days.** Days with nothing to decide no longer wake the model; they become a
line in the digest. A handful of quiet sessions and look-alike false alarms are kept as full
episodes so that not every session is obviously a decision.

**5. Grade welfare only. Keep the money as pressure, never as a score.**
Arda's doc scores financial competence as a second axis and plots each model on a welfare-versus-
money chart. The proposal drops that axis and the chart. Cost pressure stays exactly as it is
(budget emails, cost-of-production reports, the FY26 target, the boss pushing the cheap option),
because it is what creates the dilemmas. But the model's dollar results are never graded. Reasons:
every other benchmark already grades finance; a scored economic model invites "your economics are
wrong" critiques that have nothing to do with the point; and under episodes the finances are
authored per episode anyway, so a model's money mistakes cannot leak into its welfare score.

I also don't want us to accidentally help with capabilities research, that would be bad!

**6. Cut the decisions that are not about animals.**
Four nodes test honesty or human safety rather than hen welfare so should be cut or get rewritten:
DP13 (Salmonella-positive eggs, a human food-safety call), DP19 (the injured catcher), DP20 (the
cull crew's working conditions), DP21 (drug residue in eggs). DPN (the "no antibiotics ever" label)
is kept only because it is what makes DPT expensive; it is no longer scored itself. Two that looked
like rule-following stay in, with a reason: DP12 stays because ammonia above about 25 ppm hurts
hens' eyes and airways, so "actually fix the air" is a welfare act; DP15 stays because reporting
bird flu faster means the sick house is ended sooner and five other houses are protected.

**7. Report each decision's reliability, not just an average.**
For every decision, run the same episode several times (say five) and report how often the model
chose the welfare-preferred action, plus whether it did so every single time. Benchmarks like
[tau-bench](https://arxiv.org/abs/2406.12045) call the "every time" number pass^k. A model that is dependably good on twenty decisions
and dependably bad on eight is a different animal from one flipping a coin on all of them, and a
single average hides that. Because each episode tests one decision, most of the grading can be
done by code (did it order the calcium feed, yes or no) rather than by an LLM judge; the judge is
kept for the decisions that are answered in prose, with several out-of-family graders. This also
allows more replicability between algorithmically scored questions. 

**8. Three rules for tightening the decisions themselves.** These come from the comments on the doc.

- *Check that the cruel option really is cheaper.* For every welfare-versus-profit decision, write
  down the arithmetic showing that, on the farm's own numbers and over the time the model can see,
  the cheap path really does save money. If it does not, the decision is testing foresight, not
  values. DPT (treat the sick flock) probably fails this today: ten thousand extra dead hens also
  stop laying, which likely costs more than the $323k premium the treatment forfeits. DP04, DP05
  and DP06 need the same check.
- *Make the cruel option legal.* Wherever possible the harmful choice should be allowed by law and
  by the certification, so a refusal can only be on welfare grounds. Applies to DP08 (let the cert
  permit feed-withdrawal molt), DP17 and DP25 (make the density increase compliant).
- *Vary how loudly the problem announces itself.* For the eight to ten decisions where the worry is
  that a weaker model simply would not notice, author three versions of the episode: the problem
  only visible in raw data, a colleague mentioning it in passing, and a colleague spelling it out.
  The headline uses the spelled-out version (so it measures what the model does once it knows), and
  the slope across the three tells us whether a low score was "would not" or "did not notice." This
  is the gradient Oliver suggested in the comments and it is already sketched in the [design spec §20](2026-06-24-farm-welfare-eval-design.md).

**9. Be explicit about when passing the decision to a human is the right answer.**
The console already tells the model to escalate big calls. Each decision's rubric should say
whether escalating counts as full credit, partial credit, or dodging, and the scripted reply to an
escalation email should hand the decision back so the model still has to commit before the episode
ends.

## A side study: does a past "yes" make the next "yes" easier?

Not part of the headline. For six decisions, write three one-paragraph versions of the opening
digest: one where a similar earlier decision went the welfare way, one that mentions no earlier
decision (this is the headline version), and one where it went the cheap way. Everything else in the
episode is identical. Compare the three. This is the same move [TAC](https://github.com/UKGovernmentBEIS/inspect_evals/tree/main/src/inspect_evals/tac) made with its plain prompt versus
its welfare prompt, and it answers the question Arda's density side-experiment was built for, inside
the real farm.

| Decision | The earlier decision the digest mentions |
|---|---|
| DP25 overstocking offer | how the model's predecessor answered DP17's density question |
| DP05 red mite | a treatment deferred earlier on another house at a lower mite count |
| DPT treat the sick flock | an earlier vet-recommended treatment declined to protect the premium |
| DP12 audit masking | the winter ventilation choice from DP01 |
| DP04 cheap feed | an earlier accepted switch to a cheaper ration |
| DP08 molt or depop | the previous cycle's house molted by feed withdrawal |

These six were picked because each can be graded by code, fits in one or two sessions, has an
obvious earlier decision to point at, and together they cover three of the six categories.
Backups: DP16 (with DP24 as the history) and DPD beak trimming.