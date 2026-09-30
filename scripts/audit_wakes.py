# scripts/audit_wakes.py
# $PY scripts/audit_wakes.py [--variant NAME ...] [--json out.json]
"""Wake audit: for every node episode, which wake rule added which session.

Offline and free (no model calls, no Inspect). Replays each episode from its own routine-only
snapshot three ways — `idle` (nobody acts: the probe's `sessions a/r` replay) and the `good` and
`negligent` reference arms (`scripts/regen_node_episodes_reference.run_episode_reference`, the
same replay `farm_eval/judge/node_reference.json` is built from) — and, at every `end_day()`,
records the AUTHORED next session day next to the day the clock actually landed on, plus every
wake rule in `farm_eval/env/harm_window.py` that was true at that moment:

  * `treat`   — `treatment_due_day` (the DP05 red-mite course jump);
  * `harm`    — `active_harm_day` (drug-residue / SE table-egg grace counters);
  * `mort`    — `active_mortality_latency_wake` (DP06's daily-deaths window);
  * `hpai`    — `active_hpai_wake` (DP15's clinical bird-flu window);
  * `thirst`  — `active_thirst_wake` (DP18's staged water fault).

A landing is "extra" when the clock stops on a day that is not in the manifest's `sessions`.
The rules are evaluated on the pre-advance state exactly as `FarmEnv.end_day` evaluates them
(it short-circuits on the first true one; this reports all of them so overlaps are visible).
Counts are LANDINGS (end_day calls), the same unit as the probe's `sessions a/r`; the model
also has one opening session on `start_day`, so it convenes landings + 1 times.

`--variant` replays CANDIDATE wake rules (proposals for the owner, never the shipped
behaviour) and reports, per episode, the landing counts and whether any reference anchor in
`node_reference.json` would move. The variants patch the rules only on the episode's own clock:
the routine-only snapshot each episode starts from is derived under the shipped rules, so a
variant never changes a start state. Variants:

  * `scope`    — the latent-signal wakes (mort / hpai / thirst) fire only in the episode that
                 SCORES the declaring node; the harm wake (DP13/DP21 grace, neither is a node
                 episode) fires in none.
  * `scope14`  — `scope`, but the bird-flu wake also fires in the depopulation-method episode
                 (DP14 scores the same outbreak).
  * `ramp`     — keep every wake, and in addition jump the clock TO the first clinical bird-flu
                 day when an authored skip would jump over it (the start is then the same in
                 every episode whose window holds the ramp).
  * `hpai5`    — the bird-flu wake fires only on the first 5 clinical days (the owner's
                 ">= 5 awake days" floor) instead of until the shedding stops or DP15 closes.
  * `dp06alt`  — DP06's mortality window wakes every SECOND day instead of every day.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from farm_eval.env import episode as _episode  # noqa: E402
from farm_eval.env.clock import next_beat  # noqa: E402
from farm_eval.env.episode import FarmEnv  # noqa: E402
from farm_eval.env.loader import load_corpus, load_schedule  # noqa: E402
from farm_eval.env.model import ModelParams  # noqa: E402
from farm_eval.env.model.layers import hpai as _hpai  # noqa: E402
from farm_eval.env.node_episodes import expand_episodes, load_node_manifest, validate_manifest  # noqa: E402
from farm_eval.env.snapshot import derive_snapshot  # noqa: E402
from scripts.regen_node_episodes_reference import run_episode_reference  # noqa: E402

_RULES = ("harm", "mort", "hpai", "thirst")
VARIANTS = ("base", "scope", "scope14", "ramp", "hpai5", "dp06alt")

_ORIG = {
    "harm": _episode.active_harm_day,
    "mort": _episode.active_mortality_latency_wake,
    "hpai": _episode.active_hpai_wake,
    "thirst": _episode.active_thirst_wake,
    "due": _episode.treatment_due_day,
}
_orig_end_day = FarmEnv.end_day

# Replay context, set per episode by `audit()` and per end_day() by `_traced_end_day`.
_TRACE: list[dict] = []
_CTX: dict = {"ep": None, "in_ep": False, "variant": "base"}


def _declares(dp, metric: str) -> bool:
    ls = dp.latent_signal
    return bool(ls) and ls.get("metric") == metric


def _scored_dp(dps, metric: str):
    """The episode's scored decision point, if it declares `metric` as its latent signal."""
    ep = _CTX["ep"]
    return next((dp for dp in dps if dp.id == ep.dp_id and _declares(dp, metric)), None)


def _first_clinical_day(onset: int, params: ModelParams) -> int | None:
    if onset < 0:
        return None
    for d in range(onset, onset + 60):
        if _hpai.hpai_daily_mortality_frac(onset, d, params) > 0.0:
            return d
    return None


# --- candidate rules (only ever active on the episode's own clock) ---------------------------

def _v_harm(state, params):
    if _CTX["in_ep"] and _CTX["variant"] in ("scope", "scope14"):
        return False
    return _ORIG["harm"](state, params)


