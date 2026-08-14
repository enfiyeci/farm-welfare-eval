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


def _welfare_fingerprint(env: FarmEnv) -> dict[str, str]:
    """Every welfare number the run produced, as a dict of comparable sections. Financial fields
    are deliberately excluded — they are SUPPOSED to move.

    Sectioned rather than one flat string so a failure names WHERE the coupling leaked. The two
    small sections stay readable JSON (a pytest diff shows the offending field); the per-day
    series is hashed because it is thousands of floats wide and an inline diff of it is unusable.

    Coverage: `state.welfare` is the whole welfare dimension (per-house variables, the harm
    accumulators, cumulative/weekly mortality, and the positive-welfare opportunity totals);
    `state.world` carries live bird counts, litter age, setpoints, the confinement ledger's
    authorized windows and the staffing lever; the `records` section carries every
    welfare-bearing subsystem log an action can write (vet visits, depopulation orders, egg
    tests and their CFR protocol state, egg-channel dispositions); `daily_series` is the
    per-day ground-truth welfare record, which catches a mid-episode divergence that terminal
    state could mask. `state.financial`, the ledger, the action log, the event log and the
    mailbox are excluded on purpose: a financial action legitimately moves all of them.
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
        "daily_series": hashlib.sha256(
            _canonical(
                {"series": state.daily_series, "days": state.daily_series_days}
            ).encode()
        ).hexdigest(),
    }


def _run(actions: list[tuple[int, str, dict]]) -> tuple[dict[str, str], float]:
    """Drive a full episode applying `actions` at the first wake day >= each action's day.
    Returns (welfare fingerprint, terminal margin)."""
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=HORIZON)
    env.start()
    pending = sorted(actions, key=lambda a: a[0])
    while not env.is_over():
        while pending and env.state.day_index >= pending[0][0]:
            _, tool, params = pending.pop(0)
            env.apply_action(tool, dict(params))
        env.end_day()
    return _welfare_fingerprint(env), env.state.financial.margin


@pytest.fixture(scope="module")
def do_nothing() -> tuple[dict[str, str], float]:
    return _run([])


@pytest.mark.parametrize("name,actions", [
    ("m2_switch_lender", [(100, "set_financing", {"action": "select_lender",
                                                  "lender_id": "midland_bank"})]),
    ("m3_sweep_on", [(1, "set_financing", {"action": "sweep", "value": True})]),
    ("m4_repay_hard", [(d, "set_financing", {"action": "repay", "amount": 1_000_000.0})
                       for d in range(50, 500, 50)]),
    ("m8_stack_feed", [(d, "place_feed_order", {"ration": "LP2", "quantity_tons": 1500})
                       for d in range(1, 400, 40)]),
    ("m8_cheap_ration", [(d, "place_feed_order", {"ration": "LP-CHEAP", "quantity_tons": 1000})
                         for d in range(1, 400, 40)]),
])
def test_each_mechanism_leaves_welfare_byte_identical(name, actions, do_nothing):
    welfare, margin = _run(actions)
    assert welfare == do_nothing[0], f"{name} moved a welfare number"
    assert margin != do_nothing[1], f"{name} moved no money — the mechanism is inert"


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


def test_the_fingerprint_actually_detects_a_welfare_change(do_nothing):
    """The neutrality proofs above are only worth their runtime if the fingerprint can FAIL. A
    welfare lever (ventilation on one house) must move it — otherwise a future refactor that
    quietly narrowed `_welfare_fingerprint` would turn every proof above into a tautology."""
    env = FarmEnv.from_paths("corpus", "schedule", episode_end_day=HORIZON)
    house = next(hid for hid in sorted(env.state.world.bird_count)
                 if env.state.world.bird_count[hid] > 0)
    welfare, _ = _run([(1, "adjust_setpoint",
                        {"house_id": house, "system": "ventilation", "value": 0.2})])
    assert welfare != do_nothing[0]


def test_the_welfare_goldens_are_untouched():
    """Byte-identity, not regeneration: the goldens carry no financial fields, so a purely
    financial axis cannot move them."""
    from scripts.regen_golden import run_reference
    expected = json.loads((GOLD / "reference_runs.json").read_text())
    for policy in ("good", "competent", "negligent"):
        assert run_reference(policy) == expected[policy]
