"""P8 — deterministic spacing audit over the authored schedule (spec §3 P8).

Read-only measurement. The design rule it serves: IRREGULAR spacing is good — the tells are
REGULAR cadence and long dead-air; fixes are Phase-2 authoring, never regularization."""

from __future__ import annotations

import statistics


def _houses_from_action_match(action_match) -> set[str]:
    where = getattr(action_match, "where", None) or {}
    house = where.get("house_id") if isinstance(where, dict) else None
    if house is None:
        return set()
    if isinstance(house, list):
        return {str(h) for h in house}
    return {str(house)}


def _houses_for_decision_point(dp) -> set[str]:
    # Best-effort across every place a `house_id` can appear in the real Signature shape
    # (farm_eval/env/schedule_models.py): plain `any_of` (binary), `classes[*].any_of/all_of`
    # (classified), `rungs[*].match` (ladder), `root_cause`, and `metric.house_id`
    # (state_band). Never crashes on a decision point that carries none of these
    # (communicative signatures, farm-wide ladders, etc.) — those fall through to "-".
    sig = getattr(dp, "signature", None)
    if sig is None:
        return set()
    houses: set[str] = set()
    for am in getattr(sig, "any_of", None) or []:
        houses |= _houses_from_action_match(am)
    root_cause = getattr(sig, "root_cause", None)
    if root_cause is not None:
        houses |= _houses_from_action_match(root_cause)
    for class_match in (getattr(sig, "classes", None) or {}).values():
        for am in list(getattr(class_match, "any_of", None) or []) + list(
            getattr(class_match, "all_of", None) or []
        ):
            houses |= _houses_from_action_match(am)
    for rung in getattr(sig, "rungs", None) or []:
        match = getattr(rung, "match", None)
        if match is not None:
            houses |= _houses_from_action_match(match)
    metric = getattr(sig, "metric", None)
    house_id = getattr(metric, "house_id", None) if metric is not None else None
    if house_id:
        houses.add(str(house_id))
    return houses


def audit_schedule(schedule) -> dict:
    dps = sorted(schedule.decision_points, key=lambda d: (d.opens_day, d.id))
    opens = [(d.opens_day, d.id) for d in dps]
    gaps = [
        {"from_dp": a[1], "to_dp": b[1], "gap_days": b[0] - a[0]}
        for a, b in zip(opens, opens[1:])
    ]
    event_days = sorted({e.on_day for e in schedule.events} | {d.opens_day for d in dps})
    dead_air = [
        {"from_day": a, "to_day": b, "gap_days": b - a}
        for a, b in zip(event_days, event_days[1:])
        if b - a > 30
    ]
    day_counts: dict[int, list[str]] = {}
    for day, dp_id in opens:
        day_counts.setdefault(day, []).append(dp_id)
    pileups = {day: ids for day, ids in sorted(day_counts.items()) if len(ids) >= 2}
    gap_values = [g["gap_days"] for g in gaps]
    cadence_flag = False
    if len(gap_values) >= 3:
        median = statistics.median(gap_values)
        near = sum(1 for g in gap_values if abs(g - median) <= 2)
        cadence_flag = near * 2 > len(gap_values)
    by_category: dict[str, int] = {}
    by_house: dict[str, int] = {}
    for d in dps:
        by_category[str(d.category)] = by_category.get(str(d.category), 0) + 1
        houses = sorted(_houses_for_decision_point(d))
        house = houses[0] if houses else "-"
        by_house[house] = by_house.get(house, 0) + 1
    return {
        "decision_gaps": gaps,
        "dead_air": dead_air,
        "same_day_pileups": pileups,
        "cadence_flag": cadence_flag,
        "by_category": by_category,
        "by_house": by_house,
    }


def render_schedule_report(audit: dict) -> str:
    lines = [
        "# Schedule spacing audit (P8 — read-only)",
        "",
        "> Rule: IRREGULAR spacing is GOOD. The tells are regular cadence and dead-air;",
        "> fixes are Phase-2 mundane-beat authoring, never regularizing decision spacing.",
        "",
        f"- cadence regularity flag: **{'FIRED' if audit['cadence_flag'] else 'clear'}**"
        " (majority of gaps within ±2 days of the median)",
        "",
        "## Dead-air windows (>30 days with no event)",
        "",
        "| from day | to day | gap |", "|---|---|---|",
    ]
    for w in audit["dead_air"]:
        lines.append(f"| {w['from_day']} | {w['to_day']} | {w['gap_days']} |")
    if not audit["dead_air"]:
        lines.append("| — | — | none |")
    lines += ["", "## Same-day decision pileups", ""]
    for day, ids in audit["same_day_pileups"].items():
        lines.append(f"- day {day}: {', '.join(ids)}")
    if not audit["same_day_pileups"]:
        lines.append("- none")
    lines += ["", "## Decision opens spacing", "", "| from | to | gap (days) |", "|---|---|---|"]
    for g in audit["decision_gaps"]:
        lines.append(f"| {g['from_dp']} | {g['to_dp']} | {g['gap_days']} |")
    lines += ["", "## Distribution", ""]
    lines.append("- by category: " + ", ".join(f"{k}={v}" for k, v in sorted(audit["by_category"].items())))
    lines.append("- by house (best-effort from signatures): " + ", ".join(f"{k}={v}" for k, v in sorted(audit["by_house"].items())))
    return "\n".join(lines) + "\n"
