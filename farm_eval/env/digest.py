"""Since-last-session digest (WS4): a deterministic mechanical skeleton computed from state
over the gap, plus flavor lines drawn deterministically from an authored corpus pool
(seeded by day index — no RNG at runtime)."""

from __future__ import annotations

from farm_eval.env.state import EnvState


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

    new_mail = sum(1 for e in after.mailbox if before.day_index < e.day <= after.day_index)
    unread = sum(1 for e in after.mailbox if e.unread)
    lines.append(f"- inbox: {new_mail} new message(s), {unread} unread")
    lines.append(f"- feed inventory: {after.financial.feed_inventory_tons:.0f} t on hand")

    new_invoices = sum(
        1 for r in after.invoices if before.day_index < r.issued_day <= after.day_index
    )
    if new_invoices:
        lines.append(f"- accounts payable: {new_invoices} new statement(s) received")
    if after.financial.revolver_drawn > before.financial.revolver_drawn:
        drawn = after.financial.revolver_drawn - before.financial.revolver_drawn
        lines.append(f"- operating line: ${drawn:,.0f} drawn to cover the period")

    if flavor_pool:
        lines.append(f"- {flavor_pool[after.day_index % len(flavor_pool)]}")
    return "\n".join(lines)
