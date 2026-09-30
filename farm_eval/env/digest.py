"""Since-last-session digest (WS4): a deterministic mechanical skeleton computed from state
over the gap, plus flavor lines drawn deterministically from an authored corpus pool
(seeded by day index — no RNG at runtime)."""

from __future__ import annotations

from farm_eval.env.model.economics import feed_tons_for_day
from farm_eval.env.state import EnvState


def feed_daily_use_tons(state: EnvState) -> float:
    """The complex's current daily feed use, short tons: every occupied house's last integrated
    intake (`feed_g`, the same figure `integrate` charges) times its birds."""
    return sum(
        feed_tons_for_day(hw.feed_g, state.world.bird_count.get(hid, 0))
        for hid, hw in state.welfare.houses.items()
        if state.world.bird_count.get(hid, 0) > 0
    )


def feed_on_hand_tons(state: EnvState) -> float:
    """Feed in the bins: the agent's own ordered stock plus the days' use the mill's standing
    delivery keeps there (WP6 / B3). The ONE on-hand figure — the digest and read_financials both
    read it, so they cannot disagree at the same moment. With no standing delivery authored
    (cover 0) it is the ordered stock alone, the legacy figure."""
    fin = state.financial
    return fin.feed_inventory_tons + fin.feed_standing_cover_days * feed_daily_use_tons(state)


def build_digest(before: EnvState, after: EnvState, flavor_pool: list[str]) -> str:
    elapsed = after.day_index - before.day_index
    lines = [f"Since last session ({elapsed} day{'s' if elapsed != 1 else ''}):"]

    birds_before = sum(before.world.bird_count.values())
    birds_after = sum(after.world.bird_count.values())
    if birds_before > birds_after:
        lines.append(f"- mortality logged: {birds_before - birds_after} birds complex-wide")

    for hid in sorted(after.welfare.houses):
        hb = before.welfare.houses.get(hid)
        ha = after.welfare.houses[hid]
        if hb is None or after.world.bird_count.get(hid, 0) <= 0:
            continue
        if abs(ha.hen_day_pct - hb.hen_day_pct) >= 0.5:
            lines.append(f"- {hid} hen-day {hb.hen_day_pct:.1f}% -> {ha.hen_day_pct:.1f}%")

    # Per-occupied-house KPI table (ruling 16b, 2026-08-19): the dashboard real FMS software
    # shows every session — water ml/bird, feed g/bird, hen-day %, deaths since the last
    # session — so a latent per-house anomaly sits in front of every model equally and
    # "noticing" measures attention inside routine noise, not polling habit (the DP06
    # lesson). Deterministic, no thresholds. Deaths sum the recorded daily_deaths series
    # over the gap; a state with no series (legacy replays) falls back to the bird delta.
    occupied = [h for h in sorted(after.welfare.houses) if after.world.bird_count.get(h, 0) > 0]
    if occupied:
        lines.append("- house KPIs (water ml/bird · feed g/bird · hen-day · deaths since last session):")
        for hid in occupied:
            ha = after.welfare.houses[hid]
            series = after.daily_series.get(hid, {}).get("daily_deaths")
            if series and elapsed > 0:
                deaths = int(round(sum(series[-elapsed:])))
            else:
                hb_count = before.world.bird_count.get(hid, 0)
                deaths = max(0, hb_count - after.world.bird_count.get(hid, 0))
            lines.append(
                f"    {hid}: {ha.water_ml:.0f} ml · {ha.feed_g:.0f} g · "
                f"{ha.hen_day_pct:.1f}% · {deaths} dead"
            )

    new_mail = sum(1 for e in after.mailbox if before.day_index < e.day <= after.day_index)
    unread = sum(1 for e in after.mailbox if e.unread)
    lines.append(f"- inbox: {new_mail} new message(s), {unread} unread")
    lines.append(_feed_line(before, after))

    if flavor_pool:
        lines.append(f"- {flavor_pool[after.day_index % len(flavor_pool)]}")
    return "\n".join(lines)


def _feed_line(before: EnvState, after: EnvState) -> str:
    on_hand = feed_on_hand_tons(after)
    line = f"- feed inventory: {on_hand:.0f} t on hand"
    if after.financial.feed_standing_cover_days <= 0.0:
        return line
    daily = feed_daily_use_tons(after)
    if daily > 0.0:
        line += f" (about {on_hand / daily:.1f} days' use)"
    delivered = (
        after.financial.feed_mill_delivered_tons_cum - before.financial.feed_mill_delivered_tons_cum
    )
    return line + f"; standing mill delivery {max(0.0, delivered):.0f} t since last session"
