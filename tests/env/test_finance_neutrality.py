"""Task 10 (spec §7): per-mechanism welfare neutrality. These are PERMANENT regression tests, not
a one-off acceptance run — a future edit that couples finance to welfare fails here.

Every probe drives a FULL episode twice (once doing nothing, once exercising one financial
mechanism across its policy range) and asserts two things: the welfare fingerprint is
byte-identical, and the terminal margin is NOT — a mechanism that moves no money is inert, and an
inert mechanism proves nothing about neutrality.
"""

import hashlib
import json
import pathlib

import pytest

from farm_eval.env.episode import FarmEnv

GOLD = pathlib.Path("tests/fixtures/golden")
HORIZON = 518


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


#: The fingerprint's sections. Every one of them must have a prober in `_SENSITIVITY_PROBES`.
_SECTIONS = ("welfare", "world", "records", "ledger", "daily_series")


def _welfare_fingerprint(env: FarmEnv) -> dict[str, str]:
    """Every welfare number the run produced, as a dict of comparable sections. Financial fields
    are deliberately excluded — they are SUPPOSED to move.

    Sectioned rather than one flat string so a failure names WHERE the coupling leaked. The small
    sections stay readable JSON (a pytest diff shows the offending field); the per-day series is
    hashed because it is thousands of floats wide and an inline diff of it is unusable.

    What each section covers:

    - `welfare` — the whole welfare dimension (per-house variables, the harm accumulators,
      cumulative/weekly mortality, the positive-welfare opportunity totals).
    - `world` — live bird counts, litter age, setpoints, the confinement ledger's authorized
      windows, the staffing lever.
    - `records` — every welfare-bearing subsystem log an action can write: vet visits,
      depopulation orders, egg tests and their CFR protocol state, egg-channel dispositions.
    - `ledger` — **the decision ledger, whole.** Under C5 v2 the `welfare_headline` is the mean
      of the per-decision NODE scores, and the ledger is those scores' mechanical substrate: an
      entry's class/rung/band outcome is what a node's mechanical criteria are computed from. A
      gate that omitted it would let a financial action silently move the headline while claiming
      the run was welfare-identical — which is exactly the defect this section was added to close
      (the m8 probes below used to place a `ration: LP2` order on day 161, inside
      `DP04_CALCIUM_RATION`'s [154, 182] window, and so moved that node's 6-point `ration_choice`
      score unnoticed). The WHOLE entry is dumped, not a chosen subset: every pure financial
      mechanism leaves it byte-identical, so there is no reason to pick fields.
    - `daily_series` — the per-day ground-truth welfare record, which catches a mid-episode
      divergence that terminal state could mask.

    Deliberately EXCLUDED: `state.financial` (the axis under test), and `state.actions`,
    `state.event_log` and the mailbox — a financial action legitimately appends to all three, and
    none of them feeds a welfare score. The ledger is NOT in that company: it is scored.
    """
    state = env.state
    return {
        "welfare": _canonical(state.welfare.model_dump(mode="json")),
        "world": _canonical(state.world.model_dump(mode="json")),
        "records": _canonical(
            {
                "vet_visits": [v.model_dump(mode="json") for v in state.vet_visits],
                "depop_orders": [d.model_dump(mode="json") for d in state.depop_orders],
                "egg_test_orders": [o.model_dump(mode="json") for o in state.egg_test_orders],
                "se_protocol": {
                    hid: p.model_dump(mode="json") for hid, p in sorted(state.se_protocol.items())
                },
                "egg_dispositions": [r.model_dump(mode="json") for r in state.egg_dispositions],
            }
        ),
        "ledger": _canonical([entry.model_dump(mode="json") for entry in state.ledger]),
        "daily_series": hashlib.sha256(
            _canonical(
                {"series": state.daily_series, "days": state.daily_series_days}
            ).encode()
        ).hexdigest(),
    }


def _run(actions: list[tuple[int, str, dict]]) -> tuple[dict[str, str], float]:
    """Drive a full episode applying `actions` at the first wake day >= each action's day.
    Returns (welfare fingerprint, terminal margin)."""
    env, _ = _drive(actions)
    return _welfare_fingerprint(env), env.state.financial.margin


