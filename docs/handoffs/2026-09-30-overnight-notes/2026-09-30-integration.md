# Integration: overnight/integration-2026-09-30

Eval: hen

- **Branch:** `overnight/integration-2026-09-30`, off `origin/feat/node-episodes` @ `6859f6f7`. Pushed to origin.
  No PR, nothing merged into `main` or `feat/node-episodes`, no force-push, no model calls.
- **Worktree:** `/home/oliver/Documents/Github/farm-welfare-eval/.claude/worktrees/integration`
- **Tip:** `f3338797` (all 10 merges; no fix commits were needed).
- **Status:** all merges done, including WP8. Every test group exits 0, every regen script leaves the tree
  byte-identical, lints are 0 findings, and every committed report reproduces.

## Merge log (`git merge --no-ff`, in this order)

| # | branch (origin tip) | merge commit | result |
|---|---|---|---|
| 1 | `overnight/run-hygiene` (WP4, `ac516bf2`) | `abed5b5a` | clean |
| 2 | `overnight/score-observability` (WP2, `8348e45d`) | `028b93cd` | clean (auto-merged `scorer.py`; WP4's `demanded_channels` + `demanded=` kwarg survive) |
| 3 | `overnight/node-discrimination-guard` (WP1, `422edf97`) | `ae5044d7` | clean |
| 4 | `overnight/cost-and-cache` (WP5, `f2072267`; contains WP4) | `737f3806` | clean |
| 5 | `overnight/detell-pass-1` (WP3, `20fff9d9`; contains WP1) | `6cecf286` | clean |
| 6 | `overnight/feed-digest` (WP6 + WP6b, `c8e8897c`) | `56b3eef5` | clean |
| 7 | `overnight/mail-clock` (WP7, `90609f61`) | `1b83afaa` | **2 conflicts** (below) |
| 8 | `overnight/wake-audit` (WP9 audit only, `be20d503`) | `2170c7a6` | clean |
| 9 | `overnight/difficulty-proposals` (doc, `33403ac8`; contains WP3) | `080783d6` | clean |
| 10 | `overnight/voice-and-leaks` (WP8, `03d44518`; contains WP3) | `f3338797` | clean |

**Not merged:** `overnight/wake-audit-scope14-proposal` (awaits the owner's ruling, as instructed).

## Conflicts and resolutions

Both were import lines only, in the WP7 merge (WP6b and WP7 each added names to the same import):

- `farm_eval/env/episode.py`: WP6b imported `long_date`, `feed_next_delivery_day`, `feed_on_hand_tons`; WP7 turned
  the clock import into a 3-line import adding `send_windows_for`. Resolved as the union:
  `from farm_eval.env.clock import (compact_date, date_for_day, long_date, next_beat, send_windows_for, session_header, timestamp_for)`
  plus `from farm_eval.env.digest import build_digest, feed_next_delivery_day, feed_on_hand_tons`.
- `farm_eval/env/loader.py`: WP6b `from farm_eval.env.clock import weekday_number`; WP7 `from farm_eval.env import clock`.
  Kept both lines.

Checked after resolving: `clock.py` auto-merged with both WP6b's weekday helpers and WP7's send-window section;
`test_feed_supply`, `test_mail_hours`, `test_clock` and `test_node_snapshot_golden` pass (75) straight after the merge.

**`corpus/personas.yml` (WP7 + WP8, flagged by the coordinator):** merged with no conflict. The result has WP8's
`global:` blocks (`bank_reply_banned_patterns`, `season_rules`) and WP7's top-level `send_hours:` block plus the
per-persona `send_hours`. The loader reads both (every test that loads the real corpus passes), and
`lint_corpus.py` applies WP8's season and bank-voice rules with 0 findings.

**`evals/hen/runs/2026-09-30-tell-audit.md` (WP3 + WP8):** no conflict (WP8's copy was built on WP3's tip).

No golden conflicted, so none had to be taken from one side.

## Regen scripts (run after all 10 merges, from the worktree root)

| script | exit | result |
|---|---|---|
| `scripts/regen_node_episodes.py --snapshots --reference` | 0 | byte-identical (`node_snapshots.json`, `node_reference.json`) |
| `scripts/regen_golden.py` | 0 | byte-identical (baseline checkpoints, reference runs, welfare reference) |
| `scripts/regen_behaviour_golden.py` | 0 | byte-identical |
| `scripts/regen_spectator_golden.py` | 0 | byte-identical |
| `scripts/regen_financial_reference.py` | 0 | byte-identical (`financial_reference.json`); took 1732 s under load, so it ran as a Bash background task, not a foreground call |

(`regen_node_episodes_reference.py` is the module behind `regen_node_episodes.py --reference`; it has no CLI of its own.)

Why nothing moves: WP6b's snapshot move (only the 26 `digest_sha256` values) was already committed on its branch and
is what the regen reproduces. WP7 does not reach the digest (the digest prints no mail stamps) or the fixture corpora
(no sender config), WP8 changes only reply text that no golden contains, and WP3's net content change (the A6
phosphorus line, the A7 beak rejection) touches no golden.

## Test groups (`PY=/home/oliver/Documents/Github/farm-welfare-eval/venv/bin/python`, `-p no:cacheprovider`, each its own call, timeout 600000)

| group | exit | result |
|---|---|---|
| `$PY -m pytest --ignore=tests/env` | 0 | 1475 passed, 3 skipped (223 s) |
| `$PY -m pytest tests/env/model` | 0 | 526 passed (140 s) |
| `$PY -m pytest tests/env/test_[a-d]*.py` | 0 | 441 passed (254 s) |
| `$PY -m pytest tests/env/test_[e-l]*.py` | 0 | 241 passed (100 s) |
| `$PY -m pytest tests/env/test_[m-z]*.py` | 0 | 579 passed (88 s) |

The env groups add up to 1787, which equals `pytest tests/env --collect-only`. The worktree's `logs/` stayed empty
(WP4's G1 conftest works). The financial regen ran alongside some of these groups, so their times are inflated.

## Lint and consistency

- `scripts/lint_corpus.py`: 0 findings (includes WP8's season and bank-voice rules over WP6b's 7 edited mill emails
  and WP7's personas).
- `scripts/check_corpus_consistency.py`: 0 findings.
- `scripts/audit_schedule.py`: exit 0, no warnings.

## Reports: regenerated and compared with the committed copies

| report | command | delta |
|---|---|---|
| `2026-09-30-node-discrimination-report.md` (WP1) | `$PY scripts/node_discrimination_report.py` | body byte-identical; only the header branch/sha line differs |
| `2026-09-30-tell-audit.md` (WP3/WP8) | `$PY scripts/tell_audit.py` | body byte-identical; header line only |
| `2026-09-30-wake-audit.md` (WP9) | `$PY scripts/audit_wakes.py --variant base scope scope14 ramp hpai5 dp06alt` | output byte-identical to the same command run on the WP9 branch that produced the doc |
| `2026-09-30-cost-report.md` (WP5) | the two commands in the report header | all 73 generated table rows appear verbatim in the committed report |
| `2026-09-30-log-leak-scan.md` (WP8) | `scripts/scan_log_leaks.py` over the 5 log dirs in its header | generated part byte-identical; the hand-written findings section is (by design) not produced by the script |
| snapshot probe (`probe_node_snapshots.py`) | `$PY scripts/probe_node_snapshots.py` | body identical to the committed 09-22, WP3 and WP6 probes (header lines only) |

So the combination changes no report, and none was rewritten (a header-only rewrite would just churn the sha line).
For WP10: the discrimination summary on the integration branch is exactly WP1's (8 pass; DP16, DP25, DPD fail for
design reasons; 7 arm-lacks-action; 5 llm-only; 41 frozen pins, none stale).

## Open issues

1. **Mill mail stamps vs. the feed digest (WP6b x WP7, realism nit, not fixed).** WP6b's test checks each
   "Next delivery <day>" in Glenn's mail against the mail's *delivery* day. WP7 stamps most mail on the previous
   day inside the sender's hours (ruling 20 item 1), and Glenn's window is 06:30–17:00. In a full real-corpus run,
   2 of 13 such mails are stamped on a **Monday morning** (day 203 at 11:04, day 371 at 09:50) and say "Next delivery
   Thursday", although Monday's afternoon drop has not yet happened by that stamp. The model reads them at the
   Tuesday session, where the digest also says Thursday, so nothing it sees at once disagrees. This is not a merge
   regression: WP6b alone (old clock) has 3 such mails. Possible fixes, all content calls: tag those mail events
   `mail_same_day: true` (WP7's opt-in), or word them "next drop Thursday" only on Tuesday-delivered mail. Owner.
2. Everything the WP notes already list as NEEDS-OWNER stays open: A3/A4/A5 de-tell texts, A8 docstrings, T24b
   (Karen's ack vs. the day-248 lab mail), the scope14 wake ruling, DP06's 29 sessions, D5, the stale
   `last login` banner, F4b, the reply subject slot, the feed terms note / cover figures, the 2027 cached-input
   price, the fixed Vertex region, `--retry-on-error 1`, the corpus lint's long-mail floor at its edge.
3. `tests/env` is now 1787 tests; `test_[a-d]` is the heaviest group (~4 min unloaded). The four-way split above
   keeps every group well under the 10-minute cap.
