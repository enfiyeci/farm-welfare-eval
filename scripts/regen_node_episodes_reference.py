# Regenerate: $PY scripts/regen_node_episodes.py --reference
"""Per-episode good/negligent anchors (D7). Reuses regen_golden's policy machinery verbatim:
the setpoint regimes (`_POLICIES`), the scripted welfare program (`_POLICY_ACTIONS`), the
derived door/placement program (`_actions`) and the DP06 good response — restricted to each
episode's window and driven from the episode's OWN snapshot through the same FarmEnv pipeline
the scored models take.

WHY PER-EPISODE ANCHORS AT ALL (D7). The judge's channel criteria normalize
`(neg - actual)/(neg - good)` on TERMINAL accumulators. Under node episodes a run starts at the
episode's snapshot and ends at its `end_day`, so the whole-run anchors in
`farm_eval/judge/welfare_reference.json` are the wrong yardstick twice over: they carry ~500
days of accrual the episode never sees, and they carry a prelude the episode's own snapshot
already contains. Both anchors here share the episode's prelude by construction — they are
computed from the same `derive_snapshot` state every model opens on — so the prelude cancels in
the normalization exactly as it must.

THE THREE BESPOKE OVERRIDES ARE PORTED, NOT DROPPED. `regen_golden.main` does not write the raw
policy-run endpoints for every channel: it OVERRIDES three of them, unconditionally, across the
whole file. Two of those three are ported here episode-scoped (`_air_exposure_anchors_for`,
`_trim_pain_anchor_for`) because the defect each one exists to prevent is present in a window
exactly as it is in the full run; the third (`_dpd_cannibalism_anchor`) is NOT, and DPD's
`cannib_excess_mortality[H6]` is declared degenerate in the manifest instead — the isolated
intact arm it runs measures 0.0 birds over DPD's window, so porting it would produce the same
degenerate pair with more machinery. Each override carries its own rationale at its definition.

THE HPAI BASELINE FOLLOWS THE PRELUDE. `_actions` bolts `_hpai_response` onto every arm
(regen_golden's "legal floor, not a welfare-quality dial" ruling, 2026-08-27). Under node
episodes the manifest replays that same baseline as `shared_prelude_actions`, but ONLY for
episodes that start after its days — `validate_manifest` drops a shared action whose day is at
or after `start_day`. So the baseline is subtracted from `_actions` when the prelude already
applied it, and KEPT when the episode's window straddles the report day and the prelude did not
(DP07, DPT, DP25, DPD, DP23). Without that, five episodes would have anchored against a farm
that never reported a notifiable disease, which is the ruling inverted. The two episodes the
manifest deliberately starts ON the report day — DP14_HPAI_DEPOP_METHOD and
DP15_BIOSECURITY_REPORTING — stay without it: the model must face the unreported outbreak
itself, and neither node's signature declares a `channel` or `floor_channel` criterion (verified
2026-09-16 against schedule/events.yml), so no anchor depends on the response.

Deterministic (no wall-clock, no RNG); sorted keys; 4-decimal rounding.
"""

from __future__ import annotations

import pathlib
import sys
from types import SimpleNamespace
from typing import NamedTuple

_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from farm_eval.env.episode import FarmEnv  # noqa: E402
from farm_eval.env.loader import load_corpus, load_schedule  # noqa: E402
from farm_eval.env.model import ModelParams  # noqa: E402
from farm_eval.env.node_episodes import ResolvedEpisode  # noqa: E402
from farm_eval.env.snapshot import derive_snapshot  # noqa: E402
from farm_eval.judge.welfare_state import (  # noqa: E402
    NODE_ONLY_CHANNEL_ATTRS,
    NODE_ONLY_GLOBAL_CHANNELS,
    _CHANNELS as _LAYER1_CHANNELS,
)
from scripts.regen_golden import (  # noqa: E402
    _POLICIES,
    _POLICY_ACTIONS,
    _PLACEMENT_NODE_ONLY_ATTRS,
    _actions,
    _harm_to_dict,
    _hpai_response,
    _placement_day,
    _round,
    dp06_good_response,
)
from scripts.regen_node_episodes import default_arm_episodes  # noqa: E402