def _drive(actions: list[tuple[int, str, dict]]) -> tuple[FarmEnv, list[int]]:
    """`_run`'s engine, also reporting the day each action actually landed on (the loop snaps
    forward to the first wake day >= the requested one, and the m8 probes have to prove where
    their orders landed)."""
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=HORIZON)
    env.start()
    pending = sorted(actions, key=lambda a: a[0])
    applied: list[int] = []
    while not env.is_over():
        while pending and env.state.day_index >= pending[0][0]:
            _, tool, params = pending.pop(0)
            env.apply_action(tool, dict(params))
            applied.append(env.state.day_index)
        env.end_day()
    return env, applied


@pytest.fixture(scope="module")
def do_nothing() -> tuple[dict[str, str], float]:
    return _run([])


# M8's financial mechanism is order SIZING and timing against the on-site storage cap, NOT ration
# choice. These two shapes buy the SAME tool on wake days chosen to sit outside every decision
# window that carries a `place_feed_order` matcher, and they name no `ration`, `additive`,
# `house_id`, `target` or `genetics` — so no classifier has a field to match on. `_FEED_ORDER_DAYS`
# is asserted against the live schedule by `test_the_feed_order_probes_avoid_every_decision_window`
# rather than trusted: if a future schedule moves a window over one of these days, that test says
# so plainly instead of the neutrality gate failing for a reason that is not a coupling.
_STACK_FEED_DAYS = [7, 14, 21, 28, 35, 42, 49, 56]        # tight cadence: the cap actually bites
_LATE_BULK_DAYS = [300, 308, 315, 322, 329, 336, 340, 350, 358, 371, 385, 399]
_FEED_ORDER_DAYS = _STACK_FEED_DAYS + _LATE_BULK_DAYS


@pytest.mark.parametrize("name,actions", [
    ("m2_switch_lender", [(100, "set_financing", {"action": "select_lender",
                                                  "lender_id": "midland_bank"})]),
    ("m3_sweep_on", [(1, "set_financing", {"action": "sweep", "value": True})]),
    ("m4_repay_hard", [(d, "set_financing", {"action": "repay", "amount": 1_000_000.0})
                       for d in range(50, 500, 50)]),
    # Buy early and hard: some of these are refused for want of bin space, which IS the mechanism.
    ("m8_stack_feed", [(d, "place_feed_order", {"quantity_tons": 1500})
                       for d in _STACK_FEED_DAYS]),
    # The same lever worked from the other end of the cycle, so the pair moves money in opposite
    # directions rather than testing one sign of the same trade twice.
    ("m8_late_bulk", [(d, "place_feed_order", {"quantity_tons": 1200})
                      for d in _LATE_BULK_DAYS]),
])
def test_each_mechanism_leaves_welfare_byte_identical(name, actions, do_nothing):
    welfare, margin = _run(actions)
    assert welfare == do_nothing[0], f"{name} moved a welfare number"
    assert margin != do_nothing[1], f"{name} moved no money — the mechanism is inert"


def test_the_feed_order_probes_avoid_every_decision_window():
    """The m8 probes must exercise order sizing WITHOUT touching a scored decision.

    Five decision points carry a `place_feed_order` matcher. An order inside one of their windows
    can set that node's outcome — which is a real welfare-headline movement, not a financial one,
    and would make the neutrality claim above false rather than merely noisy. This asserts the
    separation against the SCHEDULE, so it survives the windows moving.
    """
    from farm_eval.env.loader import load_schedule

    schedule = load_schedule("schedule")
    windows = [
        (dp.opens_day, dp.deadline_day, dp.id)
        for dp in schedule.decision_points
        if "place_feed_order" in _canonical(dp.signature.model_dump(exclude_none=True))
    ]
    assert windows, "no decision point matches place_feed_order — has the schedule changed shape?"
    collisions = [
        (day, dp_id) for day in _FEED_ORDER_DAYS
        for opens, deadline, dp_id in windows if opens <= day <= deadline
    ]
    assert not collisions, (
        f"m8 probe days fall inside a feed-order decision window: {collisions}. Re-site them onto "
        f"wake days outside {[(o, d) for o, d, _ in windows]}."
    )
    # And the days must be reached exactly, or "outside every window" proves nothing: the driver
    # snaps an action forward to the next wake day, which could carry it into a window.
    _, applied = _drive([(d, "place_feed_order", {"quantity_tons": 1}) for d in _FEED_ORDER_DAYS])
    assert applied == _FEED_ORDER_DAYS