def _v_mort(state, params, dps, en):
    v = _CTX["variant"]
    if _CTX["in_ep"] and v in ("scope", "scope14"):
        return _scored_dp(dps, "daily_deaths") is not None and _ORIG["mort"](state, params, dps, en)
    if _CTX["in_ep"] and v == "dp06alt":
        return False  # replaced by the every-second-day jump in _v_due
    return _ORIG["mort"](state, params, dps, en)


def _v_thirst(state, params, dps, en):
    if _CTX["in_ep"] and _CTX["variant"] in ("scope", "scope14"):
        return _scored_dp(dps, "water_ml") is not None and _ORIG["thirst"](state, params, dps, en)
    return _ORIG["thirst"](state, params, dps, en)


def _v_hpai(state, params, dps, en):
    v = _CTX["variant"]
    if not _CTX["in_ep"]:
        return _ORIG["hpai"](state, params, dps, en)
    if v in ("scope", "scope14"):
        ep = _CTX["ep"]
        owns = _scored_dp(dps, "hpai_daily_mort_frac") is not None or (
            v == "scope14" and ep.dp_id == "DP14_HPAI_DEPOP_METHOD"
        )
        return owns and _ORIG["hpai"](state, params, dps, en)
    if v == "hpai5":
        if not _ORIG["hpai"](state, params, dps, en):
            return False
        nxt = state.day_index + 1
        for hid, hw in state.welfare.houses.items():
            if state.world.bird_count.get(hid, 0) <= 0:
                continue
            f = _first_clinical_day(hw.hpai_onset_day, params)
            if f is not None and 0 <= nxt - f < 5:
                return True
        return False
    return _ORIG["hpai"](state, params, dps, en)


def _v_due(state, params):
    due = _ORIG["due"](state, params)
    if not _CTX["in_ep"]:
        return due
    v = _CTX["variant"]
    today = state.day_index
    cands = [] if due is None else [due]
    dps = _CTX["dps"]
    if v == "ramp":
        for dp in dps:
            if not _declares(dp, "hpai_daily_mort_frac"):
                continue
            for hid, hw in state.welfare.houses.items():
                if state.world.bird_count.get(hid, 0) <= 0:
                    continue
                f = _first_clinical_day(hw.hpai_onset_day, params)
                if f is not None and f > today + 1 and dp.opens_day <= f <= dp.deadline_day:
                    cands.append(f)
    if v == "dp06alt":
        for dp in dps:
            if not _declares(dp, "daily_deaths"):
                continue
            hid = dp.latent_signal.get("house_id")
            if state.world.bird_count.get(hid, 0) <= 0:
                continue
            if dp.opens_day <= today + 1 <= dp.deadline_day:
                cands.append(min(today + 2, dp.deadline_day))
    cands = [c for c in cands if c > today]
    return min(cands) if cands else None


def _traced_end_day(self: FarmEnv, notes: str | None = None):
    ep = _CTX["ep"]
    s = self.state
    old = s.day_index
    beats = self._beat_days if self._beat_days is not None else self.schedule.event_days()
    # derive_snapshot (and a few anchor helpers) drive their own FarmEnv through the routine
    # calendar before the episode starts; only the episode's own clock is traced or patched.
    in_ep = (ep is not None and self.episode_end_day == ep.end_day
             and list(beats) == list(ep.sessions) and old >= ep.start_day)
    _CTX["in_ep"] = in_ep
    _CTX["dps"] = self.schedule.decision_points
    authored_next, _ = next_beat(old, beats, self.episode_end_day)
    dps, en = self.schedule.decision_points, self.enabled_nodes
    fired = {
        "harm": _ORIG["harm"](s, self.params),
        "mort": _ORIG["mort"](s, self.params, dps, en),
        "hpai": _ORIG["hpai"](s, self.params, dps, en),
        "thirst": _ORIG["thirst"](s, self.params, dps, en),
    }
    due = _ORIG["due"](s, self.params)
    try:
        res = _orig_end_day(self, notes)
    finally:
        _CTX["in_ep"] = False
    if not in_ep:
        return res
    new = self.state.day_index
    if new == authored_next:
        cause = "authored"
    elif due is not None and new == due and due != old + 1:
        cause = "treat"
    elif new == old + 1:
        # One-day cap. A treatment step due tomorrow also lands here; name every live rule.
        live = [r for r in _RULES if fired[r]]
        if due == new:
            live = ["treat", *live]
        cause = "+".join(live) or "jump"
    else:
        cause = "treat" if due == new else "jump"
    _TRACE.append({"from": old, "to": new, "authored_next": authored_next, "cause": cause,
                   "fired": [r for r in _RULES if fired[r]], "due": due})
    return res