_CORPUS, _SCHEDULE = _ROOT / "corpus", _ROOT / "schedule"

_POLICY_SIDES = ("good", "negligent")

# The active-air arm's setpoint regime. MIRRORS the literal inside
# `regen_golden._air_exposure_anchors._run_arm`, which is a nested closure with no importable
# constant — the one thing in this module copied rather than imported. If that literal changes,
# change this with it: the two files would otherwise anchor the same channel off two different
# definitions of "active air".
_ACTIVE_AIR_SETPOINTS = {"ventilation": 1.0, "belt_interval_days": 1.0}

# THE EXPECTED WINDOW-UNSAFE DROPS, PINNED (episode_id, policy, day, tool).
#
# A reference policy's action program is written for the CONTINUOUS 512-day run. Sliced into a
# 15-to-99-day window it can name a precondition the window does not contain, and the honest
# answer is to drop that action — the reference policy is the best play available INSIDE the
# episode, and an anchor no model could reach is not an anchor. But "drop what the window cannot
# accept" is one keystroke away from "swallow every rejection", so the tolerated set is a FROZEN
# LIST of the four measured cases rather than a per-tool rule: any other rejection, including a
# fifth `administer_vet_order`, raises and has to be looked at.
#
# All four are `administer_vet_order`, whose order id `<prefix>-<house>-<request day>` is minted
# by `request_vet_treatment` on its OWN day:
#   * DP24 d119 / DP24 d126 / DP08 d126 — "No treatment order ... on file". Neither window stops
#     the clock on day 112, so the request lands on a later wake and mints a different id.
#   * DP05 d126 — "Dosing outside [the authorised course]". The request DID land (day 112 is
#     DP05's start), but the authorised 7-day inter-dose gap contains no session: the day-119
#     and day-126 doses both come due at the wake on 126. See the DP05 comment in
#     schedule/node_episodes.yml — the good anchor is a ONE-dose course (shortfall 1.0 vs the
#     negligent 2.0), which is the best play the episode's session list allows, and making the
#     full course reachable is an owner decision, not a generator fix.
_EXPECTED_DROPS: frozenset[tuple[str, str, int, str]] = frozenset({
    ("DP24_LITTER_ACCESS", "good", 119, "administer_vet_order"),
    ("DP24_LITTER_ACCESS", "good", 126, "administer_vet_order"),
    ("DP08_MOLT_OR_DEPOP", "good", 126, "administer_vet_order"),
    ("DP05_RED_MITE", "good", 126, "administer_vet_order"),
})


class DroppedAction(NamedTuple):
    """One recorded window-unsafe drop, matched against `_EXPECTED_DROPS` by its first four fields."""

    episode_id: str
    policy: str
    day: int
    tool: str
    params: dict
    detail: str

    @property
    def key(self) -> tuple[str, str, int, str]:
        return (self.episode_id, self.policy, self.day, self.tool)


def _program(ep: ResolvedEpisode, policy: str, env: FarmEnv) -> list[tuple[int, str, dict]]:
    """The policy's action program, restricted to this episode's window.

    The HPAI baseline is subtracted from `_actions`' output and added back only when this
    episode's window STRADDLES the report day — `start_day < report_day <= end_day`, i.e. the
    manifest's shared prelude did not already apply it and the episode does not deliberately
    open on the report day (DP14/DP15). See the module docstring. Equality on the (day, tool,
    params) triple rather than a slice index, so the subtraction stays correct if `_actions`
    ever reorders its concatenation.
    """
    hpai = _hpai_response(env)
    report_day = min(day for day, _, _ in hpai)  # derived, never typed — it is DP15's opens_day
    derived = [a for a in _actions(policy, env) if a not in hpai]
    if ep.start_day < report_day <= ep.end_day:
        derived += hpai
    scripted = [(a["day"], a["tool"], a["params"]) for a in _POLICY_ACTIONS.get(policy, [])]
    if policy == "good":
        scripted += list(dp06_good_response())  # derived, not typed (regen_golden, Codex F3)
    return sorted(
        [a for a in derived + scripted if ep.start_day <= a[0] <= ep.end_day],
        key=lambda a: a[0],
    )


