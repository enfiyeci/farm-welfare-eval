"""Since-last-session digest (WS4): a deterministic mechanical skeleton computed from state
over the gap, plus flavor lines drawn deterministically from an authored corpus pool
(seeded by day index — no RNG at runtime)."""

from __future__ import annotations

import hashlib

from farm_eval.env.clock import weekday_name, weekday_of
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


def feed_days_to_next_delivery(state: EnvState) -> int | None:
    """Whole days from today to the mill's next standing drop (0 = due today), or None with no
    cadence authored. Drops land in the afternoon (the mill's mail: "Thursday morning instead of
    afternoon" is the exception), after the console opens, so today's drop is still to come."""
    days = state.financial.feed_delivery_weekdays
    if not days:
        return None
    today = weekday_of(state.start_date, state.day_index)
    return min((d - today) % 7 for d in days)


def _drop_overshoot_days(state: EnvState, drop_day: int) -> float:
    """What the drop on `drop_day` left above its target, in days' use: a drop is whole
    truckloads, so it overshoots by a different fraction of a load each time. Deterministic in
    the drop's day index (a hash, like mail timestamps), uniform in [0, spread)."""
    spread = state.financial.feed_reserve_spread_days
    if spread <= 0.0:
        return 0.0
    h = int(hashlib.sha256(f"feed-drop:{drop_day}".encode("utf-8")).hexdigest()[:8], 16)
    return spread * h / 0x1_0000_0000


def feed_bin_cover_days(state: EnvState) -> float:
    """Days' use the standing delivery has in the bins right now (WP6b): each drop fills them to
    carry the flocks to the next drop plus the reserve (and its truckload overshoot), so the
    cover falls a day each day through the gap and is back at the top the day after a drop.
    0 with no cadence authored."""
    to_next = feed_days_to_next_delivery(state)
    if to_next is None:
        return 0.0
    today = weekday_of(state.start_date, state.day_index)
    # The drop the bins are running on: today's has not come yet, so it is 1-7 days back.
    since_last = min((today - d - 1) % 7 + 1 for d in state.financial.feed_delivery_weekdays)
    overshoot = _drop_overshoot_days(state, state.day_index - since_last)
    return state.financial.feed_reserve_days + overshoot + to_next


def feed_on_hand_tons(state: EnvState) -> float:
    """Feed in the bins: the agent's own ordered stock plus what the mill's standing delivery
    has there (WP6 / B3). The ONE on-hand figure — the digest and read_financials both read it,
    so they cannot disagree at the same moment. With no standing delivery authored it is the
    ordered stock alone, the legacy figure."""
    return state.financial.feed_inventory_tons + feed_bin_cover_days(state) * feed_daily_use_tons(state)


def feed_next_delivery_day(state: EnvState) -> int | None:
    """Day index of the next standing drop (today if it is due today), or None."""
    to_next = feed_days_to_next_delivery(state)
    return None if to_next is None else state.day_index + to_next


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
    lines.append(_feed_line(after))

    if flavor_pool:
        lines.append(f"- {flavor_pool[after.day_index % len(flavor_pool)]}")
    return "\n".join(lines)


def _feed_line(after: EnvState) -> str:
    on_hand = feed_on_hand_tons(after)
    line = f"- feed inventory: {on_hand:.0f} t on hand"
    to_next = feed_days_to_next_delivery(after)
    daily = feed_daily_use_tons(after)
    if to_next is None or daily <= 0.0:
        return line
    line += f" (about {on_hand / daily:.1f} days' use)"
    if to_next == 0:
        return line + "; mill delivery due this afternoon"
    return line + f"; next mill delivery {weekday_name(weekday_of(after.start_date, after.day_index + to_next))}"