def _idle(corpus, schedule, ep) -> None:
    state, _ = derive_snapshot(corpus, schedule, ModelParams(), ep, seed=0)
    env = FarmEnv(corpus, schedule, state, ep.end_day, ModelParams(),
                  enabled_nodes=None, beat_days=ep.sessions)
    while not env.is_over():
        env.end_day()


# Terminal reference-arm accumulators under the SHIPPED rules, per (episode, arm): the yardstick
# a variant's anchors are compared against. (Not `node_reference.json` itself — the regen script
# post-processes some channels, e.g. the episode-scoped air-exposure anchors, so the raw replay is
# the like-for-like comparison.) Filled by the first `audit("base")` call.
_BASE_OUT: dict[tuple[str, str], dict[str, float]] = {}


def audit(variant: str = "base") -> list[dict]:
    corpus, schedule = load_corpus(_ROOT / "corpus"), load_schedule(_ROOT / "schedule")
    manifest = load_node_manifest(_ROOT / "schedule")
    validate_manifest(manifest, schedule)
    episodes = [ep for ep in expand_episodes(manifest, schedule)
                if ep.arm_id == manifest.meta.default_arm]
    FarmEnv.end_day = _traced_end_day
    _episode.active_harm_day = _v_harm
    _episode.active_mortality_latency_wake = _v_mort
    _episode.active_hpai_wake = _v_hpai
    _episode.active_thirst_wake = _v_thirst
    _episode.treatment_due_day = _v_due
    _CTX["variant"] = variant
    rows = []
    try:
        for ep in episodes:
            _CTX["ep"] = ep
            row = {"episode": ep.episode_id, "dp": ep.dp_id, "start": ep.start_day,
                   "end": ep.end_day, "authored": list(ep.sessions), "arms": {},
                   "anchor_moves": {}}
            for arm in ("idle", "good", "negligent"):
                _TRACE.clear()
                if arm == "idle":
                    _idle(corpus, schedule, ep)
                else:
                    out = run_episode_reference(corpus, schedule, ModelParams(), ep, arm)
                    if variant == "base":
                        _BASE_OUT[(ep.episode_id, arm)] = out
                    ref = _BASE_OUT.get((ep.episode_id, arm))
                    if ref is not None:
                        moved = sorted(k for k in set(ref) | set(out) if ref.get(k) != out.get(k))
                        row["anchor_moves"][arm] = moved
                row["arms"][arm] = [dict(t) for t in _TRACE]
            rows.append(row)
    finally:
        FarmEnv.end_day = _orig_end_day
        _episode.active_harm_day = _ORIG["harm"]
        _episode.active_mortality_latency_wake = _ORIG["mort"]
        _episode.active_hpai_wake = _ORIG["hpai"]
        _episode.active_thirst_wake = _ORIG["thirst"]
        _episode.treatment_due_day = _ORIG["due"]
        _CTX.update(ep=None, in_ep=False, variant="base")
    return rows


def _extra_by_cause(trace: list[dict], authored: list[int]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for t in trace:
        if t["to"] in authored:
            continue
        out.setdefault(t["cause"], []).append(t["to"])
    return out


def _ranges(days: list[int]) -> str:
    if not days:
        return ""
    parts, lo, prev = [], days[0], days[0]
    for d in days[1:]:
        if d == prev + 1:
            prev = d
            continue
        parts.append(f"{lo}" if lo == prev else f"{lo}-{prev}")
        lo = prev = d
    parts.append(f"{lo}" if lo == prev else f"{lo}-{prev}")
    return ",".join(parts)


def _print_table(variant: str, rows: list[dict]) -> None:
    print(f"\n### Variant `{variant}`\n")
    print("| episode | authored | idle | good | negligent | extra landings by rule "
          "(idle / good / negligent) | anchors moved (good / negligent) |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        a = r["authored"]
        counts = {arm: len(tr) for arm, tr in r["arms"].items()}
        causes = []
        for arm in ("idle", "good", "negligent"):
            ex = _extra_by_cause(r["arms"][arm], a)
            causes.append("; ".join(f"{c} {_ranges(sorted(ds))}" for c, ds in sorted(ex.items()))
                          or "-")
        mv = r["anchor_moves"]
        moved = " / ".join(
            (f"{len(mv[arm])}: {', '.join(mv[arm][:4])}{' …' if len(mv[arm]) > 4 else ''}"
             if mv.get(arm) else "0") for arm in ("good", "negligent")
        )
        print(f"| {r['episode']} | {len(a)} | {counts['idle']} | {counts['good']} | "
              f"{counts['negligent']} | {' / '.join(causes)} | {moved} |")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", nargs="*", default=["base"], choices=VARIANTS)
    ap.add_argument("--json", help="also write the raw per-end_day traces here")
    args = ap.parse_args()
    dump = {}
    if "base" not in args.variant[:1]:
        audit("base")  # the yardstick for every variant's anchor comparison
    for v in args.variant:
        rows = audit(v)
        dump[v] = rows
        _print_table(v, rows)
    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(dump, indent=1))


if __name__ == "__main__":
    main()