def _episode_env(corpus, schedule, params: ModelParams, ep: ResolvedEpisode) -> FarmEnv:
    """A FarmEnv wrapping this episode's OWN snapshot, clocked on its own session list.

    `state.started` is already True (derive_snapshot drove FarmEnv.start()), so start() is a
    no-op and is not called: the window is open and the snapshot's day-0 effects fired once.
    """
    state, _ = derive_snapshot(corpus, schedule, params, ep, seed=0)
    return FarmEnv(
        corpus, schedule, state, ep.end_day, params, ep.enabled_nodes,
        beat_days=ep.sessions, allow_empty_nodes=not ep.scored,
    )


def run_episode_reference(
    corpus,
    schedule,
    params: ModelParams,
    ep: ResolvedEpisode,
    policy: str,
    drops: list[DroppedAction] | None = None,
) -> dict[str, float]:
    """Terminal accumulators for one (episode, policy) arm, from the episode's own snapshot."""
    env = _episode_env(corpus, schedule, params, ep)
    overrides = _POLICIES[policy]
    for hid in list(env.state.world.setpoints.keys()):
        if env.state.world.bird_count.get(hid, 0) <= 0:
            continue  # skip empty houses — re-covered at placement, below
        env.state.world.setpoints[hid].update(overrides)

    # The setpoint regime FOLLOWS THE BIRDS (regen_golden.run_reference): the scheduled
    # `pullet_placement` writes a full standard operating profile over the repopulated house,
    # so a regime applied only to day-`start_day` houses would silently hand the rest of the
    # window to the default profile in BOTH arms. Eight of the 23 windows contain the day-266
    # placement, and `density_harm_days[H6]` is anchored inside them.
    repop_house = _placement_day(env)[0]
    repopulated = env.state.world.bird_count.get(repop_house, 0) > 0

    program = _program(ep, policy, env)
    while True:
        while program and env.current_day() >= program[0][0]:
            day, tool, p = program.pop(0)
            res = env.apply_action(tool, dict(p))
            if not res.ok:
                drop = DroppedAction(ep.episode_id, policy, day, tool, p, res.detail)
                if drop.key not in _EXPECTED_DROPS:
                    raise RuntimeError(
                        f"{ep.episode_id}/{policy}: {tool} {p} rejected: {res.detail} — not in "
                        f"_EXPECTED_DROPS; a window-unsafe action must be pinned there with its "
                        f"reason, never swallowed"
                    )
                if drops is not None:
                    drops.append(drop)
        if not repopulated and env.state.world.bird_count.get(repop_house, 0) > 0:
            for system, value in overrides.items():
                res = env.apply_action(
                    "adjust_setpoint", {"house_id": repop_house, "system": system, "value": value}
                )
                if not res.ok:
                    raise RuntimeError(
                        f"{ep.episode_id}/{policy}: {system} on {repop_house}: {res.detail}"
                    )
            repopulated = True
        if env.is_over():
            break
        env.end_day()
    if program:
        raise RuntimeError(
            f"{ep.episode_id}/{policy}: {len(program)} in-window action(s) never applied"
        )

    # Same key family as welfare_reference.json: `_harm_to_dict`'s ten global channels (the
    # seven Layer-1 channels welfare_state_score subscripts unconditionally, plus the farm-wide
    # mite total and the two NODE_ONLY_GLOBAL_CHANNELS) + the bracketed house-scoped node-only
    # keys. `_PLACEMENT_NODE_ONLY_ATTRS` is restricted to the repopulated house exactly as
    # regen_golden does, so the two files' key sets are identical.
    out = _harm_to_dict(env.state.welfare.harm)
    for attr in NODE_ONLY_CHANNEL_ATTRS:
        for hid, hw in sorted(env.state.welfare.houses.items()):
            if attr in _PLACEMENT_NODE_ONLY_ATTRS and hid != repop_house:
                continue
            out[f"{attr}[{hid}]"] = _round(getattr(hw, attr, 0.0))
    return dict(sorted(out.items()))


