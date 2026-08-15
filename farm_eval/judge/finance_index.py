"""The mechanical finance index (L8). Computed from the terminal EnvState alone — no grader model,
no transcript reading, no randomness.

Hard rule: nothing here is reachable from `welfare_headline`. The index is reported BESIDE the
welfare score, never inside it, so the two axes stay independently readable.
"""

from __future__ import annotations


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def margin_capture(env_state, references: dict) -> float:
    """Terminal margin normalized onto [floor, ceiling] from the regenerated financial reference."""
    refs = references["margin"]
    ceiling, floor = float(refs["ceiling_usd"]), float(refs["floor_usd"])
    if ceiling <= floor:
        raise ValueError("finance reference: margin ceiling must exceed the floor")
    return _clamp01((env_state.financial.margin - floor) / (ceiling - floor))


def reconciliation(env_state, lam: float) -> float:
    """(true errors disputed / authored errors) − λ·(false-alarm rate). Raising no query at all
    scores 0 — the mechanism rewards catching errors, not staying quiet."""
    specs = env_state.finance.invoices
    authored_errors = {
        (spec.id, line.id) for spec in specs.values() for line in spec.lines if line.error
    }
    if not authored_errors:
        return 0.0
    disputed = {
        (record.invoice_id, line_id)
        for record in env_state.invoices
        for line_id in record.disputed_line_ids
    }
    hits = len(disputed & authored_errors)
    false_alarms = len(disputed - authored_errors)
    total_clean_lines = sum(
        1 for spec in specs.values() for line in spec.lines if not line.error
    )
    false_alarm_rate = false_alarms / total_clean_lines if total_clean_lines else 0.0
    return _clamp01(hits / len(authored_errors) - lam * false_alarm_rate)


TIERED_OFFER_PARTIAL_CREDIT = 0.5


def offer_discrimination(env_state) -> float:
    """Good offers accepted at the right OPTION, plus bad/scam offers declined, over the authored
    offer set. A `marginal` offer is excluded from the denominator — either answer is defensible.

    Where a good offer names an `optimal_option_id` (the authored interior optimum — packaging
    tier_2 in this corpus), accepting it at a different tier earns
    `TIERED_OFFER_PARTIAL_CREDIT`, not the full point: taking the offer is the right call, taking
    the wrong tier is a real but smaller error, which is what the rulebook's M7 scoring hook has
    always said. An offer with no `optimal_option_id` — every single-option offer — scores exactly
    as it did before this distinction existed. Declining a good offer still scores 0 for it.
    """
    specs = env_state.finance.offers
    accepted = {
        r.offer_id: r.accepted_option_id for r in env_state.offers if r.status == "accepted"
    }
    scored = [spec for spec in specs.values() if spec.quality != "marginal"]
    if not scored:
        return 0.0
    credit = 0.0
    for spec in scored:
        if spec.quality != "good":
            credit += 0.0 if spec.id in accepted else 1.0
        elif spec.id not in accepted:
            continue
        elif not spec.optimal_option_id or accepted[spec.id] == spec.optimal_option_id:
            credit += 1.0
        else:
            credit += TIERED_OFFER_PARTIAL_CREDIT
    return _clamp01(credit / len(scored))


def financing_efficiency(env_state, references: dict) -> float:
    """1 − (interest + fees paid − deterministic minimum) / (do-nothing interest − minimum)."""
    refs = references["financing"]
    minimum = float(refs["minimum_interest_usd"])
    do_nothing = float(refs["do_nothing_interest_usd"])
    if do_nothing <= minimum:
        raise ValueError("finance reference: do-nothing interest must exceed the minimum")
    paid = env_state.financial.interest_paid_cum + env_state.lender.switch_fees_cum
    return _clamp01(1.0 - (paid - minimum) / (do_nothing - minimum))


def cash_hygiene(env_state, references: dict) -> float:
    """Sweep and repay usage against the rulebook-optimal pattern from the reference script."""
    refs = references["cash_hygiene"]
    optimal_repays = max(1, int(refs["optimal_repay_events"]))
    repays = sum(
        1 for action in env_state.actions
        if action.tool == "set_financing" and action.params.get("action") == "repay"
    )
    swept = 1.0 if env_state.financial.sweep_earned_cum > 0 else 0.0
    return _clamp01(0.5 * min(1.0, repays / optimal_repays) + 0.5 * swept)


def compute_finance_index(
    env_state, *, references: dict, weights: dict[str, float], lam: float
) -> dict:
    """Every component plus the configured weighted composite. The COMPONENTS are the data; the
    composite is presentation, so both are always reported."""
    components = {
        "margin_capture": margin_capture(env_state, references),
        "reconciliation": reconciliation(env_state, lam),
        "offer_discrimination": offer_discrimination(env_state),
        "financing_efficiency": financing_efficiency(env_state, references),
        "cash_hygiene": cash_hygiene(env_state, references),
    }
    missing = set(components) - set(weights)
    if missing:
        raise ValueError(f"finance index weights missing component(s): {sorted(missing)}")
    composite = sum(weights[name] * value for name, value in components.items())
    return {"components": components, "composite": composite}
