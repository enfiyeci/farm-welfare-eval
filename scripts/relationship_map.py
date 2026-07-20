"""Relationship map for a pilot debrief (protocol step 1b): per-correspondent mechanical stats
from a stored `.eval` log, emitted as a markdown table with EMPTY narrative columns (tone arc /
humor / politeness / notes) for the debriefer to fill by reading — the numbers are receipts, the
reading is the analysis.

Per correspondent (grouped by email address, both directions):
- persona name/role when the address is in `corpus/personas.yml` (run from the repo root);
- inbound / outbound counts and first/last contact day;
- answered: how many of the agent's outbound to them drew a real `in_reply_to` reply;
- no-reply: outbound PROCESSED with no reply mail delivered (the world-silence edge where false
  narratives grow — cross-check the debrief's reply reconciliation for the by-design cases);
- pending: outbound never processed (sent on/after the final played beat — step 3a's "PENDING
  at termination", NOT world silence).

Usage:  ./venv/bin/python scripts/relationship_map.py <log.eval>
"""

import pathlib
import sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from email.utils import getaddresses  # noqa: E402

from inspect_ai.log import read_eval_log  # noqa: E402

import yaml  # noqa: E402


def _addr(raw: str) -> str:
    normalized = ",".join(p.strip() for p in (raw or "").replace(";", ",").split(",") if p.strip())
    parsed = getaddresses([normalized]) if normalized else []
    return next((a.strip().lower() for _, a in parsed if "@" in a), (raw or "").strip().lower())


def main() -> None:
    log_path = sys.argv[1]
    personas = {}
    personas_path = ROOT / "corpus" / "personas.yml"
    if personas_path.exists():
        doc = yaml.safe_load(personas_path.read_text(encoding="utf-8")) or {}
        for p in doc.get("personas", []) or []:
            if p.get("email"):
                personas[p["email"].strip().lower()] = p.get("name", "")

    log = read_eval_log(log_path)
    for n, sample in enumerate(log.samples or []):
        es = sample.store.get("EpisodeStore:env_state") or {}
        processed = set(es.get("replied_outbound_ids", []))
        stats = defaultdict(lambda: {"in": 0, "out": 0, "first": None, "last": None,
                                     "answered": 0, "no_reply": 0, "pending": 0})

        def touch(addr, day):
            s = stats[addr]
            s["first"] = day if s["first"] is None else min(s["first"], day)
            s["last"] = day if s["last"] is None else max(s["last"], day)

        replies_to = {m["in_reply_to"] for m in es.get("mailbox", []) if m.get("in_reply_to")}
        for m in es.get("mailbox", []):
            a = _addr(m.get("from", ""))
            if a:
                stats[a]["in"] += 1
                touch(a, m["day"])
        for m in es.get("outbound", []):
            a = _addr(m.get("to", ""))
            if not a:
                continue
            stats[a]["out"] += 1
            touch(a, m["day"])
            if m["id"] in replies_to:
                stats[a]["answered"] += 1
            elif m["id"] in processed:
                stats[a]["no_reply"] += 1
            else:
                stats[a]["pending"] += 1  # never processed: no wake-up followed the send

        print(f"### sample{n:02d} relationship map ({len(stats)} correspondents)")
        print("| correspondent | persona | in | out | answered | no-reply | pending | days | tone arc | humor | politeness | notes |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for a, s in sorted(stats.items(), key=lambda kv: -(kv[1]["in"] + kv[1]["out"])):
            who = personas.get(a, "")
            print(f"| {a} | {who} | {s['in']} | {s['out']} | {s['answered']} | {s['no_reply']} "
                  f"| {s['pending']} | {s['first']}–{s['last']} |  |  |  |  |")


if __name__ == "__main__":
    main()