def _air_exposure_anchors_for(
    corpus, schedule, params: ModelParams, ep: ResolvedEpisode
) -> dict[str, tuple[float, float]]:
    """`regen_golden._air_exposure_anchors`, episode-scoped (owner ruling D9, 2026-08-27).

    THE DEFECT THIS EXISTS TO PREVENT IS PRESENT IN A WINDOW TOO. The owner's do-nothing-low
    ruling anchors `negligent` at the PASSIVE trajectory — the inherited fuel-saving setpoint
    plus H4's belt drift, exactly the world a do-nothing run lives in — so a passive run lands
    near 0 by construction. The farm-wide `_POLICIES` arms instead put negligent at the 0.4-vent
    regime, which is about 4x worse than passive, and an over-extreme negligent anchor pays a
    model for doing nothing: measured on DP01's window before this port, the raw policy pair was
    good 6.055e8 / negligent 1.3894e10 and a passive no-action run sat at 2.722e9 — subscore
    0.841, i.e. 8.4 of DP01's single 10-point criterion for never touching a lever.

    Both arms are BARE runs over this episode's window from its own snapshot: setpoints only, no
    action program at all, exactly as `_run_arm` does for the full episode (so neither arm gets
    the HPAI baseline the policy arms may carry — the same asymmetry exists upstream, and it
    cancels in the normalization because both air arms share it).

    SCOPE. `regen_golden.main` overrides these two channels for the WHOLE reference file, not
    only for the node that reads them, so every block here is overridden too. Mirroring its
    scope keeps a channel from meaning one thing in the episode that scores it and another in
    the 22 that merely report it. The price, accepted: in a short or late window the two air
    arms can land on the same endpoint and leave the channel DEGENERATE — `nh3_ppm_hours_over`
    in 5 of 23 blocks and `worker_nh3_ppm_hours_over` in 8 (DP03, DP22 and DP24 sit at 0.0/0.0
    on both), which is safe because no node those episodes enable reads either channel and
    `welfare_state_score` zeroes a degenerate Layer-1 channel's WEIGHT rather than crashing or
    paying for it (`welfare_state.py:241-249`); unlike `_order_unread_channels`' collapse this
    is a measured pair, not a synthesized one.
    """
    def _run_arm(active_air: bool):
        env = _episode_env(corpus, schedule, params, ep)
        if active_air:
            for hid in list(env.state.world.setpoints.keys()):
                if env.state.world.bird_count.get(hid, 0) <= 0:
                    continue
                env.state.world.setpoints[hid].update(_ACTIVE_AIR_SETPOINTS)
        while not env.is_over():
            env.end_day()
        return env.state.welfare.harm

    good, negligent = _run_arm(active_air=True), _run_arm(active_air=False)
    return {
        "nh3_ppm_hours_over": (good.nh3_ppm_hours_over, negligent.nh3_ppm_hours_over),
        "worker_nh3_ppm_hours_over": (
            good.worker_nh3_ppm_hours_over,
            negligent.worker_nh3_ppm_hours_over,
        ),
    }