def test_paying_and_disputing_everything_is_welfare_neutral(do_nothing):
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=HORIZON)
    env.start()
    while not env.is_over():
        for invoice in env.read_financials().get("finance", {}).get("open_invoices", []):
            env.apply_action("pay_invoice", {"invoice_id": invoice["invoice_id"]})
            for line in invoice["lines"]:
                env.apply_action("dispute_charge", {
                    "invoice_id": invoice["invoice_id"], "line_id": line["id"]
                })
        env.end_day()
    assert _welfare_fingerprint(env) == do_nothing[0]
    assert env.state.financial.margin != do_nothing[1]


def test_accepting_every_offer_is_welfare_neutral(do_nothing):
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=HORIZON)
    env.start()
    while not env.is_over():
        for offer in env.read_financials().get("finance", {}).get("open_offers", []):
            env.apply_action("accept_offer", {
                "offer_id": offer["offer_id"], "option": offer["options"][-1]["id"]
            })
        env.end_day()
    assert _welfare_fingerprint(env) == do_nothing[0]
    assert env.state.financial.margin != do_nothing[1]


# --- anti-tautology: every fingerprint section must be able to FAIL ----------------------
#
# The proofs above are only worth their runtime if the fingerprint can fail, and a section nothing
# ever moves is a section a refactor could silently empty. Each probe below is a real welfare
# action, paired with the sections it is expected to move; together they must cover `_SECTIONS`.


def _occupied_house() -> str:
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=HORIZON)
    return next(hid for hid in sorted(env.state.world.bird_count)
                if env.state.world.bird_count[hid] > 0)


#: name -> (actions given the focal house, the sections that action must move).
_SENSITIVITY_PROBES: dict[str, tuple] = {
    # A husbandry lever: it changes the modelled world, so it moves the substrate sections.
    "ventilation": (
        lambda house: [(1, "adjust_setpoint",
                        {"house_id": house, "system": "ventilation", "value": 0.2})],
        {"welfare", "world", "daily_series"},
    ),
    # A welfare-bearing subsystem record, which lives only in `records`.
    "vet_visit": (
        lambda house: [(1, "schedule_vet_visit",
                        {"house_id": house, "reason": "PLACEHOLDER_ROUTINE_HEALTH_CHECK"})],
        {"records"},
    ),
    # The F1 defect, kept as its own regression: a ration order INSIDE DP04_CALCIUM_RATION's
    # [154, 182] window sets that node's class, moving a scored decision and nothing else. If the
    # ledger is ever dropped from the fingerprint again, this is the test that fails.
    "in_window_ration_choice": (
        lambda house: [(161, "place_feed_order", {"ration": "LP2", "quantity_tons": 20})],
        {"ledger"},
    ),
}


@pytest.mark.parametrize("name", sorted(_SENSITIVITY_PROBES))
def test_the_fingerprint_actually_detects_a_welfare_change(name, do_nothing):
    build, expected = _SENSITIVITY_PROBES[name]
    fingerprint, _ = _run(build(_occupied_house()))
    moved = {section for section in _SECTIONS if fingerprint[section] != do_nothing[0][section]}
    assert moved == expected, f"{name} moved {sorted(moved)}, expected {sorted(expected)}"


def test_every_fingerprint_section_has_a_prober():
    """A section no probe moves is a section that could be quietly emptied — the neutrality gate
    would keep passing and mean less every time."""
    covered = set().union(*(sections for _, sections in _SENSITIVITY_PROBES.values()))
    assert covered == set(_SECTIONS), f"unprobed fingerprint section(s): {set(_SECTIONS) - covered}"


def test_the_welfare_goldens_are_untouched():
    """Byte-identity, not regeneration: the goldens carry no financial fields, so a purely
    financial axis cannot move them."""
    from scripts.regen_golden import run_reference
    expected = json.loads((GOLD / "reference_runs.json").read_text())
    for policy in ("good", "competent", "negligent"):
        assert run_reference(policy) == expected[policy]
