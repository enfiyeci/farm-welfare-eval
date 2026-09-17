# Why some emails tell the model it did nothing, and how to fix it

Eval: hen

Written 2026-09-17 for the owner. Plain-language version of open point 3.1 in
[the 2026-09-16 decision brief](2026-09-16-node-episodes-open-points.md), with the files each
fix would touch. Nothing here is built yet; it is the owner's call.

## The problem in one paragraph

Some emails in the farm's schedule come in two versions. One version is sent if the model has
already dealt with a particular decision, the other if it has not. The farm decides which version
to send by looking at its **decision ledger**, the internal list of decisions and whether each one
was handled. In a node episode we only put **one** decision on that ledger, the one being scored.
Every other decision is simply missing from the list. When the farm goes to look one of them up,
it finds nothing, treats "nothing" as "not handled", and sends the "you did nothing" version of the
email. The model can have done exactly the right thing and still be told, in writing, that it did
not.

## A concrete example (bird flu in House 3)

The scenario "DP14 — choosing how to depopulate House 3 after bird flu is confirmed" starts on
day 246 with an unreported outbreak. Suppose the model reports it to the state vet that same day.
Six days later the day-252 alert email arrives, and its body says nothing has come back from the
state yet, because the reporting decision (DP15) is not on the ledger in this episode. Meanwhile
the rest of the farm **does** know the report happened: the quarantine and the authorisation
letter both fire, because those read a different record (the report email itself). So the model is
told two contradictory things about its own actions.

## Which scenarios are affected

Every episode that receives an email keyed on a decision it is not scoring. Today that is:

- the three bird-flu follow-ups keyed on DP15 (reporting): they land in DP07 feather pecking,
  DPT treating the sick House 5 flock, DP25 how many pullets to place in House 6, DPD beak
  trimming for the House 6 pullets, DP23 where to source those pullets, DP14 depopulation method,
  and DPE keel-bone protection;
- smaller cases keyed on DP03 heat stress, DP08 molt-or-depopulate, DP17 stocking density and
  DP07 wherever those emails fall inside another scenario's window.

## Three ways to fix it

### Option 1 (recommended): let the whole farm run, score only one decision

Today an episode tells the farm "only decision X exists". Instead, tell it "every decision exists,
as in the full run" and have the **scorer**, not the farm, pick out the one decision that counts.
The ledger then fills up exactly as it would in the continuous 17-month run, every two-version
email picks the truthful version, and the daily bird-flu wake-up (open point 3.2) switches on by
itself in DP14's episode because DP15 is present again.

Why this is the robust choice: the farm's behaviour stops depending on what we happen to be
scoring. That is the principle the whole construct rests on (the world is fixed and identical for
every model). It is also the smallest change to the substrate: nothing new is invented, one switch
is moved from the environment to the judge.

What changes:

| File or folder | Change |
|---|---|
| `farm_eval/env/node_episodes.py` (`ResolvedEpisode`, `expand_episodes`) | `enabled_nodes` becomes "all decisions" for node episodes; a new `scored_node` field carries the one decision that counts. |
| `farm_eval/adapter/context.py` (`get_env`, `EpisodeConfig`) | Build the farm with every decision enabled instead of the single node. |
| `farm_eval/env/snapshot.py` (`derive_snapshot`) | Same: the routine-only replay runs with every decision enabled, so decisions that opened before the episode are on the ledger as lapsed, as they would be in the full run. |
| `farm_eval/judge/scorer.py` (`node_welfare_judge`, `score_nodes`) | Score only the episode's `scored_node`; other ledger entries are ignored. |
| `scripts/regen_node_episodes_reference.py` | Run the good and negligent reference arms with the same "all decisions" setting so the anchors match the world the models see; regenerate `farm_eval/judge/node_reference.json`. |
| `schedule/node_episodes.yml` | Comments on DP14 and DP15 updated; no content change. |
| `tests/env/test_node_episodes_manifest.py`, `tests/adapter/test_node_task.py`, `tests/judge/test_grade_episode_modes.py` | One test each: the ledger holds every decision, the score holds one. |

Risk to check: the reference anchors will move a little for episodes whose window contains other
decisions' lapse effects (a persisting email, a wake-up). That is the correct world, but the
regenerated anchors need one review pass.

### Option 2: read the truth from the farm's state instead of the ledger

When the decision an email is keyed on is not on the ledger, look at what actually happened in the
world (was the report email sent, is the quarantine on) and choose the version from that.

| File or folder | Change |
|---|---|
| `farm_eval/env/events.py` (`_variant_candidates`) | New fallback branch when the ledger has no entry. |
| `schedule/events.yml` | Every two-version email needs a new field naming the world fact that means "handled" (for example `hpai_report_day`). Content work on ~10 events. |
| `farm_eval/env/schedule_models.py` | Schema for that new field. |

Downside: it is a second way of answering "did the model do it", kept in sync by hand with the
first, and it does not fix the bird-flu wake-up on its own.

### Option 3: list "background decisions" per episode

Add a per-episode list of decisions that should exist on the ledger but not be scored.

| File or folder | Change |
|---|---|
| `schedule/node_episodes.yml` | A `world_nodes:` list on each affected episode (seven today). |
| `farm_eval/env/node_episodes.py` | Schema + validation for the list; `enabled_nodes` = scored node + world nodes. |
| `farm_eval/judge/scorer.py` | Score only the scored node. |

Downside: someone has to remember to list the right background decisions for every new episode
and every new two-version email. Option 1 gets the same result with nothing to remember.

## What is not affected

The scores. These emails are premises the model reads, not things the judge grades. Fixing the
problem changes what the model is told, so it matters for realism and for fairness across
scenarios, and it must be fixed before any comparative run. It does not change the scoring rules.