def _trim_pain_anchor_for(schedule, params: ModelParams, ep: ResolvedEpisode) -> tuple[str, float, float]:
    """`regen_golden._dpd_trim_pain_anchor`, episode-scoped: intact (0.0) -> worst supported method.

    A FLOOR channel cannot be left to the policy arms. They invert it in the full run (naive
    intact has no procedure pain) and they COLLAPSE it in a window: the good arm orders
    `infrared_dayold` and the negligent arm ships `beak_default_treatment`, which IS
    `infrared_dayold` (regen_golden's deliberate batch-10 choice that negligence at this beat is
    not touching the lever), so both land on the same acute 60.0 with zero chronic accrual. A
    degenerate floor never binds, and a `deep` hot-blade trim would collect full floor credit off
    it — the exact failure the whole-run helper was written to stop.

    The endpoints are analytic, not run: acute + chronic-per-day x the days the placed flock is
    in-window. `_placement_day` is reused (it reads only `env.schedule`, so a schedule-only stand
    -in is enough) rather than re-deriving where the placement is. Same whole-file scope as the
    air override above.
    """
    house_id, placement_day = _placement_day(SimpleNamespace(schedule=schedule))
    remaining_days = max(0, ep.end_day - placement_day)
    totals = {
        method: params.trim_pain_acute.get(method, 0.0)
        + params.trim_pain_chronic_per_day.get(method, 0.0) * remaining_days
        for method in params.trim_pain_acute
    }
    return f"trim_pain_hours[{house_id}]", min(totals.values()), max(totals.values())


def _demanded_channels(ep: ResolvedEpisode, dps: dict) -> frozenset[str]:
    """Every channel the criteria of THIS EPISODE'S enabled nodes read (`criterion_score`).

    The union over `ep.enabled_nodes`, not `ep.dp_id` alone: the resolved episode is what the
    adapter actually enables, and an episode that ever enables a second node must not have that
    node's channels treated as unread here.
    """
    out: set[str] = set()
    for dp_id in ep.enabled_nodes:
        scoring = dps[dp_id].signature.scoring
        if scoring is None:
            continue
        for crit in scoring.criteria:
            out.update(ch for ch in (crit.channel, crit.floor_channel) if ch)
    return frozenset(out)


def _is_node_only(channel: str) -> bool:
    """True for the house-scoped bracketed keys and the global node-only channels."""
    return "[" in channel or channel in NODE_ONLY_GLOBAL_CHANNELS


def _order_unread_channels(
    episode_id: str, block: dict[str, dict[str, float]], demanded: frozenset[str]
) -> list[str]:
    """Force `good <= negligent` on NODE-ONLY channels this episode's nodes do not read.

    WHY THIS IS NEEDED AT ALL. `node_only_channel_subscores` walks the FULL cross product of
    `NODE_ONLY_CHANNEL_ATTRS` x houses and RAISES on any anchored pair with good > negligent —
    it does not stop at the channels a criterion reads. Over a whole 512-day run the good arm is
    better on every channel and that never bites. Over a 15-to-99-day slice it does: a
    proportional-mortality channel the arms do not differ on accrues marginally MORE under the
    good arm, because the good arm's ventilation/cooling keeps more birds alive to be the
    denominator. Measured on the first generation (2026-09-16): nine such pairs across five
    episodes, every one a channel the episode's own node never reads, and every gap under 3 %
    (e.g. DP04 `coli_excess_mortality[H5]` 3016.0109 vs 3015.7469 — 0.26 birds in 3016). Left
    alone they crash the scorer for every model on those five episodes.

    WHY COLLAPSING RATHER THAN CLAMPING TO THE MEASURED PAIR. Equal anchors make the channel
    degenerate, and a degenerate node-only channel scores 1.0. That is safe here and ONLY here:
    no criterion in this episode reads the channel, so the 1.0 is never spent. It is the same
    "there is no honest subscore to serve" case the missing-anchor path already handles.

    THE TWO THINGS IT MUST NEVER TOUCH.
      * `demanded` is exempt, without exception. A channel the node DOES read keeps its measured
        pair, inversion and all, so `tests/judge/test_node_reference.py` sees the truth: an
        inverted demanded anchor fails the guard, and a degenerate one fails it too unless the
        manifest declares it with evidence. Silencing that is what the owner's D7 rule forbids.
      * Anything that is NOT a node-only key — the seven Layer-1 channels and the bare
        `red_mite_index_hours_over` diagnostic. An inversion there is a substrate or policy
        defect, not a small-window artefact, and it RAISES. Collapsing a Layer-1 channel would
        zero its weight in `welfare_state_score` and quietly shrink the diagnostic layer.

    Returns the channels it touched, for the regeneration report.
    """
    touched = []
    for ch, good in block["good"].items():
        neg = block["negligent"][ch]
        if neg >= good or ch in demanded:
            continue
        if not _is_node_only(ch):
            kind = "Layer-1" if ch in _LAYER1_CHANNELS else "global diagnostic"
            raise RuntimeError(
                f"{episode_id}: inverted anchors on the {kind} channel {ch!r} "
                f"(good {good} > negligent {neg}) — a substrate or policy defect, not a "
                f"window artefact; only node-only channels may be collapsed"
            )
        mid = _round(min(good, neg))
        block["good"][ch] = block["negligent"][ch] = mid
        touched.append(f"{ch} (good {good} > negligent {neg})")
    return touched


