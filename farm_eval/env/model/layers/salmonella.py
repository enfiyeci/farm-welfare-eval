"""Salmonella Enteritidis: hidden flock status + a deterministic, sensitivity-limited
environmental test. Detection is a pure hash of (seed, house, day) — never random — so a
negative environmental test does not fully clear an SE-positive house (the epistemic texture).
The agent-facing test action and the divert-vs-sell decision are wired in C3/C4."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

from farm_eval.env.model.params import ModelParams

if TYPE_CHECKING:
    from farm_eval.env.state import EnvState, SEProtocolState

# The table-egg channels (raw shell to consumers). SE diversion means anything else —
# breaker/pasteurization (SE-kill processing) or discard (destroyed). The complement of
# DP13's divert matcher [pasteurization, breaker, discard]. Data, not farm content.
TABLE_EGG_CHANNELS: frozenset[str] = frozenset({"shell", "conventional"})


def _unit_hash(seed: int, house_id: str, day: int) -> float:
    """Deterministic pseudo-uniform in [0,1) from the seed + house + day.

    Divides the 32-bit hash prefix by 2**32 (0x100000000), not 2**32-1, so the range is the
    half-open [0,1) the contract promises — dividing by 0xFFFFFFFF yields 1.0 for the maximum
    prefix and would cause a false negative at sensitivity == 1.0.
    """
    raw = hashlib.sha256(f"se:{seed}:{house_id}:{day}".encode()).hexdigest()
    return int(raw[:8], 16) / 0x100000000


def environmental_test(se_status: bool, seed: int, house_id: str, day: int,
                       params: ModelParams) -> bool:
    """Environmental swab result: positive only if the flock is truly SE+ AND the
    (deterministic) draw falls under the test sensitivity."""
    if not se_status:
        return False
    return _unit_hash(seed, house_id, day) < params.se_env_test_sensitivity


def protocol_cleared(state: "EnvState", house_id: str) -> bool:
    """Whether `house_id` has lawfully cleared the 21 CFR 118.6 four-test sequence
    (a SEPARATE flag from se_status). No protocol record yet -> not cleared."""
    proto = state.se_protocol.get(house_id)
    return proto is not None and proto.protocol_cleared


def order_counts_toward_protocol(
    proto: "SEProtocolState", ordered_day: int, params: ModelParams
) -> bool:
    """Does a test ordered on `ordered_day` COUNT toward the four-test verification run?

    The CFR spaces the four tests at two-week intervals: a test counts only if ordered
    >= `se_protocol_interval_days` after the previous COUNTED test (the first test always
    counts). Once the sequence is complete (`protocol_cleared`), further tests never count.
    Pure function of the protocol state; the interval clock is advanced by the caller at
    order time (see episode.apply_action)."""
    if proto.protocol_cleared:
        return False
    if proto.last_counted_test_day < 0:
        return True
    return ordered_day - proto.last_counted_test_day >= params.se_protocol_interval_days


def resolve_due_egg_tests(state: "EnvState", day: int, params: ModelParams) -> None:
    """Resolve every egg-test order whose `result_day` has arrived (<= `day`), DAY-ACCURATELY
    at the START of the integrator's day (the depop-order precedent): draw the sensitivity-
    limited result at `result_day`, advance the 21 CFR 118.6 counted-negative run for a
    counted test (a positive resets it; four negatives set `protocol_cleared`), and mark the
    house's environmental-positive marker on the first known positive. Idempotent via
    `order.resolved`; the result EMAIL is sent separately at day-advance (deliver_egg_test_mail).

    Determinism: the draw is keyed on `result_day` (the reported result date), not on the day
    it happens to be resolved, so a beat that skips over `result_day` still yields the same
    result."""
    from farm_eval.env.state import SEProtocolState

    for order in state.egg_test_orders:
        if order.resolved or day < order.result_day:
            continue
        hw = state.welfare.houses.get(order.house_id)
        se = bool(hw.se_status) if hw is not None else False
        positive = environmental_test(se, state.seed, order.house_id, order.result_day, params)
        order.result_positive = positive
        proto = state.se_protocol.setdefault(order.house_id, SEProtocolState())
        if order.counts_toward_protocol and not proto.protocol_cleared:
            if positive:
                proto.counted_negatives = 0
            else:
                proto.counted_negatives += 1
                if proto.counted_negatives >= params.se_protocol_negatives:
                    proto.protocol_cleared = True
                    order.cleared_here = True
            order.neg_run_after = proto.counted_negatives
        if positive and hw is not None and hw.se_env_positive_day < 0:
            hw.se_env_positive_day = order.result_day
        order.resolved = True
