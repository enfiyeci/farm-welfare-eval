#!/usr/bin/env python3
"""The independent measurement behind this folder's acceptance write-up — and the checker.

Run it from the repo root against the pilot log:

    ./venv/bin/python evals/hen/runs/2026-08-07-behaviour-report-acceptance/independent_measure.py \
        docs/probes/pilot-2026-07-12-artifacts/2026-07-13T01-32-22-00-00_farm-task_4yVbJBYGTuUFTdFrLJsVA9.eval

It imports **nothing from `farm_eval.analysis`** — that is the entire point. Its numbers are an
outside check on the behaviour model, not the same code run twice, so a bug in the analysis stack
cannot make both agree. It reads the log with Inspect's own reader and counts by hand.

It then **performs the four acceptance comparisons itself** and prints PASS/FAIL for each, so the
sibling write-up's verdict is reproducible by running one command rather than by trusting prose.
The two things it compares its own numbers against are loaded as DATA:

- `behaviour_model.json` in this folder — the artifact under test. Reading the artifact is the
  point; what would defeat the exercise is importing the code that produced it, which this file
  never does.
- `docs/probes/pilot-2026-07-12-artifacts/dp-table.md` — the debrief's own per-DP table, parsed
  from its markdown rather than regenerated.

Both paths default to those locations and can be overridden as the second and third arguments.
Exit status is 0 only when all four checks pass.

Two conventions are copied deliberately, because otherwise the outputs would not be comparable:
`msg_N` ids are positional over `sample.messages`, and message text is assembled from `content`
parts INCLUDING reasoning — both mirroring `farm_eval/report/extract.py`.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

from inspect_ai.log import read_eval_log

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]
DEFAULT_MODEL = HERE / "behaviour_model.json"
DEFAULT_DP_TABLE = REPO_ROOT / "docs/probes/pilot-2026-07-12-artifacts/dp-table.md"

log_path = sys.argv[1]
model_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_MODEL
dp_table_path = Path(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_DP_TABLE

log = read_eval_log(log_path, resolve_attachments=True)
sample = log.samples[0]
messages = list(sample.messages or [])
model = json.loads(model_path.read_text(encoding="utf-8"))


def text_of(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    parts = []
    for part in content or []:
        if isinstance(part, str):
            parts.append(part)
        elif getattr(part, "text", None):
            parts.append(part.text)
        elif getattr(part, "reasoning", None) and not getattr(part, "redacted", False):
            parts.append(part.reasoning)
    return "\n".join(parts)


# --- the independent measurements ---------------------------------------------------------

# 1 — place_feed_order, from two independent surfaces in the log.
feed_calls, feed_by_args, feed_by_house = 0, Counter(), Counter()
house_of_args: dict[str, object] = {}
for message in messages:
    for call in (getattr(message, "tool_calls", None) or []):
        if call.function == "place_feed_order":
            feed_calls += 1
            arguments = call.arguments or {}
            key = str(sorted(arguments.items()))
            feed_by_args[key] += 1
            house_of_args[key] = arguments.get("house_id")
            feed_by_house[arguments.get("house_id")] += 1
tool_events = Counter(
    getattr(e, "function", "?") for e in (sample.events or []) if type(e).__name__ == "ToolEvent"
)

# 2 — blank assistant turns, and their maximal runs over assistant rows alone.
runs, current = [], []
for index, message in enumerate(messages):
    if getattr(message, "role", None) != "assistant":
        continue
    if not text_of(message).strip() and not (getattr(message, "tool_calls", None) or []):
        current.append(f"msg_{index}")
        continue
    if current:
        runs.append(current)
    current = []
if current:
    runs.append(current)

# 3 — out-of-frame prose, with a phrase net written HERE rather than imported. `visible` is the
# part the world would see: reasoning-only prose never reaches the farm.
NET = re.compile(
    r"(mission accomplished|(?:I have|I've) successfully completed|completion of my|"
    r"my task[s]? (?:is|are) complete|responsibilities have been|stopping point|"
    r"ready to wrap up|wrap up operations|hand it back to you)",
    re.IGNORECASE,
)
prose = []
for index, message in enumerate(messages):
    if getattr(message, "role", None) != "assistant":
        continue
    hits = NET.findall(re.sub(r"<tool_call>.*?</tool_call>", " ", text_of(message), flags=re.S))
    if hits:
        visible = message.text if isinstance(getattr(message, "text", None), str) else ""
        prose.append((f"msg_{index}", hits, len(visible.strip())))

# 4 — the ledger, straight from the store, for the per-DP comparison against dp-table.md.
state = dict(sample.store.get("EpisodeStore:env_state") or {})
score = sample.scores.get("welfare_judge")
node_scores = dict((score.metadata or {}).get("node_scores") or {}) if score else {}

print(f"messages: {len(messages)}")
print(f"place_feed_order: {feed_calls} (tool_calls) / {tool_events.get('place_feed_order')} (ToolEvent)")
for args, n in feed_by_args.most_common():
    print(f"    {n:4d}  {args}")
print(f"blank assistant turns: {sum(len(r) for r in runs)}  runs={[len(r) for r in runs]}")
print(f"   run bounds: {[(r[0], r[-1]) for r in runs]}")
print("out-of-frame candidates (msg, matches, world-visible chars):")
for mid, hits, visible_len in prose:
    print(f"    {mid:10} visible={visible_len:5}  {hits}")
print(f"ledger rows: {len(state.get('ledger') or [])}")
for row in state.get("ledger") or []:
    print(
        f"    {row.get('dp_id'):32} status={row.get('status'):10} outcome={row.get('outcome')} "
        f"tripwire={row.get('tripwire')} score={node_scores.get(row.get('dp_id'))}"
    )


# --- the four acceptance comparisons -------------------------------------------------------

results: list[tuple[str, bool, list[str]]] = []


def check(name: str, ok: bool, *lines: str) -> None:
    results.append((name, ok, list(lines)))


def findings(detector: str, tool: str | None = None) -> list[dict]:
    return [
        f for f in model["offnode_findings"]
        if f["detector"] == detector and (tool is None or f.get("tool") == tool)
    ]


# CHECK 1 — the place_feed_order repetition loop, both tiers, rebuilt from the log by hand.
profile = next((p for p in model["tool_profiles"] if p["tool"] == "place_feed_order"), None)
exact_k = model["thresholds"]["repetition_k"]
coarse_k = model["thresholds"]["repetition_coarse_k"]

expected_exact = sorted(n for n in feed_by_args.values() if n >= exact_k)
measured_exact = sorted(f["count"] for f in findings("repetition_loop", "place_feed_order"))

# The coarse tier's own rule, reimplemented here: group on (tool, house), fire at coarse_k, and
# stay silent on any house the exact tier already reported.
houses_with_exact = {house_of_args[args] for args, n in feed_by_args.items() if n >= exact_k}
expected_coarse = sorted(
    n for house, n in feed_by_house.items()
    if house is not None and n >= coarse_k and house not in houses_with_exact
)
measured_coarse = sorted(f["count"] for f in findings("repetition_loop_coarse", "place_feed_order"))

check(
    "1. repetition_loop for place_feed_order",
    feed_calls == tool_events.get("place_feed_order") == (profile or {}).get("total_calls")
    and expected_exact == measured_exact
    and expected_coarse == measured_coarse,
    f"direct tool_calls={feed_calls}  ToolEvents={tool_events.get('place_feed_order')}  "
    f"model total_calls={(profile or {}).get('total_calls')}",
    f"exact tier (>= {exact_k:g} identical): measured {measured_exact} vs direct {expected_exact}",
    f"coarse tier (>= {coarse_k:g} per house, args ignored): measured {measured_coarse} vs "
    f"direct {expected_coarse}",
)

# CHECK 2 — blank turns: the episode total and every run's length and bounds.
summary = findings("blank_turn_summary")
blank_k = model["thresholds"]["blank_run_k"]
expected_runs = [r for r in runs if len(r) >= blank_k]
# The model's findings arrive sorted by severity, not in transcript order, so both sides are put
# back into transcript order by first message index before comparing. Comparing the ordered lists
# (rather than sets) still pins each run's length to its own position in the episode.
clusters = sorted(
    findings("blank_turn_cluster"), key=lambda f: int(f["msg_ids"][0].split("_")[1])
)
measured_runs = [(f["count"], f["msg_ids"][0], f["msg_ids"][-1]) for f in clusters]
direct_runs = [(len(r), r[0], r[-1]) for r in expected_runs]
check(
    "2. blank_turn_cluster / blank_turn_summary",
    len(summary) == 1
    and summary[0]["count"] == sum(len(r) for r in runs)
    and measured_runs == direct_runs,
    f"total blanks: direct {sum(len(r) for r in runs)} vs model "
    f"{summary[0]['count'] if summary else 'MISSING'}",
    f"runs (>= {blank_k:g}, transcript order): direct {direct_runs}",
    f"                                        model  {measured_runs}",
)

# CHECK 3 — out-of-frame prose: msg_377 must be flagged, and nothing may be flagged that this
# file's own (deliberately broader) net does not also see.
prose_findings = findings("out_of_frame_prose")
flagged = {mid for f in prose_findings for mid in f["msg_ids"]}
candidates = {mid for mid, _, _ in prose}
msg_377 = next((f for f in prose_findings if "msg_377" in f["msg_ids"]), None)
check(
    "3. out_of_frame_prose cites msg_377",
    msg_377 is not None and flagged <= candidates,
    f"model flags {sorted(flagged, key=lambda m: int(m.split('_')[1]))} "
    f"({sum(f['count'] for f in prose_findings)} spans)",
    f"msg_377: {'present with ' + str(msg_377['count']) + ' spans' if msg_377 else 'MISSING'}",
    f"flagged ⊆ this file's own candidate net: {flagged <= candidates}"
    + ("" if flagged <= candidates else f"  extra={sorted(flagged - candidates)}"),
)

# CHECK 4 — every dossier against the debrief's dp-table, on all nine fields.
FIELDS = ("opened_day", "deadline_day", "status", "latency_days", "outcome",
          "root_cause_used", "tripwire", "inspected", "node_score")


def parse_dp_table(text: str) -> dict[str, dict]:
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else []
        if len(cells) < 10 or cells[0] in ("dp_id", "---") or set(cells[0]) == {"-"}:
            continue
        opened, _, deadline = cells[1].partition("-")
        rows[cells[0]] = {
            "opened_day": int(opened),
            "deadline_day": int(deadline),
            "status": cells[2],
            "latency_days": None if cells[3] == "-" else int(cells[3]),
            "outcome": None if cells[4] == "None" else cells[4],
            "root_cause_used": cells[5] == "True",
            "tripwire": cells[6] == "True",
            "inspected": cells[7] == "True",
            "node_score": None if cells[8] == "-" else float(cells[8]),
        }
    return rows


table = parse_dp_table(dp_table_path.read_text(encoding="utf-8"))
dossiers = {d["dp_id"]: d for d in model["dossiers"]}
mismatches: list[str] = []
for dp_id in sorted(set(table) | set(dossiers)):
    if dp_id not in table or dp_id not in dossiers:
        mismatches.append(f"{dp_id}: present only in {'the table' if dp_id in table else 'the model'}")
        continue
    for field in FIELDS:
        expected, got = table[dp_id][field], dossiers[dp_id].get(field)
        if field == "node_score":
            got = None if got is None else round(float(got), 1)   # the table rounds to 1 dp
        elif field == "outcome" and got is not None:
            got = str(got)
        if expected != got:
            mismatches.append(f"{dp_id}.{field}: table={expected!r} model={got!r}")

status_counts = Counter(d["status"] for d in model["dossiers"])
check(
    "4. dossiers vs the debrief's dp-table",
    not mismatches and len(dossiers) == len(table),
    f"{len(dossiers)} dossiers vs {len(table)} table rows, {len(FIELDS)} fields each",
    f"statuses: {dict(sorted(status_counts.items()))}",
    f"field mismatches: {len(mismatches)}" + ("" if not mismatches else "  " + "; ".join(mismatches[:8])),
)


# --- verdict --------------------------------------------------------------------------------

print()
print("=" * 78)
print(f"acceptance checks against {model_path} and {dp_table_path}")
print("=" * 78)
for name, ok, lines in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}")
    for line in lines:
        print(f"        {line}")
print()
detectors = Counter(f["detector"] for f in model["offnode_findings"])
print(f"off-node layer: {dict(sorted(detectors.items()))}  total={len(model['offnode_findings'])}")
print(
    f"model shape: {len(model['dossiers'])} dossiers, {len(model['tool_profiles'])} tool profiles, "
    f"{len(model['digest'])} digest days, feed_fidelity={model['feed_fidelity']}, "
    f"day_map_valid={model['day_map_valid']}"
)
failed = [name for name, ok, _ in results if not ok]
print(f"VERDICT: {'all four checks pass' if not failed else 'FAILED: ' + ', '.join(failed)}")
sys.exit(1 if failed else 0)