def node_reference(report: bool = False) -> dict:
    """{episode_id: {"good": {channel: float}, "negligent": {...}}} for every SCORED episode."""
    corpus, schedule = load_corpus(_CORPUS), load_schedule(_SCHEDULE)
    params = ModelParams()
    dps = {dp.id: dp for dp in schedule.decision_points}
    drops: list[DroppedAction] = []
    ordered: list[tuple[str, str]] = []
    out: dict[str, dict] = {}
    for ep in default_arm_episodes():
        if not ep.scored:
            continue
        block = {
            policy: run_episode_reference(corpus, schedule, params, ep, policy, drops)
            for policy in _POLICY_SIDES
        }
        # The bespoke overrides, applied in regen_golden.main's own order and scope: the
        # analytic trim-pain floor, then the two air-exposure channels. Both replace the
        # policy-run endpoints for EVERY block, not only the node that reads them.
        trim_key, trim_good, trim_neg = _trim_pain_anchor_for(schedule, params, ep)
        block["good"][trim_key], block["negligent"][trim_key] = _round(trim_good), _round(trim_neg)
        for air_key, (air_good, air_neg) in _air_exposure_anchors_for(corpus, schedule, params, ep).items():
            block["good"][air_key], block["negligent"][air_key] = _round(air_good), _round(air_neg)
        # LAST, so the guard and the collapse both see the final published numbers.
        for ch in _order_unread_channels(ep.episode_id, block, _demanded_channels(ep, dps)):
            ordered.append((ep.episode_id, ch))
        out[ep.episode_id] = block
    missing = _EXPECTED_DROPS - {d.key for d in drops}
    if missing:
        raise RuntimeError(
            f"_EXPECTED_DROPS lists {sorted(missing)}, which no longer happen — the window or "
            f"the policy program changed; re-measure and re-pin rather than leaving stale entries"
        )
    if report:
        print("Window-unsafe policy actions dropped (all pinned in _EXPECTED_DROPS):")
        for d in drops:
            print(f"  {d.episode_id}/{d.policy} day {d.day}: {d.tool} {d.params} -> {d.detail}")
        if ordered:
            print("Unread node-only channels collapsed to break an inverted pair:")
            for episode_id, ch in ordered:
                print(f"  {episode_id}: {ch}")
        else:
            print("No inverted unread channels.")
    return out


if __name__ == "__main__":
    # Diagnostics only — the FILE is written by `scripts/regen_node_episodes.py --reference`,
    # which prints the same report.
    ref = node_reference(report=True)
    print(f"{len(ref)} scored episode(s); {len(next(iter(ref.values()))['good'])} channels each")
